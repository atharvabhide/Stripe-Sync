import uuid
from sqlalchemy import (
    Column, String, DateTime, func
)
from db.database import Base
from pydantic import BaseModel


class Customer(Base):
    '''
    Customer model

    Attributes
    ----------
    id : str
        Customer id
    name : str
        Customer name
    email : str
        Customer email
    '''
    __tablename__ = "customer"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())

class CustomerCreateUpdate(BaseModel):
    '''
    CustomerCreateUpdate model

    Attributes
    ----------
    name : str
        Customer name
    email : str
        Customer email
    '''
    name: str
    email: str