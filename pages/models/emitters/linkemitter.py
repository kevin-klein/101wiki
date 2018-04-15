from creole.emitter import creol2html_emitter

from .wikiemitter import WikiEmitter

class LinkEmitter(WikiEmitter):

    def __init__(self, *args, **kwargs):
        WikiEmitter.__init__(self, *args, **kwargs)

        self.links = []

    def link_emit(self, node):
        self.links.append(node.content)

        return WikiEmitter.link_emit(self, node)
