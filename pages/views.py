from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
from django.db.models import Count
import elasticsearch.exceptions
import json

from .models import Page, PageChange, User, Triple
from .forms import SearchForm, PageForm

def local_login(request):
    user = authenticate(username=request.GET['username'])

    login(request, user, backend='pages.auth_backend.PasswordlessAuthBackend')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def index(request):

    def cloud_data(namespace):
        return {row['object']:row['object__count'] for row in Triple.objects.filter(object__startswith=namespace+':').values("object").annotate(Count('object')).order_by()[:30] }

    def popular_contributions():
        return {'Contribution:' + row['page__title']:row['page__title__count'] for row in Triple.objects.filter(page__namespace='Contribution').values("page__title").annotate(Count('page__title')).order_by('page__title')[:300] }

    technology_pages = Page.objects.filter(namespace='Technology')[:5]
    technologies = cloud_data('Technology')

    feature_pages = Page.objects.filter(namespace='Feature')[:5]
    features = cloud_data('Feature')

    contribution_pages = Page.objects.filter(namespace='Contribution')[:5]
    contributions = popular_contributions()

    language_pages = Page.objects.filter(namespace='Language')[:5]
    languages = cloud_data('Language')

    # @front_page = PageModule.front_page
    # @courses_page = PageModule.courses_page
    front_page = Page.objects.get(namespace='Internal', title='FrontPage')
    courses_page = Page.objects.get(namespace='Internal', title='Courses')

    return render(request, 'wiki/front_page.html', {
        'technologies': json.dumps(technologies),
        'technology_pages': technology_pages,
        'feature_pages': feature_pages,
        'features': features,
        'contributions': contributions,
        'contribution_pages': contribution_pages,
        'languages': languages,
        'language_pages': language_pages,
        'front_page_content': front_page.render_to_html(),
        'courses_content': courses_page.render_to_html()
    })


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
