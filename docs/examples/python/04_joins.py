"""
04_joins.py â€” Merge / Join
============================
Demonstra INNER, LEFT, RIGHT, OUTER JOIN com Pandas
usando employees, customers e orders.

Execute: python examples/python/04_joins.py
Datasets: datasets/employees.csv, datasets/customers.csv, datasets/orders.csv
"""

import os
import pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
DATASETS = os.path.join(BASE, "datasets")

emp   = pd.read_csv(os.path.join(DATASETS, "employees.csv"))
cust  = pd.read_csv(os.path.join(DATASETS, "customers.csv"))
ord_  = pd.read_csv(os.path.join(DATASETS, "orders.csv"))


def sep(titulo):
    print(f"\n{'='*60}\n{titulo}\n{'='*60}")


def inner_join():
    sep("1. INNER JOIN â€” apenas correspondencias")
    joined = pd.merge(ord_, cust, on="id_cliente", how="inner")
    print(f"Orders: {len(ord_)} | Clientes: {len(cust)} | Inner: {len(joined)}")
    print(joined[["id_pedido", "nome", "cidade", "valor_total"]].head(5).to_string(index=False))


def left_join():
    sep("2. LEFT JOIN â€” todos os pedidos + dados do cliente")
    joined = pd.merge(ord_, cust, on="id_cliente", how="left")
    sem_cliente = joined[joined["nome"].isna()]
    print(f"Total pedidos: {len(joined)} | Sem cliente correspondente: {len(sem_cliente)}")
    print(joined[["id_pedido", "nome", "segmento", "valor_total"]].head(5).to_string(index=False))


def right_join():
    sep("3. RIGHT JOIN â€” todos os clientes + pedidos")
    joined = pd.merge(ord_, cust, on="id_cliente", how="right")
    sem_pedido = joined[joined["id_pedido"].isna()]
    print(f"Total: {len(joined)} | Clientes sem pedido: {len(sem_pedido)}")


def outer_join():
    sep("4. OUTER JOIN â€” todos de ambas as tabelas")
    joined = pd.merge(ord_, cust, on="id_cliente", how="outer")
    print(f"Resultado outer join: {len(joined)} linhas")


def join_encadeado():
    sep("5. JOIN ENCADEADO â€” multiplas tabelas")
    # orders + customers + (simulando um terceiro join)
    base = ord_.merge(cust, on="id_cliente", how="left")
    print(f"Orders + Customers: {len(base)} linhas | Colunas: {list(base.columns)}")

    # Agrupado: total por cliente
    por_cliente = (
        base.groupby(["id_cliente", "nome", "segmento"])
        .agg(
            qtd_pedidos=("id_pedido", "count"),
            total_gasto=("valor_total", "sum"),
            ticket_medio=("valor_total", "mean"),
        )
        .round(2)
        .sort_values("total_gasto", ascending=False)
        .reset_index()
    )
    print("\nTop 10 clientes por total gasto:")
    print(por_cliente.head(10).to_string(index=False))


def anti_join():
    sep("6. ANTI JOIN â€” clientes SEM pedidos")
    # LEFT JOIN + filtrar os que nao tiveram match
    todos = pd.merge(cust, ord_[["id_cliente"]].drop_duplicates(),
                     on="id_cliente", how="left", indicator=True)
    sem_pedido = todos[todos["_merge"] == "left_only"].drop(columns=["_merge"])
    print(f"Clientes sem nenhum pedido: {len(sem_pedido)}")
    if len(sem_pedido) > 0:
        print(sem_pedido[["id_cliente", "nome", "segmento"]].to_string(index=False))
    else:
        print("  (todos os clientes tem pelo menos um pedido)")


def join_com_sufixos():
    sep("7. JOIN COM SUFIXOS â€” evitar conflito de nomes")
    # Simular join onde ambas as tabelas tem coluna 'cidade'
    joined = pd.merge(
        ord_, cust,
        on="id_cliente",
        how="left",
        suffixes=("_pedido", "_cliente"),
    )
    print(f"Colunas geradas: {list(joined.columns)}")


if __name__ == "__main__":
    print("MERGE / JOIN â€” Cheat Sheet Python")
    inner_join()
    left_join()
    right_join()
    outer_join()
    join_encadeado()
    anti_join()
    join_com_sufixos()
    print("\n[OK] Script 04_joins.py concluido.")
