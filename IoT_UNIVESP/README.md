🌐 Projeto Integrador – Pipeline de Dados com Docker, PostgreSQL, Python e Streamlit
📘 Visão Geral

Este projeto foi desenvolvido para a disciplina Disruptive Architectures: IoT, Big Data e IA e tem como objetivo construir um pipeline de dados IoT completo, com coleta, armazenamento, processamento e visualização de leituras de temperatura geradas por sensores.

O pipeline foi construído com as seguintes tecnologias:

🐳 Docker + PostgreSQL (banco de dados em container)

🐍 Python + pandas + SQLAlchemy (ETL e persistência)

🧠 Views SQL (camada analítica)

📊 Streamlit + Plotly (dashboard interativo)

🧱 Tecnologias Utilizadas
Camada	Ferramentas
Banco de Dados	PostgreSQL + Docker
ETL	Python, pandas, SQLAlchemy
Análises	Views SQL
Visualização	Streamlit + Plotly
⚙️ Como Executar o Projeto
🐳 1. Subir o banco PostgreSQL com Docker
docker run --name postgres-iot -e POSTGRES_PASSWORD=sua_senha -p 5432:5432 -d postgres


Caso o container já exista:

docker start postgres-iot


Criar o banco:

docker exec -it postgres-iot psql -U postgres -c "CREATE DATABASE iot_db;"

🐍 2. Preparar o ambiente Python
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

🔁 3. Executar o pipeline de ingestão e criação de views
python src/pipeline.py

📊 4. Rodar o dashboard interativo
streamlit run src/dashboard.py


Acesse no navegador: http://localhost:8501

📁 Estrutura de Pastas
PI_IV_UNIVESP/
│
├── src/
│   ├── pipeline.py         # Ingestão de dados e criação das views
│   └── dashboard.py        # Interface interativa com Streamlit
│
├── sql/                    # Scripts SQL das views criadas
│   ├── init.sql
│   ├── temp_media...
│   └── ...
│
├── docs/
│   └── prints-dashboard/   # Capturas de tela do dashboard
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

🗂️ Views SQL Criadas
avg_temp_por_dispositivo
SELECT device_id, AVG(temperature) AS avg_temp
FROM temperature_readings
GROUP BY device_id;


📌 Temperatura média por dispositivo.

leituras_por_hora
SELECT EXTRACT(HOUR FROM timestamp) AS hora, COUNT(*) AS contagem
FROM temperature_readings
GROUP BY hora
ORDER BY hora;


📌 Distribuição de leituras por hora do dia.

temp_max_min_por_dia
SELECT DATE(timestamp) AS data,
       MAX(temperature) AS temp_max,
       MIN(temperature) AS temp_min
FROM temperature_readings
GROUP BY DATE(timestamp)
ORDER BY DATE(timestamp);


📌 Temperaturas máxima e mínima por dia.

📊 Visualizações no Dashboard

Temperatura média por dispositivo


Leituras por hora do dia


Temperaturas máximas e mínimas por dia


Média de temperatura por localização (in/out)


🔍 Principais Insights

🌡️ Variações de temperatura entre dispositivos, sugerindo diferenças ambientais ou calibração.

⏰ Picos de leitura em horários específicos, indicando momentos críticos de monitoramento.

📈 Tendência de máximas e mínimas diárias, com potencial aplicação em agricultura e energia.

🏠 Diferenças claras entre locais internos e externos, importantes para controle climático.

📦 Dependências (requirements.txt)
pandas
sqlalchemy
psycopg2-binary
streamlit
plotly


Instale com:

pip install -r requirements.txt

🧪 Comandos Git Utilizados
git init
git add .
git commit -m "IoT pipeline: ingestão, views e dashboard"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/projeto-iot.git
git push -u origin main

🔗 Dataset de Origem

📁 Kaggle – Temperature Readings: IoT Devices