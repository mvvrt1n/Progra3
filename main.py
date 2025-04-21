from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from models import SessionLocal, Vuelo
from linked_list import ListaDoblementeEnlazada

app = FastAPI()

# Pydantic models
class VueloCreate(BaseModel):
    codigo: str
    tipo: str
    estado: str

class VueloResponse(BaseModel):
    id: int
    codigo: str
    tipo: str
    estado: str

    class Config:
        orm_mode = True

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Lista doblemente enlazada
lista = ListaDoblementeEnlazada()

def cargar_lista_desde_db(db: Session = Depends(get_db)):
    vuelos_db = db.query(Vuelo).all()
    for vuelo in vuelos_db:
        lista.insertar_al_final(vuelo)
    return lista

# POST /vuelos/ - Añadir un vuelo al final (normal) o al frente (emergencia)
@app.post("/vuelos/", response_model=VueloResponse)
def crear_vuelo(vuelo: VueloCreate, emergencia: bool = Query(False, description="Insertar al frente por emergencia"), db: Session = Depends(get_db)):
    db_vuelo = Vuelo(codigo=vuelo.codigo, tipo=vuelo.tipo, estado=vuelo.estado)
    db.add(db_vuelo)
    db.commit()
    db.refresh(db_vuelo)
    if emergencia:
        lista.insertar_al_frente(db_vuelo)
    else:
        lista.insertar_al_final(db_vuelo)
    return db_vuelo

# GET /vuelos/total - Retornar el número total de vuelos en la cola
@app.get("/vuelos/total")
def obtener_total_vuelos_en_cola(db: Session = Depends(get_db)):
    total_vuelos = db.query(Vuelo).count()  # Cuenta el número total de vuelos en la base de datos
    return {"total_vuelos": total_vuelos}

# GET /vuelos/proximo - Retornar el primer vuelo sin remover
@app.get("/vuelos/proximo", response_model=VueloResponse)
def obtener_primer_vuelo_en_cola():
    primer_vuelo = lista.obtener_primero()
    if not primer_vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos en la cola")
    return primer_vuelo

# GET /vuelos/ultimo - Retornar el último vuelo sin remover
@app.get("/vuelos/ultimo", response_model=VueloResponse)
def obtener_ultimo_vuelo_en_cola():
    ultimo_vuelo = lista.obtener_ultimo()
    if not ultimo_vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos en la cola")
    return ultimo_vuelo

# GET /vuelos/lista - Lista todos los vuelos en orden actual
@app.get("/vuelos/lista", response_model=List[VueloResponse])
def obtener_lista_de_vuelos():
    vuelos = lista.obtener_lista_ordenada()  # Asegúrate de que se está llamando al método correcto
    if not vuelos:
        raise HTTPException(status_code=404, detail="No hay vuelos en la lista")
    return vuelos


# PATCH /vuelos/reordenar - Reordena manualmente la cola
@app.patch("/vuelos/reordenar")
def reordenar_vuelos(nuevo_orden_ids: List[int]):
    try:
        lista.reordenar(nuevo_orden_ids)  # Llamamos al método reordenar
    except IndexError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Cola de vuelos reordenada"}


@app.delete("/vuelos/{vuelo_id}")
def eliminar_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    db_vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    if db_vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    db.delete(db_vuelo)
    db.commit()
    nodo_actual = lista.cabeza
    indice = 0
    while nodo_actual:
        if nodo_actual.vuelo.id == vuelo_id:
            lista.extraer_de_posicion(indice)
            break
        nodo_actual = nodo_actual.siguiente
        indice += 1
    return {"detail": "Vuelo eliminado"}

@app.get("/vuelos/", response_model=List[VueloResponse])
def obtener_todos_los_vuelos(db: Session = Depends(get_db)):
    vuelos = db.query(Vuelo).all()
    return vuelos
