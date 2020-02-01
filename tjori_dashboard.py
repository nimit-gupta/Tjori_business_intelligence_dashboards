#Python programming language: script

'''Importing Python Libraries'''

import psycopg2 as pg
import pandas as pd
import matplotlib.pyplot as plt

conn = pg.connect(user = 'doadmin', 
                      password = 'xpmt05ij9uf9rknn', 
                      host = 'tjori-bi-do-user-6486966-0.db.ondigitalocean.com', 
                      port = '25060', 
                      database = 'defaultdb')
    

def write_sql_query_revenue():
    sql = '''
             --strucutred query language; query

             SELECT 
                  fsq.category
                 ,CEIL(SUM(fsq.gross_revenue)) AS gross_revenue
                 ,CEIL(SUM(fsq.net_revenue)) AS net_revenue
             FROM 
                (
                 SELECT 
                      sc.name AS category
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
                     AND so.email NOT LIKE '%%@tjori.com%%'
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
                ) AS fsq

             WHERE 
                fsq.category IS NOT NULL 

             GROUP BY 
                1
             ORDER BY 
                3 desc
            ;
             '''
    return pd.read_sql_query(sql,conn)

def write_sql_query_pageviews():
    sql = '''
            --strucutred query language; query

             SELECT 
                  sc.name as category
                 ,SUM(ga.page_views) as pageviews
             FROM 
                  ga_union_pageviews AS ga
             LEFT JOIN 
                  store_product AS sp ON (ga.product_id = sp.id)
             LEFT JOIN 
                  store_category AS sc ON (sp.category_id = sc.id)
             WHERE 
                  DATE >= CURRENT_DATE - INTERVAL '1 year'
                  AND sc.name IS NOT NULL 
             GROUP BY 
                  sc.name
             ;'''
    return pd.read_sql_query(sql, conn)

def write_sql_query_pips():
    sql = '''
            --strucutred query language; query
            SET statement_timeout TO 900000;

            SELECT 
                 fsq.ct AS category
                ,sum(fsq.pg) AS pageviews
                ,sum(fsq.qty) AS quanity
                ,ROUND((SUM(fsq.qty)/SUM(fsq.pg)*100),2) AS pips
            FROM
               (
                SELECT 
                    sc.name AS ct
                   ,SUM(ga.page_views) AS pg
                   ,lsq.sq_soiquanity AS qty
                FROM 
                   ga_union_pageviews AS ga
                LEFT JOIN 
                   store_product AS sp ON (ga.product_id = sp.id)
                LEFT JOIN 
                   store_category AS sc ON (sp.category_id = sc.id)
                LEFT JOIN 
                  (SELECT 
                       sp.id AS sq_spid
                      ,sum(soi.quanity) AS sq_soiquanity
                  FROM
		             order_order AS so
		          LEFT JOIN 
		             order_orderproduct AS soi ON (so.id = soi.order_id)
		          LEFT JOIN 
		             store_product AS sp ON (soi.product_id = sp.id)
		          WHERE 
		             soi.created >= CURRENT_DATE - INTERVAL '1 year'
			         AND so.status = 'confirmed'
			         AND so.email NOT LIKE '%@tjori.com'
		         GROUP BY 
		             1
		
			     ) AS lsq ON (sp.id = sq_spid) 
              WHERE 
                 DATE >= CURRENT_DATE - INTERVAL '1 year'
                 AND sc.name IS NOT NULL 
              GROUP BY 
                 1
                ,3
     
             ) AS fsq
             GROUP BY 
                 1
    
             ;'''
    return pd.read_sql_query(sql,conn)

def write_sql_query_month_revenue():
    sql = '''
            --strucutred query language; query

            SELECT 
               fsq.month
              ,sum(fsq.qty) AS quantity
              ,CEIL(SUM(fsq.gross_revenue)) AS gross_revenue
              ,CEIL(SUM(fsq.net_revenue)) AS net_revenue
            FROM 
              (
               SELECT 
                   TO_CHAR(soi.created, 'MON') AS month
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
              3 asc
           ;'''
    return pd.read_sql_query(sql, conn)

def write_sql_query_month_pageviews():
    sql = '''
            --strucutred query language; query

            SELECT 
                TO_CHAR(ga.DATE, 'MON') as month
               ,SUM(ga.page_views) as pageviews
            FROM 
                ga_union_pageviews AS ga
            WHERE 
                ga.date >= CURRENT_DATE - INTERVAL '1 year'
           GROUP BY 
                1
           ORDER BY 
               MIN(ga.Date)
            ;'''
    return pd.read_sql_query(sql, conn)

def execute_sql_query():
    df_0 = write_sql_query_revenue()
    df_1 = write_sql_query_pageviews()
    df_2 = write_sql_query_pips()
    df_3 = write_sql_query_month_revenue()
    df_4 = write_sql_query_month_pageviews()
    return df_0, df_1, df_2, df_3, df_4
    
def plot_dashboard():
    df_0, df_1, df_2, df_3, df_4 = execute_sql_query()
    
    colors = ["#E13F29", "#D69A80", "#D63B59", "#AE5552", "#CB5C3B", "#EB8076", "#96624E"]
  
  
    
    fig, (ax1,ax2,ax3) = plt.subplots(1,3, figsize = (20,20))
    fig_2, ax4 = plt.subplots(1,1, figsize = (20,6))
    fig_3, ax5 = plt.subplots(1,1, figsize = (20,8))
    fig_4, ax6 = plt.subplots(1,1, figsize = (20,8))
    
    
    
    ax1.pie(df_0['net_revenue'], labels = df_0['category'], shadow = False, colors=colors, startangle=90, autopct='%1.1f%%')
    ax2.pie(df_1['pageviews'], labels = df_1['category'], shadow = False, colors=colors, startangle=90, autopct='%1.1f%%')
    ax3.pie(df_2['pips'], labels = df_2['category'], shadow = False, colors=colors, startangle=90,  autopct='%1.1f%%')
    ax4.bar(df_3['month'], df_3['quantity'], color='#D69A80')
    ax5.bar(df_3['month'], df_3['net_revenue'], color='#CB5C3B')
    ax6.bar(df_4['month'], df_4['pageviews'], color='#D63B59')
    
    ax4.set_ylim(10000, 50000)
    ax5.set_ylim(8000000,15000000)
    
    
    ax1.set_title('Category Wise Revenue Distribution', bbox={'facecolor':'0.8', 'pad':3})
    ax2.set_title('Category Wise Pageviews Distribution', bbox={'facecolor':'0.8', 'pad':3})
    ax3.set_title('Category Wise PIPS Distribution',bbox={'facecolor':'0.8', 'pad':3})
    ax4.set_title('Month wise Quantity Sold Distribution',bbox={'facecolor':'0.8', 'pad':3})
    ax5.set_title('Month wise Revenue Distribution',bbox={'facecolor':'0.8', 'pad':3})
    ax6.set_title('Month wise Pageviews Distribution',bbox={'facecolor':'0.8', 'pad':3})
    
    plt.subplots_adjust(bottom=0.30, top=0.75, wspace = 0.8)
    plt.show()
    
def main():
    plot_dashboard()
   
if __name__ == '__main__':
    main()
