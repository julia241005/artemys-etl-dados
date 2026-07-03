import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Configuração do ambiente
load_dotenv()
password = os.getenv("DB_PASSWORD")

# String de conexão configurada para o banco Artemys
conn_str = f"mssql+pyodbc:///?odbc_connect=Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:servidor-etl-v5.database.windows.net,1433;Database=db_etl_dados;Uid=admin_etl;Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
engine = create_engine(conn_str)

# 2. Configuração da página e Branding
st.set_page_config(page_title="Artemys Dashboard", page_icon="🐾")

st.title("🐾 Dashboard de Socorro Emergencial - Artemys")
st.write("Monitoramento em tempo real de atendimentos e status de ambulâncias.")

# 3. Leitura dos dados da nova tabela de chamados
try:
    query = "SELECT * FROM tb_chamados_artemys"
    df = pd.read_sql(query, engine)

    # 4. Exibição da Tabela
    st.subheader("Lista de Chamados Atuais")
    st.dataframe(df, use_container_width=True)

    # 5. Colunas para gráficos (lado a lado)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Status dos Atendimentos")
        # Conta quantos chamados estão em cada status
        status_counts = df['status_socorro'].value_counts()
        st.bar_chart(status_counts)

    with col2:
        st.subheader("Tipos de Emergência")
        # Conta quantos chamados estão em cada tipo
        emergencia_counts = df['tipo_emergencia'].value_counts()
        st.bar_chart(emergencia_counts)

except Exception as e:
    st.error("Ops! Ainda não encontrei a tabela 'tb_chamados_artemys' no banco.")
    st.info("Certifique-se de que o script ETL (etl_process.py) foi executado com sucesso primeiro.")