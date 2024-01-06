import ast
from visitors.visitor import Visitor
import visitors.accepts as accepts

class Visitor_print(Visitor):

     ####################### Visits extra ######################

    def visit_comp(self, comp, params, depth: int):
        print("-"*depth + "Comp")
        comp.target.accept(self, params, depth+1)
        comp.iter.accept(self, params, depth+1)
        for child in comp.ifs:
            child.accept(self, params, depth+1)
        return
    
    def visit_keyword(self, kyw, params, depth: int):
        print("-"*depth + "Keyword")
        if kyw.arg: print("-"*(depth+1) + "Identifier: " + kyw.args)
        kyw.value.accept(self, params, depth+1)
        return

    ###########################################################
    
    def visit_module(self, node: ast.Module, params, depth: int):
        print("-"*depth + "Module")
        for child in node.body:
            child.accept(self, params, depth+1)
        return
    
    def visit_functiondef(self, node: ast.FunctionDef, params, depth: int):
        print("-"*depth + "Function Def")
        for child in node.body:
            child.accept(self, params, depth+1)
        return
    
    def visit_asyncfunctiondef(self, node: ast.AsyncFunctionDef, params, depth: int):
        print("-"*depth + "Async Function Def")
        for child in node.body:
            child.accept(self, params, depth+1)
        return

    def visit_classdef(self, node: ast.ClassDef, params, depth: int):
        print("-"*depth + "Class Def")
        for child in node.body:
            child.accept(self, params, depth+1)
        return

    ############################### STATEMENTS #############################

    def visit_return(self, node: ast.Return, params, depth: int):
        print("-"*depth + "Return")
        if node.value: node.value.accept(self, params, depth+1)
        return

    def visit_delete(self, node: ast.Delete, params, depth: int):
        print("-"*depth + "Delete")
        for child in node.targets:
            child.accept(self, params, depth+1)
        return

    def visit_assign(self, node: ast.Assign, params, depth: int):
        print("-"*depth + "Assign")
        for child in node.targets:
            child.accept(self, params, depth+1)
        node.value.accept(self, params, depth+1)
        return

    '''
    
    def visit_typealias(self, node: ast.TypeAlias, params, depth: int):
        return
    '''

    def visit_augassign(self, node: ast.AugAssign, params, depth: int):
        print("-"*depth + "Aug Assign")
        node.target.accept(self, params, depth+1)
        node.value.accept(self, params, depth+1)
        return

    def visit_annassign(self, node: ast.AnnAssign, params, depth: int):
        print("-"*depth + "Ann Assign")
        node.target.accept(self, params, depth+1)
        node.annotation.accept(self, params, depth+1)
        if node.value: node.value.accept(self, params, depth+1)
        return

    def visit_for(self, node: ast.For, params, depth: int):
        print("-"*depth + "For")
        node.target.accept(self, params, depth+1)
        node.iter.accept(self, params, depth+1)
        for child in node.body:
            child.accept(self, params, depth+1)
        for child in node.orelse:
            child.accept(self, params, depth+1)
        return

    
    def visit_asyncfor(self, node: ast.AsyncFor, params, depth: int):
        print("-"*depth + "Async For")
        node.target.accept(self, params, depth+1)
        node.iter.accept(self, params, depth+1)
        for child in node.body:
            child.accept(self, params, depth+1)
        for child in node.orelse:
            child.accept(self, params, depth+1)
        return

    
    def visit_while(self, node: ast.While, params, depth: int):
        print("-"*depth + "While")
        node.test.accept(self, params, depth+1)
        for child in node.body:
            child.accept(self, params, depth+1)
        for child in node.orelse:
            child.accept(self, params, depth+1)
        return

    
    def visit_if(self, node: ast.If, params, depth: int):
        print("-"*depth + "If")
        node.test.accept(self, params, depth+1)
        for child in node.body:
            child.accept(self, params, depth+1)
        for child in node.orelse:
            child.accept(self, params, depth+1)
        return

    
    def visit_with(self, node: ast.With, params, depth: int):
        print("-"*depth + "With")
        for child in node.items:
            child.context_expr.accept(self, params, depth+1)
        for child in node.body:
            child.accept(self, params, depth+1)
        return

    
    def visit_asyncwith(self, node: ast.AsyncWith, params, depth: int):
        print("-"*depth + "Async With")
        for child in node.items:
            child.context_expr.accept(self, params, depth+1)
        for child in node.body:
            child.accept(self, params, depth+1)
        return

    
    def visit_match(self, node: ast.Match, params, depth: int):
        print("-"*depth + "Match")
        node.subject.accept(self, params, depth+1)
        for child in node.cases:
            child.pattern.accept(self, params, depth+1)
            if child.guard: child.guard.accept(self, params, depth+1)
            for child2 in child.body:
                child2.accept(self, params, depth+2)
        return

    
    def visit_raise(self, node: ast.Raise, params, depth: int):
        print("-"*depth + "Raise")
        if node.exc: node.exc.accept(self, params, depth+1)
        if node.cause: node.cause.accept(self, params, depth+1)
        return

    
    def visit_try(self, node: ast.Try, params, depth: int):
        print("-"*depth + "Try")
        for child in node.body:
            child.accept(self, params, depth+1)
        for child in node.handlers:
            child.accept(self, params, depth+1)
        for child in node.orelse:
            child.accept(self, params, depth+1)
        for child in node.finalbody:
            child.accept(self, params, depth+1)
        return

    
    def visit_trystar(self, node: ast.Try, params, depth: int):
        print("-"*depth + "Try Star")
        for child in node.body:
            child.accept(self, params, depth+1)
        for child in node.handlers:
            child.accept(self, params, depth+1)
        for child in node.orelse:
            child.accept(self, params, depth+1)
        for child in node.finalbody:
            child.accept(self, params, depth+1)
        return

    
    def visit_assert(self, node: ast.Assert, params, depth: int):
        print("-"*depth + "Assert")
        node.test.accept(self, params, depth+1)
        if node.msg: node.msg.accept(self, params, depth+1)
        return

    
    def visit_global(self, node: ast.Global, params, depth: int):
        print("-"*depth + "Global")
        for child in node.names:
            print("-"*(depth+1) + "Identifier: " + child)
        return

    
    def visit_nonlocal(self, node: ast.Nonlocal, params, depth: int):
        print("-"*depth + "Non Local")
        for child in node.names:
            print("-"*(depth+1) + "Identifier: " + child)
        return

    
    def visit_pass(self, node: ast.Pass, params, depth: int):
        print("-"*depth + "Pass")
        return

    
    def visit_break(self, node: ast.Break, params, depth: int):
        print("-"*depth + "Break")
        return

    
    def visit_continue(self, node: ast.Continue, params, depth: int):
        print("-"*depth + "Continue")
        return

    ############################ IMPORTS ##################################

    
    def visit_import(self, node: ast.Import, params, depth: int):
        print("-"*depth + "Import")
        for child in node.names:
            print("-"*(depth+1) + "Identifier: ")
        return

    
    def visit_importfrom(self, node: ast.ImportFrom, params, depth: int):
        print("-"*depth + "Import From")
        if node.module: print("-"*depth + "Identifier: " + node.module)
        for child in node.names:
            print("-"*(depth+1) + "Identifier: " + child)
        return

    ############################ EXPRESSIONS ##################################

    def visit_boolop(self, node: ast.BoolOp, params, depth: int):
        print("-"*depth + "Bool Op")
        for child in node.values:
            child.accept(self, params, depth+1)
        print("-"*depth + node.op.__doc__)
        return

    
    def visit_namedexpr(self, node: ast.NamedExpr, params, depth: int):
        print("-"*depth + "Named Expr")
        node.target.accept(self, params, depth+1)
        node.value.accept(self, params, depth+1)
        return

    
    def visit_binop(self, node: ast.BinOp, params, depth: int):
        print("-"*depth + "Bin Op")
        node.left.accept(self, params, depth+1)
        print("-"*depth + node.op.__doc__)
        node.right.accept(self, params, depth+1)
        return
    
    
    def visit_unaryop(self, node: ast.UnaryOp, params, depth: int):
        print("-"*depth + "Unary Op")
        print("-"*depth + node.op.__doc__)
        node.operand.accept(self, params, depth+1)
        return
    
    
    def visit_lambda(self, node: ast.Lambda, params, depth: int):
        print("-"*depth + "Lambda")
        for child in node.body:
            child.accept(self, params, depth+1)
        return
    
    
    def visit_ifexp(self, node: ast.IfExp, params, depth: int):
        print("-"*depth + "If Exp")
        node.test.accept(self, params, depth+1)
        node.body.accept(self, params, depth+1)
        node.orelse.accept(self, params, depth+1)
        return

    ######################### COMPREHENSIONS #############################

    
    def visit_listcomp(self, node: ast.ListComp, params, depth: int):
        print("-"*depth + "List Comp")
        node.elt.accept(self, params, depth+1)
        for child in node.generators:
            self.visit_comp(child, params, depth+1)
        return

    
    def visit_setcomp(self, node: ast.SetComp, params, depth: int):
        print("-"*depth + "Set Comp")
        node.elt.accept(self, params, depth+1)
        for child in node.generators:
            self.visit_comp(child, params, depth+1)
        return

    
    def visit_dictcomp(self, node: ast.DictComp, params, depth: int):
        print("-"*depth + "Dict Comp")
        node.key.accept(self, params, depth+1)
        node.value.accept(self, params, depth+1)
        for child in node.generators:
            self.visit_comp(child, params, depth+1)
        return

    
    def visit_generatorexp(self, node: ast.GeneratorExp, params, depth: int):
        print("-"*depth + "Generator Exp")
        node.elt.accept(self, params, depth+1)
        for child in node.generators:
            self.visit_comp(child, params, depth+1)
        return

    ######################################################################

    
    def visit_await(self, node: ast.Await, params, depth: int):
        print("-"*depth + "Await")
        node.value.accept(self, params, depth+1)
        return

    
    def visit_yield(self, node: ast.Yield, params, depth: int):
        print("-"*depth + "Yield")
        if node.value: node.value.accept(self, params, depth+1)
        return

    
    def visit_yieldfrom(self, node: ast.YieldFrom, params, depth: int):
        print("-"*depth + "Yield From")
        node.value.accept(self, params, depth+1)
        return

    
    def visit_compare(self, node: ast.Compare, params, depth: int):
        print("-"*depth + "Compare")
        node.left.accept(self, params, depth+1)
        for child in node.ops:
            print("-"*depth+1 + node.ops.__doc__)
        for child in node.comparators:
            child.accept(self, params, depth+1)
        return

    ########################## call_args ###########################

    
    def visit_call(self, node: ast.Call, params, depth: int):
        print("-"*depth + "Call")
        node.func.accept(self, params, depth+1)
        for child in node.args:
            child.accept(self, params, depth+1)
        for child in node.keywords:
            self.visit_keyword(child, params, depth)
        return

    ################################################################

    
    def visit_formattedvalue(self, node: ast.FormattedValue, params, depth: int):
        print("-"*depth + "Formated Value")
        node.value.accept(self, params, depth+1)
        if node.format_spec: node.format_spec.accept(self, params, depth+1)
        return

    ########################### F-strings #####################################

    
    def visit_joinedstr(self, node: ast.JoinedStr, params, depth: int):
        print("-"*depth + "Joined Str")
        for child in node.values:
            child.accept(self, params, depth+1)
        return

    ###########################################################################

    
    def visit_constant(self, node: ast.Constant, params, depth: int):
        print("-"*depth + "Constant")
        print("-"*(depth+1) + "Value")
        if node.kind: print("-"*(depth+1) + "Kind:" + node.kind + "")
        return

    
    def visit_attribute(self, node: ast.Attribute, params, depth: int):
        print("-"*depth + "Attribute")
        node.value.accept(self, params, depth+1)
        print("-"*(depth+1) + "Identifier: " + node.attr)
        print("-"*(depth+1) + "Expr Context: " + node.ctx.__doc__)
        return

    
    def visit_subscript(self, node: ast.Subscript, params, depth: int):
        print("-"*depth + "Subscript")
        node.value.accept(self, params, depth+1)
        node.slice.accept(self, params, depth+1)
        print("-"*(depth+1) + "Expr Context" + node.ctx.__doc__)
        return

    
    def visit_starred(self, node: ast.Starred, params, depth: int):
        print("-"*depth + "Starred")
        node.value.accept(self, params, depth+1)
        print("-"*(depth+1) + "Expr Context: " + node.ctx.__doc__)
        return

    ############################# Variable ##################################

    
    def visit_name(self, node: ast.Name, params, depth: int):
        print("-"*depth + "Name")
        print("-"*(depth+1) + "Identifier: " + node.id)
        print("-"*(depth+1) + "Expr Context: " + node.ctx.__doc__)
        return

    ############################### Vectors #################################

    
    def visit_list(self, node: ast.List, params, depth: int):
        print("-"*depth + "List")
        for child in node.elts:
            child.accept(self, params, depth+1)
        print("-"*(depth+1) + "Expr Context: " + node.ctx.__doc__)
        return

    
    def visit_tuple(self, node: ast.Tuple, params, depth: int):
        print("-"*depth + "Tuple")
        for child in node.elts:
            child.accept(self, params, depth+1)
        print("-"*(depth+1) + "Expr Context: " + node.ctx.__doc__)
        return

    
    def visit_dict(self, node: ast.Dict, params, depth: int):
        print("-"*depth + "Dict")
        print("-"*depth + "Keys")
        for child in node.keys:
            child.accept(self, params, depth+1)
        print("-"*depth + "Values")
        for child in node.values:
            child.accept(self, params, depth+1)
        return

    
    def visit_set(self, node: ast.Set, params, depth: int):
        print("-"*depth + "Set")
        for child in node.elts:
            child.accept(self, params, depth+1)
        return

    ########################################################################

    
    def visit_slice(self, node: ast.Slice, params, depth: int):
        print("-"*depth + "Slice")
        if node.lower: node.lower.accept(self, params, depth+1)
        if node.upper: node.upper.accept(self, params, depth+1)
        if node.step: node.step.accept(self, params, depth+1)
        return

    ############################### Cases ###################################

    
    def visit_matchvalue(self, node: ast.MatchValue, params, depth: int):
        print("-"*depth + "Match Value")
        node.value.accept(self, params, depth+1)
        return

    
    def visit_matchsingleton(self, node: ast.MatchSingleton, params, depth: int):
        print("-"*depth + "Match Singleton")
        print("-"*(depth+1) + "Value")
        return

    
    def visit_matchsequence(self, node: ast.MatchSequence, params, depth: int):
        print("-"*depth + "Match Sequence")
        for child in node.patterns:
            child.accept(self, params, depth+1)
        return

    
    def visit_matchmapping(self, node: ast.MatchMapping, params, depth: int):
        print("-"*depth + "Match Mapping")
        for child in node.keys:
            child.accept(self, params, depth+1)
        for child in node.patterns:
            child.accept(self, params, depth+1)
        if node.rest: print("-"*(depth+1) + "Identifier: " + node.rest)
        return

    
    def visit_matchclass(self, node: ast.MatchClass, params, depth: int):
        print("-"*depth + "Match Class")
        node.cls.accept(self, params, depth+1)
        for child in node.patterns:
            child.accept(self, params, depth+1)
        for child in node.kwd_attrs:
            print("-"*(depth+1) + "Identifier: " + child)
        for child in node.kwd_patterns:
            child.accept(self, params, depth+1)
        return

    
    def visit_matchstar(self, node: ast.MatchStar, params, depth: int):
        print("-"*depth + "Match Star")
        if node.name: print("-"*(depth+1) + "Identifier: " + node.name)
        return

    
    def visit_matchas(self, node: ast.MatchAs, params, depth: int):
        print("-"*depth + "Match As")
        if node.pattern: node.pattern.accept(self, params, depth+1)
        if node.name: print("-"*(depth+1) + "Identifier: " + node.name)
        return

    
    def visit_matchor(self, node: ast.MatchOr, params, depth: int):
        print("-"*depth + "Match Or")
        for child in node.patterns:
            child.accept(self, params, depth+1)
        return
    
    #################################################################

    def visit_excepthandler(self, node: ast.ExceptHandler, params, depth: int):
        print("-"*depth + "Except Handler")
        if node.type: node.type.accept(self, params, depth+1)
        if node.name: print("-"*(depth+1) + "Identifier: " + node.name)
        for child in node.body:
            child.accept(self, params, depth+1)
        return
    