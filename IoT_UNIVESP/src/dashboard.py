import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# ==============================
# Configurações de conexão Railway
# ==============================
USER = "postgres"
PASSWORD = "123456"
HOST = "yamanote.proxy.rlwy.net"
PORT = "19069"
DB = "railway"

TABLE = "weather_readings"

# ==============================
# Conexão com o banco
# ==============================
engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

@st.cache_data
def load_view(view_name):
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql(query, engine)

# ==============================
# Layout do Streamlit
# ==============================
st.set_page_config(page_title="Painel Climático", layout="wide")
st.title("📊 Painel de Visualização Climática")
abas = ["Educação Climática", "🌡️ Temperatura Média", "🔥 Extremos de Temperatura", "💧 Umidade", "🌬️ Vento", "🌧️ Precipitação"]
aba = st.sidebar.radio("Escolha uma aba", abas)

# ==============================
# Aba 1: Educação Climática
# ==============================
if aba == "Educação Climática":
    st.subheader("🧠 Por que monitorar o clima?")
    st.markdown(
        """
        Monitorar variáveis climáticas é essencial para:
        - 🌾 Agricultura de precisão
        - 🏙️ Planejamento urbano e prevenção de desastres
        - 🌡️ Análise de mudanças climáticas
        - 💧 Gestão de recursos hídricos
        - 🦠 Saúde pública (doenças sazonais)
        """
    )

# ==============================
# Aba 2: Temperatura Média
# ==============================
elif aba == "🌡️ Temperatura Média":
    st.subheader("📈 Temperatura Média Diária")
    df_temp = load_view("temp_media_diaria")
    fig = px.line(df_temp, x="data", y="temp_media", title="Temperatura Média Diária")
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# Aba 3: Extremos de Temperatura
# ==============================
elif aba == "🔥 Extremos de Temperatura":
    st.subheader("🌡️ Mínimas e Máximas Diárias")
    df_ext = load_view("temp_extremos")
    fig = px.line(df_ext, x="data", y=["temp_min", "temp_max"], title="Extremos Diários")
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# Aba 4: Umidade
# ==============================
elif aba == "💧 Umidade":
    st.subheader("💧 Umidade Relativa")
    df_umid = load_view("umidade_stats")
    fig = px.line(df_umid, x="data", y=["hum_min", "hum_max"], title="Umidade Relativa Diária")
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# Aba 5: Vento
# ==============================
elif aba == "🌬️ Vento":
    st.subheader("🌬️ Velocidade do Vento")
    df_vento = load_view("vento_stats")
    fig = px.line(df_vento, x="data", y=["vento_medio", "vento_max"], title="Velocidade do Vento (média e máxima)")
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# Aba 6: Precipitação
# ==============================
elif aba == "🌧️ Precipitação":
    st.subheader("🌧️ Precipitação Acumulada")
    df_prec = load_view("precipitacao_diaria")
    fig = px.bar(df_prec, x="data", y="rain_max", title="Precipitação Máxima Diária")
    st.plotly_chart(fig, use_container_width=True)
