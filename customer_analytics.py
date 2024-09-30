import pandas as pd 
from libs import customer_health

df = pd.read_csv(r'C:\Users\aleja\Desktop\Data Science\GitHub\py.customer_health\dataset.csv', low_memory=False)
df = df[df['distribuidor_x']=='graba']
df = df.iloc[0:100]

ua = customer_health.universo_analytics(
                data=df,
                col_customer_code='cod_cliente',
                col_sku_code= 'cod_art',
                col_date='fecha',
                ikey='kilos',
                col_customer_type='cod_canal'
                )
report = ua.create_report()
#report.to_csv('resultado.csv', sep='|')

print('datos procesados verficar resultados')