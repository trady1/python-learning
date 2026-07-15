from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator
from jose import JWTError, jwt
from datetime import datetime, timedelta
import sqlite3
import bcrypt
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow(
    ) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


def get_db():
    conn = sqlite3.connect("mydb.sqlite")
    conn.row_factory = sqlite3.Row
    return conn


def setup_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


setup_db()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class RegisterRequest(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("username")
    @classmethod
    def username_length(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v


class ContactCreate(BaseModel):
    name: str
    phone: str

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v):
        if not v.isdigit():
            raise ValueError("Phone must contain only digits")
        if not (7 <= len(v) <= 15):
            raise ValueError("Phone must be 7-15 digits")
        return v


class ContactUpdate(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v):
        if not v.isdigit():
            raise ValueError("Phone must contain only digits")
        if not (7 <= len(v) <= 15):
            raise ValueError("Phone must be 7-15 digits")
        return v


@app.post("/register", status_code=201)
def register(body: RegisterRequest):
    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM users WHERE username = ?", (body.username,)
    ).fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed = hash_password(body.password)
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (body.username, hashed)
    )
    conn.commit()
    conn.close()
    return {"message": f"User '{body.username}' registered successfully"}


@app.post("/login")
@limiter.limit("5/minute")
def login(request: Request, form: OAuth2PasswordRequestForm = Depends()):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (form.username,)
    ).fetchone()
    conn.close()
    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password"
        )
    token = create_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/contacts")
def get_contacts(user: str = Depends(get_current_user)):
    conn = get_db()
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return {"contacts": [dict(c) for c in contacts]}


@app.get("/contacts/{id}")
def get_contact(id: int, user: str = Depends(get_current_user)):
    conn = get_db()
    contact = conn.execute(
        "SELECT * FROM contacts WHERE id = ?", (id,)
    ).fetchone()
    conn.close()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"contact": dict(contact)}


@app.post("/contacts", status_code=201)
def add_contact(body: ContactCreate, user: str = Depends(get_current_user)):
    conn = get_db()
    conn.execute(
        "INSERT INTO contacts (name, phone) VALUES (?, ?)", (body.name, body.phone)
    )
    conn.commit()
    conn.close()
    return {"message": "Contact added!", "name": body.name, "phone": body.phone}


@app.put("/contacts/{id}")
def update_contact(id: int, body: ContactUpdate, user: str = Depends(get_current_user)):
    conn = get_db()
    conn.execute(
        "UPDATE contacts SET phone = ? WHERE id = ?", (body.phone, id)
    )
    conn.commit()
    conn.close()
    return {"message": "Contact updated!", "id": id, "phone": body.phone}


@app.delete("/contacts/{id}")
def delete_contact(id: int, user: str = Depends(get_current_user)):
    conn = get_db()
    conn.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": f"Contact {id} deleted"}
