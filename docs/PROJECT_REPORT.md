# SmartAttend AI — Short Project Report

## 1. Problem Statement
Manual classroom roll calls consume teaching time and can introduce errors. SmartAttend AI automates attendance by detecting and recognizing registered students from classroom images, while retaining teacher verification.

## 2. Objective
Automatically detect faces, identify registered students, mark attendance, store attendance history, provide teacher correction, and export reports.

## 3. Architecture
Camera/upload → React dashboard → FastAPI REST API → InsightFace/ArcFace face detection + embeddings → similarity matching → SQLite attendance database → teacher dashboard/CSV.

## 4. Dataset
Registration images are collected from participating students with consent. Each student should have several varied images (front, slight left/right, different lighting) for robust evaluation. Do not use unconsented biometric data.

## 5. Recognition Method
InsightFace is used to detect faces and produce normalized face embeddings. Recognition uses cosine similarity (dot product for normalized vectors) against registered embeddings. A configurable threshold is applied; unmatched faces are labelled Unknown.

## 6. Attendance Logic
All registered students start as Absent for the selected date. Recognized students above the threshold are marked Present. Duplicate detections for the same student are collapsed. Teachers can manually correct records.

## 7. Evaluation
Report accuracy using a held-out test set and include: face detection rate, recognition accuracy, false acceptance rate, false rejection rate, and average processing time per classroom image. Do not claim an accuracy percentage until measured on your own dataset.

## 8. Limitations and Future Work
Current implementation is CPU-oriented and photo-first. Production improvements include live camera streaming, liveness/anti-spoofing, PostgreSQL, authentication, audit logs, threshold calibration, privacy controls, and larger real-classroom validation.
