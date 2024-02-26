import ast
from visitor import Visitor

####### SPECIAL ACCEPTS ##########

def accept_expr(self, visitor, params):
    self.value.accept(visitor, params)

ast.Expr.accept = accept_expr

##################################

def accept_module(self, visitor, params):
    visitor.visit_Module(self, params)

def accept_functiondef(self, visitor, params):
    visitor.visit_FunctionDef(self, params)

def accept_asyncfunctiondef(self, visitor, params):
    visitor.visit_AsyncFunctionDef(self, params)

def accept_classdef(self, visitor, params):
    visitor.visit_ClassDef(self, params)

def accept_return(self, visitor, params):
    visitor.visit_Return(self, params)

def accept_delete(self, visitor, params):
    visitor.visit_Delete(self, params)

def accept_assign(self, visitor, params):
    visitor.visit_Assign(self, params)

def accept_augassign(self, visitor, params):
    visitor.visit_AugAssign(self, params)

def accept_annassign(self, visitor, params):
    visitor.visit_AnnAssign(self, params)

def accept_for(self, visitor, params):
    visitor.visit_For(self, params)

def accept_asyncfor(self, visitor, params):
    visitor.visit_AsyncFor(self, params)

def accept_while(self, visitor, params):
    visitor.visit_While(self, params)

def accept_if(self, visitor, params):
    visitor.visit_if(self, params)

def accept_with(self, visitor, params):
    visitor.visit_with(self, params)

def accept_asyncwith(self, visitor, params):
    visitor.visit_asyncwith(self, params)

def accept_match(self, visitor, params):
    visitor.visit_match(self, params)

def accept_raise(self, visitor, params):
    visitor.visit_raise(self, params)

def accept_try(self, visitor, params):
    visitor.visit_try(self, params)

def accept_trystar(self, visitor, params):
    visitor.visit_trystar(self, params)

def accept_assert(self, visitor, params):
    visitor.visit_assert(self, params)

def accept_global(self, visitor, params):
    visitor.visit_global(self, params)

def accept_nonlocal(self, visitor, params):
    visitor.visit_nonlocal(self, params)

def accept_pass(self, visitor, params):
    visitor.visit_pass(self, params)

def accept_break(self, visitor, params):
    visitor.visit_break(self, params)

def accept_continue(self, visitor, params):
    visitor.visit_continue(self, params)

def accept_import(self, visitor, params):
    visitor.visit_import(self, params)

def accept_importfrom(self, visitor, params):
    visitor.visit_importfrom(self, params)

def accept_boolop(self, visitor, params):
    visitor.visit_boolop(self, params)

def accept_namedexpr(self, visitor, params):
    visitor.visit_namedexpr(self, params)

def accept_binop(self, visitor, params):
    visitor.visit_binop(self, params)

def accept_unaryop(self, visitor, params):
    visitor.visit_unaryop(self, params)

def accept_lambda(self, visitor, params):
    visitor.visit_lambda(self, params)

def accept_ifexp(self, visitor, params):
    visitor.visit_ifexp(self, params)

def accept_listcomp(self, visitor, params):
    visitor.visit_listcomp(self, params)

def accept_setcomp(self, visitor, params):
    visitor.visit_setcomp(self, params)

def accept_dictcomp(self, visitor, params):
    visitor.visit_dictcomp(self, params)

def accept_generatorexp(self, visitor, params):
    visitor.visit_generatorexp(self, params)

def accept_await(self, visitor, params):
    visitor.visit_await(self, params)

def accept_yield(self, visitor, params):
    visitor.visit_yield(self, params)

def accept_yieldfrom(self, visitor, params):
    visitor.visit_yieldfrom(self, params)

def accept_compare(self, visitor, params):
    visitor.visit_compare(self, params)

def accept_call(self, visitor, params):
    visitor.visit_call(self, params)

def accept_formattedvalue(self, visitor, params):
    visitor.visit_formattedvalue(self, params)

def accept_joinedstr(self, visitor, params):
    visitor.visit_joinedstr(self, params)

def accept_constant(self, visitor, params):
    visitor.visit_constant(self, params)

def accept_attribute(self, visitor, params):
    visitor.visit_attribute(self, params)

