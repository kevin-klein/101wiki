from django.db import models, DatabaseError, transaction

from creole import creole2html
from creole.emitter import creol2html_emitter
from creole.parser.creol2html_parser import CreoleParser

from pygments import highlight, lexers
from pygments.formatters import HtmlFormatter

def get_pygments_formatter():
    return HtmlFormatter(linenos = True, encoding='utf-8',
                         style='colorful', outencoding='utf-8',
                         noclasses=True)


def get_pygments_lexer(source_type, code):
    try:
        return lexers.get_lexer_by_name(source_type)
    except:
        return lexers.guess_lexer(code)

def syntaxhighlight(lang, text):
    lexer = get_pygments_lexer(lang, text)
    formatter = get_pygments_formatter()
    highlighted = highlight(text, lexer, formatter)

    return highlighted.decode('utf-8')

class WikiEmitter(creol2html_emitter.HtmlEmitter):

    def __init__(self, document):
        macros = {
            'syntaxhighlight': syntaxhighlight
        }
        self._in_metadata = False

        creol2html_emitter.HtmlEmitter.__init__(self, document, macros=macros)

    def header_emit(self, node):
        if node.content == 'Metadata':
            self._in_metadata = True
            return ''
        else:
            url = '/Section:%s' % self.html_escape(node.content)
            header = '<a href="%s"><h%d>%s</h%d></a>' % (
                url, node.level, self.html_escape(node.content), node.level
            )
            if self.toc is not None:
                self.toc.add_headline(node.level, node.content)
                # add link attribute for toc navigation
                header = '<a name="%s">%s</a>' % (
                    self.html_escape(node.content), header
                )

            header += "\n"
            return header

    def bullet_list_emit(self, node):
        if self._in_metadata:
            return ''
        else:
            return creol2html_emitter.HtmlEmitter.bullet_list_emit(self, node)

    def link_emit(self, node):
        if self._in_metadata:
            return ''
        target = node.content
        if node.children:
            inside = self.emit_children(node)
        else:
            inside = self.html_escape(target)

        if target[0] != '/':
            target = '/' + target

        return '<a href="%s">%s</a>' % (
            self.attr_escape(target), inside)

class MetadataCollector(creol2html_emitter.HtmlEmitter):

    def __init__(self, document):
        creol2html_emitter.HtmlEmitter.__init__(self, document)

        self._in_metadata = False
        self.metadata = []

    def header_emit(self, node):
        if node.content == 'Metadata':
            self._in_metadata = True
            return ''
        else:
            return creol2html_emitter.HtmlEmitter.header_emit(self, node)

    def link_emit(self, node):
        if self._in_metadata:
            predicate, obj = node.content.split('::')
            self.metadata.append({ 'predicate': predicate, 'object': obj })
            return ''
        else:
            return creol2html_emitter.HtmlEmitter.link_emit(self, node)

class User(models.Model):
    email = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    github_name = models.CharField(max_length=100)
    github_avatar = models.CharField(max_length=100)
    github_token = models.CharField(max_length=100)
    github_uid = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    developer = models.BooleanField(default=False)
    last_message_id = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'users'

class Page(models.Model):
    title = models.CharField(max_length=100)
    raw_content = models.TextField()
    namespace = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_title(self):
        return self.namespace + ":" + self.title

    def render_to_html(self):
        document = CreoleParser(self.raw_content.replace('<', '<<').replace('>', '>>')).parse()
        return WikiEmitter(document).emit()

    def metadata(self):
        document = CreoleParser(self.raw_content.replace('<', '<<').replace('>', '>>')).parse()
        emitter = MetadataCollector(document)
        emitter.emit()

        metadata = []
        resources = []
        for item in emitter.metadata:
            if item['object'].startswith('http'):
                resources.append(item)
            else:
                metadata.append(item)

        return [metadata, resources]

    class Meta:
        db_table = 'pages'

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

class Triple(models.Model):
    page = models.ForeignKey(Page)
    predicate = models.CharField(max_length=100)
    object = models.CharField(max_length=100)

    class Meta:
        db_table = 'triples'

class PageUser(models.Model):
    page = models.ForeignKey(Page)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'page_users'

@transaction.atomic
def import_data(data):
    for page in data['pages']:
        Page(**page).save()

    for user in data['users']:
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
