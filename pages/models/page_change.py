from django.db import models

from .page import Page
from .user import User

class PageChange(models.Model):
    page = models.ForeignKey(Page)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    namespace = models.CharField(max_length=100)
    raw_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'page_changes'
