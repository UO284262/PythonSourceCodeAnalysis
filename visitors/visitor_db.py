import ast
from typing import Dict, Self
import uuid
import util.util as util
from visitors.My_NodeVisitor import NodeVisitor
from visitors.visitor import Visitor
import db.dbentities as dbentities
from db.db_utils import writeOnDB

class Visitor_db(NodeVisitor):

    def __init__(self):
        self.sql_insert = []
        self.datos_a_insertar = []
    
    def visit_Module(self, node: dbentities.DBModule, params):
        self.insert_module(params.node)
        writeOnDB(self.sql_insert, self.datos_a_insertar)
        pass
    
    def visit_FunctionDef(self, node: ast.FunctionDef, params):
        self.insert_node(params.dbnode)
        self.insert_functiondef(params.node)
        self.insert_parameter(params.dbparams)
        pass
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef, params):
        self.insert_node(params.dbnode)
        self.insert_functiondef(params.node)
        self.insert_parameter(params.dbparams)
        pass
    
    def visit_ClassDef(self, node: ast.ClassDef, params):
        self.insert_node(params.dbnode)
        self.insert_classdef(params.node)
        pass

    ############################### STATEMENTS #############################
    
    def visit_Return(self, node: ast.Return, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_Delete(self, node: ast.Delete, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_Assign(self, node: ast.Assign, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_TypeAlias(self, node: ast.TypeAlias, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_AugAssign(self, node: ast.AugAssign, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_AnnAssign(self, node: ast.AnnAssign, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_For(self, node: ast.For, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_AsyncFor(self, node: ast.AsyncFor, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_While(self, node: ast.While, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_If(self, node: ast.If, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_With(self, node: ast.With, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_AsyncWith(self, node: ast.AsyncWith, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_Match(self, node: ast.Match, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_Raise(self, node: ast.Raise, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_Try(self, node: ast.Try, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_TryStar(self, node: ast.Try, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_Assert(self, node: ast.Assert, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_Global(self, node: ast.Global, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_NonLocal(self, node: ast.Nonlocal, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_Pass(self, node: ast.Pass, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_Break(self, node: ast.Break, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass
    
    def visit_Continue(self, node: ast.Continue, params):
        self.insert_node(params.dbnode)
        self.insert_statement(params.node)
        pass

    ############################ IMPORTS ##################################
    
    def visit_Import(self, node: ast.Import, params):
        self.insert_import(params.node)
        pass
    
    def visit_ImportFrom(self, node: ast.ImportFrom, params):
        self.insert_import(params.node)
        pass

    ############################ EXPRESSIONS ##################################
    
    def visit_BoolOp(self, node: ast.BoolOp, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_NamedExpr(self, node: ast.NamedExpr, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_BinOp(self, node: ast.BinOp, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_UnaryOp(self, node: ast.UnaryOp, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_Lambda(self, node: ast.Lambda, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_IfExp(self, node: ast.IfExp, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass

    ######################### COMPREHENSIONS #############################
    
    def visit_ListComp(self, node: ast.ListComp, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.expr)
        self.insert_comprehension(params.node)
        pass
    
    def visit_SetComp(self, node: ast.SetComp, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.expr)
        self.insert_comprehension(params.node)
        pass
    
    def visit_DictComp(self, node: ast.DictComp, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.expr)
        self.insert_comprehension(params.node)
        pass
    
    def visit_GeneratorExp(self, node: ast.GeneratorExp, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.expr)
        self.insert_comprehension(params.node)
        pass

    ######################################################################
    
    def visit_Await(self, node: ast.Await, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_Yield(self, node: ast.Yield, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_YieldFrom(self, node: ast.YieldFrom, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_Compare(self, node: ast.Compare, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass

    ########################## call_args ###########################
    
    def visit_Call(self, node: ast.Call, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.expr)
        self.insert_callarg(params.node)
        pass

    ################################################################
    
    def visit_FormattedValue(self, node: ast.FormattedValue, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass

    ########################### F-strings #####################################
    
    def visit_JoinedStr(self, node: ast.JoinedStr, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        self.insert_fstring(params)
        pass

    ###########################################################################
    
    def visit_Constant(self, node: ast.Constant, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_Attribute(self, node: ast.Attribute, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_Subscript(self, node: ast.Subscript, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_Starred(self, node: ast.Starred, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass

    ############################# Variable ##################################
    
    def visit_Name(self, node: ast.Name, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.expr)
        self.insert_variable(params.node)
        pass

    ############################### Vectors #################################
    
    def visit_List(self, node: ast.List, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.expr)
        self.insert_vector(params.node)
        pass
    
    def visit_Tuple(self, node: ast.Tuple, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.expr)
        self.insert_vector(params.node)
        pass
    
    def visit_Dict(self, node: ast.Dict, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.expr)
        self.insert_vector(params.node)
        pass
    
    def visit_Set(self, node: ast.Set, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.expr)
        self.insert_vector(params.node)
        pass

    ########################################################################
    
    def visit_Slice(self, node: ast.Slice, params):
        self.insert_node(params.dbnode)
        self.insert_expression(params.node)
        pass
    
    def visit_ExceptHandler(self, node: ast.ExceptHandler, params):
        self.insert_node(params.node)
        pass

    ############################### Cases ###################################
    
    def visit_MatchValue(self, node: ast.MatchValue, params):
        self.insert_case(params.node)
        pass
    
    def visit_MatchSingleton(self, node: ast.MatchSingleton, params):
        self.insert_case(params.node)
        pass
    
    def visit_MatchSequence(self, node: ast.MatchSequence, params):
        self.insert_case(params.node)
        pass
    
    def visit_MatchMapping(self, node: ast.MatchMapping, params):
        self.insert_case(params.node)
        pass
    
    def visit_MatchClass(self, node: ast.MatchClass, params):
        self.insert_case(params.node)
        pass
    
    def visit_MatchStar(self, node: ast.MatchStar, params):
        self.insert_case(params.node)
        pass
    
    def visit_MatchAs(self, node: ast.MatchAs, params):
        self.insert_case(params.node)
        pass
    
    def visit_MatchOr(self, node: ast.MatchOr, params):
        self.insert_case(params.node)
        pass

    def insert_functiondef(self : Self, node: dbentities.DBFunctionDef):
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
                            parameters_id,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %s, %d, %s, %s, %d, %f, %s, %d, %s, %s, %d, %f, %s, %s, %s, %s, %f);'''
        datos_a_insertar = (node.functiondef_id,
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
                            node.parameters_id,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_module(self : Self, node: dbentities.DBModule):
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
                            userID,
                            experticeLevel) 
                        VALUES (%s, %s, %s, %s, %f, %f, %d, %d, %f, %f, %f, %d, %d, %f, %s, %s, %s, %s, %s, %f);'''
        datos_a_insertar = (node.module_id, 
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
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_node(self : Self, node: dbentities.DBNode):
        sql_insert = '''INSERT INTO Nodes (
                            node_id,
                            parent_table, 
                            parent_id) 
                        VALUES (%s, %s, %s);'''
        datos_a_insertar = (node.node_id,
                            node.parent_table, 
                            node.parent_id)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_import(self : Self, node: dbentities.DBImport):
        sql_insert = '''INSERT INTO Imports (
                            import_id,
                            numberImports,
                            moduleImportsPct, 
                            averageImportedModules, 
                            fromImportsPct,
                            averageFromImportedModules, 
                            averageAsInImportedModules, 
                            localImportsPct,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %d, %f, %d, %f, %d, %d, %f, %s, %f);'''
        datos_a_insertar = (node.import_id,
                            node.numberImports,
                            node.moduleImportsPct, 
                            node.averageImportedModules, 
                            node.fromImportsPct, 
                            node.averageAsInImportedModules, 
                            node.localImportsPct,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_classdef(self : Self, node: dbentities.DBClassDef):
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
                            propertyMethodsPct
                            sourceCode, 
                            module_id,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %s, %s, %d, %d, %d, %d, %s, %s, %d, %f, %f, %s, %d, %d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %s, %s, %s, %f);'''
        datos_a_insertar = (node.classdef_id,
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
                            node.sourceCode, 
                            node.module_id,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_methoddef(self : Self, node: dbentities.DBMethodDef):
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
                            userID,
                            experticeLevel) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %f);'''
        datos_a_insertar = (node.methoddef_id,
                            node.classdef_id, 
                            node.isClassMethod, 
                            node.isStaticMethod, 
                            node.isConstructorMethod,
                            node.isAbstractMethod, 
                            node.isProperty, 
                            node.isWrapper, 
                            node.isCached,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_statement(self : Self, node: dbentities.DBStatement):
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
                            userID,
                            experticeLevel) 
                        VALUES (%s, %s, %s, %s, %d, %d, %s, %s, %d, %s, %s, %s, %s, %s, %f);'''
        datos_a_insertar = (node.statement_id,
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
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
    
    def insert_case(self : Self, node: dbentities.DBCase):
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
                            userID,
                            experticeLevel) 
                        VALUES (%s, %d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %s, %s, %f);'''
        datos_a_insertar = (node.statement_id,
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
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_handler(self : Self, node: dbentities.DBHandler):
        sql_insert = '''INSERT INTO Handlers (
                            statement_id,
                            numberOfHandlers, 
                            hasFinally, 
                            hasCatchAll, 
                            averageBodyCount, 
                            hasStar,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %d, %s, %s, %f, %s, %s, %f);'''
        datos_a_insertar = (node.statement_id,
                            node.numberOfHandlers, 
                            node.hasFinally, 
                            node.hasCatchAll, 
                            node.averageBodyCount, 
                            node.hasStar,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_expression(self : Self, node: dbentities.DBExpression):
        sql_insert = '''INSERT INTO Expressions (
                            expression_id
                            category, 
                            first_child_category, 
                            second_child_category, 
                            third_child_category, 
                            fourth_child_category, 
                            parent, 
                            expressionRole, 
                            height, 
                            depth, 
                            sourceCode, 
                            parent_id,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %s, %s, %s, %f);'''
        datos_a_insertar = (node.expression_id,
                            node.category, 
                            node.first_child_category, 
                            node.second_child_category, 
                            node.third_child_category, 
                            node.fourth_child_category, 
                            node.parent, 
                            node.expressionRole, 
                            node.height, 
                            node.depth, 
                            node.sourceCode, 
                            node.parent_id,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)

    def insert_comprehension(self : Self, node: dbentities.DBComprehension):
        sql_insert = '''INSERT INTO Comprehensions (
                            expression_id,
                            category, 
                            numberOfIfs, 
                            numberOfGenerators, 
                            isAsync,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %s, %d, %d, %s, %s, %f);'''
        datos_a_insertar = (node.expression_id,
                            node.category, 
                            node.numberOfIfs, 
                            node.numberOfGenerators, 
                            node.isAsync,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_fstring(self : Self, node: dbentities.DBFString):
        sql_insert = '''INSERT INTO FStrings (
                            expression_id,
                            numberOfElements, 
                            constantsPct, 
                            expressionsPct,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %d, %f, %f, %s, %f);'''
        datos_a_insertar = (node.expression_id,
                            node.numberOfElements, 
                            node.constantsPct, 
                            node.expressionsPct,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_callarg(self : Self, node: dbentities.DBCallArg):
        sql_insert = '''INSERT INTO CallArgs (
                            expression_id,
                            numberArgs, 
                            namedArgsPct, 
                            doubleStarArgsPct,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %d, %f, %f, %s, %f);'''
        datos_a_insertar = (node.expression_id,
                            node.numberArgs, 
                            node.namedArgsPct, 
                            node.doubleStarArgsPct,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
    
    def insert_variable(self : Self, node: dbentities.DBVariable):
        sql_insert = '''INSERT INTO Variables (
                            expression_id,
                            nameConvention, 
                            numberOfCharacters, 
                            isPrivate,
                            isMagic,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %s, %d, %s, %s, %s, %f);'''
        datos_a_insertar = (node.expression_id,
                            node.nameConvention, 
                            node.numberOfCharacters, 
                            node.isPrivate,
                            node.isMagic,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_vector(self : Self, node: dbentities.DBVector):
        sql_insert = '''INSERT INTO Vectors (
                            expression_id,
                            category,
                            numberOfElements,
                            homogeneous,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %s, %d, %s, %s, %f);'''
        datos_a_insertar = (node.expression_id,
                            node.category,
                            node.numberOfElements,
                            node.homogeneous,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)
        
    def insert_parameter(self : Self, node: dbentities.DBParameter):
        sql_insert = '''INSERT INTO Parameters (
                            parameter_id,
                            numberOfParams, 
                            posOnlyParamPct, 
                            varParamPct, 
                            hasVarParam, 
                            typeAnnotationPct, 
                            kwOnlyParamPct, 
                            defaultValuePct, 
                            hasKWParam, 
                            nameConvention,
                            userID,
                            experticeLevel) 
                        VALUES (%s, %d, %f, %f, %s, %f, %f, %f, %s, %s, %s, %f);'''
        datos_a_insertar = (node.parameter_id,
                            node.numberOfParams, 
                            node.posOnlyParamPct, 
                            node.varParamPct, 
                            node.hasVarParam, 
                            node.typeAnnotationPct, 
                            node.kwOnlyParamPct, 
                            node.defaultValuePct, 
                            node.hasKWParam, 
                            node.nameConvention,
                            node.userId,
                            node.experticeLevel)
        self.sql_insert.append(sql_insert)
        self.datos_a_insertar.append(datos_a_insertar)