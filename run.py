import uvicorn
from app.db.init_db import init_db, create_initial_sources
from app.db.session import SessionLocal

def init():
    db = SessionLocal()
    try:
        init_db()
        create_initial_sources(db)
    finally:
        db.close()

if __name__ == "__main__":
    init()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 