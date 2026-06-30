import enum
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime, Enum, Text, ForeignKey, null, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DB_NAME = "hito3"
DB_USERNAME = "realwebuser"
DB_PASSWORD = "contrasena"
DB_HOST = "localhost"
DB_PORT = 5432
DATABASE_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---------- Funciones -------------

def free_search_carrera(query: str = "", jornada: str = "", modalidad: str = "", page: int = 0, page_size: int = 20, nivel: str = ""):
    session = SessionLocal()
    q = "SELECT C.* FROM carrera C WHERE 1=1"
    if query:
        q += " AND (C.NOMB_CARRERA LIKE :q OR C.NOMB_I LIKE :q OR C.NOMB_S LIKE :q)"
    if jornada:
        q += " AND  C.JORNADA = :j"
    if modalidad:
        q += " AND C.MODALIDAD = :m"
    if nivel:
        q += " AND C.NIVEL_CARRERA = :n"
    q += " ORDER BY C.NOMB_CARRERA DESC LIMIT :items OFFSET :page;"
    result = session.execute(text(q), {"q": f"%{query.upper()}%", "j": jornada, "m": modalidad, "page": page*page_size, "items": page_size, "n": nivel}).all()
    session.close()
    return result

def total_carreras(query, jornada, modalidad, nivel):
    session = SessionLocal()
    q = "SELECT COUNT(C.NOMB_CARRERA) FROM carrera C WHERE 1=1"
    if query:
        q += " AND (C.NOMB_CARRERA LIKE :q OR C.NOMB_I LIKE :q OR C.NOMB_S LIKE :q)"
    if jornada:
        q += " AND  C.JORNADA = :j"
    if modalidad:
        q += " AND C.MODALIDAD = :m"
    if nivel:
        q += " AND C.NIVEL_CARRERA = :n"
    q += " ;"
    result = session.execute(text(q), {"q": f"%{query.upper()}%", "j": jornada, "m": modalidad, "n": nivel}).one()
    session.close()
    return result
