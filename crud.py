from datetime import date
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas
from fastapi import HTTPException

# --- Validações Genéricas ---
def validar_existencia(db: Session, model, model_id: int, nome_modelo: str):
    db_objeto = db.query(model).filter(model.id == model_id).first()
    if not db_objeto:
        raise HTTPException(status_code=404, detail=f"{nome_modelo} com ID {model_id} não encontrado.")
    return db_objeto

# --- CRUD Jogadores ---
def criar_jogador(db: Session, jogador: schemas.JogadorCriar):
    db_jogador = models.Jogador(**jogador.dict())
    try:
        db.add(db_jogador)
        db.commit()
        db.refresh(db_jogador)
        return db_jogador
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Jogador já cadastrado.")

def listar_jogadores(db: Session, pular: int = 0, limite: int = 10):
    return db.query(models.Jogador).offset(pular).limit(limite).all()

def atualizar_jogador(db: Session, jogador_id: int, jogador: schemas.JogadorAtualizar):
    db_jogador = validar_existencia(db, models.Jogador, jogador_id, "Jogador")
    for chave, valor in jogador.dict(exclude_unset=True).items():
        setattr(db_jogador, chave, valor)
    db.commit()
    db.refresh(db_jogador)
    return db_jogador 

def deletar_jogador(db: Session, jogador_id: int):
    db_jogador = validar_existencia(db, models.Jogador, jogador_id, "Jogador")
    db.delete(db_jogador)
    db.commit()
    return {"mensagem": "Jogador deletado com sucesso"}

# --- CRUD Times ---
def criar_time(db: Session, time: schemas.TimeCriar):
    db_time = models.Time(**time.dict())
    try:
        db.add(db_time)
        db.commit()
        db.refresh(db_time)
        return db_time
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Time já cadastrado.")

def listar_times(db: Session, pular: int = 0, limite: int = 10):
    return db.query(models.Time).offset(pular).limit(limite).all()

def atualizar_time(db: Session, time_id: int, time: schemas.TimeAtualizar):
    db_time = validar_existencia(db, models.Time, time_id, "Time")
    for chave, valor in time.dict(exclude_unset=True).items():
        setattr(db_time, chave, valor)
    db.commit()
    db.refresh(db_time)
    return db_time

def deletar_time(db: Session, time_id: int):
    db_time = validar_existencia(db, models.Time, time_id, "Time")
    db.delete(db_time)
    db.commit()
    return {"mensagem": "Time deletado com sucesso"}

# --- CRUD Partidas ---
def criar_partida(db: Session, partida: schemas.PartidaCriar):
    time_casa = validar_existencia(db, models.Time, partida.time_casa_id, "Time")
    time_visitante = validar_existencia(db, models.Time, partida.time_visitante_id, "Time")
    if partida.data < date.today():
        raise HTTPException(status_code=400, detail="Não é possível criar uma partida no passado.")
    db_partida = models.Partida(**partida.dict())
    try:
        db.add(db_partida)
        db.commit()
        db.refresh(db_partida)
        return db_partida
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Partida já cadastrada.")

def listar_partidas(db: Session, pular: int = 0, limite: int = 10):
    return db.query(models.Partida).offset(pular).limit(limite).all()

def atualizar_partida(db: Session, partida_id: int, partida: schemas.PartidaAtualizar):
    db_partida = validar_existencia(db, models.Partida, partida_id, "Partida")
    if partida.data and partida.data < date.today():
        raise HTTPException(status_code=400, detail="Não é possível definir uma partida no passado.")
    for chave, valor in partida.dict(exclude_unset=True).items():
        setattr(db_partida, chave, valor)
    db.commit()
    db.refresh(db_partida)
    return db_partida

def deletar_partida(db: Session, partida_id: int):
    db_partida = validar_existencia(db, models.Partida, partida_id, "Partida")
    db.delete(db_partida)
    db.commit()
    return {"mensagem": "Partida deletada com sucesso"}
