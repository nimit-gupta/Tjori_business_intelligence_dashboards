#python programming language: script

import dash 
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import psycopg2 as pg
import pandas as pd
from datetime import datetime as dt
import warnings
warnings.filterwarnings('ignore')

conn = pg.connect (
                      user = 'doadmin', 
                      password = 'xpmt05ij9uf9rknn', 
                      host = 'tjori-bi-do-user-6486966-0.db.ondigitalocean.com', 
                      port = '25060', 
                      database = 'defaultdb' 
                  )


app = dash.Dash()

app.layout = html.Div([
                        html.Div([
                                  html.H1('E-Commerce Dashboard')
                                 ], style={'marginBottom': 25, 'marginTop': 25, 'textAlign': 'center'}
                                ),

                        dcc.Tabs 
                                (
                                    [
                                       dcc.Tab(
                                                label = 'Category Wise', children = [
                                                                       
                                                                         html.Div([
                                                                                     html.Label('Choose Category')
                                                                                  ], 
                                                                                     style={'textAlign': 'center'}
                                                                                 ),        

                                                                          html.Div([
                                
                                                                                  dcc.RadioItems(
                                                                                                  id='my-dropdown',
                                                                                                  options=[
                                                                                                           {'label': 'Apparel', 'value': 'Apparel'},
                                                                                                           {'label': 'Wellness', 'value': 'Wellness'},
                                                                                                           {'label': 'Footwear', 'value': 'Footwear'},
                                                                                                           {'label': 'Mother & Child', 'value': 'Mother & Child'},
                                                                                                           {'label': 'Jewelry', 'value': 'Jewelry'},
                                                                                                           {'label': 'Home & Decor', 'value': 'Home & Decor'}
                                  
                                                                                                          ],
                                                                                                      value = 'Apparel',
                                                                                                      style={'marginBottom': 25, 'marginTop': 25, 'textAlign': 'center'}
                                                                                                   )
                                                                                                      ]
                                                                                                ),

                                                                          html.Div([
                                                                                    dcc.DatePickerRange(
                                                                                                         id='my-date-picker-range',
                                                                                                         min_date_allowed=dt(1995, 8, 5),
                                                                                                         max_date_allowed=dt(2020, 12, 31),
                                                                                                         start_date = dt(2019, 1, 1).date(),
                                                                                                         end_date=dt(2020, 12, 31).date()
                                                                                                        )
                                                                                                      ],  style={'marginBottom': 25, 'marginTop': 25, 'textAlign': 'center'}
                                                                                                    ),

                                                                          html.Div (
                                                                                    [
                                                                                     dcc.Graph( id="my-graph")
                                                                                    ]
                                                                                  ),
                                                                          html.Div(
                                                                                  [
                                                                                     dcc.Graph(id = "my-graph-1")

                                                                                  ]
                                                                                  ),
                                                                         html.Div(
                                                                                 [
                                                                                    dcc.Graph( id = "my-graph-2")
                                                                                 ]
                                                                                 )
                                          
                                                                            ]
                                                                          ),
                                                                        dcc.Tab(
                                                                                 label = "Product Wise", children = [
                                                                                                                      html.Div([
                                                                                                                                html.Label('Choose Category')
                                                                                                                               ], 
                                                                                                                               style={'textAlign': 'center'} 
                                                                                                                               ),  
                                                                                                                      html.Div([  dcc.RadioItems(
                                                                                                                                                 id='my-dropdown-tab-2',
                                                                                                                                                 options=[
                                                                                                                                                          {'label': 'Apparel', 'value': 'Apparel'},
                                                                                                                                                          {'label': 'Wellness', 'value': 'Wellness'},
                                                                                                                                                          {'label': 'Footwear', 'value': 'Footwear'},
                                                                                                                                                          {'label': 'Mother & Child', 'value': 'Mother & Child'},
                                                                                                                                                          {'label': 'Jewelry', 'value': 'Jewelry'},
                                                                                                                                                          {'label': 'Home & Decor', 'value': 'Home & Decor'}
                                  
                                                                                                                                                         ],
                                                                                                                                                       value = 'Apparel',
                                                                                                                                                       style={'marginBottom': 25, 'marginTop': 25, 'textAlign': 'center'}
                                                                                                                                                   )
                                                                                                                                                 ]
                                                                                                                                               ), 
                                                                                                                       html.Div (
                                                                                                                                 [
                                                                                                                                  dcc.Graph( id="my-graph-tab-2")
                                                                                                                                 ]
                                                                                                                               ),

                                                                                                                       html.Div (
                                                                                                                                 [
                                                                                                                                  dcc.Graph(id = "my-graph-tab-3")
                                                                                                                                 ]
                                                                                                                                ), 
                                                                                                                       html.Div (
                                                                                                                                 [
                                                                                                                                  dcc.Graph(id = "my-graph-tab-4")
                                                                                                                                 ]
                                                                                                                                ),



                                                                                 ]
                                                                               ),
                                                                               dcc.Tab(
                                                                                 label = "Product Brief Summary", children = [
                                                                                                                      html.Div(
                                              [html.H4('Product Brief Summary'),
                                              ], style = {'textAlign': 'center'}
                                            ),

                                    html.Div(
                                             [
                                               html.Label('Choose Category'),
                                               dcc.Dropdown(
                                                             id='my-dropdown-tab-3',
                                                             options=[
                                                                      {'label': 'Apparel', 'value': 'Apparel'},
                                                                      {'label': 'Wellness', 'value': 'Wellness'},
                                                                      {'label': 'Footwear', 'value': 'Footwear'},
                                                                      {'label': 'Mother & Child', 'value': 'Mother & Child'},
                                                                      {'label': 'Jewelry', 'value': 'Jewelry'},
                                                                      {'label': 'Home & Decor', 'value': 'Home & Decor'}
                                                                    ],
                                                                     value = 'Apparel'
                                                              )
                                            ]
                                           ),

                                        html.Div(
                                                 [
                                                   dash_table.DataTable (
                                                                         id = 'my-table',
                                                                         style_cell={'textAlign': 'center'},
                                                                         style_header={ 'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                                                                         style_data_conditional=[
                                                                                                 {
                                                                                                  'if': {'column_id': 'product_quantities',
                                                                                                        'filter_query': '{product_quantities} > 500'
                                                                                                        },
                                                                                                 
                                                                                                   'color': 'green',
                                                                                                   'fontWeight': 'bold'

                                                                                                 },
                                                                                                 {
                                                                                                  'if': {'column_id': 'product_quantities',
                                                                                                        'filter_query': '{product_quantities} < 100'
                                                                                                        },
                                                                                                  
                                                                                                   'color': 'red',
                                                                                                   'fontWeight': 'bold'

                                                                                                 }

                                                                                               ]
                                                                         
                                                                        )
                                                 ]
                                               )  
                                           ]
                                        ) 






                                                                             ]
                                                                           )
                                                                         ]
                                                                       )
