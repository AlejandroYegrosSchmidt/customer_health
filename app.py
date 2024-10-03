import pandas as pd
import gradio as gr
from libs.customer_health import diagnostic 

intro_text = '''
How Py.customer_health work:
Py.customer_health creates a universe for each type of customer, and within each universe, it generates six indicators. For each indicator, it creates an index value used to evaluate each customer. The indicators are as follows: 

Each index values have the range from 0 to 100 where 0 it is a low (bad) values and 100 it is hight values (good) 
1-Days since last sales: Days have passed between the most recent transaction of the selected customer and the maximum date in the dataset
2-Customer age in days:It is the age of the customer, calculated using the date of the first transaction and the date of last transaction
3-Recency: It is the average days that have passed between each transaction of the customer
4-Sku number: It is the quantity of SKUs that the customer has been bought
5-Frecuency: It is the number of time that the customer bought. This measure consideres one transaction per days
6-Indicator Key: It can be the sales amount or the quantities anyway there is a business decision'''




def test(*args):
    args = list(args)
    df = pd.read_csv(args[0],low_memory=False)

    diag = diagnostic(
        data=df,
        col_date=args[1],
        col_customer_code=args[2],
        col_sku_code=args[3],
        ikey=args[4],
        col_customer_type=args[5],
        select_customer=args[6]
    )
    benchmark = diag.indicator_outcome(customer_list=[args[6]]).T.reset_index()
    benchmark.columns = ['Indicator', 'index values']
    return benchmark

def app():
    with gr.Blocks() as customer_health_app:
        gr.Markdown('# How to uses Py.customer_health')
        gr.TextArea(label='Hello word', value=intro_text)
        # ==================================================
        # Setting the inputs
        # ==================================================
        gr.Markdown('# Upload your csv file:')
        with gr.Row():
            file = gr.File(label='Upload your csv file')
        gr.Markdown('# Write the name of each column that contains:')
        with gr.Row():
            # ==================================================
            # Create the customer list
            # ==================================================

            with gr.Column():
                col_date = gr.Textbox(label='Dates')
                col_ikey = gr.Textbox(label='Indicator key' )
                col_customer_type = gr.Textbox(label='Customer type' )
            with gr.Column():
                col_customer_code = gr.Textbox(label='Customer code' )
                col_sku_code = gr.Textbox(label='SKU code' )
        gr.Markdown('# Insert the customer code that wants to create the diagnostis')
        with gr.Row():
            customer_list = gr.Textbox(label='Customer Code')

        # ==================================================
        # Agregamos el título
        # ==================================================    
        gr.Markdown('# Customer Health')
        with gr.Row():               
            with gr.Column(scale=1):
                evaluate_button = gr.Button('Analizar')
        
        # ==================================================
        # Creamos el objeto result y evaluate button
        # ==================================================
        with gr.Row():
            result = gr.Dataframe(label='Diagnostic', col_count=2)

        # Run the python scripts                
        evaluate_button.click(
            fn=test,
            inputs=[file, col_date, col_customer_code, col_sku_code, col_ikey, col_customer_type, customer_list],
            outputs=result
            )
    customer_health_app.launch()
    
app()
