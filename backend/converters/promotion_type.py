from dbo_models.promotion_type import  PromotionTypeDBO
from dto_models.promotion_type import  PromotionTypeDTO
from sqlalchemy.dialects.postgresql import UUID


def promotion_type_dto_to_dbo(dto: PromotionTypeDTO) -> PromotionTypeDBO:
    dbo = PromotionTypeDBO(dto)
    dbo.created_time = dto.created_time
    return dbo


def promotion_type_dbo_to_dto(dbo: PromotionTypeDBO) -> PromotionTypeDTO:
    if dbo:
        dto = PromotionTypeDTO(
            promotion_type=dbo.promotion_type,
            description=dbo.description,
            id=dbo.id
        )
        dto.created_time = dbo.created_time
        return dto
    empty_dto = PromotionTypeDTO()
    return empty_dto

