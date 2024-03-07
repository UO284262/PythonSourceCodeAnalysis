import ast
from visitors.My_NodeVisitor import NodeVisitor
from typing import Dict, Self

class Visitor_print(NodeVisitor):

    def visit_Expr(self: Self, node : ast.Expr, params : Dict):
        self.visit(node.value, params)
        return 

    def visit_Module(self : Self, node : ast.Module , params : Dict) -> Dict:
        print('|->Module') 
        for child in node.body:
            self.visit(child, {'depth' : 1})
        return
    
    def visit_FunctionDef(self : Self, node : ast.FunctionDef , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->FunctionDef')
        print(('  '*(params['depth'] + 1)) + '|->Args')
        self.visit(node.args, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Decorators')
        for child in node.decorator_list:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->ReturnType')
        if(node.returns):
            self.visit(node.returns, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->TypeParams')
        for child in node.type_params:
            self.visit(child, {'depth': params['depth'] + 2})
        return
    
    def visit_AsyncFunctionDef(self : Self, node : ast.AsyncFunctionDef , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->AsyncFunctionDef')
        print(('  '*(params['depth'] + 1)) + '|->Args')
        self.visit(node.args, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Decorators')
        for child in node.decorator_list:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->ReturnType')
        if(node.returns):
            self.visit(node.returns, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->TypeParams')
        for child in node.type_params:
            self.visit(child, {'depth': params['depth'] + 2})
        return
        
    def visit_ClassDef(self : Self, node : ast.ClassDef , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->ClassDef')
        print(('  '*(params['depth'] + 1)) + '|->Bases')
        for child in node.bases:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Keywords')
        for child in node.keywords:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Decorators')
        for child in node.decorator_list:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->TypeParams')
        for child in node.type_params:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    ############################### STATEMENTS #############################

    def visit_Return(self : Self, node : ast.Return , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Return')
        if(node.value): self.visit(node.value, {'depth': params['depth'] + 1})
        return

    def visit_Delete(self : Self, node : ast.Delete , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Delete')
        for child in node.targets:
            self.visit(child, {'depth': params['depth'] + 1})
        return

    def visit_Assign(self : Self, node : ast.Assign , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Assign')
        print(('  '*(params['depth'] + 1)) + '|->Targets')
        for child in node.targets:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        return
    
    def visit_TypeAlias(self : Self, node : ast.TypeAlias , params : Dict) -> Dict:
        print(('  '*params['depth']) + '|->TypeAlias')
        print(('  '*(params['depth'] + 1)) + '|->TypeParams')
        for child in node.type_params:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Name')
        self.visit(node.name, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        return
    
    def visit_AugAssign(self : Self, node : ast.AugAssign , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->AugAssign')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.target, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        return

    def visit_AnnAssign(self : Self, node : ast.AnnAssign , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->AnnAssign')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.target, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Annotation')
        self.visit(node.annotation, {'depth': params['depth'] + 2})
        if(node.value): 
            print(('  '*(params['depth'] + 1)) + '|->Value')
            self.visit(node.value, {'depth': params['depth'] + 2})
        return

    def visit_For(self : Self, node : ast.For , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->For')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.target, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Iter')
        self.visit(node.iter, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->OrElse')
        for child in node.orelse:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_AsyncFor(self : Self, node : ast.AsyncFor , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->AsyncFor')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.target, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Iter')
        self.visit(node.iter, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->OrElse')
        for child in node.orelse:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_While(self : Self, node : ast.While , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->While')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.test, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->OrElse')
        for child in node.orelse:
            self.visit(child, {'depth': params['depth'] + 2})
        return


    def visit_If(self : Self, node : ast.If , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->If')
        self.visit(node.test, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->OrElse')
        for child in node.orelse:
            self.visit(child, {'depth': params['depth'] + 2})
        return


    def visit_With(self : Self, node : ast.With , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->With')
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Items')
        for child in node.items:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_AsyncWith(self : Self, node : ast.AsyncWith , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->AsyncWith')
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Items')
        for child in node.items:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_Match(self : Self, node : ast.Match , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Matc')
        print(('  '*(params['depth'] + 1)) + '|->Subject')
        self.visit(node.subject, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Cases')
        for child in node.cases:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_Raise(self : Self, node : ast.Raise , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Raise')
        ############## PROPAGAR VISIT ############
        if(node.exc):
            print(('  '*(params['depth'] + 1)) + '|->Exc')
            self.visit(node.exc, {'depth': params['depth'] + 2})
        if(node.cause): 
            print(('  '*(params['depth'] + 1)) + '|->Cause')
            self.visit(node.cause, {'depth': params['depth'] + 2})
        return
    
    def visit_Try(self : Self, node : ast.Try , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Try')
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Handlers')
        for child in node.handlers:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->OrElse')
        for child in node.orelse:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->FinalBody')
        for child in node.finalbody:
            self.visit(child, {'depth': params['depth'] + 2})
        return
    
    def visit_TryStar(self : Self, node : ast.TryStar , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Try')
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Handlers')
        for child in node.handlers:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->OrElse')
        for child in node.orelse:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->FinalBody')
        for child in node.finalbody:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_Assert(self : Self, node : ast.Assert , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Try')
        print(('  '*(params['depth'] + 1)) + '|->Test')
        self.visit(node.test, {'depth': params['depth'] + 2})
        if(node.msg):
            print(('  '*(params['depth'] + 1)) + '|->Msg')
            self.visit(node.msg, {'depth': params['depth'] + 2})
        return

    
    def visit_Global(self : Self, node : ast.Global , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Global')
        print(('  '*(params['depth'] + 1)) + '|->Names')
        for name in node.names:
            print(('  '*(params['depth'] + 2)) + '|->' + name)
        return

    
    def visit_Nonlocal(self : Self, node : ast.Nonlocal , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->NonLocal')
        print(('  '*(params['depth'] + 1)) + '|->Names')
        for name in node.names:
            print(('  '*(params['depth'] + 2)) + '|->' + name)
        return

    
    def visit_Pass(self : Self, node : ast.Pass , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Pass')
        return

    
    def visit_Break(self : Self, node : ast.Break , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Break')
        return

    
    def visit_Continue(self : Self, node : ast.Continue , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Continue')
        return

    ############################ IMPORTS ##################################

    
    def visit_Import(self : Self, node : ast.Import , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Import')
        print(('  '*(params['depth'] + 1)) + '|->Names')
        for alias in node.names:
            print(('  '*(params['depth'] + 2)) + '|->' + alias.name)
        return

    
    def visit_ImportFrom(self : Self, node : ast.ImportFrom , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Import')
        if node.module:
            print(('  '*(params['depth'] + 1)) + '|->Module')
            print(('  '*(params['depth'] + 2)) + '|->' + node.module)
        print(('  '*(params['depth'] + 1)) + '|->Names')
        for alias in node.names:
            print(('  '*(params['depth'] + 2)) + '|->' + alias.name)
        return

    ############################ EXPRESSIONS ##################################

    def visit_BoolOp(self : Self, node : ast.BoolOp , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->BoolOp')
        print(('  '*(params['depth'] + 1)) + '|->Operator')
        print(('  '*(params['depth'] + 2)) + '|->' + node.op.__doc__)
        print(('  '*(params['depth'] + 1)) + '|->Values')
        for child in node.values:
            self.visit(child, {'depth': params['depth'] + 2})       
        return

    
    def visit_NamedExpr(self : Self, node : ast.NamedExpr , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->NamedExpr')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.target, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        return

    
    def visit_BinOp(self : Self, node : ast.BinOp , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->BinOp')
        print(('  '*(params['depth'] + 1)) + '|->Operator')   
        print(('  '*(params['depth'] + 2)) + '|->' + node.op.__doc__)
        print(('  '*(params['depth'] + 1)) + '|->Left')
        self.visit(node.left, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Right')
        self.visit(node.right, {'depth': params['depth'] + 2})
        return
    
    
    def visit_UnaryOp(self : Self, node : ast.UnaryOp , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->UnaryOp')
        print(('  '*(params['depth'] + 1)) + '|->Operator')
        print(('  '*(params['depth'] + 2)) + '|->' + node.op.__doc__)
        print(('  '*(params['depth'] + 1)) + '|->Operand')
        self.visit(node.operand, {'depth': params['depth'] + 2})
        return
    
    
    def visit_Lambda(self : Self, node : ast.Lambda , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Lambda')
        print(('  '*(params['depth'] + 1)) + '|->Arguments')
        self.visit(node.args, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        self.visit(node.body, {'depth': params['depth'] + 2})
        return
    
    
    def visit_IfExp(self : Self, node : ast.IfExp , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->IfExp')
        print(('  '*(params['depth'] + 1)) + '|->Test')
        self.visit(node.test, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        self.visit(node.body, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->OrElse')
        self.visit(node.orelse, {'depth': params['depth'] + 2})
        return

    ######################### COMPREHENSIONS #############################

    
    def visit_ListComp(self : Self, node : ast.ListComp , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->ListComp')
        print(('  '*(params['depth'] + 1)) + '|->Generators')
        for child in node.generators:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Elt')
        self.visit(node.elt, {'depth': params['depth'] + 2})
        return

    
    def visit_SetComp(self : Self, node : ast.SetComp , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->SetComp')
        print(('  '*(params['depth'] + 1)) + '|->Generators')
        for child in node.generators:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Elt')
        self.visit(node.elt, {'depth': params['depth'] + 2})
        return

    
    def visit_DictComp(self : Self, node : ast.DictComp , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->DictComp')
        print(('  '*(params['depth'] + 1)) + '|->Generators')
        for child in node.generators:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Key')
        self.visit(node.key, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        return

    
    def visit_GeneratorExp(self : Self, node : ast.GeneratorExp , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->GeneratorExp')
        print(('  '*(params['depth'] + 1)) + '|->Generators')
        for child in node.generators:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Elt')
        self.visit(node.elt, {'depth': params['depth'] + 2})
        return

    ######################################################################

    
    def visit_Await(self : Self, node : ast.Await , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Await')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        return

    
    def visit_Yield(self : Self, node : ast.Yield , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Yield')
        if(node.value): 
            print(('  '*(params['depth'] + 1)) + '|->Value')
            self.visit(node.value, {'depth': params['depth'] + 2})
        return

    
    def visit_YieldFrom(self : Self, node : ast.YieldFrom , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->YieldFrom')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        return

    
    def visit_Compare(self : Self, node : ast.Compare , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Compare')
        print(('  '*(params['depth'] + 1)) + '|->Left')
        self.visit(node.left, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Comparators')
        for child in node.comparators:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    ########################## call_args ###########################

    
    def visit_Call(self : Self, node : ast.Call , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Call')
        print(('  '*(params['depth'] + 1)) + '|->Args')
        for child in node.args:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Func')
        self.visit(node.func, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Keywords')
        for child in node.keywords:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    ################################################################

    def visit_FormattedValue(self : Self, node : ast.FormattedValue , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->FormattedValue')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        if(node.format_spec):
            print(('  '*(params['depth'] + 1)) + '|->FormatSpec')
            self.visit(node.format_spec, {'depth': params['depth'] + 2})
        return

    ########################### F-strings #####################################

    
    def visit_JoinedStr(self : Self, node : ast.JoinedStr , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->JoinedStr')
        print(('  '*(params['depth'] + 1)) + '|->Values')
        for child in node.values:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    ###########################################################################

    
    def visit_Constant(self : Self, node : ast.Constant , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Constant')
        print(('  '*(params['depth'] + 1)) + '|->' + str(node.value))
        return

    
    def visit_Attribute(self : Self, node : ast.Attribute , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Attribute')
        print(('  '*(params['depth'] + 1)) + '|->' + node.attr)
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        return

    
    def visit_Subscript(self : Self, node : ast.Subscript , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Subscript')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Slice')
        self.visit(node.slice, {'depth': params['depth'] + 2})
        return

    
    def visit_Starred(self : Self, node : ast.Starred , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Starred')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        return

    ############################# Variable ##################################

    
    def visit_Name(self : Self, node : ast.Name , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Name')
        print(('  '*(params['depth'] + 1)) + '|->' + node.id)
        return

    ############################### Vectors #################################

    
    def visit_List(self : Self, node : ast.List , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->List')
        print(('  '*(params['depth'] + 1)) + '|->Elts')
        for child in node.elts:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_Tuple(self : Self, node : ast.Tuple , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Tuple')
        print(('  '*(params['depth'] + 1)) + '|->Elts')
        for child in node.elts:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_Dict(self : Self, node : ast.Dict , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Dict')
        print(('  '*(params['depth'] + 1)) + '|->Keys')
        for key in node.keys:
            self.visit(key, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Values')
        for value in node.values:
            self.visit(value, {'depth': params['depth'] + 2})
        return

    
    def visit_Set(self : Self, node : ast.Set , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Set')
        print(('  '*(params['depth'] + 1)) + '|->Elts')
        for child in node.elts:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    ########################################################################

    
    def visit_Slice(self : Self, node : ast.Slice , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Slice')
        print(('  '*(params['depth'] + 1)) + '|->Lower')
        if(node.lower):
            self.visit(node.lower, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Upper')
        if(node.upper):
            self.visit(node.upper, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Step')
        if(node.step):
            self.visit(node.step, {'depth': params['depth'] + 2})
        return

    ############################### Cases ###################################

    
    def visit_MatchValue(self : Self, node : ast.MatchValue , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->MatchValue')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        return

    
    def visit_MatchSingleton(self : Self, node : ast.MatchSingleton , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->MatchSingleton')
        print(('  '*(params['depth'] + 1)) + '|->' + node.value)
        return

    
    def visit_MatchSequence(self : Self, node : ast.MatchSequence , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->MatchSequence')
        print(('  '*(params['depth'] + 1)) + '|->Patterns')
        for child in node.patterns:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_MatchMapping(self : Self, node : ast.MatchMapping , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->MatchMapping')
        print(('  '*(params['depth'] + 1)) + '|->Patterns')
        for child in node.patterns:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Keys')
        for child in node.keys:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_MatchClass(self : Self, node : ast.MatchClass , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->MatchClass')
        print(('  '*(params['depth'] + 1)) + '|->Cls')
        self.visit(node.cls, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Patterns')
        for child in node.patterns:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->KwdPatterns')
        for child in node.kwd_patterns:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    
    def visit_MatchStar(self : Self, node : ast.MatchStar , params : Dict) -> Dict:
        print(('  '*params['depth']) + '|->MatchStar')
        print(('  '*(params['depth'] + 1)) + '|->' + node.name)
        return

    
    def visit_MatchAs(self : Self, node : ast.MatchAs , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->MatchAs')
        if(node.name):
            print(('  '*(params['depth'] + 1)) + '|->' + node.name)
        if(node.pattern): 
            print(('  '*(params['depth'] + 1)) + '|->Pattern')
            self.visit(node.pattern, {'depth': params['depth'] + 2})
        return

    
    def visit_MatchOr(self : Self, node : ast.MatchOr , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->MatchOr')
        print(('  '*(params['depth'] + 1)) + '|->Patterns')
        for child in node.patterns:
            self.visit(child, {'depth': params['depth'] + 2})
        return
    
    ############################# HANDLER ####################################

    def visit_ExceptHandler(self : Self, node : ast.ExceptHandler , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->ExceptHandler')
        if(node.type): 
            print(('  '*(params['depth'] + 1)) + '|->Type')
            self.visit(node.type, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')    
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        return

    ####################### Visits extra ######################

    def visit_comprehension(self : Self, node : ast.comprehension , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->comprehension')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.target, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Iter')   
        self.visit(node.iter, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Ifs')  
        for child in node.ifs:
            self.visit(child, {'depth' : params['depth'] + 2})
        return
    
    def visit_arguments(self : Self, node : ast.arguments , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->Arguments') 
        print(('  '*(params['depth'] + 1)) + '|->PosOnlyArgs') 
        for child in node.posonlyargs:
            self.visit(child, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Args') 
        for child in node.args:
            self.visit(child, {'depth' : params['depth'] + 2})
        if(node.vararg):
            print(('  '*(params['depth'] + 1)) + '|->VarArg') 
            self.visit(node.vararg, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->KwOnlyArgs') 
        for child in node.kwonlyargs:
            self.visit(child, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->KwDefaults') 
        for child in node.kw_defaults:
            self.visit(child, {'depth' : params['depth'] + 2})
        if(node.kwarg):
            print(('  '*(params['depth'] + 1)) + '|->KwArg') 
            self.visit(node.kwarg, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Defaults') 
        for child in node.defaults:
            self.visit(child, {'depth' : params['depth'] + 2})
        return
    
    def visit_arg(self : Self, node : ast.arg , params : Dict) -> Dict:
        print(('  '*params['depth']) + '|->arg')
        print(('  '*(params['depth'] + 1)) + '|->' + node.arg) 
        if(node.annotation):
            print(('  '*(params['depth'] + 1)) + '|->Annotation') 
            self.visit(node.annotation, {'depth' : params['depth'] + 2})
            return
        return
    
    def visit_keyword(self : Self, node : ast.keyword , params : Dict) -> Dict:
        print(('  '*params['depth']) + '|->Keyword') 
        if(node.arg):
            print(('  '*(params['depth'] + 1)) + '|->' + node.arg) 
        print(('  '*(params['depth'] + 1)) + '|->Value') 
        self.visit(node.value, {'depth' : params['depth'] + 2})
        return
    
    def visit_withitem(self : Self, node : ast.withitem , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->withitem') 
        print(('  '*(params['depth'] + 1)) + '|->ContextExpr') 
        self.visit(node.context_expr, {'depth': params['depth'] + 2})
        if(node.optional_vars): 
            print(('  '*(params['depth'] + 1)) + '|->OptionalVars') 
            self.visit(node.optional_vars, {'depth': params['depth'] + 2})
        return
    
    def visit_match_case(self : Self, node : ast.match_case , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->matchcase')
        print(('  '*(params['depth'] + 1)) + '|->Pattern') 
        self.visit(node.pattern, {'depth' : params['depth'] + 2})
        if(node.guard): 
            print(('  '*(params['depth'] + 1)) + '|->Guard') 
            self.visit(node.guard, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body') 
        for child in node.body:
            self.visit(child, {'depth' : params['depth'] + 2})
        return
    
    def visit_TypeVar(self : Self, node : ast.TypeVar , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->TypeVar') 
        print(('  '*(params['depth'] + 1)) + '|->' + node.name) 
        if(node.bound):
            print(('  '*(params['depth'] + 1)) + '|->Bound') 
            self.visit(node.bound, {'depth' : params['depth'] + 2})
        return
    
    def visit_ParamSpec(self : Self, node : ast.ParamSpec , params : Dict) -> Dict: 
        print(('  '*params['depth']) + '|->ParamSpec') 
        print(('  '*(params['depth'] + 1)) + '|->' + node.name)
        return
    
    def visit_TypeVarTuple(self : Self, node : ast.TypeVarTuple , params : Dict) -> Dict:
        print(('  '*params['depth']) + '|->TypeVarTuple') 
        print(('  '*(params['depth'] + 1)) + '|->' + node.name)
        return

    ###########################################################