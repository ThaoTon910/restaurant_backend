
from dbo_models.addon_group import AddonGroupDBO
from dto_models.addon_group import AddonGroupDTO
def addon_dto_to_dbo(dto:AddonGroupDTO) -> AddonGroupDBO:
    dbo = AddonGroupDBO(
        name=dto.name,
        max_quantity=dto.max_quantity,
        min_quantity=dto.min_quantity,
        id = dto.id
    )
    dbo.updated_time = dto.updated_time
    dbo.created_time = dto.created_time
    return dbo

def addon_dbo_to_dto(dbo: AddonGroupDBO) -> AddonGroupDTO:
    dto = AddonGroupDTO(
        name=dbo.name,
        max_quantity=dbo.max_quantity,
        min_quantity=dbo.min_quantity
    )# Only take DTO attribute that has init=True
    dto.updated_time = dbo.updated_time
    dto.created_time = dbo.created_time
    dto.id = dbo.id
    return dto
