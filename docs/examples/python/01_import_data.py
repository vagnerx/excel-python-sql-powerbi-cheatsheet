"""
01_import_data.py â€” Importar Dados
===================================
Demonstra diferentes formas de importar dados com Pandas:
  - CSV, Excel, JSON, SQL (SQLite), URL

Execute: python examples/python/01_import_data.py
Dataset: datasets/employees.csv
"""

import os
import pandas as pd

# â”€â”€ Caminho base do repositÃ³rio â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
DATASETS = os.path.join(BASE, "datasets")


def importar_csv():
    print("\n" + "=" * 55)
    print("1. IMPORTAR CSV")
    print("=" * 55)

    # Leitura bÃ¡sica
    df = pd.read_csv(os.path.join(DATASETS, "employees.csv"))
    print(f"Shape: {df.shape}  |  Colunas: {list(df.columns)}")
    print(df.head(3).to_string(index=False))

    # Com parÃ¢metros explÃ­citos
    df2 = pd.read_csv(
        os.path.join(DATASETS, "employees.csv"),
        encoding="utf-8",
        sep=",",
        dtype={"id": int, "nome": str},
        parse_dates=["data_admissao"],
    )
    print(f"\nTipos apÃ³s parse_dates:\n{df2.dtypes}")
    return df


def importar_multiplos():
    print("\n" + "=" * 55)
    print("2. IMPORTAR MÃšLTIPLOS CSVs")
    print("=" * 55)

    arquivos = ["employees.csv", "customers.csv", "orders.csv"]
    dataframes = {}
    for arq in arquivos:
        caminho = os.path.join(DATASETS, arq)
        nome = arq.replace(".csv", "")
        dataframes[nome] = pd.read_csv(caminho)
        print(f"  {arq:20s} â†’ {dataframes[nome].shape[0]:>3} linhas")

    return dataframes


def inspecionar_dataframe(df):
    print("\n" + "=" * 55)
    print("3. INSPECIONAR O DATAFRAME")
    print("=" * 55)

    print("\n--- head(5) ---")
    print(df.head(5).to_string(index=False))

    print("\n--- info() ---")
    df.info()

    print("\n--- describe() ---")
    print(df.describe().round(2))

    print("\n--- Nulos por coluna ---")
    nulos = df.isna().sum()
    print(nulos[nulos > 0])

    print(f"\n--- MemÃ³ria: {df.memory_usage(deep=True).sum() / 1024:.1f} KB ---")


def importar_de_url():
    print("\n" + "=" * 55)
    print("4. IMPORTAR DE URL (exemplo)")
    print("=" * 55)
    print("# Exemplo de importaÃ§Ã£o de URL pÃºblica:")
    print("# url = 'https://raw.githubusercontent.com/.../employees.csv'")
    print("# df = pd.read_csv(url)")
    print("# (nÃ£o executado â€” requer conexÃ£o com internet)")


def importar_sqlite():
    print("\n" + "=" * 55)
    print("5. IMPORTAR DE SQLITE")
    print("=" * 55)

    db_path = os.path.join(DATASETS, "cheatsheet.db")
    if os.path.exists(db_path):
        import sqlite3
        conn = sqlite3.connect(db_path)
        df_sql = pd.read_sql("SELECT * FROM employees LIMIT 5", conn)
        conn.close()
        print(df_sql.to_string(index=False))
    else:
        print("  cheatsheet.db nÃ£o encontrado. Execute T2 primeiro.")
        print("  Exemplo de cÃ³digo:")
        print("  import sqlite3")
        print("  conn = sqlite3.connect('datasets/cheatsheet.db')")
        print("  df = pd.read_sql('SELECT * FROM employees', conn)")


if __name__ == "__main__":
    print("=" * 55)
    print(" IMPORTAR DADOS â€” Cheat Sheet Excel > Python > SQL > Power BI")
    print("=" * 55)

    df = importar_csv()
    dataframes = importar_multiplos()
    inspecionar_dataframe(df)
    importar_de_url()
    importar_sqlite()

    print("\n[OK] Script 01_import_data.py concluido.")
