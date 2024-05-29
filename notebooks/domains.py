NAMING_CONVENTION_VALUES = ['SnakeCase', 'Lower', 'NoNameConvention', 'CamelUp', 'Upper', 'CamelLow', 'Discard']

STATEMENT_CATEGORY_VALUES = ['AssignmentStmt', 'If', 'Return', 'For', 'ImportFrom', 'Import', 'AugmentedAssignment', 'Raise', 'Try', 'Assert', 'While', 'With', 'Break', 'Pass', 'AnnotatedAssignment', 'Continue', 'Delete', 'Global', 'Match', 'Nonlocal', 'AsyncWith', 'ExceptHandler', 'TypeAlias']
STATEMENT_PARENT_VALUES = ['Module', 'ClassDef', 'FunctionDef', 'MethodDef'] + STATEMENT_CATEGORY_VALUES
STATEMENT_ROLE_VALUES = ['Module', 'IfBody', 'IfElseBody', 'FunctionDefBody', 'AsyncFunctionDefBody', 'MethodDefBody', 'AsyncMethodDefBody', 'ClassDefBody', 'ForBody', 'ForElseBody', 'AsyncForBody', 'AsyncForElseBody', 'WithBody', 'WhileBody', 'WhileElseBody', 'ExceptBody', 'AsyncWithBody', 'TryBody', 'TryElseBody', 'TryFinallyBody', 'TryHandler', 'TryHandlerStar', 'CaseBody']

EXPRESSION_CATEGORY_VALUES = ['Logical', 'AssignmentExp', 'Arithmetic', 'Pow', 'Shift', 'BWLogical', 'MatMult', 'UnaryArithmetic', 'UnaryNot', 'UnaryBWNot', 'Lambda', 'Ternary', 'SetLiteral', 'ListLiteral', 'TupleLiteral', 'DictionaryLiteral', 'ListComprehension', 'SetComprehension', 'DictComprehension', 'GeneratorComprehension', 'Await', 'Yield', 'YieldFrom', 'Compare', 'Call', 'FString', 'FormattedValue', 'IntLiteral', 'FloatLiteral', 'ComplexLiteral', 'NoneLiteral', 'BoolLiteral', 'StringLiteral', 'EllipsisLiteral', 'Dot', 'Variable', 'Slice', 'Indexing', 'Star']

STATEMENT_CHILDREN_VALUES = ['Parameter', None] + EXPRESSION_CATEGORY_VALUES
