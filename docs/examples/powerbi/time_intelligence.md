# Time Intelligence (DAX)

```DAX
Sales YTD =
TOTALYTD(
    [Total Sales],
    Calendar[Date]
)

Sales LY =
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(
        Calendar[Date]
    )
)
```
