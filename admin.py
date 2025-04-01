import sqlite3
from _datetime import datetime
from tkinter import *
from tkinter import messagebox, ttk

import tkinter as tk

conn = sqlite3.connect('shop_sys_db')
cursor = conn.cursor()


# Initialize Database
def init_db():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                    (product_id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER, barcode TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales 
                    (sale_id INTEGER PRIMARY KEY, product_id INTEGER, customer_id INTEGER, quantity INTEGER, sale_date TEXT,
                    FOREIGN KEY(product_id) REFERENCES products(product_id)
                    FOREIGN KEY(customer_id) REFERENCES customers(customer_id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers 
                    (customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    conn.commit()
    conn.close()


# Adding a Product
def add_product(name, price, stock, barcode):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, stock, barcode) VALUES (?, ?, ?, ?)', (name, price, stock, barcode))
    conn.commit()
    conn.close()


# Fetching all products
def fetch_products():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products


# Sale Processing
def process_sale(product_id, quantity, customer_id):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    # Reduce stock
    cursor.execute('SELECT stock FROM products WHERE product_id = ?', (product_id,))
    stock = cursor.fetchone()[0]

    if stock >= quantity:
        new_stock = stock - quantity
        cursor.execute('UPDATE products SET stock = ? WHERE product_id = ?', (new_stock, product_id))

        # Record sale
        sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO sales (product_id, customer_id, quantity, sale_date) VALUES (?, ?, ?, ?)',
                       (product_id, customer_id, quantity, sale_date))
        conn.commit()
        messagebox.showinfo("Success", "Sale processed successfully!")
    else:
        messagebox.showerror("Error", "Not enough stock available!")

    conn.close()


# Initialize Database
init_db()


class ShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Shop Management System")
        self.root.geometry("1270x900")
        self.root.config(bg="#f8f9fa")



        # Title
        title = Label(root, text="Retail Shop Management System", font=("Arial", 24, "bold"), bg="#007bff", fg="white",
                      pady=10)
        title.pack(fill=X)

        # Form Frame for adding products
        form_frame = Frame(root, padx=60, pady=60, bg="#f8f9fa", bd=3, relief=SOLID)
        form_frame.pack(pady=20)

        # Product Name
        self.name_label = Label(form_frame, text="Product Name", font=("Arial", 20, "bold"), bg="#f8f9fa", fg="#343a40")
        self.name_label.grid(row=0, column=0, padx=30, pady=20, sticky=W)
        self.name_entry = Entry(form_frame, font=("Arial", 20), bd=3, relief=SOLID, bg="white", fg="black", width=25)
        self.name_entry.grid(row=0, column=1, padx=30, pady=20)

        # Price
        self.price_label = Label(form_frame, text="Price", font=("Arial", 20, "bold"), bg="#f8f9fa", fg="#343a40")
        self.price_label.grid(row=1, column=0, padx=30, pady=20, sticky=W)
        self.price_entry = Entry(form_frame, font=("Arial", 20), bd=3, relief=SOLID, bg="white", fg="black", width=25)
        self.price_entry.grid(row=1, column=1, padx=30, pady=20)

        # Stock
        self.stock_label = Label(form_frame, text="Stock", font=("Arial", 20, "bold"), bg="#f8f9fa", fg="#343a40")
        self.stock_label.grid(row=2, column=0, padx=30, pady=20, sticky=W)
        self.stock_entry = Entry(form_frame, font=("Arial", 20), bd=3, relief=SOLID, bg="white", fg="black", width=25)
        self.stock_entry.grid(row=2, column=1, padx=30, pady=20)

        # Barcode
        self.barcode_label = Label(form_frame, text="Barcode", font=("Arial", 20, "bold"), bg="#f8f9fa", fg="#343a40")
        self.barcode_label.grid(row=3, column=0, padx=30, pady=20, sticky=W)
        self.barcode_entry = Entry(form_frame, font=("Arial", 20), bd=3, relief=SOLID, bg="white", fg="black", width=25)
        self.barcode_entry.grid(row=3, column=1, padx=50, pady=20)

        # Add Product Button
        self.add_button = Button(form_frame, text="Add Product", font=("Arial", 18, "bold"), bg="#28a745", fg="black",
                                 bd=0, relief=FLAT, padx=20, pady=15, cursor="hand", command=self.add_product)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Product List Section
        self.product_list_label = Label(self.root, text="Product List", font=("Helvetica Neue", 28, "bold"),
                                        bg="#007bff", fg="white", pady=10)
        self.product_list_label.pack(fill=BOTH)

        # Frame for the product list with rounded corners
        self.product_list_frame = Frame(self.root, bg="#ffffff", padx=20, pady=20, bd=5, height=90, relief=SOLID)
        self.product_list_frame.pack(pady=10)

        # Listbox for displaying products with improved styling
        self.product_list = Listbox(self.product_list_frame, font=("Helvetica Neue", 16), width=50, bd=0,
                                    bg="#ffffff", fg="black", selectbackground="#e0e0e0", activestyle="none")
        self.product_list.pack(side=LEFT, fill=BOTH)

        # Scrollbar for the product list
        scrollbar = Scrollbar(self.product_list_frame, orient="vertical", command=self.product_list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.product_list.config(yscrollcommand=scrollbar.set)
        # Populate the product list
        self.load_products()

    def add_product(self):
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        stock = int(self.stock_entry.get())
        barcode = self.barcode_entry.get()
        # You would use a real database function here
        add_product(name, price, stock, barcode)
        self.load_products()
        messagebox.showinfo("Success", "Product added successfully!")

    def load_products(self):
        self.product_list.delete(0, END)
        # You would fetch real products from the database
        products = fetch_products()
        for product in products:
            self.product_list.insert(END,
            f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]:.2f}, Stock: {product[3]}, Barcode: {product[4]}")

class SalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Management")
        self.root.geometry("1270x900")
        self.root.config(bg="#f8f9fa")

        # Frame for the form
        self.form_frame = ttk.Frame(root, padding="20")
        self.form_frame.pack(pady=20)

        # Title Label
        self.title_label = ttk.Label(self.form_frame, text="Sales Management", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Product ID
        self.product_id_label = ttk.Label(self.form_frame, text="Product ID:")
        self.product_id_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.product_id_entry = ttk.Entry(self.form_frame, width=30)
        self.product_id_entry.grid(row=1, column=1, padx=(0, 20))

        # Quantity
        self.quantity_label = ttk.Label(self.form_frame, text="Quantity:")
        self.quantity_label.grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.quantity_entry = ttk.Entry(self.form_frame, width=30)
        self.quantity_entry.grid(row=2, column=1, padx=(0, 20))

        # Customer ID
        self.customer_id_label = ttk.Label(self.form_frame, text="Customer ID:")
        self.customer_id_label.grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        self.customer_id_entry = ttk.Entry(self.form_frame, width=30)
        self.customer_id_entry.grid(row=3, column=1, padx=(0, 20))

        # Process Sale Button
        self.sale_button = ttk.Button(self.form_frame, text="Process Sale", command=self.process_sale)
        self.sale_button.grid(row=4, column=0, columnspan=2, pady=(20, 0))

        # Additional Styling
        for widget in self.form_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)  # Adding padding around widgets

    def process_sale(self):
        product_id = int(self.product_id_entry.get().strip())
        quantity = int(self.quantity_entry.get().strip())
        customer_id = int(self.customer_id_entry.get().strip())

        process_sale(product_id, quantity, customer_id)

def process_sale(product_id, quantity, customer_id):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    # Check product availability
    cursor.execute('SELECT stock, price FROM products WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()

    if not product:
        messagebox.showerror("Error", "Product not found!")
        return

    stock, price = product

    if stock < quantity:
        messagebox.showerror("Error", "Insufficient stock!")
        return

    # Reduce stock
    new_stock = stock - quantity
    cursor.execute('UPDATE products SET stock = ? WHERE product_id = ?', (new_stock, product_id))

    # Record sale
    sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO sales (product_id, customer_id, quantity, sale_date) VALUES (?, ?, ?, ?)',
                   (product_id, customer_id, quantity, sale_date))

    conn.commit()
    messagebox.showinfo("Success", f"Sale of {quantity} units processed successfully!")


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management")
        self.root.geometry("1270x900")
        self.root.config(bg="#f8f9fa")

        # Title Label
        self.title_label = Label(root, text="Inventory Management", font=("Arial", 24, "bold"), bg="#007bff",
                                 fg="white", pady=10)
        self.title_label.pack(fill=X)

        # Form Frame
        self.form_frame = Frame(root, bg="#ffffff", padx=40, pady=40)
        self.form_frame.pack(pady=20)

        # Product ID Label and Entry
        self.product_id_label = Label(self.form_frame, text="Product ID", font=("Arial", 18, "bold"), bg="#ffffff",
                                      fg="#343a40")
        self.product_id_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.product_id_entry = Entry(self.form_frame, font=("Arial", 16), bd=2, relief=SOLID, bg="#ffffff",
                                      fg="#343a40", width=40)
        self.product_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Name Label and Entry
        self.name_label = Label(self.form_frame, text="Name (Optional)", font=("Arial", 18, "bold"), bg="#ffffff",
                                fg="#343a40")
        self.name_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.name_entry = Entry(self.form_frame, font=("Arial", 16), bd=2, relief=SOLID, bg="#ffffff", fg="#343a40",
                                width=40)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Price Label and Entry
        self.price_label = Label(self.form_frame, text="Price (Optional)", font=("Arial", 18, "bold"), bg="#ffffff",
                                 fg="#343a40")
        self.price_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.price_entry = Entry(self.form_frame, font=("Arial", 16), bd=2, relief=SOLID, bg="#ffffff", fg="#343a40",
                                 width=40)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)


        # Stock Label and Entry
        self.stock_label = Label(self.form_frame, text="Stock (Optional)", font=("Arial", 18, "bold"), bg="#ffffff",
                                 fg="black")
        self.stock_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.stock_entry = Entry(self.form_frame, font=("Arial", 16), bd=2, relief=SOLID, bg="#ffffff", fg="black",
                                 width=40)
        self.stock_entry.grid(row=3, column=1, padx=10, pady=10)

        # Update Product Button
        self.update_button = Button(self.form_frame, text="Update Product", font=("Arial", 16, "bold"), bg="#28a745",
                                    fg="black", bd=0, cursor="hand", relief=FLAT, padx=20, pady=10, command=self.update_product)
        self.update_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Delete Product Button
        self.delete_button = Button(self.form_frame, text="Delete Product", font=("Arial", 16, "bold"), bg="#dc3545",
                                    fg="black", bd=0,cursor="hand", relief=FLAT, padx=20, pady=10, command=self.delete_product)
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=10)

    def update_product(self):
        product_id = int(self.product_id_entry.get())
        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        if name:
            cursor.execute('UPDATE products SET name = ? WHERE product_id = ?', (name, product_id))
        if price:
            cursor.execute('UPDATE products SET price = ? WHERE product_id = ?', (float(price), product_id))
        if stock:
            cursor.execute('UPDATE products SET stock = ? WHERE product_id = ?', (int(stock), product_id))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product updated successfully!")

    def delete_product(self):
        product_id = int(self.product_id_entry.get())

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product deleted successfully!")


class CustomerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Management")
        self.root.geometry("1270x900")
        self.root.config(bg="#f8f9fa")

        # Title Label
        self.title_label = Label(root, text="Customer Management", font=("Arial", 24, "bold"), bg="#007bff", fg="white",
                                 pady=10)
        self.title_label.pack(fill=X)

        # Form Frame
        self.form_frame = Frame(root, bg="#ffffff", padx=40, pady=40)
        self.form_frame.pack(pady=20)

        # Customer Name Label and Entry
        self.name_label = Label(self.form_frame, text="Customer Name", font=("Arial", 18, "bold"), bg="#ffffff",
                                fg="#343a40")
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.name_entry = Entry(self.form_frame, font=("Arial", 16), bd=2, relief=SOLID, bg="#ffffff", fg="#343a40",
                                width=40)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Customer Email Label and Entry
        self.email_label = Label(self.form_frame, text="Customer Email", font=("Arial", 18, "bold"), bg="#ffffff",
                                 fg="#343a40")
        self.email_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.email_entry = Entry(self.form_frame, font=("Arial", 16), bd=2, relief=SOLID, bg="#ffffff", fg="#343a40",
                                 width=40)
        self.email_entry.grid(row=1, column=1, padx=10, pady=10)

        # Add Customer Button
        self.add_button = Button(self.form_frame, text="Add Customer", font=("Arial", 16, "bold"), bg="#28a745",
                                 fg="black", bd=0, cursor="hand", relief=FLAT, padx=20, pady=10, command=self.add_customer)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=20)

    def add_customer(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO customers (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Customer added successfully!")



if __name__ == "__main__":
    root = Tk()
    app = ShopApp(root)
    root.mainloop()
