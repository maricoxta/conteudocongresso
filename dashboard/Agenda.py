import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# === CONFIGURAÇÕES ===
TEMAS = {
    'Meio Ambiente': ['meio ambiente', 'ambiental', 'floresta', 'biodiversidade', 'ecologia'],
    'Saneamento Básico': ['saneamento', 'água', 'esgoto', 'resíduos', 'abastecimento'],
    'Defesa Civil': ['defesa civil', 'desastre', 'emergência', 'inundações', 'chuva', 'alagamento']
}

# Configurações do banco de dados com valores padrão
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', '5432')
PG_DBNAME = os.getenv('PG_DBNAME', 'congresso_db')
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'senha123')

DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}"

# === EXTRAÇÃO ===
def extrair_camara(data_inicio):
    url = 'https://dadosabertos.camara.leg.br/api/v2/eventos'
    params = {
        'dataInicio': data_inicio.strftime('%Y-%m-%d'),
        'itens': 200,
        'ordem': 'DESC',
        'ordenarPor': 'dataHoraInicio'
    }
    response = requests.get(url, params=params)
    if response.ok:
        return response.json().get('dados', [])
    else:
        print("[ERRO] Falha na requisição da Câmara.")
        return []

def extrair_senado(data_inicio):
    url = 'https://legis.senado.leg.br/dadosabertos/eventos'
    params = {'dataInicio': data_inicio.strftime('%Y-%m-%d')}
    response = requests.get(url, params=params)
    if response.ok:
        return response.json().get('ListaEventos', {}).get('Evento', [])
    else:
        print("[ERRO] Falha na requisição do Senado.")
        return []

# === TRANSFORMAÇÃO ===
def classificar_tema(texto):
    texto = texto.lower()
    for tema, palavras in TEMAS.items():
        if any(p in texto for p in palavras):
            return tema
    return 'Outros'

def transformar_camara(eventos, orgao='camara'):
    registros = []
    for ev in eventos:
        tema = classificar_tema(ev.get("descricaoTipo", "") + ' ' + ev.get("assunto", ""))
        registros.append({
            "id": ev.get("idEvento"),
            "situacao": ev.get("situacao"),
            "data_inicio": ev.get("dataHoraInicio"),
            "data_fim": ev.get("dataHoraFim"),
            "nome": ev.get("descricaoTipo"),
            "assunto": ev.get("assunto", ""),
            "tipo": ev.get("tipoEvento"),
            "tipo_orgao": orgao,
            "nome_publicacao": ev.get("nomePublicacao", ""),
            "tema": tema,
            "local": ev.get("localCamara", ""),
            "link": ev.get("uri")
        })
    return pd.DataFrame(registros)

def transformar_senado(eventos):
    registros = []
    for ev in eventos:
        registros.append({
            'id': ev.get('idevento'),
            'situacao': ev.get('situacaoevento'),
            'data_inicio': ev.get('datahorainicio'),
            'data_fim': ev.get('datahorafim'),
            'nome': ev.get('tipoevento'),
            'assunto': ev.get('assuntoevento', ''),
            'tipo': ev.get('tipoevento'),
            'tipo_orgao': 'senado',
            'nome_publicacao': ev.get('nomepublicacao', ''),
            'tema': classificar_tema(ev.get('tipoevento', '') + ' ' + ev.get('assuntoevento', '')),
            'local': ev.get('localevento', ''),
            'link': ev.get('urlevento')
        })
    return pd.DataFrame(registros)

# === CARREGAMENTO ===
def carregar_postgres(df, tabela='eventos_congresso'):
    try:
        engine = create_engine(DATABASE_URL)
        df.to_sql(tabela, engine, if_exists='replace', index=False)
        print(f"[OK] Dados carregados no PostgreSQL na tabela '{tabela}'.")
    except Exception as e:
        print(f"[ERRO] Falha ao carregar dados no PostgreSQL: {e}")
        print("[INFO] Salvando dados em CSV como alternativa...")
        df.to_csv('eventos_congresso.csv', index=False)
        print("[OK] Dados salvos em eventos_congresso.csv")

# === DASHBOARD ===
def carregar_dataframe():
    """
    Retorna um DataFrame com os eventos da tabela 'eventos_congresso',
    renomeando as colunas para o formato esperado pelo dashboard.
    """
    try:
        engine = create_engine(DATABASE_URL)
        query = """
            SELECT
                nome AS "Título",
                data_inicio AS "Data e Hora Início",
                assunto AS "Assunto",
                local AS "Local",
                tema AS "Tema",
                link AS "Link"
            FROM eventos_congresso
        """
        df = pd.read_sql(query, engine)
        if 'Data e Hora Início' in df.columns:
            df['Data e Hora Início'] = pd.to_datetime(df['Data e Hora Início'])
        return df
    except Exception as e:
        print(f"[ERRO] Falha ao carregar dados do PostgreSQL: {e}")
        print("[INFO] Tentando carregar dados do CSV...")
        try:
            df = pd.read_csv('eventos_congresso.csv')
            # Renomear colunas para o formato esperado
            df = df.rename(columns={
                'nome': 'Título',
                'data_inicio': 'Data e Hora Início',
                'assunto': 'Assunto',
                'local': 'Local',
                'tema': 'Tema',
                'link': 'Link'
            })
            if 'Data e Hora Início' in df.columns:
                df['Data e Hora Início'] = pd.to_datetime(df['Data e Hora Início'])
            return df
        except Exception as csv_error:
            print(f"[ERRO] Falha ao carregar dados do CSV: {csv_error}")
            return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

# === PIPELINE ===
def run_pipeline(dias=7):
    data_inicio = datetime.now() - timedelta(days=dias)
    print(f"[INFO] Extraindo eventos desde {data_inicio.date()}...")

    raw_cam = extrair_camara(data_inicio)
    raw_sen = extrair_senado(data_inicio)

    print(f"[INFO] Transformando eventos...")
    df_cam = transformar_camara(raw_cam)
    df_sen = transformar_senado(raw_sen)

    df = pd.concat([df_cam, df_sen], ignore_index=True)
    df['data_inicio'] = pd.to_datetime(df['data_inicio'])
    df['data_fim'] = pd.to_datetime(df['data_fim'], errors='coerce')

    print(f"[INFO] Total de eventos processados: {len(df)}")
    carregar_postgres(df)

# === EXECUÇÃO ===
if __name__ == "__main__":
    run_pipeline()