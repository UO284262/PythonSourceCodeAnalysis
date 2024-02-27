-- Creación de la tabla NODES
CREATE TABLE NODES (
    node_id BIGINT PRIMARY KEY,
    parent_table VARCHAR(255),
    parent_id BIGINT,
    FOREIGN KEY (parent_id) REFERENCES NODES(node_id)
);

-- Creación de la tabla PROGRAMS
CREATE TABLE PROGRAMS (
    program_id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    hasSubDirsWithCode BOOLEAN,
    hasPackages BOOLEAN,
    numberOfModules INTEGER,
    numberOfSubDirsWithCode INTEGER,
    numberOfPackages INTEGER,
    classDefsPct REAL CHECK (classDefsPct >= 0 AND classDefsPct <= 1),
    functionDefsPct REAL CHECK (functionDefsPct >= 0 AND functionDefsPct <= 1),
    enumDefsPct REAL CHECK (enumDefsPct >= 0 AND enumDefsPct <= 1),
    hasCodeRootPackage BOOLEAN,
    avegareDefsPerModule REAL,
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla PARAMETERS
CREATE TABLE PARAMETERS (
    parameters_id BIGINT PRIMARY KEY,
    parent_id BIGINT,
    parametersRole VARCHAR(255),
    numberOfParams INTEGER,
    posOnlyParamPct REAL CHECK (posOnlyParamPct >= 0 AND posOnlyParamPct <= 1),
    varParamPct REAL CHECK (varParamPct >= 0 AND varParamPct <= 1),
    hasVarParam BOOLEAN,
    typeAnnotationPct REAL CHECK (typeAnnotationPct >= 0 AND typeAnnotationPct <= 1),
    kwOnlyParamPct REAL CHECK (kwOnlyParamPct >= 0 AND kwOnlyParamPct <= 1),
    defaultValuePct REAL CHECK (defaultValuePct >= 0 AND defaultValuePct <= 1),
    hasKWParam BOOLEAN,
    nameConvention VARCHAR(255),
    user_id BIGINT,
    experticeLevel BOOLEAN,
    FOREIGN KEY (parent_id) REFERENCES NODES(node_id),
    FOREIGN KEY (parameters_id) REFERENCES NODES(node_id)
);

-- Creación de la tabla MODULES
CREATE TABLE MODULES (
    module_id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    nameConvention VARCHAR(255),
    hasDocString BOOLEAN,
    globalStmtsPct REAL CHECK (globalStmtsPct >= 0 AND globalStmtsPct <= 1),
    globalExpressions REAL CHECK (globalExpressions >= 0 AND globalExpressions <= 1),
    numberOfClasses INTEGER,
    numberOfFunctions INTEGER,
    classDefsPct REAL CHECK (classDefsPct >= 0 AND classDefsPct <= 1),
    functionDefsPct REAL CHECK (functionDefsPct >= 0 AND functionDefsPct <= 1),
    enumDefsPct REAL CHECK (enumDefsPct >= 0 AND enumDefsPct <= 1),
    averageStmtsFunctionBody REAL,
    averageStmtsMethodBody REAL,
    typeAnnotationsPct REAL CHECK (typeAnnotationsPct >= 0 AND typeAnnotationsPct <= 1),
    hasEntryPoint BOOLEAN,
    path VARCHAR(255),
    program_id BIGINT,
    import_id BIGINT,
    FOREIGN KEY (module_id) REFERENCES NODES(node_id),
    FOREIGN KEY (program_id) REFERENCES PROGRAMS(program_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla IMPORTS
CREATE TABLE IMPORTS (
    import_id BIGINT PRIMARY KEY,
    numberImports INTEGER,
    moduleImportsPct REAL CHECK (moduleImportsPct >= 0 AND moduleImportsPct <= 1),
    averageImportedModules REAL,
    fromImportsPct REAL CHECK (fromImportsPct >= 0 AND fromImportsPct <= 1),
    averageFromImportedModules REAL,
    averageAsInImportedModules REAL,
    localImportsPct REAL CHECK (localImportsPct >= 0 AND localImportsPct <= 1),
    user_id BIGINT,
    experticeLevel BOOLEAN,
    FOREIGN KEY (import_id) REFERENCES NODES(node_id)
);

-- Creación de la tabla CLASSDEFS
CREATE TABLE CLASSDEFS (
    classdef_id BIGINT PRIMARY KEY,
    nameConvention VARCHAR(255),
    isEnumClass BOOLEAN,
    numberOfCharacters INTEGER,
    numberOfDecorators INTEGER,
    numberOfBaseClasses INTEGER,
    hasGenericTypeAnnotations BOOLEAN,
    hasDocString BOOLEAN,
    bodyCount INTEGER,
    assignmentsPct REAL CHECK (assignmentsPct >= 0 AND assignmentsPct <= 1),
    expressionsPct REAL CHECK (expressionsPct >= 0 AND expressionsPct <= 1),
    usesMetaclass BOOLEAN,
    numberOfKeyWords INTEGER,
    height INTEGER,
    averageStmtsMethodBody REAL,
    typeAnnotationsPct REAL CHECK (typeAnnotationsPct >= 0 AND typeAnnotationsPct <= 1),
    privateMethodsPct REAL CHECK (privateMethodsPct >= 0 AND privateMethodsPct <= 1),
    magicMethodsPct REAL CHECK (magicMethodsPct >= 0 AND magicMethodsPct <= 1),
    asyncMethodsPct REAL CHECK (asyncMethodsPct >= 0 AND asyncMethodsPct <= 1),
    classMethodsPct REAL CHECK (classMethodsPct >= 0 AND classMethodsPct <= 1),
    staticMethodsPct REAL CHECK (staticMethodsPct >= 0 AND staticMethodsPct <= 1),
    abstractMethodsPct REAL CHECK (abstractMethodsPct >= 0 AND abstractMethodsPct <= 1),
    sourceCode VARCHAR(255),
    module_id BIGINT,
    FOREIGN KEY (classdef_id) REFERENCES NODES(node_id),
    FOREIGN KEY (module_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla FUNCTIONDEFS
CREATE TABLE FUNCTIONDEFS (
    functiondef_id BIGINT PRIMARY KEY,
    nameConvention VARCHAR(255),
    numberOfCharacters INTEGER,
    isPrivate BOOLEAN,
    isMagic BOOLEAN,
    bodyCount INTEGER,
    expressionsPct REAL CHECK (expressionsPct >= 0 AND expressionsPct <= 1),
    isAsync BOOLEAN,
    numberOfDecorators INTEGER,
    hasReturnTypeAnnotation BOOLEAN,
    hasDocString BOOLEAN,
    height INTEGER,
    typeAnnotationsPct REAL CHECK (typeAnnotationsPct >= 0 AND typeAnnotationsPct <= 1),
    sourceCode VARCHAR(255),
    module_id BIGINT,
    parameters_id BIGINT,
    FOREIGN KEY (functiondef_id) REFERENCES NODES(node_id),
    FOREIGN KEY (module_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla METHODDEFS
CREATE TABLE METHODDEFS (
    methoddef_id BIGINT PRIMARY KEY,
    isClassMethod BOOLEAN,
    isStaticMethod BOOLEAN,
    isConstructorMethod BOOLEAN,
    isAbstractMethod BOOLEAN,
    isProperty BOOLEAN,
    isWrapper BOOLEAN,
    isCached BOOLEAN,
    classdef_id BIGINT,
    FOREIGN KEY (methoddef_id) REFERENCES NODES(node_id),
    FOREIGN KEY (classdef_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla STATEMENTS
CREATE TABLE STATEMENTS (
    statement_id BIGINT PRIMARY KEY,
    category VARCHAR(255),
    parent VARCHAR(255),
    statementRole VARCHAR(255),
    height INTEGER,
    depth INTEGER,
    sourceCode VARCHAR(255),
    hasOrElse BOOLEAN,
    bodySize INTEGER,
    first_child_id BIGINT,
    second_child_id BIGINT,
    third_child_id BIGINT,
    parent_id BIGINT,
    FOREIGN KEY (statement_id) REFERENCES NODES(node_id),
    FOREIGN KEY (first_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (second_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (third_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (parent_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla CASES
CREATE TABLE CASES (
    statement_id BIGINT PRIMARY KEY,
    numberOfCases INTEGER,
    guards REAL CHECK (guards >= 0 AND guards <= 1),
    averageBodyCount REAL,
    averageMatchValue REAL CHECK (averageMatchValue >= 0 AND averageMatchValue <= 1),
    averageMatchSingleton REAL CHECK (averageMatchSingleton >= 0 AND averageMatchSingleton <= 1),
    averageMatchSequence REAL CHECK (averageMatchSequence >= 0 AND averageMatchSequence <= 1),
    averageMatchMapping REAL CHECK (averageMatchMapping >= 0 AND averageMatchMapping <= 1),
    averageMatchClass REAL CHECK (averageMatchClass >= 0 AND averageMatchClass <= 1),
    averageMatchStar REAL CHECK (averageMatchStar >= 0 AND averageMatchStar <= 1),
    averageMatchAs REAL CHECK (averageMatchAs >= 0 AND averageMatchAs <= 1),
    averageMatchOr REAL CHECK (averageMatchOr >= 0 AND averageMatchOr <= 1),
    FOREIGN KEY (statement_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla HANDLERS
CREATE TABLE HANDLERS (
    statement_id BIGINT PRIMARY KEY,
    numberOfHandlers INTEGER,
    hasFinally BOOLEAN,
    hasCatchAll BOOLEAN,
    averageBodyCOunt REAL,
    hasStar BOOLEAN,
    FOREIGN KEY (statement_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla EXPRESSIONS
CREATE TABLE EXPRESSIONS (
    expression_id BIGINT PRIMARY KEY,
    category VARCHAR(255),
    parent VARCHAR(255),
    first_child_category VARCHAR(255),
    second_child_category VARCHAR(255),
    third_child_category VARCHAR(255),
    fourth_child_category VARCHAR(255),
    first_child_id BIGINT,
    second_child_id BIGINT,
    third_child_id BIGINT,
    fourth_child_id BIGINT,
    expressionRole VARCHAR(255),
    height INTEGER,
    depth INTEGER,
    sourceCode VARCHAR(255),
    parent_id BIGINT,
    FOREIGN KEY (expression_id) REFERENCES NODES(node_id),
    FOREIGN KEY (first_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (second_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (third_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (fourth_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (parent_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla COMPREHENSIONS
CREATE TABLE COMPREHENSIONS (
    expression_id BIGINT PRIMARY KEY,
    category VARCHAR(255),
    numberOfIfs INTEGER,
    numberOfGenerators INTEGER,
    isAsync BOOLEAN,
    FOREIGN KEY (expression_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla CALLARGS
CREATE TABLE CALLARGS (
    expression_id BIGINT PRIMARY KEY,
    numberArgs INTEGER,
    namedArgsPct REAL CHECK (namedArgsPct >= 0 AND namedArgsPct <= 1),
    doubleStarArgsPct REAL CHECK (doubleStarArgsPct >= 0 AND doubleStarArgsPct <= 1),
    FOREIGN KEY (expression_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla FSTRINGS
CREATE TABLE FSTRINGS (
    expression_id BIGINT PRIMARY KEY,
    numberOfElements INTEGER,
    constantsPct REAL CHECK (constantsPct >= 0 AND constantsPct <= 1),
    expressionsPct REAL CHECK (expressionsPct >= 0 AND expressionsPct <= 1),
    FOREIGN KEY (expression_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla VARIABLES
CREATE TABLE VARIABLES (
    expression_id BIGINT PRIMARY KEY,
    nameConvention VARCHAR(255),
    numberOfCharacters INTEGER,
    isPrivate BOOLEAN,
    isMagic BOOLEAN,
    FOREIGN KEY (expression_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);

-- Creación de la tabla VECTORS
CREATE TABLE VECTORS (
    expression_id BIGINT PRIMARY KEY,
    category VARCHAR(255),
    numberOfElements INTEGER,
    homogeneous BOOLEAN,
    FOREIGN KEY (expression_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    experticeLevel BOOLEAN
);