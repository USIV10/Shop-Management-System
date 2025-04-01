import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def generate_sales_report():
    conn = sqlite3.connect('shop.db')
    query = '''SELECT s.sale_date, p.name, s.quantity, (s.quantity * p.price) as total 
               FROM sales s 
               JOIN products p ON s.product_id = p.product_id'''

    sales_data = pd.read_sql_query(query, conn)
    conn.close()

    # Display report as a table
    print(sales_data)

    # Plot total sales by product
    sales_by_product = sales_data.groupby('name')['total'].sum()
    sales_by_product.plot(kind='bar')

    plt.title("Total Sales by Product")
    plt.ylabel("Revenue ($)")
    plt.show()
