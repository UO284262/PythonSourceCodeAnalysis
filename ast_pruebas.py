import ast
import visitors.accepts as accepts
from visitors.visitor_info import Visitor_info
from visitors.visitor_print import Visitor_print
from db.db_utils import init_db 

init_db()

ast_1 = ast.parse("""
if 1:
    print('a')
""")
info = Visitor_info()
info.visit(ast_1, {})
1