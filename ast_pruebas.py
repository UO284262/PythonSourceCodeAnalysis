import ast
from visitors.visitor_print import Visitor_print

ast_1 = ast.parse("""\
@decorator1
@decorator2
class Foo(Enum, base2, metaclass=meta):
    @absact
    def a(a: str):
        return a
    pass
""")
1