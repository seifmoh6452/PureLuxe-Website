from app import app, db, Order, OrderItem

def clear_all_orders():
    try:
        # First delete all order items
        print("Deleting all order items...")
        OrderItem.query.delete()
        
        # Then delete all orders
        print("Deleting all orders...")
        Order.query.delete()
        
        # Commit the changes
        db.session.commit()
        print("Successfully cleared all orders from the database!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error clearing orders: {str(e)}")

if __name__ == "__main__":
    with app.app_context():
        clear_all_orders() 