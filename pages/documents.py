from django_elasticsearch_dsl import DocType, Index
from .models import Page

pages = Index('pages')

@pages.doc_type
class PageDocument(DocType):

    def full_title(self):
        return '%s:%s' % (self.namespace, self.title)

    class Meta:
        model = Page # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
            'namespace',
            'raw_content'
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000
