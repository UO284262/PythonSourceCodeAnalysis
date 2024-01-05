import ast
import visitors.accepts as accepts
from visitors.visitor_print import Visitor_print

ast_1 = ast.parse('type Alias = int')
printer = Visitor_print()
ast_1.accept(printer,0)