class DBNode:
    def __init__(self, parent_table = None, parent_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Nodes"
        self.parent_table = parent_table
        self.parent_id = parent_id
        self.node_id = 0

class DBProgram:
    def __init__(self, category = None, name: str = None,  hasSubDirsWithCode: bool = None,  hasPackages: bool = None,  numberOfModules: int = None, 
                 numberOfSubDirsWithCode: int = None,  numberOfPackages: int = None,  classDefsPct: int = None,  functionDefsPct: int = None, 
                 enumDefsPct: int = None,  hasCodeRootPackage: bool = None,  averageDefsPerModule: int = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
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
        self.program_id = 0

class DBModule:
    def __init__(self, category = None, module_id = None,  name: str = None,  nameConvention: str = None,  hasDocString: bool = None, 
                 globalStmtsPct: float = None,  globalExpressions: float = None,  numberOfClasses: int = None, 
                 numberOfFunctions: int = None,  classDefsPct: float = None,  functionDefsPct: float = None, 
                 enumDefsPct: float = None,  averageStmtsFunctionBody: float = None, 
                 averageStmtsMethodBody: float = None,  typeAnnotationsPct: float = None, 
                 hasEntryPoint: bool = None,  path: str = None,  program_id = None,  import_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Modules"
        self.category = "Module"
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
    def __init__(self, numberImports: int = None,  moduleImportsPct: float = None, 
                 averageImportedModules: float = None,  fromImportsPct: float = None, averageFromImportedModules: float = None,
                 averageAsInImportedModules: float = None,  localImportsPct: float = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Imports"
        self.numberImports = numberImports
        self.moduleImportsPct = moduleImportsPct
        self.averageImportedModules = averageImportedModules
        self.averageFromImportedModules = averageFromImportedModules
        self.fromImportsPct = fromImportsPct
        self.averageAsInImportedModules = averageAsInImportedModules
        self.localImportsPct = localImportsPct
        self.import_id = 0

class DBClassDef:
    def __init__(self, category = None, classdef_id = None,  nameConvention: str = None,  isEnumClass: bool = None, 
                 numberOfCharacters: int = None, numberOfMethods: int = None, numberOfDecorators: int = None, 
                 numberOfBaseClasses: int = None,  hasGenericTypeAnnotations: bool = None, 
                 hasDocString: bool = None,  bodyCount: int = None,  assignmentsPct: float = None, 
                 expressionsPct: float = None,  usesMetaclass: bool = None, 
                 numberOfKeyWords: int = None,  height: int = None, 
                 averageStmtsMethodBody: float = None,  typeAnnotationsPct: float = None, 
                 privateMethodsPct: float = None,  magicMethodsPct: float = None, 
                 asyncMethodsPct: float = None,  classMethodsPct: float = None, 
                 staticMethodsPct: float = None,  abstractMethodsPct: float = None, 
                 propertyMethodsPct: float = None, sourceCode: str = None,  module_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "ClassDefs"
        self.category = "ClassDef"
        self.classdef_id = classdef_id
        self.nameConvention = nameConvention
        self.isEnumClass = isEnumClass
        self.numberOfCharacters = numberOfCharacters
        self.numberOfDecorators = numberOfDecorators
        self.numberOfMethods = numberOfMethods
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
        self.propertyMethodsPct = propertyMethodsPct
        self.sourceCode = sourceCode
        self.module_id = module_id

class DBFunctionDef:
    def __init__(self, category = None, functiondef_id = None,  nameConvention: str = None, 
                 numberOfCharacters: int = None,  isPrivate: bool = None,  isMagic: bool = None, 
                 bodyCount: int = None,  expressionsPct: float = None, 
                 isAsync: bool = None,  numberOfDecorators: int = None, 
                 hasReturnTypeAnnotation: bool = None,  hasDocString: bool = None, 
                 height: int = None,  typeAnnotationsPct: float = None, 
                 sourceCode: str = None,  module_id = None,  parameters_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "FunctionDefs"
        self.category = "FunctionDef"
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
    def __init__(self, category = None, methoddef_id = None,  classdef_id = None, 
                 isClassMethod: bool = None,  isStaticMethod: bool = None, 
                 isConstructorMethod: bool = None,  isAbstractMethod: bool = None, 
                 isProperty: bool = None,  isWrapper: bool = None,  isCached: bool = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "MethodDefs"
        self.category = "MethodDef"
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
    def __init__(self,  numberOfParams: int = None, parent_id: int = None,
                 posOnlyParamPct: float = None,  varParamPct: float = None, 
                 hasVarParam: bool = None,  typeAnnotationPct: float = None, 
                 kwOnlyParamPct: float = None,  defaultValuePct: float = None, 
                 hasKWParam: bool = None,  nameConvention: str = None,  node = None,
                 user_id = None, expertise_level = None, parametersRole : str = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
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
        self.parent_id = parent_id
        self.parametersRole = parametersRole

class DBStatement:
    def __init__(self,  statement_id = None,  category: str = None,  parent: str = None,  statementRole: str = None, 
                 height: int = None,  depth: int = None,  sourceCode: str = None,  parent_id = None,  node = None, 
                 hasOrElse: bool = None,  bodySize: int = None, 
                 first_child_id: int = None,  second_child_id: int = None, 
                 third_child_id: int = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
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
    def __init__(self,  expression_id = None,  category: str = None, 
                 first_child_category: str = None,  second_child_category: str = None, 
                 third_child_category: str = None,  fourth_child_category: str = None,
                 first_child_id: str = None, second_child_id: str = None,
                 third_child_id: str = None, fourth_child_id: str = None,
                 parent: str = None,  expressionRole: str = None,  height: int = None, 
                 depth: int = None,  sourceCode: str = None,  parent_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Expressions"
        self.expression_id = expression_id
        self.category = category
        self.first_child_category = first_child_category
        self.second_child_category = second_child_category
        self.third_child_category = third_child_category
        self.fourth_child_category = fourth_child_category
        self.first_child_id = first_child_id
        self.second_child_id = second_child_id
        self.third_child_id = third_child_id
        self.fourth_child_id = fourth_child_id
        self.parent = parent
        self.expressionRole = expressionRole
        self.height = height
        self.depth = depth
        self.sourceCode = sourceCode
        self.parent_id = parent_id

class DBComprehension:
    def __init__(self,  category: str = None,  numberOfIfs: int = None, 
                 numberOfGenerators: int = None,  isAsync: bool = None, 
                 expression_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Comprehensions"
        self.category = category
        self.numberOfIfs = numberOfIfs
        self.numberOfGenerators = numberOfGenerators
        self.isAsync = isAsync
        self.expression_id = expression_id

class DBFString:
    def __init__(self,  numberOfElements: int = None,  constantsPct: float = None, 
                 expressionsPct: float = None,  expression_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "FStrings"
        self.numberOfElements = numberOfElements
        self.constantsPct = constantsPct
        self.expressionsPct = expressionsPct
        self.expression_id = expression_id

class DBVariable:
    def __init__(self,  nameConvention: str = None,  numberOfCharacters: int = None, 
                 isPrivate: bool = None,  isMagic: bool = None,  expression_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Variables"
        self.nameConvention = nameConvention
        self.numberOfCharacters = numberOfCharacters
        self.isPrivate = isPrivate
        self.isMagic = isMagic
        self.expression_id = expression_id

class DBVector:
    def __init__(self,  category: str = None,  numberOfElements: int = None, 
                 homogeneous: bool = None,  expression_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Vectors"
        self.category = category
        self.numberOfElements = numberOfElements
        self.homogeneous = homogeneous
        self.expression_id = expression_id

class DBCallArg:
    def __init__(self,  numberArgs: int = None, 
                 namedArgsPct: float = None,  doubleStarArgsPct: float = None, 
                 expression_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "CallArgs"
        self.numberArgs = numberArgs
        self.namedArgsPct = namedArgsPct
        self.doubleStarArgsPct = doubleStarArgsPct
        self.expression_id = expression_id
        self.callArgs_id = 0

class DBCase:
    def __init__(self,  numberOfCases: int = None,  guards: float = None, 
                 averageBodyCount: float = None,  averageMatchValue: float = None, 
                 averageMatchSingleton: float = None,  averageMatchSequence: float = None, 
                 averageMatchMapping: float = None,  averageMatchClass: float = None, 
                 averageMatchStar: float = None,  averageMatchAs: float = None, 
                 averageMatchOr: float = None,  statement_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
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

class DBHandler:
    def __init__(self,  numberOfHandlers: int = None, category: str = None, 
                 hasFinally: bool = None,  hasCatchAll: bool = None, 
                 averageBodyCount: float = None,  hasStar: bool = None, 
                 statement_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Handler"
        self.category = "ExceptHandler"
        self.numberOfHandlers = numberOfHandlers
        self.hasFinally = hasFinally
        self.hasCatchAll = hasCatchAll
        self.averageBodyCount = averageBodyCount
        self.hasStar = hasStar
        self.statement_id = statement_id
