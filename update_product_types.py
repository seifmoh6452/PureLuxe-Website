from app import app, db, Product

def update_product_types():
    with app.app_context():
        products = Product.query.all()
        
        # Print current state
        print("Current product types:")
        for product in products:
            print(f"{product.name}: {product.product_type}")
        
        # Update products without types
        for product in products:
            if not product.product_type:
                if "shampoo" in product.name.lower():
                    product.product_type = "Shampoo"
                elif "conditioner" in product.name.lower():
                    product.product_type = "Conditioner"
                elif "cleanser" in product.name.lower():
                    product.product_type = "Skin Care"
                else:
                    product.product_type = "Hair Care"  # default category
        
        # Save changes
        db.session.commit()
        
        # Print updated state
        print("\nUpdated product types:")
        for product in products:
            print(f"{product.name}: {product.product_type}")

if __name__ == "__main__":
    update_product_types() 