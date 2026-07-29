"""
05_dates.py â€” Trabalhar com Datas
====================================
Demonstra extraÃ§Ã£o de partes de data, filtros temporais,
tempo de casa, rolling e resampling.

Execute: python examples/python/05_dates.py
Datasets: datasets/employees.csv, datasets/orders.csv
"""

import os
import pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
DATASETS = os.path.join(BASE, "datasets")

emp   = pd.read_csv(os.path.join(DATASETS, "employees.csv"))
ord_  = pd.read_csv(os.path.join(DATASETS, "orders.csv"))

# Converter para datetime
emp["data_admissao"] = pd.to_datetime(emp["data_admissao"], errors="coerce")
ord_["data_pedido"]  = pd.to_datetime(ord_["data_pedido"],  errors="coerce")


def sep(titulo):
    print(f"\n{'='*60}\n{titulo}\n{'='*60}")


def extrair_partes():
    sep("1. EXTRAIR PARTES DA DATA")
    df = emp.dropna(subset=["data_admissao"]).copy()
    df["ano"]        = df["data_admissao"].dt.year
    df["mes"]        = df["data_admissao"].dt.month
    df["dia"]        = df["data_admissao"].dt.day
    df["trimestre"]  = df["data_admissao"].dt.quarter
    df["dia_semana"] = df["data_admissao"].dt.day_name()
    df["nome_mes"]   = df["data_admissao"].dt.month_name()

    print(df[["nome", "data_admissao", "ano", "mes", "trimestre", "dia_semana"]]
          .head(8).to_string(index=False))


def tempo_de_casa():
    sep("2. TEMPO DE CASA")
    df = emp.dropna(subset=["data_admissao"]).copy()
    hoje = pd.Timestamp.today()
    df["dias_empresa"] = (hoje - df["data_admissao"]).dt.days
    df["anos_empresa"] = (df["dias_empresa"] / 365.25).round(1)

    print(df[["nome", "data_admissao", "anos_empresa"]]
          .sort_values("anos_empresa", ascending=False)
          .head(10).to_string(index=False))
    print(f"\nMedia de tempo de casa: {df['anos_empresa'].mean():.1f} anos")


def filtro_por_data():
    sep("3. FILTRAR POR DATA")
    df = emp.dropna(subset=["data_admissao"]).copy()

    # Por ano
    em_2023 = df[df["data_admissao"].dt.year == 2023]
    print(f"Admitidos em 2023: {len(em_2023)}")

    # Por intervalo
    intervalo = df[df["data_admissao"].between("2022-01-01", "2023-12-31")]
    print(f"Admitidos em 2022-2023: {len(intervalo)}")

    # Por trimestre
    q1 = df[df["data_admissao"].dt.quarter == 1]
    print(f"Admitidos no Q1 (jan-mar de qualquer ano): {len(q1)}")


def contratacoes_por_periodo():
    sep("4. CONTRATACOES POR ANO E TRIMESTRE")
    df = emp.dropna(subset=["data_admissao"]).copy()

    por_ano = df.groupby(df["data_admissao"].dt.year)["id"].count()
    por_ano.index.name = "ano"
    por_ano.name = "contratacoes"
    print("Por ano:")
    print(por_ano.to_string())

    por_trim = df.groupby(df["data_admissao"].dt.to_period("Q"))["id"].count()
    print("\nPor trimestre:")
    print(por_trim.to_string())


def pedidos_por_mes():
    sep("5. PEDIDOS POR MES (orders)")
    df = ord_.dropna(subset=["data_pedido"]).copy()
    mensal = (
        df.groupby(df["data_pedido"].dt.to_period("M"))["valor_total"]
        .agg(["count", "sum"])
        .rename(columns={"count": "qtd_pedidos", "sum": "total"})
        .round(2)
    )
    print(mensal.to_string())


def media_movel():
    sep("6. MEDIA MOVEL DE 7 DIAS (rolling)")
    df = ord_.dropna(subset=["data_pedido"]).copy()
    diario = (
        df.groupby("data_pedido")["valor_total"].sum()
        .reset_index()
        .sort_values("data_pedido")
        .set_index("data_pedido")
    )
    diario["media_7d"] = diario["valor_total"].rolling("7D").mean().round(2)
    diario["soma_7d"]  = diario["valor_total"].rolling("7D").sum().round(2)

    print(diario.tail(15).to_string())


def acumulado():
    sep("7. TOTAL ACUMULADO (cumsum)")
    df = ord_.dropna(subset=["data_pedido"]).copy()
    mensal = (
        df.groupby(df["data_pedido"].dt.to_period("M"))["valor_total"]
        .sum()
        .reset_index()
    )
    mensal.columns = ["mes", "total_mes"]
    mensal["acumulado"] = mensal["total_mes"].cumsum().round(2)
    print(mensal.to_string(index=False))


if __name__ == "__main__":
    print("DATAS â€” Cheat Sheet Python")
    extrair_partes()
    tempo_de_casa()
    filtro_por_data()
    contratacoes_por_periodo()
    pedidos_por_mes()
    media_movel()
    acumulado()
    print("\n[OK] Script 05_dates.py concluido.")
