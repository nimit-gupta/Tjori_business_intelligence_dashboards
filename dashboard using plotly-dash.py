#python programming language: script

import dash 
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import psycopg2 as pg
import pandas as pd

conn = pg.connect (
                      user = 'doadmin', 
                      password = 'xpmt05ij9uf9rknn', 
                      host = 'tjori-bi-do-user-6486966-0.db.ondigitalocean.com', 
                      port = '25060', 
                      database = 'defaultdb'                 
                  )

sql = '''
         --structured query language; query

         SELECT 
              fsq.months AS month
             ,fsq.category AS category
             ,SUM(fsq.quantity) AS value
         FROM 
             (
              SELECT 
                   TO_CHAR(soi.created, 'Month') AS months
                  ,sc.name AS category
                  ,SUM(soi.quanity) AS quantity
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
                  AND so.email NOT LIKE '%@tjori.com'
                  AND sc.name IS NOT NULL 
              GROUP BY 
                  soi.created
                 ,sc.name
             ) fsq
         GROUP BY 
              1
             ,2

           ;
           '''
df = pd.read_sql_query(sql, conn)



app = dash.Dash()

app.layout = html.Div(children = [
    
                   html.Div(
                       dcc.Graph(
                                 id = 'Graph',
                           
                                  figure = {
                                            'data' : [
                                                      go.Bar(
                                                             x = df['month'],
                                                             y = df['value']
                                                            )
                                                     ],
                                            'layout' : 
                                                     go.Layout(
                                                                title = 'Months vs Quantities Sold'
                                                              )
                                                
                                            }
                                 
                                  
                               )
                        ),
    
                        html.Div(
                                  dcc.Graph(
                                             id = 'graph_1',
                                      
                                             figure = {
                                                       'data' : [
                                                                  
                                                                  go.Bar(
                                                                          x = df['category'],
                                                                          y = df['value']
                                                                  ) 
                                                                ],
                                                        'layout' : go.Layout(
                                                                             title = 'Category vs Quantities Sold'                     
                                                                             )
                                                      
                                                       }
                                  )
                        )
                     ])

if __name__ == '__main__':
    app.run_server(debug = True)
    

