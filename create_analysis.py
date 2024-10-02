import pandas as pd 
from libs.customer_health import diagnostic 

df_r = pd.read_csv(r'dataset\dataset_food_recoleta.csv', low_memory=False, index_col=None)
#df_r = df.drop(columns='Unnamed: 0', index=1)

diag = diagnostic(
    data=df_r,
    col_date='fecha',
    col_customer_code='cod_cliente',
    col_sku_code= 'cod_art',
    ikey='kilos',
    col_customer_type='_canal_cliente',
    select_customer=None
)
universal = diag.universal_analytic(customer_list=df_r.cod_cliente.unique())
universal.to_csv('dataset_recoleta.csv', index=None)


df_y = pd.read_csv(r'dataset\dataset_food_ykua_sati.csv', low_memory=False, index_col=None)
#df_y = df.drop(columns='Unnamed: 0', index=1)

diag = diagnostic(
    data=df_y,
    col_date='fecha',
    col_customer_code='cod_cliente',
    col_sku_code= 'cod_art',
    ikey='kilos',
    col_customer_type='_canal_cliente',
    select_customer=None
)
universal2 = diag.universal_analytic(customer_list=df_y.cod_cliente.unique())
universal2.to_csv('dataset_ykua_sati.csv', index=None)

