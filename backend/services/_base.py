from sqlalchemy.orm import Session
from database import db
import logging

logger = logging.getLogger(__name__)

class BaseService:
    def __init__(self) -> None:
        self.session: Session = db.session
