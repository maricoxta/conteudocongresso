import requests
import json
from datetime import date, timedelta
import xml.etree.ElementTree as ET
import locale
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set locale for Portuguese day names
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def get_senate_commission_meetings(dataInicio, dataFim):
    url = f"https://legis.senado.leg.br/dadosabertos/comissao/agenda/{dataInicio}/{dataFim}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        root = ET.fromstring(response.content)
        return root
    except requests.exceptions.RequestException as e:
        print(f"Erro ao coletar dados da API do Senado: {e}")
        return None
    except ET.ParseError as e:
        print(f"Erro ao analisar XML da API do Senado: {e}")
        return None

def process_senate_meetings(xml_root):
    meetings_data = []
    for reuniao in xml_root.findall(".//reuniao"):
        codigo = reuniao.find("codigo").text if reuniao.find("codigo") is not None else ""
        descricao = reuniao.find("descricao").text if reuniao.find("descricao") is not None else ""
        titulo = reuniao.find("titulo").text if reuniao.find("titulo") is not None else ""
        sigla_colegiado = reuniao.find(".//colegiadoCriador/sigla").text if reuniao.find(".//colegiadoCriador/sigla") is not None else ""
        nome_colegiado = reuniao.find(".//colegiadoCriador/nome").text if reuniao.find(".//colegiadoCriador/nome") is not None else ""
        data_inicio = reuniao.find("dataInicio").text if reuniao.find("dataInicio") is not None else ""
        local = reuniao.find("local").text if reuniao.find("local") is not None else ""

        itens_pauta = []
        for item in reuniao.findall(".//itens/item"):
            nome_item = item.find("nome").text if item.find("nome") is not None else ""
            descricao_item = item.find("descricao").text if item.find("descricao") is not None else ""
            itens_pauta.append({"nome": nome_item, "descricao": descricao_item})

        meetings_data.append({
            "codigo": codigo,
            "descricao": descricao,
            "titulo": titulo,
            "sigla_colegiado": sigla_colegiado,
            "nome_colegiado": nome_colegiado,
            "data_inicio": data_inicio,
            "local": local,
            "itens_pauta": itens_pauta
        })
    return meetings_data

def get_chamber_events():
    url = "https://dadosabertos.camara.leg.br/api/v2/eventos"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao coletar dados da API da Câmara: {e}")
        return None

def process_chamber_events(json_data):
    events_data = []
    for evento in json_data["dados"]:
        events_data.append({
            "id": evento.get("id", ""),
            "uri": evento.get("uri", ""),
            "dataHoraInicio": evento.get("dataHoraInicio", ""),
            "dataHoraFim": evento.get("dataHoraFim", ""),
            "situacao": evento.get("situacao", ""),
            "descricao": evento.get("descricao", ""),
            "local": evento.get("local", ""),
            "url": evento.get("url", ""),
            "orgaos": evento.get("orgaos", []),
            "descricaoTipo": evento.get("descricaoTipo", "")
        })
    return events_data

KEYWORDS = {
    "saneamento": ["saneamento", "saneamento básico", "água", "esgoto", "resíduos sólidos", "drenagem", "abastecimento de agua", "esgotamento", "transbordo", "compostagem", "prestacao regionalizada"],
    "meio ambiente": ["meio ambiente", "sustentabilidade", "preservação", "desmatamento", "poluição", "recursos hídricos", "biodiversidade", "climático", "clima", "aquecimento global", "ambientalistas", "rio tietê", "florestas", "ambiental", "sustentavel", "vegetacao", "licenciamento", "bioma", "incendios", "natureza", "lixões", "aterro sanitario", "aterro controlado"],
    "defesa civil": ["defesa civil", "desastres naturais", "enchentes", "deslizamentos", "secas", "emergência", "risco", "prevenção", "mitigação", "calamidades"],
    "geral": ["cop30", "lixo", "residuos", "catadores", "coleta", "manejo", "limpeza", "reciclagem", "logistica reversa", "galpao de triagem", "caminhao de lixo", "cooperativas", "disposicao final", "universalizacao"]
}

def filter_senate_meetings(meetings_data, keywords):
    filtered_meetings = []
    for meeting in meetings_data:
        text_to_search = f'{meeting.get("descricao", "")} {meeting.get("titulo", "")} {meeting.get("nome_colegiado", "")}'
        for item in meeting.get("itens_pauta", []):
            text_to_search += f' {item.get("nome", "")} {item.get("descricao", "")}'

        for category, terms in keywords.items():
            if any(term.lower() in text_to_search.lower() for term in terms):
                filtered_meetings.append(meeting)
                break
    return filtered_meetings

