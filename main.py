from fastapi import Depends,FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from schema import Product
from typing import List
from database import session, engine
import models
from sqlalchemy.orm import Session

app = FastAPI() 


# Create all database tables from the models
models.Base.metadata.create_all(bind = engine)
# prints metadata content 
# print(models.Base.metadata.tables)


# decorator 
# routes
@app.get("/")
def greet():
    return "hello, how are you"
                 
products = [
    Product(id = 1,name = "iphone",price = 55.6),
    Product(id = 2,name = "realme",price = 55.4),
    Product(id = 3,name = "vivo",price = 55.7),
    Product(id = 4,name = "moto",price = 55.3),
]

#dependency 
def get_db():
    db = session()
    try:
        yield db 
    finally:
        db.close()


def init_db():
    db = session()

# it is used for count because id is primary key
    count = db.query(models.Product).count
# i can insert the values when table is empty because of count
    if count == 0:
        for product in products:
            db.add(models.Product(**product.model_dump()))

        db.commit()
init_db()


# read and fetch data
@app.get("/orders")
def get_product(db: Session = Depends(get_db)):  #dependency injection
    db_products =  db.query(models.Product).all()


    return db_products


@app.get("/product/{id}")
def get_product_id(id : int, db: Session = Depends(get_db)):
    db_products = db.query(models.Product).filter(models.Product.id == id).first()
    if db_products:
        return db_products
        
    return "product not found"

# add data
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(models.Product(**product.model_dump()))
    db.commit()
    return products

@app.post("/products/values")
def add_multiple_values(items: List[Product]):
    products.extend(items)
    return items

@app.put("/products")
def update(id :  int, product : Product, db: Session = Depends(get_db)):
    db_products = db.query(models.Product).filter(models.Product.id == id).first()
    if db_products:
            db_products.name = product.name
            db_products.price = product.price
            db.commit()
            return "Updated successfully"
    else:    
        return "Product Not Found"

@app.delete("/products")
def delete_item(id : int, db:  Session = Depends(get_db)):
    db_products = db.query(models.Product).filter(models.Product.id == id).first()
    if db_products:
        db.delete(db_products)
        db.commit()
        return "deleted successfully"
    else:     
        return "product not found"












# practice code get,put,post
"""@app.post("/products")
def add_products(product: Product):
   products.append(product)
   return product
    

# DYNAMIC(CAN CHANGE)
# use exception for this error
@app.get("/products/{id}")
def get_products(id : int):
    products = ["laptop lelo kam ayega","mouse lelo kam ayega","keyboard lelo kam ayega","webcam lelo kam ayega"]
    return products[id]

# STATIC(REMAINS SAME)
@app.get("/path")
def greeting():
  return "localhost"


@app.put("/products")
def update_items(id :  int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "added successfully"
    return "not found"

@app.put("/products")
def update_product(id : int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "added successfully"
    return "id not found"  


def get_db():

    Dependency function to provide a database session.
    It creates a new session for each request and ensures
    the session is properly closed after the request completes.
    
    # Create a new database session
    db = session()
    
    try:
        # Yield the session to the route function.
        # FastAPI injects this into endpoints using Depends(get_db).
        yield db
    
    finally:
        # This block runs after the request is finished,
        # even if an exception occurs.
        # It ensures the database connection is closed properly.
        db.close()         """