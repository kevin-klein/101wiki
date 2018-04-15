from django.db import models

from .page import Page

class RepoLink(models.Model):
    repo = models.CharField(max_length=100)
    folder = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    page = models.OneToOneField(Page)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def url(self):
        return "https://github.com/%s/%s" % (self.user, self.repo)

    class Meta:
        db_table = 'repo_links'
