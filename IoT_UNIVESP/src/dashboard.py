import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Brazil Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# ==========================
# Configuração da conexão
# ==========================
USER = "postgres"
PASSWORD = "123456"
HOST = "localhost"
PORT = "5432"
DB = "iot_db"

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

# ==========================
# Carregar dados de uma view
# ==========================
@st.cache_data
def load_view(view_name):
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql(query, engine)

# ==========================
# Filtro de ano e mês
# ==========================
def aplicar_filtros(df, col_data="data", prefix=""):
    df[col_data] = pd.to_datetime(df[col_data])
    df["ano"] = df[col_data].dt.year
    df["mes"] = df[col_data].dt.month

    anos = sorted(df["ano"].unique())
    ano_selecionado = st.selectbox("📅 Escolha o ano:", anos, index=len(anos)-1, key=f"{prefix}_ano")

    meses = sorted(df[df["ano"] == ano_selecionado]["mes"].unique())
    mes_selecionado = st.selectbox("📆 Escolha o mês:", ["Todos"] + list(meses), key=f"{prefix}_mes")

    df_filtrado = df[df["ano"] == ano_selecionado]
    if mes_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["mes"] == mes_selecionado]

    return df_filtrado, ano_selecionado, mes_selecionado

# ==========================
# Layout personalizado
# ==========================
def layout_legivel(titulo, fundo):
    return dict(
        title=dict(text=titulo, font=dict(color="black", size=20, family="Comic Sans MS")),
        plot_bgcolor=fundo,
        paper_bgcolor=fundo,
        font=dict(color="black"),
        xaxis=dict(showgrid=False, tickfont=dict(color="black"), title_font=dict(color="black")),
        yaxis=dict(showgrid=True, gridcolor="#BDBDBD", tickfont=dict(color="black"), title_font=dict(color="black")),
        legend=dict(font=dict(color="black"))
    )

# ==========================
# Abas do dashboard
# ==========================
tabs = st.tabs([
    "📖 Educação Climática",
    "🌡️ Temperatura Média",
    "🔥 Extremos de Temperatura",
    "💧 Umidade",
    "🌬️ Vento",
    "🌧️ Precipitação"
])

# --------------------------
# 1. Educação Climática
# --------------------------
with tabs[0]:
    st.title("📖 A Importância de Estudar o Clima")
    st.markdown("""
Estudar o clima no Brasil é super importante por vários motivos que afetam nossa vida diária, a economia e o meio ambiente. Aqui estão alguns pontos principais:      
                
                1. Por que o clima é diferente em cada lugar
O Brasil é um país gigante e tem muitos tipos de clima. No Norte, perto da floresta Amazônica, o clima é quente e úmido; no Centro-Oeste e Sudeste, é tropical, com estações mais definidas; no Nordeste, é semiárido, ou seja, faz muito calor e chove pouco; e no Sul, é subtropical, com invernos mais frios. Entender essas diferenças nos ajuda a prever o tempo e cuidar melhor das plantações.

                2. Clima e agricultura
O clima influencia bastante a nossa comida! Saber quando chove, a temperatura e as estações do ano ajuda os agricultores a plantar na hora certa, evitar perdas com seca ou muito calor e usar água da irrigação com inteligência. Isso também protege a economia, porque menos prejuízo significa mais alimento e dinheiro para todo mundo.

                3. Preparação para desastres
Às vezes, acontecem eventos extremos, como enchentes, secas ou tempestades. Quem estuda o clima consegue avisar a população antes das catástrofes, assim as pessoas podem se proteger e os prejuízos diminuem.

                4. Mudanças no clima
O clima do Brasil tem mudado com o tempo. A temperatura aumenta, algumas regiões ficam mais secas ou chuvosas, e eventos extremos acontecem com mais frequência. Estudar o clima ajuda os cientistas e o governo a tomar decisões para proteger o meio ambiente e planejar o futuro, como cuidar dos rios e florestas.

                5. Planejamento das cidades e recursos naturais
O clima também influencia água, energia e transporte. Conhecendo o clima, podemos construir cidades melhores, planejar estradas, cuidar dos reservatórios de água e garantir uma vida melhor para todos  

    ✨ Use as abas acima para explorar os gráficos e descubra curiosidades sobre o clima no Brasil!  
    """)

