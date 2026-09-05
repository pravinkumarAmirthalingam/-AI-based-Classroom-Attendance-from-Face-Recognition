# SmartAttend AI — AI-based Classroom Attendance

A complete starter implementation for the Smart India Hackathon requirement: register students with face embeddings, recognize multiple faces from a classroom image, automatically mark Present/Absent, let a teacher correct records, and export CSV.

## Stack
- React + Vite dashboard
- FastAPI backend
- SQLite (portable default; can be migrated to PostgreSQL)
- InsightFace / ArcFace embeddings + OpenCV
- Docker Compose

## Run locally
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
The first InsightFace initialization downloads its model pack when the environment permits it.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

### Docker
```bash
docker compose up --build
```

## Demo flow
1. Register 2–5 students using clear, front-facing photos.
2. Upload a classroom/group photo under Mark Attendance.
3. Review Present/Absent results.
4. Use teacher correction buttons if needed.
5. Export today's CSV.

## Important production notes
This prototype intentionally keeps face embeddings in the local database and uses CPU inference. For production, add authentication/RBAC, encrypted storage, PostgreSQL, audit logs, liveness/anti-spoofing, configurable recognition thresholds, consent/retention controls, and comprehensive validation under classroom lighting and occlusion conditions.
