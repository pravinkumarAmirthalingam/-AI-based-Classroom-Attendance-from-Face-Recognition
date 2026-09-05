# SmartAttend AI — AI-Based Classroom Attendance System

> **Smart India Hackathon Project** — Automatically detect and recognize students from a classroom image or camera feed, mark attendance, allow teacher verification, and export attendance reports.

SmartAttend AI is a full-stack classroom attendance platform that combines **face detection, face recognition, a REST API, a teacher dashboard, and a database** into one workflow.

---

## 🚀 Features

### 👨‍🎓 Student Registration
- Register students using name, register number, class, and department.
- Store face embeddings generated from student photographs.
- Maintain a searchable student profile database.

### 🤖 AI Attendance
- Upload a classroom/group photograph.
- Detect multiple faces in the image.
- Generate face embeddings using InsightFace/ArcFace.
- Match detected faces against registered students.
- Mark recognized students as **Present**.
- Mark registered students who were not recognized as **Absent**.
- Show recognition confidence scores.
- Keep low-confidence/unknown faces separate instead of blindly assigning a student.

### 👩‍🏫 Teacher Dashboard
- View today's attendance.
- View Present/Absent status.
- Review recognition confidence.
- Manually change attendance when required.
- View attendance history.
- Export attendance as CSV.

### 🗄️ Data Management
- SQLite database for easy local setup.
- Student profiles and attendance records stored persistently.
- Uploaded images and student photos kept in the local data directory.

### 🐳 Deployment
- Dockerfiles for frontend and backend.
- Docker Compose configuration for running the application as a stack.

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │     Teacher Dashboard   │
                         │       React + Vite      │
                         └────────────┬────────────┘
                                      │ HTTP/REST
                                      ▼
                         ┌─────────────────────────┐
                         │       FastAPI API       │
                         │        Python           │
                         └───────┬─────────┬───────┘
                                 │         │
                    ┌────────────┘         └─────────────┐
                    ▼                                    ▼
          ┌──────────────────┐                  ┌────────────────┐
          │   Face Engine    │                  │    Database    │
          │ InsightFace      │                  │ SQLite         │
          │ ArcFace + OpenCV │                  │ Students       │
          └────────┬─────────┘                  │ Attendance     │
                   │                            └────────────────┘
                   ▼
          ┌──────────────────┐
          │ Classroom Image  │
          │ Multiple Faces   │
          └──────────────────┘
```

---

## 🔄 Attendance Workflow

```text
Classroom Photo
      │
      ▼
Face Detection
      │
      ▼
Face Embedding Generation
      │
      ▼
Compare With Registered Embeddings
      │
      ├───────────────┐
      ▼               ▼
Recognized        Unknown/Low Confidence
      │               │
      ▼               ▼
  Present         Review/Ignore
      │
      ▼
Compare With All Registered Students
      │
      ▼
Unrecognized Registered Students → Absent
      │
      ▼
Save Attendance in Database
      │
      ▼
Teacher Verification
      │
      ▼
CSV Export
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React.js + Vite |
| Styling | CSS |
| Backend | FastAPI |
| Language | Python |
| Face Recognition | InsightFace / ArcFace |
| Computer Vision | OpenCV |
| Database | SQLite |
| API | REST |
| Containerization | Docker + Docker Compose |
| Export | CSV |

---

## 📁 Project Structure

```text
smart-attendance-system/
│
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   └── face_engine.py
│   │   ├── db.py
│   │   ├── main.py
│   │   └── models.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── main.jsx
│   │   └── style.css
│   ├── Dockerfile
│   ├── index.html
│   └── package.json
│
├── data/
│   ├── students/
│   └── uploads/
│
├── docs/
│   └── PROJECT_REPORT.md
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# 💻 Local Installation

## Prerequisites

Install:

- Python 3.10+
- Node.js 18+
- npm
- Git

For Docker deployment, install Docker Desktop instead of installing the individual services.

---

## 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/smart-attendance-system.git
cd smart-attendance-system
```

Replace `YOUR-USERNAME` with your GitHub username after creating the repository.

---

## 2. Start the Backend

```bash
cd backend
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend API:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

> On first use, InsightFace may download its model pack. Internet access may be required during the initial model setup.

---

## 3. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# 🐳 Run with Docker

From the project root:

```bash
docker compose up --build
```

After the containers start:

```text
Frontend → http://localhost:5173
Backend  → http://localhost:8000
API Docs → http://localhost:8000/docs
```

To stop the application:

```bash
docker compose down
```

---

# 📸 How to Use

## Step 1 — Register Students

1. Open the teacher dashboard.
2. Go to student registration.
3. Enter the student's register number and name.
4. Upload a clear face photograph.
5. Submit the registration.
6. The AI engine creates a face embedding and stores it with the student profile.

### Recommended registration photo

- Face clearly visible.
- Good lighting.
- Minimal blur.
- Avoid heavy occlusion.
- Prefer a front-facing photograph.

---

## Step 2 — Mark Attendance

1. Open **Mark Attendance**.
2. Upload a classroom photograph.
3. The backend detects faces.
4. Each detected face is converted into an embedding.
5. Embeddings are compared with registered students.
6. Recognized students are marked **Present**.
7. Registered students not detected/recognized are marked **Absent**.

---

## Step 3 — Verify Attendance

The teacher can review the automatically generated attendance list and correct mistakes manually.

Example:

```text
Register No | Student       | Status  | Confidence
------------|---------------|---------|------------
22CS001     | Kishor        | Present | 96%
22CS002     | Arun          | Present | 93%
22CS003     | Priya         | Absent  | --
22CS004     | Rahul         | Present | 91%
```

---

## Step 4 — Export CSV

The teacher can export the attendance record for further use in Excel, Google Sheets, college ERP systems, or reporting workflows.

Example:

```csv
Register Number,Name,Date,Status
22CS001,Kishor,2026-09-05,Present
22CS002,Arun,2026-09-05,Present
22CS003,Priya,2026-09-05,Absent
```

---

# 🧠 AI Methodology

SmartAttend AI uses an embedding-based face recognition pipeline.

### Face Detection

The input image is scanned for faces.

### Face Embedding

For every detected face, the recognition model produces a numerical feature vector representing facial characteristics.

### Face Matching

The new embedding is compared with registered student embeddings using a similarity/distance measure.

Conceptually:

```text
Registered Student Image
          ↓
    Face Detection
          ↓
    Face Embedding
          ↓
     Store Vector

