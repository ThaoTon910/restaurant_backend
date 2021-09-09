# dbo_models/customer.py
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

    id = db.Column(GUID, primary_key=True)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow())

    def __init__(self, dto: CustomerDTO):
        self.id = dto.id
        self.first_name = dto.first_name.strip()
        self.last_name = dto.last_name.strip()
        self.phone_number = dto.phone_number.strip()
        self.email = dto.email.strip()
        self.street = dto.street
        self.city = dto.city
        self.state = dto.state
        self.zipcode = dto.zipcode
        self.reward_point = dto.reward_point
