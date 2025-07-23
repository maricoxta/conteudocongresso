# email_sender.py

import os, smtplib
from Agenda import carregar_dataframe
import pandas as pd
from email.mime.text import MIMEText
from datetime import datetime, timedelta

EMAIS = {
    "Meio Ambiente e Saneamento": "meioambiente@cnm.org.br",
    "Defesa Civil": "defesacivil@cnm.org.br",
    "Saneamento Básico": "saneamento@cnm.org.br"
}

def format_msg(df, area):
    lines = ["Prezados, boa tarde!\n", 
             "Segue a relação das reuniões da semana:\n"]
    for _, r in df.iterrows():
        lines.append(f"{r['data_inicio'].strftime('%d/%m/%Y')} - "
                     f"{r['data_inicio'].strftime('%A')}\n"
                     f"Horário de Início: {r['data_inicio'].strftime('%Hh%M')}\n"
                     f"Horário de Fim: {r['data_fim'].strftime('%Hh%M') if not pd.isna(r['data_fim']) else '-'}\n"
                     f"Situação: {r['situacao']}\n"
                     f"Tipo: {r['tipoevento']}\n"
                     f"Tema: {r['tema']}\n"
                     f"Área Técnica: {area}\n"
                     f"Título: {r['nome']}\n"
                     f"Local: {r['local']}\n"
                     f"Link: {r['link']}\n\n")
    lines.append("Atenciosamente,")
    return "\n".join(lines)

def send_email():
    df = carregar_dataframe()
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # segunda
    week_df = df[df["data_inicio"].dt.date >= week_start]

    server = smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
    server.starttls()
    server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))

    for area, email in EMAIS.items():
        subdf = week_df[week_df["tema"] == area]
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
