import ast
from visitor import Visitor


####### SPECIAL ACCEPTS ##########
def accept_Expr(self, visitor, params):
    self.value.accept(visitor, params)


def accept_Module(self, visitor, params):
    visitor.visit_Module(self, params)


def accept_FunctionDef(self, visitor, params):
    visitor.visit_FunctionDef(self, params)


def accept_AsyncFunctionDef(self, visitor, params):
    visitor.visit_AsyncFunctionDef(self, params)


def accept_ClassDef(self, visitor, params):
    visitor.visit_ClassDef(self, params)


def accept_Return(self, visitor, params):
    visitor.visit_Return(self, params)


def accept_Delete(self, visitor, params):
    visitor.visit_Delete(self, params)


def accept_Assign(self, visitor, params):
    visitor.visit_Assign(self, params)


def accept_AugAssign(self, visitor, params):
    visitor.visit_AugAssign(self, params)


def accept_AnnAssign(self, visitor, params):
    visitor.visit_AnnAssign(self, params)


def accept_For(self, visitor, params):
    visitor.visit_For(self, params)


def accept_AsyncFor(self, visitor, params):
    visitor.visit_AsyncFor(self, params)


def accept_While(self, visitor, params):
    visitor.visit_While(self, params)


def accept_If(self, visitor, params):
    visitor.visit_If(self, params)


def accept_With(self, visitor, params):
    visitor.visit_With(self, params)


def accept_AsyncWith(self, visitor, params):
    visitor.visit_AsyncWith(self, params)


def accept_Match(self, visitor, params):
    visitor.visit_Match(self, params)


def accept_Raise(self, visitor, params):
    visitor.visit_Raise(self, params)


def accept_Try(self, visitor, params):
    visitor.visit_Try(self, params)


def accept_TryStar(self, visitor, params):
    visitor.visit_TryStar(self, params)


def accept_Assert(self, visitor, params):
    visitor.visit_Assert(self, params)


def accept_Global(self, visitor, params):
    visitor.visit_Global(self, params)


def accept_NonLocal(self, visitor, params):
    visitor.visit_NonLocal(self, params)


def accept_Pass(self, visitor, params):
    visitor.visit_Pass(self, params)


def accept_Break(self, visitor, params):
    visitor.visit_Break(self, params)


def accept_Continue(self, visitor, params):
    visitor.visit_Continue(self, params)


def accept_Import(self, visitor, params):
    visitor.visit_Import(self, params)


def accept_ImportFrom(self, visitor, params):
    visitor.visit_ImportFrom(self, params)


def accept_BoolOp(self, visitor, params):
    visitor.visit_BoolOp(self, params)


def accept_NamedExpr(self, visitor, params):
    visitor.visit_NamedExpr(self, params)


def accept_BinOp(self, visitor, params):
    visitor.visit_BinOp(self, params)


def accept_UnaryOp(self, visitor, params):
    visitor.visit_UnaryOp(self, params)


def accept_Lambda(self, visitor, params):
    visitor.visit_Lambda(self, params)


def accept_IfExp(self, visitor, params):
    visitor.visit_IfExp(self, params)


def accept_ListComp(self, visitor, params):
    visitor.visit_ListComp(self, params)


def accept_SetComp(self, visitor, params):
    visitor.visit_SetComp(self, params)


def accept_DictComp(self, visitor, params):
    visitor.visit_DictComp(self, params)


def accept_GeneratorExp(self, visitor, params):
    visitor.visit_GeneratorExp(self, params)


def accept_Await(self, visitor, params):
    visitor.visit_Await(self, params)


def accept_Yield(self, visitor, params):
    visitor.visit_Yield(self, params)


def accept_YieldFrom(self, visitor, params):
    visitor.visit_YieldFrom(self, params)


def accept_Compare(self, visitor, params):
    visitor.visit_Compare(self, params)


def accept_Call(self, visitor, params):
    visitor.visit_Call(self, params)


def accept_FormattedValue(self, visitor, params):
    visitor.visit_FormattedValue(self, params)


def accept_JoinedStr(self, visitor, params):
    visitor.visit_JoinedStr(self, params)


def accept_Constant(self, visitor, params):
    visitor.visit_Constant(self, params)


def accept_Attribute(self, visitor, params):
    visitor.visit_Attribute(self, params)


def accept_Subscript(self, visitor, params):
    visitor.visit_Subscript(self, params)


