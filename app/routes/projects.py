from fastapi import APIRouter, Depends, Form, Request, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, User
from app.routes.auth import require_admin, verify_project_admin
from typing import Optional
from app.models import ProjectMember

router = APIRouter()

@router.post("/")
def create_project(request: Request, name: str = Form(...), description: Optional[str] = Form(None), db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    new_project = Project(name=name, description=description, owner_id=admin.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return {"message": "Project created successfully"}

@router.patch("/{project_id}/note")
def update_project_note(request: Request, project_id: str, note: str = Form(...), db: Session = Depends(get_db), current_user: User = Depends(verify_project_admin)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    project.pinned_note = note
    db.commit()
    return {"message": "Note updated"}

@router.post("/{project_id}/members")
def add_project_member(project_id: str, user_id: str = Form(...), db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if member already exists
    existing_member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id).first()
    if existing_member:
        return {"message": "User is already a member"}
        
    new_member = ProjectMember(project_id=project_id, user_id=user_id)
    db.add(new_member)
    db.commit()
    return {"message": "Member added successfully"}

@router.delete("/{project_id}/members/{user_id}")
def remove_project_member(project_id: str, user_id: str, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found in project")
    
    db.delete(member)
    db.commit()
    return {"message": "Member removed successfully"}
