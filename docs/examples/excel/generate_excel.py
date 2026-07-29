"""
generate_excel.py - Gera cheatsheet_excel.xlsx
================================================
Cria um arquivo Excel completo com multiplas abas, dados reais
e formulas Excel prontas para estudo.

Abas geradas:
  Dados          - dataset employees raw + formatacao
  Filtros        - exemplos de filtros com formulas
  Agrupamento    - SUMIF, COUNTIF, AVERAGEIF por departamento
  Datas          - ANO, MES, DIA, TODAY, calculos de tempo
  Condicional    - SE, IFS, IFERROR, coluna de nivel
  Lookup         - VLOOKUP, XLOOKUP, INDEX+MATCH
  Metricas       - MIN, MAX, RANK.EQ, LARGE, SUMRPRODUTO

Execute: python docs/examples/excel/generate_excel.py
Dataset: datasets/employees.csv, datasets/customers.csv, datasets/orders.csv
Saida:   docs/examples/excel/cheatsheet_excel.xlsx
"""

import os
import csv
from datetime import datetime

try:
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.styles import (
        Font, PatternFill, Alignment, Border, Side, GradientFill
    )
    from openpyxl.utils import get_column_letter
    from openpyxl.formatting.rule import ColorScaleRule, DataBarRule
except ImportError:
    print("ERRO: openpyxl nao encontrado. Execute: pip install openpyxl")
    raise

# ── Caminhos ─────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT   = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
DATASETS    = os.path.join(REPO_ROOT, "datasets")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "cheatsheet_excel.xlsx")


# ── Estilos ──────────────────────────────────────────────────────────────────
def header_style(ws, row, col, texto, cor_hex="1F4E79"):
    cell = ws.cell(row=row, column=col, value=texto)
    cell.font = Font(bold=True, color="FFFFFF", size=11)
    cell.fill = PatternFill("solid", fgColor=cor_hex)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    return cell


def section_style(ws, row, col, texto, cor_hex="2E75B6"):
    cell = ws.cell(row=row, column=col, value=texto)
    cell.font = Font(bold=True, color="FFFFFF", size=10)
    cell.fill = PatternFill("solid", fgColor=cor_hex)
    cell.alignment = Alignment(horizontal="left", vertical="center")
    return cell


def formula_style(ws, row, col, formula, label=""):
    """Coloca formula e destaca a celula."""
    cell = ws.cell(row=row, column=col, value=formula)
    cell.fill = PatternFill("solid", fgColor="FFF2CC")  # amarelo claro
    cell.font = Font(color="000000", size=10)
    cell.alignment = Alignment(horizontal="left")
    if label:
        ws.cell(row=row, column=col - 1, value=label).font = Font(italic=True, size=10)
    return cell


def thin_border():
    thin = Side(style="thin")
    return Border(left=thin, right=thin, top=thin, bottom=thin)


def apply_table_border(ws, min_row, max_row, min_col, max_col):
    thin = thin_border()
    for row in ws.iter_rows(min_row=min_row, max_row=max_row,
                            min_col=min_col, max_col=max_col):
        for cell in row:
            cell.border = thin


# ── Leitura dos datasets ─────────────────────────────────────────────────────
def read_csv(nome):
    path = os.path.join(DATASETS, nome)
    rows = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


