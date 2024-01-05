import ast
from visitors.visitor import Visitor

####### SPECIAL ACCEPTS ##########

def accept_expr(self, visitor, depth):
    self.value.accept(visitor,depth)

ast.Expr.accept = accept_expr

##################################

def accept_module(self, visitor, depth):
    visitor.visit_module(self, depth)

def accept_functiondef(self, visitor, depth):
    visitor.visit_functiondef(self, depth)

def accept_asyncfunctiondef(self, visitor, depth):
    visitor.visit_asyncfunctiondef(self, depth)

def accept_classdef(self, visitor, depth):
    visitor.visit_classdef(self, depth)

def accept_return(self, visitor, depth):
    visitor.visit_return(self, depth)

def accept_delete(self, visitor, depth):
    visitor.visit_delete(self, depth)

def accept_assign(self, visitor, depth):
    visitor.visit_assign(self, depth)

def accept_augassign(self, visitor, depth):
    visitor.visit_augassign(self, depth)

def accept_annassign(self, visitor, depth):
    visitor.visit_annassign(self, depth)

def accept_for(self, visitor, depth):
    visitor.visit_for(self, depth)

def accept_asyncfor(self, visitor, depth):
    visitor.visit_asyncfor(self, depth)

def accept_while(self, visitor, depth):
    visitor.visit_while(self, depth)

def accept_if(self, visitor, depth):
    visitor.visit_if(self, depth)

def accept_with(self, visitor, depth):
    visitor.visit_with(self, depth)

def accept_asyncwith(self, visitor, depth):
    visitor.visit_asyncwith(self, depth)

def accept_match(self, visitor, depth):
    visitor.visit_match(self, depth)

def accept_raise(self, visitor, depth):
    visitor.visit_raise(self, depth)

def accept_try(self, visitor, depth):
    visitor.visit_try(self, depth)

def accept_trystar(self, visitor, depth):
    visitor.visit_trystar(self, depth)

def accept_assert(self, visitor, depth):
    visitor.visit_assert(self, depth)

def accept_global(self, visitor, depth):
    visitor.visit_global(self, depth)

def accept_nonlocal(self, visitor, depth):
    visitor.visit_nonlocal(self, depth)

def accept_pass(self, visitor, depth):
    visitor.visit_pass(self, depth)

def accept_break(self, visitor, depth):
    visitor.visit_break(self, depth)

def accept_continue(self, visitor, depth):
    visitor.visit_continue(self, depth)

def accept_import(self, visitor, depth):
    visitor.visit_import(self, depth)

def accept_importfrom(self, visitor, depth):
    visitor.visit_importfrom(self, depth)

def accept_boolop(self, visitor, depth):
    visitor.visit_boolop(self, depth)

def accept_namedexpr(self, visitor, depth):
    visitor.visit_namedexpr(self, depth)

def accept_binop(self, visitor, depth):
    visitor.visit_binop(self, depth)

def accept_unaryop(self, visitor, depth):
    visitor.visit_unaryop(self, depth)

def accept_lambda(self, visitor, depth):
    visitor.visit_lambda(self, depth)

def accept_ifexp(self, visitor, depth):
    visitor.visit_ifexp(self, depth)

def accept_listcomp(self, visitor, depth):
    visitor.visit_listcomp(self, depth)

def accept_setcomp(self, visitor, depth):
    visitor.visit_setcomp(self, depth)

def accept_dictcomp(self, visitor, depth):
    visitor.visit_dictcomp(self, depth)

def accept_generatorexp(self, visitor, depth):
    visitor.visit_generatorexp(self, depth)

def accept_await(self, visitor, depth):
    visitor.visit_await(self, depth)

def accept_yield(self, visitor, depth):
    visitor.visit_yield(self, depth)

def accept_yieldfrom(self, visitor, depth):
    visitor.visit_yieldfrom(self, depth)

def accept_compare(self, visitor, depth):
    visitor.visit_compare(self, depth)

def accept_call(self, visitor, depth):
    visitor.visit_call(self, depth)

def accept_formattedvalue(self, visitor, depth):
    visitor.visit_formattedvalue(self, depth)

def accept_joinedstr(self, visitor, depth):
    visitor.visit_joinedstr(self, depth)

def accept_constant(self, visitor, depth):
    visitor.visit_constant(self, depth)

def accept_attribute(self, visitor, depth):
    visitor.visit_attribute(self, depth)

def accept_subscript(self, visitor, depth):
    visitor.visit_subscript(self, depth)

def accept_starred(self, visitor, depth):
    visitor.visit_starred(self, depth)

def accept_name(self, visitor, depth):
    visitor.visit_name(self, depth)

def accept_list(self, visitor, depth):
    visitor.visit_list(self, depth)

def accept_tuple(self, visitor, depth):
    visitor.visit_tuple(self, depth)

def accept_dict(self, visitor, depth):
    visitor.visit_dict(self, depth)

def accept_set(self, visitor, depth):
    visitor.visit_set(self, depth)

def accept_slice(self, visitor, depth):
    visitor.visit_slice(self, depth)

def accept_matchvalue(self, visitor, depth):
    visitor.visit_matchvalue(self, depth)

def accept_matchsingleton(self, visitor, depth):
    visitor.visit_matchsingleton(self, depth)

def accept_matchsequence(self, visitor, depth):
    visitor.visit_matchsequence(self, depth)

def accept_matchmapping(self, visitor, depth):
    visitor.visit_matchmapping(self, depth)

def accept_matchclass(self, visitor, depth):
    visitor.visit_matchclass(self, depth)

def accept_matchstar(self, visitor, depth):
    visitor.visit_matchstar(self, depth)

def accept_matchas(self, visitor, depth):
    visitor.visit_matchas(self, depth)

def accept_matchor(self, visitor, depth):
    visitor.visit_matchor(self, depth)

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