@app.callback(dash.dependencies.Output('my-graph', 'figure'),[dash.dependencies.Input('my-date-picker-range', 'start_date'),dash.dependencies.Input('my-date-picker-range', 'end_date'),dash.dependencies.Input('my-dropdown', 'value')])

def update_graph_1(start_date, end_date, value):

    sql = '''
             SELECT 
                  soi.created::date AS month_date
                 ,floor(SUM((soi.price * soi.quanity) - soi.discount)) AS gross_revenue
             FROM 
                  order_order AS so
             LEFT JOIN 
                  order_orderproduct AS soi ON (so.id = soi.order_id)
             LEFT JOIN 
                  store_product AS sp ON (soi.product_id = sp.id)
             LEFT JOIN 
                  store_category AS sc ON (sp.category_id = sc.id)
             WHERE 
                  soi.created BETWEEN '%s' AND '%s'
                  AND so.status = 'confirmed'
                  AND so.email NOT LIKE '%%@tjori.com'
                  AND sc.name = '%s'
            GROUP BY
                  1
              ;'''%(
                    start_date,
                    end_date,
                    value
                    )

    df = pd.read_sql_query(sql, conn)
    return  {
                    'data': [ 
                             go.Bar (
                                      x = df['month_date'],
                                      y = df['gross_revenue']
                                    )
                           
                            ],
                    'layout':  
                                go.Layout (
                                           xaxis = {
                                                     'title' : 'Months'
                                                   },
                                           yaxis = {
                                                    'title' : 'Revenue'
                                                   },
                                           
                                          

                                           hovermode = 'closest',
            
                                           title = 'Month Wise Category Revenue Earned',

                                           colorway = ['#f3cec9'],

                                           paper_bgcolor = '#e0dcdc',

                                           plot_bgcolor = '#061778'

                                          
                                            
                                          )
                             
                    }
