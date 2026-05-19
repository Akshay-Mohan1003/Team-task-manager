from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routes import auth, tasks, projects
from app.models import User, Project, Task, StatusEnum
from app.routes.auth import get_current_user
from datetime import datetime
import app.models

app.models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Team Task Manager")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="base.html", context={"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        user = get_current_user(request, db)
    except Exception:
        return RedirectResponse(url="/", status_code=303)
    
    projects_list = db.query(Project).all()
    tasks_list = db.query(Task).all()
    users_list = db.query(User).all()

    # Calculate Telemetry Metrics
    tasks_in_progress = sum(1 for t in tasks_list if t.status == StatusEnum.IN_PROGRESS)
    tasks_done = sum(1 for t in tasks_list if t.status == StatusEnum.DONE)
    total_tasks = len(tasks_list)
    
    compute_load_raw = 75 + (tasks_in_progress * 2.3)
    compute_load = round(min(compute_load_raw, 98.2), 1)
    
    pipeline_throughput = round(total_tasks * 1.2, 1)
    
    degraded_jobs = 0
    now_str = datetime.utcnow().strftime("%Y-%m-%d")
    for t in tasks_list:
        if t.status != StatusEnum.DONE and t.due_date and t.due_date < now_str:
            degraded_jobs += 1

    telemetry = {
        "compute_load": compute_load,
        "pipeline_throughput": pipeline_throughput,
        "human_in_loop": tasks_in_progress,
        "autonomous_runs": tasks_done,
        "degraded_jobs": degraded_jobs
    }

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html", 
        context={
            "request": request, 
            "user": user, 
            "projects": projects_list, 
            "tasks": tasks_list,
            "users": users_list,
            "telemetry": telemetry
        }
    )

@app.get("/projects/new")
def project_provisioner(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="project_provisioner.html", context={"request": request, "user": user})

@app.get("/projects/{project_id}")
def project_workspace(request: Request, project_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    users_list = db.query(User).all()
    return templates.TemplateResponse(request=request, name="project_workspace.html", context={"request": request, "user": user, "project": project, "users": users_list})

@app.get("/projects/{project_id}/members/add")
def operator_provisioner(request: Request, project_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    return templates.TemplateResponse(request=request, name="operator_provisioner.html", context={"request": request, "user": user, "project": project})

@app.get("/operators/{operator_id}")
def operator_profile(request: Request, operator_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    operator = db.query(User).filter(User.id == operator_id).first()
    all_projects = db.query(Project).all()
    return templates.TemplateResponse(request=request, name="operator_profile.html", context={"request": request, "user": user, "operator": operator, "all_projects": all_projects})