def accept_subscript(self, visitor, params):
    visitor.visit_subscript(self, params)

def accept_starred(self, visitor, params):
    visitor.visit_starred(self, params)

def accept_name(self, visitor, params):
    visitor.visit_name(self, params)

def accept_list(self, visitor, params):
    visitor.visit_list(self, params)

def accept_tuple(self, visitor, params):
    visitor.visit_tuple(self, params)

def accept_dict(self, visitor, params):
    visitor.visit_dict(self, params)

def accept_set(self, visitor, params):
    visitor.visit_set(self, params)

def accept_slice(self, visitor, params):
    visitor.visit_slice(self, params)

def accept_matchvalue(self, visitor, params):
    visitor.visit_matchvalue(self, params)

def accept_matchsingleton(self, visitor, params):
    visitor.visit_matchsingleton(self, params)

def accept_matchsequence(self, visitor, params):
    visitor.visit_matchsequence(self, params)

def accept_matchmapping(self, visitor, params):
    visitor.visit_matchmapping(self, params)

def accept_matchclass(self, visitor, params):
    visitor.visit_matchclass(self, params)

def accept_matchstar(self, visitor, params):
    visitor.visit_matchstar(self, params)

def accept_matchas(self, visitor, params):
    visitor.visit_matchas(self, params)

def accept_matchor(self, visitor, params):
    visitor.visit_matchor(self, params)

# Agregar los métodos accept a las clases del módulo ast
ast.Module.accept = accept_module
ast.FunctionDef.accept = accept_functiondef
ast.AsyncFunctionDef.accept = accept_asyncfunctiondef
ast.ClassDef.accept = accept_classdef
ast.Return.accept = accept_return
ast.Delete.accept = accept_delete
ast.Assign.accept = accept_assign
ast.AugAssign.accept = accept_augassign
ast.AnnAssign.accept = accept_annassign
ast.For.accept = accept_for
ast.AsyncFor.accept = accept_asyncfor
ast.While.accept = accept_while
ast.If.accept = accept_if
ast.With.accept = accept_with
ast.AsyncWith.accept = accept_asyncwith
ast.Match.accept = accept_match
ast.Raise.accept = accept_raise
ast.Try.accept = accept_try
ast.Try.accept = accept_trystar
ast.Assert.accept = accept_assert
ast.Global.accept = accept_global
ast.Nonlocal.accept = accept_nonlocal
ast.Pass.accept = accept_pass
ast.Break.accept = accept_break
ast.Continue.accept = accept_continue
ast.Import.accept = accept_import
ast.ImportFrom.accept = accept_importfrom
ast.BoolOp.accept = accept_boolop
ast.NamedExpr.accept = accept_namedexpr
ast.BinOp.accept = accept_binop
ast.UnaryOp.accept = accept_unaryop
ast.Lambda.accept = accept_lambda
ast.IfExp.accept = accept_ifexp
ast.ListComp.accept = accept_listcomp
ast.SetComp.accept = accept_setcomp
ast.DictComp.accept = accept_dictcomp
ast.GeneratorExp.accept = accept_generatorexp
ast.Await.accept = accept_await
ast.Yield.accept = accept_yield
ast.YieldFrom.accept = accept_yieldfrom
ast.Compare.accept = accept_compare
ast.Call.accept = accept_call
ast.FormattedValue.accept = accept_formattedvalue
ast.JoinedStr.accept = accept_joinedstr
ast.Constant.accept = accept_constant
ast.Attribute.accept = accept_attribute
ast.Subscript.accept = accept_subscript
ast.Starred.accept = accept_starred
ast.Name.accept = accept_name
ast.List.accept = accept_list
ast.Tuple.accept = accept_tuple
ast.Dict.accept = accept_dict
ast.Set.accept = accept_set
ast.Slice.accept = accept_slice
ast.MatchValue.accept = accept_matchvalue
ast.MatchSingleton.accept = accept_matchsingleton
ast.MatchSequence.accept = accept_matchsequence
ast.MatchMapping.accept = accept_matchmapping
ast.MatchClass.accept = accept_matchclass
ast.MatchStar.accept = accept_matchstar
ast.MatchAs.accept = accept_matchas
ast.MatchOr.accept = accept_matchor