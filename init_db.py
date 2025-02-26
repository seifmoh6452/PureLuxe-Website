from app import app, db, Product

def init_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create products
        products = [
            {
                'name': 'PureLuxe BodyWash',
                'description': 'Our signature cleanser with natural ingredients for deep cleansing without stripping natural oils. Promotes healthy skin and enhances natural glow.',
                'price': 149.99,
                'image_url': 'PureLuxe Signature Cleanser.jpg',
                'size': '250ml',
                'stock': 100,
                'product_type': 'Body Care'
            },
            {
                'name': 'PureLuxe Clarifying Cleanser',
                'description': 'Gentle clarifying cleanser for sensitive skin',
                'price': 189.99,
                'image_url': 'PureLuxe Clarifying Cleanser.jpg',
                'size': '150ml',
                'stock': 100,
                'product_type': 'Cleanser'
            },
            {
                'name': 'PureLuxe Sensitive Formula',
                'description': 'Specially formulated for sensitive skin',
                'price': 169.99,
                'image_url': 'PureLuxe Sensitive Formula.jpg',
                'size': '200ml',
                'stock': 100,
                'product_type': 'Shampoo'
            },
            {
                'name': 'PureLuxe Travel Companion',
                'description': 'Perfect travel-sized skin care set',
                'price': 69.99,
                'image_url': 'PureLuxe Travel Companion.jpg',
                'size': '100ml',
                'stock': 100,
                'product_type': 'Travel Kit'
            },
            {
                'name': 'PureLuxe Professional Size',
                'description': 'Professional-sized skin care products',
                'price': 249.99,
                'image_url': 'PureLuxe Professional Size.jpg',
                'size': '500ml',
                'stock': 100,
                'product_type': 'Shampoo'
            },
            {
                'name': 'PureLuxe Hydration Boost',
                'description': 'Intensive hydration treatment',
                'price': 159.99,
                'image_url': 'PureLuxe Hydration Boost.jpg',
                'size': '200ml',
                'stock': 100,
                'product_type': 'Conditioner'
            },
            {
                'name': 'PureLuxe Intensive Treatment',
                'description': 'Deep intensive skin treatment',
                'price': 179.99,
                'image_url': 'PureLuxe Intensive Treatment.jpg',
                'size': '250ml',
                'stock': 100,
                'product_type': 'Hair Mask'
            },
            {
                'name': 'PureLuxe Gift Set',
                'description': 'Luxury gift set with our best products',
                'price': 299.99,
                'image_url': 'PureLuxe Gift Set.jpg',
                'size': 'Various',
                'stock': 100,
                'product_type': 'Gift Set'
            },
            {
                'name': 'PureLuxe Family Size',
                'description': 'Large family-sized skin care products',
                'price': 249.99,
                'image_url': 'PureLuxe Family Size.jpg',
                'size': '500ml',
                'stock': 100,
                'product_type': 'Shampoo'
            }
        ]
        
        # Add products to database
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        # Commit changes
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db() 