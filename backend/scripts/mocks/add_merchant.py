import datetime

import requests
import os
import codecs
import json

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_URL = 'http://localhost:8080/v0'

def create_merchant(merchant_name: str):
    about_file = os.path.join(CURRENT_DIR, merchant_name, 'about.json')
    with open(about_file, 'r') as fp:
        about = json.load(fp)
        r = requests.post(BASE_URL + '/merchant', json=about)
        if (r.status_code == 500):
            print(r.text)

def create_categories(merchant_name: str):
    categories_file = os.path.join(CURRENT_DIR, merchant_name, 'categories.json')
    with open(categories_file, 'r') as fp:
        categories = json.load(fp)
        for index, category in enumerate(categories):
            category['index'] = index
            r = requests.post(BASE_URL + '/category', json=category)
            if(r.status_code == 500):
                print(r.text)

def create_addon_group(merchant_name: str):
    addOnGroups_file = os.path.join(CURRENT_DIR, merchant_name, 'addOnGroups.json')
    with open(addOnGroups_file, 'r') as fp:
        addOnGroups = json.load(fp)
        for index, group in enumerate(addOnGroups):
            r = requests.post(BASE_URL + '/addon-group', json=group)
            if(r.status_code == 500):
                print(r.text)

def create_menu_item(merchant_name: str):
    recipe_file = os.path.join(CURRENT_DIR, merchant_name, 'recipes.json')
    with open(recipe_file, 'r') as fp:
        category_group = json.load(fp)

        actual_category_groups = requests.get(BASE_URL + '/category').json() #get real category in database
        mapping = {}
        try:
            for item in actual_category_groups:
                mapping[item['name']] = item['id']
        except Exception as e:
            print(e)
            x = 1
        for category_name, recipes in category_group.items():
            for recipe in recipes:
                recipe['categoryId'] = mapping[category_name]
                # print(json.dumps(recipe, indent=2))
                r = requests.post(BASE_URL + '/menu-item', json=recipe)
                if(r.status_code == 500):
                    print(r.text)

def create_addon(merchant_name: str):
    addon_file = os.path.join(CURRENT_DIR, merchant_name, 'addsOn.json')
    actual_addon_groups = requests.get(BASE_URL + '/addon-group').json()  # get real category in database
    mapping = {}
    for item in actual_addon_groups:
        addon_names = list(map(lambda a: a['name'], item['addons']))
        mapping[item['name']] = {'id': item['id'], 'addon_names': addon_names}
        #get addongroupID and groupname

    with open(addon_file, 'r') as fp:
        addOns = json.load(fp)
        for key, values in addOns.items():
            for addon in values:
                addon['addonGroupId'] = mapping[key]['id']
                if addon['name'] not in mapping[key]['addon_names']:
                    r = requests.post(BASE_URL + '/addon', json=addon)
                    if(r.status_code == 500):
                        print(r.text)

def create_menu_item_to_addon_group(merchant_name: str):
    recipeToAddOnGroup_file = os.path.join(CURRENT_DIR, merchant_name, 'recipeToAddOnGroup.json') # open
    actual_recipe = requests.get(BASE_URL + '/menu-item').json() #open recipe file to get recipe_id
    actual_addOnGroup = requests.get(BASE_URL + '/addon-group').json()  # get add on group id
    mapping_recipe= {}
    mapping_addOnGroup= {}
    for recipe in actual_recipe:
        addon_group_ids = recipe['addonGroupIds']
        mapping_recipe[recipe['name']] = {'id': recipe['id'], 'addon_group_ids': addon_group_ids}

    for addOnGroup in actual_addOnGroup:
        mapping_addOnGroup[addOnGroup['name']] = addOnGroup['id']

    with open(recipeToAddOnGroup_file, 'r') as fp:
        recipeToAddOnGroup = json.load(fp)
        for recipe_name, addon_groups in recipeToAddOnGroup.items():
            recipe_id = mapping_recipe[recipe_name]['id']
            addon_group_ids = mapping_recipe[recipe_name]['addon_group_ids']

            for group_name in addon_groups:
                group_id = mapping_addOnGroup[group_name]

                if group_id not in addon_group_ids:
                    data = {
                        'menuItemId': recipe_id,
                        'addonGroupId': group_id
                    }

                    r = requests.post(BASE_URL + '/menu-item-to-addon-group', json=data)
                    print(r.text)
                    if(r.status_code == 500):
                        print(r.text)

def add_orders(merchant_name):
    r = requests.get(BASE_URL + '/merchant')
    merchant_id = r.json()['id']
    print(merchant_id)

    r = requests.get(BASE_URL + '/menu')
    menu = r.json()
    categories = menu['categories']
    addon_groups = menu['addonGroups']

    pho_category = categories[1]
    first_pho = pho_category['menuItems'][0]
    first_addongroup_id = first_pho['addonGroupIds'][0]
    # Get group detail data from group id where id is stored in first_addongroup_id and group list in addon_groups
    addon_group = None
    for group in addon_groups:
        if group['id'] == first_addongroup_id:
            addon_group = group
            break
    first_addon_id = addon_group['addons'][0]['id']

    order_payload = {
          "customer": {
            "email": "123@example.com",
            "firstName": "Test",
            "lastName": "User",
            "phone": "(408) 123 4567"
          },
          "delivery": {
            "deliveryFee": 0,
            "info": {
              "deliveryType": "deliveryType_test",
              "merchantId": merchant_id,
              "time": str(datetime.datetime.now())
            }
          },
          "items": [
            {
              "addOns": [
                first_addon_id # uuid addon
              ],
              "menuItemId": first_pho["id"],
              "quantity": 1,
              "specialInstruction": "special"
            }
          ],
          "paymentToken": "string",
          "promoCode": "string",
          "taxMultiplier": 0,
          "tipMultiplier": 0
        }
    r = requests.post(BASE_URL + '/order', json=order_payload)
    print("order ", r.json())
    assert r.status_code == 200


def create_merchant_detail(merchant_name):
    create_merchant(merchant_name)
    create_categories(merchant_name)
    create_addon_group(merchant_name)
    create_menu_item(merchant_name)
    create_addon(merchant_name)
    create_menu_item_to_addon_group(merchant_name)
    add_orders(merchant_name)

if __name__ == "__main__":
    create_merchant_detail("pho21")
