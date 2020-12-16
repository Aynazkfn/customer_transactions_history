#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import copy
import dash
import datetime
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime as dt
import matplotlib.pyplot as plt
import plotly
import datetime
import matplotlib.pyplot as plt
import re
import base64
from io import BytesIO
import statsmodels.api as sm

# create the app object
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server





##############################################################
# Data

df1 = pd.read_csv('C:/Users/20190041/Desktop/Datachef assignment/customer_transactions_history-main/transactions_1.csv')
df2 = pd.read_csv('C:/Users/20190041/Desktop/Datachef assignment/customer_transactions_history-main/transactions_2.csv')
df = pd.concat ([df1,df2], axis=0, ignore_index=True).drop(['Unnamed: 0'], axis=1)

df['date']= pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month

sales = df.copy()
sales['date']= pd.to_datetime(sales['date'])
sales['date'] = sales['date'].dt.year.astype('str') + '-' + sales['date'].dt.month.astype('str') + '-01'
sales['date'] = pd.to_datetime(sales['date'])
sales = sales.groupby(['customer_id', 'date']).size().reset_index()
sales.columns = ['customer_id', 'date', 'Order_count']

sales_all = sales.groupby(['date'])['Order_count'].sum().reset_index()


list1=list(df['product_id'].unique())
list1.insert(0, "All")


list2=list(df['customer_id'].unique())
list2.insert(0, "All")

##############################################################
# Create app layout

app.layout = html.Div(
    [
     dcc.Store(id="aggregate_data"),
     # empty Div to trigger javascript file for graph resizing
     html.Div(id="output-clientside"),
#############################################################  
# first container (title)
        
     html.Div([ 
           # logo
           html.Div( 
                     className="one-third column",),
           # main title
           html.Div([html.Div([ html.H3( "Monthly Sales",
                                    style={"margin-bottom": "0px"},),
                                 html.H5("Overview and Prediction", style={"margin-top": "0px"}),
                            ])    ],
                     className="one-half column",style={"margin-top": "0px", "margin-right": "29.5%"},
                     id="title",),
         
         
            ],
    id="header",
    className="row flex-display",
    style={"margin-bottom": "25px"},
        ),

##########################################################               
# second container (Sales, histogram)     
      
      dcc.Tabs([
        dcc.Tab(label='Overview', children=[
           
        
            
              html.Div([
                # map
                html.Div( [ 
                            html.Label(["Product ID", dcc.Dropdown(
                                                id="dropdown-product",
                                                options=[ {'label':i, 'value':i} for i in list1],
                                                value="All",
                                                searchable=True,
                                                style={"margin-left": "10px","margin-right": "15px","margin-top": "10px"},
                                            )]),   
                            html.Label(["Customer ID", dcc.Dropdown(
                                                id="dropdown-customer",
                                                options=[ {'label':i, 'value':i} for i in list2],
                                                value="All",
                                                searchable=True,
                                                style={"margin-left": "10px","margin-right": "15px","margin-top": "5px"},
                                            )]),
                           html.Label(["Year", dcc.Dropdown(
                                                id="dropdown-year",
                                                options=[ {'label':i, 'value':i} for i in df['year'].unique()],
                                                value=2018,
                                                searchable=True,
                                                style={"margin-left": "10px","margin-right": "15px","margin-top": "5px"},
                                            )]),
                                         
                    
                   ],
                className="pretty_container three columns",),
            
            
            
             html.Div(
                                     [
                                   
                    dcc.Graph(id="graph-sales", 
                                   
                                   config={'displayModeBar': False}),
                    
                  
           
                                    ],
                          className="pretty_container nine columns",
                         
                ),
            
                       
            
        ],
            className="row flex-display",
        ),   
            
        
        
        
        
        ]),
        dcc.Tab(label='Modeling', children=[
       
              
              html.Div([
                
                html.Div( [ 
                          html.Label(["Customer ID",  dcc.Dropdown(
                                                id="dropdown-customer1",
                                                options=[ {'label':i, 'value':i} for i in list2],
                                                value='All',
                                                searchable=True,
                                                style={"margin-left": "10px","margin-right": "15px","margin-top": "10px"},
                                                #multi=True
                                            )]),
                                          
                                       
                    
                   ],
                className="pretty_container three columns",),
            
            
            
             html.Div(
                                     [
                                   
                    dcc.Graph(id="graph-model", 
                                   
                                   config={'displayModeBar': False}),
                    
                   
           
                                    ],
                          className="pretty_container nine columns",
                         
                ),
            
                       
            
        ],
            className="row flex-display",
        ),   
            
            
            
        ]),
      
    ])
        
        
        
        
    
    ],
       id="mainContainer",
       style={"display": "flex", "flex-direction": "column"},
)


