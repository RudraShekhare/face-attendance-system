import streamlit as st
import sqlite3
import pandas as pd
import cv2
import face_recognition
import pickle
from datetime import datetime
import numpy as np
import os

# Paths
DB_PATH = "../attendance.db"
ENCODINGS_PATH = "../models/encodings.pkl"
DATASET_DIR = "../dataset"

# Ensure dataset dir exists
os.makedirs(DATASET_DIR, exist_ok=True)

# Load encodings
def load_encodings():
    with open(ENCODINGS_PATH, "rb") as f:
        return pickle.load(f)

data = load_encodings()

# DB functions
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

def mark_attendance(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    c.execute("SELECT * FROM attendance WHERE name=? AND date=?", (name, date))
    result = c.fetchone()
    if result is None:
        c.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
        conn.commit()
        st.success(f"✅ Attendance marked for {name} at {time}")
    else:
        st.info(f"ℹ️ Attendance already marked for {name} today")
    conn.close()

init_db()

st.set_page_config(page_title="Face Attendance System", layout="wide")
st.title("📷 Face Recognition Attendance System")

# Sidebar for Admin
st.sidebar.header("🔑 Admin Panel")

# --- New Person Registration ---
st.sidebar.subheader("➕ Add New Person")
new_name = st.sidebar.text_input("Enter name of new person")
new_img = st.sidebar.camera_input("Capture face")

if new_name and new_img:
    # Save the captured image
    person_dir = os.path.join(DATASET_DIR, new_name)
    os.makedirs(person_dir, exist_ok=True)

    file_bytes = np.asarray(bytearray(new_img.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    img_path = os.path.join(person_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    cv2.imwrite(img_path, frame)
    st.sidebar.success(f"📸 Image saved for {new_name}")

    # --- Incremental encoding update ---
    if os.path.exists(ENCODINGS_PATH):
        # Load existing encodings
        with open(ENCODINGS_PATH, "rb") as f:
            data = pickle.load(f)
        known_encodings = data["encodings"]
        known_names = data["names"]
    else:
        known_encodings, known_names = [], []

    # Encode only this new person's folder
    for img in os.listdir(person_dir):
        image_path = os.path.join(person_dir, img)
        if not os.path.isfile(image_path):
            continue

        image = cv2.imread(image_path)
        if image is None:
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")  # "cnn" for accuracy
        encs = face_recognition.face_encodings(rgb, boxes)

        for enc in encs:
            known_encodings.append(enc)
            known_names.append(new_name)

    # Save updated encodings
    data = {"encodings": known_encodings, "names": known_names}
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)

    # Reload into memory immediately
    with open(ENCODINGS_PATH, "rb") as f:
        data = pickle.load(f)

    st.sidebar.success(f"✅ Encodings updated for {new_name}")


# --- Mark Attendance Section ---
st.subheader("📸 Mark Your Attendance")
img_file = st.camera_input("Take a picture")

if img_file is not None:
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb, model="cnn")  # more accurate
    encodings = face_recognition.face_encodings(rgb, boxes)

    if len(encodings) == 0:
        st.warning("⚠️ No face detected, try again with better lighting/position")

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.65)
        name = "Unknown"

        if True in matches:
            matched_idxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matched_idxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)

        if name != "Unknown":
            mark_attendance(name)
        else:
            st.error("❌ Face not recognized")
## --- View Attendance Logs ---
st.subheader("📊 Attendance Records")

# Always load DB into df
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM attendance", conn)
conn.close()

# Filters (work even before refresh)
if not df.empty:
    name_filter = st.selectbox("Filter by name", ["All"] + df["name"].unique().tolist(), key="name_filter")
    date_filter = st.date_input("Filter by date", key="date_filter")

    # Apply filters
    if name_filter != "All":
        df = df[df["name"] == name_filter]
    if date_filter:
        df = df[df["date"] == str(date_filter)]

else:
    st.info("ℹ️ No attendance records found yet.")
    name_filter, date_filter = None, None

# Refresh button
if st.button("🔄 Refresh Attendance Table"):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    conn.close()
    st.success("✅ Attendance table refreshed!")

# Show table
st.dataframe(df, use_container_width=True)

# Export CSV
if not df.empty:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Attendance CSV",
        csv,
        "attendance.csv",
        "text/csv",
        key="download_csv_main"
    )


    # Reset refresh so it only runs again when button clicked
    st.session_state["refresh"] = False


# Filters
name_filter = st.selectbox("Filter by name", ["All"] + df["name"].unique().tolist())
date_filter = st.date_input("Filter by date")

if name_filter != "All":
    df = df[df["name"] == name_filter]
if date_filter:
    df = df[df["date"] == str(date_filter)]

st.dataframe(df, use_container_width=True)

# Export CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Attendance CSV", csv, "attendance.csv", "text/csv")

# --- Admin Reset Option ---
if st.sidebar.button("🗑️ Clear Attendance Logs"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM attendance")
    conn.commit()
    conn.close()
    st.sidebar.warning("⚠️ All attendance logs cleared")
