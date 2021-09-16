# dbo_models/customer.py
import uuid
from database import db
from sqlalchemy import VARCHAR, Integer, DateTime
from datetime import datetime
from dto_models.customer import CustomerDTO
from ._helper import GUID


class CustomerDBO(db.Model):
    __tablename__ = "customer"
    first_name = db.Column(VARCHAR(50), nullable=False)
    last_name = db.Column(VARCHAR(50), nullable=False)
    phone_number = db.Column(VARCHAR(15), nullable=False)
    email = db.Column(VARCHAR(50), nullable=False)
    street = db.Column(VARCHAR(100), nullable=True)
    city = db.Column(VARCHAR(20), nullable=True)
    state = db.Column(VARCHAR(15), nullable=True)
    zipcode = db.Column(Integer, nullable=True)
    reward_point = db.Column(Integer, nullable=True)

    id = db.Column(GUID, primary_key=True, default=uuid.uuid4)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow())

    def __init__(self, first_name: str, last_name: str, phone_number: str, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
