"""
03_grouping.py â€” Agrupar e Agregar Dados
==========================================
Demonstra groupby, agg, pivot_table, value_counts e transform.

Execute: python examples/python/03_grouping.py
Dataset: datasets/employees.csv
"""

import os
import pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
DATASETS = os.path.join(BASE, "datasets")

df = pd.read_csv(os.path.join(DATASETS, "employees.csv"))


def sep(titulo):
    print(f"\n{'='*60}\n{titulo}\n{'='*60}")


def groupby_simples():
    sep("1. GROUPBY SIMPLES")
    resultado = df.groupby("departamento")["salario"].mean().round(2)
    print("Media salarial por departamento:")
    print(resultado.sort_values(ascending=False).to_string())


def groupby_multiplas_metricas():
    sep("2. GROUPBY COM MULTIPLAS METRICAS (agg)")
    resumo = df.groupby("departamento").agg(
        funcionarios=("id", "count"),
        salario_medio=("salario", "mean"),
        salario_total=("salario", "sum"),
        salario_max=("salario", "max"),
        salario_min=("salario", "min"),
    ).round(2)
    print(resumo.sort_values("salario_total", ascending=False).to_string())


def groupby_multiplos_grupos():
    sep("3. GROUPBY POR MULTIPLOS GRUPOS")
    resultado = (
        df.groupby(["departamento", "ativo"])["salario"]
        .agg(["count", "mean"])
        .round(2)
        .rename(columns={"count": "qtd", "mean": "media"})
    )
    print(resultado.to_string())


def value_counts():
    sep("4. VALUE_COUNTS â€” distribuicao de valores")
    print("Funcionarios por departamento:")
    print(df["departamento"].value_counts().to_string())

    print("\nDistribuicao por status ativo:")
    print(df["ativo"].value_counts(normalize=True).mul(100).round(1).to_string())


def pivot_table():
    sep("5. PIVOT TABLE â€” Tabela Dinamica")
    pivot = df.pivot_table(
        values="salario",
        index="departamento",
        columns="ativo",
        aggfunc="mean",
        fill_value=0,
    ).round(2)
    print("Media salarial por departamento e status:")
    print(pivot.to_string())


def pivot_multi_metrica():
    sep("6. PIVOT TABLE COM MULTIPLAS METRICAS")
    pivot = df.pivot_table(
        values="salario",
        index="departamento",
        aggfunc=["count", "mean", "sum"],
    ).round(2)
    pivot.columns = ["qtd", "media", "total"]
    print(pivot.sort_values("total", ascending=False).to_string())


def transform_pct():
    sep("7. TRANSFORM â€” participacao % dentro do grupo")
    df2 = df.dropna(subset=["salario", "departamento"]).copy()
    df2["total_depto"] = df2.groupby("departamento")["salario"].transform("sum")
    df2["pct_no_depto"] = (df2["salario"] / df2["total_depto"] * 100).round(1)
    print(df2[["nome", "departamento", "salario", "pct_no_depto"]]
          .sort_values(["departamento", "pct_no_depto"], ascending=[True, False])
          .head(10).to_string(index=False))


def having_equivalente():
    sep("8. EQUIVALENTE AO HAVING DO SQL")
    # Filtrar grupos com mais de 8 funcionarios
    contagem = df.groupby("departamento")["id"].count()
    deptos_grandes = contagem[contagem > 8].index
    resultado = df[df["departamento"].isin(deptos_grandes)]
    print(f"Departamentos com mais de 8 funcionarios: {list(deptos_grandes)}")
    print(resultado["departamento"].value_counts().to_string())


if __name__ == "__main__":
    print("AGRUPAR E AGREGAR â€” Cheat Sheet Python")
    groupby_simples()
    groupby_multiplas_metricas()
    groupby_multiplos_grupos()
    value_counts()
    pivot_table()
    pivot_multi_metrica()
    transform_pct()
    having_equivalente()
    print("\n[OK] Script 03_grouping.py concluido.")
