from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class Jogador(Base):
    __tablename__ = "jogadores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    posicao = Column(String)
    idade = Column(Integer)
    time_id = Column(Integer, ForeignKey("times.id"))

    # Relacionamento com time
    time = relationship("Time", back_populates="jogadores")
    # Relacionamento com Estatísticas
    estatisticas = relationship("Estatisticas", back_populates="jogador")

class Time(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    pais = Column(String, index=True)
    # Relacionamento com Jogadores
    jogadores = relationship("Jogador", back_populates="time")
    # Relacionamento com Partidas (como time da casa e fora)
    partidas_casa = relationship("Partida", foreign_keys='Partida.time_casa_id', back_populates="time_casa")
    partidas_fora = relationship("Partida", foreign_keys ='Partida.time_fora_id', back_populates="time_fora")

class Partida(Base):
    __tablename__= "partidas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_casa_id = Column(Integer, ForeignKey("times.id"))
    time_fora_id = Column(Integer, ForeignKey("times.id"))
    data_partida = Column(Date)
    gols_casa = Column(Integer, default=0)
    gols_fora = Column(Integer, default=0)
    # Relacionamentos com os Times
    time_casa = relationship("Time", foreign_keys=[time_casa_id], back_populates="partidas_casa")
    time_fora = relationship("Time", foreign_keys=[time_fora_id], back_populates="partidas_fora")
    # Relacionamento com Estatísticas
    estatisticas = relationship("Estatistica", back_populates="partida")

class Estatistica(Base):
    __tabelename__ = "estatisticas"

    id = Column(Integer, primary_key=True, index=True)
    jogador_estatistica = Column(Integer, ForeignKey("jogadores.id"))
    partida_estatistica = Column(Integer, ForeignKey("jogadores.id"))
    gols = Column(Integer, default=0)
    assistencias = Column(Integer, default=0)
    cartoes_amarelos = Column(Integer, default=0)
    cartoes_vermelhos = Column(Integer, default=0)

    jogador = relationship("Jogador")
    partida = relationship("Partida")