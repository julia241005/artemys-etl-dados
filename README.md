# Artemys — Pipeline ETL e painel de chamados

Pipeline de ETL em Python que trata dados de chamados de emergência veterinária e os carrega no **Azure SQL Database**, com um painel em **Streamlit** para acompanhar os atendimentos.

Faz parte do projeto **Artemys**, uma plataforma de apoio a donos de pets em situações de emergência.

## Como funciona

```
Dados de chamados  →  Transformação (Pandas)  →  Azure SQL Database  →  Painel Streamlit
     (extract)            (transform)                 (load)
```

1. **Extração:** gera um conjunto de chamados de exemplo (nome do pet, tipo de emergência e status).
2. **Transformação:** remove espaços extras, padroniza o status em maiúsculas e o tipo de emergência.
3. **Carga:** grava os dados tratados na tabela `tb_chamados_artemys` do Azure SQL.
4. **Painel:** o `app.py` lê a tabela e mostra a lista de chamados e gráficos por status e por tipo de emergência.

Cada execução do ETL é registrada no arquivo `etl_log.log`.

## Tecnologias

- Python, Pandas
- SQLAlchemy e pyodbc (ODBC Driver 18 for SQL Server)
- Azure SQL Database
- Streamlit
- python-dotenv para as credenciais

## Como executar

Pré-requisitos: Python 3.10+, o [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server) e um banco Azure SQL.

```bash
pip install -r requirements.txt
cp .env.example .env        # preencha com os dados do seu banco
python etl_process.py       # executa o ETL e cria a tabela
streamlit run app.py        # abre o painel no navegador
```

## Segurança

As credenciais ficam no arquivo `.env`, que não vai para o repositório (está no `.gitignore`). Use o `.env.example` como modelo.

## Próximos passos

- Extrair os chamados de uma fonte real (API ou arquivo CSV) em vez dos dados de exemplo
- Testes automatizados das transformações
- Carga incremental em vez de substituir a tabela a cada execução

---

Desenvolvido por [Júlia Duarte Silva](https://julia241005.github.io/mapa_de_carreira/).
