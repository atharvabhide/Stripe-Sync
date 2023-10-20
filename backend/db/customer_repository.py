from sqlalchemy.orm import Session
from models.customer import Customer
import uuid

def create_customer(db: Session, customer: Customer):
    '''
    Create a new Customer

    Parameters
    ----------
    customer : Customer
        Customer data
    db: Session
        Database session

    Returns
    -------
    Customer
        The created customer
    '''
    try:
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    except Exception as e:
        raise e

def get_customer(db: Session, customer_id: uuid.UUID):
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
        return db.query(Customer).filter(Customer.id == str(customer_id)).first()
    except Exception as e:
        raise e

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    '''
    Read all Customers

    Parameters
    ----------
    skip : int, optional
        Skip the first n customers, by default 0
    limit : int, optional
        Limit the number of customers, by default 100

    Returns
    -------
    list
        List of customers
    '''
    try:
        return db.query(Customer).offset(skip).limit(limit).all()
    except Exception as e:
        raise e

def update_customer(db: Session, customer: Customer, customer_id: uuid.UUID):
    '''
    Update a Customer

    Parameters
    ----------
    customer : Customer
        Customer data
    customer_id : uuid.UUID
        Customer id
    db: Session
        Database session

    Returns
    -------
    Customer
        The updated customer
    '''
    try:
        existing_customer = db.query(Customer).filter(Customer.id == str(customer.id)).first()
        if existing_customer:
            existing_customer.name = customer.name
            existing_customer.email = customer.email
            db.commit()
            db.refresh(existing_customer)
            return existing_customer
        return None
    except Exception as e:
        raise e

def delete_customer(db: Session, customer_id: uuid.UUID):
    '''
    Delete a Customer

    Parameters
    ----------
    customer_id : uuid.UUID
        Customer id

    Returns
    -------
    bool
        True if the customer was deleted, False otherwise
    '''
    try:
        customer = get_customer(db, customer_id)
        if customer:
            db.delete(customer)
            db.commit()
            return True
        return False
    except Exception as e:
        raise e