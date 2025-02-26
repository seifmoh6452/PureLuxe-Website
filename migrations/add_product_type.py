from flask_migrate import Migrate
from app import app, db, Product
from sqlalchemy import text

migrate = Migrate(app, db)

def upgrade():
    with app.app_context():
        # Add the product_type column if it doesn't exist
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE product ADD COLUMN IF NOT EXISTS product_type VARCHAR(50)"))
            
        # Update existing products with types
        products = Product.query.all()
        for product in products:
            if not product.product_type:  # Only update if type is not set
                if "shampoo" in product.name.lower():
                    product.product_type = "Shampoo"
                elif "conditioner" in product.name.lower():
                    product.product_type = "Conditioner"
                elif "cleanser" in product.name.lower():
                    product.product_type = "Skin Care"
                else:
                    product.product_type = "Hair Care"  # default category
        
        db.session.commit()
        print("Migration completed successfully!")

if __name__ == "__main__":
    upgrade() 