@app.callback(dash.dependencies.Output('my-graph-1', 'figure'),[dash.dependencies.Input('my-date-picker-range', 'start_date'),dash.dependencies.Input('my-date-picker-range', 'end_date'),dash.dependencies.Input('my-dropdown', 'value')])

def update_graph_2(start_date, end_date, value):

    sql = '''
             SELECT 
                  soi.created::date AS date_created
                 ,SUM(soi.quanity) AS quantity_sold
             FROM 
                  order_order AS so
             LEFT JOIN 
                  order_orderproduct AS soi ON (so.id = soi.order_id)
             LEFT JOIN 
                  store_product AS sp ON (soi.product_id = sp.id)
             LEFT JOIN 
                  store_category AS sc ON (sp.category_id = sc.id)
             WHERE 
                  soi.created BETWEEN '%s' AND '%s'
                  AND so.status = 'confirmed'
                  AND so.email NOT LIKE '%%@tjori.com'
                  AND sc.name = '%s'
             GROUP BY 
                  1
                ;'''%(
                       start_date,
                       end_date,
                       value
                )
    df = pd.read_sql_query(sql, conn)
    return  {
                    'data': [ 
                             go.Bar (
                                      x = df['date_created'],
                                      y = df['quantity_sold']
                                    )
                           
                            ],
                    'layout':  
                                go.Layout (
                                           xaxis = {
                                                     'title' : 'Days'
                                                   },
                                           yaxis = {
                                                    'title' : 'Quantity_Sold'
                                                   },
                                           
                                          

                                           hovermode = 'closest',
            
                                           title = 'Day Wise Category Quanitity Sold',

                                           colorway = ['#f70505'],

                                           paper_bgcolor = '#e0dcdc',

                                           plot_bgcolor = '#061778'

                                          
                                            
                                          )
                             
                    }   

@app.callback(dash.dependencies.Output('my-graph-2', 'figure'),[dash.dependencies.Input('my-date-picker-range', 'start_date'),dash.dependencies.Input('my-date-picker-range', 'end_date'),dash.dependencies.Input('my-dropdown', 'value')])

def update_graph_3(start_date, end_date, value):

    sql = '''
             SELECT 
                  ga.date::DATE AS accured_date
                 ,SUM(ga.unique_page_views) AS unique_pageviews
             FROM 
                  ga_union_pageviews AS ga
             LEFT JOIN 
                  store_product AS sp ON (ga.product_id = sp.id)
             LEFT JOIN 
                  store_category AS sc ON (sp.category_id = sc.id)
             WHERE 
                  ga.date BETWEEN '%s' AND '%s'
                  AND sc.name = '%s'
             GROUP BY 
                 1
                ;'''%(
                       start_date,
                       end_date,
                       value
                     )
    df = pd.read_sql_query(sql, conn)
    return  {
                    'data': [ 
                             go.Bar (
                                      x = df['accured_date'],
                                      y = df['unique_pageviews']
                                    )
                           
                            ],
                    'layout':  
                                go.Layout (
                                           xaxis = {
                                                     'title' : 'Days'
                                                   },
                                           yaxis = {
                                                    'title' : 'Unique Pageview'
                                                   },
                                           
                                          

                                           hovermode = 'closest',
            
                                           title = 'Day Wise Category Unique Pageviews',

                                           colorway = ['#12bf0f'],

                                           paper_bgcolor = '#e0dcdc',

                                           plot_bgcolor = '#061778'

                                          
                                            
                                          )
                             
                    }  

