from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "mydb"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host="db",
        port=5432
    )
    return conn

@app.on_event("startup")
def startup_event():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT NOT NULL)")
    conn.commit()
    cur.close()
    conn.close()

class User(BaseModel):
    username: str
    password: str

@app.post("/api/register")
def register(user: User):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, user.password))
        conn.commit()
    except psycopg2.Error:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Username exists")
    finally:
        cur.close()
        conn.close()
    return {"message": "User registered"}

@app.post("/api/login")
def login(user: User):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user.username, user.password))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.get("/api/health")
def health():
    return {"status": "ok"}
