#!/usr/bin/env python
# coding: utf-8

# In[32]:


#python programming language: script

'''Importing Python Libraries'''

import psycopg2 as pg
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

pd.options.display.float_format = '{0:,.0f}'.format

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))


'''Connecting to PostgreSQL database using psycopg2 library'''

conn = pg.connect(user = 'doadmin', 
                      password = 'xpmt05ij9uf9rknn', 
                      host = 'tjori-bi-do-user-6486966-0.db.ondigitalocean.com', 
                      port = '25060', 
                      database = 'defaultdb')

def write_sql():
    sql = '''
            --structured query language; query

            SELECT 
                 to_char(fsq.order_date, 'MON') AS month
                ,sum(fsq.qty) as quantity
                ,ceil(sum(fsq.net_revenue)) as net_revenue
            FROM 
               (
                SELECT 
                    soi.created AS order_date
                   ,SUM(soi.quanity) AS qty
	               ,CASE 
	                  WHEN so.currency = 'USD' THEN SUM(((soi.quanity * soi.price)*70))
	                  WHEN so.currency = 'INR' THEN SUM((soi.quanity * soi.price))
	                END AS gross_revenue
	               ,CASE
                      WHEN so.currency = 'USD' THEN 
			       CASE 
				      WHEN (((soi.quanity * soi.price)*70) - (COALESCE(soi.discount, 0)*70)) < 999 THEN SUM(((((soi.quanity * soi.price)*70) - (COALESCE(soi.discount, 0)*70)) - (((((soi.quanity * soi.price)*70) - (coalesce(soi.discount, 0) *70))*hsn.tax_under999::integer)/100)))  
					  WHEN (((soi.quanity * soi.price)*70) - (COALESCE(soi.discount, 0)*70)) > 999 THEN SUM(((((soi.quanity * soi.price)*70) - (COALESCE(soi.discount, 0)*70)) - (((((soi.quanity * soi.price)*70) - (coalesce(soi.discount, 0) *70))*hsn.tax::integer)/100)))
                   END 
                   WHEN so.currency = 'INR' THEN 
			          CASE 
				         WHEN ((soi.quanity * soi.price) - coalesce(soi.discount,0)) < 999 THEN SUM((((soi.quanity * soi.price) - coalesce(soi.discount,0)) - ((((soi.quanity * soi.price) - coalesce(soi.discount,0))*hsn.tax_under999::integer)/100)))
                         WHEN ((soi.quanity * soi.price) - coalesce(soi.discount,0)) > 999 THEN SUM((((soi.quanity * soi.price) - coalesce(soi.discount,0)) - ((((soi.quanity * soi.price) - coalesce(soi.discount,0))*hsn.tax::integer)/100)))
	                  END
		           END AS net_revenue
               FROM 
                  order_order AS so
               LEFT JOIN 
                  order_orderproduct AS soi ON (so.id = soi.order_id)
               LEFT JOIN 
                  store_product AS sp ON (soi.product_id = sp.id)
               LEFT JOIN 
                  store_category AS sc ON (sp.category_id = sc.id)
               LEFT JOIN 
                  tms_hsncode AS hsn ON (sp.hsncode_id = hsn.id)
               WHERE
                  soi.created >= CURRENT_DATE - INTERVAL ' 1 year '
                  AND so.status = 'confirmed'
                  AND so.email NOT LIKE '%@tjori.com'
                  AND soi.removed = False
                  AND soi.returned = False
                  AND soi.exchanged = False
               GROUP BY 
                  sc.name
                 ,soi.price
                 ,soi.discount
                 ,soi.quanity
                 ,so.currency
                 ,hsn.tax_under999
                 ,hsn.tax
                 ,soi.created
               ) AS fsq

              GROUP BY 
                    1

              ORDER BY
                   MIN(fsq.order_date)
              ;'''
    return pd.read_sql_query(sql, conn)

def retrieve_result():
    df = write_sql()
    df['3m_MV'] = df['quantity'].rolling(window = 3).mean()
    df['6m_MV'] = df['quantity'].rolling(window = 6).mean()
    df['9m_MV'] = df['quantity'].rolling(window = 9).mean()
   
    df['3m_EMV'] = 0.3 * df['quantity'] + (1-0.3)*df['3m_MV']
    df['6m_EMV'] = 0.6 * df['quantity'] + (1-0.6)*df['6m_MV']
    df['9m_EMV'] = 0.9 * df['quantity'] + (1-0.9)*df['9m_MV']
    return df

def plot_result():
    df = retrieve_result()
    display(df)

    '''Creating Subplots'''
    
    fig, (ax1, ax2) = plt.subplots(2, figsize = (15,10))

    '''Plotting the data'''
    
    ax1.plot(df['month'],df['quantity'])
    ax1.plot(df['month'],df['3m_MV'])
    ax1.plot(df['month'],df['6m_MV'])
    ax1.plot(df['month'],df['9m_MV'])
    ax1.set_ylabel('Quantities')
    ax1.set_xlabel('Month')
    
    ax2.plot(df['month'],df['quantity'])
    ax2.plot(df['month'],df['3m_EMV'])
    ax2.plot(df['month'],df['6m_EMV'])
    ax2.plot(df['month'],df['9m_EMV'])
    ax2.set_ylabel('Quantities')
    ax2.set_xlabel('Month')

    '''Setting the chart title'''
    
    ax1.set_title('Moving Average - Orders', bbox={'facecolor':'0.8', 'pad':3})
    ax2.set_title('Exponential Moving Average - Orders', bbox={'facecolor':'0.8', 'pad':3})

    '''Setting the chart legend'''
    
    ax1.figure.legend(['Qty','3MV','6MV','9MV'], bbox_to_anchor=(1.,1), loc=1, bbox_transform=ax1.transAxes)
    ax2.figure.legend(['Qty','3EMV','6EMV','9EMV'], bbox_to_anchor=(1.,1), loc=1, bbox_transform=ax2.transAxes)
    
    plt.subplots_adjust(bottom=0.30, top=0.95, wspace = 2.0)
                       
    plt.show()
    
   

def main():
    plot_result()
   
    
if __name__ == '__main__':
    main()
    


# In[ ]:





# In[ ]:




