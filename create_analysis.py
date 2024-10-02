import pandas as pd 
from libs.customer_health import diagnostic 

df = pd.read_csv(r'dataset\dataset_food_recoleta.csv', low_memory=False, index_col=None)


diag = diagnostic(
        data=df,
        col_date='fecha',
        col_customer_code='cod_cliente',
        col_sku_code= 'cod_art',
        ikey='kilos',
        col_customer_type='_canal_cliente',
        select_customer='895recoleta211350840014'
)

benchmark = diag.benchmark(indicator=1)
universal = diag.indicator_outcome(customer_list=['895recoleta211350840014']).T.reset_index()

