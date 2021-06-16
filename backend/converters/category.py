
from dbo_models.category import Category as CategoryDBO
from dto_models.category import Category as CategoryDTO

def category_dbo_to_dto(dbo: CategoryDBO) -> CategoryDTO:
    dto = CategoryDTO(name=dbo.name, index=dbo.index)
    dto.updated_time = dbo.updated_time
    dto.created_time = dbo.created_time
    dto.id = dbo.id
    return dto

def category_dto_to_dbo(dto: CategoryDTO) -> CategoryDBO:
    dbo = CategoryDBO(id=dto.id, name=dto.name, index=dto.index)
    dbo.updated_time = dto.updated_time
    dbo.created_time = dto.created_time
    return dbo