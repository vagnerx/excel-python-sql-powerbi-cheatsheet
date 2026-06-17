import pandas as pd
df=pd.read_csv('../../datasets/employees.csv',parse_dates=['hire_date'])
print(df['hire_date'].dt.year)