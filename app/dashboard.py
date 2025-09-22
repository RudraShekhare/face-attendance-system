import streamlit as st
import sqlite3
import pandas as pd
import cv2
import numpy as np
import os
from datetime import datetime
from deepface import DeepFace

# Paths
DB_PATH = "attendance.db"       # ✅ local inside repo (works on cloud)
DATASET_DIR = "dataset"         # dataset folder

# Ensure dataset dir exists
os.makedirs(DATASET_DIR, exist_ok=True)

# --- DB functions ---
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

# Init DB
init_db()

# --- Streamlit UI ---
st.set_page_config(page_title="Face Attendance System", layout="wide")
st.title("📷 Face Recognition Attendance System")

# Sidebar Admin Panel
st.sidebar.header("🔑 Admin Panel")

# --- New Person Registration ---
st.sidebar.subheader("➕ Add New Person")
new_name = st.sidebar.text_input("Enter name of new person")
new_img = st.sidebar.camera_input("Capture face")

if new_name and new_img:
    person_dir = os.path.join(DATASET_DIR, new_name)
    os.makedirs(person_dir, exist_ok=True)

    image = Image.open(new_img)
    frame = np.array(image)  # still available as numpy for DeepFace
    img_path = os.path.join(person_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    image.save(img_path)
    st.sidebar.success(f"📸 Image saved for {new_name}")


# --- Mark Attendance Section ---
st.subheader("📸 Mark Your Attendance")
img_file = st.camera_input("Take a picture")

if img_file is not None:
    image = Image.open(img_file)
    frame = np.array(image)
    temp_img_path = "temp.jpg"
    image.save(temp_img_path)

    try:
        result = DeepFace.find(img_path=temp_img_path, db_path=DATASET_DIR, model_name="VGG-Face")

        if len(result) > 0 and not result[0].empty:
            identity = result[0].iloc[0]["identity"]
            name = os.path.basename(os.path.dirname(identity))
            mark_attendance(name)
        else:
            st.error("❌ Face not recognized")

    except Exception as e:
        st.error(f"⚠️ Recognition failed: {e}")

# --- View Attendance Logs ---
st.subheader("📊 Attendance Records")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM attendance", conn)
conn.close()

if not df.empty:
    name_filter = st.selectbox("Filter by name", ["All"] + df["name"].unique().tolist(), key="name_filter")
    date_filter = st.date_input("Filter by date", key="date_filter")

    if name_filter != "All":
        df = df[df["name"] == name_filter]
    if date_filter:
        df = df[df["date"] == str(date_filter)]

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Attendance CSV",
        csv,
        "attendance.csv",
        "text/csv",
        key="download_csv_main"
    )
else:
    st.info("ℹ️ No attendance records found yet.")

# --- Admin Reset Option ---
if st.sidebar.button("🗑️ Clear Attendance Logs"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM attendance")
    conn.commit()
    conn.close()
    st.sidebar.warning("⚠️ All attendance logs cleared")
