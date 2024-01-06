from abc import ABC, abstractmethod
import ast

class Visitor(ABC):

    @abstractmethod
    def visit_module(self, node: ast.Module, params, depth: int):
        pass

    @abstractmethod
    def visit_functiondef(self, node: ast.FunctionDef, params, depth: int):
        pass

    @abstractmethod
    def visit_asyncfunctiondef(self, node: ast.AsyncFunctionDef, params, depth: int):
        pass

    @abstractmethod
    def visit_classdef(self, node: ast.ClassDef, params, depth: int):
        pass

    ############################### STATEMENTS #############################

    @abstractmethod
    def visit_return(self, node: ast.Return, params, depth: int):
        pass

    @abstractmethod
    def visit_delete(self, node: ast.Delete, params, depth: int):
        pass

    @abstractmethod
    def visit_assign(self, node: ast.Assign, params, depth: int):
        pass

    '''
    @abstractmethod
    def visit_typealias(self, node: ast.TypeAlias, params, depth: int):
        pass
    '''

    @abstractmethod
    def visit_augassign(self, node: ast.AugAssign, params, depth: int):
        pass

    @abstractmethod
    def visit_annassign(self, node: ast.AnnAssign, params, depth: int):
        pass

    @abstractmethod
    def visit_for(self, node: ast.For, params, depth: int):
        pass

    @abstractmethod
    def visit_asyncfor(self, node: ast.AsyncFor, params, depth: int):
        pass

    @abstractmethod
    def visit_while(self, node: ast.While, params, depth: int):
        pass

    @abstractmethod
    def visit_if(self, node: ast.If, params, depth: int):
        pass

    @abstractmethod
    def visit_with(self, node: ast.With, params, depth: int):
        pass

    @abstractmethod
    def visit_asyncwith(self, node: ast.AsyncWith, params, depth: int):
        pass

    @abstractmethod
    def visit_match(self, node: ast.Match, params, depth: int):
        pass

    @abstractmethod
    def visit_raise(self, node: ast.Raise, params, depth: int):
        pass

    @abstractmethod
    def visit_try(self, node: ast.Try, params, depth: int):
        pass

    @abstractmethod
    def visit_trystar(self, node: ast.Try, params, depth: int):
        pass

    @abstractmethod
    def visit_assert(self, node: ast.Assert, params, depth: int):
        pass

    @abstractmethod
    def visit_global(self, node: ast.Global, params, depth: int):
        pass

    @abstractmethod
    def visit_nonlocal(self, node: ast.Nonlocal, params, depth: int):
        pass

    @abstractmethod
    def visit_pass(self, node: ast.Pass, params, depth: int):
        pass

    @abstractmethod
    def visit_break(self, node: ast.Break, params, depth: int):
        pass

    @abstractmethod
    def visit_continue(self, node: ast.Continue, params, depth: int):
        pass

    ############################ IMPORTS ##################################

    @abstractmethod
    def visit_import(self, node: ast.Import, params, depth: int):
        pass

    @abstractmethod
    def visit_importfrom(self, node: ast.ImportFrom, params, depth: int):
        pass

    ############################ EXPRESSIONS ##################################

    @abstractmethod
    def visit_boolop(self, node: ast.BoolOp, params, depth: int):
        pass

    @abstractmethod
    def visit_namedexpr(self, node: ast.NamedExpr, params, depth: int):
        pass

    @abstractmethod
    def visit_binop(self, node: ast.BinOp, params, depth: int):
        pass

    @abstractmethod
    def visit_unaryop(self, node: ast.UnaryOp, params, depth: int):
        pass

    @abstractmethod
    def visit_lambda(self, node: ast.Lambda, params, depth: int):
        pass

    @abstractmethod
    def visit_ifexp(self, node: ast.IfExp, params, depth: int):
        pass

    ######################### COMPREHENSIONS #############################

    @abstractmethod
    def visit_listcomp(self, node: ast.ListComp, params, depth: int):
        pass

    @abstractmethod
    def visit_setcomp(self, node: ast.SetComp, params, depth: int):
        pass

    @abstractmethod
    def visit_dictcomp(self, node: ast.DictComp, params, depth: int):
        pass

    @abstractmethod
    def visit_generatorexp(self, node: ast.GeneratorExp, params, depth: int):
        pass

    ######################################################################

    @abstractmethod
    def visit_await(self, node: ast.Await, params, depth: int):
        pass

    @abstractmethod
    def visit_yield(self, node: ast.Yield, params, depth: int):
        pass

    @abstractmethod
    def visit_yieldfrom(self, node: ast.YieldFrom, params, depth: int):
        pass

    @abstractmethod
    def visit_compare(self, node: ast.Compare, params, depth: int):
        pass

    ########################## call_args ###########################

    @abstractmethod
    def visit_call(self, node: ast.Call, params, depth: int):
        pass

    ################################################################

    @abstractmethod
    def visit_formattedvalue(self, node: ast.FormattedValue, params, depth: int):
        pass

    ########################### F-strings #####################################

    @abstractmethod
    def visit_joinedstr(self, node: ast.JoinedStr, params, depth: int):
        pass

    ###########################################################################

    @abstractmethod
    def visit_constant(self, node: ast.Constant, params, depth: int):
        pass

    @abstractmethod
    def visit_attribute(self, node: ast.Attribute, params, depth: int):
        pass

    @abstractmethod
    def visit_subscript(self, node: ast.Subscript, params, depth: int):
        pass

    @abstractmethod
    def visit_starred(self, node: ast.Starred, params, depth: int):
        pass

    ############################# Variable ##################################

    @abstractmethod
    def visit_name(self, node: ast.Name, params, depth: int):
        pass

    ############################### Vectors #################################

    @abstractmethod
    def visit_list(self, node: ast.List, params, depth: int):
        pass

    @abstractmethod
    def visit_tuple(self, node: ast.Tuple, params, depth: int):
        pass

    @abstractmethod
    def visit_dict(self, node: ast.Dict, params, depth: int):
        pass

    @abstractmethod
    def visit_set(self, node: ast.Set, params, depth: int):
        pass

    ########################################################################

    @abstractmethod
    def visit_slice(self, node: ast.Slice, params, depth: int):
        pass

    @abstractmethod
    def visit_excepthandler(self, node: ast.ExceptHandler, params, depth: int):
        pass

    ############################### Cases ###################################

    @abstractmethod
    def visit_matchvalue(self, node: ast.MatchValue, params, depth: int):
        pass

    @abstractmethod
    def visit_matchsingleton(self, node: ast.MatchSingleton, params, depth: int):
        pass

    @abstractmethod
    def visit_matchsequence(self, node: ast.MatchSequence, params, depth: int):
        pass

    @abstractmethod
    def visit_matchmapping(self, node: ast.MatchMapping, params, depth: int):
        pass

    @abstractmethod
    def visit_matchclass(self, node: ast.MatchClass, params, depth: int):
        pass

    @abstractmethod
    def visit_matchstar(self, node: ast.MatchStar, params, depth: int):
        pass

    @abstractmethod
    def visit_matchas(self, node: ast.MatchAs, params, depth: int):
        pass

    @abstractmethod
    def visit_matchor(self, node: ast.MatchOr, params, depth: int):
        pass