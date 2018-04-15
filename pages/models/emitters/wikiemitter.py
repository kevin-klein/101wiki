from creole.emitter import creol2html_emitter

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
