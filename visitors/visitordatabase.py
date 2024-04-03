import ast
from typing import Dict
from visitors.nodevisitor import NodeVisitor
import db.db_entities as db_entities
from db.db_utils import write_on_db


class VisitorDataBase(NodeVisitor):
    def __init__(self):
        self.modules = []
        self.sql_insert = []
        self.data_to_insert = []
        self.sql_nodes_to_insert = []
        self.nodes_data_to_insert = []

    def visit_Program(self, node: db_entities.DBProgram, params: Dict):
        self.insert_Program(node)
        #write_on_db(self.sql_nodes_to_insert, self.nodes_data_to_insert, self.sql_insert, self.data_to_insert, self.modules)
        self.sql_insert = []
        self.data_to_insert = []
        self.nodes_data_to_insert = []
        self.sql_nodes_to_insert = []
        pass
    
    def visit_Module(self, node: db_entities.DBModule, params: Dict):
        self.insert_Import(params["dbimport"])
        self.insert_Module(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append(params["node"].path)
        pass
    
    def visit_FunctionDef(self, node: ast.FunctionDef, params: Dict):
        if params['isMethod']:
            self.insert_MethodDef(params['method'])
        self.insert_FunctionDef(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef, params: Dict):
        if params['isMethod']:
            self.insert_MethodDef(params['method'])
        self.insert_FunctionDef(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_ClassDef(self, node: ast.ClassDef, params: Dict):
        self.insert_ClassDef(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ############################### STATEMENTS #############################
    def visit_Return(self, node: ast.Return, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Delete(self, node: ast.Delete, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Assign(self, node: ast.Assign, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_TypeAlias(self, node: ast.TypeAlias, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_AugAssign(self, node: ast.AugAssign, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_AnnAssign(self, node: ast.AnnAssign, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_For(self, node: ast.For, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_AsyncFor(self, node: ast.AsyncFor, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_While(self, node: ast.While, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_If(self, node: ast.If, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_With(self, node: ast.With, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_AsyncWith(self, node: ast.AsyncWith, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Match(self, node: ast.Match, params: Dict):
        self.insert_Case(params["case"])
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Raise(self, node: ast.Raise, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Try(self, node: ast.Try, params: Dict):
        self.insert_Handler(params["handler"])
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_TryStar(self, node: ast.Try, params: Dict):
        self.insert_Handler(params["handler"])
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Assert(self, node: ast.Assert, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Global(self, node: ast.Global, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_NonLocal(self, node: ast.Nonlocal, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Pass(self, node: ast.Pass, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Break(self, node: ast.Break, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Continue(self, node: ast.Continue, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ############################ IMPORTS ##################################
    def visit_Import(self, node: ast.Import, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_ImportFrom(self, node: ast.ImportFrom, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ############################ EXPRESSIONS ##################################
    def visit_BoolOp(self, node: ast.BoolOp, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_NamedExpr(self, node: ast.NamedExpr, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_BinOp(self, node: ast.BinOp, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_UnaryOp(self, node: ast.UnaryOp, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Lambda(self, node: ast.Lambda, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_IfExp(self, node: ast.IfExp, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ######################### COMPREHENSIONS #############################
    def visit_ListComp(self, node: ast.ListComp, params: Dict):
        self.insert_Comprehension(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_SetComp(self, node: ast.SetComp, params: Dict):
        self.insert_Comprehension(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_DictComp(self, node: ast.DictComp, params: Dict):
        self.insert_Comprehension(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_GeneratorExp(self, node: ast.GeneratorExp, params: Dict):
        self.insert_Comprehension(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ######################################################################
    def visit_Await(self, node: ast.Await, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Yield(self, node: ast.Yield, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_YieldFrom(self, node: ast.YieldFrom, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Compare(self, node: ast.Compare, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ########################## call_args ###########################
    def visit_Call(self, node: ast.Call, params: Dict):
        self.insert_CallArg(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ################################################################
    def visit_FormattedValue(self, node: ast.FormattedValue, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ########################### F-strings #####################################
    def visit_JoinedStr(self, node: ast.JoinedStr, params: Dict):
        self.insert_FString(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ###########################################################################
    def visit_constant(self, node: ast.Constant, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Attribute(self, node: ast.Attribute, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Subscript(self, node: ast.Subscript, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Starred(self, node: ast.Starred, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ############################# Variable ##################################
    def visit_Name(self, node: ast.Name, params: Dict):
        self.insert_Variable(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")        
        pass

    ############################### Vectors #################################
    def visit_List(self, node: ast.List, params: Dict):
        self.insert_Vector(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Tuple(self, node: ast.Tuple, params: Dict):
        self.insert_Vector(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Dict(self, node: ast.Dict, params: Dict):
        self.insert_Vector(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_Set(self, node: ast.Set, params: Dict):
        self.insert_Vector(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass

    ########################################################################
    def visit_Slice(self, node: ast.Slice, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["dbnode"])
        self.modules.append("No module")
        pass
    
    def visit_ExceptHandler(self, node: ast.ExceptHandler, params: Dict):
        pass

    ############################### Cases ###################################
    def visit_MatchValue(self, node: ast.MatchValue, params: Dict):
        pass
    
    def visit_MatchSingleton(self, node: ast.MatchSingleton, params: Dict):
        pass
    
    def visit_MatchSequence(self, node: ast.MatchSequence, params: Dict):
        pass
    
    def visit_MatchMapping(self, node: ast.MatchMapping, params: Dict):
        pass
    
    def visit_MatchClass(self, node: ast.MatchClass, params: Dict):
        pass
    
    def visit_MatchStar(self, node: ast.MatchStar, params: Dict):
        pass
    
    def visit_MatchAs(self, node: ast.MatchAs, params: Dict):
        pass
    
    def visit_MatchOr(self, node: ast.MatchOr, params: Dict):
        pass

    ########################## visit extras #################################
    def visit_Arguments(self, node: ast.arguments, params: Dict):
        self.insert_Parameter(params["dbparams"])
        pass

    def insert_Program(self, node: db_entities.DBProgram):
        sql_insert = '''INSERT INTO Programs (
                            program_id,
                            name, 
                            hasSubDirsWithCode, 
                            hasPackages, 
                            numberOfModules, 
                            numberOfSubDirsWithCode, 
                            numberOfPackages,
                            classDefsPct, 
                            functionDefsPct, 
                            enumDefsPct, 
                            hasCodeRootPackage, 
                            averageDefsPerModule, 
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.program_id,
                            node.name, 
                            node.hasSubDirsWithCode, 
                            node.hasPackages, 
                            node.numberOfModules, 
                            node.numberOfSubDirsWithCode, 
                            node.numberOfPackages,
                            node.classDefsPct, 
                            node.functionDefsPct, 
                            node.enumDefsPct, 
                            node.hasCodeRootPackage, 
                            node.averageDefsPerModule, 
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)

    def insert_FunctionDef(self, node: db_entities.DBFunctionDef):
        sql_insert = '''INSERT INTO FunctionDefs (
                            functiondef_id,
                            nameConvention, 
                            numberOfCharacters, 
                            isPrivate, 
                            isMagic, 
                            bodyCount, 
                            expressionsPct,
                            isAsync, 
                            numberOfDecorators, 
                            hasReturnTypeAnnotation, 
                            hasDocString, 
                            height, 
                            typeAnnotationsPct, 
                            sourceCode, 
                            module_id,
                            parent_id,
                            parameters_id,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.functiondef_id,
                            node.nameConvention, 
                            node.numberOfCharacters, 
                            node.isPrivate, 
                            node.isMagic, 
                            node.bodyCount, 
                            node.expressionsPct, 
                            node.isAsync, 
                            node.numberOfDecorators, 
                            node.hasReturnTypeAnnotation, 
                            node.hasDocString,
                            node.height, 
                            node.typeAnnotationsPct,
                            node.sourceCode, 
                            node.module_id,
                            node.parent_id,
                            node.parameters_id,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Module(self, node: db_entities.DBModule):
        sql_insert = '''INSERT INTO Modules (
                            module_id, 
                            name, 
                            nameConvention, 
                            hasDocString, 
                            globalStmtsPct, 
                            globalExpressions, 
                            numberOfClasses, 
                            numberOfFunctions, 
                            classDefsPct, 
                            functionDefsPct, 
                            enumDefsPct, 
                            averageStmtsFunctionBody, 
                            averageStmtsMethodBody, 
                            typeAnnotationsPct, 
                            hasEntryPoint, 
                            program_id, 
                            path, 
                            import_id,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.module_id,
                            node.name, 
                            node.nameConvention, 
                            node.hasDocString, 
                            node.globalStmtsPct, 
                            node.globalExpressions, 
                            node.numberOfClasses, 
                            node.numberOfFunctions, 
                            node.classDefsPct, 
                            node.functionDefsPct, 
                            node.enumDefsPct, 
                            node.averageStmtsFunctionBody, 
                            node.averageStmtsMethodBody, 
                            node.typeAnnotationsPct, 
                            node.hasEntryPoint, 
                            node.program_id, 
                            node.path, 
                            node.import_id,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Node(self, node: db_entities.DBNode):
        sql_nodes_insert = '''INSERT INTO Nodes (
                            node_id,
                            parent_table, 
                            parent_id) 
                        VALUES (%s, %s, %s);'''
        nodes_data_to_insert = (node.node_id,
                            node.parent_table, 
                            node.parent_id)
        self.sql_nodes_to_insert.append(sql_nodes_insert)
        self.nodes_data_to_insert.append(nodes_data_to_insert)
        
    def insert_Import(self, node: db_entities.DBImport):
        sql_insert = '''INSERT INTO Imports (
                            import_id,
                            numberImports,
                            moduleImportsPct, 
                            averageImportedModules, 
                            fromImportsPct,
                            averageFromImportedModules, 
                            averageAsInImportedModules, 
                            localImportsPct,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.import_id,
                            node.numberImports,
                            node.moduleImportsPct, 
                            node.averageImportedModules, 
                            node.fromImportsPct, 
                            node.averageFromImportedModules,
                            node.averageAsInImportedModules, 
                            node.localImportsPct,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_ClassDef(self, node: db_entities.DBClassDef):
        sql_insert = '''INSERT INTO ClassDefs (
                            classdef_id,
                            nameConvention, 
                            isEnumClass, 
                            numberOfCharacters, 
                            numberOfDecorators, 
                            numberOfMethods,
                            numberOfBaseClasses, 
                            hasGenericTypeAnnotations, 
                            hasDocString, 
                            bodyCount, 
                            assignmentsPct, 
                            expressionsPct, 
                            usesMetaclass, 
                            numberOfKeyWords, 
                            height, 
                            averageStmtsMethodBody, 
                            typeAnnotationsPct, 
                            privateMethodsPct, 
                            magicMethodsPct, 
                            asyncMethodsPct, 
                            classMethodsPct, 
                            staticMethodsPct, 
                            abstractMethodsPct, 
                            propertyMethodsPct,
                            sourceCode, 
                            module_id,
                            parent_id,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.classdef_id,
                            node.nameConvention, 
                            node.isEnumClass, 
                            node.numberOfCharacters, 
                            node.numberOfDecorators, 
                            node.numberOfMethods,
                            node.numberOfBaseClasses, 
                            node.hasGenericTypeAnnotations, 
                            node.hasDocString, 
                            node.bodyCount, 
                            node.assignmentsPct, 
                            node.expressionsPct, 
                            node.usesMetaclass, 
                            node.numberOfKeyWords, 
                            node.height, 
                            node.averageStmtsMethodBody, 
                            node.typeAnnotationsPct, 
                            node.privateMethodsPct, 
                            node.magicMethodsPct, 
                            node.asyncMethodsPct, 
                            node.classMethodsPct, 
                            node.staticMethodsPct, 
                            node.abstractMethodsPct, 
                            node.propertyMethodsPct,
                            node.sourceCode, 
                            node.module_id,
                            node.parent_id,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_MethodDef(self, node: db_entities.DBMethodDef):
        sql_insert = '''INSERT INTO MethodDefs (
                            methoddef_id,
                            classdef_id, 
                            isClassMethod, 
                            isStaticMethod, 
                            isConstructorMethod,
                            isAbstractMethod, 
                            isProperty, 
                            isWrapper, 
                            isCached,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.methoddef_id,
                            node.classdef_id, 
                            node.isClassMethod, 
                            node.isStaticMethod, 
                            node.isConstructorMethod,
                            node.isAbstractMethod, 
                            node.isProperty, 
                            node.isWrapper, 
                            node.isCached,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Statement(self, node: db_entities.DBStatement):
        sql_insert = '''INSERT INTO Statements (
                            statement_id,
                            category, 
                            parent, 
                            statementRole, 
                            height, 
                            depth, 
                            sourceCode, 
                            hasOrElse, 
                            bodySize, 
                            first_child_id, 
                            second_child_id, 
                            third_child_id,
                            parent_id,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.statement_id,
                            node.category, 
                            node.parent, 
                            node.statementRole, 
                            node.height, 
                            node.depth, 
                            node.sourceCode, 
                            node.hasOrElse, 
                            node.bodySize, 
                            node.first_child_id, 
                            node.second_child_id, 
                            node.third_child_id,
                            node.parent_id,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
    
    def insert_Case(self, node: db_entities.DBCase):
        sql_insert = '''INSERT INTO Cases (
                            statement_id,
                            numberOfCases, 
                            guards, 
                            averageBodyCount, 
                            averageMatchValue, 
                            averageMatchSingleton, 
                            averageMatchSequence, 
                            averageMatchMapping, 
                            averageMatchClass, 
                            averageMatchStar, 
                            averageMatchAs, 
                            averageMatchOr,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.statement_id,
                            node.numberOfCases, 
                            node.guards, 
                            node.averageBodyCount, 
                            node.averageMatchValue, 
                            node.averageMatchSingleton, 
                            node.averageMatchSequence, 
                            node.averageMatchMapping, 
                            node.averageMatchClass, 
                            node.averageMatchStar, 
                            node.averageMatchAs, 
                            node.averageMatchOr,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Handler(self, node: db_entities.DBHandler):
        sql_insert = '''INSERT INTO Handlers (
                            statement_id,
                            numberOfHandlers, 
                            hasFinally, 
                            hasCatchAll, 
                            averageBodyCount, 
                            hasStar,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.statement_id,
                            node.numberOfHandlers, 
                            node.hasFinally, 
                            node.hasCatchAll, 
                            node.averageBodyCount, 
                            node.hasStar,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Expression(self, node: db_entities.DBExpression):
        sql_insert = '''INSERT INTO Expressions (
                            expression_id,
                            category, 
                            first_child_category, 
                            second_child_category, 
                            third_child_category, 
                            fourth_child_category, 
                            first_child_id, 
                            second_child_id, 
                            third_child_id, 
                            fourth_child_id,
                            parent, 
                            expressionRole, 
                            height, 
                            depth, 
                            sourceCode, 
                            parent_id,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.category, 
                            node.first_child_category, 
                            node.second_child_category, 
                            node.third_child_category, 
                            node.fourth_child_category, 
                            node.first_child_id,
                            node.second_child_id,
                            node.third_child_id,
                            node.fourth_child_id,
                            node.parent, 
                            node.expressionRole, 
                            node.height, 
                            node.depth, 
                            node.sourceCode, 
                            node.parent_id,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)

    def insert_Comprehension(self, node: db_entities.DBComprehension):
        sql_insert = '''INSERT INTO Comprehensions (
                            expression_id,
                            category, 
                            numberOfIfs, 
                            numberOfGenerators, 
                            isAsync,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.category, 
                            node.numberOfIfs, 
                            node.numberOfGenerators, 
                            node.isAsync,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_FString(self, node: db_entities.DBFString):
        sql_insert = '''INSERT INTO FStrings (
                            expression_id,
                            numberOfElements, 
                            constantsPct, 
                            expressionsPct,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.numberOfElements, 
                            node.constantsPct, 
                            node.expressionsPct,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_CallArg(self, node: db_entities.DBCallArg):
        sql_insert = '''INSERT INTO CallArgs (
                            expression_id,
                            numberArgs, 
                            namedArgsPct, 
                            doubleStarArgsPct,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.numberArgs, 
                            node.namedArgsPct, 
                            node.doubleStarArgsPct,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
    
    def insert_Variable(self, node: db_entities.DBVariable):
        sql_insert = '''INSERT INTO Variables (
                            expression_id,
                            nameConvention, 
                            numberOfCharacters, 
                            isPrivate,
                            isMagic,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.nameConvention, 
                            node.numberOfCharacters, 
                            node.isPrivate,
                            node.isMagic,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Vector(self, node: db_entities.DBVector):
        sql_insert = '''INSERT INTO Vectors (
                            expression_id,
                            category,
                            numberOfElements,
                            homogeneous,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.category,
                            node.numberOfElements,
                            node.homogeneous,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Parameter(self, node: db_entities.DBParameter):
        sql_insert = '''INSERT INTO Parameters (
                            parameters_id,
                            parent_id,
                            parametersRole,
                            numberOfParams, 
                            posOnlyParamPct, 
                            varParamPct, 
                            hasVarParam, 
                            typeAnnotationPct, 
                            kwOnlyParamPct, 
                            defaultValuePct, 
                            hasKWParam, 
                            nameConvention,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.parameters_id,
                            node.parent_id,
                            node.parametersRole,
                            node.numberOfParams, 
                            node.posOnlyParamPct, 
                            node.varParamPct, 
                            node.hasVarParam, 
                            node.typeAnnotationPct, 
                            node.kwOnlyParamPct, 
                            node.defaultValuePct, 
                            node.hasKWParam, 
                            node.nameConvention,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)