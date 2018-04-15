from django.db import models, DatabaseError, transaction
from django.contrib.auth.base_user import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, db_column='github_name', null=True)
    github_avatar = models.CharField(max_length=100, null=True)
    github_token = models.CharField(max_length=100, null=True)
    github_uid = models.CharField(max_length=100, null=True)
    last_login = models.DateTimeField(null=True)
    password = models.CharField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    developer = models.BooleanField(default=False)
    last_message_id = models.CharField(max_length=100, null=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'
