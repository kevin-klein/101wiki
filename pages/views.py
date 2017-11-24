from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Page, PageChange

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def page(request, name):
    pieces = name.split(':')
    if len(pieces) == 2:
        namespace, title = pieces
    else:
        namespace = 'Concept'
        title = pieces[0]
    page = Page.objects.get(namespace=namespace, title=title)

    changes = page.pagechange_set.all

    metadata, resources = page.metadata()

    try:
        repo_link = page.repolink
    except ObjectDoesNotExist:
        repo_link = None

    context = {
        'page': page,
        'content': page.render_to_html(),
        'changes': changes,
        'metadata': metadata,
        'resources': resources,
        'repo_link': repo_link
    }
    return render(request, 'wiki/page.html', context)
