from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, crud, schemas
from database import SessionLocal, engine
from typing import List

# Criação das tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência para obter a sessão do banco de dados
def obter_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota raiz
@app.get("/")
def read_root():
    return {"mensagem": "Bem-vindo ao sistema de gerenciamento de times esportivos!"}


# --- Rotas Times ---
@app.post("/times/", response_model=schemas.Time)
def criar_time(time: schemas.TimeCriar, db: Session = Depends(obter_db)):
    return crud.criar_time(db, time)

@app.get("/times/", response_model=List[schemas.Time])
def listar_times(pular: int = 0, limite: int = 10, db: Session = Depends(obter_db)):
    return crud.listar_times(db, pular=pular, limite=limite)

@app.put("/times/{time_id}", response_model=schemas.Time)
def atualizar_time(time_id: int, time: schemas.TimeAtualizar, db: Session = Depends(obter_db)):
    return crud.atualizar_time(db, time_id, time)

@app.delete("/times/{time_id}")
def deletar_time(time_id: int, db: Session = Depends(obter_db)):
    return crud.deletar_time(db, time_id)

# --- Rotas Jogadores ---
@app.post("/jogadores/", response_model=schemas.Jogador)
def criar_jogador(jogador: schemas.JogadorCriar, db: Session = Depends(obter_db)):
    return crud.criar_jogador(db, jogador)

@app.get("/jogadores/", response_model=List[schemas.Jogador])
def listar_jogadores(pular: int = 0, limite: int = 10, db: Session = Depends(obter_db)):
    return crud.listar_jogadores(db, pular=pular, limite=limite)

@app.put("/jogadores/{jogador_id}", response_model=schemas.Jogador)
def atualizar_jogador(jogador_id: int, jogador: schemas.JogadorAtualizar, db: Session = Depends(obter_db)):
    return crud.atualizar_jogador(db, jogador_id, jogador)

@app.delete("/jogadores/{jogador_id}")
def deletar_jogador(jogador_id: int, db: Session = Depends(obter_db)):
    return crud.deletar_jogador(db, jogador_id)

# --- Rotas Partidas ---
@app.post("/partidas/", response_model=schemas.Partida)
def criar_partida(partida: schemas.PartidaCriar, db: Session = Depends(obter_db)):
    return crud.criar_partida(db, partida)

@app.get("/partidas/", response_model=List[schemas.Partida])
def listar_partidas(pular: int = 0, limite: int = 10, db: Session = Depends(obter_db)):
    return crud.listar_partidas(db, pular=pular, limite=limite)

@app.put("/partidas/{partida_id}", response_model=schemas.Partida)
def atualizar_partida(partida_id: int, partida: schemas.PartidaAtualizar, db: Session = Depends(obter_db)):
    return crud.atualizar_partida(db, partida_id, partida)

@app.delete("/partidas/{partida_id}")
def deletar_partida(partida_id: int, db: Session = Depends(obter_db)):
    return crud.deletar_partida(db, partida_id)

# --- Rotas Estatísticas ---
@app.post("/estatisticas/", response_model=schemas.Estatistica)
def criar_estatistica(estatistica: schemas.EstatisticaCriar, db: Session = Depends(obter_db)):
    return crud.criar_estatistica(db, estatistica)

@app.get("/estatisticas/", response_model=List[schemas.Estatistica])
def listar_estatisticas(pular: int = 0, limite: int = 10, db: Session = Depends(obter_db)):
    return crud.listar_estatisticas(db, pular=pular, limite=limite)

@app.put("/estatisticas/{estatistica_id}", response_model=schemas.Estatistica)
def atualizar_estatistica(estatistica_id: int, estatistica: schemas.EstatisticaAtualizar, db: Session = Depends(obter_db)):
    return crud.atualizar_estatistica(db, estatistica_id, estatistica)

@app.delete("/estatisticas/{estatistica_id}")
def deletar_estatistica(estatistica_id: int, db: Session = Depends(obter_db)):
    return crud.deletar_estatistica(db, estatistica_id)

# --- Relatórios Estatísticos com Pandas ---
@app.get("/relatorio-jogadores/", response_model=List[schemas.RelatorioJogador])
def obter_relatorio_jogadores(db: Session = Depends(obter_db)):
    return crud.gerar_relatorio_jogadores(db)

@app.get("/relatorio-times/", response_model=List[schemas.RelatorioTime])
def obter_relatorio_times(db: Session = Depends(obter_db)):
    return crud.gerar_relatorio_times(db)