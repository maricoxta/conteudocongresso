# Automação de Monitoramento de Agendas Legislativas

Este script Python automatiza a varredura das agendas da Câmara dos Deputados e do Senado Federal para identificar reuniões e eventos relacionados a saneamento, meio ambiente e defesa civil. Ele gera um relatório consolidado e o envia por e-mail.

## Funcionalidades

- Coleta de dados das APIs da Câmara dos Deputados e do Senado Federal.
- Filtragem de eventos com base em palavras-chave predefinidas.
- Geração de relatório formatado com informações relevantes.
- Envio automático do relatório por e-mail.
- Agendamento da execução da tarefa.

## Pré-requisitos

- Python 3.x instalado.
- As seguintes bibliotecas Python:
  - `requests`
  - `lxml` (para processamento de XML, embora o script atual use `ElementTree` nativo, é bom ter para robustez)

## Instalação

1. Clone ou baixe este repositório.
2. Navegue até o diretório do projeto.
3. Instale as dependências:
   ```bash
   pip install requests lxml
   ```

## Configuração

Abra o arquivo `main.py` e edite as seguintes variáveis:

- **Credenciais de E-mail:**
  ```python
  from_email = "seu_email@example.com"  # Substitua pelo seu e-mail
  from_password = "sua_senha_app"      # Substitua pela sua senha de aplicativo (para Gmail, por exemplo)
  to_email = "destinatario@example.com"  # Substitua pelo e-mail do destinatário
  ```
  **Importante:** Se estiver usando Gmail, você precisará gerar uma "senha de aplicativo" em suas configurações de segurança do Google, pois a senha da sua conta principal não funcionará diretamente.

- **Palavras-chave:**
  As palavras-chave para filtragem estão definidas na variável `KEYWORDS`. Você pode adicionar, remover ou modificar os termos conforme necessário:
  ```python
  KEYWORDS = {
      "saneamento": ["saneamento", "saneamento básico", "água", "esgoto", "resíduos sólidos", "drenagem", "abastecimento de agua", "esgotamento", "transbordo", "compostagem", "prestacao regionalizada"],
      "meio ambiente": ["meio ambiente", "sustentabilidade", "preservação", "desmatamento", "poluição", "recursos hídricos", "biodiversidade", "climático", "clima", "aquecimento global", "ambientalistas", "rio tietê", "florestas", "ambiental", "sustentavel", "vegetacao", "licenciamento", "bioma", "incendios", "natureza", "lixões", "aterro sanitario", "aterro controlado"],
      "defesa civil": ["defesa civil", "desastres naturais", "enchentes", "deslizamentos", "secas", "emergência", "risco", "prevenção", "mitigação", "calamidades"],
      "geral": ["cop30", "lixo", "residuos", "catadores", "coleta", "manejo", "limpeza", "reciclagem", "logistica reversa", "galpao de triagem", "caminhao de lixo", "cooperativas", "disposicao final", "universalizacao"]
  }
  ```

## Execução

Para executar o script manualmente:

```bash
python3 main.py
```

## Agendamento

Esta automação foi configurada para ser executada semanalmente, toda segunda-feira às 8h, utilizando o agendador de tarefas do sistema. Se precisar alterar a periodicidade, entre em contato com o suporte ou com o administrador do sistema onde a automação está sendo executada.

## Estrutura do Código

- `get_senate_commission_meetings()`: Coleta dados da API do Senado.
- `process_senate_meetings()`: Processa os dados XML do Senado.
- `get_chamber_events()`: Coleta dados da API da Câmara.
- `process_chamber_events()`: Processa os dados JSON da Câmara.
- `filter_senate_meetings()`: Filtra os eventos do Senado com base nas palavras-chave.
- `filter_chamber_events()`: Filtra os eventos da Câmara com base nas palavras-chave.
- `generate_report()`: Gera o relatório final no formato especificado.
- `send_email()`: Envia o relatório por e-mail.

## Solução de Problemas

- **E-mail não enviado:** Verifique suas credenciais de e-mail e se a opção de "aplicativos menos seguros" está ativada para sua conta (ou use uma senha de aplicativo).
- **Eventos faltando:** Verifique se as palavras-chave estão abrangendo os termos desejados e se os eventos estão realmente disponíveis nas APIs da Câmara e do Senado para o período solicitado.

---

**Desenvolvido por Manus AI**


