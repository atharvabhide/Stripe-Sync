import uuid
from sqlalchemy import (
    Column, String, DateTime, func
)
from sqlalchemy.schema import UniqueConstraint
from db.database import Base
from pydantic import BaseModel
from typing import Optional

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
    email = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())

    __table_args__ = (UniqueConstraint('email'),)

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
    id: Optional[str]
    name: str
    email: str