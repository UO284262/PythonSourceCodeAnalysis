import uuid

class DBNode:
    def __init__(self,parent_table,parent_id, node):
        self.node = node
        self.table = "Nodes"
        self.parent_table = parent_table
        self.parent_id = parent_id
        self.node_id = 0

class DBProgram:
    def __init__(self, name: str, hasSubDirsWithCode: bool, hasPackages: bool, numberOfModules: int,
                 numberOfSubDirsWithCode: int, numberOfPackages: int, classDefsPct: int, functionDefsPct: int,
                 enumDefsPct: int, hasCodeRootPackage: bool, averageDefsPerModule: int, user_id, isExpert: bool, node):
        self.node = node
        self.table = "Programs"
        self.name = name
        self.hasSubDirsWithCode = hasSubDirsWithCode
        self.hasPackages = hasPackages
        self.numberOfModules = numberOfModules
        self.numberOfSubDirsWithCode = numberOfSubDirsWithCode
        self.numberOfPackages = numberOfPackages
        self.classDefsPct = classDefsPct
        self.functionDefsPct = functionDefsPct
        self.enumDefsPct = enumDefsPct
        self.hasCodeRootPackage = hasCodeRootPackage
        self.averageDefsPerModule = averageDefsPerModule
        self.user_id = user_id
        self.isExpert = isExpert
        self.program_id = 0

class DBModule:
    def __init__(self, module_id, name: str, nameConvention: str, hasDocString: bool,
                 globalStmtsPct: float, globalExpressions: float, numberOfClasses: int,
                 numberOfFunctions: int, classDefsPct: float, functionDefsPct: float,
                 enumDefsPct: float, averageStmtsFunctionBody: float,
                 averageStmtsMethodBody: float, typeAnnotationsPct: float,
                 hasEntryPoint: bool, path: str, program_id, import_id, node):
        self.node = node
        self.table = "Modules"
        self.module_id = module_id
        self.name = name
        self.nameConvention = nameConvention
        self.hasDocString = hasDocString
        self.globalStmtsPct = globalStmtsPct
        self.globalExpressions = globalExpressions
        self.numberOfClasses = numberOfClasses
        self.numberOfFunctions = numberOfFunctions
        self.classDefsPct = classDefsPct
        self.functionDefsPct = functionDefsPct
        self.enumDefsPct = enumDefsPct
        self.averageStmtsFunctionBody = averageStmtsFunctionBody
        self.averageStmtsMethodBody = averageStmtsMethodBody
        self.typeAnnotationsPct = typeAnnotationsPct
        self.hasEntryPoint = hasEntryPoint
        self.path = path
        self.program_id = program_id
        self.import_id = import_id

class DBImport:
    def __init__(self, numberImports: int, moduleImportsPct: float,
                 averageImportedModules: float, fromImportsPct: float,
                 averageAsInImportedModules: float, localImportsPct: float, node):
        self.node = node
        self.table = "Imports"
        self.numberImports = numberImports
        self.moduleImportsPct = moduleImportsPct
        self.averageImportedModules = averageImportedModules
        self.fromImportsPct = fromImportsPct
        self.averageAsInImportedModules = averageAsInImportedModules
        self.localImportsPct = localImportsPct
        self.import_id = 0

class DBClassDef:
    def __init__(self, classdef_id, nameConvention: str, isEnumClass: bool,
                 numberOfCharacters: int, numberOfDecorators: int,
                 numberOfBaseClasses: int, hasGenericTypeAnnotations: bool,
                 hasDocString: bool, bodyCount: int, assignmentsPct: float,
                 expressionsPct: float, usesMetaclass: bool,
                 numberOfKeyWords: int, height: int,
                 averageStmtsMethodBody: float, typeAnnotationsPct: float,
                 privateMethodsPct: float, magicMethodsPct: float,
                 asyncMethodsPct: float, classMethodsPct: float,
                 staticMethodsPct: float, abstractMethodsPct: float,
                 sourceCode: str, module_id, node):
        self.node = node
        self.table = "ClassDefs"
        self.classdef_id = classdef_id
        self.nameConvention = nameConvention
        self.isEnumClass = isEnumClass
        self.numberOfCharacters = numberOfCharacters
        self.numberOfDecorators = numberOfDecorators
        self.numberOfBaseClasses = numberOfBaseClasses
        self.hasGenericTypeAnnotations = hasGenericTypeAnnotations
        self.hasDocString = hasDocString
        self.bodyCount = bodyCount
        self.assignmentsPct = assignmentsPct
        self.expressionsPct = expressionsPct
        self.usesMetaclass = usesMetaclass
        self.numberOfKeyWords = numberOfKeyWords
        self.height = height
        self.averageStmtsMethodBody = averageStmtsMethodBody
        self.typeAnnotationsPct = typeAnnotationsPct
        self.privateMethodsPct = privateMethodsPct
        self.magicMethodsPct = magicMethodsPct
        self.asyncMethodsPct = asyncMethodsPct
        self.classMethodsPct = classMethodsPct
        self.staticMethodsPct = staticMethodsPct
        self.abstractMethodsPct = abstractMethodsPct
        self.sourceCode = sourceCode
        self.module_id = module_id

