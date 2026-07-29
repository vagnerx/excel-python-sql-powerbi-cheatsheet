"""
create_db.py - Inicializa e popula o banco de dados SQLite
============================================================
Lê os CSVs da pasta datasets/ e cria o banco datasets/cheatsheet.db
Demonstra também DDL (Create Table, Índices, Constraints).
"""

import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
DB_PATH = os.path.join(DATASETS_DIR, "cheatsheet.db")

def create_and_populate():
    print(f"Criando banco de dados em: {DB_PATH}")
    
    # Se ja existe, remove para recriar
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. DDL: Criação manual das tabelas com restrições
    cursor.execute("""
    CREATE TABLE customers (
        id_cliente INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        cidade TEXT,
        segmento TEXT,
        data_cadastro DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        departamento TEXT,
        cargo TEXT,
        cidade TEXT,
        salario REAL,
        data_admissao DATE,
        ativo TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE orders (
        id_pedido INTEGER PRIMARY KEY,
        id_cliente INTEGER,
        id_produto INTEGER,
        quantidade INTEGER,
        valor_unit REAL,
        valor_total REAL,
        data_pedido DATE,
        FOREIGN KEY (id_cliente) REFERENCES customers(id_cliente)
    )
    """)

    # 2. DDL: Criação de índices para performance
    cursor.execute("CREATE INDEX idx_emp_depto ON employees(departamento)")
    cursor.execute("CREATE INDEX idx_ord_cliente ON orders(id_cliente)")
    cursor.execute("CREATE INDEX idx_ord_data ON orders(data_pedido)")

    conn.commit()

    # 3. Importar CSVs via Pandas para dentro do SQLite
    print("Importando dados dos CSVs...")
    
    df_cust = pd.read_csv(os.path.join(DATASETS_DIR, "customers.csv"))
    df_cust.to_sql("customers", conn, if_exists="append", index=False)
    
    df_emp = pd.read_csv(os.path.join(DATASETS_DIR, "employees.csv"))
    df_emp.to_sql("employees", conn, if_exists="append", index=False)
    
    df_ord = pd.read_csv(os.path.join(DATASETS_DIR, "orders.csv"))
    df_ord.to_sql("orders", conn, if_exists="append", index=False)

    print("Dados inseridos com sucesso!")

    # Validando os dados
    print("\nResumo das tabelas criadas:")
    for table in ["customers", "employees", "orders"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f" - {table}: {count} linhas")

    conn.close()
    print("\n[OK] Banco SQLite inicializado.")

if __name__ == "__main__":
    create_and_populate()
