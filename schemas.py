from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# --- Schemas para Jogador ---
class JogadorBase(BaseModel):
    nome: str
    posicao: str
    idade: int
    time_id: int

class JogadorCriar(JogadorBase):
    pass

class JogadorAtualizar(BaseModel):
    nome: Optional[str] = None
    posicao: Optional[str] = None
    idade: Optional[int] = None
    time_id: Optional[int] = None

class Jogador(JogadorBase):
    id: int

    class Config:
        orm_mode = True


# --- Schemas para Time ---
class TimeBase(BaseModel):
    nome: str
    pais: str

class TimeCriar(TimeBase):
    pass

class TimeAtualizar(BaseModel):
    nome: Optional[str] = None
    pais: Optional[str] = None

class Time(TimeBase):
    id: int
    jogadores: List[Jogador] = []  # Lista de jogadores no time

    class Config:
        orm_mode = True


# --- Schemas para Partida ---
class PartidaBase(BaseModel):
    time_casa_id: int
    time_fora_id: int
    data_partida: date
    gols_casa: int = 0
    gols_fora: int = 0

class PartidaCriar(PartidaBase):
    pass

class PartidaAtualizar(BaseModel):
    time_casa_id: Optional[int] = None
    time_fora_id: Optional[int] = None
    data_partida: Optional[date] = None
    gols_casa: Optional[int] = 0
    gols_fora: Optional[int] = 0

class Partida(PartidaBase):
    id: int

    class Config:
        orm_mode = True


# --- Schemas para Estatísticas ---
class EstatisticaBase(BaseModel):
    jogador_estatistica: int
    partida_estatistica: int
    gols: int = 0
    assistencias: int = 0
    cartoes_amarelos: int = 0
    cartoes_vermelhos: int = 0

class EstatisticaCriar(EstatisticaBase):
    pass

class EstatisticaAtualizar(BaseModel):
    gols: Optional[int] = None
    assistencias: Optional[int] = None
    cartoes_amarelos: Optional[int] = None
    cartoes_vermelhos: Optional[int] = None

class Estatistica(EstatisticaBase):
    id: int

    class Config:
        orm_mode = True


# --- Schema para Relatório ---
class Relatorio(BaseModel):
    total_jogadores: int
    total_times: int
    partidas_realizadas: int
    gols_totais: int
    assistencias_totais: int

    class Config:
        orm_mode = True
