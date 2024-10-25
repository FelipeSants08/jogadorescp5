import oracledb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Função para criar uma conexão com o banco de dados Oracle
def create_oracle_connection():
    dsn_str = oracledb.makedsn("oracle.fiap.com.br", 1521, "ORCL")
    con = oracledb.connect(
        user="rm558916",
        password="081105",
        dsn=dsn_str
    )
    return con

# Conexão com o banco de dados
base = create_oracle_connection()
print("Conexão com o banco de dados estabelecida com sucesso.")

# Criação do motor (engine)
DATABASE_URL = "oracle+oracledb://rm558916:081105@oracle.fiap.com.br:1521/ORCL"
engine = create_engine(DATABASE_URL)

# Definição de Base para uso com SQLAlchemy
Base = declarative_base()

# Criação da classe SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cursor para execução de comandos
cur = base.cursor()


cur.close()
base.close()
