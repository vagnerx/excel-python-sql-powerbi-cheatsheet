"""
02_filtering.py â€” Filtrar Linhas
==================================
Demonstra filtros simples, compostos, com texto e com nulos.

Execute: python examples/python/02_filtering.py
Dataset: datasets/employees.csv
"""

import os
import pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
DATASETS = os.path.join(BASE, "datasets")

df = pd.read_csv(os.path.join(DATASETS, "employees.csv"))
df["data_admissao"] = pd.to_datetime(df["data_admissao"], errors="coerce")


def sep(titulo):
    print(f"\n{'='*55}\n{titulo}\n{'='*55}")


def filtro_simples():
    sep("1. FILTRO SIMPLES")
    resultado = df[df["salario"] > 8000]
    print(f"Salario > 8000: {len(resultado)} funcionarios")
    print(resultado[["nome", "departamento", "salario"]].head(5).to_string(index=False))


def filtro_e():
    sep("2. FILTRO COM 'E' (AND)")
    resultado = df[(df["departamento"] == "TI") & (df["salario"] > 7000)]
    print(f"TI E salario > 7000: {len(resultado)} funcionarios")
    print(resultado[["nome", "departamento", "salario"]].to_string(index=False))


def filtro_ou():
    sep("3. FILTRO COM 'OU' (OR)")
    resultado = df[(df["departamento"] == "TI") | (df["departamento"] == "Financeiro")]
    print(f"TI OU Financeiro: {len(resultado)} funcionarios")
    print(resultado[["nome", "departamento", "salario"]].head(8).to_string(index=False))


def filtro_isin():
    sep("4. FILTRO COM LISTA (isin)")
    deptos = ["TI", "Financeiro", "Marketing"]
    resultado = df[df["departamento"].isin(deptos)]
    print(f"Departamentos {deptos}: {len(resultado)} funcionarios")
    print(resultado["departamento"].value_counts().to_string())


def filtro_texto():
    sep("5. FILTRO COM TEXTO (str.contains)")
    resultado = df[df["nome"].str.contains("a", case=False, na=False)]
    print(f"Nomes com letra 'a': {len(resultado)}")
    print(resultado["nome"].tolist())


def filtro_negacao():
    sep("6. NEGACAO (~)")
    resultado = df[~df["departamento"].isin(["TI", "RH"])]
    print(f"Excluindo TI e RH: {len(resultado)} funcionarios")
    print(resultado["departamento"].value_counts().to_string())


def filtro_nulos():
    sep("7. FILTRO COM NULOS")
    com_salario    = df[df["salario"].notna()]
    sem_salario    = df[df["salario"].isna()]
    com_depto      = df[df["departamento"].notna()]
    print(f"Com salario:        {len(com_salario)}")
    print(f"Sem salario (nulo): {len(sem_salario)}")
    print(f"Com departamento:   {len(com_depto)}")


def filtro_data():
    sep("8. FILTRO POR DATA")
    admitidos_2023 = df[df["data_admissao"].dt.year == 2023]
    recentes = df[df["data_admissao"] >= "2024-01-01"]
    print(f"Admitidos em 2023: {len(admitidos_2023)}")
    print(f"Admitidos a partir de 2024: {len(recentes)}")


def filtro_between():
    sep("9. FILTRO ENTRE VALORES (between)")
    faixa = df[df["salario"].between(5000, 9000)]
    print(f"Salario entre 5000 e 9000: {len(faixa)} funcionarios")


def query_sintaxe():
    sep("10. SINTAXE query() â€” mais legivel")
    resultado = df.query("salario > 7000 and departamento == 'Vendas'")
    print(f"Vendas com salario > 7000: {len(resultado)}")
    print(resultado[["nome", "salario"]].to_string(index=False))


if __name__ == "__main__":
    print("FILTRAR LINHAS â€” Cheat Sheet Python")
    filtro_simples()
    filtro_e()
    filtro_ou()
    filtro_isin()
    filtro_texto()
    filtro_negacao()
    filtro_nulos()
    filtro_data()
    filtro_between()
    query_sintaxe()
    print("\n[OK] Script 02_filtering.py concluido.")
