from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from admin import SalesApp, InventoryApp, CustomerApp, ShopApp

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


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Shop Management System")
        self.root.geometry("1270x900")

        # Title Label
        self.title_label = Label(root, text="Retail Shop Management System", font=("Arial", 30, "bold"), bg="#007bff",fg="white", pady=20)
        self.title_label.pack(fill=X)

        # Form Frame for adding products
        self.main_frame = Frame(root, padx=40, pady=40, bg="#f8f9fa", bd=3, relief=SOLID)
        self.main_frame.pack(pady=40)

        # Main Frame
        self.main_frame = Frame(root, bg="#ffffff", padx=40, pady=40)
        self.main_frame.pack(pady=20)

        # Sales Management Button
        self.sales_button = Button(self.main_frame, text="Sales Management", width=20, font=("Arial", 16), bg="#28a745",fg="black", command=self.open_sales)
        self.sales_button.pack(pady=10)

        # Inventory Management Button
        self.inventory_button = Button(self.main_frame, text="Inventory Management", width=20, font=("Arial", 16),bg="#007bff", fg="black", command=self.open_inventory)
        self.inventory_button.pack(pady=10)

        # Customer Management Button
        self.customer_button = Button(self.main_frame, text="Customer Management", width=20, font=("Arial", 16),bg="#17a2b8", fg="black", command=self.open_customer)
        self.customer_button.pack(pady=10)

        # Generate Sales Report Button
        self.report_button = Button(self.main_frame, text="Generate Sales Report", width=20, font=("Arial", 16), bg="#ffc107", fg="black", command=generate_sales_report)
        self.report_button.pack(pady=10)

        # Admin Page Button
        self.admin_button = Button(self.main_frame, text="Admin Page", width=20, font=("Arial", 16), bg="#dc3545",fg="black", command=self.admin_page)
        self.admin_button.pack(pady=10)

    def open_sales(self):
        sales = Toplevel(self.root)
        SalesApp(sales)

    def open_inventory(self):
        inventory = Toplevel(self.root)
        InventoryApp(inventory)

    def open_customer(self):
        customer = Toplevel(self.root)
        CustomerApp(customer)

    def admin_page(self):
        adm = Toplevel(self.root)
        ShopApp(adm)

if __name__ == "__main__":
    root = Tk()
    main_menu = MainMenu(root)
    root.mainloop()
