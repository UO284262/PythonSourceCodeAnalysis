import ast
from typing import Dict, Self
import uuid
import util.util as util
from visitors.My_NodeVisitor import NodeVisitor
from visitors.visitor import Visitor
import db.dbentities as dbentities
import visitors.visitor_db as visitor_db

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
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = module.module_id = id
        ############# PARAMS #####################
        childparams = {"parent" : module, "depth" : 1, "parent_id" : id, "role" : "Module"}
        ############## PROPAGAR VISIT ############
        for child in node.body:
            self.visit(child, childparams)
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : module, 'dbnode' : dbnode})
        return
    
    def visit_FunctionDef(self : Self, node : ast.FunctionDef , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        function = dbentities.DBFunctionDef()
        method = dbentities.DBMethodDef()
        dbparams = dbentities.DBParameter()
        ############ IDS #########################
        id = uuid.uuid4().int
        params_id = uuid.uuid4().int
        dbparams.parameters_id = function.parameters_id = params_id
        dbnode.node_id = function.functiondef_id = method.methoddef_id = id
        dbnode.parent_id = method.classdef_id = function.module_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : function, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["FunctionDef", "MethodDef"]
        exprRoles = ["FuncDecorator", "ReturnType", "FuncBody", "MethodBody"]
        ############## PROPAGAR VISIT ############
        self.visit(node.args, childparams)
        for child in node.body:
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.decorator_list:
            self.visit(child, childparams.addParam("role", exprRoles[0]))
        if(node.returns):
            self.visit(node.returns, childparams.addParam("role", exprRoles[1]))
        for child in node.type_params:
            self.visit(child, childparams)
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : function, 'dbnode' : dbnode, 'dbparams': dbparams})
        return
    
    def visit_AsyncFunctionDef(self : Self, node : ast.AsyncFunctionDef , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        function = dbentities.DBFunctionDef()
        method = dbentities.DBMethodDef()
        dbparams = dbentities.DBParameter()
        ############ IDS #########################
        id = uuid.uuid4().int
        params_id = uuid.uuid4().int
        dbparams.parameters_id = function.parameters_id = params_id
        dbnode.node_id = function.functiondef_id = method.methoddef_id = id
        dbnode.parent_id = method.classdef_id = function.module_id = params.parent_id
        ############# PARAMS #####################
        childparams = {"parent" : function, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["AsyncFunctionDef", "AsyncMethodDef"]
        exprRoles = ["FuncDecorator", "ReturnType", "FuncBody", "MethodBody"]
        ############## PROPAGAR VISIT ############
        self.visit(node.args, childparams)
        for child in node.body:
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.decorator_list:
            self.visit(child, childparams.addParam("role", exprRoles[0]))
        if(node.returns):
            self.visit(node.returns, childparams.addParam("role", exprRoles[1]))
        for child in node.type_params:
            self.visit(child, childparams)
        ############## VISITOR DB ################
        visitor_db.visit(node, {'node' : function, 'dbnode' : dbnode, 'dbparams': dbparams})
        return

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
        ############## PROPAGAR VISIT ############
        for child in node.bases:
            self.visit(child, childparams.addParam("role", exprRoles[0]))
        for child in node.keywords:
            self.visit(child, childparams)
        for child in node.body:
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.decorator_list:
            self.visit(child, childparams.addParam("role", exprRoles[1]))
        for child in node.type_params:
            self.visit(child, childparams)
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
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(child is ast.Expr):
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
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[2]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(child is ast.Expr):
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
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[1]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(child is ast.Expr):
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
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[1]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(child is ast.Expr):
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
            if(child is ast.Expr):
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
            if(child is ast.Expr):
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
        exprRoles = ["MatchCondition", "CaseGuard", "CaseBody"]
        ############## PROPAGAR VISIT ############
        self.visit(node.subject, childparams.addParam('role', exprRoles[0]))
        for child in node.cases:
            self.visit(child, childparams.addParam('role_guard', exprRoles[1]).addParam('role_body', exprRoles[2]))
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
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[0]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[1]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[1]))
        for child in node.finalbody:
            if(child is ast.Expr):
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
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[0]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[0]))
        for child in node.orelse:
            if(child is ast.Expr):
                self.visit(child, childparams.addParam("role", exprRoles[1]))
            else:
                self.visit(child, childparams.addParam("role", stmtRoles[1]))
        for child in node.finalbody:
            if(child is ast.Expr):
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
        
        return
    
    def visit_Arguments(self : Self, node : ast.arguments , params : Dict) -> None: 
        
        return
    
    def visit_Arg(self : Self, node : ast.arg , params : Dict) -> None: 
        
        return
    
    def visit_Keyword(self : Self, node : ast.keyword , params : Dict) -> None: 
        
        return
    
    def visit_Alias(self : Self, node : ast.alias , params : Dict) -> None: 
        
        return
    
    def visit_Withitem(self : Self, node : ast.withitem , params : Dict) -> None: 
        
        return
    
    def visit_Match_case(self : Self, node : ast.match_case , params : Dict) -> None: 
        
        return
    
    def visit_TypeIgnore(self : Self, node : ast.TypeIgnore , params : Dict) -> None: 
        
        return
    
    def visit_TypeVar(self : Self, node : ast.TypeVar , params : Dict) -> None: 
        exprRules = ["TypeAnnotation"]
        return
    
    def visit_ParamSpec(self : Self, node : ast.ParamSpec , params : Dict) -> None: 
        exprRules = ["DefaultParamValue"]
        return
    
    def visit_TypeVarTuple(self : Self, node : ast.TypeVarTuple , params : Dict) -> None: 
        exprRules = ["TypeVar"]
        return
    
    ###########################################################
    