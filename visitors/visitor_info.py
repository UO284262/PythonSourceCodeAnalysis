import ast
import re
from typing import Dict, Self
import uuid
import util.util as util
from visitors.My_NodeVisitor import NodeVisitor
from visitors.visitor import Visitor
import db.dbentities as dbentities
import visitors.visitor_db as visitor_db

def what_it_is(method):
    what_it_is = {'magic' : False, 'private' : False, 'abstract' : False, 'wrapper' : False, 'cached' : False, 'static' : False, 'classmethod' : False, 'property' : False}
    magic_patron = re.compile(r'^__\w+__$')
    private_patron = re.compile(r'^_\w+$')
    what_it_is.magic = magic_patron.match(method.name)
    what_it_is.private = private_patron.match(method.name)
    for decorator in method.decorator_list:
        if(decorator.id == "abstractmethod"): what_it_is.abstract = True
        if(decorator.id == "wraps"): what_it_is.wrapper = True
        if(decorator.id == "cache"): what_it_is.cached = True
        if(decorator.id == "staticmethod"): what_it_is.static = True
        if(decorator.id == "classmethod"): what_it_is.classmethod = True
        if(decorator.id == "property"): what_it_is.property = True
    return what_it_is

def addParam(self : Dict, param, value):
    new_dict = self.copy()
    new_dict[param] = value
    return new_dict

Dict.addParam = addParam

