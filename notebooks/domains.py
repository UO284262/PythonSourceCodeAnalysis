NAMING_CONVENTION_VALUES = ['SnakeCase', 'Lower', 'NoNameConvention', 'CamelUp', 'Upper', 'CamelLow', 'Discard']

STATEMENT_CATEGORY_VALUES = ['AssignmentStmt', 'If', 'Return', 'For', 'ImportFrom', 'Import', 'AugmentedAssignment', 'Raise', 'Try', 'Assert', 'While', 'With', 'Break', 'Pass', 'AnnotatedAssignment', 'Continue', 'Delete', 'Global', 'Match', 'Nonlocal', 'AsyncWith', 'ExceptHandler', 'TypeAlias']
STATEMENT_PARENT_VALUES = ['Module', 'ClassDef', 'FunctionDef', 'MethodDef'] + STATEMENT_CATEGORY_VALUES
STATEMENT_ROLE_VALUES = ['Module', 'IfBody', 'IfElseBody', 'FunctionDefBody', 'AsyncFunctionDefBody', 'MethodDefBody', 'AsyncMethodDefBody', 'ClassDefBody', 'ForBody', 'ForElseBody', 'AsyncForBody', 'AsyncForElseBody', 'WithBody', 'WhileBody', 'WhileElseBody', 'ExceptBody', 'AsyncWithBody', 'TryBody', 'TryElseBody', 'TryFinallyBody', 'TryHandler', 'TryHandlerStar', 'CaseBody']

EXPRESSION_CATEGORY_VALUES = ['NoneType', 'Logical', 'AssignmentExp', 'Arithmetic', 'Pow', 'Shift', 'BWLogical', 'MatMult', 'UnaryArithmetic', 'UnaryNot', 'UnaryBWNot', 'Lambda', 'Ternary', 'SetLiteral', 'ListLiteral', 'TupleLiteral', 'DictionaryLiteral', 'ListComprehension', 'SetComprehension', 'DictComprehension', 'GeneratorComprehension', 'Await', 'Yield', 'YieldFrom', 'Compare', 'Call', 'FString', 'FormattedValue', 'IntLiteral', 'FloatLiteral', 'ComplexLiteral', 'NoneLiteral', 'BoolLiteral', 'StringLiteral', 'EllipsisLiteral', 'Dot', 'Variable', 'Slice', 'Indexing', 'Star']
EXPRESSION_PARENT_VALUES = STATEMENT_PARENT_VALUES + EXPRESSION_CATEGORY_VALUES
EXPRESSION_ROLE_VALUES = ['Module', 'FuncDecorator', 'FuncBody', 'ReturnType', 'ClassBase', 'ClassDecorator', 'MethodBody', 'ClassBody', 'Return', 'Delete', 'AssignLHS', 'AssignRHS', 'TypeAliasLHS', 'TypeAliasRHS', 'AugmentedAssignmentLHS', 'AugmentedAssignmentRHS', 'VarDefVarName', 'VarDefType', 'VarDefInitValue', 'ForElement', 'ForEnumerable', 'ForBody', 'ForElseBody', 'AsyncForElement', 'AsyncForEnumerable', 'AsyncForBody', 'AsyncForElseBody', 'WhileCondition', 'WhileBody', 'WhileElseBody', 'IfCondition', 'IfBody', 'IfElseBody', 'WithElement', 'WithAs', 'WithBody', 'AsyncWithElement', 'AsyncWithAs', 'AsyncWithBody', 'MatchCondition', 'CaseCondition', 'CaseGuard', 'CaseBody', 'Raise', 'RaiseFrom', 'TryBody', 'ExceptType', 'ExceptBody', 'TryElse', 'FinallyBody', 'AssertCondition', 'AssertMessage', 'Logical', 'AssignExpLHS', 'AssignExpRHS', 'Arithmetic', 'Pow', 'Shift', 'BWLogical', 'MatMult', 'LambdaBody', 'TernaryCondition', 'TernaryIfBody', 'TernaryElseBody', 'SetLiteral', 'ListLiteral', 'TupleLiteral', 'DictionaryLiteralKey', 'DictionaryLiteralValue', 'ComprehensionElement', 'ComprehensionTarget', 'ComprehensionIter', 'ComprehensionIf', 'Await', 'Yield', 'YieldFrom', 'Relational', 'Is', 'In', 'CallFuncName', 'CallArg', 'FString', 'Dot', 'Slice', 'Indexing', 'Star', 'TypeAnnotation', 'DefaultParamValue', 'TypeVar', 'FormattedFormat', 'AugmentedAssigmentLHS', 'Compare', 'FormattedValue', 'AugmentedAssigmentRHS', 'TryElseBody', 'ComprenhensionElement']

STATEMENT_CHILDREN_VALUES = ['Parameter', None] + EXPRESSION_CATEGORY_VALUES
EXPRESSION_CHILDREN_VALUES = STATEMENT_CHILDREN_VALUES

COMPREHENSION_CATEGORY_VALUES = ['ListComprehension', 'GeneratorComprehension', 'DictComprehension', 'SetComprehension']
VECTOR_CATEGORY_VALUES = ['TupleLiteral', 'ListLiteral', 'DictionaryLiteral', 'SetLiteral']


