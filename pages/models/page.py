from django.db import models, DatabaseError, transaction

from creole import creole2html
from creole.parser.creol2html_parser import CreoleParser

from .emitters import *

class Page(models.Model):
    title = models.CharField(max_length=100)
    raw_content = models.TextField()
    namespace = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def links(self):
        document = CreoleParser(self.raw_content.replace('<', '<<').replace('>', '>>')).parse()
        emitter = LinkEmitter(document)
        emitter.emit()

        return emitter.links


    def validate(self):
        SCHEMA_PREDICATES = [
            'hasMandatory',
            'hasOptional'
        ]

        namespace_page = Page.objects.get(namespace='Namespace', title=self.namespace)

        errors = []
        warnings = []

        schema_triples = Triple.objects.filter(page__namespace='Namespace', page__title=self.namespace, predicate__in=SCHEMA_PREDICATES)

        document = CreoleParser(self.raw_content.replace('<', '<<').replace('>', '>>')).parse()
        emitter = SchemaCollector(document)
        emitter.emit()

        metadata = emitter.metadata
        sections = emitter.sections

        properties = [item['predicate'] for item in metadata]

        # validate sections and properties
        for triple in schema_triples:
            if triple.predicate == 'hasOptional':
                namespace, title = triple.object.split(':')
                if namespace == 'Section':
                    if title not in sections:
                        warnings.append({
                            'type': 'missing_optional_section',
                            'section': triple.object
                        })
                elif namespace == 'Property':
                    if title not in properties:
                        warnings.append({
                            'type': 'missing_optional_property',
                            'property': triple.object
                        })
            elif triple.predicate == 'hasMandatory':
                namespace, title = triple.object.split(':')
                if namespace == 'Section':
                    if title not in sections:
                        errors.append({
                            'type': 'missing_mandatory_section',
                            'section': triple.object
                        })
                elif namespace == 'Property':
                    if title not in properties:
                        errors.append({
                            'type': 'missing_mandatory_property',
                            'property': triple.object
                        })

        allowed_sections = [triple.object.split(':')[1] for triple in schema_triples if 'Section:' in triple.object]

        for section in sections:
            if section not in allowed_sections:
                errors.append({
                    'type': 'invalid_section',
                    'section': section
                })
                # raise

        return {
            'errors': errors,
            'warnings': warnings
        }

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

    def only_metadata(self):
        metadata, _ = self.metadata()
        return metadata


    def only_resources(self):
        _, resources = self.metadata()
        return resources

    class Meta:
        db_table = 'pages'

class Triple(models.Model):
    page = models.ForeignKey(Page)
    predicate = models.CharField(max_length=100)
    object = models.CharField(max_length=100)

    def __str__(self):
        return str(self.__dict__)

    class Meta:
        db_table = 'triples'
