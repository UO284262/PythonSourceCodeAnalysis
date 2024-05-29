NAMING_CONVENTION_VALUES = ['SnakeCase', 'Lower', 'NoNameConvention', 'CamelUp', 'Upper', 'CamelLow', 'Discard']
STATEMENT_CATEGORY_VALUES = ['AssignmentStmt', 'If', 'Return', 'For', 'ImportFrom', 'Import', 'AugmentedAssignment', 'Raise', 'Try', 'Assert', 'While', 'With', 'Break', 'Pass', 'AnnotatedAssignment', 'Continue', 'Delete', 'Global', 'Match', 'Nonlocal', 'AsyncWith', 'ExceptHandler', 'TypeAlias']
STATEMENT_PARENT_VALUES = ['Module', 'ClassDef', 'FunctionDef', 'MethodDef'] + STATEMENT_CATEGORY_VALUES
