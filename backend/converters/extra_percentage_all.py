# converts/extra_percentage_all.py
from dbo_models.extra_percentage_all import ExtraPercentageAllDBO
from dto_models.extra_percentage_all import ExtraPercentageAllDTO

def extra_percentage_all_dto_to_dbo(dto: ExtraPercentageAllDTO) -> ExtraPercentageAllDBO:
    dbo = ExtraPercentageAllDBO(dto)
    dbo.updated_time = dto.updated_time  # auto generate
    return dbo

def extra_percentage_all_dbo_to_dto(dbo: ExtraPercentageAllDBO) -> ExtraPercentageAllDTO:
    dto = ExtraPercentageAllDTO(
        promotiontype_id=dbo.promotiontype_id,
        percent_off=dbo.percent_off,
        id=dbo.id
    )
    dto.updated_time = dbo.updated_time
    return dto

