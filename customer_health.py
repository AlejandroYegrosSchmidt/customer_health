# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 21:13:29 2024

@author: Alejandro Yegros
"""

import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler


class customer_autopsy():
    def __init__(self,path,date,customer_code,sku_code,primary_key,select_customer=None):
        self.date = date
        self.customer_code = customer_code
        self.sku_code = sku_code
        self.primary_key = primary_key
        self.path = path
        self.select_customer = select_customer
        self.df = self.dataset()
    def dataset(self):
        df = pd.read_csv(self.path, sep=',', low_memory=False)
        df = df[[self.date, self.customer_code,self.sku_code ,self.primary_key]]
        df[self.date] = pd.to_datetime(df[self.date])
        # Filter the df if the field select customer have a customer code
        df = df if self.select_customer == None else df[df[self.customer_code]==self.select_customer]
        return df          
   # Caracteristicas de los clientes
    def customer_old(self):
        # Calculamos la age que tienen los clientes en función a la self.date de su primera compra vs su última compra
        df = self.df
        df['born'] = df[self.date]
        df = df[[self.customer_code,'born',self.date]].groupby(self.customer_code).agg({'born':'min',self.date:'max'}).reset_index()
        df['age'] = (df[self.date] - df['born']).dt.days
        df = df.rename({self.date:'fecha_last', self.customer_code:'cod_cliente_edad'}, axis=1)    
        return df    
    def recencia(self):
        # La recencia son los días que pasan desde que un cliente hace una nueva compra
        df = self.df
        df['id_customer'] = df[self.customer_code]
        df = df[[self.customer_code,self.date,'id_customer']].groupby([self.date,self.customer_code]).agg({'id_customer':'count'}).reset_index()
        df['recencia'] = df.groupby(self.customer_code)[self.date].diff().apply(lambda x: x.days).fillna(0).astype(int)
        df['recencia_mean'] = df['recencia']
        df['recencia_max'] = df['recencia']
        df['recencia_std'] = df['recencia']
        df = df.groupby(self.customer_code).agg({'recencia_mean':'mean','recencia_max':'max','recencia_std':'std'}).fillna(0).astype(int).reset_index()
        df = df.rename({self.customer_code:'cod_cliente_recencia'})
        return df
    def nro_sku(self):
        # Calculamos la cantidad de sku que compran los clientes
        df = self.df
        df = df[[self.customer_code,self.date,self.sku_code]].groupby([self.date,self.customer_code]).agg({self.sku_code:'nunique'}).reset_index()
        df['nro_sku_min'] = df[self.sku_code]
        df['nro_sku_mean'] = df[self.sku_code]
        df['nro_sku_max'] = df[self.sku_code]
        df['nro_sku_std'] = df[self.sku_code]
        df = df.groupby(self.customer_code).agg({'nro_sku_min':'min','nro_sku_mean':'mean','nro_sku_max':'max','nro_sku_std':'std'}).fillna(0).astype(int).reset_index()
        df = df.rename({self.customer_code:'cod_cliente_nro_sku'})
        return df
    def frequency(self):
        # Cuantas vences el cliente hizo una compra. Se tiene en cuenta una sola compra por self.date
        df = self.df
        df['id_customer']= df[self.customer_code]
        df = df[[self.customer_code,self.date]].groupby([self.customer_code]).agg({self.date:'nunique'}).reset_index()
        df = df.rename({self.date:'nro_vistas'}, axis=1)
        return df
    # Creamos una tabla con las variables a ser analizadas
    def customer_atribute(self):
        t1 = customer_autopsy.customer_old()
        t2 = customer_autopsy.recencia()
        t3 = customer_autopsy.nro_sku()
        t4 = customer_autopsy.frequency()
        df = pd.concat([t1,t2,t3,t4], axis=1)  
        df = df.drop(self.customer_code, axis=1)
        return df
    # Analizamos las ventas
    def customer_life(self, customer_code=None):
        normalizado = MinMaxScaler()
        df = self.df
        df = df if customer_code==None else df[df[self.customer_code]==customer_code]
        # Remove values under cero
        df = df[df[self.primary_key]>0]
        df = df.groupby([self.date]).agg({self.primary_key:'sum'}).reset_index()
        # Normalice the feacture columns 
        df['pk_normalice'] = normalizado.fit_transform(df[[self.primary_key]])
        df['idx_date'] = df.index
        df['idx_date'] = normalizado.fit_transform(df[['idx_date']])
        df['decil_date'] = pd.qcut(df['idx_date'], q=10)
        # Print the barchart
        plt.figure(figsize=(12,8))
        plt.title('Cicle life of the customer')
        sns.barplot(data=df, x='decil_date', y='pk_normalice')
        return df 

customer_autopsy = customer_autopsy(
    path=r'C:\Users\aleja\Desktop\Data Science\Investigaciones\Desersión de clientes\empresa_1\dataset.csv',
    date='fecha',
    customer_code='cod_cliente',
    sku_code= 'cod_art',
    primary_key='kilos'
    )
#dataset = customer_autopsy.dataset()
#customer = customer_autopsy.customer_atribute()
#ventas = customer_autopsy.customer_life()
print('datos procesados')
