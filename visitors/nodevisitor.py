from ast import AST, iter_fields


class NodeVisitor(object):
    def __init__(self):
        self._const_node_type_names = {
            bool: 'NameConstant',  # should be before int
            type(None): 'NameConstant',
            int: 'Num',
            float: 'Num',
            complex: 'Num',
            str: 'Str',
            bytes: 'Bytes',
            type(...): 'Ellipsis',
        }
    """
    A node visitor base class that walks the abstract syntax tree and calls a
    visitor function for every node found.  This function may return a value
    which is forwarded by the `visit` method.

    This class is meant to be subclassed, with the subclass adding visitor
    methods.

    Per default the visitor functions for the nodes are ``'visit_'`` +
    class name of the node.  So a `TryFinally` node visit function would
    be `visit_TryFinally`.  This behavior can be changed by overriding
    the `visit` method.  If no visitor function exists for a node
    (return value `None`) the `generic_visit` visitor is used instead.

    Don't use the `NodeVisitor` if you want to apply changes to nodes during
    traversing.  For this a special visitor exists (`NodeTransformer`) that
    allows modifications.
    """

    def visit(self, node, params):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, params)

    def generic_visit(self, node, params):
        """Called if no explicit visitor function exists for a node."""
        if node is not None:
            for field, value in iter_fields(node):
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, AST):
                            return self.visit(item, params)
                elif isinstance(value, AST):
                    return self.visit(value, params)

    def visit_constant(self, node, params):
        value = node.value
        type_name = self._const_node_type_names.get(type(value))
        if type_name is None:
            for cls, name in self._const_node_type_names.items():
                if isinstance(value, cls):
                    type_name = name
                    break
        if type_name is not None:
            method = 'visit_' + type_name
            try:
                visitor = getattr(self, method)
            except AttributeError:
                pass
            else:
                import warnings
                warnings.warn(f"{method} is deprecated; add visit_Constant",
                              DeprecationWarning, 2)
                return visitor(node)
        return self.generic_visit(node, params)
