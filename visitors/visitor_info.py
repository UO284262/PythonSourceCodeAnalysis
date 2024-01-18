import ast
from typing import Dict, Self
import uuid
import util.util as util
from visitors.My_NodeVisitor import NodeVisitor
from visitors.visitor import Visitor
import db.dbentities as dbentities

class Visitor_info(NodeVisitor):

    # params = [parent, parent_id = node]

    ####################### Visits extra ######################
    """
    def visit_comp(self : Self, node: ast. ,comp) -> None: 
        print("-"*depth + "Comp")
        comp.target.accept(self : Self,depth+1)
        comp.iter.accept(self : Self,depth+1)
        for child in comp.ifs:
            child.accept(self : Self,depth+1)
        return
    
    def visit_keyword(self : Self, node: ast. ,kyw) -> None: 
        print("-"*depth + "Keyword")
        if kyw.arg: print("-"*(depth+1) + "Identifier: " + kyw.args)
        kyw.value.accept(self : Self,depth+1)
        return
    """
    ###########################################################

    def visit_Module(self : Self, node : ast.Module , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        module = dbentities.DBModule()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = module.module_id = id
        ############# PARAMS #####################
        params = {"parent" : module, "depth" : 1, "parent_id" : id, "role" : "Module"}
        ##########################################
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
        params = {"parent" : function, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["FunctionDef", "MethodDef"]
        exprRoles = ["FuncDecorator", "ReturnType", "FuncBody"]
        ##########################################
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
        params = {"parent" : function, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["AsyncFunctionDef", "AsyncMethodDef"]
        exprRoles = ["FuncDecorator", "ReturnType", "FuncBody", "MethodBody"]
        ##########################################
        return

    def visit_ClassDef(self : Self, node : ast.ClassDef , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        classdef = dbentities.DBClassDef()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = classdef.classdef_id = id
        dbnode.parent_id = classdef.module_id = params.parent_id
        ############# PARAMS #####################
        params = {"parent" : classdef, "depth" : params.depth + 1, "parent_id" : id}
        stmtRoles = ["ClassDef"]
        exprRoles = ["ClassBase", "ClassDecorator", "ClassBody"]
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id, "role" : "Return"}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id, "role" : "Delete"}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        roles = ["AssignLHS", "AssignRHS"]
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        roles = ["TypeAliasLHS", "TypeAliasRHS"]
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        roles = ["AugmentedAssigmentLHS", "AugmentedAssigmentRHS"]
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        roles = ["VarDefVarName", "VarDefType", "VarDefInitValue"]
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : stmt, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    ############################ IMPORTS ##################################

    
    def visit_Import(self : Self, node : ast.Import , params : Dict) -> None: 
        dbnode = dbentities.DBImport()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.import_id = params.parent.import_id = id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    
    def visit_ImportFrom(self : Self, node : ast.ImportFrom , params : Dict) -> None: 
        dbnode = dbentities.DBImport()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.import_id = params.parent.import_id = id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    ################################################################

    """
    def visit_formattedvalue(self : Self, node : ast. , params : Dict) -> None: 
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.node_id = expr.expression_id = id
        dbnode.parent_id = expr.parent_id = params.parent_id
        ##########################################
        return
    """

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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
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
        params = {"parent" : expr, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    ############################### Cases ###################################

    
    def visit_MatchValue(self : Self, node : ast.MatchValue , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    
    def visit_MatchSingleton(self : Self, node : ast.MatchSingleton , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    
    def visit_MatchSequence(self : Self, node : ast.MatchSequence , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    
    def visit_MatchMapping(self : Self, node : ast.MatchMapping , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    
    def visit_MatchClass(self : Self, node : ast.MatchClass , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    
    def visit_MatchStar(self : Self, node : ast.MatchStar , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    
    def visit_MatchAs(self : Self, node : ast.MatchAs , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return

    
    def visit_MatchOr(self : Self, node : ast.MatchOr , params : Dict) -> None: 
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return
    
    ############################# HANDLER ####################################

    def visit_ExceptHandler(self : Self, node : ast.ExceptHandler , params : Dict) -> None: 
        dbnode = dbentities.DBHandler()
        ############ IDS #########################
        id = uuid.uuid4().int
        dbnode.handler_id = id
        dbnode.statement_id = params.parent_id
        ############# PARAMS #####################
        params = {"parent" : dbnode, "depth" : params.depth + 1, "parent_id" : id}
        ##########################################
        return
    