def accept_Starred(self, visitor, params):
    visitor.visit_Starred(self, params)


def accept_Name(self, visitor, params):
    visitor.visit_Name(self, params)


def accept_List(self, visitor, params):
    visitor.visit_List(self, params)


def accept_Tuple(self, visitor, params):
    visitor.visit_Tuple(self, params)


def accept_Dict(self, visitor, params):
    visitor.visit_Dict(self, params)


def accept_Set(self, visitor, params):
    visitor.visit_Set(self, params)


def accept_Slice(self, visitor, params):
    visitor.visit_Slice(self, params)


def accept_MatchValue(self, visitor, params):
    visitor.visit_MatchValue(self, params)


def accept_MatchSingleton(self, visitor, params):
    visitor.visit_MatchSingleton(self, params)


def accept_MatchSequence(self, visitor, params):
    visitor.visit_MatchSequence(self, params)


def accept_MatchMapping(self, visitor, params):
    visitor.visit_MatchMapping(self, params)


def accept_MatchClass(self, visitor, params):
    visitor.visit_MatchClass(self, params)


def accept_MatchStar(self, visitor, params):
    visitor.visit_MatchStar(self, params)


def accept_MatchAs(self, visitor, params):
    visitor.visit_MatchAs(self, params)


def accept_MatchOr(self, visitor, params):
    visitor.visit_MatchOr(self, params)


# Add accept methods to ast module classes
ast.Expr.accept = accept_Expr
ast.Module.accept = accept_Module
ast.FunctionDef.accept = accept_FunctionDef
ast.AsyncFunctionDef.accept = accept_AsyncFunctionDef
ast.ClassDef.accept = accept_ClassDef
ast.Return.accept = accept_Return
ast.Delete.accept = accept_Delete
ast.Assign.accept = accept_Assign
ast.AugAssign.accept = accept_AugAssign
ast.AnnAssign.accept = accept_AnnAssign
ast.For.accept = accept_For
ast.AsyncFor.accept = accept_AsyncFor
ast.While.accept = accept_While
ast.If.accept = accept_If
ast.With.accept = accept_With
ast.AsyncWith.accept = accept_AsyncWith
ast.Match.accept = accept_Match
ast.Raise.accept = accept_Raise
ast.Try.accept = accept_Try
ast.Try.accept = accept_TryStar
ast.Assert.accept = accept_Assert
ast.Global.accept = accept_Global
ast.Nonlocal.accept = accept_NonLocal
ast.Pass.accept = accept_Pass
ast.Break.accept = accept_Break
ast.Continue.accept = accept_Continue
ast.Import.accept = accept_Import
ast.ImportFrom.accept = accept_ImportFrom
ast.BoolOp.accept = accept_BoolOp
ast.NamedExpr.accept = accept_NamedExpr
ast.BinOp.accept = accept_BinOp
ast.UnaryOp.accept = accept_UnaryOp
ast.Lambda.accept = accept_Lambda
ast.IfExp.accept = accept_IfExp
ast.ListComp.accept = accept_ListComp
ast.SetComp.accept = accept_SetComp
ast.DictComp.accept = accept_DictComp
ast.GeneratorExp.accept = accept_GeneratorExp
ast.Await.accept = accept_Await
ast.Yield.accept = accept_Yield
ast.YieldFrom.accept = accept_YieldFrom
ast.Compare.accept = accept_Compare
ast.Call.accept = accept_Call
ast.FormattedValue.accept = accept_FormattedValue
ast.JoinedStr.accept = accept_JoinedStr
ast.Constant.accept = accept_Constant
ast.Attribute.accept = accept_Attribute
ast.Subscript.accept = accept_Subscript
ast.Starred.accept = accept_Starred
ast.Name.accept = accept_Name
ast.List.accept = accept_List
ast.Tuple.accept = accept_Tuple
ast.Dict.accept = accept_Dict
ast.Set.accept = accept_Set
ast.Slice.accept = accept_Slice
ast.MatchValue.accept = accept_MatchValue
ast.MatchSingleton.accept = accept_MatchSingleton
ast.MatchSequence.accept = accept_MatchSequence
ast.MatchMapping.accept = accept_MatchMapping
ast.MatchClass.accept = accept_MatchClass
ast.MatchStar.accept = accept_MatchStar
ast.MatchAs.accept = accept_MatchAs
ast.MatchOr.accept = accept_MatchOr
