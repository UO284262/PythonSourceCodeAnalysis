import ast
from dataset.visitors.nodevisitor import NodeVisitor
from typing import Dict


class VisitorPrint(NodeVisitor):
    def visit_Expr(self, node: ast.Expr, params: Dict):
        self.visit(node.value, params)

    def visit_Module(self, node: ast.Module, params: Dict):
        print('|->Module') 
        for child in node.body:
            self.visit(child, {'depth': 1})
    
    def visit_FunctionDef(self, node: ast.FunctionDef, params: Dict):
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
        if node.returns:
            self.visit(node.returns, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->TypeParams')
        for child in node.type_params:
            self.visit(child, {'depth': params['depth'] + 2})
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef, params: Dict):
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
        if node.returns:
            self.visit(node.returns, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->TypeParams')
        for child in node.type_params:
            self.visit(child, {'depth': params['depth'] + 2})
        
    def visit_ClassDef(self, node: ast.ClassDef, params: Dict):
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

    ############################### STATEMENTS #############################
    def visit_Return(self, node: ast.Return, params: Dict):
        print(('  '*params['depth']) + '|->Return')
        if node.value:
            self.visit(node.value, {'depth': params['depth'] + 1})

    def visit_Delete(self, node: ast.Delete, params: Dict):
        print(('  '*params['depth']) + '|->Delete')
        for child in node.targets:
            self.visit(child, {'depth': params['depth'] + 1})

    def visit_Assign(self, node: ast.Assign, params: Dict):
        print(('  '*params['depth']) + '|->Assign')
        print(('  '*(params['depth'] + 1)) + '|->Targets')
        for child in node.targets:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
    
    def visit_TypeAlias(self, node: ast.TypeAlias, params: Dict):
        print(('  '*params['depth']) + '|->TypeAlias')
        print(('  '*(params['depth'] + 1)) + '|->TypeParams')
        for child in node.type_params:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Name')
        self.visit(node.name, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
    
    def visit_AugAssign(self, node: ast.AugAssign, params: Dict):
        print(('  '*params['depth']) + '|->AugAssign')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.target, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})

    def visit_AnnAssign(self, node: ast.AnnAssign, params: Dict):
        print(('  '*params['depth']) + '|->AnnAssign')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.target, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Annotation')
        self.visit(node.annotation, {'depth': params['depth'] + 2})
        if(node.value): 
            print(('  '*(params['depth'] + 1)) + '|->Value')
            self.visit(node.value, {'depth': params['depth'] + 2})

    def visit_For(self, node: ast.For, params: Dict):
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

    def visit_AsyncFor(self, node: ast.AsyncFor, params: Dict):
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

    def visit_While(self, node: ast.While, params: Dict):
        print(('  '*params['depth']) + '|->While')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.test, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->OrElse')
        for child in node.orelse:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_If(self, node: ast.If, params: Dict):
        print(('  '*params['depth']) + '|->If')
        self.visit(node.test, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->OrElse')
        for child in node.orelse:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_With(self, node: ast.With, params: Dict):
        print(('  '*params['depth']) + '|->With')
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Items')
        for child in node.items:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_AsyncWith(self, node: ast.AsyncWith, params: Dict):
        print(('  '*params['depth']) + '|->AsyncWith')
        print(('  '*(params['depth'] + 1)) + '|->Body')
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Items')
        for child in node.items:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_Match(self, node: ast.Match, params: Dict):
        print(('  '*params['depth']) + '|->Matc')
        print(('  '*(params['depth'] + 1)) + '|->Subject')
        self.visit(node.subject, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Cases')
        for child in node.cases:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_Raise(self, node: ast.Raise, params: Dict):
        print(('  '*params['depth']) + '|->Raise')
        if node.exc:
            print(('  '*(params['depth'] + 1)) + '|->Exc')
            self.visit(node.exc, {'depth': params['depth'] + 2})
        if node.cause:
            print(('  '*(params['depth'] + 1)) + '|->Cause')
            self.visit(node.cause, {'depth': params['depth'] + 2})
    
    def visit_Try(self, node: ast.Try, params: Dict):
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
    
    def visit_TryStar(self, node: ast.TryStar, params: Dict):
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

    def visit_Assert(self, node: ast.Assert, params: Dict):
        print(('  '*params['depth']) + '|->Try')
        print(('  '*(params['depth'] + 1)) + '|->Test')
        self.visit(node.test, {'depth': params['depth'] + 2})
        if node.msg:
            print(('  '*(params['depth'] + 1)) + '|->Msg')
            self.visit(node.msg, {'depth': params['depth'] + 2})

    def visit_Global(self, node: ast.Global, params: Dict):
        print(('  '*params['depth']) + '|->Global')
        print(('  '*(params['depth'] + 1)) + '|->Names')
        for name in node.names:
            print(('  '*(params['depth'] + 2)) + '|->' + name)

    def visit_Nonlocal(self, node: ast.Nonlocal, params: Dict):
        print(('  '*params['depth']) + '|->NonLocal')
        print(('  '*(params['depth'] + 1)) + '|->Names')
        for name in node.names:
            print(('  '*(params['depth'] + 2)) + '|->' + name)

    def visit_Pass(self, node: ast.Pass, params: Dict):
        print(('  '*params['depth']) + '|->Pass')

    def visit_Break(self, node: ast.Break, params: Dict):
        print(('  '*params['depth']) + '|->Break')
    
    def visit_Continue(self, node: ast.Continue, params: Dict): 
        print(('  '*params['depth']) + '|->Continue')        

    ############################ IMPORTS ##################################
    def visit_Import(self, node: ast.Import, params: Dict): 
        print(('  '*params['depth']) + '|->Import')
        print(('  '*(params['depth'] + 1)) + '|->Names')
        for alias in node.names:
            print(('  '*(params['depth'] + 2)) + '|->' + alias.name)
        
    def visit_ImportFrom(self, node: ast.ImportFrom, params: Dict): 
        print(('  '*params['depth']) + '|->Import')
        if node.module:
            print(('  '*(params['depth'] + 1)) + '|->Module')
            print(('  '*(params['depth'] + 2)) + '|->' + node.module)
        print(('  '*(params['depth'] + 1)) + '|->Names')
        for alias in node.names:
            print(('  '*(params['depth'] + 2)) + '|->' + alias.name)
        
    ############################ EXPRESSIONS ##################################
    def visit_BoolOp(self, node: ast.BoolOp, params: Dict): 
        print(('  '*params['depth']) + '|->BoolOp')
        print(('  '*(params['depth'] + 1)) + '|->Operator')
        print(('  '*(params['depth'] + 2)) + '|->' + node.op.__doc__)
        print(('  '*(params['depth'] + 1)) + '|->Values')
        for child in node.values:
            self.visit(child, {'depth': params['depth'] + 2})       
        
    def visit_NamedExpr(self, node: ast.NamedExpr, params: Dict): 
        print(('  '*params['depth']) + '|->NamedExpr')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.target, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        
    def visit_BinOp(self, node: ast.BinOp, params: Dict): 
        print(('  '*params['depth']) + '|->BinOp')
        print(('  '*(params['depth'] + 1)) + '|->Operator')   
        print(('  '*(params['depth'] + 2)) + '|->' + node.op.__doc__)
        print(('  '*(params['depth'] + 1)) + '|->Left')
        self.visit(node.left, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Right')
        self.visit(node.right, {'depth': params['depth'] + 2})

    def visit_UnaryOp(self, node: ast.UnaryOp, params: Dict): 
        print(('  '*params['depth']) + '|->UnaryOp')
        print(('  '*(params['depth'] + 1)) + '|->Operator')
        print(('  '*(params['depth'] + 2)) + '|->' + node.op.__doc__)
        print(('  '*(params['depth'] + 1)) + '|->Operand')
        self.visit(node.operand, {'depth': params['depth'] + 2})

    def visit_Lambda(self, node: ast.Lambda, params: Dict): 
        print(('  '*params['depth']) + '|->Lambda')
        print(('  '*(params['depth'] + 1)) + '|->Arguments')
        self.visit(node.args, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        self.visit(node.body, {'depth': params['depth'] + 2})

    def visit_IfExp(self, node: ast.IfExp, params: Dict): 
        print(('  '*params['depth']) + '|->IfExp')
        print(('  '*(params['depth'] + 1)) + '|->Test')
        self.visit(node.test, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')
        self.visit(node.body, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->OrElse')
        self.visit(node.orelse, {'depth': params['depth'] + 2})

    ######################### COMPREHENSIONS #############################
    def visit_ListComp(self, node: ast.ListComp, params: Dict): 
        print(('  '*params['depth']) + '|->ListComp')
        print(('  '*(params['depth'] + 1)) + '|->Generators')
        for child in node.generators:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Elt')
        self.visit(node.elt, {'depth': params['depth'] + 2})

    def visit_SetComp(self, node: ast.SetComp, params: Dict): 
        print(('  '*params['depth']) + '|->SetComp')
        print(('  '*(params['depth'] + 1)) + '|->Generators')
        for child in node.generators:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Elt')
        self.visit(node.elt, {'depth': params['depth'] + 2})

    def visit_DictComp(self, node: ast.DictComp, params: Dict): 
        print(('  '*params['depth']) + '|->DictComp')
        print(('  '*(params['depth'] + 1)) + '|->Generators')
        for child in node.generators:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Key')
        self.visit(node.key, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})

    def visit_GeneratorExp(self, node: ast.GeneratorExp, params: Dict): 
        print(('  '*params['depth']) + '|->GeneratorExp')
        print(('  '*(params['depth'] + 1)) + '|->Generators')
        for child in node.generators:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Elt')
        self.visit(node.elt, {'depth': params['depth'] + 2})

    def visit_Await(self, node: ast.Await, params: Dict): 
        print(('  '*params['depth']) + '|->Await')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})

    def visit_Yield(self, node: ast.Yield, params: Dict): 
        print(('  '*params['depth']) + '|->Yield')
        if node.value:
            print(('  '*(params['depth'] + 1)) + '|->Value')
            self.visit(node.value, {'depth': params['depth'] + 2})

    def visit_YieldFrom(self, node: ast.YieldFrom, params: Dict): 
        print(('  '*params['depth']) + '|->YieldFrom')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})

    def visit_Compare(self, node: ast.Compare, params: Dict): 
        print(('  '*params['depth']) + '|->Compare')
        print(('  '*(params['depth'] + 1)) + '|->Left')
        self.visit(node.left, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Comparators')
        for child in node.comparators:
            self.visit(child, {'depth': params['depth'] + 2})

    ########################## call ###########################
    def visit_Call(self, node: ast.Call, params: Dict): 
        print(('  '*params['depth']) + '|->Call')
        print(('  '*(params['depth'] + 1)) + '|->Args')
        for child in node.args:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Func')
        self.visit(node.func, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Keywords')
        for child in node.keywords:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_FormattedValue(self, node: ast.FormattedValue, params: Dict): 
        print(('  '*params['depth']) + '|->FormattedValue')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        if node.format_spec:
            print(('  '*(params['depth'] + 1)) + '|->FormatSpec')
            self.visit(node.format_spec, {'depth': params['depth'] + 2})

    ########################### F-strings #####################################
    def visit_JoinedStr(self, node: ast.JoinedStr, params: Dict): 
        print(('  '*params['depth']) + '|->JoinedStr')
        print(('  '*(params['depth'] + 1)) + '|->Values')
        for child in node.values:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_constant(self, node: ast.Constant, params: Dict):
        print(('  '*params['depth']) + '|->Constant')
        print(('  '*(params['depth'] + 1)) + '|->' + str(node.value))

    def visit_Attribute(self, node: ast.Attribute, params: Dict): 
        print(('  '*params['depth']) + '|->Attribute')
        print(('  '*(params['depth'] + 1)) + '|->' + node.attr)
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})

    def visit_Subscript(self, node: ast.Subscript, params: Dict): 
        print(('  '*params['depth']) + '|->Subscript')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Slice')
        self.visit(node.slice, {'depth': params['depth'] + 2})

    def visit_Starred(self, node: ast.Starred, params: Dict): 
        print(('  '*params['depth']) + '|->Starred')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})

    ############################# Variable ##################################
    def visit_Name(self, node: ast.Name, params: Dict): 
        print(('  '*params['depth']) + '|->Name')
        print(('  '*(params['depth'] + 1)) + '|->' + node.id)
        return

    ############################### Vectors #################################
    def visit_List(self, node: ast.List, params: Dict): 
        print(('  '*params['depth']) + '|->List')
        print(('  '*(params['depth'] + 1)) + '|->Elts')
        for child in node.elts:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_Tuple(self, node: ast.Tuple, params: Dict): 
        print(('  '*params['depth']) + '|->Tuple')
        print(('  '*(params['depth'] + 1)) + '|->Elts')
        for child in node.elts:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_Dict(self, node: ast.Dict, params: Dict): 
        print(('  '*params['depth']) + '|->Dict')
        print(('  '*(params['depth'] + 1)) + '|->Keys')
        for key in node.keys:
            self.visit(key, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Values')
        for value in node.values:
            self.visit(value, {'depth': params['depth'] + 2})

    def visit_Set(self, node: ast.Set, params: Dict): 
        print(('  '*params['depth']) + '|->Set')
        print(('  '*(params['depth'] + 1)) + '|->Elts')
        for child in node.elts:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_Slice(self, node: ast.Slice, params: Dict): 
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

    ############################### Cases ###################################
    def visit_MatchValue(self, node: ast.MatchValue, params: Dict):
        print(('  '*params['depth']) + '|->MatchValue')
        print(('  '*(params['depth'] + 1)) + '|->Value')
        self.visit(node.value, {'depth': params['depth'] + 2})

    def visit_MatchSingleton(self, node: ast.MatchSingleton, params: Dict):
        print(('  '*params['depth']) + '|->MatchSingleton')
        print(('  '*(params['depth'] + 1)) + '|->' + node.value if node.value is not None else 'None')

    def visit_MatchSequence(self, node: ast.MatchSequence, params: Dict):
        print(('  '*params['depth']) + '|->MatchSequence')
        print(('  '*(params['depth'] + 1)) + '|->Patterns')
        for child in node.patterns:
            self.visit(child, {'depth': params['depth'] + 2})
    
    def visit_MatchMapping(self, node: ast.MatchMapping, params: Dict):
        print(('  '*params['depth']) + '|->MatchMapping')
        print(('  '*(params['depth'] + 1)) + '|->Patterns')
        for child in node.patterns:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Keys')
        for child in node.keys:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_MatchClass(self, node: ast.MatchClass, params: Dict):
        print(('  '*params['depth']) + '|->MatchClass')
        print(('  '*(params['depth'] + 1)) + '|->Cls')
        self.visit(node.cls, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Patterns')
        for child in node.patterns:
            self.visit(child, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->KwdPatterns')
        for child in node.kwd_patterns:
            self.visit(child, {'depth': params['depth'] + 2})

    def visit_MatchStar(self, node: ast.MatchStar, params: Dict):
        print(('  '*params['depth']) + '|->MatchStar')
        print(('  '*(params['depth'] + 1)) + '|->' + node.name if node.name is not None else 'None')

    def visit_MatchAs(self, node: ast.MatchAs, params: Dict):
        print(('  '*params['depth']) + '|->MatchAs')
        if node.name:
            print(('  '*(params['depth'] + 1)) + '|->' + node.name)
        if node.pattern:
            print(('  '*(params['depth'] + 1)) + '|->Pattern')
            self.visit(node.pattern, {'depth': params['depth'] + 2})
    
    def visit_MatchOr(self, node: ast.MatchOr, params: Dict):
        print(('  '*params['depth']) + '|->MatchOr')
        print(('  '*(params['depth'] + 1)) + '|->Patterns')
        for child in node.patterns:
            self.visit(child, {'depth': params['depth'] + 2})
    
    ############################# HANDLER ####################################
    def visit_ExceptHandler(self, node: ast.ExceptHandler, params: Dict):
        print(('  '*params['depth']) + '|->ExceptHandler')
        if node.type:
            print(('  '*(params['depth'] + 1)) + '|->Type')
            self.visit(node.type, {'depth': params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body')    
        for child in node.body:
            self.visit(child, {'depth': params['depth'] + 2})

    ####################### Extra Visits ######################
    def visit_comprehension(self, node: ast.comprehension, params: Dict):
        print(('  '*params['depth']) + '|->comprehension')
        print(('  '*(params['depth'] + 1)) + '|->Target')
        self.visit(node.target, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Iter')   
        self.visit(node.iter, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Ifs')  
        for child in node.ifs:
            self.visit(child, {'depth' : params['depth'] + 2})
    
    def visit_arguments(self, node: ast.arguments, params: Dict):
        print(('  '*params['depth']) + '|->Arguments') 
        print(('  '*(params['depth'] + 1)) + '|->PosOnlyArgs') 
        for child in node.posonlyargs:
            self.visit(child, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Args') 
        for child in node.args:
            self.visit(child, {'depth' : params['depth'] + 2})
        if node.vararg:
            print(('  '*(params['depth'] + 1)) + '|->VarArg') 
            self.visit(node.vararg, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->KwOnlyArgs') 
        for child in node.kwonlyargs:
            self.visit(child, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->KwDefaults') 
        for child in node.kw_defaults:
            self.visit(child, {'depth' : params['depth'] + 2})
        if node.kwarg:
            print(('  '*(params['depth'] + 1)) + '|->KwArg') 
            self.visit(node.kwarg, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Defaults') 
        for child in node.defaults:
            self.visit(child, {'depth' : params['depth'] + 2})
    
    def visit_arg(self, node: ast.arg, params: Dict):
        print(('  '*params['depth']) + '|->arg')
        print(('  '*(params['depth'] + 1)) + '|->' + node.arg) 
        if node.annotation:
            print(('  '*(params['depth'] + 1)) + '|->Annotation') 
            self.visit(node.annotation, {'depth' : params['depth'] + 2})

    def visit_keyword(self, node: ast.keyword, params: Dict):
        print(('  '*params['depth']) + '|->Keyword') 
        if node.arg:
            print(('  '*(params['depth'] + 1)) + '|->' + node.arg) 
        print(('  '*(params['depth'] + 1)) + '|->Value') 
        self.visit(node.value, {'depth' : params['depth'] + 2})
    
    def visit_withitem(self, node: ast.withitem, params: Dict):
        print(('  '*params['depth']) + '|->withitem') 
        print(('  '*(params['depth'] + 1)) + '|->ContextExpr') 
        self.visit(node.context_expr, {'depth': params['depth'] + 2})
        if node.optional_vars:
            print(('  '*(params['depth'] + 1)) + '|->OptionalVars') 
            self.visit(node.optional_vars, {'depth': params['depth'] + 2})
    
    def visit_match_case(self, node: ast.match_case, params: Dict):
        print(('  '*params['depth']) + '|->matchcase')
        print(('  '*(params['depth'] + 1)) + '|->Pattern') 
        self.visit(node.pattern, {'depth' : params['depth'] + 2})
        if node.guard:
            print(('  '*(params['depth'] + 1)) + '|->Guard') 
            self.visit(node.guard, {'depth' : params['depth'] + 2})
        print(('  '*(params['depth'] + 1)) + '|->Body') 
        for child in node.body:
            self.visit(child, {'depth' : params['depth'] + 2})
    
    def visit_TypeVar(self, node: ast.TypeVar, params: Dict):
        print(('  '*params['depth']) + '|->TypeVar') 
        print(('  '*(params['depth'] + 1)) + '|->' + node.name) 
        if node.bound:
            print(('  '*(params['depth'] + 1)) + '|->Bound') 
            self.visit(node.bound, {'depth' : params['depth'] + 2})
    
    def visit_ParamSpec(self, node: ast.ParamSpec, params: Dict):
        print(('  '*params['depth']) + '|->ParamSpec') 
        print(('  '*(params['depth'] + 1)) + '|->' + node.name)
    
    def visit_TypeVarTuple(self, node: ast.TypeVarTuple, params: Dict):
        print(('  '*params['depth']) + '|->TypeVarTuple') 
        print(('  '*(params['depth'] + 1)) + '|->' + node.name)