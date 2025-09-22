# 📷 Face Recognition Attendance System

  An AI-powered attendance system using Face Recognition + Streamlit Dashboard.

    The app allows users to:
    ✅ Register new people (via webcam snapshots)
    ✅ Mark attendance by taking a picture
    ✅ Store logs in a SQLite database
    ✅ View and filter attendance records
    ✅ Export logs to CSV for reporting
    
---

## ✨ Features

- 🔐 Face Recognition: Uses face_recognition library for encoding and matching
- 📝 Attendance Logging: Stores attendance in SQLite (attendance.db)
- 📊 Streamlit Dashboard:
    Mark attendance using webcam
    Admin panel to register new people
- View logs with filters (name/date)
- Refresh table without restarting app
- Export records to CSV
- ⚡ Incremental Encoding: New registrations don’t reprocess the entire dataset → much faster

---


## 🛠️ Tech Stack

- 🐍 Python 3.11
- 🎥 OpenCV – image handling
- 😃 face_recognition – face embeddings & recognition

--- 


🌐 Streamlit – interactive dashboard

🗄️ SQLite – lightweight attendance database

📊 Pandas – data manipulation