##########################################################
# Visualizing

@app.callback(Output("graph-sales", "figure"),
              [ Input("dropdown-product", "value"), 
                Input("dropdown-customer", "value"),
                Input("dropdown-year", "value")
               
    ])   
def sales_figure( productid,customerid,year):
    
    if productid == "All":
        if customerid == "All":
            df_filtered=df[(df['year']==year)]
            df_monthly = pd.DataFrame(df_filtered.groupby( 'month').size().rename('order_counts').reset_index())
        else:
            df_filtered=df[(df['year']==year)&(df['customer_id']==customerid)]
            df_monthly = pd.DataFrame(df_filtered.groupby( 'month').size().rename('order_counts').reset_index())
    elif customerid == "All":
        df_filtered=df[(df['year']==year)&(df['product_id']==productid)]
        df_monthly = pd.DataFrame(df_filtered.groupby( 'month').size().rename('order_counts').reset_index())
    else:
        df_filtered=df[(df['year']==year) & (df['product_id']==productid)&(df['customer_id']==customerid)]     
        df_monthly = pd.DataFrame(df_filtered.groupby( 'month').size().rename('order_counts').reset_index())
 
 
        
##########################################################
# Visualization

    traces = []
   
    trace = go.Scatter(
            x=df_monthly['month'], 
            y=df_monthly['order_counts'],
            mode = 'lines',
                   line = dict(shape = 'linear', width= 2),
                    connectgaps = True
        )
    traces.append(trace)
    
    
    layout=go.Layout(title_text ='Monthly Sales for '+productid+' in year '+str(year),
                     xaxis = dict(title = 'Month',tickmode = 'array',
        tickvals = np.arange(1,13),
        ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']),
                     yaxis = dict(title = 'Sales'))    
    figure = dict(data = traces, layout = layout)
    
    
    return figure

##########################################################
# Modeling

@app.callback(Output("graph-model", "figure"),
              [ 
                Input("dropdown-customer1", "value"),
            
               
    ])   
def model_figure( customerid):
    
    
    if customerid == "All":        
        customerx = sales_all
    else: 

        customerx = sales[sales['customer_id'] == customerid]
        customerx= customerx.drop('customer_id', axis=1)
    
    y = customerx.set_index('date')
    mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 1, 12),
                                #enforce_stationarity=False,
                                enforce_invertibility=False)
    results = mod.fit()

    pred = results.get_prediction(start=pd.to_datetime('2019-01-01'), dynamic=False)
    pred_ci = pred.conf_int()
    pred_df = pd.DataFrame(pred.predicted_mean)
    pred_df[pred_df < 0] = 0
    pred_ci[pred_ci < 0] = 0
 
   
##########################################################
    traces = []
   
    trace1 = go.Scatter(
            name='Actual Sales',
            x=y.index, 
            y=y['Order_count'],
            mode = 'lines',
                   line = dict(shape = 'linear', width= 2),
                    connectgaps = True
        )
    
    trace2 = go.Scatter(
        name='Predicted Sales',
        x=pred_df.index, 
        y=pred_df['predicted_mean'],
        mode='lines',
        line=dict(color='red'),
    )
    
    trace3 = go.Scatter(
        name='Upper Bound',
        x=pred_ci.index,
        y=pred_ci.iloc[:, 1],
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        showlegend=False
    )
    trace4 = go.Scatter(
        name='Lower Bound',
        x=pred_ci.index,
        y=pred_ci.iloc[:, 0],
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False
    )

    traces.append(trace1)
    traces.append(trace2)
    traces.append(trace3)
    traces.append(trace4)

    
    layout=go.Layout(title_text ='Monthly Sales for '+customerid,
                     xaxis = dict(title = 'Date',tickmode = 'array'),
                     yaxis = dict(title = 'Sales'))
    
    figure = dict(data = traces, layout = layout)
    
    return figure

    

# Main
if __name__ == "__main__":
    app.run_server(debug=False)


# In[ ]:




