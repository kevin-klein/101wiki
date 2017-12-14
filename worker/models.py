from .worker import *

import javalang

class PrettyPrinter(object):

    def emit_CompilationUnit(self, node):
        fragments = []
        for t in node.types:
            fragments.append(self.render_node(t))

        return fragments

    def emit_Import(self, node):
        print(node.__dict__)

    def emit_Documented(self, node):
        pass

    def emit_Declaration(self, node):
        pass

    def emit_TypeDeclaration(self, node):
        pass

    def emit_PackageDeclaration(self, node):
        print(node.__dict__)

    def emit_ClassDeclaration(self, node):
        body = [self.render_node(n) for n in node.body]
        return {
            'classifier': 'class',
            'body': body
        }

    def emit_EnumDeclaration(self, node):
        pass

    def emit_InterfaceDeclaration(self, node):
        pass

    def emit_AnnotationDeclaration(self, node):
        pass

    def emit_Type(self, node):
        pass

    def emit_BasicType(self, node):
        dimensions = self.render_dimensions(node)
        return "%s%s" % (node.name, dimensions)

    def emit_ReferenceType(self, node):
        dimensions = self.render_dimensions(node)
        return "%s%s" % (node.name, dimensions)

    def render_dimensions(self, node):
        return '[]' * len(node.dimensions)

    def emit_TypeArgument(self, node):
        pass

    def emit_TypeParameter(self, node):
        pass

    def emit_Annotation(self, node):
        pass

    def emit_ElementValuePair(self, node):
        pass

    def emit_ElementArrayValue(self, node):
        pass

    def emit_Member(self, node):
        pass

    def emit_MethodDeclaration(self, node):
        modifiers = ' '.join(node.modifiers).strip()

        name = node.name
        return_type = self.render_node(node.return_type)

        params = ', '.join([self.render_node(n) for n in node.parameters])

        print(node.body)
        body = '\n'.join([self.render_node(n) for n in node.body])

        return {
            'classifier': 'method',
            'name': name,
            'code': ('%s %s %s(%s) { %s }' % (modifiers, return_type, name, params, body)).strip()
        }

    def emit_NoneType(self, node):
        return 'void'

    def emit_FieldDeclaration(self, node):
        pass

    def emit_ConstructorDeclaration(self, node):
        pass

    def emit_ConstantDeclaration(self, node):
        pass

    def emit_ArrayInitializer(self, node):
        pass

    def emit_VariableDeclaration(self, node):
        pass

    def emit_LocalVariableDeclaration(self, node):
        # print(node.__dict__)
        # print(node.declarators)
        return "%s %s" % (self.render_node(node.type), ', '.join([self.render_node(n) for n in node.declarators]))

    def emit_VariableDeclarator(self, node):
        print(node.__dict__)
        return "%s = %s" % (node.name)

    def emit_FormalParameter(self, node):
        return "%s %s" % (self.render_node(node.type), node.name)

    def emit_InferredFormalParameter(self, node):
        pass

    def emit_Statement(self, node):
        pass

    def emit_IfStatement(self, node):
        pass

    def emit_WhileStatement(self, node):
        pass

    def emit_DoStatement(self, node):
        pass

    def emit_ForStatement(self, node):
        pass

    def emit_AssertStatement(self, node):
        pass

    def emit_BreakStatement(self, node):
        pass

    def emit_ContinueStatement(self, node):
        pass

    def emit_ReturnStatement(self, node):
        return 'return %s;' % self.render_node(node.expression)

    def emit_ThrowStatement(self, node):
        pass

    def emit_SynchronizedStatement(self, node):
        pass

    def emit_TryStatement(self, node):
        pass

    def emit_SwitchStatement(self, node):
        pass

    def emit_BlockStatement(self, node):
        pass

    def emit_StatementExpression(self, node):
        return "%s;" % self.render_node(node.expression)

    def emit_TryResource(self, node):
        pass

    def emit_CatchClause(self, node):
        pass

    def emit_CatchClauseParameter(self, node):
        pass

    def emit_SwitchStatementCase(self, node):
        pass

    def emit_ForControl(self, node):
        pass

    def emit_EnhancedForControl(self, node):
        pass

    def emit_Expression(self, node):
        pass

    def emit_Assignment(self, node):
        pass

    def emit_TernaryExpression(self, node):
        pass

    def emit_BinaryOperation(self, node):
        pass

    def emit_Cast(self, node):
        pass

    def emit_MethodReference(self, node):
        pass

    def emit_LambdaExpression(self, node):
        pass

    def emit_Primary(self, node):
        pass

    def emit_Literal(self, node):
        return node.value

    def emit_This(self, node):
        pass

    def emit_MemberReference(self, node):
        return node.member

    def emit_Invocation(self, node):
        pass

    def emit_ExplicitConstructorInvocation(self, node):
        pass

    def emit_SuperConstructorInvocation(self, node):
        pass

    def emit_MethodInvocation(self, node):
        args = ' '.join([self.render_node(n) for n in node.arguments]).strip()
        return '%s.%s(%s)' % (node.qualifier, node.member, args)

    def emit_SuperMethodInvocation(self, node):
        pass

    def emit_SuperMemberReference(self, node):
        pass

    def emit_ArraySelector(self, node):
        pass

    def emit_ClassReference(self, node):
        pass

    def emit_VoidClassReference(self, node):
        pass

    def emit_Creator(self, node):
        pass

    def emit_ArrayCreator(self, node):
        pass

    def emit_ClassCreator(self, node):
        pass

    def emit_InnerClassCreator(self, node):
        pass

    def emit_EnumBody(self, node):
        pass

    def emit_EnumConstantDeclaration(self, node):
        pass

    def emit_AnnotationMethod(self, node):
        pass

    def render_node(self, node):
        # print(node.__class__.__name__)
        emit = getattr(self, 'emit_%s' % node.__class__.__name__, self.default_emit)
        return emit(node)

    def default_emit(self, node):
        """Fallback function for emitting unknown nodes."""
        raise NotImplementedError("Node '%s' unknown" % node.__class__.__name__)

class JavaExtractor(object):

    def extract(self, source):
        return javalang.parse.parse(source)

    def to_string(self, node):
        printer = PrettyPrinter()
        return printer.render_node(node)
