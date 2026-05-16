from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Task, User, StatusEnum
from app.routes.auth import require_admin, get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/")
def create_task(title: str = Form(...), project_id: str = Form(...), assignee_id: str = Form(...), due_date: Optional[str] = Form(None), db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    new_task = Task(title=title, project_id=project_id, assignee_id=assignee_id, due_date=due_date)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created successfully"}

@router.patch("/{task_id}/status")
def update_task_status(request: Request, task_id: str, status: StatusEnum = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.assignee_id != current_user.id and current_user.role.value != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    task.status = status
    db.commit()
    db.refresh(task)
    
    return templates.TemplateResponse(
        request=request,
        name="partials/task_status.html", 
        context={"request": request, "task": task}
    )