# ── ABA 1: Dados ─────────────────────────────────────────────────────────────
def create_dados(wb):
    ws = wb.active
    ws.title = "Dados"
    ws.sheet_view.showGridLines = True

    # Titulo
    ws.merge_cells("A1:H1")
    cell = ws["A1"]
    cell.value = "Dataset: Funcionarios (employees.csv)"
    cell.font = Font(bold=True, size=14, color="1F4E79")
    cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    # Cabecalhos
    headers = ["ID", "Nome", "Departamento", "Cargo", "Cidade", "Salario", "Data Admissao", "Ativo"]
    cols_w  = [6,    22,     16,              20,      16,        12,       16,              8]

    for i, (h, w) in enumerate(zip(headers, cols_w), start=1):
        header_style(ws, 2, i, h)
        ws.column_dimensions[get_column_letter(i)].width = w

    # Dados
    emp = read_csv("employees.csv")
    cores = ["F2F7FF", "FFFFFF"]  # alternado
    for r, row in enumerate(emp, start=3):
        cor = cores[r % 2]
        fill = PatternFill("solid", fgColor=cor)
        vals = [
            row.get("id",""),
            row.get("nome",""),
            row.get("departamento",""),
            row.get("cargo",""),
            row.get("cidade",""),
            float(row["salario"]) if row.get("salario") else None,
            row.get("data_admissao",""),
            row.get("ativo",""),
        ]
        for c, v in enumerate(vals, start=1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.fill = fill
            cell.alignment = Alignment(vertical="center")
            if c == 6 and v:  # salario
                cell.number_format = 'R$ #,##0.00'
            if c == 7 and v:  # data
                cell.number_format = 'DD/MM/YYYY'

    n_linhas = len(emp) + 2
    apply_table_border(ws, 2, n_linhas, 1, 8)

    # Painel de resumo rapido
    ws.merge_cells("J2:M2")
    section_style(ws, 2, 10, "Resumo Rapido")
    ws.column_dimensions["J"].width = 24
    ws.column_dimensions["K"].width = 16
    ws.column_dimensions["L"].width = 4
    ws.column_dimensions["M"].width = 16

    resumo = [
        ("Total de funcionarios",   "=COUNTA(A3:A54)"),
        ("Total de funcionarios ativos", '=COUNTIF(H3:H54,"Sim")'),
        ("Salario medio",           "=AVERAGE(F3:F54)"),
        ("Maior salario",           "=MAX(F3:F54)"),
        ("Menor salario",           "=MIN(F3:F54)"),
        ("Folha total",             "=SUM(F3:F54)"),
        ("Nulos em salario",        "=COUNTA(F3:F54)-COUNT(F3:F54)"),
    ]
    for i, (label, formula) in enumerate(resumo, start=3):
        ws.cell(row=i, column=10, value=label).font = Font(size=10)
        cell = ws.cell(row=i, column=11, value=formula)
        cell.fill = PatternFill("solid", fgColor="FFF2CC")
        cell.font = Font(bold=True)
        if "AVERAGE" in formula or "MAX" in formula or "MIN" in formula or "SUM" in formula:
            cell.number_format = 'R$ #,##0.00'

    ws.row_dimensions[2].height = 20
    print("  [OK] Aba 'Dados' criada")
    return n_linhas


# ── ABA 2: Filtros ───────────────────────────────────────────────────────────
def create_filtros(wb):
    ws = wb.create_sheet("Filtros")

    ws.merge_cells("A1:F1")
    cell = ws["A1"]
    cell.value = "Exemplos de Filtros com Formulas Excel"
    cell.font = Font(bold=True, size=13, color="1F4E79")
    cell.alignment = Alignment(horizontal="center")
    ws.row_dimensions[1].height = 25

    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 40
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 3
    ws.column_dimensions["E"].width = 30
    ws.column_dimensions["F"].width = 40

    # Coluna de referencia
    section_style(ws, 2, 1, "Descricao")
    section_style(ws, 2, 2, "Formula Excel")
    section_style(ws, 2, 5, "Descricao")
    section_style(ws, 2, 6, "Formula Excel")

    filtros_esq = [
        ("Contar TI",               '=COUNTIF(Dados!C3:C54,"TI")'),
        ("Contar ativos",           '=COUNTIF(Dados!H3:H54,"Sim")'),
        ("Contar salario > 8000",   "=COUNTIF(Dados!F3:F54,\">8000\")"),
        ("Contar nulos salario",    "=COUNTA(Dados!F3:F54)-COUNT(Dados!F3:F54)"),
        ("Soma salario TI",         '=SUMIF(Dados!C3:C54,"TI",Dados!F3:F54)'),
        ("Soma salario > 5000",     '=SUMIF(Dados!F3:F54,">5000",Dados!F3:F54)'),
        ("Media TI",                '=AVERAGEIF(Dados!C3:C54,"TI",Dados!F3:F54)'),
        ("Valor min salario",       "=MIN(Dados!F3:F54)"),
        ("Valor max salario",       "=MAX(Dados!F3:F54)"),
        ("Total geral folha",       "=SUM(Dados!F3:F54)"),
    ]
    filtros_dir = [
        ("COUNTIFS - TI E Ativo",    '=COUNTIFS(Dados!C3:C54,"TI",Dados!H3:H54,"Sim")'),
        ("SUMIFS - Vendas E Ativo",  '=SUMIFS(Dados!F3:F54,Dados!C3:C54,"Vendas",Dados!H3:H54,"Sim")'),
        ("AVERAGEIFS - TI E > 5000",    '=AVERAGEIFS(Dados!F3:F54,Dados!C3:C54,"TI",Dados!F3:F54,">5000")'),
        ("Nome maior salario",        "=INDEX(Dados!B3:B54,MATCH(MAX(Dados!F3:F54),Dados!F3:F54,0))"),
        ("Nome menor salario",        "=INDEX(Dados!B3:B54,MATCH(MIN(Dados!F3:F54),Dados!F3:F54,0))"),
        ("3o maior salario",          "=LARGE(Dados!F3:F54,3)"),
        ("3o menor salario",          "=SMALL(Dados!F3:F54,3)"),
        ("Unicos departamentos",      "=SUMRPRODUTO(1/COUNTIF(Dados!C3:C53,Dados!C3:C53))"),
        ("% salario > 8000",         "=COUNTIF(Dados!F3:F54,\">8000\")/COUNTA(Dados!F3:F54)"),
        ("Folha ativos",              '=SUMIF(Dados!H3:H54,"Sim",Dados!F3:F54)'),
    ]

    for i, (desc, form) in enumerate(filtros_esq, start=3):
        ws.cell(row=i, column=1, value=desc).font = Font(size=10)
        cell = ws.cell(row=i, column=2, value=form)
        cell.fill = PatternFill("solid", fgColor="FFF2CC")
        cell.font = Font(size=10)
        if "AVERAGE" in form or "SUM" in form or "MIN" in form or "MAX" in form or "LARGE" in form:
            cell.number_format = 'R$ #,##0.00'
        if "%" in desc:
            cell.number_format = '0.0%'

    for i, (desc, form) in enumerate(filtros_dir, start=3):
        ws.cell(row=i, column=5, value=desc).font = Font(size=10)
        cell = ws.cell(row=i, column=6, value=form)
        cell.fill = PatternFill("solid", fgColor="E2EFDA")
        cell.font = Font(size=10)
        if "AVERAGE" in form or "SUM" in form or "LARGE" in form or "SMALL" in form:
            cell.number_format = 'R$ #,##0.00'
        if "%" in desc:
            cell.number_format = '0.0%'

    apply_table_border(ws, 2, 12, 1, 2)
    apply_table_border(ws, 2, 12, 5, 6)

    # Nota
    ws.cell(row=14, column=1, value="Nota: As formulas acima referenciam a aba 'Dados'. Certifique-se de que ela existe.").font = Font(italic=True, color="595959", size=9)
    print("  [OK] Aba 'Filtros' criada")


# ── ABA 3: Agrupamento ───────────────────────────────────────────────────────
def create_agrupamento(wb):
    ws = wb.create_sheet("Agrupamento")

    ws.merge_cells("A1:G1")
    cell = ws["A1"]
    cell.value = "Agrupamento por Departamento (equivalente ao GROUP BY)"
    cell.font = Font(bold=True, size=13, color="1F4E79")
    cell.alignment = Alignment(horizontal="center")
    ws.row_dimensions[1].height = 25

    departamentos = ["Financeiro", "Marketing", "Operacoes", "RH", "TI", "Vendas"]

    # Cabecalhos
    headers = ["Departamento", "Qtd Funcionarios", "Salario Total", "Salario Medio", "Maior Salario", "Menor Salario", "% da Folha"]
    widths  = [18, 18, 16, 15, 15, 15, 12]
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        header_style(ws, 2, i, h, cor_hex="375623")
        ws.column_dimensions[get_column_letter(i)].width = w

    total_row = len(departamentos) + 3

    for r, dept in enumerate(departamentos, start=3):
        row_fill = PatternFill("solid", fgColor="F2F7F0" if r % 2 == 0 else "FFFFFF")

        ws.cell(row=r, column=1, value=dept).font = Font(bold=True, size=10)

        formulas = [
            f'=COUNTIF(Dados!C$3:C$54,A{r})',
            f'=SUMIF(Dados!C$3:C$54,A{r},Dados!F$3:F$54)',
            f'=AVERAGEIF(Dados!C$3:C$54,A{r},Dados!F$3:F$54)',
            f'=MAXIFS(Dados!F$3:F$54,Dados!C$3:C$54,A{r})',
            f'=MINIFS(Dados!F$3:F$54,Dados!C$3:C$54,A{r})',
            f'=C{r}/C${total_row}',
        ]
        formats = ["General", 'R$ #,##0.00', 'R$ #,##0.00', 'R$ #,##0.00', 'R$ #,##0.00', '0.00%']

        for c, (form, fmt) in enumerate(zip(formulas, formats), start=2):
            cell = ws.cell(row=r, column=c, value=form)
            cell.fill = PatternFill("solid", fgColor="FFF2CC")
            cell.number_format = fmt
            cell.font = Font(size=10)
            cell.alignment = Alignment(horizontal="right")

        ws.cell(row=r, column=1).fill = row_fill

    # Linha de total
    ws.cell(row=total_row, column=1, value="TOTAL").font = Font(bold=True, size=10)
    ws.cell(row=total_row, column=1).fill = PatternFill("solid", fgColor="375623")
    ws.cell(row=total_row, column=1).font = Font(bold=True, color="FFFFFF")

    totais = [
        (2, f'=SUM(B3:B{total_row-1})', "General"),
        (3, f'=SUM(C3:C{total_row-1})', 'R$ #,##0.00'),
        (4, f'=AVERAGE(Dados!F3:F54)',      'R$ #,##0.00'),
        (5, f'=MAX(Dados!F3:F54)',     'R$ #,##0.00'),
        (6, f'=MIN(Dados!F3:F54)',     'R$ #,##0.00'),
        (7, "=SUM(G3:G8)",               '0.00%'),
    ]
    for col, form, fmt in totais:
        cell = ws.cell(row=total_row, column=col, value=form)
        cell.fill = PatternFill("solid", fgColor="D9E8D4")
        cell.font = Font(bold=True, size=10)
        cell.number_format = fmt

    apply_table_border(ws, 2, total_row, 1, 7)

    # Nota sobre MAXIFS/MINIFS
    ws.cell(row=total_row+2, column=1,
            value="Nota: MAXIFS e MINIFS requerem Excel 2019 ou 365. Em versoes mais antigas, use MAX com IFERROR(INDEX...)").font = Font(italic=True, color="595959", size=9)
    ws.merge_cells(f"A{total_row+2}:G{total_row+2}")

    print("  [OK] Aba 'Agrupamento' criada")


# ── ABA 4: Datas ─────────────────────────────────────────────────────────────
def create_datas(wb):
    ws = wb.create_sheet("Datas")

    ws.merge_cells("A1:F1")
    cell = ws["A1"]
    cell.value = "Trabalhar com Datas no Excel"
    cell.font = Font(bold=True, size=13, color="1F4E79")
    cell.alignment = Alignment(horizontal="center")
    ws.row_dimensions[1].height = 25

    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 38
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 3
    ws.column_dimensions["E"].width = 28
    ws.column_dimensions["F"].width = 38

    section_style(ws, 2, 1, "Funcao / Descricao")
    section_style(ws, 2, 2, "Formula (referencia: Dados!G3 = data_admissao)")
    section_style(ws, 2, 5, "Calculo Avancado")
    section_style(ws, 2, 6, "Formula")

    formulas_basicas = [
        ("Extrair Ano",             "=YEAR(Dados!G3)"),
        ("Extrair Mes",             "=MONTH(Dados!G3)"),
        ("Extrair Dia",             "=DAY(Dados!G3)"),
        ("Nome do Mes",             '=TEXT(Dados!G3,"MMMM")'),
        ("Dia da Semana (nome)",    '=TEXT(Dados!G3,"DDDD")'),
        ("Numero dia semana",       "=WEEKDAY(Dados!G3,2)"),
        ("Trimestre",               "=INT((MONTH(Dados!G3)-1)/3)+1"),
        ("Semana do ano",           "=WEEKNUM(Dados!G3,2)"),
        ("Hoje",                    "=TODAY()"),
        ("Agora",                   "=NOW()"),
    ]
    formulas_avancadas = [
        ("Tempo de casa (dias)",    "=TODAY()-Dados!G3"),
        ("Tempo de casa (anos)",    "=FRAÇÃO.YEAR(Dados!G3,TODAY())"),
        ("Tempo de casa (meses)",   "=EDATE(Dados!G3,0)"),
        ("Data + 30 dias",          "=Dados!G3+30"),
        ("Primeiro dia do mes",     "=DATE(YEAR(Dados!G3),MONTH(Dados!G3),1)"),
        ("Ultimo dia do mes",       "=EOMONTH(Dados!G3,0)"),
        ("Dias entre duas datas",   "=DAYS(TODAY(),Dados!G3)"),
        ("Dias uteis entre datas",  "=WORKDAY(Dados!G3,30)"),
        ("Filtrar ano 2023",        '=COUNTIF(Dados!G3:G54,">=01/01/2023")-COUNTIF(Dados!G3:G54,">=01/01/2024")'),
        ("Mais recente admissao",   "=MAX(Dados!G3:G54)"),
    ]

    for i, (desc, form) in enumerate(formulas_basicas, start=3):
        ws.cell(row=i, column=1, value=desc).font = Font(size=10)
        cell = ws.cell(row=i, column=2, value=form)
        cell.fill = PatternFill("solid", fgColor="FFF2CC")
        cell.font = Font(size=10)
        if "TODAY" in form and "CONT" not in form:
            cell.number_format = "DD/MM/YYYY"
        if "NOW" in form:
            cell.number_format = "DD/MM/YYYY HH:MM"

    for i, (desc, form) in enumerate(formulas_avancadas, start=3):
        ws.cell(row=i, column=5, value=desc).font = Font(size=10)
        cell = ws.cell(row=i, column=6, value=form)
        cell.fill = PatternFill("solid", fgColor="E2EFDA")
        cell.font = Font(size=10)
        if "data" in desc.lower() or "recente" in desc.lower():
            cell.number_format = "DD/MM/YYYY"
        if "anos" in desc.lower():
            cell.number_format = "0.0"

    apply_table_border(ws, 2, 12, 1, 2)
    apply_table_border(ws, 2, 12, 5, 6)
    print("  [OK] Aba 'Datas' criada")


# ── ABA 5: Condicional ───────────────────────────────────────────────────────
def create_condicional(wb):
    ws = wb.create_sheet("Condicional")

    ws.merge_cells("A1:G1")
    cell = ws["A1"]
    cell.value = "Coluna Condicional — SE, IFS, IFERROR, SWITCH"
    cell.font = Font(bold=True, size=13, color="1F4E79")
    cell.alignment = Alignment(horizontal="center")
    ws.row_dimensions[1].height = 25

    headers = ["Nome", "Departamento", "Salario", "Nivel (SE aninhado)", "Nivel (IFS)", "Faixa Salarial", "Ativo Label"]
    widths  = [22, 16, 14, 22, 22, 18, 14]
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        header_style(ws, 2, i, h, cor_hex="7030A0")
        ws.column_dimensions[get_column_letter(i)].width = w

    emp = read_csv("employees.csv")
    for r, row in enumerate(emp, start=3):
        cor = "F9F0FF" if r % 2 == 0 else "FFFFFF"
        fill = PatternFill("solid", fgColor=cor)
        nome  = row.get("nome", "")
        dept  = row.get("departamento", "")
        sal   = float(row["salario"]) if row.get("salario") else None
        ativo = row.get("ativo", "")

        ws.cell(row=r, column=1, value=nome).fill = fill
        ws.cell(row=r, column=2, value=dept).fill = fill
        cell = ws.cell(row=r, column=3, value=sal)
        cell.fill = fill
        cell.number_format = 'R$ #,##0.00'

        # SE aninhado
        cell = ws.cell(row=r, column=4,
                       value=f'=IF(C{r}>12000,"Especialista",IF(C{r}>8000,"Senior",IF(C{r}>5000,"Pleno","Junior")))')
        cell.fill = PatternFill("solid", fgColor="FFF2CC")
        cell.font = Font(size=9)

        # IFS (Excel 2016+)
        cell = ws.cell(row=r, column=5,
                       value=f'=IFS(C{r}>12000,"Especialista",C{r}>8000,"Senior",C{r}>5000,"Pleno",TRUE,"Junior")')
        cell.fill = PatternFill("solid", fgColor="FFF2CC")
        cell.font = Font(size=9)

        # Faixa salarial
        cell = ws.cell(row=r, column=6,
                       value=f'=IF(C{r}>10000,"Alto",IF(C{r}>6000,"Medio","Baixo"))')
        cell.fill = PatternFill("solid", fgColor="E2EFDA")
        cell.font = Font(size=9)

        # Ativo Label
        cell = ws.cell(row=r, column=7,
                       value=f'=IF(Dados!H{r}="Sim","Ativo","Inativo")')
        cell.fill = PatternFill("solid", fgColor="E2EFDA")
        cell.font = Font(size=9)

    n = len(emp) + 2
    apply_table_border(ws, 2, n, 1, 7)
    print("  [OK] Aba 'Condicional' criada")


# ── ABA 6: Lookup ────────────────────────────────────────────────────────────
def create_lookup(wb):
    ws = wb.create_sheet("Lookup")

    ws.merge_cells("A1:G1")
    cell = ws["A1"]
    cell.value = "Lookup — VLOOKUP, XLOOKUP, INDEX+MATCH"
    cell.font = Font(bold=True, size=13, color="1F4E79")
    cell.alignment = Alignment(horizontal="center")
    ws.row_dimensions[1].height = 25

    # Secao de exemplos
    section_style(ws, 2, 1, "ID Buscado")
    section_style(ws, 2, 2, "VLOOKUP — Nome")
    section_style(ws, 2, 3, "VLOOKUP — Departamento")
    section_style(ws, 2, 4, "VLOOKUP — Salario")
    section_style(ws, 2, 5, "XLOOKUP — Cargo")
    section_style(ws, 2, 6, "INDEX+MATCH — Cidade")
    section_style(ws, 2, 7, "IFERROR — seguro")

    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 15
    ws.column_dimensions["E"].width = 22
    ws.column_dimensions["F"].width = 20
    ws.column_dimensions["G"].width = 22

    # IDs para buscar (alguns existem, um nao existe para demonstrar IFERROR)
    ids = [1, 5, 10, 20, 35, 50, 99]
    for r, id_val in enumerate(ids, start=3):
        ws.cell(row=r, column=1, value=id_val).font = Font(bold=True)

        # VLOOKUP
        ws.cell(row=r, column=2,
                value=f'=VLOOKUP(A{r},Dados!$A$3:$H$54,2,FALSE)').fill = PatternFill("solid", fgColor="FFF2CC")
        ws.cell(row=r, column=3,
                value=f'=VLOOKUP(A{r},Dados!$A$3:$H$54,3,FALSE)').fill = PatternFill("solid", fgColor="FFF2CC")
        cell = ws.cell(row=r, column=4,
                value=f'=VLOOKUP(A{r},Dados!$A$3:$H$54,6,FALSE)')
        cell.fill = PatternFill("solid", fgColor="FFF2CC")
        cell.number_format = 'R$ #,##0.00'

        # XLOOKUP (Excel 365 / 2021)
        ws.cell(row=r, column=5,
                value=f'=XLOOKUP(A{r},Dados!$A$3:$A$54,Dados!$D$3:$D$54,"Nao encontrado")').fill = PatternFill("solid", fgColor="E2EFDA")

        # INDEX + MATCH
        ws.cell(row=r, column=6,
                value=f'=INDEX(Dados!$E$3:$E$54,MATCH(A{r},Dados!$A$3:$A$54,0))').fill = PatternFill("solid", fgColor="DDEEFF")

        # IFERROR + VLOOKUP (tratamento de erro)
        ws.cell(row=r, column=7,
                value=f'=IFERROR(VLOOKUP(A{r},Dados!$A$3:$H$54,2,FALSE),"ID nao encontrado")').fill = PatternFill("solid", fgColor="FFE0E0")

    apply_table_border(ws, 2, 3+len(ids)-1, 1, 7)

    # Legenda
    ws.cell(row=12, column=1, value="Amarelo = VLOOKUP  |  Verde = XLOOKUP (Excel 365+)  |  Azul = INDEX+MATCH  |  Vermelho = IFERROR").font = Font(italic=True, color="595959", size=9)
    ws.merge_cells("A12:G12")

    print("  [OK] Aba 'Lookup' criada")


# ── ABA 7: Metricas ──────────────────────────────────────────────────────────
def create_metricas(wb):
    ws = wb.create_sheet("Metricas")

    ws.merge_cells("A1:D1")
    cell = ws["A1"]
    cell.value = "Metricas Avancadas — Ranking, Top N, Percentual"
    cell.font = Font(bold=True, size=13, color="1F4E79")
    cell.alignment = Alignment(horizontal="center")
    ws.row_dimensions[1].height = 25

    headers = ["Nome", "Departamento", "Salario", "Ranking (RANK.EQ)"]
    widths  = [22, 16, 14, 20]
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        header_style(ws, 2, i, h, cor_hex="C55A11")
        ws.column_dimensions[get_column_letter(i)].width = w

    emp = read_csv("employees.csv")
    for r, row in enumerate(emp, start=3):
        cor = "FFF4E6" if r % 2 == 0 else "FFFFFF"
        fill = PatternFill("solid", fgColor=cor)
        nome = row.get("nome","")
        dept = row.get("departamento","")
        sal  = float(row["salario"]) if row.get("salario") else None

        ws.cell(row=r, column=1, value=nome).fill = fill
        ws.cell(row=r, column=2, value=dept).fill = fill
        cell = ws.cell(row=r, column=3, value=sal)
        cell.fill = fill
        cell.number_format = 'R$ #,##0.00'

        n_total = len(emp) + 2
        cell = ws.cell(row=r, column=4,
                       value=f'=RANK.EQ(C{r},$C$3:$C${n_total},0)')
        cell.fill = PatternFill("solid", fgColor="FFF2CC")

    n = len(emp) + 2

    # Painel de metricas
    section_style(ws, 2, 6, "Metrica", cor_hex="C55A11")
    section_style(ws, 2, 7, "Formula", cor_hex="C55A11")
    ws.column_dimensions["F"].width = 24
    ws.column_dimensions["G"].width = 42

    metricas = [
        ("1o maior salario",   "=LARGE($C$3:$C$54,1)"),
        ("2o maior salario",   "=LARGE($C$3:$C$54,2)"),
        ("3o maior salario",   "=LARGE($C$3:$C$54,3)"),
        ("1o menor salario",   "=SMALL($C$3:$C$54,1)"),
        ("Mediana",            "=MEDIAN($C$3:$C$54)"),
        ("Desvio Padrao",      "=STDEV($C$3:$C$54)"),
        ("% acima da media",   "=COUNTIF($C$3:$C$54,\">\"&AVERAGE($C$3:$C$54))/COUNTA($C$3:$C$54)"),
        ("Folha top 10",       "=SUMRPRODUTO(LARGE($C$3:$C$54,{1,2,3,4,5,6,7,8,9,10}))"),
    ]
    for i, (label, form) in enumerate(metricas, start=3):
        ws.cell(row=i, column=6, value=label).font = Font(size=10)
        cell = ws.cell(row=i, column=7, value=form)
        cell.fill = PatternFill("solid", fgColor="FFF2CC")
        cell.font = Font(size=10)
        if "%" in label:
            cell.number_format = "0.0%"
        elif label not in ["Desvio Padrao"]:
            cell.number_format = 'R$ #,##0.00'

    apply_table_border(ws, 2, n, 1, 4)
    apply_table_border(ws, 2, 10, 6, 7)

    print("  [OK] Aba 'Metricas' criada")


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    print("Gerando cheatsheet_excel.xlsx ...")
    wb = Workbook()

    create_dados(wb)
    create_filtros(wb)
    create_agrupamento(wb)
    create_datas(wb)
    create_condicional(wb)
    create_lookup(wb)
    create_metricas(wb)

    wb.save(OUTPUT_FILE)
    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\n[OK] Arquivo salvo: {OUTPUT_FILE}")
    print(f"     Tamanho: {size_kb:.1f} KB")
    print(f"     Abas: {[ws.title for ws in wb.worksheets]}")


if __name__ == "__main__":
    main()
