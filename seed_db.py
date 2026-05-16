import uuid
import bcrypt
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Project, Task, RoleEnum, StatusEnum
import os

print("Recreating database...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def hash_pw(pw):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print("Seeding users...")
admin = User(email="admin@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.ADMIN)
u1 = User(email="aaditya.rana@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.MEMBER)
u2 = User(email="abdus.samadint17@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.MEMBER)
u3 = User(email="jatin@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.MEMBER)
u4 = User(email="kush.ajmera@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.MEMBER)
u5 = User(email="adarsh.shuklaint17@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.MEMBER)
u6 = User(email="piyush.pal2004@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.MEMBER)
u7 = User(email="aakanksha.kaushal2829@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.MEMBER)
u8 = User(email="akshay.mohan1003@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.MEMBER)
u9 = User(email="anuj.mishra2005@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.MEMBER)
u10 = User(email="antriksh.singhint17@ethara.ai", hashed_password=hash_pw("pass"), role=RoleEnum.MEMBER)

db.add_all([admin, u1, u2, u3, u4, u5, u6, u7, u8, u9, u10])
db.commit()

print("Seeding projects...")
p1 = Project(name="Kensei", description="LLM Post Training Technical Project", pinned_note="Focus on instruction tuning and alignment pipelines.", owner_id=admin.id)
p2 = Project(name="Talos", description="Technical Platform Development", pinned_note="Odoo integration is the priority this week.", owner_id=admin.id)
db.add_all([p1, p2])
db.commit()

print("Seeding tasks...")
db.add(Task(title="Evaluate RLHF model on TruthfulQA", status=StatusEnum.TODO, project_id=p1.id, assignee_id=u1.id, due_date="2026-05-20"))
db.add(Task(title="Refactor Odoo modules", status=StatusEnum.IN_PROGRESS, project_id=p2.id, assignee_id=u3.id, due_date="2026-05-18"))
db.add(Task(title="Data pipeline optimization", status=StatusEnum.DONE, project_id=p2.id, assignee_id=u4.id, due_date="2026-05-15"))
db.add(Task(title="Setup distributed training cluster", status=StatusEnum.IN_PROGRESS, project_id=p1.id, assignee_id=u6.id, due_date="2026-05-22"))
db.add(Task(title="Build tokenization pipeline", status=StatusEnum.TODO, project_id=p1.id, assignee_id=u2.id, due_date="2026-05-25"))

db.commit()
print("Database seeded with dummy data successfully. All passwords are 'pass'.")
