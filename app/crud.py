from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    from .auth import verify_password
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_issues(db: Session, status: str | None = None, priority: str | None = None):
    query = db.query(models.Issue)
    if status:
        query = query.filter(models.Issue.status == status)
    if priority:
        query = query.filter(models.Issue.priority == priority)
    return query.order_by(models.Issue.created_at.desc()).all()


def get_issue(db: Session, issue_id: int):
    return db.query(models.Issue).filter(models.Issue.id == issue_id).first()


def create_issue(db: Session, issue: schemas.IssueCreate):
    db_issue = models.Issue(
        title=issue.title,
        description=issue.description,
        priority=issue.priority,
        status=models.IssueStatus.abierto,
    )
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def update_issue(db: Session, issue_id: int, issue_update: schemas.IssueUpdate):
    db_issue = get_issue(db, issue_id)
    if not db_issue:
        return None
    if issue_update.status is not None:
        db_issue.status = issue_update.status
    if issue_update.priority is not None:
        db_issue.priority = issue_update.priority
    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_summary(db: Session):
    total = db.query(func.count(models.Issue.id)).scalar() or 0
    abierto = db.query(func.count(models.Issue.id)).filter(models.Issue.status == models.IssueStatus.abierto).scalar() or 0
    en_progreso = db.query(func.count(models.Issue.id)).filter(models.Issue.status == models.IssueStatus.en_progreso).scalar() or 0
    completado = db.query(func.count(models.Issue.id)).filter(models.Issue.status == models.IssueStatus.completado).scalar() or 0
    return {
        "total": total,
        "abierto": abierto,
        "en_progreso": en_progreso,
        "completado": completado,
    }
