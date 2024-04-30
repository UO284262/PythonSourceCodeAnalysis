import ast
from typing import Dict

from db.db_utils import write_on_db
from visitors.nodevisitor import NodeVisitor
import db.db_entities as db_entities


class VisitorDataBase(NodeVisitor):
    def __init__(self):
        self.sql_insert = []
        self.data_to_insert = []
        self.sql_nodes_to_insert = []
        self.nodes_data_to_insert = []

    def visit_Program(self, node: db_entities.DBProgram, params: Dict):
        self.insert_Program(node)
        #write_on_db(self.sql_nodes_to_insert, self.nodes_data_to_insert, self.sql_insert, self.data_to_insert)
        self.sql_insert = []
        self.data_to_insert = []
        self.nodes_data_to_insert = []
        self.sql_nodes_to_insert = []
        pass
    
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
    
    def visit_Nonlocal(self, node: ast.Nonlocal, params: Dict):
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
        sql_insert = '''INSERT INTO Programs (
                            program_id,
                            name, 
                            has_sub_dirs_with_code, 
                            has_packages, 
                            number_of_modules, 
                            number_of_sub_dirs_with_code, 
                            number_of_packages,
                            class_defs_pct, 
                            function_defs_pct, 
                            enum_defs_pct, 
                            has_code_root_package, 
                            average_defs_per_module, 
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.program_id,
                            node.name, 
                            node.has_sub_dirs_with_code, 
                            node.has_packages, 
                            node.number_of_modules, 
                            node.number_of_sub_dirs_with_code, 
                            node.number_of_packages,
                            node.class_defs_pct, 
                            node.function_defs_pct, 
                            node.enum_defs_pct, 
                            node.has_code_root_package, 
                            node.average_defs_per_module, 
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)

    def insert_FunctionDef(self, node: db_entities.DBFunctionDef):
        sql_insert = '''INSERT INTO FunctionDefs (
                            functiondef_id,
                            name_convention, 
                            number_of_characters, 
                            is_private, 
                            is_magic, 
                            body_count, 
                            expressions_pct,
                            is_async, 
                            number_of_decorators, 
                            has_return_type_annotation, 
                            has_doc_string, 
                            height, 
                            type_annotations_pct, 
                            source_code, 
                            module_id,
                            parent_id,
                            parameters_id,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.functiondef_id,
                            node.name_convention, 
                            node.number_of_characters, 
                            node.is_private, 
                            node.is_magic, 
                            node.body_count, 
                            node.expressions_pct, 
                            node.is_async, 
                            node.number_of_decorators, 
                            node.has_return_type_annotation, 
                            node.has_doc_string,
                            node.height, 
                            node.type_annotations_pct,
                            node.source_code, 
                            node.module_id,
                            node.parent_id,
                            node.parameters_id,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Module(self, node: db_entities.DBModule):
        sql_insert = '''INSERT INTO Modules (
                            module_id, 
                            name, 
                            name_convention, 
                            has_doc_string, 
                            global_stmts_pct, 
                            global_expressions, 
                            number_of_classes, 
                            number_of_functions, 
                            class_defs_pct, 
                            function_defs_pct, 
                            enum_defs_pct, 
                            average_stmts_function_body, 
                            average_stmts_method_body, 
                            type_annotations_pct, 
                            has_entry_point, 
                            program_id, 
                            path, 
                            import_id,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.module_id,
                            node.name, 
                            node.name_convention, 
                            node.has_doc_string, 
                            node.global_stmts_pct, 
                            node.global_expressions, 
                            node.number_of_classes, 
                            node.number_of_functions, 
                            node.class_defs_pct, 
                            node.function_defs_pct, 
                            node.enum_defs_pct, 
                            node.average_stmts_function_body, 
                            node.average_stmts_method_body, 
                            node.type_annotations_pct, 
                            node.has_entry_point, 
                            node.program_id, 
                            node.path, 
                            node.import_id,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Node(self, node: db_entities.DBNode):
        sql_nodes_insert = '''INSERT INTO Nodes (
                            node_id,
                            parent_table, 
                            parent_id) 
                        VALUES (%s, %s, %s);'''
        nodes_data_to_insert = (node.node_id,
                            node.parent_table, 
                            node.parent_id)
        self.sql_nodes_to_insert.append(sql_nodes_insert)
        self.nodes_data_to_insert.append(nodes_data_to_insert)
        
    def insert_Import(self, node: db_entities.DBImport):
        sql_insert = '''INSERT INTO Imports (
                            import_id,
                            number_imports,
                            module_imports_pct, 
                            average_imported_modules, 
                            from_imports_pct,
                            average_from_imported_modules, 
                            average_as_in_imported_modules, 
                            local_imports_pct,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.import_id,
                            node.number_imports,
                            node.module_imports_pct, 
                            node.average_imported_modules, 
                            node.from_imports_pct, 
                            node.average_from_imported_modules,
                            node.average_as_in_imported_modules, 
                            node.local_imports_pct,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_ClassDef(self, node: db_entities.DBClassDef):
        sql_insert = '''INSERT INTO ClassDefs (
                            classdef_id,
                            name_convention, 
                            is_enum_class, 
                            number_of_characters, 
                            number_of_decorators, 
                            number_of_methods,
                            number_of_base_classes, 
                            has_generic_type_annotations, 
                            has_doc_string, 
                            body_count, 
                            assignments_pct, 
                            expressions_pct, 
                            uses_meta_class, 
                            number_of_keywords, 
                            height, 
                            average_stmts_method_body, 
                            type_annotations_pct, 
                            private_methods_pct, 
                            magic_methods_pct, 
                            async_methods_pct, 
                            class_methods_pct, 
                            static_methods_pct, 
                            abstract_methods_pct, 
                            property_methods_pct,
                            source_code, 
                            module_id,
                            parent_id,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.classdef_id,
                            node.name_convention, 
                            node.is_enum_class, 
                            node.number_of_characters, 
                            node.number_of_decorators, 
                            node.number_of_methods,
                            node.number_of_base_classes, 
                            node.has_generic_type_annotations, 
                            node.has_doc_string, 
                            node.body_count, 
                            node.assignments_pct, 
                            node.expressions_pct, 
                            node.uses_meta_class, 
                            node.number_of_keywords, 
                            node.height, 
                            node.average_stmts_method_body, 
                            node.type_annotations_pct, 
                            node.private_methods_pct, 
                            node.magic_methods_pct, 
                            node.async_methods_pct, 
                            node.class_methods_pct, 
                            node.static_methods_pct, 
                            node.abstract_methods_pct, 
                            node.property_methods_pct,
                            node.source_code, 
                            node.module_id,
                            node.parent_id,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_MethodDef(self, node: db_entities.DBMethodDef):
        sql_insert = '''INSERT INTO MethodDefs (
                            methoddef_id,
                            classdef_id, 
                            is_class_method, 
                            is_static_method, 
                            is_constructor_method,
                            is_abstract_method, 
                            is_property, 
                            is_wrapper, 
                            is_cached,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.methoddef_id,
                            node.classdef_id, 
                            node.is_class_method, 
                            node.is_static_method, 
                            node.is_constructor_method,
                            node.is_abstract_method, 
                            node.is_property, 
                            node.is_wrapper, 
                            node.is_cached,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Statement(self, node: db_entities.DBStatement):
        sql_insert = '''INSERT INTO Statements (
                            statement_id,
                            category, 
                            parent, 
                            statement_role, 
                            height, 
                            depth, 
                            source_code, 
                            has_or_else, 
                            body_size, 
                            first_child_id, 
                            second_child_id, 
                            third_child_id,
                            parent_id,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.statement_id,
                            node.category, 
                            node.parent, 
                            node.statement_role, 
                            node.height, 
                            node.depth, 
                            node.source_code, 
                            node.has_or_else, 
                            node.body_size, 
                            node.first_child_id, 
                            node.second_child_id, 
                            node.third_child_id,
                            node.parent_id,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
    
    def insert_Case(self, node: db_entities.DBCase):
        sql_insert = '''INSERT INTO Cases (
                            statement_id,
                            number_of_cases, 
                            guards, 
                            average_body_count, 
                            average_match_value, 
                            average_match_singleton, 
                            average_match_sequence, 
                            average_match_mapping, 
                            average_match_class, 
                            average_match_star, 
                            average_match_as, 
                            average_match_or,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.statement_id,
                            node.number_of_cases, 
                            node.guards, 
                            node.average_body_count, 
                            node.average_match_value, 
                            node.average_match_singleton, 
                            node.average_match_sequence, 
                            node.average_match_mapping, 
                            node.average_match_class, 
                            node.average_match_star, 
                            node.average_match_as, 
                            node.average_match_or,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Handler(self, node: db_entities.DBHandler):
        sql_insert = '''INSERT INTO Handlers (
                            statement_id,
                            number_of_handlers, 
                            has_finally, 
                            has_catch_all, 
                            average_body_count, 
                            has_star,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.statement_id,
                            node.number_of_handlers, 
                            node.has_finally, 
                            node.has_catch_all, 
                            node.average_body_count, 
                            node.has_star,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Expression(self, node: db_entities.DBExpression):
        sql_insert = '''INSERT INTO Expressions (
                            expression_id,
                            category, 
                            first_child_category, 
                            second_child_category, 
                            third_child_category, 
                            fourth_child_category, 
                            first_child_id, 
                            second_child_id, 
                            third_child_id, 
                            fourth_child_id,
                            parent, 
                            expression_role, 
                            height, 
                            depth, 
                            source_code, 
                            parent_id,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.category, 
                            node.first_child_category, 
                            node.second_child_category, 
                            node.third_child_category, 
                            node.fourth_child_category, 
                            node.first_child_id,
                            node.second_child_id,
                            node.third_child_id,
                            node.fourth_child_id,
                            node.parent, 
                            node.expression_role, 
                            node.height, 
                            node.depth, 
                            node.source_code, 
                            node.parent_id,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)

    def insert_Comprehension(self, node: db_entities.DBComprehension):
        sql_insert = '''INSERT INTO Comprehensions (
                            expression_id,
                            category, 
                            number_of_ifs, 
                            number_of_generators, 
                            is_async,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.category, 
                            node.number_of_ifs, 
                            node.number_of_generators, 
                            node.is_async,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_FString(self, node: db_entities.DBFString):
        sql_insert = '''INSERT INTO FStrings (
                            expression_id,
                            number_of_elements, 
                            constants_pct, 
                            expressions_pct,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.number_of_elements, 
                            node.constants_pct, 
                            node.expressions_pct,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_CallArg(self, node: db_entities.DBCallArg):
        sql_insert = '''INSERT INTO CallArgs (
                            expression_id,
                            number_args, 
                            named_args_pct, 
                            double_star_args_pct,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.number_args, 
                            node.named_args_pct, 
                            node.double_star_args_pct,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
    
    def insert_Variable(self, node: db_entities.DBVariable):
        sql_insert = '''INSERT INTO Variables (
                            expression_id,
                            name_convention, 
                            number_of_characters, 
                            is_private,
                            is_magic,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.name_convention, 
                            node.number_of_characters, 
                            node.is_private,
                            node.is_magic,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Vector(self, node: db_entities.DBVector):
        sql_insert = '''INSERT INTO Vectors (
                            expression_id,
                            category,
                            number_of_elements,
                            homogeneous,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.expression_id,
                            node.category,
                            node.number_of_elements,
                            node.homogeneous,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)
        
    def insert_Parameter(self, node: db_entities.DBParameter):
        sql_insert = '''INSERT INTO Parameters (
                            parameters_id,
                            parent_id,
                            parameters_role,
                            number_of_params, 
                            pos_only_param_pct, 
                            var_param_pct, 
                            has_var_param, 
                            type_annotation_pct, 
                            kw_only_param_pct, 
                            default_value_pct, 
                            has_KW_param, 
                            name_convention,
                            user_id,
                            expertise_level) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        data_to_insert = (node.parameters_id,
                            node.parent_id,
                            node.parameters_role,
                            node.number_of_params, 
                            node.pos_only_param_pct, 
                            node.var_param_pct, 
                            node.has_var_param, 
                            node.type_annotation_pct, 
                            node.kw_only_param_pct, 
                            node.default_value_pct, 
                            node.has_KW_param, 
                            node.name_convention,
                            node.user_id,
                            node.expertise_level)
        self.sql_insert.append(sql_insert)
        self.data_to_insert.append(data_to_insert)