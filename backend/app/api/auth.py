from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.services.security import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/api/auth", tags=["authentication"])
bearer = HTTPBearer(auto_error=False)

class RegisterRequest(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=10, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required", headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired access token", headers={"WWW-Authenticate":"Bearer"})
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Account no longer exists")
    return user

def require_role(*roles):
    def guard(user: User = Depends(current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user
    return guard

def public_user(user):
    return {"id":user.id,"email":user.email,"display_name":user.display_name,"role":user.role,"created_at":user.created_at}

@router.post("/register", status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(email=email, display_name=payload.display_name.strip(), password_hash=hash_password(payload.password), role="learner")
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token":create_access_token(user.id,user.role),"token_type":"bearer","user":public_user(user)}

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"access_token":create_access_token(user.id,user.role),"token_type":"bearer","user":public_user(user)}

@router.get("/me")
def me(user: User = Depends(current_user)):
    return public_user(user)

@router.get("/users")
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_role("admin"))):
    return [public_user(user) for user in db.query(User).order_by(User.created_at.desc()).limit(200).all()]

class RoleUpdate(BaseModel):
    role: str = Field(pattern="^(learner|educator|admin)$")

@router.patch("/users/{user_id}/role")
def update_role(user_id: int, payload: RoleUpdate, db: Session = Depends(get_db), admin: User = Depends(require_role("admin"))):
    user = db.get(User, user_id)
    if not user: raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin.id and payload.role != "admin":
        raise HTTPException(status_code=400, detail="Administrators cannot demote their own account")
    user.role = payload.role; db.commit(); db.refresh(user)
    return public_user(user)

def optional_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)):
    if not credentials:
        return None
    try:
        payload=decode_access_token(credentials.credentials)
        user=db.get(User,int(payload["sub"]))
    except Exception:
        raise HTTPException(status_code=401,detail="Invalid or expired access token")
    if not user: raise HTTPException(status_code=401,detail="Account no longer exists")
    return user
