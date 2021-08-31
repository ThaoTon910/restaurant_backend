from dbo_models.merchant import MerchantDBO
from dto_models.merchant import MerchantDTO
from schemas.hour import HourSchema
from dto_models.hour import HourDTO
def merchant_dto_to_dbo(dto: MerchantDTO) -> MerchantDBO:
    # hours = []
    # for hour in dto.hours:
    #     hours.append(hour.asdict())
    schema = HourSchema(many=True)
    hours = schema.dump(dto.hours)

    dbo = MerchantDBO(
        id=dto.id,
        name=dto.name,
        phone=dto.phone,
        address=dto.address,
        hours=hours
    )
    # dbo.updated_time = dto.updated_time
    # dbo.created_time = dto.created_time
    return dbo

def merchant_dbo_to_dto(dbo: MerchantDBO) -> MerchantDTO:
    schema = HourSchema(many=True)
    hours = []
    for hour_dict in schema.load(dbo.hours):
        hours.append(HourDTO(**hour_dict))

    dto = MerchantDTO(
        name=dbo.name,
        phone=dbo.phone,
        address=dbo.address,
        hours=hours
    )
    dto.id = dbo.id
    dto.updated_time = dbo.updated_time
    dto.created_time = dbo.created_time
    return dto

