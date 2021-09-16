# # converters/customer.py
# from dbo_models.customer import  CustomerDBO
# from dto_models.customer import  CustomerDTO
# from sqlalchemy.dialects.postgresql import UUID
#
# def customer_dto_to_dbo(dto: CustomerDTO) -> CustomerDBO:
#     dbo = CustomerDBO(dto)
#     dbo.created_time = dto.created_time
#     return dbo
#
# def customer_dbo_to_dto(dbo: CustomerDBO) -> CustomerDTO:
#     if dbo:
#         dto = CustomerDTO(
#             first_name=dbo.first_name,
#             last_name=dbo.last_name,
#             phone_number=dbo.phone_number,
#             email=dbo.email,
#             street=dbo.street,
#             city=dbo.city,
#             state=dbo.state,
#             zipcode=dbo.zipcode,
#             reward_point=dbo.reward_point,
#             id=dbo.id
#
#         )
#         dto.created_time = dbo.created_time
#         return dto
#     return None