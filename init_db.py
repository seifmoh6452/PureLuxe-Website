from app import app, db, Product

with app.app_context():
    # Drop all existing tables
    db.drop_all()
    
    # Create all tables with the new schema
    db.create_all()
    
    # Add products
    products = [
        Product(
            name='PureLuxe Body Wash',  
            description='Our classic body wash for daily use.',  
            price=129.00,
            image_url='PureLuxe Signature Cleanser.jpg',  
            size='200ml',
            stock=50,
            product_type='Body Wash'  
        ),
        Product(
            name='PureLuxe Clarifying Cleanser',
            description='Deep cleansing formula that removes impurities while maintaining skin balance.',
            price=149.00,
            image_url='PureLuxe Clarifying Cleanser.jpg',
            size='200ml',
            stock=50,
            product_type='Cleanser'
        ),
        Product(
            name='PureLuxe Family Size',
            description='Generous family-sized packaging for extended use.',
            price=249.00,
            image_url='PureLuxe Family Size.jpg',
            size='500ml',
            stock=40,
            product_type='Family Pack'
        ),
        Product(
            name='PureLuxe Gift Set',
            description='Luxurious gift set featuring our premium products.',
            price=399.00,
            image_url='PureLuxe Gift Set.jpg',
            size='Set',
            stock=30,
            product_type='Gift Set'
        ),
        Product(
            name='PureLuxe Hydration Boost',
            description='Intensive hydration formula for all skin types.',
            price=169.00,
            image_url='PureLuxe Hydration Boost.jpg',
            size='50ml',
            stock=45,
            product_type='Hydrator'
        ),
        Product(
            name='PureLuxe Intensive Treatment',
            description='Advanced treatment for specific skin concerns.',
            price=199.00,
            image_url='PureLuxe Intensive Treatment.jpg',
            size='30ml',
            stock=35,
            product_type='Treatment'
        ),
        Product(
            name='PureLuxe Professional Size',
            description='Professional-grade size for salons and frequent users.',
            price=349.00,
            image_url='PureLuxe Professional Size.jpg',
            size='1000ml',
            stock=25,
            product_type='Professional'
        ),
        Product(
            name='PureLuxe Sensitive Formula',
            description='Gentle formula specially designed for sensitive skin.',
            price=159.00,
            image_url='PureLuxe Sensitive Formula.jpg',
            size='200ml',
            stock=40,
            product_type='Sensitive'
        ),
        Product(
            name='PureLuxe Travel Companion',
            description='Travel-friendly sizes of our essential products.',
            price=119.00,
            image_url='PureLuxe Travel Companion.jpg',
            size='Travel Set',
            stock=60,
            product_type='Travel'
        )
    ]
    
    # Add products to database
    for product in products:
        db.session.add(product)
    
    # Commit changes
    db.session.commit()
    
    print("Database initialized successfully with all 9 products!")