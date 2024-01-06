import ast
from visitors.visitor import Visitor

####### SPECIAL ACCEPTS ##########

def accept_expr(self, visitor, params, depth):
    self.value.accept(visitor, params, depth)

ast.Expr.accept = accept_expr

##################################

def accept_module(self, visitor, params, depth):
    visitor.visit_module(self, params, depth)

def accept_functiondef(self, visitor, params, depth):
    visitor.visit_functiondef(self, params, depth)

def accept_asyncfunctiondef(self, visitor, params, depth):
    visitor.visit_asyncfunctiondef(self, params, depth)

def accept_classdef(self, visitor, params, depth):
    visitor.visit_classdef(self, params, depth)

def accept_return(self, visitor, params, depth):
    visitor.visit_return(self, params, depth)

def accept_delete(self, visitor, params, depth):
    visitor.visit_delete(self, params, depth)

def accept_assign(self, visitor, params, depth):
    visitor.visit_assign(self, params, depth)

def accept_augassign(self, visitor, params, depth):
    visitor.visit_augassign(self, params, depth)

def accept_annassign(self, visitor, params, depth):
    visitor.visit_annassign(self, params, depth)

def accept_for(self, visitor, params, depth):
    visitor.visit_for(self, params, depth)

def accept_asyncfor(self, visitor, params, depth):
    visitor.visit_asyncfor(self, params, depth)

def accept_while(self, visitor, params, depth):
    visitor.visit_while(self, params, depth)

def accept_if(self, visitor, params, depth):
    visitor.visit_if(self, params, depth)

def accept_with(self, visitor, params, depth):
    visitor.visit_with(self, params, depth)

def accept_asyncwith(self, visitor, params, depth):
    visitor.visit_asyncwith(self, params, depth)

def accept_match(self, visitor, params, depth):
    visitor.visit_match(self, params, depth)

def accept_raise(self, visitor, params, depth):
    visitor.visit_raise(self, params, depth)

def accept_try(self, visitor, params, depth):
    visitor.visit_try(self, params, depth)

def accept_trystar(self, visitor, params, depth):
    visitor.visit_trystar(self, params, depth)

def accept_assert(self, visitor, params, depth):
    visitor.visit_assert(self, params, depth)

def accept_global(self, visitor, params, depth):
    visitor.visit_global(self, params, depth)

def accept_nonlocal(self, visitor, params, depth):
    visitor.visit_nonlocal(self, params, depth)

def accept_pass(self, visitor, params, depth):
    visitor.visit_pass(self, params, depth)

def accept_break(self, visitor, params, depth):
    visitor.visit_break(self, params, depth)

def accept_continue(self, visitor, params, depth):
    visitor.visit_continue(self, params, depth)

def accept_import(self, visitor, params, depth):
    visitor.visit_import(self, params, depth)

def accept_importfrom(self, visitor, params, depth):
    visitor.visit_importfrom(self, params, depth)

def accept_boolop(self, visitor, params, depth):
    visitor.visit_boolop(self, params, depth)

def accept_namedexpr(self, visitor, params, depth):
    visitor.visit_namedexpr(self, params, depth)

def accept_binop(self, visitor, params, depth):
    visitor.visit_binop(self, params, depth)

def accept_unaryop(self, visitor, params, depth):
    visitor.visit_unaryop(self, params, depth)

def accept_lambda(self, visitor, params, depth):
    visitor.visit_lambda(self, params, depth)

def accept_ifexp(self, visitor, params, depth):
    visitor.visit_ifexp(self, params, depth)

def accept_listcomp(self, visitor, params, depth):
    visitor.visit_listcomp(self, params, depth)

def accept_setcomp(self, visitor, params, depth):
    visitor.visit_setcomp(self, params, depth)

def accept_dictcomp(self, visitor, params, depth):
    visitor.visit_dictcomp(self, params, depth)

def accept_generatorexp(self, visitor, params, depth):
    visitor.visit_generatorexp(self, params, depth)

def accept_await(self, visitor, params, depth):
    visitor.visit_await(self, params, depth)

def accept_yield(self, visitor, params, depth):
    visitor.visit_yield(self, params, depth)

def accept_yieldfrom(self, visitor, params, depth):
    visitor.visit_yieldfrom(self, params, depth)

def accept_compare(self, visitor, params, depth):
    visitor.visit_compare(self, params, depth)

def accept_call(self, visitor, params, depth):
    visitor.visit_call(self, params, depth)

def accept_formattedvalue(self, visitor, params, depth):
    visitor.visit_formattedvalue(self, params, depth)

def accept_joinedstr(self, visitor, params, depth):
    visitor.visit_joinedstr(self, params, depth)

def accept_constant(self, visitor, params, depth):
    visitor.visit_constant(self, params, depth)

def accept_attribute(self, visitor, params, depth):
    visitor.visit_attribute(self, params, depth)

def accept_subscript(self, visitor, params, depth):
    visitor.visit_subscript(self, params, depth)

def accept_starred(self, visitor, params, depth):
    visitor.visit_starred(self, params, depth)

def accept_name(self, visitor, params, depth):
    visitor.visit_name(self, params, depth)

def accept_list(self, visitor, params, depth):
    visitor.visit_list(self, params, depth)

def accept_tuple(self, visitor, params, depth):
    visitor.visit_tuple(self, params, depth)

def accept_dict(self, visitor, params, depth):
    visitor.visit_dict(self, params, depth)

def accept_set(self, visitor, params, depth):
    visitor.visit_set(self, params, depth)

def accept_slice(self, visitor, params, depth):
    visitor.visit_slice(self, params, depth)

def accept_matchvalue(self, visitor, params, depth):
    visitor.visit_matchvalue(self, params, depth)

def accept_matchsingleton(self, visitor, params, depth):
    visitor.visit_matchsingleton(self, params, depth)

def accept_matchsequence(self, visitor, params, depth):
    visitor.visit_matchsequence(self, params, depth)

def accept_matchmapping(self, visitor, params, depth):
    visitor.visit_matchmapping(self, params, depth)

def accept_matchclass(self, visitor, params, depth):
    visitor.visit_matchclass(self, params, depth)

def accept_matchstar(self, visitor, params, depth):
    visitor.visit_matchstar(self, params, depth)

def accept_matchas(self, visitor, params, depth):
    visitor.visit_matchas(self, params, depth)

def accept_matchor(self, visitor, params, depth):
    visitor.visit_matchor(self, params, depth)

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