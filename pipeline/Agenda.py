import requests 
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os


#Criar sessão e base declarativa para utilizar os dados do env. 
DATABASE_URL = os.getenv("DATABASE_KEY")
# Criação do engine e sessão
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Definição do modelo de dados
class Agenda(Base):
    __tablename__ = "congresso_dados"
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    SiglaPartido = Column(String(100))
    uf = Column(String(100))

# Cria a tabela (se não existir)
Base.metadata.create_all(engine)

#Extração dos dados sobre os eventos da Câmara dos Deputados
def extrair():
    url = "https://dadosabertos.camara.leg.br/api/v2/eventos"
    requests.get(url)

#Organizar e utilizar somente os dados relevantes da agenda
def transformar(dados):
    eventos = []
    for evento in dados['dados']:
        info = {
            'id': evento['id'],
            'situação': evento['situacao'],
            'Data de Início': evento['dataHoraInicio'],
            'Data Fim': evento['dataHoraFim'],           
            'nome': evento['nome'],
            'Assunto': evento['descricao'],
            'tipo': evento['descricaoTipo'],
            'tipoOrgao': evento['tipoOrgao'],
            'nomePublicacao': evento['nomePublicacao'],   
            'Tema': evento['nomeResumido'],
            'local': evento['local'],
            'link': evento['uri']
        }
        eventos.append(info)
    return eventos


#Carregar os dados em um banco de dados utilizando SQL - PostgreSQL
def carregar(eventos):
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_KEY")
    with Session() as session:
        objetos = [
            Agenda(
                id=evento['id'],
                situacao=evento['situação'],
                data_inicio=evento['Data de Início'],
                data_fim=evento['Data Fim'],
                nome=evento['nome'],
                assunto=evento['Assunto'],
                tipo=evento['tipo'],
                tipo_orgao=evento['tipoOrgao'],
                nome_publicacao=evento['nomePublicacao'],
                tema=evento['Tema'],
                local=evento['local'],
                link=evento['link']
            )
            for evento in eventos
        ]
        session.add_all(objetos)
        session.commit()
        print("Dados salvos no PostgreSQL!")