from abc import ABC, abstractmethod
import ast
from typing import Dict


class Visitor(ABC):
    @abstractmethod
    def visit_Module(self, node: ast.Module, params: Dict):
        pass

    @abstractmethod
    def visit_FunctionDef(self, node: ast.FunctionDef, params: Dict):
        pass

    @abstractmethod
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef, params: Dict):
        pass

    @abstractmethod
    def visit_ClassDef(self, node: ast.ClassDef, params: Dict):
        pass

    ############################### STATEMENTS #############################
    @abstractmethod
    def visit_Return(self, node: ast.Return, params: Dict):
        pass

    @abstractmethod
    def visit_Delete(self, node: ast.Delete, params: Dict):
        pass

    @abstractmethod
    def visit_Assign(self, node: ast.Assign, params: Dict):
        pass

    @abstractmethod
    def visit_TypeAlias(self, node: ast.TypeAlias, params: Dict):
        pass

    @abstractmethod
    def visit_AugAssign(self, node: ast.AugAssign, params: Dict):
        pass

    @abstractmethod
    def visit_AnnAssign(self, node: ast.AnnAssign, params: Dict):
        pass

    @abstractmethod
    def visit_For(self, node: ast.For, params: Dict):
        pass

    @abstractmethod
    def visit_AsyncFor(self, node: ast.AsyncFor, params: Dict):
        pass

    @abstractmethod
    def visit_While(self, node: ast.While, params: Dict):
        pass

    @abstractmethod
    def visit_If(self, node: ast.If, params: Dict):
        pass

    @abstractmethod
    def visit_With(self, node: ast.With, params: Dict):
        pass

    @abstractmethod
    def visit_AsyncWith(self, node: ast.AsyncWith, params: Dict):
        pass

    @abstractmethod
    def visit_Match(self, node: ast.Match, params: Dict):
        pass

    @abstractmethod
    def visit_Raise(self, node: ast.Raise, params: Dict):
        pass

    @abstractmethod
    def visit_Try(self, node: ast.Try, params: Dict):
        pass

    @abstractmethod
    def visit_TryStar(self, node: ast.TryStar, params: Dict):
        pass

    @abstractmethod
    def visit_Assert(self, node: ast.Assert, params: Dict):
        pass

    @abstractmethod
    def visit_Global(self, node: ast.Global, params: Dict):
        pass

    @abstractmethod
    def visit_NonLocal(self, node: ast.Nonlocal, params: Dict):
        pass

    @abstractmethod
    def visit_Pass(self, node: ast.Pass, params: Dict):
        pass

    @abstractmethod
    def visit_Break(self, node: ast.Break, params: Dict):
        pass

    @abstractmethod
    def visit_Continue(self, node: ast.Continue, params: Dict):
        pass

    ############################ IMPORTS ##################################
    @abstractmethod
    def visit_Import(self, node: ast.Import, params: Dict):
        pass

    @abstractmethod
    def visit_ImportFrom(self, node: ast.ImportFrom, params: Dict):
        pass

    ############################ EXPRESSIONS ##################################
    @abstractmethod
    def visit_BoolOp(self, node: ast.BoolOp, params: Dict):
        pass

    @abstractmethod
    def visit_NamedExpr(self, node: ast.NamedExpr, params: Dict):
        pass

    @abstractmethod
    def visit_BinOp(self, node: ast.BinOp, params: Dict):
        pass

    @abstractmethod
    def visit_UnaryOp(self, node: ast.UnaryOp, params: Dict):
        pass

    @abstractmethod
    def visit_Lambda(self, node: ast.Lambda, params: Dict):
        pass

    @abstractmethod
    def visit_IfExp(self, node: ast.IfExp, params: Dict):
        pass

    ######################### COMPREHENSIONS #############################
    @abstractmethod
    def visit_ListComp(self, node: ast.ListComp, params: Dict):
        pass

    @abstractmethod
    def visit_SetComp(self, node: ast.SetComp, params: Dict):
        pass

    @abstractmethod
    def visit_DictComp(self, node: ast.DictComp, params: Dict):
        pass

    @abstractmethod
    def visit_GeneratorExp(self, node: ast.GeneratorExp, params: Dict):
        pass

    @abstractmethod
    def visit_Await(self, node: ast.Await, params: Dict):
        pass

    @abstractmethod
    def visit_Yield(self, node: ast.Yield, params: Dict):
        pass

    @abstractmethod
    def visit_YieldFrom(self, node: ast.YieldFrom, params: Dict):
        pass

    @abstractmethod
    def visit_Compare(self, node: ast.Compare, params: Dict):
        pass

    ########################## call ###########################
    @abstractmethod
    def visit_Call(self, node: ast.Call, params: Dict):
        pass

    @abstractmethod
    def visit_FormattedValue(self, node: ast.FormattedValue, params: Dict):
        pass

    ########################### F-strings #####################################
    @abstractmethod
    def visit_JoinedStr(self, node: ast.JoinedStr, params: Dict):
        pass

    ###########################################################################

    @abstractmethod
    def visit_Constant(self, node: ast.Constant, params: Dict):
        pass

    @abstractmethod
    def visit_Attribute(self, node: ast.Attribute, params: Dict):
        pass

    @abstractmethod
    def visit_Subscript(self, node: ast.Subscript, params: Dict):
        pass

    @abstractmethod
    def visit_Starred(self, node: ast.Starred, params: Dict):
        pass

    ############################# Variable ##################################
    @abstractmethod
    def visit_Name(self, node: ast.Name, params: Dict):
        pass

    ############################### Vectors #################################
    @abstractmethod
    def visit_List(self, node: ast.List, params: Dict):
        pass

    @abstractmethod
    def visit_Tuple(self, node: ast.Tuple, params: Dict):
        pass

    @abstractmethod
    def visit_Dict(self, node: ast.Dict, params: Dict):
        pass

    @abstractmethod
    def visit_Set(self, node: ast.Set, params: Dict):
        pass

    @abstractmethod
    def visit_Slice(self, node: ast.Slice, params: Dict):
        pass

    @abstractmethod
    def visit_ExceptHandler(self, node: ast.ExceptHandler, params: Dict):
        pass

    ############################### Cases ###################################
    @abstractmethod
    def visit_MatchValue(self, node: ast.MatchValue, params: Dict):
        pass

    @abstractmethod
    def visit_MatchSingleton(self, node: ast.MatchSingleton, params: Dict):
        pass

    @abstractmethod
    def visit_MatchSequence(self, node: ast.MatchSequence, params: Dict):
        pass

    @abstractmethod
    def visit_MatchMapping(self, node: ast.MatchMapping, params: Dict):
        pass

    @abstractmethod
    def visit_MatchClass(self, node: ast.MatchClass, params: Dict):
        pass

    @abstractmethod
    def visit_MatchStar(self, node: ast.MatchStar, params: Dict):
        pass

    @abstractmethod
    def visit_MatchAs(self, node: ast.MatchAs, params: Dict):
        pass

    @abstractmethod
    def visit_MatchOr(self, node: ast.MatchOr, params: Dict):
        pass
