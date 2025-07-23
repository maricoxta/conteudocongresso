# etl_congresso.py

import requests
import pandas as pd
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES 📌
TEMAS = {
    'Meio Ambiente': ['meio ambiente','ambiental','floresta','biodiversidade','ecologia'],
    'Saneamento Básico': ['saneamento','água','esgoto','resíduos','abastecimento'],
    'Defesa Civil': ['defesa civil','desastre','emergência','inundações','chuva','alagamento']
}

# 2. EXTRAÇÃO
def extrair_camara(data_inicio):
    url = 'https://dadosabertos.camara.leg.br/api/v2/eventos'
    params = {
        'dataInicio': data_inicio.strftime('%Y-%m-%d'),
        'itens': 200,
        'ordem': 'DESC',
        'ordenarPor': 'dataHoraInicio'
    }
    resp = requests.get(url, params=params)
    return resp.json().get('dados', [])

def extrair_senado(data_inicio):
    url = 'https://legis.senado.leg.br/dadosabertos/eventos'
    params = {'dataInicio': data_inicio.strftime('%Y-%m-%d')}
    resp = requests.get(url, params=params)
    return resp.json().get('ListaEventos', [])

# 3. TRANSFORMAÇÃO
def classificar_tema(texto):
    texto = texto.lower()
    for tema, palavras in TEMAS.items():
        if any(p in texto for p in palavras):
            return tema
    return 'Outros'

def transformar_eventos(raw, orgao):
    registros = []
    for ev in raw:
        if orgao == 'câmara':
            id_ev = ev.get('idEvento')
            situacao = ev.get('situacao')
            inicio = ev.get('dataHoraInicio')
            fim = ev.get('dataHoraFim')
            nome = ev.get('descricaoTipo')
            assunto = ev.get('assunto') or ''
            tipo = ev.get('tipoEvento')
            tipo_orgao = 'camara'
            nome_publicacao = ev.get('nomePublicacao') or ''
            local = ev.get('localCamara')
            link = ev.get('uri')
        else:  # senado
            id_ev = ev.get('idevento')
            situacao = ev.get('situacaoevento')
            inicio = ev.get('datahorainicio')
            fim = ev.get('datahorafim')
            nome = ev.get('tipoevento')
            assunto = ev.get('assuntoevento')
            tipo = ev.get('tipoevento')
            tipo_orgao = 'senado'
            nome_publicacao = ev.get('nomepublicacao')
            local = ev.get('localevento')
            link = ev.get('urlevento')
        tema = classificar_tema(nome + ' ' + assunto)
        registros.append({
            'id': id_ev,
            'situacao': situacao,
            'data_inicio': inicio,
            'data_fim': fim,
            'nome': nome,
            'assunto': assunto,
            'tipo': tipo,
            'tipo_orgao': tipo_orgao,
            'nome_publicacao': nome_publicacao,
            'tema': tema,
            'local': local,
            'link': link
        })
    return pd.DataFrame(registros)

# 4. CARREGAMENTO
def carregar_csv(df, caminho='relatorio_eventos.csv'):
    df.to_csv(caminho, index=False)
    print(f"[OK] Relatório salvo em {caminho} com {len(df)} linhas.")

# 5. PIPELINE PRINCIPAL
def run_pipeline(dias=7):
    data_inicio = datetime.now() - timedelta(days=dias)
    print(f"[INFO] Extraindo eventos desde {data_inicio.date()}...")

    raw_cam = extrair_camara(data_inicio)
    raw_sen = extrair_senado(data_inicio)

    print(f"[INFO] Transformando {len(raw_cam)} eventos da Câmara e {len(raw_sen)} do Senado...")
    df_cam = transformar_eventos(raw_cam, 'câmara')
    df_sen = transformar_eventos(raw_sen, 'senado')

    df = pd.concat([df_cam, df_sen], ignore_index=True)
    df['data_inicio'] = pd.to_datetime(df['data_inicio'])
    df['data_fim'] = pd.to_datetime(df['data_fim'], errors='coerce')

    print(f"[INFO] Total de eventos processados: {len(df)}")
    carregar_csv(df)

if __name__ == "__main__":
    run_pipeline(dias=7)
