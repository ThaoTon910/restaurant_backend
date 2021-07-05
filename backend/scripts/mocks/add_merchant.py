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
        for item in actual_category_groups:
            mapping[item['name']] = item['id']
        for category_name, recipes in category_group.items():
            for recipe in recipes:
                recipe['categoryId'] = mapping[category_name]
                # print(json.dumps(recipe, indent=2))
                r = requests.post(BASE_URL + '/menu-item', json=recipe)
                if(r.status_code == 500):
                    print(r.text)

def create_addOn(merchant_name: str):
    addOn_file = os.path.join(CURRENT_DIR, merchant_name, 'addsOn.json')
    actual_addon_groups = requests.get(BASE_URL + '/addOnGroup').json()  # get real category in database
    mapping = {}
    for item in actual_addon_groups:
        mapping[item['name']] = item['id']
        #get addongroupID and groupname

    with open(addOn_file, 'r') as fp:
        addOns = json.load(fp)
        for key, values in addOns.items():
            for addon in values:
                addon['addOnGroupId'] = mapping[key]
                r = requests.post(BASE_URL + '/addOn', json=addon)
                if(r.status_code == 500):
                    print(r.text)

def create_recipeToAddOnGroup(merchant_name: str):
    recipeToAddOnGroup_file = os.path.join(CURRENT_DIR, merchant_name, 'recipeToAddOnGroup.json') # open
    actual_recipe = requests.get(BASE_URL + '/recipe').json() #open recipe file to get recipe_id
    actual_addOnGroup = requests.get(BASE_URL + '/addOnGroup').json()  # get add on group id
    mapping_recipe= {}
    mapping_addOnGroup= {}
    for recipe in actual_recipe:
        mapping_recipe[recipe['name']] = recipe['id']

    for addOnGroup in actual_addOnGroup:
        mapping_addOnGroup[addOnGroup['name']] = addOnGroup['id']

    with open(recipeToAddOnGroup_file, 'r') as fp:
        recipeToAddOnGroup = json.load(fp)
        for recipe_name, addon_groups in recipeToAddOnGroup.items():
            recipe_id = mapping_recipe[recipe_name]
            for group_name in addon_groups:

                group_id = mapping_addOnGroup[group_name]
                data = {
                    'recipeId': recipe_id,
                    'addOnGroupId': group_id
                }

                r = requests.post(BASE_URL + '/recipeToAddOnGroup', json=data)
                print(r.text)
                if(r.status_code == 500):
                    print(r.text)

def create_merchant_detail(merchant_name):
    # create_merchant(merchant_name)
    create_categories(merchant_name)
    create_addon_group(merchant_name)
    create_menu_item(merchant_name)
    # create_addOn(merchant_name)
    # create_recipeToAddOnGroup(merchant_name)

if __name__ == "__main__":
    create_merchant_detail("pho21")