def filter_chamber_events(events_data, keywords):
    filtered_events = []
    for event in events_data:
        text_to_search = f'{event.get("descricao", "")} {event.get("local", "")} {event.get("descricaoTipo", "")}'
        for orgao in event.get("orgaos", []):
            text_to_search += f' {orgao.get("nome", "")}'

        found_keyword = False
        for category, terms in keywords.items():
            for term in terms:
                if term.lower() in text_to_search.lower():
                    filtered_events.append(event)
                    found_keyword = True
                    break
            if found_keyword:
                break
    return filtered_events

def generate_report(senate_data, chamber_data):
    report = "Prezados,\n\n"
    report += "Segue a relação das reuniões das Comissões da Câmara de Deputados e do Senado desta semana que são de interesse da Gerência de Sustentabilidade e Resiliência da CNM, bem como votação de PLs de interesse em outras Comissões:\n\n"

    report += "CÂMARA DOS DEPUTADOS\n\n"
    # Group chamber data by date
    chamber_by_date = {}
    for event in chamber_data:
        event_date = event["dataHoraInicio"].split("T")[0] # YYYY-MM-DD
        if event_date not in chamber_by_date:
            chamber_by_date[event_date] = []
        chamber_by_date[event_date].append(event)

    for date_str in sorted(chamber_by_date.keys()):
        date_obj = date.fromisoformat(date_str)
        report += f"{date_obj.strftime('%d/%m/%Y')} - {date_obj.strftime('%A').capitalize()}\n\n"
        for event in chamber_by_date[date_str]:
            commission_name = ""
            if event.get("orgaos"):
                commission_name = event["orgaos"][0].get("nome", "")
            report += f"{event.get('dataHoraInicio', '').split('T')[1][:5]} - {commission_name}\n"
            report += f"{event.get('descricao', '')}\n"
            report += f"{event.get('situacao', '')}\n"
            report += f"{event.get('local', '')}\n\n"

    report += "SENADO\n\n"
    # Group senate data by date
    senate_by_date = {}
    for meeting in senate_data:
        meeting_date = meeting["data_inicio"].split("T")[0] # YYYY-MM-DD
        if meeting_date not in senate_by_date:
            senate_by_date[meeting_date] = []
        senate_by_date[meeting_date].append(meeting)

    for date_str in sorted(senate_by_date.keys()):
        date_obj = date.fromisoformat(date_str)
        report += f"{date_obj.strftime('%d/%m/%Y')} - {date_obj.strftime('%A').capitalize()}\n\n"
        for meeting in senate_by_date[date_str]:
            report += f"{meeting.get('data_inicio', '').split('T')[1][:5]} - {meeting.get('nome_colegiado', '')}\n"
            report += f"{meeting.get('local', '')}\n\n"
            for i, item in enumerate(meeting.get("itens_pauta", [])):
                report += f"{i+1} - {item.get('nome', '')} - {item.get('descricao', '')}\n"
            report += "\n"

    report += "Atenciosamente,\n"
    return report

def send_email(subject, body, to_email, attachment_path=None):
    from_email = "agendacongressosustentabilidad@gmail.com"
    from_password = "jkqs wsiq hiky besp"

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if attachment_path:
        with open(attachment_path, "rb") as attachment:
            part = MIMEText(attachment.read().decode("utf-8"), "plain")
            part.add_header("Content-Disposition", f"attachment; filename= {attachment_path}")
            msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Exemplo para Gmail
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

if __name__ == "__main__":
    today = date.today()
    next_week = today + timedelta(days=7)

    senate_meetings_xml = get_senate_commission_meetings(today.strftime("%Y%m%d"), next_week.strftime("%Y%m%d"))
    senate_processed_data = []
    if senate_meetings_xml:
        senate_processed_data = process_senate_meetings(senate_meetings_xml)
        filtered_senate_meetings = filter_senate_meetings(senate_processed_data, KEYWORDS)
        with open("senate_meetings_filtered.json", "w", encoding="utf-8") as f:
            json.dump(filtered_senate_meetings, f, ensure_ascii=False, indent=4)
        print("Dados das reuniões de comissão do Senado filtrados e salvos em senate_meetings_filtered.json")
    else:
        print("Não foi possível obter ou processar os dados das reuniões de comissão do Senado.")

    chamber_events = get_chamber_events()
    chamber_processed_data = []
    if chamber_events:
        chamber_processed_data = process_chamber_events(chamber_events)
        filtered_chamber_events = filter_chamber_events(chamber_processed_data, KEYWORDS)
        with open("chamber_events_filtered.json", "w", encoding="utf-8") as f:
            json.dump(filtered_chamber_events, f, ensure_ascii=False, indent=4)
        print("Dados dos eventos da Câmara filtrados e salvos em chamber_events_filtered.json")
    else:
        print("Não foi possível obter os dados dos eventos da Câmara.")

    final_report = generate_report(filtered_senate_meetings, filtered_chamber_events)
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(final_report)
    print("Relatório gerado e salvo em report.txt")

    # Enviar e-mail
    send_email("Relatório de Agendas Legislativas", final_report, "marianna.costa@cnm.org.br", "report.txt")


