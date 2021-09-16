# converters/promotion.py
from dbo_models.promotion import PromotionDBO
from dto_models.promotion import PromotionDTO

def promotion_dto_to_dbo(dto: PromotionDTO) -> PromotionDBO:
    print(f"\n IN --> promotion_dto_to_dbo ENDDAY{dto.end_date}\n")
    dbo = PromotionDBO(dto)
    dbo.created_time = dto.created_time  # auto generate
    return dbo

def promotion_dbo_to_dto(dbo: PromotionDBO) -> PromotionDTO:
    dto = PromotionDTO(
        promotiontype_id=dbo.promotiontype_id,
        description=dbo.description,
        is_active=dbo.is_active,
        image_url=dbo.image_url,
        promo_code=dbo.promo_code,
        id = dbo.id,
        start_date=dbo.start_date,
        end_date=dbo.end_date
    )
    dto.created_time = dbo.created_time
    return dto

