# Acompanhamento Congresso Nacional

Este projeto tem como objetivo **monitorar e acompanhar eventos e proposições legislativas** relacionadas às áreas de **saneamento básico, meio ambiente e defesa civil** no Congresso Nacional (Câmara dos Deputados e Senado Federal).

## Objetivo

O objetivo principal é facilitar o acesso e a análise de informações legislativas relevantes para essas áreas técnicas, permitindo que profissionais e gestores possam:

- Identificar rapidamente reuniões, audiências e votações de interesse.
- Receber alertas sobre proposições importantes (como Projetos de Lei).
- Visualizar indicadores semanais e tendências de atuação parlamentar.
- Gerar relatórios e enviar notificações automáticas para equipes técnicas.

## Como funciona

O projeto realiza as seguintes etapas:

1. **Extração de dados:**  
   Utiliza APIs públicas da Câmara dos Deputados e do Senado Federal para coletar eventos e proposições legislativas.

2. **Processamento e classificação:**  
   Os dados são tratados e classificados automaticamente conforme temas de interesse (saneamento, meio ambiente, defesa civil), usando palavras-chave e regras definidas no código.

3. **Armazenamento:**  
   Os eventos são salvos em um banco de dados PostgreSQL para consulta e análise.

4. **Dashboard interativo:**  
   Um painel desenvolvido com Streamlit permite visualizar os eventos por área técnica, acompanhar indicadores semanais, consultar o calendário de reuniões e receber alertas sobre proposições relevantes.

5. **Notificações automáticas:**  
   O sistema pode enviar e-mails para equipes técnicas com a agenda semanal e alertas personalizados.

## Tecnologias utilizadas

- Python
- Streamlit (dashboard)
- Pandas (tratamento de dados)
- SQLAlchemy (conexão com banco de dados)
- PostgreSQL (armazenamento)
- Requests (extração de dados das APIs)
- Plotly (visualização gráfica)

## Como executar

1. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

2. Configure o arquivo `.env` com suas credenciais do banco de dados.

3. Execute o pipeline para atualizar os dados:
   ```sh
   python pipeline/Agenda.py
   ```

4. Inicie o dashboard:
   ```sh
   streamlit run dashboard/Painel_Agenda.py
   ```

---

**Este projeto é uma ferramenta de apoio à gestão pública, promovendo transparência e agilidade no acompanhamento legislativo das áreas de saneamento, meio ambiente e defesa civil.**
