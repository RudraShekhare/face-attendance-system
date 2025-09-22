import cv2
import face_recognition
import pickle
import sqlite3
from datetime import datetime

# Paths
ENCODINGS_PATH = "../models/encodings.pkl"
DB_PATH = "../attendance.db"

# Load known encodings
print("[INFO] Loading encodings...")
with open(ENCODINGS_PATH, "rb") as f:
    data = pickle.load(f)

# Initialize database
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

    # Check if already marked today
    c.execute("SELECT * FROM attendance WHERE name=? AND date=?", (name, date))
    result = c.fetchone()
    if result is None:
        c.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
        conn.commit()
        print(f"[INFO] Attendance marked for {name} at {time}")
    conn.close()

# Initialize DB
init_db()

# Start webcam
print("[INFO] Starting video stream...")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations and encodings
    boxes = face_recognition.face_locations(rgb, model="hog")  # try "cnn" if you have GPU
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            matched_idxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matched_idxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

        names.append(name)

        # Mark attendance if recognized
        if name != "Unknown":
            mark_attendance(name)

    # Draw boxes + labels
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)

    cv2.imshow("Face Recognition Attendance", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
