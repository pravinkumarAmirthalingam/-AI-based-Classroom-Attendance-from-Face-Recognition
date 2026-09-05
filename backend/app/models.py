from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float, UniqueConstraint
from datetime import datetime, date
from .db import Base

class Student(Base):
    __tablename__='students'
    id=Column(Integer, primary_key=True)
    register_number=Column(String, unique=True, nullable=False, index=True)
    name=Column(String, nullable=False)
    class_name=Column(String, default='')
    department=Column(String, default='')
    embedding=Column(String, nullable=False)
    created_at=Column(DateTime, default=datetime.utcnow)

class Attendance(Base):
    __tablename__='attendance'
    id=Column(Integer, primary_key=True)
    student_id=Column(Integer, ForeignKey('students.id'), nullable=False)
    attendance_date=Column(Date, default=date.today, index=True)
    attendance_time=Column(DateTime, default=datetime.utcnow)
    status=Column(String, default='Present')
    confidence=Column(Float, nullable=True)
    source=Column(String, default='photo')
    __table_args__=(UniqueConstraint('student_id','attendance_date', name='uq_student_day'),)
