from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.postgres import PostgresTools
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize PostgresTools with connection details
postgres_tools = PostgresTools (
    host=os.getenv("PG_HOST"),
    port=int(os.getenv("PG_PORT", 5432)),
    db_name=os.getenv("PG_DBNAME"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    table_schema=os.getenv("PG_SCHEMA", "public"),
)

# Create an agent with the PostgresTools
agent = Agent(tools=[postgres_tools],
              model=Groq(id="llama-3.3-70b-versatile"))

agent.print_response("Mostre todas as tabelas do banco de dados", markdown=True)

agent.print_response("""
Faça uma query para pegar todos os eventos que ocorrerem da Câmara de Deputados e do Senado Federal na semana inteira que envolvam assuntos das áreas de meio ambiente, saneamento e defesa civil.                    
                     
""")

agent.print_response("""
Faça uma análise super complexa sobre o bitcoin usando os dados da tabela bitcoin_dados
""")

print("PG_HOST:", os.getenv("PG_HOST"))
print("PG_DBNAME:", os.getenv("PG_DBNAME"))
print("PG_USER:", os.getenv("PG_USER"))
print("PG_PASSWORD:", os.getenv("PG_PASSWORD"))