from dbo_models.menu_item_to_addon_group import MenuItemToAddonGroupDBO
from dto_models.menu_item_to_addon_group import MenuItemToAddonGroupDTO

def menu_item_to_addon_group_dto_to_dbo(dto: MenuItemToAddonGroupDTO) -> MenuItemToAddonGroupDBO:
    dbo = MenuItemToAddonGroupDBO(
        menu_item_id=dto.menu_item_id,
        addon_group_id=dto.addon_group_id
    )
    return dbo

def menu_item_to_addon_group_dbo_to_dto(dbo: MenuItemToAddonGroupDBO) -> MenuItemToAddonGroupDTO:
    dto = MenuItemToAddonGroupDTO(
        menu_item_id=dbo.menu_item_id,
        addon_group_id=dbo.addon_group_id
    )

    return dto
