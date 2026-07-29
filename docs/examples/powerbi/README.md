# Power BI — Cheat Sheet

Este diretório contém a documentação e os scripts em **DAX** e **Power Query (M)** necessários para reproduzir as 24 operações do cheat sheet.

## Como utilizar

O desenvolvimento no Power BI é essencialmente visual. Diferente de Python ou SQL, as lógicas são aplicadas dentro de caixas de edição no **Power BI Desktop**.

Nós preparamos guias temáticos para cada etapa do desenvolvimento no Power BI:

### 1. Power Query (M) — ETL
Como realizar limpezas, joins (mesclar consultas), transformações e pivots.
👉 [Ver Power Query (M)](powerquery-m.md)

### 2. Modelagem (Star Schema)
Como relacionar as tabelas `employees`, `customers` e `orders` da forma otimizada para o Power BI.
👉 [Ver Star Schema](star_schema.md)

### 3. Fórmulas DAX — Medidas
As expressões para operações avançadas: filtros complexos (`CALCULATE`), percentuais, rankings dinâmicos e soma por grupos.
👉 [Ver Medidas DAX](dax.md)

### 4. Inteligência de Tempo (Time Intelligence)
Como calcular Acumulado no Ano (YTD), variações versus ano anterior e médias móveis (Janela Móvel).
👉 [Ver Time Intelligence](time_intelligence.md)

---

## Criando seu próprio `.pbix`

Como o arquivo `.pbix` é um formato binário gerado pela interface da Microsoft, você deve criá-lo seguindo estes passos:

1. Abra o **Power BI Desktop** (versão Windows).
2. Vá em **Obter Dados** > **Texto/CSV** e importe os 3 arquivos da pasta `datasets/` (`employees.csv`, `customers.csv`, `orders.csv`).
3. Abra o **Transformar Dados** (Power Query) e aplique as lógicas do arquivo [powerquery-m.md](powerquery-m.md).
4. Feche e aplique, vá para a visão de **Modelo** e siga o [star_schema.md](star_schema.md) para ligar as tabelas.
5. Vá para a visão de **Dados** e crie uma **Nova Tabela** para a dimensão Calendário, conforme o [time_intelligence.md](time_intelligence.md).
6. Crie uma **Nova Medida** para cada fórmula encontrada no [dax.md](dax.md).
7. Arraste essas medidas para visuais de Matriz, Gráficos de Coluna e Cartões na tela de Relatório.
8. Salve o arquivo como `cheatsheet.pbix` dentro desta pasta `docs/examples/powerbi/`.

> 💡 **Pronto?** Após criar o arquivo e commitar no GitHub, ele estará disponível para download aqui:  
> 📥 **[Baixar cheatsheet.pbix](cheatsheet.pbix)** *(Requer Power BI Desktop para abrir)*

---

## Veja também

- [Exemplos Python](../python/README.md)
- [Exemplos SQL](../sql/README.md)
- [Exemplos Excel](../excel/README.md)
