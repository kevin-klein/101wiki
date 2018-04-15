from creole.emitter import creol2html_emitter

from .metadatacollector import MetadataCollector

class SchemaCollector(MetadataCollector):

    def __init__(self, document):
        MetadataCollector.__init__(self, document)

        self.sections = []

    def header_emit(self, node):
        self.sections.append(node.content)
        return MetadataCollector.header_emit(self, node)
