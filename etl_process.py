import os
import urllib.parse
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import logging

# Configuração do log
logging.basicConfig(
    filename='etl_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Carrega as variáveis do arquivo .env
load_dotenv()
password = os.getenv("DB_PASSWORD")

# Configuração da string de conexão Azure
params = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:servidor-etl-v5.database.windows.net,1433;"
    "Database=db_etl_dados;"
    "Uid=admin_etl;"
    f"Pwd={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

conn_str = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(params)}"
engine = create_engine(conn_str)


# ==========================================
# PHASE E: EXTRAÇÃO (Dados de Socorro Pet)
# ==========================================
def extrair_dados():
    print("=== [E] Extraindo dados de chamados de emergência... ===")
    dados_brutos = {
        'id_chamado': [1001, 1002, 1003, 1004],
        'pet_nome': ['Rex', ' Luna ', 'Thor', 'Bolinha'],
        'tipo_emergencia': ['Atropelamento', 'Intoxicação', 'Dificuldade Respiratória', 'Ferimento Grave'],
        'status_socorro': ['pendente', 'em atendimento', 'concluido', 'pendente']
    }
    df = pd.DataFrame(dados_brutos)
    return df


# ==========================================
# PHASE T: TRANSFORMAÇÃO (Limpeza e Padronização)
# ==========================================
def transformar_dados(df):
    print("=== [T] Tratando dados de emergência... ===")
    
    # 1. Limpando espaços em branco nos nomes dos pets
    df['pet_nome'] = df['pet_nome'].str.strip()
    
    # 2. Padronizando status para maiúsculas (para consistência no banco)
    df['status_socorro'] = df['status_socorro'].str.upper()
    
    # 3. Garantindo que o tipo de emergência também esteja padronizado
    df['tipo_emergencia'] = df['tipo_emergencia'].str.capitalize()
    
    return df


# ==========================================
# PHASE L: CARGA (Load)
# ==========================================
def carregar_dados(df_limpo):
    print("=== [L] Injetando chamados na nuvem... ===")
    
    # Agora salvando na tabela correta do projeto Artemys
    df_limpo.to_sql(
        name='tb_chamados_artemys', 
        con=engine, 
        if_exists='replace', 
        index=False
    )
    print("🐾 Sucesso! Chamados do Artemys atualizados com segurança.")


# ==========================================
# EXECUÇÃO
# ==========================================
if __name__ == "__main__":
    logging.info("Iniciando processo ETL Artemys...") 
    try:
        dados = extrair_dados()
        dados_tratados = transformar_dados(dados)
        carregar_dados(dados_tratados)
        logging.info("Pipeline Artemys concluído.")
    except Exception as e:
        logging.error(f"Erro no Pipeline Artemys: {e}")
        print(f"\n❌ Erro no Pipeline: {e}")