class Visitor_info(NodeVisitor):

    # params = [parent, parent_id = node]
    def visit_Expr(self: Self, node : ast.Expr, params : Dict):
        return self.visit(node.value, params)

    def visit_Module(self : Self, node : ast.Module , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        module = dbentities.DBModule()
        imports = dbentities.DBImport()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = module.module_id = id
        ############# PARAMS #####################
        childparams = {"parent" : module, "depth" : 1, "parent_id" : id, "role" : "Module"}
        ############## PROPAGAR VISIT ############
        for child in node.body:
            retnode = self.visit(child, childparams)
        ########## ENTITIE PROPERTIES ############
        
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : module, 'dbnode' : dbnode})
        return
    
    def visit_FunctionDef(self : Self, node : ast.FunctionDef , params : Dict) -> None: 
        isMethod = params.parent.table == 'ClassDefs'
        dbnode = dbentities.DBNode()
        function = dbentities.DBFunctionDef()
        if(isMethod): method = dbentities.DBMethodDef()
        dbparams = dbentities.DBParameter()
        ############ IDS #########################
        id = uuid.uuid4().int
        params_id = uuid.uuid4().int
        dbparams.parameters_id = function.parameters_id = params_id
        dbnode.node_id = function.functiondef_id = id
        dbnode.parent_id = function.module_id = params.parent_id
        if(isMethod):
            method.classdef_id = params.parent_id
            method.methoddef_id = id
        ############# PARAMS #####################
        childparams = {"parent" : function, "depth" : params.depth + 1, "parent_id" : id}
        if(isMethod):
            stmtRoles = ["MethodDef"]
            exprRoles = ["FuncDecorator", "ReturnType", "MethodBody"]
        else:
            stmtRoles = ["FunctionDef"]
            exprRoles = ["FuncDecorator", "ReturnType", "FuncBody"]
        ########## ENTITIE PROPERTIES ############
        numberOfBodyExpr = 0
        ############## PROPAGAR VISIT ############
        args = self.visit(node.args, {"parent": function, "depth": params.depth + 1, "params_id": params_id, "dbparams": dbparams})
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
                numberOfBodyExpr += 1
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.decorator_list:
            self.visit(child, childparams.addParam("role", exprRoles[0]))
        if(node.returns):
            self.visit(node.returns, childparams.addParam("role", exprRoles[1]))
        for child in node.type_params:
            self.visit(child, childparams)
        ########## ENTITIE PROPERTIES ############
        whatitis = what_it_is(node)
        function.isPrivate = whatitis.private
        function.isMagic = whatitis.magic
        function.bodyCount = len(node.body)
        function.isAsync = False
        function.numberOfDecorators = len(node.decorator_list)
        function.hasReturnTypeAnnotation = node.returns
        if(node.returns): args.typeAnnotations += 1
        function.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        function.height = params.depth
        function.typeAnnotationsPct = args.typeAnnotations/(args.numberOfArgs + 1)
        function.sourceCode = ast.unparse(node)
        if(isMethod):
            method.isClassMethod = whatitis.classmethod
            method.isStaticMethod = whatitis.static
            method.isConstructorMethod = node.name == '__init__'
            method.isAbstractMethod = whatitis.abstract
            method.isProperty = whatitis.property
            method.isWrapper = whatitis.wrapper
            method.isCached = whatitis.cached
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : function, 'dbnode' : dbnode, 'dbparams': dbparams})
        if(isMethod):
            return {'method': method, 'function': function, 'args': args}
        else:
            return{'node': function}
    
    def visit_AsyncFunctionDef(self : Self, node : ast.AsyncFunctionDef , params : Dict) -> None: 
        isMethod = params.parent.table == 'ClassDefs'
        dbnode = dbentities.DBNode()
        function = dbentities.DBFunctionDef()
        if(isMethod): method = dbentities.DBMethodDef()
        dbparams = dbentities.DBParameter()
        ############ IDS #########################
        id = uuid.uuid4().int
        params_id = uuid.uuid4().int
        dbparams.parameters_id = function.parameters_id = params_id
        dbnode.node_id = function.functiondef_id = id
        dbnode.parent_id = function.module_id = params.parent_id
        if(isMethod):
            method.classdef_id = params.parent_id
            method.methoddef_id = id
        ############# PARAMS #####################
        childparams = {"parent" : function, "depth" : params.depth + 1, "parent_id" : id}
        if(isMethod):
            stmtRoles = ["AsyncMethodDef"]
            exprRoles = ["FuncDecorator", "ReturnType", "MethodBody"]
        else:
            stmtRoles = ["AsyncFunctionDef"]
            exprRoles = ["FuncDecorator", "ReturnType", "FuncBody"]
        ########## ENTITIE PROPERTIES ############
        numberOfBodyExpr = 0
        ############## PROPAGAR VISIT ############
        args = self.visit(node.args, {"parent": function, "depth": params.depth + 1, "params_id": params_id, "dbparams": dbparams})
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
                numberOfBodyExpr += 1
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.decorator_list:
            self.visit(child, childparams.addParam("role", exprRoles[0]))
        if(node.returns):
            self.visit(node.returns, childparams.addParam("role", exprRoles[1]))
        for child in node.type_params:
            self.visit(child, childparams)
        ########## ENTITIE PROPERTIES ############
        whatitis = what_it_is(node)
        function.isPrivate = whatitis.private
        function.isMagic = whatitis.magic
        function.bodyCount = len(node.body)
        function.isAsync = True
        function.numberOfDecorators = len(node.decorator_list)
        function.hasReturnTypeAnnotation = node.returns
        if(node.returns): args.typeAnnotations += 1
        function.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        function.height = params.depth
        function.typeAnnotationsPct = args.typeAnnotations/(args.numberOfArgs + 1)
        function.sourceCode = ast.unparse(node)
        if(isMethod):
            method.isClassMethod = whatitis.classmethod
            method.isStaticMethod = whatitis.static
            method.isConstructorMethod = node.name == '__init__'
            method.isAbstractMethod = whatitis.abstract
            method.isProperty = whatitis.property
            method.isWrapper = whatitis.wrapper
            method.isCached = whatitis.cached
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : function, 'dbnode' : dbnode, 'dbparams': dbparams})
        if(isMethod):
            return {'method': method, 'function': function, 'args': args}
        else:
            return{'node': function}
        
    def visit_ClassDef(self : Self, node : ast.ClassDef , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        classdef = dbentities.DBClassDef()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = classdef.classdef_id = id
        dbnode.parent_id = classdef.module_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : classdef, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["ClassDef"]
        exprRoles = ["ClassBase", "ClassDecorator", "ClassBody"]
        ########## ENTITIE PROPERTIES ############
        numberOfMethods = 0
        bodyCount = len(node.body)
        assignmentNumber = 0
        expressionNumber = 0
        metaclassNumber = 0
        keywordNumber = 0
        numberOfMethodStmt = 0
        numberOfPrivateMethods = 0
        numberOfMethodTypeAnnotations = 0
        numberOfMethodParamsRet = 0
        numberOfMagicMethods = 0
        numberOfAsyncMethods = 0
        numberOfClassMethods = 0
        numberOfStaticMethods = 0
        numberOfAbstractMethods = 0
        numberOfPropertyMethods = 0
        ############## PROPAGAR VISIT ############
        for child in node.bases:
            self.visit(child, childparams.addParam("role", exprRoles[0]))
            classdef.isEnumClass = (child.id == 'Enum')
        for child in node.keywords:
            if(child.arg == 'metaclass'): metaclassNumber += 1
            else : keywordNumber += 1
            self.visit(child, childparams)
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                expressionNumber += 1
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                if(isinstance(child, ast.AnnAssign) or isinstance(child, ast.AugAssign) or isinstance(child, ast.Assign)): assignmentNumber += 1
                returns = self.visit(child, childparams.addParam("role", stmtRoles[0]))
                if(isinstance(child,ast.FunctionDef) or isinstance(child,ast.AsyncFunctionDef)):
                    numberOfMethods += 1
                    numberOfMethodStmt += returns.function.bodyCount
                    numberOfMethodParamsRet += (returns.args.numberOfArgs + 1)
                    numberOfMethodTypeAnnotations += returns.args.typeAnnotations
                    if(returns.function.isMagic): numberOfMagicMethods += 1
                    if(returns.function.isPrivate): numberOfPrivateMethods += 1
                    if(returns.function.isAsync): numberOfAsyncMethods += 1
                    if(returns.method.isAbstractMethod): numberOfAbstractMethods += 1
                    if(returns.method.isClassMethod): numberOfClassMethods += 1
                    if(returns.method.isStaticMethod): numberOfStaticMethods += 1
                    if(returns.method.isProperty): numberOfPropertyMethods += 1
        for child in node.decorator_list:
            self.visit(child, childparams.addParam("role", exprRoles[1]))
        for child in node.type_params:
            self.visit(child, childparams)
        ########## ENTITIE PROPERTIES ############
        classdef.numberOfMethods = numberOfMethods
        classdef.numberOfDecorators = len(node.decorator_list)
        classdef.numberOfBaseClasses = len(node.bases)
        classdef.hasGenericTypeAnnotations = len(node.type_params) > 0
        classdef.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        classdef.bodyCount = bodyCount
        classdef.assignmentsPct = assignmentNumber/bodyCount
        classdef.expressionsPct = expressionNumber/bodyCount
        classdef.usesMetaclass = metaclassNumber > 0
        classdef.numberOfKeyWords = keywordNumber
        classdef.height = params.depth
        classdef.averageStmtsMethodBody = numberOfMethodStmt/numberOfMethods
        classdef.typeAnnotationsPct = numberOfMethodTypeAnnotations/numberOfMethodParamsRet
        classdef.privateMethodsPct = numberOfPrivateMethods/numberOfMethods
        classdef.magicMethodsPct = numberOfMagicMethods/numberOfMethods
        classdef.asyncMethodsPct = numberOfAsyncMethods/numberOfMethods
        classdef.classMethodsPct = numberOfClassMethods/numberOfMethods
        classdef.staticMethodsPct = numberOfStaticMethods/numberOfMethods
        classdef.abstractMethodsPct = numberOfAbstractMethods/numberOfMethods
        classdef.propertyMethodsPct = numberOfPropertyMethods/numberOfMethods
        classdef.sourceCode = ast.unparse(node)
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : classdef, 'dbnode' : dbnode})
        return

    ############################### STATEMENTS #############################

    def visit_Return(self : Self, node : ast.Return , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id, "role" : "Return"}
        ############## PROPAGAR VISIT ############
        if(node.value): self.visit(node.value, childparams)
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    def visit_Delete(self : Self, node : ast.Delete , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id, "role" : "Delete"}
        ############## PROPAGAR VISIT ############
        for child in node.targets:
            self.visit(child, childparams)
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    def visit_Assign(self : Self, node : ast.Assign , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = "AssignmentStmt"
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        roles = ["AssignLHS", "AssignRHS"]
        ############## PROPAGAR VISIT ############
        for child in node.targets:
            self.visit(child, childparams.addParam('role',roles[0]))
        self.visit(node.value, childparams.addParam('role',roles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return
    
    def visit_TypeAlias(self : Self, node : ast.TypeAlias , params : Dict) -> None:
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        roles = ["TypeAliasLHS", "TypeAliasRHS"]
        ############## PROPAGAR VISIT ############
        for child in node.type_params:
            self.visit(child, childparams)
        self.visit(node.name, childparams.addParam('role', roles[0]))
        self.visit(node.value, childparams.addParam('role', roles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return
    
    def visit_AugAssign(self : Self, node : ast.AugAssign , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = "AugmentedAssignment"
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        roles = ["AugmentedAssigmentLHS", "AugmentedAssigmentRHS"]
        ############## PROPAGAR VISIT ############
        self.visit(node.target, childparams.addParam('role', roles[0]))
        self.visit(node.value, childparams.addParam('role', roles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    def visit_AnnAssign(self : Self, node : ast.AnnAssign , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = "AnnotatedAssignment"
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        roles = ["VarDefVarName", "VarDefType", "VarDefInitValue"]
        ############## PROPAGAR VISIT ############
        self.visit(node.target, childparams.addParam('role', roles[0]))
        self.visit(node.annotation, childparams.addParam('role', roles[1]))
        if(node.value): self.visit(node.value, childparams.addParam('role', roles[2]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    def visit_For(self : Self, node : ast.For , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["For", "ForElse"]
        exprRoles = ["ForElement", "ForEnumerable", "ForBody", "ForElseBody"]
        ############## PROPAGAR VISIT ############
        self.visit(node.target, childparams.addParam('role', exprRoles[0]))
        self.visit(node.iter, childparams.addParam('role', exprRoles[1]))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[3]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_AsyncFor(self : Self, node : ast.AsyncFor , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = "For"
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["AsyncFor", "AsyncForElse"]
        exprRoles = ["AsyncForElement", "AsyncForEnumerable", "AsyncForBody", "AsyncForElseBody"]
        ############## PROPAGAR VISIT ############
        self.visit(node.target, childparams.addParam('role', exprRoles[0]))
        self.visit(node.iter, childparams.addParam('role', exprRoles[1]))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[3]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_While(self : Self, node : ast.While , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["While", "WhileElse"]
        exprRoles = ["WhileCondition", "WhileBody", "WhileElseBody"]
        ############## PROPAGAR VISIT ############
        self.visit(node.test, childparams.addParam('role', exprRoles[0]))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[1]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_If(self : Self, node : ast.If , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["If", "IfElse"]
        exprRoles = ["IfCondition", "IfBody", "IfElseBody"]
        ############## PROPAGAR VISIT ############
        self.visit(node.test, childparams.addParam('role', exprRoles[0]))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[1]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_With(self : Self, node : ast.With , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["With"]
        exprRoles = ["WithElement", "WithAs", "WithBody"]
        ############## PROPAGAR VISIT ############
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.items:
            self.visit(child, childparams.addParam("role_ctx", exprRoles[0]).addParam('role_vars', exprRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_AsyncWith(self : Self, node : ast.AsyncWith , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["AsyncWith"]
        exprRoles = ["AsyncWithElement", "AsyncWithAs", "AsyncWithBody"]
        ############## PROPAGAR VISIT ############
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.items:
            self.visit(child, childparams.addParam("role_ctx", exprRoles[0]).addParam('role_vars', exprRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_Match(self : Self, node : ast.Match , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["MatchCondition"]
        ############## PROPAGAR VISIT ############
        self.visit(node.subject, childparams.addParam('role', exprRoles[0]))
        for child in node.cases:
            self.visit(child, childparams)
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_Raise(self : Self, node : ast.Raise , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Raise","RaiseFrom"]
        ############## PROPAGAR VISIT ############
        if(node.exc): self.visit(node.exc, childparams.addParam('role', exprRoles[0]))
        if(node.cause): self.visit(node.cause, childparams.addParam('role', exprRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return
    
    def visit_Try(self : Self, node : ast.Try , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["Try", "TryElse", "TryFinally", "TryHandler"]
        exprRoles = ["TryBody", "TryElse", "FinallyBody"]
        ############## PROPAGAR VISIT ############
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[0]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[1]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[1]))
        for child in node.finalbody:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[2]))
        for child in node.handlers:
            self.visit(child, childparams.addParam("role", stmtRoles[3]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_TryStar(self : Self, node : ast.TryStar , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = "Try"
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["Try", "TryElse", "TryFinally", "TryHandlerStar"]
        exprRoles = ["TryBody", "TryElse", "FinallyBody"]
        ############## PROPAGAR VISIT ############
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[0]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[1]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[1]))
        for child in node.finalbody:
            if(isinstance(child,ast.Expr)):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[2]))
        for child in node.handlers:
            self.visit(child, childparams.addParam("role", stmtRoles[3]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_Assert(self : Self, node : ast.Assert , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES #######################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["AssertCondition", "AssertMessage"]
        ############## PROPAGAR VISIT ############
        self.visit(node.test, childparams.addParam('role', exprRoles[0]))
        if(node.msg): self.visit(node.msg, childparams.addParam('role', exprRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_Global(self : Self, node : ast.Global , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_Nonlocal(self : Self, node : ast.Nonlocal , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_Pass(self : Self, node : ast.Pass , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_Break(self : Self, node : ast.Break , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    
    def visit_Continue(self : Self, node : ast.Continue , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = stmt.statement_id = id
        dbnode.parent_id = stmt.parent_id = params.parent_id
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        stmt.parent = params.parent.category
        ############# ROLES ######################
        stmt.statementRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : stmt, 'dbnode' : dbnode})
        return

    ############################ IMPORTS ##################################

    
    def visit_Import(self : Self, node : ast.Import , params : Dict) -> None: 
        dbnode = dbentities.DBImport()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.import_id = params.parent.import_id = id
        ########## ENTITIE PROPERTIES ############
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return

    
    def visit_ImportFrom(self : Self, node : ast.ImportFrom , params : Dict) -> None: 
        dbnode = dbentities.DBImport()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.import_id = params.parent.import_id = id
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return

    ############################ EXPRESSIONS ##################################

    def visit_BoolOp(self : Self, node : ast.BoolOp , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "Logical"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Logical"]
        ############## PROPAGAR VISIT ############
        self.visit(node.op, childparams)
        for child in node.values:
            self.visit(child, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    
    def visit_NamedExpr(self : Self, node : ast.NamedExpr , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES #######################
        expr.category = "AssignmentExp"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["AssignExpLHS", "AssignExpRHS"]
        ############## PROPAGAR VISIT ############
        self.visit(node.target, childparams.addParam('role', exprRoles[0]))
        self.visit(node.value, childparams.addParam('role', exprRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    
    def visit_BinOp(self : Self, node : ast.BinOp , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = util.opCategory(node)
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Arithmetic", "Shift", "Pow", "MatMult", "BWLogical"]
        ############## PROPAGAR VISIT ############
        self.visit(node.op, childparams)
        match node.op:
            case ast.MatMult: role = exprRoles[3]
            case ast.LShift, ast.RShift: role = exprRoles[1]
            case ast.Pow: role = exprRoles[2]
            case ast.BitAnd, ast.BitOr, ast.BitXor: role = exprRoles[4]
            case default: role = exprRoles[0]
        self.visit(node.left, childparams.addParam('role', role))
        self.visit(node.right, childparams.addParam('role', role))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return
    
    
    def visit_UnaryOp(self : Self, node : ast.UnaryOp , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = util.opCategory(node)
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Arithmetic"]
        ############## PROPAGAR VISIT ############
        self.visit(node.op, childparams)
        self.visit(node.operand, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return
    
    
    def visit_Lambda(self : Self, node : ast.Lambda , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["LambdaBody"]
        ############## PROPAGAR VISIT ############
        self.visit(node.args, childparams)
        for child in node.body:
            self.visit(child, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return
    
    
    def visit_Ifexp(self : Self, node : ast.IfExp , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "Ternary"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############ PARAMS ######################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["TernaryCondition", "TernaryIfBody", "TernaryElseBody"]
        ############## PROPAGAR VISIT ############
        self.visit(node.test, childparams.addParam('role', exprRoles[0]))
        self.visit(node.body, childparams.addParam('role', exprRoles[1]))
        self.visit(node.orelse, childparams.addParam('role', exprRoles[2]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    ######################### COMPREHENSIONS #############################

    
    def visit_ListComp(self : Self, node : ast.ListComp , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = comp.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category, comp.category = "ListComprehension"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["ComprenhensionElement"]
        ############## PROPAGAR VISIT ############
        for child in node.generators:
            self.visit(child, childparams)
        self.visit(node.elt, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : comp, 'dbnode' : dbnode, 'expr': expr})
        return

    
    def visit_SetComp(self : Self, node : ast.SetComp , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = comp.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category, comp.category = "SetComprehension"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["ComprenhensionElement"]
        ############## PROPAGAR VISIT ############
        for child in node.generators:
            self.visit(child, childparams)
        self.visit(node.elt, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : comp, 'dbnode' : dbnode, 'expr': expr})
        return

    
    def visit_DictComp(self : Self, node : ast.DictComp , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = comp.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category, comp.category = "DictComprehension"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["DictionaryLiteralKey", "DictionaryLiteralValue"]
        ############## PROPAGAR VISIT ############
        for child in node.generators:
            self.visit(child, childparams)
        self.visit(node.key, childparams.addParam('role', exprRoles[0]))
        self.visit(node.value, childparams.addParam('role', exprRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : comp, 'dbnode' : dbnode, 'expr': expr})
        return

    
    def visit_GeneratorExp(self : Self, node : ast.GeneratorExp , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = comp.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category, comp.category = "GeneratorComprehension"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["ComprenhensionElement"]
        ############## PROPAGAR VISIT ############
        for child in node.generators:
            self.visit(child, childparams)
        self.visit(node.elt, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : comp, 'dbnode' : dbnode, 'expr': expr})
        return

    ######################################################################

    
    def visit_Await(self : Self, node : ast.Await , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Await"]
        ############## PROPAGAR VISIT ############
        self.visit(node.value, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    
    def visit_Yield(self : Self, node : ast.Yield , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Yield"]
        ############## PROPAGAR VISIT ############
        if(node.value): self.visit(node.value, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    
    def visit_YieldFrom(self : Self, node : ast.YieldFrom , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["YieldFrom"]
        ############## PROPAGAR VISIT ############
        self.visit(node.value, childparams.addParam('role', exprRoles[0]))
         ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    
    def visit_Compare(self : Self, node : ast.Compare , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Compare", "Relational", "Is", "In"]
        ############## PROPAGAR VISIT ############
        self.visit(node.left, childparams.addParam('role', exprRoles[0]))
        index = 0
        for child in node.comparators:
            match node.ops[index]:
                case ast.Is, ast.IsNot: self.visit(child, childparams.addParam('role', exprRoles[2]))
                case ast.In: self.visit(child, childparams.addParam('role', exprRoles[3]))
                case default: self.visit(child, childparams.addParam('role', exprRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    ########################## call_args ###########################

    
    def visit_Call(self : Self, node : ast.Call , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        callArgs = dbentities.DBCallArg()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = callArgs.expression_id = id
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["CallFuncName", "CallArg"]
        ############## PROPAGAR VISIT ############
        for child in node.args:
            self.visit(child, childparams.addParam('role', exprRoles[1]))
        self.visit(node.func, childparams.addParam('role', exprRoles[0]))
        for child in node.keywords:
            self.visit(child, childparams)
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : callArgs, 'dbnode' : dbnode, 'expr' : expr})
        return

    ################################################################

    def visit_formattedvalue(self : Self, node : ast.FormattedValue , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["FormattedValue", "FormattedFormat"]
        ############## PROPAGAR VISIT ############
        self.visit(node.value, childparams.addPamam('role', exprRoles[0]))
        if(node.format_spec): self.visit(node.format_spec, childparams.addParam('role', exprRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    ########################### F-strings #####################################

    
    def visit_JoinedStr(self : Self, node : ast.JoinedStr , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        fstr = dbentities.DBFString()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = fstr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "FString"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["FString"]
        ############## PROPAGAR VISIT ############
        for child in node.values:
            self.visit(child, childparams.addParam('node', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : fstr, 'dbnode' : dbnode, 'expr' : expr})
        return

    ###########################################################################

    
    def visit_Constant(self : Self, node : ast.Constant , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = util.constCategory(node)
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    
    def visit_Attribute(self : Self, node : ast.Attribute , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "Dot"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Dot"]
        ############## PROPAGAR VISIT ############
        self.visit(node.value, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    
    def visit_Subscript(self : Self, node : ast.Subscript , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "Indexing"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Slice", "Indexing"]
        ############## PROPAGAR VISIT ############
        self.visit(node.value, childparams.addParam('role', exprRoles[1]))
        self.visit(node.slice, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    
    def visit_Starred(self : Self, node : ast.Starred , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "Star"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Star"]
        ############## PROPAGAR VISIT ############
        self.visit(node.value, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    ############################# Variable ##################################

    
    def visit_Name(self : Self, node : ast.Name , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        var = dbentities.DBVariable()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = var.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "Variable"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : var, 'dbnode' : dbnode, 'expr' : expr})
        return

    ############################### Vectors #################################

    
    def visit_List(self : Self, node : ast.List , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = vct.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "ListLiteral"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["ListLiteral"]
        ############## PROPAGAR VISIT ############
        for child in node.elts:
            self.visit(child, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : vct, 'dbnode' : dbnode, 'expr' : expr})
        return

    
    def visit_Tuple(self : Self, node : ast.Tuple , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = vct.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "TupleLiteral"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["TupleLiteral"]
        ############## PROPAGAR VISIT ############
        for child in node.elts:
            self.visit(child, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : vct, 'dbnode' : dbnode, 'expr' : expr})
        return

    
    def visit_Dict(self : Self, node : ast.Dict , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = vct.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "DictionaryLiteral"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["DictionaryLiteralKey", "DictionaryLiteralValue"]
        ############## PROPAGAR VISIT ############
        for child in node.keys:
            self.visit(child, childparams.addParam('role', exprRoles[0]))
        for child in node.values:
            self.visit(child, childparams.addParam('role', exprRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : vct, 'dbnode' : dbnode, 'expr' : expr})
        return

    
    def visit_Set(self : Self, node : ast.Set , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = vct.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = "SetLiteral"
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["SetLiteral"]
        ############## PROPAGAR VISIT ############
        for child in node.elts:
            self.visit(child, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : vct, 'dbnode' : dbnode, 'expr' : expr})
        return

    ########################################################################

    
    def visit_Slice(self : Self, node : ast.Slice , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        dbnode.parent_table = params.parent.table
        expr.parent = params.parent.category
        ############# ROLES ######################
        expr.expressionRole = params.role
        ############# PARAMS #####################
        childparams = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["Slice"]
        ############## PROPAGAR VISIT ############
        if(node.lower): self.visit(node.lower, childparams.addParam('role', exprRoles[0]))
        if(node.upper): self.visit(node.upper, childparams.addParam('role', exprRoles[0]))
        if(node.step): self.visit(node.step, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : expr, 'dbnode' : dbnode})
        return

    ############################### Cases ###################################

    
    def visit_MatchValue(self : Self, node : ast.MatchValue , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["MatchCondition"]
        ############## PROPAGAR VISIT ############
        self.visit(node.value, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return

    
    def visit_MatchSingleton(self : Self, node : ast.MatchSingleton , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return

    
    def visit_MatchSequence(self : Self, node : ast.MatchSequence , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return

    
    def visit_MatchMapping(self : Self, node : ast.MatchMapping , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["MatchCondition"]
        ############## PROPAGAR VISIT ############
        for child in node.keys:
            self.visit(child, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return

    
    def visit_MatchClass(self : Self, node : ast.MatchClass , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["MatchCondition"]
        ############## PROPAGAR VISIT ############
        self.visit(node.cls, childparams.addParam('role', exprRoles[0]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return

    
    def visit_MatchStar(self : Self, node : ast.MatchStar , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return

    
    def visit_MatchAs(self : Self, node : ast.MatchAs , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return

    
    def visit_MatchOr(self : Self, node : ast.MatchOr , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return
    
    ############################# HANDLER ####################################

    def visit_ExceptHandler(self : Self, node : ast.ExceptHandler , params : Dict) -> None: 
        dbnode = dbentities.DBHandler()
        ############ IDS #########################
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        exprRoles = ["ExceptType", "ExceptBody"]
        ############## PROPAGAR VISIT ############
        if(node.type): self.visit(node.type, childparams.addParam('role', exprRoles[0]))
        for child in node.body:
            self.visit(child, childparams.addParam('role', exprRoles[1]))
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : dbnode})
        return

    ####################### Visits extra ######################

    def visit_Comprehension(self : Self, node : ast.comprehension , params : Dict) -> None: 
        ############# PARAMS #####################
        exprRoles = ["ComprehensionTarget", "ComprehensionIter", "ComprehensionIf"]
        ############## PROPAGAR VISIT ############
        self.visit(node.target, params.addParam('role', exprRoles[0]))
        self.visit(node.iter, params.addParam('role', exprRoles[1]))
        for child in node.ifs:
            self.visit(child, params.addParam('role', exprRoles[2]))
        return
    
    def visit_Arguments(self : Self, node : ast.arguments , params : Dict) -> None: 
        ############# PARAMS #####################
        exprRoles = ["ArgumentDefault"]
        ########## ENTITIE PROPERTIES ############
        numberOfAnnotations = 0
        numberOfParams = 0
        ############## PROPAGAR VISIT ############
        for child in node.posonlyargs:
            arg = self.visit(child, params)
            if(arg.typeAnnotation): numberOfAnnotations += 1
            numberOfParams += 1
        for child in node.args:
            arg =  self.visit(child, params)
            if(arg.typeAnnotation): numberOfAnnotations += 1
            numberOfParams += 1
        if(node.vararg): 
            arg =  self.visit(node.vararg, params)
            if(arg.typeAnnotation): numberOfAnnotations += 1
            numberOfParams += 1
        for child in node.kwonlyargs:
            arg =  self.visit(child, params)
            if(arg.typeAnnotation): numberOfAnnotations += 1
            numberOfParams += 1
        for child in node.kw_defaults:
            self.visit(child, params.addParam('role', exprRoles[0]))
        if(node.kwarg):
            arg = self.visit(node.kwarg, params)
            if(arg.typeAnnotation): numberOfAnnotations += 1
            numberOfParams += 1
        for child in node.defaults:
            self.visit(child, params.addParam('role', exprRoles[0]))
        return {"typeAnnotations" : numberOfAnnotations, "numberOfArgs" : numberOfParams}
    
    def visit_Arg(self : Self, node : ast.arg , params : Dict) -> None:
        ############# PARAMS ##################### 
        exprRoles = ["ArgumentAnnotation"]
        ############## PROPAGAR VISIT ############
        if(node.annotation): 
            self.visit(node.annotation, params.addParam('role', exprRoles[0]))
            return {'typeAnnotation' : True}
        return {'typeAnnotation' : False}
    
    def visit_Keyword(self : Self, node : ast.keyword , params : Dict) -> None: 
        ############## PROPAGAR VISIT ############
        self.visit(node.value, params)
        return
    
    def visit_Withitem(self : Self, node : ast.withitem , params : Dict) -> None: 
        ############# PARAMS #####################
        childparams = {"parent" : params.dbnode, "depth" : params.depth, "parent_id" : params.parent_id}
        ############## PROPAGAR VISIT ############
        self.visit(node.context_expr, childparams.addParam('role', params.role_ctx))
        if(node.optional_vars): self.visit(node.optional_vars, childparams.addParam('role', params.role_vars))
        return
    
    def visit_Match_case(self : Self, node : ast.match_case , params : Dict) -> None: 
        ############# PARAMS #####################
        stmtRoles = ["Case"]
        exprRoles = ["CaseGuard", "CaseBody"]
        ############## PROPAGAR VISIT ############
        self.visit(node.pattern, params)
        if(node.guard): self.visit(node.guard, params.addParam('role', exprRoles[0]))
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                self.visit(child, params.addParam("role", exprRoles[1]))
            else:
                self.visit(child, params.addParam("role", stmtRoles[0]))
        return
    
    def visit_TypeVar(self : Self, node : ast.TypeVar , params : Dict) -> None: 
        ############# PARAMS #####################
        exprRoles = ["TypeVar"]
        ############## PROPAGAR VISIT ############
        if(node.bound): self.visit(node.bound, params.addParam('role', exprRoles[0]))
        return
    
    def visit_ParamSpec(self : Self, node : ast.ParamSpec , params : Dict) -> None: 
        exprRoles = ["DefaultParamValue"]
        return
    
    def visit_TypeVarTuple(self : Self, node : ast.TypeVarTuple , params : Dict) -> None: 
        exprRoles = ["TypeAnnotation"]
        return
    
    ###########################################################
    