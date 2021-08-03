from dbo_models.addon import AddonDBO
from dto_models.addon import AddonDTO

def addon_dto_to_dbo(dto: AddonDTO) -> AddonDBO:
    dbo = AddonDBO(
        addon_group_id = dto.addon_group_id,
        name = dto.name,
        price = dto.price,
        description = dto.description,
        is_taxable = dto.is_taxable,
        id = dto.id
    )
    # dbo.updated_time = dto.updated_time
    # dbo.created_time = dto.created_time
    return dbo

def addon_dbo_to_dto(dbo: AddonDBO) -> AddonDTO:
    dto = AddonDTO(
        addon_group_id = dbo.addon_group_id,
        name = dbo.name,
        price = dbo.price,
        description = dbo.description,
        is_taxable = dbo.is_taxable,
    )
    dto.id = dbo.id
    dto.updated_time = dbo.updated_time
    dto.created_time = dbo.created_time
    return dto
