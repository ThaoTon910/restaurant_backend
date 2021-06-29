import os
import connexion
from flask import Response, Flask
from flask_migrate import Migrate
from flask_cors import CORS
from database import db
from settings import flask_config
from uuid import UUID
from resources.category import CategoryResource
from resources.menu_item import MenuItemResource
import logging

logger = logging.getLogger(__name__)
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
MIGRATION_DIR = os.path.join(CURRENT_DIR, "migrations")

def create_app():
    # create and configure the app
    options = {"swagger_ui": True}
    app = connexion.FlaskApp(__name__, specification_dir=CURRENT_DIR, options=options) #Connexion App
    flask_app: Flask = app.app # Flask app
    CORS(flask_app)

    flask_app.config.from_object(flask_config)
    app.add_api('app.yaml', validate_responses=True, strict_validation=True)

    #database migration
    db.init_app(flask_app)
    migrate = Migrate(flask_app, db, directory=MIGRATION_DIR)

    app.run(port=8080)
    return app, flask_app


def get_merchant(merchant_id: UUID) -> Response:
    return {}#MerchantResource.get(merchant_id)

def create_merchant() -> Response:
    return {}#MerchantResource.post()

def create_category() -> Response:
    return CategoryResource.post()

def get_all_categories() -> Response:
    return CategoryResource.get_all_categories()

def get_category(category_id: UUID) -> Response:
    return CategoryResource.get_by_id(category_id)

def delete_category(category_id: UUID) -> Response:
    return CategoryResource.delete(category_id)

def update_category(category_id: UUID) -> Response:
    return {}#CategoryResource.update(category_id)

def create_menu_item() -> Response:
    return MenuItemResource.post()

def get_all_menu_items() -> Response:
    return MenuItemResource.get_all_menu_items()

def get_menu_item(menu_item_id: UUID) -> Response:
    return MenuItemResource.get_by_id(menu_item_id)

def delete_menu_item(menu_item_id: UUID) -> Response:
    return MenuItemResource.delete(menu_item_id)

def update_menu_item(menu_item_id: UUID) -> Response:
    return {}#MenuItemResource.update(menu_item_id)


app, flask_app = create_app()
