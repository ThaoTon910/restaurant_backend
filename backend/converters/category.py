
from dbo_models.category import CategoryDBO
from dto_models.category import CategoryDTO
from converters.menu_item import menu_item_dbo_to_dto

def category_dto_to_dbo(dto: CategoryDTO) -> CategoryDBO:
    dbo = CategoryDBO(
        id = dto.id,
        name = dto.name,
        index = dto.index
    )
    # dbo.updated_time = dto.updated_time
    # dbo.created_time = dto.created_time
    return dbo

def category_dbo_to_dto(dbo: CategoryDBO) -> CategoryDTO:
    dto = CategoryDTO(
        name = dbo.name,
        index = dbo.index
    )
    dto.updated_time = dbo.updated_time
    dto.created_time = dbo.created_time
    if dbo.menu_items:
        dto.menu_items = [menu_item_dbo_to_dto(m_dbo) for m_dbo in dbo.menu_items]
    else:
        dto.menu_items = []
    dto.id = dbo.id
    return dto

