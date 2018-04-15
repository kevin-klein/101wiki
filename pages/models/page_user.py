from django.db import models

from .page import Page
from .user import User

class PageUser(models.Model):
    page = models.ForeignKey(Page)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'page_users'
