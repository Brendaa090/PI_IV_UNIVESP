import pandas as pd
from sqlalchemy import create_engine, text

# ==============================
# Configurações de conexão
# ==============================
engine = create_engine("postgresql://neondb_owner:npg_FLXS1ZIN8gQR@ep-late-water-a441wvij-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# ==============================
# Conexão com o banco
# ==============================
engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

# ==============================
# Carregar CSV com encoding correto
# ==============================
df = pd.read_csv(CSV_PATH, low_memory=False, encoding="latin1")

# Garantir UTF-8
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].astype(str).apply(
        lambda x: x.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
    )

# Renomear colunas
df.columns = [c.strip().lower() for c in df.columns]
rename_map = {
    "data (yyyy-mm-dd)": "timestamp",
    "estacao": "station",
    "temp_avg": "temperature_avg",
    "temp_max": "temperature_max",
    "temp_min": "temperature_min",
    "hum_max": "humidity_max",
    "hum_min": "humidity_min",
    "rain_max": "rain_max",
    "rad_max": "radiation_max",
    "wind_max": "wind_max",
    "wind_avg": "wind_avg"
}
df = df.rename(columns=rename_map)

# Converter datas
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

print("✅ Colunas finais do DataFrame:", list(df.columns))

# ==============================
# Enviar para o Postgres
# ==============================
df.to_sql(TABLE, engine, if_exists="append", index=False)

# ==============================
# Criar Views no Postgres
# ==============================
with engine.begin() as conn:
    # Remover views antigas (se existirem)
    conn.execute(text("DROP VIEW IF EXISTS temp_media_diaria;"))
    conn.execute(text("DROP VIEW IF EXISTS temp_extremos;"))
    conn.execute(text("DROP VIEW IF EXISTS umidade_stats;"))
    conn.execute(text("DROP VIEW IF EXISTS vento_stats;"))
    conn.execute(text("DROP VIEW IF EXISTS chuva_stats;"))
    conn.execute(text("DROP VIEW IF EXISTS precipitacao_diaria;"))

    # 1️⃣ Temperatura média diária
    conn.execute(text("""
        CREATE OR REPLACE VIEW temp_media_diaria AS
        SELECT DATE(timestamp) AS data,
               AVG(temperature_avg) AS temp_media
        FROM weather_readings
        WHERE temperature_avg IS NOT NULL
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp);
    """))

    # 2️⃣ Máximas e mínimas de temperatura
    conn.execute(text("""
        CREATE OR REPLACE VIEW temp_extremos AS
        SELECT DATE(timestamp) AS data,
               MAX(temperature_max) AS temp_max,
               MIN(temperature_min) AS temp_min
        FROM weather_readings
        WHERE temperature_max IS NOT NULL AND temperature_min IS NOT NULL
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp);
    """))

    # 3️⃣ Umidade (máxima e mínima)
    conn.execute(text("""
        CREATE OR REPLACE VIEW umidade_stats AS
        SELECT DATE(timestamp) AS data,
               MAX(humidity_max) AS hum_max,
               MIN(humidity_min) AS hum_min
        FROM weather_readings
        WHERE humidity_max IS NOT NULL AND humidity_min IS NOT NULL
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp);
    """))

    # 4️⃣ Vento (máximo e médio)
    conn.execute(text("""
        CREATE OR REPLACE VIEW vento_stats AS
        SELECT DATE(timestamp) AS data,
               MAX(wind_max) AS vento_max,
               AVG(wind_avg) AS vento_medio
        FROM weather_readings
        WHERE wind_max IS NOT NULL AND wind_avg IS NOT NULL
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp);
    """))

    # 5️⃣ Precipitação (chuva)
    conn.execute(text("""
        CREATE OR REPLACE VIEW precipitacao_diaria AS
        SELECT DATE(timestamp) AS data,
               MAX(rain_max) AS rain_max
        FROM weather_readings
        WHERE rain_max IS NOT NULL
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp);
    """))

print("🎉 Pipeline concluído com sucesso! Tabela 'weather_readings' e todas as views foram criadas.")
