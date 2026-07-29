"""
run_sql.py - Utilitário para executar scripts SQL no SQLite
=============================================================
Lê arquivos .sql da pasta ou permite rodar queries diretamente,
exibindo o resultado no console formatado via Pandas.

Uso:
  python docs/examples/sql/run_sql.py docs/examples/sql/01_basic.sql
"""

import os
import sys
import sqlite3
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "datasets", "cheatsheet.db")

def run_query(sql_text):
    if not os.path.exists(DB_PATH):
        print("Erro: Banco de dados não encontrado.")
        print("Execute primeiro: python docs/examples/sql/create_db.py")
        return

    conn = sqlite3.connect(DB_PATH)
    queries = [q.strip() for q in sql_text.split(";") if q.strip()]

    for i, q in enumerate(queries, 1):
        print(f"--- Query {i} ---")
        if q.upper().startswith(("SELECT", "WITH", "PRAGMA")):
            try:
                df = pd.read_sql(q, conn)
                if df.empty:
                    print("(Nenhum resultado retornado)\n")
                else:
                    print(df.to_string(index=False))
                    print(f"[{len(df)} linhas retornadas]\n")
            except Exception as e:
                print(f"Erro na execução da query:\n{e}\n")
        else:
            try:
                cursor = conn.cursor()
                cursor.execute(q)
                conn.commit()
                print("Instrução executada com sucesso.\n")
            except Exception as e:
                print(f"Erro na execução do script:\n{e}\n")
            
    conn.close()

def main():
    if len(sys.argv) < 2:
        print("Uso: python run_sql.py <arquivo.sql>")
        print("Ex:  python run_sql.py docs/examples/sql/01_basic.sql")
        return

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        sql = f.read()
    
    print("=" * 60)
    print(f"Executando: {os.path.basename(filepath)}")
    print("=" * 60)
    run_query(sql)

if __name__ == "__main__":
    main()
