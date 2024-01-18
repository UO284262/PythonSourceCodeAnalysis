import ast
import visitors.accepts as accepts
from visitors.visitor_info import Visitor_info
from visitors.visitor_print import Visitor_print

accepts.accept_annassign

ast_1 = ast.parse("""
if 1:
    print('a')
""")
info = Visitor_info()
info.visit(ast_1, {})
1