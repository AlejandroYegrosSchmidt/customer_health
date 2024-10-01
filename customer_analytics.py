import pandas as pd 
from libs.customer_health import diagnostic 

df = pd.read_csv(r'dataset\dataset_food_manora.csv', low_memory=False, index_col=None)
df = df.drop(columns='Unnamed: 0', index=1)

diag = diagnostic(
    data=df,
    col_date='fecha',
    col_customer_code='cod_cliente',
    col_sku_code= 'cod_art',
    ikey='kilos',
    col_customer_type='_canal_cliente',
    select_customer='17017manora'
)

universal = diag.universal_analytic(customer_list=['17017manora']).T.reset_index()
frecuency = diag.benchmark(indicator=5)