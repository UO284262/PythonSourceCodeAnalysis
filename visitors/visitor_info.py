import ast
import uuid
import util.util as util
from visitors.visitor import Visitor
import db.dbentities as dbentities

class Visitor_print(Visitor):

    ####################### Visits extra ######################
    """
    def visit_comp(self, params.node: ast. ,comp, depth: int):
        print("-"*depth + "Comp")
        comp.target.accept(self,depth+1)
        comp.iter.accept(self,depth+1)
        for child in comp.ifs:
            child.accept(self,depth+1)
        return
    
    def visit_keyword(self, params.node: ast. ,kyw, depth: int):
        print("-"*depth + "Keyword")
        if kyw.arg: print("-"*(depth+1) + "Identifier: " + kyw.args)
        kyw.value.accept(self,depth+1)
        return
    """
    ###########################################################

        ############ TYPES #######################
        ##########################################

    def visit_module(self, params, depth: int):
        dbnode = dbentities.DBNode()
        module = dbentities.DBModule()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, module.module_id = id
        dbnode.parent_id = params.parent_id
        ############ TYPES #######################
        ##########################################
        return
    
    def visit_functiondef(self, params, depth: int):
        dbnode = dbentities.DBNode()
        function = dbentities.DBFunctionDef()
        method = dbentities.DBMethodDef()
        params = dbentities.DBParameter()
        ############ IDS #########################
        id = uuid.uuid4()
        params_id = uuid.uuid4()
        params.parameters_id, function.parameters_id = params_id
        dbnode.node_id, function.functiondef_id, method.methoddef_id = id
        dbnode.parent_id, method.classdef_id, function.module_id = params.parent_id
        ##########################################
        return
    
    def visit_asyncfunctiondef(self, params, depth: int):
        dbnode = dbentities.DBNode()
        function = dbentities.DBFunctionDef()
        method = dbentities.DBMethodDef()
        params = dbentities.DBParameter()
        ############ IDS #########################
        id = uuid.uuid4()
        params_id = uuid.uuid4()
        params.parameters_id, function.parameters_id = params_id
        dbnode.node_id, function.functiondef_id, method.methoddef_id = id
        dbnode.parent_id, method.classdef_id, function.module_id = params.parent_id
        ##########################################
        return

    def visit_classdef(self, params, depth: int):
        dbnode = dbentities.DBNode()
        classdef = dbentities.DBClassDef()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, classdef.classdef_id = id
        dbnode.parent_id, classdef.module_id = params.parent_id
        ##########################################
        return

    ############################### STATEMENTS #############################

    def visit_return(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    def visit_delete(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    def visit_assign(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = "AssignmentStmt"
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    '''
    
    def visit_typealias(self,parent, params.parent_id, depth: int):
        return
    '''

    def visit_augassign(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = "AugmentedAssignment"
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    def visit_annassign(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = "AnnotatedAssignment"
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    def visit_for(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_asyncfor(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = "For"
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_while(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_if(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_with(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_asyncwith(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_match(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_raise(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_try(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_trystar(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = "Try"
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_assert(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_global(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_nonlocal(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_pass(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_break(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    
    def visit_continue(self, params, depth: int):
        dbnode = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, stmt.statement_id = id
        dbnode.parent_id, stmt.parent_id = params.parent_id
        ############ TYPES #######################
        stmt.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, stmt.parent = params.parent.table
        ##########################################
        return

    ############################ IMPORTS ##################################

    
    def visit_import(self, params, depth: int):
        dbnode = dbentities.DBImport()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.import_id, params.parent.import_id = id
        ##########################################
        return

    
    def visit_importfrom(self, params, depth: int):
        dbnode = dbentities.DBImport()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.import_id, params.parent.import_id = id
        ##########################################
        return

    ############################ EXPRESSIONS ##################################

    def visit_boolop(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "Logical"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_namedexpr(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "AssignmentExp"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_binop(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = util.opCategory(params.node)
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return
    
    
    def visit_unaryop(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = util.opCategory(params.node)
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return
    
    
    def visit_lambda(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return
    
    
    def visit_ifexp(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "Ternary"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    ######################### COMPREHENSIONS #############################

    
    def visit_listcomp(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, comp.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category, comp.category = "ListComprehension"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_setcomp(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, comp.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category, comp.category = "SetComprehension"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_dictcomp(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, comp.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category, comp.category = "DictComprehension"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_generatorexp(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, comp.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category, comp.category = "GeneratorComprehension"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    ######################################################################

    
    def visit_await(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_yield(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_yieldfrom(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_compare(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    ########################## call_args ###########################

    
    def visit_call(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        callArgs = dbentities.DBCallArg()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, callArgs.expression_id = id
        ############ TYPES #######################
        expr.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    ################################################################

    """
    def visit_formattedvalue(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ##########################################
        return
    """

    ########################### F-strings #####################################

    
    def visit_joinedstr(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        fstr = dbentities.DBFString()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, fstr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "FString"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    ###########################################################################

    
    def visit_constant(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = util.constCategory(params.node)
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_attribute(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "Dot"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_subscript(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "Indexing"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_starred(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "Star"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    ############################# Variable ##################################

    
    def visit_name(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        var = dbentities.DBVariable()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, var.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "Variable"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    ############################### Vectors #################################

    
    def visit_list(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, vct.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "ListLiteral"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_tuple(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, vct.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "TupleLiteral"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_dict(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, vct.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "DictionaryLiteral"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    
    def visit_set(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id, vct.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = "SetLiteral"
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    ########################################################################

    
    def visit_slice(self, params, depth: int):
        dbnode = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.node_id, expr.expression_id = id
        dbnode.parent_id, expr.parent_id = params.parent_id
        ############ TYPES #######################
        expr.category = params.node.__doc__.split('(')[0]
        dbnode.parent_table, expr.parent = params.parent.table
        ##########################################
        return

    ############################### Cases ###################################

    
    def visit_matchvalue(self, params, depth: int):
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ##########################################
        return

    
    def visit_matchsingleton(self, params, depth: int):
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ##########################################
        return

    
    def visit_matchsequence(self, params, depth: int):
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ##########################################
        return

    
    def visit_matchmapping(self, params, depth: int):
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ##########################################
        return

    
    def visit_matchclass(self, params, depth: int):
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ##########################################
        return

    
    def visit_matchstar(self, params, depth: int):
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ##########################################
        return

    
    def visit_matchas(self, params, depth: int):
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ##########################################
        return

    
    def visit_matchor(self, params, depth: int):
        dbnode = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.cases_id = id
        dbnode.statement_id = params.parent_id
        ##########################################
        return
    
    ############################# HANDLER ####################################

    def visit_excepthandler(self, params, depth: int):
        dbnode = dbentities.DBHandler()
        ############ IDS #########################
        id = uuid.uuid4()
        dbnode.handler_id = id
        dbnode.statement_id = params.parent_id
        ##########################################
        return
    