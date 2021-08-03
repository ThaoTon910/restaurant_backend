from sqlalchemy.orm import Session
from database import db
import logging

logger = logging.getLogger(__name__)

class BaseService:
    def __init__(self) -> None:
        self.session: Session = db.session

    def get_updated_key_value(self, dbo: db.Model):
        data = {}
        for key in dbo.__dict__.keys():
            if not key.startswith("_"):
                data[key] = dbo.__dict__[key]
        return data