# --------------------------
# 2. Temperatura Média
# --------------------------
with tabs[1]:
    st.title("🌡️ Temperatura Média")
    df_temp = load_view("temp_media_diaria")
    df_filtrado, ano, mes = aplicar_filtros(df_temp, "data", prefix="temp")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado["data"],
        y=df_filtrado["temp_media"],
        mode="lines+markers",
        line=dict(width=3, color="orange"),
        marker=dict(size=10, symbol="star", color="yellow"),
        name="🌞 Temperatura"
    ))

    fig.update_layout(layout_legivel(
        f"🌞 Temperatura Média - {ano}{'' if mes=='Todos' else f'/{mes}'}",
        fundo="#FFE0B2"
    ))
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# 3. Extremos de Temperatura
# --------------------------
with tabs[2]:
    st.title("🔥 Máximas e Mínimas")
    df_extremos = load_view("temp_extremos")
    df_filtrado, ano, mes = aplicar_filtros(df_extremos, "data", prefix="extremos")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado["data"], y=df_filtrado["temp_max"],
        mode="lines+markers",
        line=dict(width=3, color="red"),
        marker=dict(symbol="triangle-up", size=8, color="darkred"),
        name="🔥 Máxima"
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado["data"], y=df_filtrado["temp_min"],
        mode="lines+markers",
        line=dict(width=3, color="blue"),
        marker=dict(symbol="triangle-down", size=8, color="lightblue"),
        name="❄️ Mínima"
    ))

    fig.update_layout(layout_legivel(
        f"🔥 Extremos de Temperatura - {ano}{'' if mes=='Todos' else f'/{mes}'}",
        fundo="#BBDEFB"
    ))
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# 4. Umidade
# --------------------------
with tabs[3]:
    st.title("💧 Umidade")
    df_umid = load_view("umidade_stats")
    df_filtrado, ano, mes = aplicar_filtros(df_umid, "data", prefix="umidade")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado["data"], y=df_filtrado["hum_max"],
        mode="lines+markers",
        line=dict(width=3, color="green"),
        marker=dict(symbol="diamond", size=8, color="lime"),
        name="💧 Máxima"
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado["data"], y=df_filtrado["hum_min"],
        mode="lines+markers",
        line=dict(width=3, color="teal"),
        marker=dict(symbol="diamond-open", size=8, color="aqua"),
        name="💧 Mínima"
    ))

    fig.update_layout(layout_legivel(
        f"💧 Umidade - {ano}{'' if mes=='Todos' else f'/{mes}'}",
        fundo="#C8E6C9"
    ))
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# 5. Vento
# --------------------------
with tabs[4]:
    st.title("🌬️ Vento")
    df_vento = load_view("vento_stats")
    df_filtrado, ano, mes = aplicar_filtros(df_vento, "data", prefix="vento")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado["data"], y=df_filtrado["vento_max"],
        mode="lines+markers",
        line=dict(width=3, color="purple"),
        marker=dict(symbol="triangle-up", size=10, color="violet"),
        name="🌪️ Máximo"
    ))
    fig.add_trace(go.Scatter(
        x=df_filtrado["data"], y=df_filtrado["vento_medio"],
        mode="lines+markers",
        line=dict(width=3, color="cyan"),
        marker=dict(symbol="circle", size=8, color="skyblue"),
        name="🍃 Médio"
    ))

    fig.update_layout(layout_legivel(
        f"🌬️ Vento - {ano}{'' if mes=='Todos' else f'/{mes}'}",
        fundo="#E1BEE7"
    ))
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# 6. Precipitação
# --------------------------
with tabs[5]:
    st.title("🌧️ Precipitação (Chuva)")
    df_chuva = load_view("precipitacao_diaria")
    df_filtrado, ano, mes = aplicar_filtros(df_chuva, "data", prefix="chuva")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado["data"],
        y=df_filtrado["rain_max"],
        mode="lines+markers",
        line=dict(width=3, color="blue"),
        marker=dict(size=9, symbol="circle", color="navy"),
        name="🌧️ Precipitação (mm)"
    ))

    fig.update_layout(layout_legivel(
        f"🌧️ Precipitação Máxima Diária - {ano}{'' if mes=='Todos' else f'/{mes}'}",
        fundo="#B3E5FC"
    ))
    st.plotly_chart(fig, use_container_width=True)
