import requests
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from time import sleep
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_KEY")
# Criação do engine e sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Definição do modelo de dados
class CongressoDados(Base):
    __tablename__ = "congresso_dados"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    SiglaPartido = Column(String(100))
    uf = Column(String(100))

# Cria a tabela (se não existir)
Base.metadata.create_all(engine)

def extrair():
    # Faz uma requisição para a API da Câmara dos Deputados
    # e retorna os dados em formato JSON
    url = "https://dadosabertos.camara.leg.br/api/v2/deputados"
    response = requests.get(url)
    return response.json()

def transformar(dados):
    # Extrai os dados relevantes dos deputados
    # e retorna uma lista de dicionários com as informações necessárias
    deputados = []
    for deputado in dados['dados']:
        info = {
            'id': deputado['id'],
            'nome': deputado['nome'],
            'siglaPartido': deputado['siglaPartido'],
            'uf': deputado['siglaUf']
        }
        deputados.append(info)
    return deputados 

def carregar(deputados):
    # Aqui você pode implementar a lógica para carregar os dados em um banco de dados utilizando SQL
    with Session() as session:
        objetos = [
            CongressoDados(
                id=dep['id'],
                nome=dep['nome'],
                SiglaPartido=dep['siglaPartido'],
                uf=dep['uf']
            )
            for dep in deputados
        ]
        session.add_all(objetos)
        session.commit()
        print("Dados salvos no PostgreSQL!")


if __name__ == "__main__":
    while True:
        try:
            dados = extrair()
            deputados = transformar(dados)
            carregar(deputados)
            print("Dados atualizados com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar os dados: {e}")
    
     

     



    