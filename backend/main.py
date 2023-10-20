from fastapi import (
    FastAPI, Depends, HTTPException, status
)
from sqlalchemy.orm import Session
from db.database import (
    engine, SessionLocal, create_tables
)
from db.customer_repository import (
    create_customer, get_customer, get_customers, update_customer, delete_customer
)
from models.customer import (
    Customer, CustomerCreateUpdate
)
import uuid

app = FastAPI()

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
        return create_customer(db, db_customer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/customers/{customer_id}", status_code=status.HTTP_200_OK)
def read_customer(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    '''
    Read a Customer

    Parameters
    ----------
    customer_id : uuid.UUID
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
def update_customer_api(customer_id: uuid.UUID, customer: CustomerCreateUpdate, db: Session = Depends(get_db)):
    '''
    Update a Customer

    Parameters
    ----------
    customer_id : uuid.UUID
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
        return update_customer(db, db_customer, customer_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer_api(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    '''
    Delete a Customer

    Parameters
    ----------
    customer_id : uuid.UUID
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
        return {"message": "Customer deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    create_tables()
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
