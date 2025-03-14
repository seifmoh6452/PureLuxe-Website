from app import app, db

with app.app_context():
    # Drop all existing tables
    db.drop_all()
    
    # Create all tables with the new schema
    db.create_all()
    
    print("Database initialized successfully!") 