========================================
🏥 DENTAL APPOINTMENT MANAGEMENT SYSTEM
========================================

It is a FastAPI-based web application that manages dental appointments, collects patient details, 
and provides an interactive web dashboard to view appointments. 
The system also supports audio recordings of conversations and transcript visualization.

----------------------------------------
📌 FEATURES:
----------------------------------------
- FastAPI Backend 🚀 - Manages API endpoints for appointment data.
- HTML Frontend 🎨 - Displays all appointments in a dynamic table.
- Live Auto-Refresh 🔄 - Updates data every 5 seconds without reloading.
- Expandable Transcripts 📜 - View detailed conversation transcripts.
- Audio Playback 🔊 - Listen to the recorded conversation.
- Appointment Status ✅❌ - Booked (🟢 Green) or Pending (🔴 Red).

----------------------------------------
📂 PROJECT STRUCTURE:
----------------------------------------
project_root/
│── main.py          # FastAPI backend
│── static/
│   ├── index.html     
│── requirements.txt # Dependencies
│── README.txt       # Documentation

----------------------------------------
🚀 SETUP & RUN:
----------------------------------------

1️⃣ INSTALL DEPENDENCIES:
-------------------------
First, create a virtual environment and install the required packages.

For Windows:
> python -m venv env
> env\Scripts\activate
> pip install -r requirements.txt

For macOS/Linux:
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt

2️⃣ RUN THE FASTAPI SERVER:
----------------------------
Start the FastAPI backend by running:

> python -m uvicorn main:app --reload


- The API will run on: http://127.0.0.1:8000/
- API documentation is available at: http://127.0.0.1:8000/docs

3️⃣ OPEN THE WEB INTERFACE:
----------------------------
- Open your browser and go to **http://127.0.0.1:8000/**
- You will see a dynamic table of all appointments.


----------------------------------------
🛠️ TECHNOLOGIES USED:
----------------------------------------
- Backend: FastAPI ⚡
- Frontend: HTML (Just for testing purpose)
- Audio Handling: Serves .wav or .mp3 recordings
