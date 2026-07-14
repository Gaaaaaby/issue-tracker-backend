from fastapi import Depends, FastAPI, HTTPException, Security, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from .auth import create_access_token, decode_access_token, get_password_hash
from .config import ACCESS_TOKEN_EXPIRE_MINUTES

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Issue Tracker API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    username = payload["sub"]
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/issues", response_model=list[schemas.IssueOut])
def read_issues(
    status: models.IssueStatus | None = Query(None),
    priority: models.IssuePriority | None = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_issues(db, status=status, priority=priority)


@app.post("/issues", response_model=schemas.IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_issue(db, issue)


@app.patch("/issues/{issue_id}", response_model=schemas.IssueOut)
def update_issue(issue_id: int, issue_update: schemas.IssueUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    updated = crud.update_issue(db, issue_id, issue_update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incidencia no encontrada")
    return updated


@app.get("/summary", response_model=schemas.IssueSummary)
def get_summary(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_summary(db)


@app.on_event("startup")
def startup_data():
    db = SessionLocal()
    try:
        if crud.get_user_by_username(db, "admin") is None:
            admin = models.User(username="admin", hashed_password=get_password_hash("Admin123!"))
            db.add(admin)
        if crud.get_user_by_username(db, "user") is None:
            user = models.User(username="user", hashed_password=get_password_hash("User123!"))
            db.add(user)
        db.commit()
    finally:
        db.close()
