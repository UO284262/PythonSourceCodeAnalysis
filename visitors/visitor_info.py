import ast
import uuid
from visitors.visitor import Visitor
import db.dbentities as dbentities

class Visitor_print(Visitor):

    ####################### Visits extra ######################
    """
    def visit_comp(self, comp, depth: int):
        print("-"*depth + "Comp")
        comp.target.accept(self, depth+1)
        comp.iter.accept(self,depth+1)
        for child in comp.ifs:
            child.accept(self, depth+1)
        return
    
    def visit_keyword(self, kyw, depth: int):
        print("-"*depth + "Keyword")
        if kyw.arg: print("-"*(depth+1) + "Identifier: " + kyw.args)
        kyw.value.accept(self,depth+1)
        return
    """
    ###########################################################

        ############ IDS #########################
        ##########################################

    def visit_module(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        module = dbentities.DBModule()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, module.module_id = id
        node.parent_id = parent_id
        ##########################################
        return
    
    def visit_functiondef(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        function = dbentities.DBFunctionDef()
        method = dbentities.DBMethodDef()
        params = dbentities.DBParameter()
        ############ IDS #########################
        id = uuid.uuid4()
        params_id = uuid.uuid4()
        params.parameters_id, function.parameters_id = params_id
        node.node_id, function.functiondef_id, method.methoddef_id = id
        node.parent_id, method.classdef_id, function.module_id = parent_id
        ##########################################
        return
    
    def visit_asyncfunctiondef(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        function = dbentities.DBFunctionDef()
        method = dbentities.DBMethodDef()
        params = dbentities.DBParameter()
        ############ IDS #########################
        id = uuid.uuid4()
        params_id = uuid.uuid4()
        params.parameters_id, function.parameters_id = params_id
        node.node_id, function.functiondef_id, method.methoddef_id = id
        node.parent_id, method.classdef_id, function.module_id = parent_id
        ##########################################
        return

    def visit_classdef(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        classdef = dbentities.DBClassDef()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, classdef.classdef_id = id
        node.parent_id, classdef.module_id = parent_id
        ##########################################
        return

    ############################### STATEMENTS #############################

    def visit_return(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    def visit_delete(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    def visit_assign(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    '''
    
    def visit_typealias(self, parent, parent_id, depth: int):
        return
    '''

    def visit_augassign(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    def visit_annassign(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    def visit_for(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_asyncfor(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_while(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_if(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_with(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_asyncwith(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_match(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_raise(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_try(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_trystar(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_assert(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_global(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_nonlocal(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_pass(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_break(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    
    def visit_continue(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        stmt = dbentities.DBStatement()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, stmt.statement_id = id
        node.parent_id, stmt.parent_id = id
        ##########################################
        return

    ############################ IMPORTS ##################################

    
    def visit_import(self, parent: dbentities.DBModule, parent_id, depth: int):
        node = dbentities.DBImport()
        ############ IDS #########################
        id = uuid.uuid4()
        node.import_id, parent.import_id = id
        ##########################################
        return

    
    def visit_importfrom(self, parent: dbentities.DBModule, parent_id, depth: int):
        node = dbentities.DBImport()
        ############ IDS #########################
        id = uuid.uuid4()
        node.import_id, parent.import_id = id
        ##########################################
        return

    ############################ EXPRESSIONS ##################################

    def visit_boolop(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_namedexpr(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_binop(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return
    
    
    def visit_unaryop(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return
    
    
    def visit_lambda(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return
    
    
    def visit_ifexp(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    ######################### COMPREHENSIONS #############################

    
    def visit_listcomp(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id, comp.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_setcomp(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id, comp.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_dictcomp(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id, comp.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_generatorexp(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        comp = dbentities.DBComprehension()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id, comp.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    ######################################################################

    
    def visit_await(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_yield(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_yieldfrom(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_compare(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    ########################## call_args ###########################

    
    def visit_call(self, parent, parent_id, depth: int):
        node = dbentities.DBCallArg()
        ############ IDS #########################
        id = uuid.uuid4()
        node.callArgs_id = id
        node.expression_id = parent_id
        ##########################################
        return

    ################################################################

    
    def visit_formattedvalue(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    ########################### F-strings #####################################

    
    def visit_joinedstr(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        fstr = dbentities.DBFString()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id, fstr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    ###########################################################################

    
    def visit_constant(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_attribute(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_subscript(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_starred(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    ############################# Variable ##################################

    
    def visit_name(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        var = dbentities.DBVariable()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id, var.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    ############################### Vectors #################################

    
    def visit_list(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id, vct.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_tuple(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id, vct.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_dict(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id, vct.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    
    def visit_set(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        vct = dbentities.DBVector()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id, vct.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    ########################################################################

    
    def visit_slice(self, parent, parent_id, depth: int):
        node = dbentities.DBNode()
        expr = dbentities.DBExpression()
        ############ IDS #########################
        id = uuid.uuid4()
        node.node_id, expr.expression_id = id
        node.parent_id, expr.parent_id = parent_id
        ##########################################
        return

    ############################### Cases ###################################

    
    def visit_matchvalue(self, parent, parent_id, depth: int):
        node = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        node.cases_id = id
        node.statement_id = parent_id
        ##########################################
        return

    
    def visit_matchsingleton(self, parent, parent_id, depth: int):
        node = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        node.cases_id = id
        node.statement_id = parent_id
        ##########################################
        return

    
    def visit_matchsequence(self, parent, parent_id, depth: int):
        node = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        node.cases_id = id
        node.statement_id = parent_id
        ##########################################
        return

    
    def visit_matchmapping(self, parent, parent_id, depth: int):
        node = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        node.cases_id = id
        node.statement_id = parent_id
        ##########################################
        return

    
    def visit_matchclass(self, parent, parent_id, depth: int):
        node = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        node.cases_id = id
        node.statement_id = parent_id
        ##########################################
        return

    
    def visit_matchstar(self, parent, parent_id, depth: int):
        node = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        node.cases_id = id
        node.statement_id = parent_id
        ##########################################
        return

    
    def visit_matchas(self, parent, parent_id, depth: int):
        node = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        node.cases_id = id
        node.statement_id = parent_id
        ##########################################
        return

    
    def visit_matchor(self, parent, parent_id, depth: int):
        node = dbentities.DBCase()
        ############ IDS #########################
        id = uuid.uuid4()
        node.cases_id = id
        node.statement_id = parent_id
        ##########################################
        return
    
    ############################# HANDLER ####################################

    def visit_excepthandler(self, parent, parent_id, depth: int):
        node = dbentities.DBHandler()
        ############ IDS #########################
        id = uuid.uuid4()
        node.handler_id = id
        node.statement_id = parent_id
        ##########################################
        return
    