# services/customer.py
from dto_models.customer import CustomerDTO
from dbo_models.customer import CustomerDBO
from converters.customer import customer_dbo_to_dto, customer_dto_to_dbo
from services._base import BaseService
from utils.exceptions import *
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)


class CustomerService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_id_exist(self, customer_id: UUID) -> bool:
        if customer_id is None:
            return False
        return self.session.query(CustomerDBO).filter_by(id=customer_id).first()

    # create new promotion type
    def create(self, dto: CustomerDTO) -> CustomerDTO:
        dbo = customer_dto_to_dbo(dto)
        if self._is_id_exist(dbo.id):
            raise ObjectAlreadyExists(f"Promotion type '{dbo.id}' already exist")

        self.session.add(dbo)
        self.session.commit()
        return customer_dbo_to_dto(dbo)

    def get_all_customer(self) -> List[CustomerDTO]:
        dbo_list = self.session.query(CustomerDBO).all()
        if not dbo_list:
            raise ObjectNotFound("Customers's info fetch failed")
        return [customer_dbo_to_dto(dbo) for dbo in dbo_list]

    def get_by_id(self, customer_id: UUID) -> CustomerDTO:
        dbo = self.session.query(CustomerDBO).filter_by(id=customer_id).first()
        if not dbo:
            raise ObjectNotFound(f" Id '{customer_id}' not found")

        return customer_dbo_to_dto(dbo)

    def delete(self, customer_id: UUID) -> CustomerDTO:
        dbo = self.session.query(CustomerDBO).filter_by(id=customer_id).first()
        if not dbo:
            raise ObjectNotFound(f" Try to delete a customer data, but the Id: "
                                 "'{customer_id}' is not found")

        self.session.delete(dbo)
        self.session.commit()
        return customer_dbo_to_dto(dbo)

    def update(self, dto: CustomerDTO) -> CustomerDTO:
        if dto.id is not None:
            if self._is_id_exist(dto.id):
                dbo = self.session.query(CustomerDBO).filter_by(id=dto.id).first()
                if not dbo:
                    raise ObjectNotFound(f" Id '{dto.id}' not found")
                dbo.first_name = dto.last_name

                self.session.commit()

                return customer_dbo_to_dto(dbo)
        return None