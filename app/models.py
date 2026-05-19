import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum, JSON, DateTime
import datetime
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

class StatusEnum(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(RoleEnum), nullable=False, default=RoleEnum.MEMBER)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    projects_owned = relationship("Project", back_populates="owner")
    tasks_assigned = relationship("Task", back_populates="assignee")
    project_memberships = relationship("ProjectMember", back_populates="user", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(String)
    pinned_note = Column(String, nullable=True)
    owner_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="projects_owned")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    telemetry = relationship("PlatformTelemetry", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    status = Column(SQLEnum(StatusEnum), nullable=False, default=StatusEnum.TODO)
    due_date = Column(String)
    project_id = Column(String, ForeignKey("projects.id"))
    assignee_id = Column(String, ForeignKey("users.id"))
    task_type = Column(String(50), default="human_hitl")
    compute_estimated_tokens = Column(Integer, default=0)
    processing_logs = Column(JSON, default=list)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks_assigned")

class ProjectMember(Base):
    __tablename__ = "project_members"
    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False, default="Member") # 'Admin' or 'Member'

    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")

class PlatformTelemetry(Base):
    __tablename__ = "platform_telemetry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    log_level = Column(String(10), default="INFO")
    subsystem = Column(String(50), nullable=False) # 'MODEL_TRAINING', 'DATA_PIPELINE', 'VECTOR_DB'
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="telemetry")
