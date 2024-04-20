import ast

ast_1 = ast.parse(
"""
a = 2
b = 5
print(a+b)
"""
)

print(ast_1)
