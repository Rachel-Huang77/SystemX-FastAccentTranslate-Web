import uuid
from tortoise import fields, models

class User(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    username = fields.CharField(max_length=256, unique=True, index=True)
    email = fields.CharField(max_length=256, null=True, unique=True)
    password_hash = fields.CharField(max_length=255)
    role = fields.CharField(max_length=16, default="user")
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    last_login = fields.DatetimeField(null=True)

    class Meta:
        table = "users"