class DBFunctionDef:
    def __init__(self, functiondef_id, nameConvention: str,
                 numberOfCharacters: int, isPrivate: bool, isMagic: bool,
                 bodyCount: int, expressionsPct: float,
                 isAsync: bool, numberOfDecorators: int,
                 hasReturnTypeAnnotation: bool, hasDocString: bool,
                 height: int, typeAnnotationsPct: float,
                 sourceCode: str, module_id, parameters_id, node):
        self.node = node
        self.table = "FunctionDefs"
        self.functiondef_id = functiondef_id
        self.nameConvention = nameConvention
        self.numberOfCharacters = numberOfCharacters
        self.isPrivate = isPrivate
        self.isMagic = isMagic
        self.bodyCount = bodyCount
        self.expressionsPct = expressionsPct
        self.isAsync = isAsync
        self.numberOfDecorators = numberOfDecorators
        self.hasReturnTypeAnnotation = hasReturnTypeAnnotation
        self.hasDocString = hasDocString
        self.height = height
        self.typeAnnotationsPct = typeAnnotationsPct
        self.sourceCode = sourceCode
        self.module_id = module_id
        self.parameters_id = parameters_id

class DBMethodDef:
    def __init__(self, methoddef_id, classdef_id,
                 isClassMethod: bool, isStaticMethod: bool,
                 isConstructorMethod: bool, isAbstractMethod: bool,
                 isProperty: bool, isWrapper: bool, isCached: bool, node):
        self.node = node
        self.table = "MethodDefs"
        self.methoddef_id = methoddef_id
        self.classdef_id = classdef_id
        self.isClassMethod = isClassMethod
        self.isStaticMethod = isStaticMethod
        self.isConstructorMethod = isConstructorMethod
        self.isAbstractMethod = isAbstractMethod
        self.isProperty = isProperty
        self.isWrapper = isWrapper
        self.isCached = isCached

class DBParameter:
    def __init__(self, numberOfParams: int,
                 posOnlyParamPct: float, varParamPct: float,
                 hasVarParam: bool, typeAnnotationPct: float,
                 kwOnlyParamPct: float, defaultValuePct: float,
                 hasKWParam: bool, nameConvention: str, node):
        self.node = node
        self.table = "Parameters"
        self.numberOfParams = numberOfParams
        self.posOnlyParamPct = posOnlyParamPct
        self.varParamPct = varParamPct
        self.hasVarParam = hasVarParam
        self.typeAnnotationPct = typeAnnotationPct
        self.kwOnlyParamPct = kwOnlyParamPct
        self.defaultValuePct = defaultValuePct
        self.hasKWParam = hasKWParam
        self.nameConvention = nameConvention
        self.parameters_id = 0

class DBStatement:
    def __init__(self, statement_id, category: str, parent: str, statementRole: str,
                 height: int, depth: int, sourceCode: str, parent_id, node,
                 hasOrElse: bool = None, bodySize: int = None,
                 first_child_id: int = None, second_child_id: int = None,
                 third_child_id: int = None):
        self.node = node
        self.table = "Statements"
        self.statement_id = statement_id
        self.category = category
        self.parent = parent
        self.statementRole = statementRole
        self.height = height
        self.depth = depth
        self.sourceCode = sourceCode
        self.hasOrElse = hasOrElse
        self.bodySize = bodySize
        self.first_child_id = first_child_id
        self.second_child_id = second_child_id
        self.third_child_id = third_child_id
        self.parent_id = parent_id

