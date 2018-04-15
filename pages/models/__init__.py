from .page import Page, Triple
from .user import User
from .page_user import PageUser
from .repo_link import RepoLink
from .user import User
from .validations import *
from .page_change import PageChange

from django.db import models, DatabaseError, transaction

from django.contrib.auth.base_user import AbstractBaseUser

@transaction.atomic
def import_data(data):
    for page in data['pages']:
        Page(**page).save()

    for user in data['users']:
        user['username'] = user['github_name']
        del user['github_name']
        User(**user).save()

    for triple in data['triples']:
        if triple['page_id']:
            Triple(**triple).save()

    for change in data['page_changes']:
        if change['page_id']:
            PageChange(**change).save()

    for link in data['repo_links']:
        if link['page_id']:
            RepoLink(**link).save()

    for page_user in data['page_users']:
        PageUser(**page_user).save()
