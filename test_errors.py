import sys
import traceback
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Project

client = TestClient(app)

resp = client.post("/api/auth/login", data={"email": "admin@ethara.ai", "password": "pass"})
print("Login:", resp.status_code)

resp = client.get("/dashboard")
print("Dashboard:", resp.status_code)
if resp.status_code == 500:
    print(resp.text)

db = SessionLocal()
p = db.query(Project).first()
if p:
    resp = client.get(f"/projects/{p.id}")
    print("Project Workspace:", resp.status_code)
    if resp.status_code == 500:
        print(resp.text)
