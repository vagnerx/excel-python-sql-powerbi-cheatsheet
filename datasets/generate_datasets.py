"""
generate_datasets.py
====================
Gera os datasets de prática para o repositório:
  - employees.csv   → dataset principal (50+ linhas, nulos, duplicatas)
  - customers.csv   → para exemplos de JOIN
  - orders.csv      → para exemplos de JOIN e agregações

Execute: python datasets/generate_datasets.py
"""

import csv
import os
from datetime import date, timedelta
import random

random.seed(42)  # Reprodutibilidade

# ── Diretório de saída ──────────────────────────────────────────────────────
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ── Helpers ─────────────────────────────────────────────────────────────────
def rand_date(start: date, end: date) -> str:
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).isoformat()


def maybe_null(value, probability: float = 0.08):
    """Retorna vazio com a probabilidade dada (simula nulos no CSV)."""
    return "" if random.random() < probability else value


# ── T0.1 — employees.csv ────────────────────────────────────────────────────
departamentos = ["TI", "Vendas", "RH", "Financeiro", "Marketing", "Operações"]
cargos = {
    "TI":         ["Analista", "Desenvolvedor", "Arquiteto", "DBA"],
    "Vendas":     ["Representante", "Gerente de Contas", "SDR", "Key Account"],
    "RH":         ["Analista RH", "HRBP", "Recruiter", "Gerente RH"],
    "Financeiro": ["Analista Financeiro", "Controller", "Tesoureiro", "Contador"],
    "Marketing":  ["Analista Marketing", "Designer", "Copywriter", "Gestor Tráfego"],
    "Operações":  ["Analista Operações", "Supervisor", "Coordenador", "Gerente Ops"],
}
nomes = [
    "Ana", "Carlos", "João", "Maria", "Pedro", "Fernanda", "Lucas", "Juliana",
    "Rafael", "Camila", "Bruno", "Larissa", "Diego", "Patrícia", "Thiago",
    "Renata", "Felipe", "Daniela", "Rodrigo", "Amanda", "Gustavo", "Vanessa",
    "Eduardo", "Aline", "Marcos", "Cristina", "Leonardo", "Priscila", "André",
    "Tatiana", "Vinícius", "Mariana", "Leandro", "Beatriz", "Ricardo", "Érica",
    "Matheus", "Letícia", "Fábio", "Natália", "Henrique", "Sabrina", "Igor",
    "Carla", "Otávio", "Simone", "Gabriel", "Mônica", "Marcelo", "Helena",
]
cidades = ["São Paulo", "Rio de Janeiro", "Porto Alegre", "Curitiba", "Belo Horizonte",
           "Salvador", "Fortaleza", "Manaus", "Recife", "Brasília"]

faixa_salarial = {
    "TI":         (5_000, 18_000),
    "Vendas":     (3_000, 12_000),
    "RH":         (3_500, 10_000),
    "Financeiro": (4_500, 16_000),
    "Marketing":  (3_000, 11_000),
    "Operações":  (2_800,  9_000),
}

employees = []
for i, nome in enumerate(nomes, start=1):
    dept = random.choice(departamentos)
    cargo = random.choice(cargos[dept])
    sal_min, sal_max = faixa_salarial[dept]
    salario = round(random.uniform(sal_min, sal_max), 2)
    data_admissao = rand_date(date(2018, 1, 1), date(2025, 6, 30))
    ativo = random.choices(["Sim", "Não"], weights=[85, 15])[0]
    cidade = random.choice(cidades)
    employees.append({
        "id":            i,
        "nome":          nome,
        "departamento":  maybe_null(dept),
        "cargo":         maybe_null(cargo),
        "cidade":        cidade,
        "salario":       maybe_null(round(salario, 2)),
        "data_admissao": maybe_null(data_admissao),
        "ativo":         ativo,
    })

# Duplicata intencional (linhas 51-52): repetir linha 5 e linha 12
employees.append({**employees[4], "id": 51})  # duplicata de Pedro
employees.append({**employees[11], "id": 52})  # duplicata de Juliana

emp_path = os.path.join(OUT_DIR, "employees.csv")
with open(emp_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id","nome","departamento","cargo",
                                           "cidade","salario","data_admissao","ativo"])
    writer.writeheader()
    writer.writerows(employees)

print(f"[OK] employees.csv  -> {len(employees)} linhas  ({emp_path})")


# ── T0.2 — customers.csv ────────────────────────────────────────────────────
segmentos = ["Varejo", "Corporativo", "PME", "Governo", "Internacional"]
nomes_clientes = [
    "Alpha Comercial", "Beta Distribuidora", "Gamma Tech", "Delta Serviços",
    "Epsilon Logística", "Zeta Consultoria", "Eta Importadora", "Theta Varejo",
    "Iota Indústrias", "Kappa Saúde", "Lambda Educação", "Mu Financeira",
    "Nu Agropecuária", "Xi Construção", "Omicron Telecom", "Pi Energia",
    "Rho Seguros", "Sigma Alimentos", "Tau Farmácia", "Upsilon Moda",
]

customers = []
for i, nome in enumerate(nomes_clientes, start=1):
    customers.append({
        "id_cliente":    i,
        "nome":          nome,
        "cidade":        random.choice(cidades),
        "segmento":      random.choice(segmentos),
        "data_cadastro": rand_date(date(2019, 1, 1), date(2025, 6, 30)),
    })

cust_path = os.path.join(OUT_DIR, "customers.csv")
with open(cust_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id_cliente","nome","cidade",
                                           "segmento","data_cadastro"])
    writer.writeheader()
    writer.writerows(customers)

print(f"[OK] customers.csv  -> {len(customers)} linhas  ({cust_path})")


# ── T0.3 — orders.csv ───────────────────────────────────────────────────────
produtos = [
    ("P001", "Notebook",   3_500, 8_000),
    ("P002", "Monitor",      900, 2_500),
    ("P003", "Teclado",      150,   500),
    ("P004", "Mouse",         80,   300),
    ("P005", "Headset",      250,   800),
    ("P006", "Webcam",       350, 1_000),
    ("P007", "SSD 1TB",      500, 1_500),
    ("P008", "Mesa Gamer",   800, 3_000),
    ("P009", "Cadeira",    1_200, 4_500),
    ("P010", "Hub USB",      100,   350),
]

orders = []
for i in range(1, 101):
    prod_id, _, preco_min, preco_max = random.choice(produtos)
    cliente_id = random.randint(1, len(customers))
    quantidade = random.randint(1, 10)
    valor_unit = round(random.uniform(preco_min, preco_max), 2)
    valor_total = round(quantidade * valor_unit, 2)
    data_pedido = rand_date(date(2023, 1, 1), date(2025, 6, 30))
    orders.append({
        "id_pedido":    i,
        "id_cliente":   cliente_id,
        "id_produto":   prod_id,
        "quantidade":   quantidade,
        "valor_unit":   valor_unit,
        "valor_total":  valor_total,
        "data_pedido":  data_pedido,
    })

ord_path = os.path.join(OUT_DIR, "orders.csv")
with open(ord_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id_pedido","id_cliente","id_produto",
                                           "quantidade","valor_unit","valor_total",
                                           "data_pedido"])
    writer.writeheader()
    writer.writerows(orders)

print(f"[OK] orders.csv     -> {len(orders)} linhas  ({ord_path})")
print("\nTodos os datasets gerados com sucesso!")
print(f"   Pasta: {OUT_DIR}")
