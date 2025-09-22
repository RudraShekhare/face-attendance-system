📷 Face Recognition Attendance System

An AI-powered attendance system using Face Recognition + Streamlit Dashboard.
The app allows users to:

Register new people (via webcam snapshots).

Mark attendance by taking a picture.

Store logs in a SQLite database.

View and filter attendance records.

Export logs to CSV for reporting.

✨ Features

🔐 Face Recognition: Uses face_recognition library for encoding and matching.

📝 Attendance Logging: Stores attendance in SQLite (attendance.db).

📊 Streamlit Dashboard:

Mark attendance using webcam.

Admin panel to register new people.

View logs with filters (name/date).

Refresh table without restarting app.

Export records to CSV.

⚡ Incremental Encoding: New registrations don’t reprocess the entire dataset → faster updates.

🛠️ Tech Stack

Python 3.11

OpenCV – image handling

face_recognition – face embeddings & recognition

Streamlit – interactive dashboard

SQLite – lightweight attendance database

Pandas – data manipulation

📂 Project Structure
face-attendance-system/
│── app/
│   ├── dashboard.py        # Streamlit dashboard
│   ├── register.py         # Capture images for dataset
│   ├── encode_faces.py     # Encode dataset into encodings.pkl
│   ├── recognize_realtime.py # Real-time recognition with OpenCV
│── models/
│   ├── encodings.pkl       # Saved face encodings
│── attendance.db           # SQLite database (auto-created)
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation

⚡ Setup & Installation

Clone this repo and install requirements:

git clone https://github.com/your-username/face-attendance-system.git
cd face-attendance-system
pip install -r requirements.txt


Run the dashboard:

streamlit run app/dashboard.py

🎮 Usage
1. Register New Person

Open Admin Panel in the sidebar.

Enter person’s name + take 3–5 snapshots.

Encodings update automatically.

2. Mark Attendance

Click Take a picture in the main dashboard.

If recognized → attendance is logged in attendance.db.

3. View Records

Attendance table displays logs.

Filter by name and date.

Refresh table anytime.

Export logs as CSV.

🌐 Deployment

You can deploy this project on Streamlit Cloud:

Push to GitHub.

Go to Streamlit Cloud
.

Connect your repo → choose app/dashboard.py as entrypoint.

Done ✅

⚠️ Note: On Streamlit Cloud, attendance.db resets when app restarts.
For persistent storage, connect Google Sheets / PostgreSQL.

🚀 Future Improvements

Integrate cloud database for persistent logs.

Add email notifications on attendance.

Support for real-time video attendance (OpenCV live feed).

Role-based access for admin/users.

📜 License

This project is for educational purposes. Feel free to fork and extend.