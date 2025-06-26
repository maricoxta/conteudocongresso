# Automação do Monitoramento do Conteúdo do Congresso
Criação de um programa automatizado para realizar diariamente o monitoramento dos sites da Câmara dos Deputados e do Senado Federal e obter as informações sobre alterações nos Projetos de Lei, Emendas Parlamentares, Requerimentos e Audiências que englobam assuntos relacionados às áreas de Saneamento Básico, Meio Ambiente e Defesa Civil. 

Após realizar uma varredura nos sites, o programa encaminha um relatório por e-mail com projetos relevantes às áreas técnicas da Confederação Nacional de Municípios. 

# Ferramenta Utilizada 
Python 

# Diagrama

![image](https://github.com/user-attachments/assets/0e08de92-a409-4ac9-8ff0-150edd0ec4f1)

# Etapas

1️⃣ Identificar as fontes oficiais para as agendas da Câmara dos Deputados e do Senado Federal, priorizando APIs públicas ou portais de dados estruturados, conforme ilustrado nos passos 'Coletar dados do Senado' e 'Coletar dados da Câmara' do diagrama.

2️⃣ Analisar a estrutura e o formato dos dados das agendas (por exemplo, HTML, JSON, XML) para determinar como extrair informações específicas como data, hora, nome da comissão, tipo de evento, local, tema e link do evento, que são requisitos para o relatório final.

3️⃣ Pesquisar métodos para acessar e analisar programaticamente as fontes de agenda identificadas, considerando técnicas de web scraping para conteúdo HTML ou utilizando a documentação da API para dados estruturados, correspondendo ao passo 'Tratar os dados'.

4️⃣ Investigar estratégias eficazes para filtrar os tópicos da agenda extraídos com base em palavras-chave como 'saneamento', 'meio ambiente' e 'defesa civil', conforme indicado no passo 'Criar Filtros' do diagrama.

5️⃣ Explorar abordagens e ferramentas comuns para agendar a execução automatizada de scripts Python de forma recorrente, especificamente para um cronograma semanal (por exemplo, toda segunda-feira às 8h), alinhando-se ao passo 'Gerar alertas com base na periodicidade definida'.

6️⃣ Encontrar informações sobre bibliotecas Python e melhores práticas para compor e enviar e-mails programaticamente, garantindo a capacidade de incluir os detalhes da agenda extraídos em um formato de relatório estruturado, como mostrado no passo 'Encaminhar e-mail'.

7️⃣ Procurar por projetos de código aberto, bibliotecas ou exemplos existentes relacionados ao monitoramento de atividades legislativas ou dados públicos no Brasil, que possam oferecer insights sobre acesso a dados, análise ou técnicas de automação.

8️⃣ Sintetizar todas as informações coletadas para fornecer uma visão geral abrangente dos componentes técnicos e etapas necessárias para construir o script de automação descrito.
