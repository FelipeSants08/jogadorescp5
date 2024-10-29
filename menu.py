from fastapi import HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from datetime import datetime

# Funções auxiliares para o menu de Jogadores
def criar_jogador_menu(db: Session):
    nome = input("\nNome do jogador: ")
    idade = int(input("Idade do jogador: "))
    posicao = input("Posição do jogador: ")
    jogador_data = {"nome": nome, "idade": idade, "posicao": posicao}
    
    try:
        crud.criar_jogador(db, schemas.JogadorCriar(**jogador_data))
        print("\nJogador criado com sucesso!")
    except HTTPException as e:
        print(f"\nErro: {e.detail}")

def atualizar_jogador_menu(db: Session):
    jogador_id = int(input("\nID do jogador a ser atualizado: "))
    nome = input("Novo nome: ")
    idade = int(input("Nova idade: "))
    posicao = input("Nova posição: ")
    jogador_data = {"nome": nome, "idade": idade, "posicao": posicao}

    try:
        crud.atualizar_jogador(db, jogador_id, schemas.JogadorAtualizar(**jogador_data))
        print("\nJogador atualizado com sucesso!")
    except HTTPException as e:
        print(f"\nErro: {e.detail}")

def listar_jogadores_menu(db: Session):
    jogadores = crud.listar_jogadores(db)
    for jogador in jogadores:
        print(f"\nID: {jogador.id}, Nome: {jogador.nome}, Idade: {jogador.idade}, Posição: {jogador.posicao}")

def deletar_jogador_menu(db: Session):
    jogador_id = int(input("\nID do jogador a ser deletado: "))
    try:
        crud.deletar_jogador(db, jogador_id)
        print("\nJogador deletado com sucesso!")
    except HTTPException as e:
        print(f"\nErro: {e.detail}")

# Funções auxiliares para o menu de Times
def criar_time_menu(db: Session):
    nome = input("\nNome do time: ")
    pais = input("País do time: ")
    
    time_data = {
        "nome": nome,
        "pais": pais
    }
    
    try:
        crud.criar_time(db, schemas.TimeCriar(**time_data))
        print("\nTime criado com sucesso!")
    except HTTPException as e:
        print(f"\nErro: {e.detail}")

def atualizar_time_menu(db: Session):
    time_id = int(input("\nID do time a ser atualizado: "))
    nome = input("Novo nome do time: ")
    pais = input("Novo país do time: ")
    
    time_data = {
        "nome": nome,
        "pais": pais
    }
    
    try:
        crud.atualizar_time(db, time_id, schemas.TimeAtualizar(**time_data))
        print("\nTime atualizado com sucesso!")
    except HTTPException as e:
        print(f"\nErro: {e.detail}")

def listar_times_menu(db: Session):
    times = crud.listar_times(db)
    if times:
        for time in times:
            print(f"\nID: {time.id}, Nome: {time.nome}, País: {time.pais}")
    else:
        print("\nNenhum time cadastrado.")

def deletar_time_menu(db: Session):
    time_id = int(input("\nID do time a ser deletado: "))
    
    try:
        crud.deletar_time(db, time_id)
        print("\nTime deletado com sucesso!")
    except HTTPException as e:
        print(f"\nErro: {e.detail}")

# Funções auxiliares para o menu de Partidas
def criar_partida_menu(db: Session):
    time_casa_id = int(input("\nID do time da casa: "))
    time_visitante_id = int(input("ID do time visitante: "))
    data_str = input("Data da partida (AAAA-MM-DD): ")
    
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        print("Formato de data inválido. Tente novamente.")
        return
    
    placar_casa = int(input("Placar do time da casa: "))
    placar_visitante = int(input("Placar do time visitante: "))
    partida_data = {"time_casa_id": time_casa_id, "time_visitante_id": time_visitante_id, "data": data, "placar_casa": placar_casa, "placar_visitante": placar_visitante}
    
    try:
        crud.criar_partida(db, schemas.PartidaCriar(**partida_data))
        print("\nPartida criada com sucesso!")
    except HTTPException as e:
        print(f"\nErro: {e.detail}")

def listar_partidas_menu(db: Session):
    partidas = crud.listar_partidas(db)
    for partida in partidas:
        print(f"\nID: {partida.id}, Time Casa: {partida.time_casa.nome}, Time Visitante: {partida.time_visitante.nome}, Data: {partida.data}, Placar Casa: {partida.placar_casa}, Placar Visitante: {partida.placar_visitante}")

def deletar_partida_menu(db: Session):
    partida_id = int(input("\nID da partida a ser deletada: "))
    try:
        crud.deletar_partida(db, partida_id)
        print("\nPartida deletada com sucesso!")
    except HTTPException as e:
        print(f"\nErro: {e.detail}")

# Menu principal dos jogadores
def menu_jogadores(db: Session):
    while True:
        print("\n--- Menu de Jogadores ---")
        print("1. Criar Jogador")
        print("2. Listar Jogadores")
        print("3. Atualizar Jogador")
        print("4. Deletar Jogador")
        print("0. Voltar ao Menu Principal")
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            criar_jogador_menu(db)
        elif opcao == "2":
            listar_jogadores_menu(db)
        elif opcao == "3":
            atualizar_jogador_menu(db)
        elif opcao == "4":
            deletar_jogador_menu(db)
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida! Tente novamente.")

# Menu principal dos times
def menu_times(db: Session):
    while True:
        print("\n--- Menu de Times ---")
        print("1. Criar Time")
        print("2. Listar Times")
        print("3. Atualizar Time")
        print("4. Deletar Time")
        print("0. Voltar ao Menu Principal")
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            criar_time_menu(db)
        elif opcao == "2":
            listar_times_menu(db)
        elif opcao == "3":
            atualizar_time_menu(db)
        elif opcao == "4":
            deletar_time_menu(db)
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida! Tente novamente.")

# Menu principal das partidas
def menu_partidas(db: Session):
    while True:
        print("\n--- Menu de Partidas ---")
        print("1. Criar Partida")
        print("2. Listar Partidas")
        print("3. Deletar Partida")
        print("0. Voltar ao Menu Principal")
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            criar_partida_menu(db)
        elif opcao == "2":
            listar_partidas_menu(db)
        elif opcao == "3":
            deletar_partida_menu(db)
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida! Tente novamente.")

# Menu principal
def menu_principal(db: Session):
    while True:
        print("\n--- Menu Principal ---")
        print("1. Gerenciar Jogadores")
        print("2. Gerenciar Times")
        print("3. Gerenciar Partidas")
        print("0. Sair")
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            menu_jogadores(db)
        elif opcao == "2":
            menu_times(db)
        elif opcao == "3":
            menu_partidas(db)
        elif opcao == "0":
            print("\nSaindo do sistema.")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

# Conexão com o banco de dados
if __name__ == "__main__":
    db = database.SessionLocal()
    menu_principal(db)
