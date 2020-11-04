from ma import ma
from models.user import UserModel

class UserSchema(ma.MoedlSchema):
    class Meta:
        model=UserModel
        load_only = ("password",)
        dump_only=("id",)