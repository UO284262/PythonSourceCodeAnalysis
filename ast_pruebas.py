import ast
import visitors.accepts as accepts
from visitors.visitor_print import Visitor_print

print(type(123))
print(type([1,2,3]))
print(type(None))
print(type(True))
print(type('a'))
print(type(...))

accepts.accept_annassign

ast_1 = ast.parse("""
123
[1,2,3]
True
'a'                  
""")
printer = Visitor_print()
ast_1.accept(printer,None,0)