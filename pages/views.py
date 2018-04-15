from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
import elasticsearch.exceptions

from .models import Page, PageChange, User
from .forms import SearchForm, PageForm

def local_login(request):
    user = authenticate(username=request.GET['username'])

    login(request, user, backend='pages.auth_backend.PasswordlessAuthBackend')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def search(request):
    form = SearchForm(request.POST)

    if form.is_valid():
        s = PageDocument.search()
        s = s.query('multi_match', type='phrase_prefix', query=form.cleaned_data['search'], fields=['title^20', 'namespace^5', 'raw_content'])
        s = s.sort('_score')

        count = s.count()

        return render(request, 'wiki/search.html', {
            'search_form': form,
            'results': s[0:100],
            'count': count
        })

def page(request, name):
    search_form = SearchForm()

    pieces = name.split(':')
    if len(pieces) == 2:
        namespace, title = pieces
    else:
        namespace = 'Concept'
        title = pieces[0]
    page = Page.objects.get(namespace=namespace, title=title)
    validation = page.validate()

    changes = page.pagechange_set.all

    metadata, resources = page.metadata()

    # s = PageDocument.search()
    #
    # like = [{
    #     "_index" : "pages",
    #     "_id" : page.id
    # }]
    #
    # s = s.query('more_like_this', like=like, fields=['raw_content'], min_term_freq=1,max_query_terms=1)
    #
    # try:
    #     repo_link = page.repolink
    # except ObjectDoesNotExist:
    #     repo_link = None
    #
    # try:
    #     s = list(s)
    # except elasticsearch.exceptions.ElasticsearchException as e:
    #     s = []
    s = []
    repo_link = None

    form = PageForm(instance=page)

    if request.method == 'POST':
        f = PageForm(request.POST, instance=page)
        if f.is_valid():
            f.save()
        else:
            raise

    context = {
        'validation': validation,
        'user': request.user,
        'similarities': s,
        'users': User.objects.all(),
        'search_form': search_form,
        'page': page,
        'content': page.render_to_html(),
        'changes': changes,
        'metadata': metadata,
        'resources': resources,
        'repo_link': repo_link,
        'form': form
    }
    return render(request, 'wiki/page.html', context)
