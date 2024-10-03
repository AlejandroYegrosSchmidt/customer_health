import pandas as pd
import gradio as gr
from libs.customer_health import diagnostic 

 

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
        # ==================================================
        # Setting the inputs
        # ==================================================
        
        gr.Markdown('# Upload your csv file:')
        with gr.Row():
            file = gr.File(label='Upload your csv file')
        gr.Markdown('# Input Setting:')
        with gr.Row():
            # ==================================================
            # Create the customer list
            # ==================================================

            with gr.Column():
                col_date = gr.Textbox(label='Column that contains dates')
                col_ikey = gr.Textbox(label='Column that contains an indicator key' )
                col_customer_type = gr.Textbox(label='Column that contains a customer type' )
            with gr.Column():
                col_customer_code = gr.Textbox(label='Column that contains a customer code' )
                col_sku_code = gr.Textbox(label='Column that contains a SKU code' )
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
