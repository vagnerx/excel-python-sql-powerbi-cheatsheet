"""
06_advanced.py â€” Analytics Avancado
======================================
Demonstra ranking, percentual, coluna condicional,
pivot/melt, janela movel e acumulado.

Execute: python examples/python/06_advanced.py
Datasets: datasets/employees.csv, datasets/orders.csv
"""

import os
import numpy as np
import pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
DATASETS = os.path.join(BASE, "datasets")

emp   = pd.read_csv(os.path.join(DATASETS, "employees.csv"))
ord_  = pd.read_csv(os.path.join(DATASETS, "orders.csv"))
ord_["data_pedido"] = pd.to_datetime(ord_["data_pedido"], errors="coerce")


def sep(titulo):
    print(f"\n{'='*65}\n{titulo}\n{'='*65}")


def ranking():
    sep("1. RANKING")
    df = emp.dropna(subset=["salario"]).copy()

    # Ranking global
    df["rank_geral"] = df["salario"].rank(method="dense", ascending=False).astype("Int64")

    # Ranking por departamento
    df["rank_depto"] = (
        df.groupby("departamento")["salario"]
        .rank(method="dense", ascending=False)
        .astype("Int64")
    )

    print("Top 10 por ranking geral:")
    print(
        df.sort_values("rank_geral")
        [["rank_geral", "nome", "departamento", "salario", "rank_depto"]]
        .head(10)
        .to_string(index=False)
    )

    # Top 2 de cada departamento
    top2 = df[df["rank_depto"] <= 2].sort_values(["departamento", "rank_depto"])
    print("\nTop 2 por departamento:")
    print(top2[["departamento", "rank_depto", "nome", "salario"]].to_string(index=False))


def percentual():
    sep("2. PERCENTUAL")
    df = emp.dropna(subset=["salario"]).copy()
    total = df["salario"].sum()

    # % individual no total
    df["pct_folha"] = (df["salario"] / total * 100).round(2)

    # % por departamento
    pct_depto = (
        df.groupby("departamento")["salario"].sum()
        .div(total).mul(100).round(1)
        .sort_values(ascending=False)
        .rename("pct_folha_%")
    )
    print("Participacao % por departamento na folha:")
    print(pct_depto.to_string())

    # % dentro do proprio departamento (transform)
    df["total_depto"] = df.groupby("departamento")["salario"].transform("sum")
    df["pct_no_depto"] = (df["salario"] / df["total_depto"] * 100).round(1)
    print("\nAmostra â€” % do funcionario dentro do depto:")
    print(df[["nome", "departamento", "salario", "pct_no_depto"]]
          .sort_values(["departamento", "pct_no_depto"], ascending=[True, False])
          .head(8).to_string(index=False))


def coluna_condicional():
    sep("3. COLUNA CONDICIONAL")
    df = emp.copy()

    # np.where (binario)
    df["senioridade"] = np.where(df["salario"] > 8000, "Senior", "Junior")

    # np.select (multiplas condicoes)
    condicoes = [
        df["salario"] > 12_000,
        df["salario"] > 8_000,
        df["salario"] > 5_000,
    ]
    niveis = ["Especialista", "Senior", "Pleno"]
    df["nivel"] = np.select(condicoes, niveis, default="Junior")

    # Map
    df["status_label"] = df["ativo"].map({"Sim": "Ativo", "Nao": "Inativo"})

    print(df[["nome", "salario", "nivel", "senioridade"]].head(10).to_string(index=False))
    print("\nDistribuicao de niveis:")
    print(df["nivel"].value_counts().to_string())


def pivot_e_melt():
    sep("4. PIVOT / UNPIVOT (pivot_table e melt)")
    df = emp.dropna(subset=["salario", "departamento", "ativo"]).copy()

    # Pivot
    pivot = df.pivot_table(
        values="salario",
        index="departamento",
        columns="ativo",
        aggfunc=["mean", "count"],
        fill_value=0,
    ).round(2)
    print("PIVOT â€” Media e contagem por depto e status:")
    print(pivot.to_string())

    # Unpivot com orders
    orders_long = ord_.melt(
        id_vars=["id_pedido", "id_cliente", "id_produto", "data_pedido"],
        value_vars=["valor_unit", "valor_total"],
        var_name="tipo_valor",
        value_name="valor",
    )
    print(f"\nUNPIVOT â€” orders de wide para long: {len(orders_long)} linhas")
    print(orders_long.head(6).to_string(index=False))


def janela_movel():
    sep("5. JANELA MOVEL (rolling)")
    diario = (
        ord_.dropna(subset=["data_pedido"])
        .groupby("data_pedido")["valor_total"].sum()
        .reset_index()
        .sort_values("data_pedido")
        .set_index("data_pedido")
    )
    diario["mm_7d"]   = diario["valor_total"].rolling("7D").mean().round(2)
    diario["mm_14d"]  = diario["valor_total"].rolling("14D").mean().round(2)
    diario["max_7d"]  = diario["valor_total"].rolling("7D").max()

    print(diario.tail(10).to_string())


def acumulado():
    sep("6. ACUMULADO (cumsum)")
    mensal = (
        ord_.dropna(subset=["data_pedido"])
        .groupby(ord_["data_pedido"].dt.to_period("M"))["valor_total"]
        .sum()
        .reset_index()
    )
    mensal.columns = ["mes", "receita_mes"]
    mensal["receita_acumulada"] = mensal["receita_mes"].cumsum().round(2)
    mensal["crescimento_pct"] = (
        mensal["receita_mes"].pct_change() * 100
    ).round(1)
    print(mensal.to_string(index=False))


def top_n():
    sep("7. TOP N POR GRUPO")
    df = emp.dropna(subset=["salario"]).copy()

    # Top 3 salarios de cada departamento
    top3 = (
        df.sort_values("salario", ascending=False)
        .groupby("departamento")
        .head(3)
        .sort_values(["departamento", "salario"], ascending=[True, False])
    )
    print("Top 3 salarios por departamento:")
    print(top3[["departamento", "nome", "salario"]].to_string(index=False))


if __name__ == "__main__":
    print("ANALYTICS AVANCADO â€” Cheat Sheet Python")
    ranking()
    percentual()
    coluna_condicional()
    pivot_e_melt()
    janela_movel()
    acumulado()
    top_n()
    print("\n[OK] Script 06_advanced.py concluido.")
