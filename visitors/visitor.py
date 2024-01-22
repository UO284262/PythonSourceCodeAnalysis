from abc import ABC, abstractmethod
import ast

class Visitor(ABC):

    @abstractmethod
    def visit_module(self, node: ast.Module, params):
        pass

    @abstractmethod
    def visit_functiondef(self, node: ast.FunctionDef, params):
        pass

    @abstractmethod
    def visit_asyncfunctiondef(self, node: ast.AsyncFunctionDef, params):
        pass

    @abstractmethod
    def visit_classdef(self, node: ast.ClassDef, params):
        pass

    ############################### STATEMENTS #############################

    @abstractmethod
    def visit_return(self, node: ast.Return, params):
        pass

    @abstractmethod
    def visit_delete(self, node: ast.Delete, params):
        pass

    @abstractmethod
    def visit_assign(self, node: ast.Assign, params):
        pass

    @abstractmethod
    def visit_typealias(self, node: ast.TypeAlias, params):
        pass

    @abstractmethod
    def visit_augassign(self, node: ast.AugAssign, params):
        pass

    @abstractmethod
    def visit_annassign(self, node: ast.AnnAssign, params):
        pass

    @abstractmethod
    def visit_for(self, node: ast.For, params):
        pass

    @abstractmethod
    def visit_asyncfor(self, node: ast.AsyncFor, params):
        pass

    @abstractmethod
    def visit_while(self, node: ast.While, params):
        pass

    @abstractmethod
    def visit_if(self, node: ast.If, params):
        pass

    @abstractmethod
    def visit_with(self, node: ast.With, params):
        pass

    @abstractmethod
    def visit_asyncwith(self, node: ast.AsyncWith, params):
        pass

    @abstractmethod
    def visit_match(self, node: ast.Match, params):
        pass

    @abstractmethod
    def visit_raise(self, node: ast.Raise, params):
        pass

    @abstractmethod
    def visit_try(self, node: ast.Try, params):
        pass

    @abstractmethod
    def visit_trystar(self, node: ast.Try, params):
        pass

    @abstractmethod
    def visit_assert(self, node: ast.Assert, params):
        pass

    @abstractmethod
    def visit_global(self, node: ast.Global, params):
        pass

    @abstractmethod
    def visit_nonlocal(self, node: ast.Nonlocal, params):
        pass

    @abstractmethod
    def visit_pass(self, node: ast.Pass, params):
        pass

    @abstractmethod
    def visit_break(self, node: ast.Break, params):
        pass

    @abstractmethod
    def visit_continue(self, node: ast.Continue, params):
        pass

    ############################ IMPORTS ##################################

    @abstractmethod
    def visit_import(self, node: ast.Import, params):
        pass

    @abstractmethod
    def visit_importfrom(self, node: ast.ImportFrom, params):
        pass

    ############################ EXPRESSIONS ##################################

    @abstractmethod
    def visit_boolop(self, node: ast.BoolOp, params):
        pass

    @abstractmethod
    def visit_namedexpr(self, node: ast.NamedExpr, params):
        pass

    @abstractmethod
    def visit_binop(self, node: ast.BinOp, params):
        pass

    @abstractmethod
    def visit_unaryop(self, node: ast.UnaryOp, params):
        pass

    @abstractmethod
    def visit_lambda(self, node: ast.Lambda, params):
        pass

    @abstractmethod
    def visit_ifexp(self, node: ast.IfExp, params):
        pass

    ######################### COMPREHENSIONS #############################

    @abstractmethod
    def visit_listcomp(self, node: ast.ListComp, params):
        pass

    @abstractmethod
    def visit_setcomp(self, node: ast.SetComp, params):
        pass

    @abstractmethod
    def visit_dictcomp(self, node: ast.DictComp, params):
        pass

    @abstractmethod
    def visit_generatorexp(self, node: ast.GeneratorExp, params):
        pass

    ######################################################################

    @abstractmethod
    def visit_await(self, node: ast.Await, params):
        pass

    @abstractmethod
    def visit_yield(self, node: ast.Yield, params):
        pass

    @abstractmethod
    def visit_yieldfrom(self, node: ast.YieldFrom, params):
        pass

    @abstractmethod
    def visit_compare(self, node: ast.Compare, params):
        pass

    ########################## call_args ###########################

    @abstractmethod
    def visit_call(self, node: ast.Call, params):
        pass

    ################################################################

    @abstractmethod
    def visit_formattedvalue(self, node: ast.FormattedValue, params):
        pass

    ########################### F-strings #####################################

    @abstractmethod
    def visit_joinedstr(self, node: ast.JoinedStr, params):
        pass

    ###########################################################################

    @abstractmethod
    def visit_constant(self, node: ast.Constant, params):
        pass

    @abstractmethod
    def visit_attribute(self, node: ast.Attribute, params):
        pass

    @abstractmethod
    def visit_subscript(self, node: ast.Subscript, params):
        pass

    @abstractmethod
    def visit_starred(self, node: ast.Starred, params):
        pass

    ############################# Variable ##################################

    @abstractmethod
    def visit_name(self, node: ast.Name, params):
        pass

    ############################### Vectors #################################

    @abstractmethod
    def visit_list(self, node: ast.List, params):
        pass

    @abstractmethod
    def visit_tuple(self, node: ast.Tuple, params):
        pass

    @abstractmethod
    def visit_dict(self, node: ast.Dict, params):
        pass

    @abstractmethod
    def visit_set(self, node: ast.Set, params):
        pass

    ########################################################################

    @abstractmethod
    def visit_slice(self, node: ast.Slice, params):
        pass

    @abstractmethod
    def visit_excepthandler(self, node: ast.ExceptHandler, params):
        pass

    ############################### Cases ###################################

    @abstractmethod
    def visit_matchvalue(self, node: ast.MatchValue, params):
        pass

    @abstractmethod
    def visit_matchsingleton(self, node: ast.MatchSingleton, params):
        pass

    @abstractmethod
    def visit_matchsequence(self, node: ast.MatchSequence, params):
        pass

    @abstractmethod
    def visit_matchmapping(self, node: ast.MatchMapping, params):
        pass

    @abstractmethod
    def visit_matchclass(self, node: ast.MatchClass, params):
        pass

    @abstractmethod
    def visit_matchstar(self, node: ast.MatchStar, params):
        pass

    @abstractmethod
    def visit_matchas(self, node: ast.MatchAs, params):
        pass

    @abstractmethod
    def visit_matchor(self, node: ast.MatchOr, params):
        pass