class DBExpression:
    def __init__(self, expression_id, category: str,
                 first_child_category: str, second_child_category: str,
                 third_child_category: str, fourth_child_category: str,
                 parent: str, expressionRole: str, height: int,
                 depth: int, sourceCode: str, parent_id, node):
        self.node = node
        self.table = "Expressions"
        self.expression_id = expression_id
        self.category = category
        self.first_child_category = first_child_category
        self.second_child_category = second_child_category
        self.third_child_category = third_child_category
        self.fourth_child_category = fourth_child_category
        self.parent = parent
        self.expressionRole = expressionRole
        self.height = height
        self.depth = depth
        self.sourceCode = sourceCode
        self.parent_id = parent_id

class DBComprehension:
    def __init__(self, category: str, numberOfIfs: int,
                 numberOfGenerators: int, isAsync: bool,
                 expression_id, node):
        self.node = node
        self.table = "Comprehensions"
        self.category = category
        self.numberOfIfs = numberOfIfs
        self.numberOfGenerators = numberOfGenerators
        self.isAsync = isAsync
        self.expression_id = expression_id

class DBFString:
    def __init__(self, numberOfElements: int, constantsPct: float,
                 expressionsPct: float, expression_id, node):
        self.node = node
        self.table = "FStrings"
        self.numberOfElements = numberOfElements
        self.constantsPct = constantsPct
        self.expressionsPct = expressionsPct
        self.expression_id = expression_id

class DBVariable:
    def __init__(self, nameConvention: str, numberOfCharacters: int,
                 isPrivate: bool, isMagic: bool, expression_id, node):
        self.node = node
        self.table = "Variables"
        self.nameConvention = nameConvention
        self.numberOfCharacters = numberOfCharacters
        self.isPrivate = isPrivate
        self.isMagic = isMagic
        self.expression_id = expression_id

class DBVector:
    def __init__(self, category: str, numberOfElements: int,
                 homogeneous: bool, expression_id, node):
        self.node = node
        self.table = "Vectors"
        self.category = category
        self.numberOfElements = numberOfElements
        self.homogeneous = homogeneous
        self.expression_id = expression_id

class DBCallArg:
    def __init__(self, numberArgs: int,
                 namedArgsPct: float, doubleStarArgsPct: float,
                 expression_id, node):
        self.node = node
        self.table = "CallArgs"
        self.numberArgs = numberArgs
        self.namedArgsPct = namedArgsPct
        self.doubleStarArgsPct = doubleStarArgsPct
        self.expression_id = expression_id
        self.callArgs_id = 0

class DBCase:
    def __init__(self, numberOfCases: int, guards: float,
                 averageBodyCount: float, averageMatchValue: float,
                 averageMatchSingleton: float, averageMatchSequence: float,
                 averageMatchMapping: float, averageMatchClass: float,
                 averageMatchStar: float, averageMatchAs: float,
                 averageMatchOr: float, statement_id, node):
        self.node = node
        self.table = "Cases"
        self.numberOfCases = numberOfCases
        self.guards = guards
        self.averageBodyCount = averageBodyCount
        self.averageMatchValue = averageMatchValue
        self.averageMatchSingleton = averageMatchSingleton
        self.averageMatchSequence = averageMatchSequence
        self.averageMatchMapping = averageMatchMapping
        self.averageMatchClass = averageMatchClass
        self.averageMatchStar = averageMatchStar
        self.averageMatchAs = averageMatchAs
        self.averageMatchOr = averageMatchOr
        self.statement_id = statement_id
        self.cases_id = 0

class DBHandler:
    def __init__(self, numberOfHandlers: int,
                 hasFinally: bool, hasCatchAll: bool,
                 averageBodyCOunt: float, hasStar: bool,
                 statement_id, node):
        self.node = node
        self.table = "Handler"
        self.numberOfHandlers = numberOfHandlers
        self.hasFinally = hasFinally
        self.hasCatchAll = hasCatchAll
        self.averageBodyCOunt = averageBodyCOunt
        self.hasStar = hasStar
        self.statement_id = statement_id
        self.handler_id = 0
