# Datasets

Para praticar todos os exemplos deste cheat sheet, você pode utilizar os datasets que geramos para este repositório. Todos eles estão na pasta `datasets/`.

## 1. Funcionários (`employees.csv`)

Este é o dataset principal utilizado em 90% dos exemplos. Ele simula uma base de RH com dados cadastrais e salariais.

- **Linhas:** 52
- **Colunas:**
  - `id`: Identificador único (Int)
  - `nome`: Nome completo (String)
  - `departamento`: Setor onde trabalha (String - ex: TI, Vendas, RH)
  - `cargo`: Posição na empresa (String)
  - `cidade`: Cidade de residência (String)
  - `salario`: Remuneração mensal (Float). *Atenção: possui valores nulos propositais para treinar tratamento de dados.*
  - `data_admissao`: Data de contratação (Date - AAAA-MM-DD)
  - `ativo`: Status atual (String - Sim/Não)

[⬇️ Baixar employees.csv](https://raw.githubusercontent.com/vagnerx/excel-python-sql-powerbi-cheatsheet/main/datasets/employees.csv)

---

## 2. Clientes (`customers.csv`)

Dataset auxiliar para treinar operações relacionais (PROCV, JOINs).

- **Linhas:** 20
- **Colunas:**
  - `id_cliente`: Identificador (Int)
  - `nome`: Nome da empresa/cliente (String)
  - `cidade`: Localização (String)
  - `segmento`: Área de atuação (String - Varejo, Tecnologia, etc.)
  - `data_cadastro`: Quando virou cliente (Date)

[⬇️ Baixar customers.csv](https://raw.githubusercontent.com/vagnerx/excel-python-sql-powerbi-cheatsheet/main/datasets/customers.csv)

---

## 3. Pedidos (`orders.csv`)

Dataset transacional (Fato) para cruzamento de dados temporais e consolidação.

- **Linhas:** 100
- **Colunas:**
  - `id_pedido`: Chave primária do pedido (Int)
  - `id_cliente`: Chave estrangeira ligando ao `customers.csv` (Int)
  - `id_produto`: Código do item (Int)
  - `quantidade`: Volume vendido (Int)
  - `valor_unit`: Preço de tabela (Float)
  - `valor_total`: `quantidade` × `valor_unit` (Float)
  - `data_pedido`: Data da transação (Date)

[⬇️ Baixar orders.csv](https://raw.githubusercontent.com/vagnerx/excel-python-sql-powerbi-cheatsheet/main/datasets/orders.csv)

---

## Como carregar nos scripts?

### Em Python (Pandas)
```python
import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/vagnerx/excel-python-sql-powerbi-cheatsheet/main/datasets/employees.csv")
```

### No Power BI
Selecione **Obter Dados > Web** e cole a URL raw acima.
