from creole.emitter import creol2html_emitter

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
