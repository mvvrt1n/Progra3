from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Vuelo(Base):
    __tablename__ = 'vuelos'

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    tipo = Column(String)  # "emergencia" o "regular"
    estado = Column(String)  # "programado", "cancelado", "retrasado"

DATABASE_URL = "sqlite:///./vuelos.db"  # Configuración de base de datos SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