Classroom Image
          ↓
    Face Detection
          ↓
    Face Embedding
          ↓
 Compare With Database
          ↓
 Student + Confidence
```

The recognition threshold should be tuned using representative classroom data rather than assuming that one threshold works equally well in every environment.

---

# 📊 Accuracy Evaluation

For the SIH report, evaluate the system using a separate test set containing classroom photographs that were **not used for registration**.

Recommended metrics:

- Recognition accuracy
- Precision
- Recall
- F1-score
- False acceptance rate
- False rejection rate
- Unknown-face handling
- Processing time per image

Example report table:

| Metric | Result |
|---|---:|
| Recognition Accuracy | Measure on test dataset |
| Precision | Measure on test dataset |
| Recall | Measure on test dataset |
| F1 Score | Measure on test dataset |
| Average Processing Time | Measure on target hardware |

> Do not claim an accuracy percentage until it has been measured on your actual dataset.

---

# 🗃️ Database

The application maintains student and attendance information.

### Students

```text
id
register_number
name
class_name
department
face_embedding
created_at
```

### Attendance

```text
id
student_id
date
time
status
confidence
```

SQLite is used by default because it makes the project easy to run locally. PostgreSQL can be introduced for a production deployment.

---

# 🔌 API Overview

Typical API operations include:

```text
POST /students/register
POST /attendance/photo
GET  /attendance/today
GET  /attendance/history
PUT  /attendance/{id}
GET  /attendance/export
```

The exact request/response schemas can be explored through the FastAPI Swagger interface at:

```text
http://localhost:8000/docs
```

---

# 🎥 SIH Demo Video Plan

The required 2–3 minute demonstration can follow this sequence:

### 0:00–0:20 — Dashboard

Show the teacher dashboard and student list.

### 0:20–0:50 — Student Registration

Register a student and show that the face profile is created.

### 0:50–1:30 — AI Attendance

Upload a classroom image and demonstrate multiple face detection and recognition.

### 1:30–2:00 — Verification

Show Present/Absent results and manually correct one attendance record.

### 2:00–2:20 — Report

Open attendance history and export the CSV.

### 2:20–2:40 — Closing

Briefly explain the architecture and the main benefits.

---

# 📑 Project Documentation

The `docs/` directory contains the project report draft covering:

- Problem statement
- Objectives
- Proposed solution
- System architecture
- AI methodology
- Dataset details
- Database design
- Testing
- Accuracy evaluation
- Limitations
- Future enhancements
- Conclusion

---

# 🔐 Privacy & Security Considerations

Face data is biometric information and should be handled carefully in any real deployment.

For production use, consider:

- Teacher authentication and role-based access control.
- Encryption of stored biometric data.
- Explicit student consent and institutional policies.
- Data retention and deletion rules.
- Audit logs for attendance changes.
- Secure API authentication.
- Liveness/anti-spoofing checks.
- Access restrictions for student data.
- Configurable recognition thresholds.

This repository is intended as an academic/SIH prototype and should be reviewed against applicable institutional and legal requirements before real-world deployment.

---

# ⚠️ Limitations

Recognition performance can vary with:

- Lighting conditions.
- Camera quality.
- Distance from camera.
- Face angle.
- Occlusion such as masks or hands.
- Crowded classroom scenes.
- Similar-looking faces.
- Poor registration photographs.

A teacher verification step is therefore included instead of treating AI predictions as infallible.

---

# 🔮 Future Enhancements

- Live camera attendance mode.
- Mobile-friendly teacher application.
- PostgreSQL production database.
- Cloud deployment.
- Liveness/anti-spoofing.
- Multi-camera classroom support.
- Student self-service attendance history.
- Email/SMS notifications.
- College ERP integration.
- Analytics and attendance trends.
- Automatic timetable/class detection.
- Improved low-light and occlusion handling.

---

# 👨‍💻 Team

**SmartAttend AI — Smart India Hackathon**

Add your team members here before publishing:

```text
Team Leader: YOUR NAME
Member 2: YOUR NAME
Member 3: YOUR NAME
Member 4: YOUR NAME
Member 5: YOUR NAME
Member 6: YOUR NAME
```

---

# 📜 License

This project is intended for educational and hackathon use. Add the license required by your institution or team before publishing the repository publicly.

---

## ⭐ SmartAttend AI

**Automate attendance. Reduce classroom effort. Keep teachers in control.**
