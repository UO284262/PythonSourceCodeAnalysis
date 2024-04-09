import ast
import db.db_entities as db_entities
from typing import Dict, List
from visitors.nodevisitor import NodeVisitor
from tkinter import Tk, END
from tkinter.ttk import Treeview, Style


class VisitorIntrospector(NodeVisitor):
    def __init__(self):
        self.programs: List[db_entities.DBProgram] = []
        self.function_defs: List[db_entities.DBFunctionDef] = []
        self.modules: List[db_entities.DBModule] = []
        self.nodes: List[db_entities.DBNode] = []
        self.imports: List[db_entities.DBImport] = []
        self.class_defs: List[db_entities.DBClassDef] = []
        self.method_defs: List[db_entities.DBMethodDef] = []
        self.statements: List[db_entities.DBStatement] = []
        self.cases: List[db_entities.DBCase] = []
        self.handlers: List[db_entities.DBHandler] = []
        self.expressions: List[db_entities.DBExpression] = []
        self.comprehensions: List[db_entities.DBComprehension] = []
        self.f_strings: List[db_entities.DBFString] = []
        self.call_args: List[db_entities.DBCallArg] = []
        self.variables: List[db_entities.DBVariable] = []
        self.vectors: List[db_entities.DBVector] = []
        self.parameters: List[db_entities.DBParameter] = []

        # TreeView
        self.window = Tk()
        self.window.title("Introspector")
        self.window.state("zoomed")
        Style().theme_use("vista")
        self.tree = Treeview(self.window)

    def visit_Program(self, node: db_entities.DBProgram, params: Dict):
        self.insert_Program(node)
        self.add_treeview_item("", node)
        self.show_treeview()

    def show_treeview(self):
        self.tree.pack(fill="both", expand=True)
        self.window.mainloop()

    def add_treeview_item(self, parent, node):
        item = self.tree.insert(parent, END, text=node.__class__.__name__)
        for attr_name, attr_value in node.__dict__.items():
            if not attr_name.endswith("id") and attr_name not in ["table", "node"]:
                self.tree.insert(item, END, text=attr_name + ': ' + str(attr_value).replace("\n", ""))
        if isinstance(node, db_entities.DBProgram):
            children = self.tree.insert(item, END, text="Modules")
            for child in filter(lambda x: x.program_id == node.program_id, self.modules):
                self.add_treeview_item(children, child)
        if isinstance(node, db_entities.DBModule):
            children = self.tree.insert(item, END, text="Imports")
            for child in filter(lambda x: x.import_id == node.import_id, self.imports):
                self.add_treeview_item(children, child)
            children = self.tree.insert(item, END, text="Definitions")
            for child in filter(lambda x: x.module_id == node.module_id, self.class_defs):
                self.add_treeview_item(children, child)
            for child in filter(lambda x: x.module_id == node.module_id, self.function_defs):
                self.add_treeview_item(children, child)
        if isinstance(node, db_entities.DBClassDef):
            children = self.tree.insert(item, END, text="Body")
            self.add_body_children(children, node.classdef_id)
        if isinstance(node, db_entities.DBFunctionDef):
            children = self.tree.insert(item, END, text="Parameters")
            for child in filter(lambda x: x.parameters_id == node.parameters_id, self.parameters):
                self.add_treeview_item(children, child)
            children = self.tree.insert(item, END, text="Body")
            self.add_body_children(children, node.functiondef_id)
        if isinstance(node, db_entities.DBMethodDef):
            for child in filter(lambda x: x.functiondef_id == node.methoddef_id, self.function_defs):
                self.add_treeview_item(item, child)
        if isinstance(node, db_entities.DBStatement):
            child = next(filter(lambda x: x.node_id == node.first_child_id, self.nodes), None)
            if child is not None:
                self.add_statement_child(item, child.node_id, "First Child")
            child = next(filter(lambda x: x.node_id == node.second_child_id, self.nodes), None)
            if child is not None:
                self.add_statement_child(item, child.node_id, "Second Child")
            child = next(filter(lambda x: x.node_id == node.third_child_id, self.nodes), None)
            if child is not None:
                self.add_statement_child(item, child.node_id, "Third Child")
        if isinstance(node, db_entities.DBExpression):
            child = next(filter(lambda x: x.node_id == node.first_child_id, self.nodes), None)
            if child is not None:
                self.add_expression_child(item, child.node_id, "First Child")
            child = next(filter(lambda x: x.node_id == node.second_child_id, self.nodes), None)
            if child is not None:
                self.add_expression_child(item, child.node_id, "Second Child")
            child = next(filter(lambda x: x.node_id == node.third_child_id, self.nodes), None)
            if child is not None:
                self.add_expression_child(item, child.node_id, "Third Child")

    def add_statement_child(self, parent: str, child_id: int, text: str):
        child = next(filter(lambda z: z.statement_id == child_id, self.statements), None)
        if child is None:
            child = next(filter(lambda z: z.expression_id == child_id, self.expressions), None)
        if child is not None:
            self.add_treeview_item(self.tree.insert(parent, END, text=text), child)

    def add_expression_child(self, parent: str, child_id: int, text: str):
        child = next(filter(lambda z: z.expression_id == child_id, self.expressions), None)
        if child is not None:
            self.add_treeview_item(self.tree.insert(parent, END, text=text), child)

    def add_body_children(self, parent: str, parent_id: int):
        for child_id in map(lambda y: y.node_id, filter(lambda x: x.parent_id == parent_id, self.nodes)):
            child = next(filter(lambda z: z.methoddef_id == child_id, self.method_defs), None)
            if child is None:
                child = next(filter(lambda z: z.statement_id == child_id, self.statements), None)
            if child is None:
                child = next(filter(lambda z: z.expression_id == child_id, self.expressions), None)
            if child is not None:
                self.add_treeview_item(parent, child)

    def visit_Module(self, node: db_entities.DBModule, params: Dict):
        self.insert_Import(params["db_import"])
        self.insert_Module(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_FunctionDef(self, node: ast.FunctionDef, params: Dict):
        if params['is_method']:
            self.insert_MethodDef(params['method'])
        self.insert_FunctionDef(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef, params: Dict):
        if params['is_method']:
            self.insert_MethodDef(params['method'])
        self.insert_FunctionDef(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_ClassDef(self, node: ast.ClassDef, params: Dict):
        self.insert_ClassDef(params["node"])
        self.insert_Node(params["db_node"])
        pass

    ############################### STATEMENTS #############################
    def visit_Return(self, node: ast.Return, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Delete(self, node: ast.Delete, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Assign(self, node: ast.Assign, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])      
        pass
    
    def visit_TypeAlias(self, node: ast.TypeAlias, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"]) 
        pass
    
    def visit_AugAssign(self, node: ast.AugAssign, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_AnnAssign(self, node: ast.AnnAssign, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_For(self, node: ast.For, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_AsyncFor(self, node: ast.AsyncFor, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_While(self, node: ast.While, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_If(self, node: ast.If, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_With(self, node: ast.With, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_AsyncWith(self, node: ast.AsyncWith, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Match(self, node: ast.Match, params: Dict):
        self.insert_Case(params["case"])
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Raise(self, node: ast.Raise, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Try(self, node: ast.Try, params: Dict):
        self.insert_Handler(params["handler"])
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_TryStar(self, node: ast.Try, params: Dict):
        self.insert_Handler(params["handler"])
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Assert(self, node: ast.Assert, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Global(self, node: ast.Global, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_NonLocal(self, node: ast.Nonlocal, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Pass(self, node: ast.Pass, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Break(self, node: ast.Break, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Continue(self, node: ast.Continue, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass

    ############################ IMPORTS ##################################
    def visit_Import(self, node: ast.Import, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_ImportFrom(self, node: ast.ImportFrom, params: Dict):
        self.insert_Statement(params["node"])
        self.insert_Node(params["db_node"])
        pass

    ############################ EXPRESSIONS ##################################
    def visit_BoolOp(self, node: ast.BoolOp, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_NamedExpr(self, node: ast.NamedExpr, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_BinOp(self, node: ast.BinOp, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_UnaryOp(self, node: ast.UnaryOp, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Lambda(self, node: ast.Lambda, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_IfExp(self, node: ast.IfExp, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass

    ######################### COMPREHENSIONS #############################
    def visit_ListComp(self, node: ast.ListComp, params: Dict):
        self.insert_Comprehension(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_SetComp(self, node: ast.SetComp, params: Dict):
        self.insert_Comprehension(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_DictComp(self, node: ast.DictComp, params: Dict):
        self.insert_Comprehension(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_GeneratorExp(self, node: ast.GeneratorExp, params: Dict):
        self.insert_Comprehension(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])
        pass

    ######################################################################
    def visit_Await(self, node: ast.Await, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Yield(self, node: ast.Yield, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_YieldFrom(self, node: ast.YieldFrom, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Compare(self, node: ast.Compare, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass

    ########################## call_args ###########################
    def visit_Call(self, node: ast.Call, params: Dict):
        self.insert_CallArg(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])
        pass

    ################################################################
    def visit_FormattedValue(self, node: ast.FormattedValue, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass

    ########################### F-strings #####################################
    def visit_JoinedStr(self, node: ast.JoinedStr, params: Dict):
        self.insert_FString(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])
        pass

    ###########################################################################
    def visit_Constant(self, node: ast.Constant, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Attribute(self, node: ast.Attribute, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Subscript(self, node: ast.Subscript, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Starred(self, node: ast.Starred, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass

    ############################# Variable ##################################
    def visit_Name(self, node: ast.Name, params: Dict):
        self.insert_Variable(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])        
        pass

    ############################### Vectors #################################
    def visit_List(self, node: ast.List, params: Dict):
        self.insert_Vector(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Tuple(self, node: ast.Tuple, params: Dict):
        self.insert_Vector(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Dict(self, node: ast.Dict, params: Dict):
        self.insert_Vector(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_Set(self, node: ast.Set, params: Dict):
        self.insert_Vector(params["node"])
        self.insert_Expression(params["expr"])
        self.insert_Node(params["db_node"])
        pass

    ########################################################################
    def visit_Slice(self, node: ast.Slice, params: Dict):
        self.insert_Expression(params["node"])
        self.insert_Node(params["db_node"])
        pass
    
    def visit_ExceptHandler(self, node: ast.ExceptHandler, params: Dict):
        pass

    ############################### Cases ###################################
    def visit_MatchValue(self, node: ast.MatchValue, params: Dict):
        pass
    
    def visit_MatchSingleton(self, node: ast.MatchSingleton, params: Dict):
        pass
    
    def visit_MatchSequence(self, node: ast.MatchSequence, params: Dict):
        pass
    
    def visit_MatchMapping(self, node: ast.MatchMapping, params: Dict):
        pass
    
    def visit_MatchClass(self, node: ast.MatchClass, params: Dict):
        pass
    
    def visit_MatchStar(self, node: ast.MatchStar, params: Dict):
        pass
    
    def visit_MatchAs(self, node: ast.MatchAs, params: Dict):
        pass
    
    def visit_MatchOr(self, node: ast.MatchOr, params: Dict):
        pass

    ########################## visit extras #################################
    def visit_arguments(self, node: ast.arguments, params: Dict):
        self.insert_Parameter(params["dbparams"])
        pass

    def insert_Program(self, node: db_entities.DBProgram):
        self.programs.append(node)

    def insert_FunctionDef(self, node: db_entities.DBFunctionDef):
        self.function_defs.append(node)
        
    def insert_Module(self, node: db_entities.DBModule):
        self.modules.append(node)
        
    def insert_Node(self, node: db_entities.DBNode):
        self.nodes.append(node)
        
    def insert_Import(self, node: db_entities.DBImport):
        self.imports.append(node)
        
    def insert_ClassDef(self, node: db_entities.DBClassDef):
        self.class_defs.append(node)
        
    def insert_MethodDef(self, node: db_entities.DBMethodDef):
        self.method_defs.append(node)
        
    def insert_Statement(self, node: db_entities.DBStatement):
        self.statements.append(node)
    
    def insert_Case(self, node: db_entities.DBCase):
        self.cases.append(node)
        
    def insert_Handler(self, node: db_entities.DBHandler):
        self.handlers.append(node)
        
    def insert_Expression(self, node: db_entities.DBExpression):
        self.expressions.append(node)

    def insert_Comprehension(self, node: db_entities.DBComprehension):
        self.comprehensions.append(node)
        
    def insert_FString(self, node: db_entities.DBFString):
        self.f_strings.append(node)
        
    def insert_CallArg(self, node: db_entities.DBCallArg):
        self.call_args.append(node)
    
    def insert_Variable(self, node: db_entities.DBVariable):
        self.variables.append(node)
        
    def insert_Vector(self, node: db_entities.DBVector):
        self.vectors.append(node)
        
    def insert_Parameter(self, node: db_entities.DBParameter):
        self.parameters.append(node)