@app.callback(dash.dependencies.Output('my-graph-tab-2', 'figure'),[dash.dependencies.Input('my-dropdown-tab-2', 'value')])

def update_graph_4(value):

    sql = '''
            SELECT 
                 sp.name as product_name
                ,SUM(soi.quanity) as product_quantity
            FROM 
                 order_order AS so
            LEFT JOIN 
                 order_orderproduct AS soi ON (so.id = soi.order_id)
            LEFT JOIN 
                 store_product AS sp ON (soi.product_id = sp.id)
            LEFT JOIN 
                 store_category AS sc ON (sp.category_id = sc.id)
            WHERE 
                 soi.created BETWEEN '2019-01-01' AND '2020-01-01'
                AND so.status = 'confirmed'
                AND so.email NOT LIKE '%%@tjori.com'
                AND sp.active = TRUE 
                AND sc.name = '%s'
            GROUP BY 
                1
            HAVING 
                SUM(soi.quanity) >= 100
            ORDER BY 
            2 desc
            ;'''%(
                  value
                 )
    
    df = pd.read_sql_query(sql, conn)
    return {

                    'data': [ 
                             go.Bar (
                                      x = df['product_name'],
                                      y = df['product_quantity']
                                    )
                           
                            ],
                    'layout':  
                                go.Layout (
                                           xaxis = {
                                                     'title' : 'Product Name'
                                                   },
                                           yaxis = {
                                                    'title' : 'Product Quanity'
                                                   },
                                           
                                          

                                           hovermode = 'closest',
            
                                           title = 'Product Quantity',

                                           colorway = ['#58e8bf'],

                                           paper_bgcolor = '#e0dcdc',

                                           plot_bgcolor = '#061778'

                                          
                                            
                                          )
                             
                    }  

@app.callback(dash.dependencies.Output('my-graph-tab-3', 'figure'),[dash.dependencies.Input('my-dropdown-tab-2', 'value')])

def update_graph_5(value):

    sql = '''
             SELECT 
                  sp.name as product_name
                 ,SUM(ga.unique_page_views) AS product_unique_pageviews
             FROM 
                 ga_union_pageviews AS ga
             LEFT JOIN 
                store_product AS sp ON (ga.product_id = sp.id)
             LEFT JOIN 
                store_category AS sc ON (sp.category_id = sc.id)
             WHERE 
                ga.date BETWEEN '2019-01-01' AND '2020-01-01'
                AND sp.active = True
                AND sc.name = '%s'
            GROUP BY 
                1
            HAVING 
               SUM(ga.unique_page_views) >= 1000
            ORDER BY 
               2 desc
            ;'''%(
                   value
                 )

    df = pd.read_sql_query(sql, conn)

    return {
              'data': [ 
                             go.Bar (
                                      x = df['product_name'],
                                      y = df['product_unique_pageviews']
                                    )
                           
                            ],
                    'layout':  
                                go.Layout (
                                           xaxis = {
                                                     'title' : 'Product Name'
                                                   },
                                           yaxis = {
                                                    'title' : 'Product Unique Pageviews'
                                                   },
                                           
                                          

                                           hovermode = 'closest',
            
                                           title = 'Product Unique Pageviews',

                                           colorway = ['#34c9eb'],

                                           paper_bgcolor = '#e0dcdc',

                                           plot_bgcolor = '#061778'

                                          
                                            
                                          )
                             
                    }  
             
