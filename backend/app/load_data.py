import csv
from app.database import SessionLocal, engine, Base
from app.models import Product, Customer, Order # Add other models
from datetime import datetime

# Create tables in the database
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def load_csv(filepath, model, date_columns=None):
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert date strings to datetime objects if needed
            if date_columns:
                for col in date_columns:
                    if row[col]:
                        row[col] = datetime.strptime(row[col], '%Y-%m-%d %H:%M:%S')
            
            # For columns with different names in CSV vs model
            # Example: if csv has 'id' but model has 'product_id'
            # if 'id' in row:
            #     row['product_id'] = row.pop('id')

            db_item = model(**row)
            db.add(db_item)
        db.commit()
    print(f"Loaded data from {filepath} into {model.__tablename__}")

# Place your downloaded CSVs into the backend/data/ directory
load_csv('data/products.csv', Product)
load_csv('data/customers.csv', Customer)
load_csv('data/orders.csv', Order, date_columns=['order_date'])
# TODO: Call for order_items.csv and reviews.csv

db.close()