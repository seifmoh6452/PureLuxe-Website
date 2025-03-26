import sqlite3
import os

# Connect to the database
db_path = os.path.join('instance', 'pureluxe.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add the product_type column if it doesn't exist
try:
    cursor.execute('ALTER TABLE product ADD COLUMN product_type TEXT')
except sqlite3.OperationalError:
    print("Column already exists")

# Get all products
cursor.execute('SELECT id, name FROM product')
products = cursor.fetchall()

# Update product types
for product_id, name in products:
    if "shampoo" in name.lower():
        product_type = "Shampoo"
    elif "conditioner" in name.lower():
        product_type = "Conditioner"
    elif "cleanser" in name.lower():
        product_type = "Skin Care"
    else:
        product_type = "Hair Care"
    
    cursor.execute('UPDATE product SET product_type = ? WHERE id = ?', (product_type, product_id))

# Commit changes and close connection
conn.commit()
conn.close()

print("Database updated successfully!") 