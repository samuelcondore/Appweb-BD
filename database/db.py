import enum
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime, Enum, Text, ForeignKey, null, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

DB_NAME = "cc3201"
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
    q = "SELECT C.* FROM public.carrera C WHERE 1=1"
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
    q = "SELECT COUNT(C.NOMB_CARRERA) FROM public.carrera C WHERE 1=1"
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

def get_distr_genero(inst):
    session = SessionLocal()
    q = "SELECT CASE a.GEN_ALU WHEN 1 THEN 'Masculino' WHEN 2 THEN 'Femenino' END AS genero, COUNT(*) AS total" 
    q += " FROM public.matricula m "
    q += " JOIN public.alumno a ON m.MRUN_A = a.MRUN"
    q += " JOIN public.institucion i ON m.NOMB_I = i.NOMB_INST"
    q += " WHERE i.TIPO_INST = :i"
    q += " GROUP BY a.GEN_ALU"
    q += " ORDER BY total DESC;"
    result = session.execute(text(q), {"i": inst}).all()
    session.close()
    return result

def total_over_30(min: int = 500, page: int = 0, page_size: int = 20):
    session = SessionLocal()
    q = "SELECT COUNT(MRUN_A) AS total_alumnos, NOMB_I, JORN"
    q += " FROM public.alumnodetalle"
    q += " WHERE ANIO_NAC_ALU <= 1995"
    q += " GROUP BY NOMB_I, JORN"
    q += " HAVING COUNT(MRUN_A) >= :m"
    q += " ORDER BY total_alumnos DESC, NOMB_I, JORN"
    q += " LIMIT :items OFFSET :page;"
    result = session.execute(text(q), {"m": min, "page": page*page_size, "items": page_size}).all()
    session.close()
    return result

def total_total_over_30(min: int = 500):
    session = SessionLocal()
    q = "SELECT COUNT(MRUN_A)"
    q += " FROM public.alumnodetalle"
    q += " WHERE ANIO_NAC_ALU <= 1995"
    q += " GROUP BY NOMB_I, JORN"
    q += " HAVING COUNT(MRUN_A) >= :m;"
    result = session.execute(text(q), {"m": min}).one()
    session.close()
    return result
