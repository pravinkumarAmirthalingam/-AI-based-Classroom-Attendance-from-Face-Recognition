import csv, io, json
from datetime import date, datetime
from pathlib import Path
from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select
from .db import Base, engine, get_db
from .models import Student, Attendance
from .services.face_engine import FaceEngine

Base.metadata.create_all(bind=engine)
app=FastAPI(title='Smart Attendance API', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173','http://127.0.0.1:5173'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
engine_ai=FaceEngine()

@app.get('/api/health')
def health(): return {'status':'ok','face_engine':engine_ai.app is not None,'error':engine_ai.error}

@app.post('/api/students/register')
async def register_student(register_number: str=Form(...), name: str=Form(...), class_name: str=Form(''), department: str=Form(''), photo: UploadFile=File(...), db: Session=Depends(get_db)):
    if db.scalar(select(Student).where(Student.register_number==register_number)):
        raise HTTPException(409,'Register number already exists')
    data=await photo.read()
    try: emb=engine_ai.embedding_from_bytes(data)
    except Exception as e: raise HTTPException(400,str(e))
    s=Student(register_number=register_number,name=name,class_name=class_name,department=department,embedding=json.dumps(emb))
    db.add(s); db.commit(); db.refresh(s)
    return {'id':s.id,'message':'Student registered successfully'}

@app.get('/api/students')
def students(db: Session=Depends(get_db)):
    rows=db.scalars(select(Student).order_by(Student.register_number)).all()
    return [{'id':s.id,'register_number':s.register_number,'name':s.name,'class_name':s.class_name,'department':s.department} for s in rows]

@app.post('/api/attendance/photo')
async def mark_from_photo(photo: UploadFile=File(...), threshold: float=Form(0.42), db: Session=Depends(get_db)):
    known=[(s,json.loads(s.embedding)) for s in db.scalars(select(Student)).all()]
    if not known: raise HTTPException(400,'Register at least one student first')
    data=await photo.read()
    try: matches=engine_ai.recognize(data,known,threshold)
    except Exception as e: raise HTTPException(400,str(e))
    today=date.today(); present_ids=set(); out=[]
    for m in matches:
        if m['student_id'] and m['student_id'] not in present_ids:
            present_ids.add(m['student_id'])
            a=db.scalar(select(Attendance).where(Attendance.student_id==m['student_id'],Attendance.attendance_date==today))
            if not a:
                a=Attendance(student_id=m['student_id'],attendance_date=today,status='Present',confidence=m['confidence'],source='photo'); db.add(a)
            else: a.status='Present'; a.confidence=m['confidence']; a.source='photo'
        out.append(m)
    for s in known:
        if s[0].id not in present_ids:
            a=db.scalar(select(Attendance).where(Attendance.student_id==s[0].id,Attendance.attendance_date==today))
            if not a: db.add(Attendance(student_id=s[0].id,attendance_date=today,status='Absent',source='photo'))
    db.commit()
    return {'date':str(today),'detected':out,'present_count':len(present_ids),'total_students':len(known)}

@app.get('/api/attendance')
def attendance(day: date=date.today(), db: Session=Depends(get_db)):
    students=db.scalars(select(Student).order_by(Student.register_number)).all(); result=[]
    for s in students:
        a=db.scalar(select(Attendance).where(Attendance.student_id==s.id,Attendance.attendance_date==day))
        result.append({'id':a.id if a else None,'student_id':s.id,'register_number':s.register_number,'name':s.name,'status':a.status if a else 'Absent','confidence':a.confidence if a else None,'time':a.attendance_time.isoformat() if a else None})
    return {'date':str(day),'total':len(result),'present':sum(x['status']=='Present' for x in result),'absent':sum(x['status']!='Present' for x in result),'records':result}

@app.put('/api/attendance/{attendance_id}')
def update_attendance(attendance_id:int,status:str,db:Session=Depends(get_db)):
    if status not in ('Present','Absent'): raise HTTPException(400,'Status must be Present or Absent')
    a=db.get(Attendance,attendance_id)
    if not a: raise HTTPException(404,'Attendance record not found')
    a.status=status; db.commit(); return {'message':'Updated'}

@app.post('/api/attendance/manual/{student_id}')
def manual_attendance(student_id:int,status:str,day:date=date.today(),db:Session=Depends(get_db)):
    if status not in ('Present','Absent'): raise HTTPException(400,'Invalid status')
    if not db.get(Student,student_id): raise HTTPException(404,'Student not found')
    a=db.scalar(select(Attendance).where(Attendance.student_id==student_id,Attendance.attendance_date==day))
    if not a: a=Attendance(student_id=student_id,attendance_date=day,status=status,source='manual'); db.add(a)
    else: a.status=status; a.source='manual'
    db.commit(); return {'message':'Updated'}

@app.get('/api/attendance/export')
def export_csv(day:date=date.today(),db:Session=Depends(get_db)):
    data=attendance(day,db)['records']; stream=io.StringIO(); w=csv.writer(stream); w.writerow(['Register Number','Name','Date','Status','Confidence','Time'])
    for r in data: w.writerow([r['register_number'],r['name'],day,r['status'],r['confidence'] or '',r['time'] or ''])
    return StreamingResponse(iter([stream.getvalue()]),media_type='text/csv',headers={'Content-Disposition':f'attachment; filename=attendance_{day}.csv'})
