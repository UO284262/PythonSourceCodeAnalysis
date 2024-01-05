from abc import ABC, abstractmethod
import ast

class Visitor(ABC):

    @abstractmethod
    def visit_module(self, node: ast.Module, depth: int):
        pass

    @abstractmethod
    def visit_functiondef(self, node: ast.FunctionDef, depth: int):
        pass

    @abstractmethod
    def visit_asyncfunctiondef(self, node: ast.AsyncFunctionDef, depth: int):
        pass

    @abstractmethod
    def visit_classdef(self, node: ast.ClassDef, depth: int):
        pass

    ############################### STATEMENTS #############################

    @abstractmethod
    def visit_return(self, node: ast.Return, depth: int):
        pass

    @abstractmethod
    def visit_delete(self, node: ast.Delete, depth: int):
        pass

    @abstractmethod
    def visit_assign(self, node: ast.Assign, depth: int):
        pass

    '''
    @abstractmethod
    def visit_typealias(self, node: ast.TypeAlias, depth: int):
        pass
    '''

    @abstractmethod
    def visit_augassign(self, node: ast.AugAssign, depth: int):
        pass

    @abstractmethod
    def visit_annassign(self, node: ast.AnnAssign, depth: int):
        pass

    @abstractmethod
    def visit_for(self, node: ast.For, depth: int):
        pass

    @abstractmethod
    def visit_asyncfor(self, node: ast.AsyncFor, depth: int):
        pass

    @abstractmethod
    def visit_while(self, node: ast.While, depth: int):
        pass

    @abstractmethod
    def visit_if(self, node: ast.If, depth: int):
        pass

    @abstractmethod
    def visit_with(self, node: ast.With, depth: int):
        pass

    @abstractmethod
    def visit_asyncwith(self, node: ast.AsyncWith, depth: int):
        pass

    @abstractmethod
    def visit_match(self, node: ast.Match, depth: int):
        pass

    @abstractmethod
    def visit_raise(self, node: ast.Raise, depth: int):
        pass

    @abstractmethod
    def visit_try(self, node: ast.Try, depth: int):
        pass

    @abstractmethod
    def visit_trystar(self, node: ast.Try, depth: int):
        pass

    @abstractmethod
    def visit_assert(self, node: ast.Assert, depth: int):
        pass

    @abstractmethod
    def visit_global(self, node: ast.Global, depth: int):
        pass

    @abstractmethod
    def visit_nonlocal(self, node: ast.Nonlocal, depth: int):
        pass

    @abstractmethod
    def visit_pass(self, node: ast.Pass, depth: int):
        pass

    @abstractmethod
    def visit_break(self, node: ast.Break, depth: int):
        pass

    @abstractmethod
    def visit_continue(self, node: ast.Continue, depth: int):
        pass

    ############################ IMPORTS ##################################

    @abstractmethod
    def visit_import(self, node: ast.Import, depth: int):
        pass

    @abstractmethod
    def visit_importfrom(self, node: ast.ImportFrom, depth: int):
        pass

    ############################ EXPRESSIONS ##################################

    @abstractmethod
    def visit_boolop(self, node: ast.BoolOp, depth: int):
        pass

    @abstractmethod
    def visit_namedexpr(self, node: ast.NamedExpr, depth: int):
        pass

    @abstractmethod
    def visit_binop(self, node: ast.BinOp, depth: int):
        pass

    @abstractmethod
    def visit_unaryop(self, node: ast.UnaryOp, depth: int):
        pass

    @abstractmethod
    def visit_lambda(self, node: ast.Lambda, depth: int):
        pass

    @abstractmethod
    def visit_ifexp(self, node: ast.IfExp, depth: int):
        pass

    ######################### COMPREHENSIONS #############################

    @abstractmethod
    def visit_listcomp(self, node: ast.ListComp, depth: int):
        pass

    @abstractmethod
    def visit_setcomp(self, node: ast.SetComp, depth: int):
        pass

    @abstractmethod
    def visit_dictcomp(self, node: ast.DictComp, depth: int):
        pass

    @abstractmethod
    def visit_generatorexp(self, node: ast.GeneratorExp, depth: int):
        pass

    ######################################################################

    @abstractmethod
    def visit_await(self, node: ast.Await, depth: int):
        pass

    @abstractmethod
    def visit_yield(self, node: ast.Yield, depth: int):
        pass

    @abstractmethod
    def visit_yieldfrom(self, node: ast.YieldFrom, depth: int):
        pass

    @abstractmethod
    def visit_compare(self, node: ast.Compare, depth: int):
        pass

    ########################## call_args ###########################

    @abstractmethod
    def visit_call(self, node: ast.Call, depth: int):
        pass

    ################################################################

    @abstractmethod
    def visit_formattedvalue(self, node: ast.FormattedValue, depth: int):
        pass

    ########################### F-strings #####################################

    @abstractmethod
    def visit_joinedstr(self, node: ast.JoinedStr, depth: int):
        pass

    ###########################################################################

    @abstractmethod
    def visit_constant(self, node: ast.Constant, depth: int):
        pass

    @abstractmethod
    def visit_attribute(self, node: ast.Attribute, depth: int):
        pass

    @abstractmethod
    def visit_subscript(self, node: ast.Subscript, depth: int):
        pass

    @abstractmethod
    def visit_starred(self, node: ast.Starred, depth: int):
        pass

    ############################# Variable ##################################

    @abstractmethod
    def visit_name(self, node: ast.Name, depth: int):
        pass

    ############################### Vectors #################################

    @abstractmethod
    def visit_list(self, node: ast.List, depth: int):
        pass

    @abstractmethod
    def visit_tuple(self, node: ast.Tuple, depth: int):
        pass

    @abstractmethod
    def visit_dict(self, node: ast.Dict, depth: int):
        pass

    @abstractmethod
    def visit_set(self, node: ast.Set, depth: int):
        pass

    ########################################################################

    @abstractmethod
    def visit_slice(self, node: ast.Slice, depth: int):
        pass

    @abstractmethod
    def visit_excepthandler(self, node: ast.ExceptHandler, depth: int):
        pass

    ############################### Cases ###################################

    @abstractmethod
    def visit_matchvalue(self, node: ast.MatchValue, depth: int):
        pass

    @abstractmethod
    def visit_matchsingleton(self, node: ast.MatchSingleton, depth: int):
        pass

    @abstractmethod
    def visit_matchsequence(self, node: ast.MatchSequence, depth: int):
        pass

    @abstractmethod
    def visit_matchmapping(self, node: ast.MatchMapping, depth: int):
        pass

    @abstractmethod
    def visit_matchclass(self, node: ast.MatchClass, depth: int):
        pass

    @abstractmethod
    def visit_matchstar(self, node: ast.MatchStar, depth: int):
        pass

    @abstractmethod
    def visit_matchas(self, node: ast.MatchAs, depth: int):
        pass

    @abstractmethod
    def visit_matchor(self, node: ast.MatchOr, depth: int):
        pass