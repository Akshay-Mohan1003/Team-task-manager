from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routes import auth, tasks, projects
from app.models import User, Project, Task
from app.routes.auth import get_current_user
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

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html", 
        context={
            "request": request, 
            "user": user, 
            "projects": projects_list, 
            "tasks": tasks_list,
            "users": users_list
        }
    )
