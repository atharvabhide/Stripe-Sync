from fastapi import (
    FastAPI, Depends, HTTPException, status
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import (
    engine, SessionLocal, create_tables
)
from db.customer_repository import (
    create_customer, get_customer, get_customers, update_customer, delete_customer, get_customer_from_email
)
from models.customer import (
    Customer, CustomerCreateUpdate
)
from kafka.producer import (
    publish_customer_created, publish_customer_updated, publish_customer_deleted
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    '''
    Create a new database session for each request
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/customers/", status_code=status.HTTP_201_CREATED)
def create_customer_api(customer: CustomerCreateUpdate, db: Session = Depends(get_db)):
    '''
    Create a new Customer

    Parameters
    ----------
    customer : CustomerCreateUpdate
        Customer data
    db: Session
        Database session

    Returns
    -------
    Customer
        The created customer
    '''
    try:
        db_customer = Customer(**customer.dict())
        db_customer = create_customer(db, db_customer)

        # Publish a customer created event
        customer_data = {
            'id': str(db_customer.id),
            'name': db_customer.name,
            'email': db_customer.email,
            'created_at': str(db_customer.created_at),
            'updated_at': str(db_customer.updated_at)
        }
        publish_customer_created(customer_data)
        return db_customer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/customers/{customer_id}", status_code=status.HTTP_200_OK)
def read_customer(customer_id: str, db: Session = Depends(get_db)):
    '''
    Read a Customer

    Parameters
    ----------
    customer_id : str
        Customer id
    db: Session
        Database session

    Returns
    -------
    Customer
        The customer
    '''
    try:
        db_customer = get_customer(db, customer_id)
        if db_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return db_customer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/customers/", status_code=status.HTTP_200_OK)
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''
    Read all Customers

    Parameters
    ----------
    skip : int, optional
        Skip the first n customers, by default 0
    limit : int, optional
        Limit the number of customers, by default 100
    db: Session
        Database session

    Returns
    -------
    [Customer]
        List of customers
    '''
    try:
        return get_customers(db, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/customers/{customer_id}", status_code=status.HTTP_200_OK)
def update_customer_api(customer_id: str, customer: CustomerCreateUpdate, db: Session = Depends(get_db)):
    '''
    Update a Customer

    Parameters
    ----------
    customer_id : str
        Customer id
    customer : CustomerCreateUpdate
        Customer data
    db: Session
        Database session

    Returns
    -------
    Customer
        The updated customer
    '''
    try:
        db_customer = Customer(**customer.dict())
        db_customer.id = customer_id
        if db_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        db_customer = update_customer(db, db_customer, customer_id)

        # Publish a customer updated event
        customer_data = {
            'id': str(db_customer.id),
            'name': db_customer.name,
            'email': db_customer.email,
            'created_at': str(db_customer.created_at),
            'updated_at': str(db_customer.updated_at)
        }
        publish_customer_updated(customer_data)

        return db_customer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer_api(customer_id: str, db: Session = Depends(get_db)):
    '''
    Delete a Customer

    Parameters
    ----------
    customer_id : str
        Customer id
    db: Session
        Database session

    Returns
    -------
    dict
        Message
    '''
    try:
        if not delete_customer(db, customer_id):
            raise HTTPException(status_code=404, detail="Customer not found")

        # Publish a customer deleted event
        customer_data = {
            'id': str(customer_id)
        }
        publish_customer_deleted(customer_data)
        
        return {"message": "Customer deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_id/{customer_email}", status_code=status.HTTP_200_OK)
def get_customer_id(customer_email: str, db: Session = Depends(get_db)):
    '''
    Get a Customer id

    Parameters
    ----------
    customer_email : str
        Customer email
    db: Session
        Database session

    Returns
    -------
    dict
        Customer id
    '''
    try:
        db_customer = get_customer_from_email(db, customer_email)
        if db_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return {"id": str(db_customer.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    create_tables()
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
