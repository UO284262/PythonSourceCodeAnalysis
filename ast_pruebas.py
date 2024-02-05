import ast
from visitors.visitor_print import Visitor_print

ast_1 = ast.parse("""\
@decorator1
@decorator2
class Foo(Enum, base2, metaclass=meta):
    @absact
    def a(a: str):
        b = 0
        c = 0
        return a, b, c
    pass
""")
1