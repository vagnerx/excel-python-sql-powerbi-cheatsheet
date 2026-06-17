import pandas as pd
df=pd.read_csv('../../datasets/employees.csv')
print(df.groupby('department')['salary'].mean())