@app.callback(dash.dependencies.Output('my-graph-tab-4', 'figure'),[dash.dependencies.Input('my-dropdown-tab-2', 'value')])

def update_graph_6(value):

    sql = '''
             WITH cte1 AS 
           (
             SELECT 
                   sp.name AS spx
                  ,SUM(soi.quanity) AS spq1
             FROM 
                   order_order AS so
             LEFT JOIN 
                   order_orderproduct AS soi ON (so.id = soi.order_id)
             LEFT JOIN 
                   store_product AS sp ON (soi.product_id = sp.id)
             LEFT JOIN 
                   store_category AS sc ON (sp.category_id = sc.id)
             WHERE 
                   soi.created BETWEEN '2019-01-01' AND '2020-01-01'
                   AND so.status = 'confirmed'
                   AND so.email NOT LIKE '%%@tjori.com'
                   AND sp.active = TRUE 
                   AND sc.name = 'Apparel'
            GROUP BY 
                   1
           
         ),
         
         cte2 AS (
                   SELECT 
                        sp.name AS spy
                       ,SUM(ga.unique_page_views) AS sppv2
                   FROM 
                        ga_union_pageviews AS ga
                   LEFT JOIN 
                        store_product AS sp ON (ga.product_id = sp.id)
                   LEFT JOIN 
                        store_category AS sc ON (sp.category_id = sc.id)
                   WHERE 
                        ga.date BETWEEN '2019-01-01' AND '2020-01-01'
                        AND sp.active = True
                        AND sc.name = '%s'
                   GROUP BY 
                        1
                   )
                   
       SELECT 
            cte2.spy as product_name
           ,ROUND(((cte1.spq1/cte2.sppv2) * 100), 2) AS pips
       FROM 
            cte1
       LEFT JOIN 
            cte2 ON (cte1.spx = cte2.spy)
       ORDER BY
            2 desc
          ;'''%(
                 value
               )

    df = pd.read_sql_query(sql, conn)
    return {
             'data': [ 
                             go.Line (
                                      x = df['product_name'],
                                      y = df['pips']
                                    )
                           
                            ],
                    'layout':  
                                go.Layout (
                                           xaxis = {
                                                     'title' : 'Product Name'
                                                   },
                                           yaxis = {
                                                    'title' : 'Product PIPS'
                                                   },
                                           
                                          

                                           hovermode = 'closest',
            
                                           title = 'Product PIPS',

                                           colorway = ['#fca903'],

                                           paper_bgcolor = '#e0dcdc',

                                           plot_bgcolor = '#061778'

                                          
                                            
                                          )
                             
                    }  
    
      
@app.callback([dash.dependencies.Output("my-table", "columns"), dash.dependencies.Output("my-table", "data")], [dash.dependencies.Input("my-dropdown-tab-3", "value")])

def update_table_7(value):

    sql = '''
         SELECT 
               sp.name as product_name
              ,SUM(soi.quanity) as product_quantities
              ,CEIL(SUM(soi.quanity * soi.price)) as gross_product_revenue
          FROM 
              order_order AS so
          LEFT JOIN 
              order_orderproduct AS soi ON (so.id = soi.order_id)
          LEFT JOIN 
             store_product AS sp ON (soi.product_id = sp.id)
          LEFT JOIN 
             store_category AS sc ON (sp.category_id = sc.id)
          WHERE 
             soi.created BETWEEN '2019-01-01' AND '2020-01-01'
             AND so.status = 'confirmed'
             AND so.email NOT LIKE '%%@tjori.com'
             AND sc.name = '%s'
             AND sp.active = TRUE 
          GROUP BY 
             1
          HAVING 
             SUM(soi.quanity) >= 1
          
             ;'''%(
                   value
                   )
    df = pd.read_sql_query(sql, conn).reset_index()
    return [{"name": i, "id": i} for i in df.columns], df.to_dict('record')          


if __name__ == '__main__':
    app.run_server(debug = True)


