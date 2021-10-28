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
from resources.addon_group import AddonGroupResource
from resources.addon import AddonResource
from resources.menu import MenuResource
from resources.merchant import MerchantResource
from resources.menu_item_to_addon_group import MenuItemToAddonGroupResource
from resources.promotion import PromotionResource
from resources.promotion_type import PromotionTypeResource
from resources.promocode import  PromoCodeResource
from resources.extra_percentage_all import  ExtraPercentageAllResource
from resources.order_resource import OrderResource
from dbo_models.extra_percentage_all import ExtraPercentageAllDBO
import logging

logger = logging.getLogger(__name__)
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
MIGRATION_DIR = os.path.join(CURRENT_DIR, "migrations")



def create_app():
    # initial app API
    os.system('swagger-cli bundle backend_api.yaml --outfile app_run.yaml --type yaml')
    # create and configure the app
    options = {"swagger_ui": True}
    app = connexion.FlaskApp(__name__, specification_dir=CURRENT_DIR, options=options) #Connexion App
    flask_app: Flask = app.app # Flask app
    CORS(flask_app)

    flask_app.config.from_object(flask_config)
    app.add_api('app_run.yaml', validate_responses=True, strict_validation=True)

    # database migration
    db.init_app(flask_app)
    migrate = Migrate(flask_app, db, directory=MIGRATION_DIR)

    app.run(port=8080)
    return app, flask_app


# Merchant
def create_merchant() -> Response:
    return MerchantResource.post()

def get_merchant() -> Response:
    return MerchantResource.get_merchant()

def delete_merchant() -> Response:
    return MerchantResource.delete()

def update_merchant() -> Response:
    return MerchantResource.update()

# def get_merchant(merchant_id: UUID) -> Response:
#     return {} # MerchantResource.get(merchant_id)
#order
# def initial_payment():
#     return OrderResource.create_payment()
def create_order():
    return OrderResource.post()
def update_order(order_id: UUID):
    return OrderResource.update_order(order_id)
def get_order(order_id: UUID):
    return  OrderResource.get_order(order_id)
def get_all_order():
    return  OrderResource.get_all_order()
def get_payment_intent():
    return OrderResource.create_payment_intent()




# Category
def create_category() -> Response:
    return CategoryResource.post()
def get_all_categories() -> Response:
    return CategoryResource.get_all_categories()
def get_category(id: UUID) -> Response:
    return CategoryResource.get_by_id(id)
def delete_category(id: UUID) -> Response:
    return CategoryResource.delete(id)
def update_category(id: UUID) -> Response:
    return CategoryResource.update(id)

#Menu Item
def create_menu_item() -> Response:
    return MenuItemResource.post()
def get_all_menu_items() -> Response:
    return MenuItemResource.get_all_menu_items()
def get_menu_items_from_category(id:UUID) -> Response:
    return MenuItemResource.get_menu_items_from_category(id)
def get_menu_item(id: UUID) -> Response:
    return MenuItemResource.get_by_id(id)
def update_menu_item(id: UUID) -> Response:
    return MenuItemResource.update(id)
def delete_menu_item(id: UUID) -> Response:
    return MenuItemResource.delete(id)

#Addon Group
def create_addon_group() -> Response:
    return AddonGroupResource.post()
def get_all_addon_groups() -> Response:
    return AddonGroupResource.get_all_addon_groups()
def get_addon_groups_from_menu_item(id:UUID) -> Response:
    return AddonGroupResource.get_addon_groups_from_menu_item(id)

def get_addon_group(id: UUID) -> Response:
    return AddonGroupResource.get_by_id(id)
def delete_addon_group( id: UUID) -> Response:
    return AddonGroupResource.delete(id)
def update(id: UUID) -> Response:
    return AddonGroupResource.update(id)

#Addon
def create_addon() -> Response:
    return AddonResource.post()
def get_all_addons() -> Response:
    return AddonResource.get_all_addons()
def get_addons_from_group(id:UUID) -> Response:
    return AddonResource.get_addons_from_group(id)
def get_addon(id: UUID) -> Response:
    return AddonResource.get_by_id(id)
def update_addon(id: UUID) -> Response:
    return AddonResource.update(id)
def delete_addon(id: UUID) -> Response:
    return AddonResource.delete(id)

#Menu Item to Addon Group
def create_menu_item_to_addon_group() -> Response:
    return MenuItemToAddonGroupResource.post()
def get_all_menu_item_to_addon_group() -> Response:
    return MenuItemToAddonGroupResource.get_all_menu_item_to_addon_group()
def delete_menu_item_to_addon_group(id: UUID, addon_group_id: UUID) -> Response:
    return MenuItemToAddonGroupResource.delete(id, addon_group_id)

def get_menu()->Response:
    return MenuResource.get_menu()

# get promo code
def validate_promo_code() -> Response:
    return PromoCodeResource.post()

# promotion functions
def create_promotion() -> Response:
    return PromotionResource.post()
def get_all_promotion() -> Response:
    return PromotionResource.get_all_promotion()
def get_promotion(id: UUID) -> Response:
    return PromotionResource.get_by_id(id)
def delete_promotion(id: UUID) -> Response:
    return PromotionResource.delete_promotion(id)
def update_promotion(id: UUID) -> Response:
    return PromotionResource.update_promotion(id)


# promotion type functions
def create_promotion_type() -> Response:
    return PromotionTypeResource.post()
def get_all_promotion_type() -> Response:
    return PromotionTypeResource.get_all_promotion_type()
def get_promotion_type(id: UUID) -> Response:
    return PromotionTypeResource.get_by_id(id)
def delete_promotion_type( id: UUID) -> Response:
    return PromotionTypeResource.delete_promotion_type(id)
def update_promotion_type( id: UUID) -> Response:
    return PromotionTypeResource.update_promotion_type(id)

# extra_percentage_all
def create_extra_percentage_all() -> Response:
    return ExtraPercentageAllResource.post()
def get_extra_percentage_all() -> Response:
    return ExtraPercentageAllResource.get_all()
def get_extra_percentage_all_id(extra_pa_id: UUID) -> Response:
    return ExtraPercentageAllResource.get_by_id(extra_pa_id)
def delete_extra_percentage_all( extra_pa_id: UUID) -> Response:
    return ExtraPercentageAllResource.delete_extra_percentage_all(extra_pa_id)
def update_extra_percentage_all( extra_pa_id: UUID) -> Response:
    return ExtraPercentageAllResource.update_extra_percentage_all(extra_pa_id)


#=============== app =========================
app, flask_app = create_app()
