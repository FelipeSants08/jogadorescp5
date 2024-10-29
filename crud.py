from datetime import date
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas
from fastapi import HTTPException
import pandas as pd
from sqlalchemy import func

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
    time_fora = validar_existencia(db, models.Time, partida.time_fora_id, "Time")
    if partida.data_partida < date.today():
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
    if partida.data_partida and partida.data_partida < date.today():
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


def criar_estatistica(db: Session, estatistica: schemas.EstatisticaCriar):
    jogador = validar_existencia(db, models.Jogador, estatistica.jogador_estatistica, "Jogador")
    partida = validar_existencia(db, models.Partida, estatistica.partida_estatistica, "Partida")
    db_estatistica = models.Estatistica(**estatistica.dict())
    try:
        db.add(db_estatistica)
        db.commit()
        db.refresh(db_estatistica)
        return db_estatistica
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Estatística já cadastrada.")

def listar_estatisticas(db: Session, pular: int = 0, limite: int = 10):
    return db.query(models.Estatistica).offset(pular).limit(limite).all()

def atualizar_estatistica(db: Session, estatistica_id: int, estatistica: schemas.EstatisticaAtualizar):
    db_estatistica = validar_existencia(db, models.Estatistica, estatistica_id, "Estatística")
    for chave, valor in estatistica.dict(exclude_unset=True).items():
        setattr(db_estatistica, chave, valor)
    db.commit()
    db.refresh(db_estatistica)
    return db_estatistica

def deletar_estatistica(db: Session, estatistica_id: int):
    db_estatistica = validar_existencia(db, models.Estatistica, estatistica_id, "Estatística")
    db.delete(db_estatistica)
    db.commit()
    return {"mensagem": "Estatística deletada com sucesso"}

def gerar_relatorio_jogadores(db: Session):
    # Consulta para somar os gols, assistências, cartões amarelos e vermelhos de cada jogador
    resultado = (
        db.query(
            models.Estatistica.jogador_estatistica.label("jogador_id"),
            func.sum(models.Estatistica.gols).label("gols"),
            func.sum(models.Estatistica.assistencias).label("assistencias"),
            func.sum(models.Estatistica.cartoes_amarelos).label("cartoes_amarelos"),
            func.sum(models.Estatistica.cartoes_vermelhos).label("cartoes_vermelhos")
        )
        .group_by(models.Estatistica.jogador_estatistica)
        .all()
    )

    # Montando a resposta no formato do schema RelatorioJogador
    relatorio = []
    for item in resultado:
        jogador = db.query(models.Jogador).filter(models.Jogador.id == item.jogador_id).first()
        if jogador:
            relatorio.append(
                schemas.RelatorioJogador(
                    jogador_id=jogador.id,
                    nome=jogador.nome,
                    gols=item.gols,
                    assistencias=item.assistencias,
                    cartoes_amarelos=item.cartoes_amarelos,
                    cartoes_vermelhos=item.cartoes_vermelhos
                )
            )

    return relatorio

def gerar_relatorio_times(db: Session):
    # Consulta para somar os gols, assistências, cartões amarelos e vermelhos por time
    resultado = (
        db.query(
            models.Jogador.time_id.label("time_id"),
            func.sum(models.Estatistica.gols).label("gols"),
            func.sum(models.Estatistica.assistencias).label("assistencias"),
            func.sum(models.Estatistica.cartoes_amarelos).label("cartoes_amarelos"),
            func.sum(models.Estatistica.cartoes_vermelhos).label("cartoes_vermelhos")
        )
        .join(models.Jogador, models.Estatistica.jogador_estatistica == models.Jogador.id)
        .group_by(models.Jogador.time_id)
        .all()
    )

    # Montando a resposta no formato do schema RelatorioTime
    relatorio = []
    for item in resultado:
        time = db.query(models.Time).filter(models.Time.id == item.time_id).first()
        if time:
            relatorio.append(
                schemas.RelatorioTime(
                    time_id=time.id,
                    nome=time.nome,
                    gols=item.gols,
                    assistencias=item.assistencias,
                    cartoes_amarelos=item.cartoes_amarelos,
                    cartoes_vermelhos=item.cartoes_vermelhos
                )
            )

    return relatorio