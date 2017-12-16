from .worker import *

import javalang
import javalang.tree

import esprima

import ast, asttokens

class JavaExtractor(object):

    def extract(self, source):
        self.source = source
        tree = javalang.parse.parse(source)

        return {
            'imports': self._extract_imports(tree),
            'package': self._extract_package(tree),
            'fragments': self._extract_fragments(tree)
        }

    def _extract_imports(self, tree):
        return [i.path for i in tree.imports]

    def _extract_package(self, tree):
        return tree.package.name

    def _extract_fragments(self, tree):
        fragments = []
        for t in tree.types:
            fragments.append(self._extract_fragment(t))

        return fragments

    def _extract_fragment(self, node):
        end = node.position.end
        if end is None:
            end = (len(self.source.split('\n')), 0)

        base = {
            'start': node.position.start[0],
            'end': end[0]
        }
        if isinstance(node, javalang.tree.ClassDeclaration):
            return {
                **base,
                'classifier': 'class',
                'name': node.name,
                'annotations': self._extract_annotations(node),
                'fragments': [self._extract_fragment(i) for i in node.body]
            }
        elif isinstance(node, javalang.tree.FieldDeclaration):
            names = [n.name for n in node.declarators]
            return {
                **base,
                'classifier': 'field',
                'names': names,
                'type': node.type.name
            }
        elif isinstance(node, javalang.tree.MethodDeclaration):
            params = [{
                **base,
                'name': param.name,
                'type': param.type.name,
                'annotations': param.annotations,
                'modifiers': list(param.modifiers)
            } for param in node.parameters]
            return {
                **base,
                'name': node.name,
                'classifier': 'method',
                'params': params,
                'annotations': [],
                'modifiers': list(node.modifiers)
            }
        elif isinstance(node, javalang.tree.ConstructorDeclaration):
            params = [{
                **base,
                'name': param.name,
                'type': param.type.name,
                'annotations': param.annotations,
                'modifiers': list(param.modifiers)
            } for param in node.parameters]

            return {
                **base,
                'classifier': 'constructor',
                'params': params,
                'annotations': [],
                'modifiers': list(node.modifiers)
            }
        else:
            print(node)
            raise

    def _extract_annotations(self, tree):
        return [annotation.name for annotation in tree.annotations]

class JavaScriptExtractor(object):

    def __init__(self):
        pass

    def extract(self, source):
        tree = esprima.parse(source, loc=True)

        fragments = [self._extract_fragment(node) for node in tree.body]

        return fragments

    def _extract_fragment(self, node):
        if node.type == 'FunctionDeclaration':
            params = [param.name for param in node.params]
            return {
                'classifier': 'function',
                'start': node.loc.start.line,
                'end': node.loc.end.line,
                'name': node.id.name,
                'params': params
            }
        elif node.type == 'VariableDeclaration':
            names = [decl.id.name for decl in node.declarations]
            return {
                'classifier': 'variable',
                'start': node.loc.start.line,
                'end': node.loc.end.line,
                'names': names
            }
        else:
            print(node.toDict())
            raise

class PythonExtractor(object):

    def extract(self, source):
        tree = asttokens.ASTTokens(source, parse=True)
        # print(tree.body)
        # print(dir(tree.body))

        print(dir(tree.tree))
        for node in tree.tree.body:
            self._extract_fragment(node)

    def _extract_fragment(self, node):
        if isinstance(node, ast.ClassDef):
            print(dir(node))
            return {
                'classifier': 'class',
                'name': node.name
            }
