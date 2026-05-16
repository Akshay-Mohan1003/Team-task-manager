from fastapi import APIRouter, Depends, Form, Request, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, User
from app.routes.auth import require_admin
from typing import Optional

router = APIRouter()

@router.post("/")
def create_project(request: Request, name: str = Form(...), description: Optional[str] = Form(None), db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    new_project = Project(name=name, description=description, owner_id=admin.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return {"message": "Project created successfully"}

@router.patch("/{project_id}/note")
def update_project_note(request: Request, project_id: str, note: str = Form(...), db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    project.pinned_note = note
    db.commit()
    return {"message": "Note updated"}
