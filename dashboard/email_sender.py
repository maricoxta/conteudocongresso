# email_sender.py

import os, smtplib
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Agenda import carregar_dataframe
from email.mime.text import MIMEText
from datetime import datetime, timedelta

EMAIS = {
    "Meio Ambiente": "meioambiente@cnm.org.br",
    "Defesa Civil": "defesacivil@cnm.org.br",
    "Saneamento Básico": "saneamento@cnm.org.br"
}

def format_msg(df, area):
    lines = ["Prezados, boa tarde!\n", 
             "Segue a relação das reuniões da semana:\n"]
    for _, r in df.iterrows():
        data_inicio = pd.to_datetime(r['Data e Hora Início'])
        lines.append(f"{data_inicio.strftime('%d/%m/%Y')} - "
                     f"{data_inicio.strftime('%A')}\n"
                     f"Horário de Início: {data_inicio.strftime('%Hh%M')}\n"
                     f"Horário de Fim: -\n"  # Não temos data_fim na query
                     f"Situação: -\n"       # Não temos situacao na query
                     f"Tipo: -\n"           # Não temos tipo na query
                     f"Tema: {r['Tema']}\n"
                     f"Área Técnica: {area}\n"
                     f"Título: {r['Título']}\n"
                     f"Local: {r['Local']}\n"
                     f"Link: {r['Link']}\n\n")
    lines.append("Atenciosamente,")
    return "\n".join(lines)

def send_email():
    df = carregar_dataframe()
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # segunda
    week_df = df[df["Data e Hora Início"].dt.date >= week_start]

    server = smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
    server.starttls()
    server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))

    for area, email in EMAIS.items():
        subdf = week_df[week_df["Tema"] == area]
        if subdf.empty: continue
        msg = MIMEText(format_msg(subdf, area))
        msg["Subject"] = f"Agenda Legislativa - {area}"
        msg["From"] = os.getenv("SMTP_USER")
        msg["To"] = email
        server.send_message(msg)
        print("E-mail enviado:", area)
    server.quit()

if __name__ == "__main__":
    send_email()
