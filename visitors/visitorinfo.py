import ast
import re
import os
from typing import Dict, Self
from util.util import op_category, const_category
import db.db_entities as db_entities
from visitors.visitordatabase import VisitorDataBase
from visitors.nodevisitor import NodeVisitor


class VisitorInfo(NodeVisitor):
    def __init__(self, id_manager):
        self.id_manager = id_manager
        self.visitor_db = VisitorDataBase()

    @staticmethod
    def get_args_name_convention(naming_conventions: Dict) -> str:
        name_convention = ''
        max = 0
        for nc in naming_conventions.keys():
            if naming_conventions[nc] > max:
                max = naming_conventions[nc]
                name_convention = nc
        return name_convention

    @staticmethod
    def what_is_it(method):
        what_is_it = {'magic': False, 'private': False, 'abstract': False, 'wrapper': False, 'cached': False, 'static': False, 'classmethod': False, 'property': False}
        magic_pattern = re.compile(r'^__\w+__$')
        private_pattern = re.compile(r'^_\w+$')
        what_is_it["magic"] = True if magic_pattern.match(method.name) else False
        what_is_it["private"] = True if private_pattern.match(method.name) else False
        for decorator in method.decorator_list:
            if isinstance(decorator, ast.Name):
                if decorator.id == "abstractmethod":
                    what_is_it["abstract"] = True
                if decorator.id == "wraps":
                    what_is_it["wrapper"] = True
                if decorator.id == "cache":
                    what_is_it["cached"] = True
                if decorator.id == "staticmethod":
                    what_is_it["static"] = True
                if decorator.id == "classmethod":
                    what_is_it["classmethod"] = True
                if decorator.id == "property":
                    what_is_it["property"] = True
        return what_is_it

    @staticmethod
    def name_convention(name) -> str:
        lower_pattern = re.compile(r'^[a-z]+$')
        upper_pattern = re.compile(r'^[A-Z_]+$')
        camel_low_pattern = re.compile(r'^[a-z][a-zA-Z]*$')
        camel_up_pattern = re.compile(r'^[A-Z][a-zA-Z]*$')
        snake_case_pattern = re.compile(r'^[a-z_]+$')
        discard_pattern = re.compile(r'^_+$')
        if discard_pattern.match(name):
            return 'Discard'
        elif snake_case_pattern.match(name):
            return 'SnakeCase'
        elif upper_pattern.match(name):
            return 'Upper'
        elif lower_pattern.match(name):
            return 'Lower'
        elif camel_low_pattern.match(name):
            return 'CamelLow'
        elif camel_up_pattern.match(name):
            return 'CamelUp'
        else: 
            return 'NoNameConvention'

    @staticmethod
    def add_param(dict_1: Dict, param, value) -> Dict:
        new_dict = dict_1.copy()
        new_dict[param] = value
        return new_dict

    @staticmethod
    def sum_match(dict_1: Dict, dict_2: Dict) -> Dict:
        return {
            'matchValue': dict_1["matchValue"] + dict_2["matchValue"],
            'matchSingleton': dict_1["matchSingleton"] + dict_2["matchSingleton"],
            'matchSequence': dict_1["matchSequence"] + dict_2["matchSequence"],
            'matchMapping': dict_1["matchMapping"] + dict_2["matchMapping"],
            'matchClass': dict_1["matchClass"] + dict_2["matchClass"],
            'matchStar': dict_1["matchStar"] + dict_2["matchStar"],
            'matchAs': dict_1["matchAs"] + dict_2["matchAs"],
            'matchOr': dict_1["matchOr"] + dict_2["matchOr"],
            'depth': max(dict_1["depth"], dict_2["depth"])
        }

    def visit_Program(self, params: Dict) -> Dict: 
        db_program = db_entities.DBProgram()
        ################## IDs ###################
        node_id = self.id_manager.get_id()
        ########## ENTITY PROPERTIES ############
        num_of_dirs = 0
        num_of_packages = 0
        total_class_defs = 0
        total_function_defs = 0
        total_enum_defs = 0
        name = params["path"].split("\\")[-1]
        ############## PROPAGAR VISIT ############
        modules = []
        routes = []
        index = 0
        for current_folder, folders, files in os.walk(params["path"]):
            has_init_py = False
            has_py = False
            has_code_root = False
            for file in files:
                if current_folder.split("\\")[-1] != name:
                    if file == '__init__.py':
                        has_init_py = True
                    elif file.endswith('.py'):
                        has_py = True
                else:
                    if file.endswith('.py'):
                        has_code_root = True
                full_path = os.path.join(current_folder, file)
                if file.endswith('.py') and not 'MACOSX' in full_path:
                    with open(r''+full_path+'', "r",  encoding='utf-8') as f:
                        module_ast = None
                        try:
                            content = f.read()
                            module_ast = ast.parse(content)
                        except Exception as e:
                            # Not compile
                            pass
                        if module_ast:
                            try:
                                if len(module_ast.body) > 0:
                                    modules.append(self.visit(module_ast, {"program_id": node_id, "user_id": params["user_id"], "expertise_level": params["expertise_level"], "filename": file.split('.')[0], "path": full_path}))
                                    total_class_defs += modules[index]["classdefs"]
                                    total_enum_defs += modules[index]["enumDefs"]
                                    total_function_defs += modules[index]["functionDefs"]
                                    index += 1
                            except Exception as e:
                                raise e
                                # Not compile
                                pass
            if has_init_py:
                num_of_packages += 1
            elif has_py:
                num_of_dirs += 1
        ########## ENTITY PROPERTIES ############
        if index > 0:
            total_defs = total_class_defs + total_enum_defs+ total_function_defs
            db_program.program_id = node_id
            db_program.name = name
            db_program.numberOfPackages = num_of_packages
            db_program.numberOfSubDirsWithCode = num_of_dirs
            db_program.hasCodeRootPackage = has_code_root
            db_program.hasPackages = num_of_packages > 0
            db_program.hasSubDirsWithCode = num_of_dirs > 0
            db_program.numberOfModules = index
            db_program.averageDefsPerModule = total_defs/index
            db_program.classDefsPct = total_class_defs/total_defs if total_defs > 0 else 0
            db_program.functionDefsPct = total_function_defs/total_defs if total_defs > 0 else 0
            db_program.enumDefsPct = total_enum_defs/total_defs if total_defs > 0 else 0
            db_program.expertise_level = params["expertise_level"]
            db_program.user_id = params["user_id"]
        ############## VISITOR DB ################  
            self.visitor_db.visit_Program(db_program, {})
        return

    # params = [parent, parent_id = node]
    def visit_Expr(self, node: ast.Expr, params: Dict) -> Dict: 
        return self.visit(node.value, params)

    def visit_Module(self, node: ast.Module, params: Dict) -> Dict: 
        db_node = db_entities.db_node()
        db_module = db_entities.DBModule()
        db_import = db_entities.DBImport()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_module.module_id = db_import.import_id = db_module.import_id = node_id
        db_module.program_id = params['program_id']
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_module, "depth": 1, "parent_id": node_id, "role": "Module"}
        ############## PROPAGAR VISIT ############
        method_count = 0
        functions_body_size = 0
        number_of_method_stmt = 0
        type_annotations = 0
        simple_import_num = 0
        from_import_num = 0
        local_imports = 0
        simple_import_modules_num = 0
        from_import_modules_num = 0
        as_names = 0
        params_rets = 0
        has_entry_point = False
        count = {'stmt': 0, 'expr': 0, 'classes': 0, 'function': 0, 'enum': 0}
        ########## ENTITY PROPERTIES ############
        returns = []
        from_imports = []
        simple_imports = []
        functions = []
        classes = []
        c_index = 0
        f_index = 0
        si_index = 0
        fi_index = 0
        index = 0
        for child in node.body:
            returns.append(self.visit(child, child_params))
            if isinstance(child, ast.Expr):
                count["expr"] += 1
            elif isinstance(child, ast.ClassDef):
                classes.append(returns[index])
                if returns[index]['isEnum']:
                    count['enum'] += 1
                else:
                    count['classes'] += 1
                number_of_method_stmt += returns[index]["number_of_method_stmt"]
                method_count += returns[index]["method_count"]
                params_rets += returns[index]["numberOfParamsRet"]
                type_annotations += returns[index]["type_annotations"]
                c_index += 1
            elif isinstance(child, ast.FunctionDef) or isinstance(child, ast.AsyncFunctionDef):
                count["function"] += 1
                functions.append(returns[index])
                functions_body_size += returns[index]["function"].bodyCount
                type_annotations += returns[index]["type_annotations"]
                params_rets += returns[index]["numberOfParamsRet"]
                f_index += 1
            elif isinstance(child, ast.Import):
                simple_import_num += 1
                simple_imports.append(returns[index])
                si_index += 1
                simple_import_modules_num += returns[index]["importedModules"]
                if si_index + fi_index != index:
                    local_imports += 1
            elif isinstance(child, ast.ImportFrom):
                from_import_num += 1
                from_imports.append(returns[index])
                fi_index += 1
                as_names += returns[index]["as_names"]
                from_import_modules_num += returns[index]["importedModules"]
                if si_index + fi_index != index:
                    local_imports += 1
            elif isinstance(child, ast.stmt):
                count["stmt"] += 1
            if isinstance(child, ast.If) and not has_entry_point:
                if ast.unparse(child.test) == "__name__ == '__main__'":
                    has_entry_point = True
            index += 1
        ########## ENTITY PROPERTIES ############
        db_module.name = params["filename"]
        db_module.nameConvention = self.name_convention(db_module.name)
        db_module.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        db_module.globalStmtsPct = count["stmt"]/index if(index > 0) else 0
        db_module.globalExpressions = count["expr"]/index if(index > 0) else 0
        db_module.numberOfClasses = count["classes"]
        db_module.numberOfFunctions = count["function"]
        enum_class_funct_sum = (count["function"] + count["enum"] + count["classes"])
        db_module.classDefsPct = count["classes"]/enum_class_funct_sum if(enum_class_funct_sum > 0) else 0
        db_module.functionDefsPct = count["function"]/enum_class_funct_sum if(enum_class_funct_sum > 0) else 0
        db_module.enumDefsPct = count["enum"]/enum_class_funct_sum if(enum_class_funct_sum > 0) else 0
        db_module.averageStmtsFunctionBody = functions_body_size/f_index if(f_index > 0) else 0
        db_module.averageStmtsMethodBody = number_of_method_stmt/method_count if(method_count > 0) else 0
        db_module.typeAnnotationsPct = type_annotations/params_rets if params_rets > 0 else 0
        db_module.path = params["path"]
        db_module.hasEntryPoint = has_entry_point
        db_module.expertise_level = params["expertise_level"]
        db_module.user_id = params["user_id"]
        #------------ imports --------------------
        db_import.numberImports = (si_index + fi_index)
        db_import.moduleImportsPct = simple_import_num/(si_index + fi_index) if si_index + fi_index > 0 else 0
        db_import.fromImportsPct = from_import_num/(si_index + fi_index) if si_index + fi_index > 0 else 0
        db_import.localImportsPct = local_imports/(si_index + fi_index) if si_index + fi_index > 0 else 0
        db_import.averageAsInImportedModules = as_names/from_import_modules_num if from_import_modules_num > 0 else 0
        db_import.averageImportedModules = simple_import_modules_num/si_index if si_index > 0 else 0
        db_import.averageFromImportedModules = from_import_modules_num/fi_index if fi_index > 0 else 0
        db_import.expertise_level = params["expertise_level"]
        db_import.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_module, 'db_node': db_node, 'db_import': db_import})
        return {"classdefs": count["classes"], "functionDefs": count["function"], "enumDefs": count["enum"]}
    
    def visit_FunctionDef(self, node: ast.FunctionDef, params: Dict) -> Dict: 
        is_method = params["parent"].table == 'ClassDefs'
        db_node = db_entities.db_node()
        db_functiondef = db_entities.DBFunctionDef()
        if is_method:
            db_method = db_entities.DBMethodDef()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_functiondef.functiondef_id = db_functiondef.parameters_id = node_id
        db_functiondef.module_id = db_functiondef.parent_id = None
        db_node.parent_id = params["parent_id"]
        db_node.parent_table = params["parent"].table
        if isinstance(params['parent'], db_entities.DBModule):
            db_functiondef.module_id = params["parent_id"]
        else:
            db_functiondef.parent_id = params["parent_id"]
        if is_method:
            db_method.classdef_id = params["parent_id"]
            db_method.methoddef_id = node_id
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_functiondef, "depth": params["depth"] + 1, "parent_id": node_id}
        if is_method:
            stmt_roles = ["MethodDef"]
            expr_roles = ["FuncDecorator", "ReturnType", "MethodBody"]
        else:
            stmt_roles = ["FunctionDef"]
            expr_roles = ["FuncDecorator", "ReturnType", "FuncBody"]
        ########## ENTITY PROPERTIES ############
        number_of_body_expr = 0
        depth = 0
        have_return = False
        have_ret_annotation = False
        ############## PROPAGAR VISIT ############
        args = self.visit(node.args, self.add_param(self.add_param(child_params, "params_id", node_id), "role", "FunctionParams"))
        for child in node.body:
            if isinstance(child,ast.Expr):
                aux = self.visit(child, self.add_param(child_params, "role", expr_roles[2]))
                number_of_body_expr += 1
            else:
                aux = self.visit(child, self.add_param(child_params, "role", stmt_roles[0]))
            if isinstance(child,ast.Return):
                have_return = True
            depth = max(depth, aux["depth"])
        for child in node.decorator_list:
            self.visit(child, self.add_param(child_params, "role", expr_roles[0]))
        if node.returns:
            aux = self.visit(node.returns, self.add_param(child_params, "role", expr_roles[1]))
            depth = max(depth, aux["depth"])
            have_ret_annotation = True
        for child in node.type_params:
            self.visit(child, child_params)
        ########## ENTITY PROPERTIES ############
        what_is_it = self.what_is_it(node)
        args_ret = args['numberOfArgs'] + 1 if have_return or have_ret_annotation else args['numberOfArgs']
        number_of_annotations = args['typeAnnotations'] + 1 if have_ret_annotation else args['typeAnnotations']
        db_functiondef.nameConvention = self.name_convention(node.name)
        db_functiondef.numberOfCharacters = len(node.name)
        db_functiondef.isPrivate = what_is_it["private"]
        db_functiondef.isMagic = what_is_it["magic"]
        db_functiondef.bodyCount = len(node.body)
        db_functiondef.expressionsPct = number_of_body_expr/len(node.body) if len(node.body) > 0 else 0
        db_functiondef.isAsync = False
        db_functiondef.numberOfDecorators = len(node.decorator_list)
        db_functiondef.hasReturnTypeAnnotation = True if node.returns else False
        db_functiondef.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        db_functiondef.height = params["depth"]
        db_functiondef.typeAnnotationsPct = number_of_annotations/args_ret if args_ret > 0 else 0
        db_functiondef.sourceCode = ast.unparse(node)
        db_functiondef.expertise_level = params["expertise_level"]
        db_functiondef.user_id = params["user_id"]
        if is_method:
            db_method.isClassMethod = what_is_it["classmethod"]
            db_method.isStaticMethod = what_is_it["static"]
            db_method.isConstructorMethod = node.name == '__init__'
            db_method.isAbstractMethod = what_is_it["abstract"]
            db_method.isProperty = what_is_it["property"]
            db_method.isWrapper = what_is_it["wrapper"]
            db_method.isCached = what_is_it["cached"]
            db_method.expertise_level = params["expertise_level"]
            db_method.user_id = params["user_id"]
        ############## VISITOR DB ################
        if is_method:
            self.visitor_db.visit(node, {'node': db_functiondef, 'db_node': db_node, 'is_method': is_method, 'db_method': db_method})
            return {'db_method': db_method, 'db_functiondef': db_functiondef, 'args': args, 'typeAnnotations': args["typeAnnotations"], 'depth': depth + 1, 'node_id': db_functiondef.functiondef_id, 'have_return': have_return}
        else:
            self.visitor_db.visit(node, {'node': db_functiondef, 'db_node': db_node, 'is_method': is_method})
            return {'numberOfParamsRet': args_ret, 'db_functiondef': db_functiondef, 'typeAnnotations': args["typeAnnotations"], 'depth': depth + 1, 'node_id': db_functiondef.functiondef_id}
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef, params: Dict) -> Dict: 
        is_method = params["parent"].table == 'ClassDefs'
        db_node = db_entities.db_node()
        db_function = db_entities.DBFunctionDef()
        if is_method:
            db_method = db_entities.DBMethodDef()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_function.functiondef_id = db_function.parameters_id = node_id
        db_function.module_id = db_function.parent_id = None
        db_node.parent_id = params["parent_id"]
        db_node.parent_table = params["parent"].table
        if isinstance(params['parent'], db_entities.DBModule):
            db_function.module_id = params["parent_id"]
        else:
            db_function.parent_id = params["parent_id"]
        if is_method:
            db_method.classdef_id = params["parent_id"]
            db_method.methoddef_id = node_id
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_function, "depth": params["depth"] + 1, "parent_id": node_id}
        if is_method:
            stmt_roles = ["AsyncMethodDef"]
            expr_roles = ["FuncDecorator", "ReturnType", "MethodBody"]
        else:
            stmt_roles = ["AsyncFunctionDef"]
            expr_roles = ["FuncDecorator", "ReturnType", "FuncBody"]
        ########## ENTITY PROPERTIES ############
        number_of_body_expr = 0
        depth = 0
        have_return = False
        have_ret_annotation = False
        ############## PROPAGAR VISIT ############
        args = self.visit(node.args, self.add_param(self.add_param(child_params, "params_id", node_id), "role", "FunctionParams"))
        for child in node.body:
            if isinstance(child, ast.Expr):
                aux = self.visit(child, self.add_param(child_params, "role", expr_roles[2]))
                number_of_body_expr += 1
            else:
                aux = self.visit(child, self.add_param(child_params, "role", stmt_roles[0]))
            if isinstance(child, ast.Return):
                have_return = True
            depth = max(depth, aux["depth"])
        for child in node.decorator_list:
            self.visit(child, self.add_param(child_params, "role", expr_roles[0]))
        if node.returns:
            aux = self.visit(node.returns, self.add_param(child_params, "role", expr_roles[1]))
            depth = max(depth, aux["depth"])
            have_ret_annotation = True
        for child in node.type_params:
            self.visit(child, child_params)
        ########## ENTITY PROPERTIES ############
        what_is_it = self.what_is_it(node)
        args_ret = args['numberOfArgs'] + 1 if have_return or have_ret_annotation else args['numberOfArgs']
        number_of_annotations = args['typeAnnotations'] + 1 if have_ret_annotation else args['typeAnnotations']
        db_function.numberOfCharacters = len(node.name)
        db_function.nameConvention = self.name_convention(node.name)
        db_function.isPrivate = what_is_it["private"]
        db_function.isMagic = what_is_it["magic"]
        db_function.bodyCount = len(node.body)
        db_function.expressionsPct = number_of_body_expr/len(node.body) if len(node.body) > 0 else 0
        db_function.isAsync = True
        db_function.numberOfDecorators = len(node.decorator_list)
        db_function.hasReturnTypeAnnotation = True if node.returns else False
        db_function.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        db_function.height = params["depth"]
        db_function.typeAnnotationsPct = number_of_annotations/args_ret if args_ret > 0 else 0
        db_function.sourceCode = ast.unparse(node)
        db_function.expertise_level = params["expertise_level"]
        db_function.user_id = params["user_id"]
        if is_method:
            db_method.isClassMethod = what_is_it["classmethod"]
            db_method.isStaticMethod = what_is_it["static"]
            db_method.isConstructorMethod = node.name == '__init__'
            db_method.isAbstractMethod = what_is_it["abstract"]
            db_method.isProperty = what_is_it["property"]
            db_method.isWrapper = what_is_it["wrapper"]
            db_method.isCached = what_is_it["cached"]
            db_method.expertise_level = params["expertise_level"]
            db_method.user_id = params["user_id"]
        ############## VISITOR DB ################
        if is_method:
            self.visitor_db.visit(node, {'node': db_function, 'db_node': db_node, 'is_method': is_method, 'db_method': db_method})
            return {'db_method': db_method, 'db_function': db_function, 'args': args, 'typeAnnotations': args["typeAnnotations"], 'depth': depth + 1, 'node_id': db_function.functiondef_id, 'have_return': have_return}
        else:
            self.visitor_db.visit(node, {'node': db_function, 'db_node': db_node, 'is_method': is_method})
            return {'numberOfParamsRet': args_ret, 'db_function': db_function, 'typeAnnotations': args["typeAnnotations"], 'depth': depth + 1, 'node_id': db_function.functiondef_id}
        
    def visit_ClassDef(self, node: ast.ClassDef, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_classdef = db_entities.DBClassDef()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_classdef.classdef_id = node_id
        db_classdef.module_id = db_classdef.parent_id = None
        db_node.parent_id = params["parent_id"]
        db_node.parent_table = params["parent"].table
        if isinstance(params['parent'], db_entities.DBModule):
            db_classdef.module_id = params["parent_id"]
        else:
            db_classdef.parent_id = params["parent_id"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_classdef, "depth": params["depth"] + 1, "parent_id": node_id}
        stmt_roles = ["ClassDef"]
        expr_roles = ["ClassBase", "ClassDecorator", "ClassBody"]
        ########## ENTITY PROPERTIES ############
        number_of_methods = 0
        body_count = len(node.body)
        assignment_number = 0
        expression_number = 0
        metaclass_number = 0
        keyword_number = 0
        number_of_method_stmt = 0
        number_of_private_methods = 0
        number_of_method_type_annotations = 0
        number_of_method_params_ret = 0
        number_of_magic_methods = 0
        number_of_async_methods = 0
        number_of_class_methods = 0
        number_of_static_methods = 0
        number_of_abstract_methods = 0
        number_of_property_methods = 0
        is_enum = False
        depth = 0
        ############## PROPAGAR VISIT ############
        for child in node.bases:
            self.visit(child, self.add_param(child_params, "role", expr_roles[0]))
            if isinstance(child, ast.Name):
                is_enum = (child.id == 'Enum')
            elif isinstance(child, ast.Attribute):
                is_enum = (child.attr == 'Enum')
        for child in node.keywords:
            if child.arg == 'metaclass':
                metaclass_number += 1
            else:
                keyword_number += 1
            self.visit(child, self.add_param(child_params, "role", expr_roles[0]))
        for child in node.body:
            if isinstance(child, ast.Expr):
                expression_number += 1
                returns = self.visit(child, self.add_param(child_params, "role", expr_roles[2]))
            else:
                if isinstance(child, ast.AnnAssign) or isinstance(child, ast.AugAssign) or isinstance(child, ast.Assign):
                    assignment_number += 1
                returns = self.visit(child, self.add_param(child_params, "role", stmt_roles[0]))
                if isinstance(child,ast.FunctionDef) or isinstance(child,ast.AsyncFunctionDef):
                    number_of_methods += 1
                    number_of_method_stmt += returns["function"].bodyCount
                    number_of_method_params_ret += (returns["args"]["numberOfArgs"])
                    if returns['haveReturn']:
                        number_of_method_params_ret += 1
                    number_of_method_type_annotations += returns["args"]["typeAnnotations"]
                    if returns["function"].isMagic:
                        number_of_magic_methods += 1
                    if returns["function"].isPrivate:
                        number_of_private_methods += 1
                    if returns["function"].isAsync:
                        number_of_async_methods += 1
                    if returns["method"].isAbstractMethod:
                        number_of_abstract_methods += 1
                    if returns["method"].isClassMethod:
                        number_of_class_methods += 1
                    if returns["method"].isStaticMethod:
                        number_of_static_methods += 1
                    if returns["method"].isProperty:
                        number_of_property_methods += 1
            depth = max(depth, returns["depth"])
        for child in node.decorator_list:
            self.visit(child, self.add_param(child_params, "role", expr_roles[1]))
        for child in node.type_params:
            self.visit(child, child_params)
        ########## ENTITY PROPERTIES ############
        db_classdef.nameConvention = self.name_convention(node.name)
        db_classdef.isEnumClass = is_enum
        db_classdef.numberOfCharacters = len(node.name)
        db_classdef.numberOfMethods = number_of_methods
        db_classdef.numberOfDecorators = len(node.decorator_list)
        db_classdef.numberOfBaseClasses = len(node.bases)
        db_classdef.hasGenericTypeAnnotations = len(node.type_params) > 0
        db_classdef.hasDocString = (isinstance(node.body[0],ast.Constant)) and isinstance(node.body[0].value, str)
        db_classdef.bodyCount = body_count
        db_classdef.assignmentsPct = assignment_number/body_count if body_count > 0 else 0
        db_classdef.expressionsPct = expression_number/body_count if body_count > 0 else 0
        db_classdef.usesMetaclass = metaclass_number > 0
        db_classdef.numberOfKeyWords = keyword_number
        db_classdef.height = params["depth"]
        db_classdef.averageStmtsMethodBody = number_of_method_stmt/number_of_methods if number_of_methods > 0 else 0
        db_classdef.typeAnnotationsPct = number_of_method_type_annotations/number_of_method_params_ret if number_of_method_params_ret > 0 else 0
        db_classdef.privateMethodsPct = number_of_private_methods/number_of_methods if number_of_methods > 0 else 0
        db_classdef.magicMethodsPct = number_of_magic_methods/number_of_methods if number_of_methods > 0 else 0
        db_classdef.asyncMethodsPct = number_of_async_methods/number_of_methods if number_of_methods > 0 else 0
        db_classdef.classMethodsPct = number_of_class_methods/number_of_methods if number_of_methods > 0 else 0
        db_classdef.staticMethodsPct = number_of_static_methods/number_of_methods if number_of_methods > 0 else 0
        db_classdef.abstractMethodsPct = number_of_abstract_methods/number_of_methods if number_of_methods > 0 else 0
        db_classdef.propertyMethodsPct = number_of_property_methods/number_of_methods if number_of_methods > 0 else 0
        db_classdef.sourceCode = ast.unparse(node)
        db_classdef.expertise_level = params['expertise_level']
        db_classdef.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_classdef, 'db_node': db_node})
        return {'numberOfParamsRet': number_of_method_params_ret, 'methodCount': number_of_methods, 'typeAnnotations': number_of_method_type_annotations, 'number_of_method_stmt': number_of_method_stmt, 'node_id': db_classdef.classdef_id, 'depth': depth + 1, 'is_enum': is_enum}

    ############################### STATEMENTS #############################
    def visit_Return(self, node: ast.Return, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id, "role": "Return"}
        ########## ENTITY PROPERTIES ############
        returns = None
        ############## PROPAGAR VISIT ############
        if node.value:
            returns = self.visit(node.value, child_params)
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        if returns:
            db_stmt.depth = returns["depth"]
            db_stmt.first_child_id = returns["id"]
        else:
            db_stmt.depth = 0
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.hasOrElse = None
        db_stmt.bodySize = None
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}

    def visit_Delete(self, node: ast.Delete, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id, "role": "Delete"}
        ########## ENTITY PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.targets:
            returns.append(self.visit(child, child_params))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.depth = depth
        db_stmt.first_child_id = first_child_id
        db_stmt.second_child_id = second_child_id
        db_stmt.third_child_id = third_child_id
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.hasOrElse = None
        db_stmt.bodySize = None
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}

    def visit_Assign(self, node: ast.Assign, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = "AssignmentStmt"
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        roles = ["AssignLHS", "AssignRHS"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns_targets = []
        index = 0
        for child in node.targets:
            returns_targets.append(self.visit(child, self.add_param(child_params, 'role', roles[0])))
            depth = max(depth, returns_targets[index]["depth"])
            if index == 0: 
                first_child_id = returns_targets[index]["id"]
            if index == 1: 
                second_child_id = returns_targets[index]["id"]
            if index == 2: 
                third_child_id = returns_targets[index]["id"]
            index += 1
        returns_value = self.visit(node.value, self.add_param(child_params, 'role', roles[1]))
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.depth = 0
        db_stmt.depth = max(returns_value["depth"], depth)
        db_stmt.first_child_id = first_child_id
        db_stmt.second_child_id = second_child_id
        db_stmt.third_child_id = third_child_id
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.hasOrElse = None
        db_stmt.bodySize = None
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}
    
    def visit_TypeAlias(self, node: ast.TypeAlias, params: Dict) -> Dict: 
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        roles = ["TypeAliasLHS", "TypeAliasRHS"]
        ############## PROPAGAR VISIT ############
        returns = []
        for child in node.type_params:
            self.visit(child, child_params)
        returns.append(self.visit(node.name, self.add_param(child_params, 'role', roles[0])))
        returns.append(self.visit(node.value, self.add_param(child_params, 'role', roles[1])))
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.depth = max(returns[0]["depth"], returns[1]["depth"])
        db_stmt.first_child_id = returns[0]["id"]
        db_stmt.second_child_id = returns[1]["id"]
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.hasOrElse = None
        db_stmt.bodySize = None
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}
    
    def visit_AugAssign(self, node: ast.AugAssign, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = "AugmentedAssignment"
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        roles = ["AugmentedAssigmentLHS", "AugmentedAssigmentRHS"]
        ############## PROPAGAR VISIT ############
        returns = []
        returns.append(self.visit(node.target, self.add_param(child_params, 'role', roles[0])))
        returns.append(self.visit(node.value, self.add_param(child_params, 'role', roles[1])))
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.depth = max(returns[0]["depth"], returns[1]["depth"])
        db_stmt.first_child_id = returns[0]["id"]
        db_stmt.second_child_id = returns[1]["id"]
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.hasOrElse = None
        db_stmt.bodySize = None
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}

    def visit_AnnAssign(self, node: ast.AnnAssign, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = "AnnotatedAssignment"
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        roles = ["VarDefVarName", "VarDefType", "VarDefInitValue"]
        ############## PROPAGAR VISIT ############
        returns = []
        returns.append(self.visit(node.target, self.add_param(child_params, 'role', roles[0])))
        returns.append(self.visit(node.annotation, self.add_param(child_params, 'role', roles[1])))
        if node.value: 
            returns.append(self.visit(node.value, self.add_param(child_params, 'role', roles[2])))
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.depth = max(returns[0]["depth"], returns[1]["depth"])
        db_stmt.first_child_id = returns[0]["id"]
        db_stmt.second_child_id = returns[1]["id"]
        if len(returns) > 2:
            db_stmt.third_child_id = returns[2]["id"]
            db_stmt.depth = max(db_stmt.depth, returns[2]["depth"])
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.hasOrElse = None
        db_stmt.bodySize = None
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}

    def visit_For(self, node: ast.For, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        stmt_roles = ["For", "ForElse"]
        expr_roles = ["ForElement", "ForEnumerable", "ForBody", "ForElseBody"]
        ########## ENTITY PROPERTIES ############
        db_stmt.hasOrElse = False
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        has_or_else = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        returns_target = self.visit(node.target, self.add_param(child_params, 'role', expr_roles[0]))
        returns_iter = self.visit(node.iter, self.add_param(child_params, 'role', expr_roles[1]))
        for child in node.body:
            if isinstance(child, ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", expr_roles[2])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmt_roles[0])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        for child in node.orelse:
            has_or_else = True
            if isinstance(child,ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", expr_roles[3])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmt_roles[1])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.height = params["depth"]
        db_stmt.depth = max(returns_target["depth"],max(returns_iter["depth"],depth))
        db_stmt.first_child_id = first_child_id
        db_stmt.second_child_id = second_child_id
        db_stmt.third_child_id = third_child_id
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.bodySize = index
        db_stmt.hasOrElse = has_or_else
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}
    
    def visit_AsyncFor(self, node: ast.AsyncFor, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = "For"
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        stmtRoles = ["AsyncFor", "AsyncForElse"]
        exprRoles = ["AsyncForElement", "AsyncForEnumerable", "AsyncForBody", "AsyncForElseBody"]
        ########## ENTITY PROPERTIES ############
        db_stmt.hasOrElse = False
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        has_or_else = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        returns_target = self.visit(node.target, self.add_param(child_params, 'role', exprRoles[0]))
        returns_iter = self.visit(node.iter, self.add_param(child_params, 'role', exprRoles[1]))
        for child in node.body:
            if isinstance(child, ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmtRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        for child in node.orelse:
            has_or_else = True
            if isinstance(child, ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", exprRoles[3])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmtRoles[1])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.height = params["depth"]
        db_stmt.depth = max(returns_target["depth"], returns_iter["depth"], depth)
        db_stmt.first_child_id = first_child_id
        db_stmt.second_child_id = second_child_id
        db_stmt.third_child_id = third_child_id
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.bodySize = index
        db_stmt.hasOrElse = has_or_else
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}
    
    def visit_While(self, node: ast.While, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        stmt_roles = ["While", "WhileElse"]
        expr_roles = ["WhileCondition", "WhileBody", "WhileElseBody"]
        ########## ENTITY PROPERTIES ############
        db_stmt.hasOrElse = False
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        has_or_else = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        returns_test = self.visit(node.test, self.add_param(child_params, 'role', expr_roles[0]))
        for child in node.body:
            if isinstance(child,ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", expr_roles[1])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmt_roles[0])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        for child in node.orelse:
            has_or_else = True
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.add_param(child_params, "role", expr_roles[2])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmt_roles[1])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.depth = max(returns_test["depth"], depth)
        db_stmt.first_child_id = first_child_id
        db_stmt.second_child_id = second_child_id
        db_stmt.third_child_id = third_child_id
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.bodySize = index
        db_stmt.hasOrElse = has_or_else
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}

    def visit_If(self, node: ast.If, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        stmtRoles = ["If", "IfElse"]
        exprRoles = ["IfCondition", "IfBody", "IfElseBody"]
        ########## ENTITY PROPERTIES ############
        db_stmt.hasOrElse = False
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        has_or_else = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        returns_test = self.visit(node.test, self.add_param(child_params, 'role', exprRoles[0]))
        for child in node.body:
            if isinstance(child, ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", exprRoles[1])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmtRoles[0])))
            
                depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        body_size = index
        for child in node.orelse:
            has_or_else = True
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.add_param(child_params, "role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmtRoles[1])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.depth = max(returns_test["depth"],depth)
        db_stmt.first_child_id = first_child_id
        db_stmt.second_child_id = second_child_id
        db_stmt.third_child_id = third_child_id
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.bodySize = body_size
        db_stmt.hasOrElse = has_or_else
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}

    def visit_With(self, node: ast.With, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        stmt_roles = ["With"]
        expr_roles = ["WithElement", "WithAs", "WithBody"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.body:
            if isinstance(child, ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", expr_roles[2])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmt_roles[0])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        for child in node.items:
            self.visit(child, self.add_param(self.add_param(child_params, "role_ctx", expr_roles[0]), 'role_vars', expr_roles[1]))
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.height = params["depth"]
        db_stmt.hasOrElse = None
        db_stmt.depth = depth
        db_stmt.first_child_id = first_child_id
        db_stmt.second_child_id = second_child_id
        db_stmt.third_child_id = third_child_id
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.bodySize = index
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}

    
    def visit_AsyncWith(self, node: ast.AsyncWith, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        stmt_roles = ["AsyncWith"]
        expr_roles = ["AsyncWithElement", "AsyncWithAs", "AsyncWithBody"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.body:
            if isinstance(child, ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", expr_roles[2])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmt_roles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.items:
            self.visit(child, self.add_param(self.add_param(child_params, "role_ctx", expr_roles[0]), 'role_vars', expr_roles[1]))
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.hasOrElse = None
        db_stmt.depth = depth
        db_stmt.first_child_id = first_child_id
        db_stmt.second_child_id = second_child_id
        db_stmt.third_child_id = third_child_id
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.bodySize = index
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}
    
    def visit_Match(self, node: ast.Match, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        case = db_entities.DBCase()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        exprRoles = ["MatchCondition"]
        ############## PROPAGAR VISIT ############
        returns = []
        depth = 0
        index = 0
        subject = self.visit(node.subject, self.add_param(child_params, 'role', exprRoles[0]))
        for child in node.cases:
            returns.append(self.visit(child, child_params))
            depth = max(depth, returns[index]["depth"])
            index += 1
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.first_child_id = subject["id"]
        db_stmt.hasOrElse = None
        db_stmt.depth = max(depth,subject["depth"])
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.bodySize = None
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        #-----------------------------------------
        number_of_cases_as = 0
        number_of_cases_or = 0
        number_of_cases_value = 0
        number_of_cases_singleton = 0
        number_of_cases_sequence = 0
        number_of_cases_mapping = 0
        number_of_cases_class = 0
        number_of_cases_star = 0
        number_of_guards = 0
        body_total_count = 0
        for i in range(index):
            number_of_cases_as += returns[i]["matchAs"]
            number_of_cases_or += returns[i]["matchOr"]
            number_of_cases_value += returns[i]["matchValue"]
            number_of_cases_mapping += returns[i]["matchMapping"]
            number_of_cases_class += returns[i]["matchClass"]
            number_of_cases_singleton += returns[i]["matchSingleton"]
            number_of_cases_sequence += returns[i]["matchSequence"]
            number_of_cases_star += returns[i]["matchStar"]
            number_of_guards += returns[i]["guards"]
            body_total_count += returns[i]["bodyCount"]
        total_cases = number_of_cases_as + number_of_cases_or + number_of_cases_mapping + number_of_cases_sequence + number_of_cases_singleton + number_of_cases_star + number_of_cases_class + number_of_cases_value
        case.numberOfCases = total_cases
        case.guards = number_of_guards/total_cases if total_cases > 0 else 0
        case.averageBodyCount = body_total_count/index if index > 0 else 0
        case.averageMatchValue = number_of_cases_value/total_cases if total_cases > 0 else 0
        case.averageMatchSingleton = number_of_cases_singleton/total_cases if total_cases > 0 else 0
        case.averageMatchSequence = number_of_cases_sequence/total_cases if total_cases > 0 else 0
        case.averageMatchMapping = number_of_cases_mapping/total_cases if total_cases > 0 else 0
        case.averageMatchClass = number_of_cases_class/total_cases if total_cases > 0 else 0
        case.averageMatchStar = number_of_cases_star/total_cases if total_cases > 0 else 0
        case.averageMatchAs = number_of_cases_as/total_cases if total_cases > 0 else 0
        case.averageMatchOr = number_of_cases_or/total_cases if total_cases > 0 else 0
        case.statement_id = node_id
        case.expertise_level = params["expertise_level"]
        case.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node, 'case': case})
        return {'id': node_id, 'depth': db_stmt.depth + 1}

    def visit_Raise(self, node: ast.Raise, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        expr_roles = ["Raise", "RaiseFrom"]
        ########## ENTITY PROPERTIES ############
        cause = None
        exc = None
        ############## PROPAGAR VISIT ############
        if node.exc:
            exc = self.visit(node.exc, self.add_param(child_params, 'role', expr_roles[0]))
        if node.cause:
            cause = self.visit(node.cause, self.add_param(child_params, 'role', expr_roles[1]))
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.hasOrElse = None
        if exc:
            db_stmt.first_child_id = exc["id"]
            if cause:
                db_stmt.second_child_id = cause["id"]
                db_stmt.depth = max(exc["depth"], cause["depth"])
            else:
                db_stmt.depth = exc["depth"]
        else:
            if cause:
                db_stmt.first_child_id = cause["id"]
                db_stmt.depth = cause["depth"]
            else:
                db_stmt.depth = 0
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.bodySize = None
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node})
        return {'id': node_id, 'depth': db_stmt.depth + 1}
    
    def visit_Try(self, node: ast.Try, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_stmt = db_entities.DBStatement()
        db_handler = db_entities.DBHandler()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_stmt.statement_id = db_handler.statement_id = node_id
        db_node.parent_id = db_stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_stmt.parent = params["parent"].category
        ############# ROLES ######################
        db_stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_stmt, "depth": params["depth"] + 1, "parent_id": node_id}
        stmt_roles = ["Try", "TryElse", "TryFinally", "TryHandler"]
        expr_roles = ["TryBody", "TryElse", "FinallyBody"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        has_or_else = False
        ############## PROPAGAR VISIT ############
        returns = []
        handlers = []
        index = 0
        h_index = 0
        handlers_bodies = 0
        for child in node.body:
            if isinstance(child, ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", expr_roles[0])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmt_roles[0])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        for child in node.handlers:
            handlers.append(self.visit(child, self.add_param(self.add_param(child_params, "role", stmt_roles[3]), 'handler', db_handler)))
            depth = max(depth, handlers[h_index]["depth"])
            for node_id in handlers[h_index]['child_ids']:
                returns.append(node_id)
                if index == 0:
                    first_child_id = node_id
                if index == 1:
                    second_child_id = node_id
                if index == 2:
                    third_child_id = node_id
                index += 1
            h_index += 1
        for child in node.orelse:
            if isinstance(child, ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", expr_roles[1])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmt_roles[1])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
            has_or_else = True
        for child in node.finalbody:
            if isinstance(child, ast.Expr):
                returns.append(self.visit(child, self.add_param(child_params, "role", expr_roles[2])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmt_roles[2])))
            depth = max(depth, returns[index]["depth"])
            if index == 0:
                first_child_id = returns[index]["id"]
            if index == 1:
                second_child_id = returns[index]["id"]
            if index == 2:
                third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITY PROPERTIES ############
        db_stmt.height = params["depth"]
        db_stmt.hasOrElse = has_or_else
        db_stmt.depth = depth
        db_stmt.first_child_id = first_child_id
        db_stmt.second_child_id = second_child_id
        db_stmt.third_child_id = third_child_id
        db_stmt.sourceCode = ast.unparse(node)
        db_stmt.bodySize = index
        db_stmt.expertise_level = params["expertise_level"]
        db_stmt.user_id = params["user_id"]
        #--------------- handler -----------------
        db_handler.numberOfHandlers = h_index
        if node.finalbody:
            db_handler.hasFinally = True
        else:
            db_handler.hasFinally = False
        db_handler.hasCatchAll = False
        for child in handlers:
            if child["isCatchAll"]:
                db_handler.hasCatchAll = True
        db_handler.averageBodyCount = handlers_bodies/h_index if h_index > 0 else 0
        db_handler.hasStar = False
        db_handler.expertise_level = params["expertise_level"]
        db_handler.user_id = params["user_id"]
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_stmt, 'db_node': db_node, 'handler': db_handler})
        return {'id': node_id, 'depth': db_stmt.depth + 1}
    
    def visit_TryStar(self, node: ast.TryStar, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        stmt = db_entities.DBStatement()
        handler = db_entities.DBHandler()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = stmt.statement_id = handler.statement_id = id
        db_node.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = "Try"
        db_node.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": stmt, "depth": params["depth"] + 1, "parent_id": id}
        stmtRoles = ["Try", "TryElse", "TryFinally", "TryHandlerStar"]
        exprRoles = ["TryBody", "TryElse", "FinallyBody"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        first_child_id = None
        second_child_id = None
        third_child_id = None
        hasOrElse = False
        ############## PROPAGAR VISIT ############
        returns = []
        handlers = []
        index = 0
        hindex = 0
        handlersBodies = 0
        for child in node.body:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.add_param(child_params, "role", exprRoles[0])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmtRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        for child in node.handlers:
            handlers.append(self.visit(child, self.add_param(self.add_param(child_params, "role", stmtRoles[3]), 'handler', handler)))
            depth = max(depth, handlers[hindex]["depth"])
            hindex += 1
            for id in handlers[hindex]['child_ids']:
                returns.append(id)
                if(index == 0): first_child_id = returns[index]["id"]
                if(index == 1): second_child_id = returns[index]["id"]
                if(index == 2): third_child_id = returns[index]["id"]
                index += 1
        for child in node.orelse:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.add_param(child_params, "role", exprRoles[1])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmtRoles[1])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
            hasOrElse = True
        for child in node.finalbody:
            if(isinstance(child,ast.Expr)):
                returns.append(self.visit(child, self.add_param(child_params, "role", exprRoles[2])))
            else:
                returns.append(self.visit(child, self.add_param(child_params, "role", stmtRoles[2])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_id = returns[index]["id"]
            if(index == 1): second_child_id = returns[index]["id"]
            if(index == 2): third_child_id = returns[index]["id"]
            index += 1
        ########## ENTITY PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = hasOrElse
        stmt.depth = depth
        stmt.first_child_id = first_child_id
        stmt.second_child_id = second_child_id
        stmt.third_child_id = third_child_id
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = index
        stmt.expertise_level = params['expertise_level']
        stmt.user_id = params['user_id']
        #--------------- handler -----------------
        handler.numberOfHandlers = hindex
        if(node.finalbody):
            handler.hasFinally = True
        else:
            handler.hasFinally = False
        handler.hasCatchAll = False
        for child in handlers:
            if(child.isCatchAll): handler.hasCatchAll = True
        handler.averageBodyCount = handlersBodies/hindex if hindex > 0 else 0
        handler.hasStar = True
        handler.expertise_level = params['expertise_level']
        handler.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': stmt, 'db_node': db_node, 'handler': handler})
        return {'id': id, 'depth': stmt.depth + 1}

    
    def visit_Assert(self, node: ast.Assert, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        stmt = db_entities.DBStatement()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = stmt.statement_id = id
        db_node.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES #######################
        stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": stmt, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["AssertCondition", "AssertMessage"]
        ########## ENTITY PROPERTIES ############
        msg = None
        ############## PROPAGAR VISIT ############
        test = self.visit(node.test, self.add_param(child_params, 'role', exprRoles[0]))
        if(node.msg): msg = self.visit(node.msg, self.add_param(child_params, 'role', exprRoles[1]))
        ########## ENTITY PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.first_child_id = test["id"]
        stmt.depth = test["depth"]
        if(msg):
            stmt.second_child_id = msg["id"]  
            stmt.depth = max(msg["depth"], stmt.depth)
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        stmt.expertise_level = params['expertise_level']
        stmt.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': stmt, 'db_node': db_node})
        return {'id': id, 'depth': stmt.depth + 1}

    
    def visit_Global(self, node: ast.Global, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        stmt = db_entities.DBStatement()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = stmt.statement_id = id
        db_node.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITY PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        stmt.expertise_level = params['expertise_level']
        stmt.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': stmt, 'db_node': db_node})
        return {'id': id, 'depth': stmt.depth + 1}

    
    def visit_Nonlocal(self, node: ast.Nonlocal, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        stmt = db_entities.DBStatement()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = stmt.statement_id = id
        db_node.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITY PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        stmt.expertise_level = params['expertise_level']
        stmt.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': stmt, 'db_node': db_node})
        return {'id': id, 'depth': stmt.depth + 1}

    
    def visit_Pass(self, node: ast.Pass, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        stmt = db_entities.DBStatement()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = stmt.statement_id = id
        db_node.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITY PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        stmt.expertise_level = params['expertise_level']
        stmt.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': stmt, 'db_node': db_node})
        return {'id': id, 'depth': stmt.depth + 1}

    
    def visit_Break(self, node: ast.Break, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        stmt = db_entities.DBStatement()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = stmt.statement_id = id
        db_node.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITY PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        stmt.expertise_level = params['expertise_level']
        stmt.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': stmt, 'db_node': db_node})
        return {'id': id, 'depth': stmt.depth + 1}

    
    def visit_Continue(self, node: ast.Continue, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        stmt = db_entities.DBStatement()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = stmt.statement_id = id
        db_node.parent_id = stmt.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITY PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        stmt.expertise_level = params['expertise_level']
        stmt.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': stmt, 'db_node': db_node})
        return {'id': id, 'depth': stmt.depth + 1}

    ############################ IMPORTS ##################################

    
    def visit_Import(self, node: ast.Import, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        stmt = db_entities.DBStatement()
        ############ IDS #########################
        id = self.id_manager.get_id()
        stmt.statement_id = db_node.node_id = id
        db_node.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITY PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        stmt.expertise_level = params['expertise_level']
        stmt.user_id = params['user_id']
        asnames = 0
        for alias in node.names:
            if(alias.asname): asnames += 1
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': stmt, 'db_node': db_node})
        return {'id': id, 'depth': stmt.depth + 1, 'importedModules': len(node.names), 'asnames': asnames}

    
    def visit_ImportFrom(self, node: ast.ImportFrom, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        stmt = db_entities.DBStatement()
        ############ IDS #########################
        id = self.id_manager.get_id()
        stmt.statement_id = db_node.node_id = id
        db_node.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        stmt.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        stmt.parent = params["parent"].category
        ############# ROLES ######################
        stmt.statementRole = params["role"]
        ########## ENTITY PROPERTIES ############
        stmt.height = params["depth"]
        stmt.hasOrElse = None
        stmt.depth = 0
        stmt.sourceCode = ast.unparse(node)
        stmt.bodySize = None
        stmt.expertise_level = params['expertise_level']
        stmt.user_id = params['user_id']
        asnames = 0
        for alias in node.names:
            if(alias.asname): asnames += 1
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': stmt, 'db_node': db_node})
        return {'id': id, 'depth': stmt.depth + 1, 'importedModules': len(node.names), 'asnames': asnames}

    ############################ EXPRESSIONS ##################################

    def visit_BoolOp(self, node: ast.BoolOp, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Logical"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["Logical"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        self.visit(node.op, child_params)
        for child in node.values:
            returns.append(self.visit(child, self.add_param(child_params, 'role', exprRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            index += 1
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_NamedExpr(self, node: ast.NamedExpr, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES #######################
        expr.category = "AssignmentExp"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["AssignExpLHS", "AssignExpRHS"]
        ############## PROPAGAR VISIT ############
        target = self.visit(node.target, self.add_param(child_params, 'role', exprRoles[0]))
        value = self.visit(node.value, self.add_param(child_params, 'role', exprRoles[1]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = target["category"]
        expr.second_child_category = value["category"]
        expr.first_child_id = target["id"]
        expr.second_child_id = value["id"]
        expr.depth = max(target["depth"], value["depth"])
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_BinOp(self, node: ast.BinOp, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = op_category(node)
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["Arithmetic", "Shift", "Pow", "MatMult", "BWLogical"]
        ############## PROPAGAR VISIT ############
        self.visit(node.op, child_params)
        match node.op:
            case ast.MatMult: role = exprRoles[3]
            case ast.LShift, ast.RShift: role = exprRoles[1]
            case ast.Pow: role = exprRoles[2]
            case ast.BitAnd, ast.BitOr, ast.BitXor: role = exprRoles[4]
            case default: role = exprRoles[0]
        left = self.visit(node.left, self.add_param(child_params, 'role', role))
        right = self.visit(node.right, self.add_param(child_params, 'role', role))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = left["category"]
        expr.second_child_category = right["category"]
        expr.first_child_id = left["id"]
        expr.second_child_id = right["id"]
        expr.depth = max(left["depth"], right["depth"])
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}
    
    
    def visit_UnaryOp(self, node: ast.UnaryOp, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = op_category(node)
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["Arithmetic"]
        ############## PROPAGAR VISIT ############
        self.visit(node.op, child_params)
        operand = self.visit(node.operand, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = operand["category"]
        expr.first_child_id = operand["id"]
        expr.depth = operand["depth"]
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}
    
    
    def visit_Lambda(self, node: ast.Lambda, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["LambdaBody"]
        ############## PROPAGAR VISIT ############
        args = self.visit(node.args, self.add_param(self.add_param(child_params, "params_id", id), "role", "LambdaParams"))
        aux = self.visit(node.body, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = aux["category"]
        expr.first_child_id = aux["id"]
        expr.depth = aux["depth"]
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}
    
    
    def visit_IfExp(self, node: ast.IfExp, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Ternary"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############ PARAMS ######################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["TernaryCondition", "TernaryIfBody", "TernaryElseBody"]
        ############## PROPAGAR VISIT ############
        test = self.visit(node.test, self.add_param(child_params, 'role', exprRoles[0]))
        body = self.visit(node.body, self.add_param(child_params, 'role', exprRoles[1]))
        orelse = self.visit(node.orelse, self.add_param(child_params, 'role', exprRoles[2]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = test["category"]
        expr.second_child_category = body["category"]
        expr.third_child_category = orelse["category"]
        expr.first_child_id = test["id"]
        expr.second_child_id = body["id"]
        expr.third_child_id = orelse["id"]
        expr.depth = max(body["depth"],orelse["depth"],test["depth"])
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    ######################### COMPREHENSIONS #############################

    
    def visit_ListComp(self, node: ast.ListComp, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        comp = db_entities.DBComprehension()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = comp.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = comp.category = "ListComprehension"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["ComprenhensionElement"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        numOfIfs = 0
        isAsync = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.generators:
            returns.append(self.visit(child, child_params))
            if(index == 0): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 1): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 2): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            numOfIfs += len(child.ifs)
            if(child.is_async): isAsync = True
            index += 1
        elt = self.visit(node.elt, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = elt["category"]
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = elt["id"]
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(elt["depth"], depth)
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #--------------- COMP --------------------
        comp.numberOfIfs = numOfIfs
        comp.numberOfGenerators = len(node.generators)
        comp.isAsync = isAsync
        comp.expertise_level = params['expertise_level']
        comp.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': comp, 'db_node': db_node, 'expr': expr})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_SetComp(self, node: ast.SetComp, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        comp = db_entities.DBComprehension()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = comp.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = comp.category = "SetComprehension"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["ComprenhensionElement"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        numOfIfs = 0
        isAsync = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.generators:
            returns.append(self.visit(child, child_params))
            if(index == 0): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 1): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 2): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            numOfIfs += len(child.ifs)
            if(child.is_async): isAsync = True
            index += 1
        elt = self.visit(node.elt, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = elt["category"]
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = elt["id"]
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(elt["depth"], depth)
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #--------------- COMP --------------------
        comp.numberOfIfs = numOfIfs
        comp.numberOfGenerators = len(node.generators)
        comp.isAsync = isAsync
        comp.expertise_level = params['expertise_level']
        comp.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': comp, 'db_node': db_node, 'expr': expr})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_DictComp(self, node: ast.DictComp, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        comp = db_entities.DBComprehension()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = comp.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = comp.category = "DictComprehension"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["DictionaryLiteralKey", "DictionaryLiteralValue"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        third_child_category = None
        fourth_child_category = None
        third_child_id = None
        fourth_child_id = None
        numOfIfs = 0
        isAsync = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.generators:
            returns.append(self.visit(child, child_params))
            if(index == 0): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 1): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            numOfIfs += len(child.ifs)
            if(child.is_async): isAsync = True
            index += 1
        key = self.visit(node.key, self.add_param(child_params, 'role', exprRoles[0]))
        value = self.visit(node.value, self.add_param(child_params, 'role', exprRoles[1]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = key["category"]
        expr.second_child_category = value["category"]
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = key["id"]
        expr.second_child_id = value["id"]
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(key["depth"], value["depth"], depth)
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #--------------- COMP --------------------
        comp.numberOfIfs = numOfIfs
        comp.numberOfGenerators = len(node.generators)
        comp.isAsync = isAsync
        comp.expertise_level = params['expertise_level']
        comp.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': comp, 'db_node': db_node, 'expr': expr})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_GeneratorExp(self, node: ast.GeneratorExp, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        comp = db_entities.DBComprehension()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = comp.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = comp.category = "GeneratorComprehension"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["ComprenhensionElement"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        numOfIfs = 0
        isAsync = False
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.generators:
            returns.append(self.visit(child, child_params))
            if(index == 0): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 1): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 2): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            numOfIfs += len(child.ifs)
            if(child.is_async): isAsync = True
            index += 1
        elt = self.visit(node.elt, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = elt["category"]
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = elt["id"]
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(elt["depth"], depth)
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #--------------- COMP --------------------
        comp.numberOfIfs = numOfIfs
        comp.numberOfGenerators = len(node.generators)
        comp.isAsync = isAsync
        comp.expertise_level = params['expertise_level']
        comp.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': comp, 'db_node': db_node, 'expr': expr})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    ######################################################################

    
    def visit_Await(self, node: ast.Await, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["Await"]
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.first_child_id = value["id"]
        expr.depth = value["depth"]
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_Yield(self, node: ast.Yield, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["Yield"]
        ########## ENTITY PROPERTIES ############
        value = None
        ############## PROPAGAR VISIT ############
        if(node.value): value = self.visit(node.value, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.depth = 0
        if(value):
            expr.first_child_category = value["category"]
            expr.first_child_id = value["id"]
            expr.depth = value["depth"]
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_YieldFrom(self, node: ast.YieldFrom, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["YieldFrom"]
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.first_child_id = value["id"]
        expr.depth = value["depth"]
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_Compare(self, node: ast.Compare, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["Compare", "Relational", "Is", "In"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        left = self.visit(node.left, self.add_param(child_params, 'role', exprRoles[0]))
        index = 0
        returns = []
        for child in node.comparators:
            match node.ops[index]:
                case ast.Is, ast.IsNot: returns.append(self.visit(child, self.add_param(child_params, 'role', exprRoles[2])))
                case ast.In: returns.append(self.visit(child, self.add_param(child_params, 'role', exprRoles[3])))
                case default: returns.append(self.visit(child, self.add_param(child_params, 'role', exprRoles[1])))
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            index += 1
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(left["depth"], depth)
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    ########################## call_args ###########################

    
    def visit_Call(self, node: ast.Call, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        callArgs = db_entities.DBCallArg()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = callArgs.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["CallFuncName", "CallArg"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        namedArgs = 0
        staredArgs = 0
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.args:
            returns.append(self.visit(child, self.add_param(child_params, 'role', exprRoles[1])))
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            depth = max(depth, returns[index]["depth"])
            index += 1
        func = self.visit(node.func, self.add_param(child_params, 'role', exprRoles[0]))
        for child in node.keywords:
            returns.append(self.visit(child, self.add_param(child_params, 'role', exprRoles[1])))
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            if(child.arg): namedArgs += 1
            if('**' in ast.unparse(child.value)): staredArgs += 1
            depth = max(depth, returns[index]["depth"])
            index += 1
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = max(func["depth"], depth)
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #------------- CallArgs ------------------
        callArgs.numberArgs = index
        callArgs.namedArgsPct = namedArgs/callArgs.numberArgs if callArgs.numberArgs > 0 else 0
        callArgs.doubleStarArgsPct = staredArgs/callArgs.numberArgs if callArgs.numberArgs > 0 else 0
        callArgs.expertise_level = params['expertise_level']
        callArgs.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': callArgs, 'db_node': db_node, 'expr': expr})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    ################################################################

    def visit_FormattedValue(self, node: ast.FormattedValue, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["FormattedValue", "FormattedFormat"]
        ########## ENTITY PROPERTIES ############
        spec = None
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.add_param(child_params, 'role', exprRoles[0]))
        if(node.format_spec): spec = self.visit(node.format_spec, self.add_param(child_params, 'role', exprRoles[1]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.first_child_id = value["id"]
        expr.depth = value["depth"]
        if(spec):
            expr.second_child_category = spec["category"]
            expr.second_child_id = spec["id"]
            expr.depth = max(spec["depth"], expr.depth)
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    ########################### F-strings #####################################

    
    def visit_JoinedStr(self, node: ast.JoinedStr, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        fstr = db_entities.DBFString()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = fstr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "FString"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["FString"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        numFVal = 0
        numConst = 0
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.values:
            returns.append(self.visit(child, self.add_param(child_params, 'role', exprRoles[0])))
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            if(isinstance(child,ast.Constant)): numConst += 1
            if(isinstance(child,ast.FormattedValue)): numFVal += 1
            depth = max(depth, returns[index]["depth"])
            index += 1
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #-----------------------------------------
        fstr.numberOfElements = numConst + numFVal
        fstr.constantsPct = numConst / len(node.values) if len(node.values) > 0 else 0
        fstr.expressionsPct = numFVal / len(node.values) if len(node.values) > 0 else 0
        fstr.expertise_level = params['expertise_level']
        fstr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': fstr, 'db_node': db_node, 'expr': expr})
        return  {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    ###########################################################################

    
    def visit_constant(self, node: ast.Constant, params: Dict) -> Dict: 
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = const_category(node)
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.depth = 0
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return  {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_Attribute(self, node: ast.Attribute, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Dot"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["Dot"]
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.first_child_id = value["id"]
        expr.depth = value["depth"]
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_Subscript(self, node: ast.Subscript, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Indexing"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["Slice", "Indexing"]
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.add_param(child_params, 'role', exprRoles[1]))
        slice = self.visit(node.slice, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.second_child_category = slice["category"]
        expr.first_child_id = value["id"]
        expr.second_child_id = slice["id"]
        expr.depth = max(slice["depth"],value["depth"])
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_Starred(self, node: ast.Starred, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Star"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["Star"]
        ############## PROPAGAR VISIT ############
        value = self.visit(node.value, self.add_param(child_params, 'role', exprRoles[0]))
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = value["category"]
        expr.first_child_id = value["id"]
        expr.depth = value["depth"]
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': expr, 'db_node': db_node})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    ############################# Variable ##################################

    
    def visit_Name(self, node: ast.Name, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        var = db_entities.DBVariable()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = var.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = "Variable"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.depth = 0
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #------------- VARIABLE ------------------
        var.numberOfCharacters = len(node.id)
        var.nameConvention = self.name_convention(node.id)
        var.isPrivate = False
        var.isMagic = False
        if(node.id.startswith('_')):
            if(node.id.endswith('_')):
                var.isMagic = True
            else:
                var.isPrivate = True
        var.expertise_level = params['expertise_level']
        var.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': var, 'db_node': db_node, 'expr': expr})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    ############################### Vectors #################################

    
    def visit_List(self, node: ast.List, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        vct = db_entities.DBVector()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = vct.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = vct.category = "ListLiteral"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["ListLiteral"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        homogeneous = True
        lastType = None
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.elts:
            returns.append(self.visit(child, self.add_param(child_params, 'role', exprRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            if(index > 0 and homogeneous and type(child) != lastType): homogeneous = False
            lastType = type(child)
            index += 1
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #-------------- VECTOR -------------------
        vct.numberOfElements = len(node.elts)
        vct.homogeneous = homogeneous
        vct.expertise_level = params['expertise_level']
        vct.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': vct, 'db_node': db_node, 'expr': expr})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_Tuple(self, node: ast.Tuple, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        vct = db_entities.DBVector()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = vct.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = vct.category = "TupleLiteral"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["TupleLiteral"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        homogeneous = True
        lastType = None
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.elts:
            returns.append(self.visit(child, self.add_param(child_params, 'role', exprRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            if(index > 0 and homogeneous and type(child) != lastType): homogeneous = False
            lastType = type(child)
            index += 1
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #-------------- VECTOR -------------------
        vct.numberOfElements = len(node.elts)
        vct.homogeneous = homogeneous
        vct.expertise_level = params['expertise_level']
        vct.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': vct, 'db_node': db_node, 'expr': expr})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_Dict(self, node: ast.Dict, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        vct = db_entities.DBVector()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = vct.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = vct.category = "DictionaryLiteral"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["DictionaryLiteralKey", "DictionaryLiteralValue"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        homogeneous = True
        lastType = None
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        keys = []
        values = []
        index = 0
        for i in range(len(node.keys)):
            keys.append(self.visit(node.keys[i], self.add_param(child_params, 'role', exprRoles[0])))
            values.append(self.visit(node.values[i], self.add_param(child_params, 'role', exprRoles[1])))
            depth = max(depth, keys[index]["depth"] if keys[index] else 0, values[index]['depth'])
            if(index == 0): 
                first_child_category = keys[index]["category"] if keys[index] else 'NoneType'; first_child_id = keys[index]["id"] if keys[index] else None
                second_child_category = values[index]["category"]; second_child_id = values[index]["id"]
            if(index == 1): 
                third_child_category = keys[index]["category"] if keys[index] else 'NoneType'; third_child_id = keys[index]["id"] if keys[index] else None
                fourth_child_category = values[index]["category"]; fourth_child_id = values[index]["id"]
            if(index > 0 and homogeneous and type(node.values[i]) != lastType): homogeneous = False
            lastType = type(node.values[i])
            index += 1
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #-------------- VECTOR -------------------
        vct.numberOfElements = len(node.keys)
        vct.homogeneous = homogeneous
        vct.expertise_level = params['expertise_level']
        vct.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': vct, 'db_node': db_node, 'expr': expr})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    
    def visit_Set(self, node: ast.Set, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        expr = db_entities.DBExpression()
        vct = db_entities.DBVector()
        ############ IDS #########################
        id = self.id_manager.get_id()
        db_node.node_id = expr.expression_id = vct.expression_id = id
        db_node.parent_id = expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        expr.category = vct.category = "SetLiteral"
        db_node.parent_table = params["parent"].table
        expr.parent = params["parent"].category
        ############# ROLES ######################
        expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": expr, "depth": params["depth"] + 1, "parent_id": id}
        exprRoles = ["SetLiteral"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        homogeneous = True
        lastType = None
        first_child_category = None
        second_child_category = None
        third_child_category = None
        fourth_child_category = None
        first_child_id = None
        second_child_id = None
        third_child_id = None
        fourth_child_id = None
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        for child in node.elts:
            returns.append(self.visit(child, self.add_param(child_params, 'role', exprRoles[0])))
            depth = max(depth, returns[index]["depth"])
            if(index == 0): first_child_category = returns[index]["category"]; first_child_id = returns[index]["id"]
            if(index == 1): second_child_category = returns[index]["category"]; second_child_id = returns[index]["id"]
            if(index == 2): third_child_category = returns[index]["category"]; third_child_id = returns[index]["id"]
            if(index == 3): fourth_child_category = returns[index]["category"]; fourth_child_id = returns[index]["id"]
            if(index > 0 and homogeneous and type(child) != lastType): homogeneous = False
            lastType = type(child)
            index += 1
        ########## ENTITY PROPERTIES ############
        expr.sourceCode = ast.unparse(node)
        expr.height = params["depth"]
        expr.first_child_category = first_child_category
        expr.second_child_category = second_child_category
        expr.third_child_category = third_child_category
        expr.fourth_child_category = fourth_child_category
        expr.first_child_id = first_child_id
        expr.second_child_id = second_child_id
        expr.third_child_id = third_child_id
        expr.fourth_child_id = fourth_child_id
        expr.depth = depth
        expr.expertise_level = params['expertise_level']
        expr.user_id = params['user_id']
        #-------------- VECTOR -------------------
        vct.numberOfElements = len(node.elts)
        vct.homogeneous = homogeneous
        vct.expertise_level = params['expertise_level']
        vct.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': vct, 'db_node': db_node, 'expr': expr})
        return {'id': id, 'depth': expr.depth + 1, 'category': expr.category}

    def visit_Slice(self, node: ast.Slice, params: Dict) -> Dict:  
        db_node = db_entities.db_node()
        db_expr = db_entities.DBExpression()
        ############ IDS #########################
        node_id = self.id_manager.get_id()
        db_node.node_id = db_expr.expression_id = node_id
        db_node.parent_id = db_expr.parent_id = params["parent_id"]
        ############ CATEGORIES ##################
        db_expr.category = node.__doc__.split('(')[0]
        db_node.parent_table = params["parent"].table
        db_expr.parent = params["parent"].category
        ############# ROLES ######################
        db_expr.expressionRole = params["role"]
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": db_expr, "depth": params["depth"] + 1, "parent_id": node_id}
        expr_roles = ["Slice"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        step = None
        lower = None
        upper = None
        ############## PROPAGAR VISIT ############
        if node.lower:
            lower = self.visit(node.lower, self.add_param(child_params, 'role', expr_roles[0]))
            depth = max(depth, lower["depth"])
        if node.upper:
            upper = self.visit(node.upper, self.add_param(child_params, 'role', expr_roles[0]))
            depth = max(depth, upper["depth"])
        if node.step:
            step = self.visit(node.step, self.add_param(child_params, 'role', expr_roles[0]))
            depth = max(depth, step["depth"])
        ########## ENTITY PROPERTIES ############
        db_expr.sourceCode = ast.unparse(node)
        db_expr.height = params["depth"]
        if lower:
            db_expr.first_child_category = lower["category"]
            db_expr.first_child_id = lower["id"]
            if upper:
                db_expr.second_child_category = upper["category"]
                db_expr.second_child_id = upper["id"]
                if step:
                    db_expr.third_child_category = step["category"]
                    db_expr.third_child_id = step["id"]
            else:
                if step:
                    db_expr.second_child_category = step["category"]
                    db_expr.second_child_id = step["id"]
        else:
            if upper:
                db_expr.first_child_category = upper["category"]
                db_expr.first_child_id = upper["id"]
                if step:
                    db_expr.second_child_category = step["category"]
                    db_expr.second_child_id = step["id"]
            else:
                if step:
                    db_expr.first_child_category = step["category"]
                    db_expr.first_child_id = step["id"]
        db_expr.depth = depth
        db_expr.expertise_level = params['expertise_level']
        db_expr.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {'node': db_expr, 'db_node': db_node})
        return {'id': node_id, 'depth': db_expr.depth + 1, 'category': db_expr.category}

    ############################### Cases ###################################
    def visit_MatchValue(self, node: ast.MatchValue, params: Dict) -> Dict:  
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": params["parent"], "depth": params["depth"] + 1, "parent_id": params["parent_id"]}
        expr_roles = ["MatchCondition"]
        ################ RETURNS #################
        depth = 0
        ############## PROPAGAR VISIT ############
        aux = self.visit(node.value, self.add_param(child_params, 'role', expr_roles[0]))
        depth = max(aux["depth"], depth)
        return {'matchValue': 1, 'matchSingleton': 0, 'matchSequence': 0, 'matchMapping': 0, 'matchClass': 0, 'matchStar': 0, 'matchAs': 0, 'matchOr': 0, 'depth': depth + 1}
    
    def visit_MatchSingleton(self, node: ast.MatchSingleton, params: Dict) -> Dict:  
        return {'matchValue': 0, 'matchSingleton': 1, 'matchSequence': 0, 'matchMapping': 0, 'matchClass': 0, 'matchStar': 0, 'matchAs': 0, 'matchOr': 0, 'depth': 1}

    def visit_MatchSequence(self, node: ast.MatchSequence, params: Dict) -> Dict:  
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": params["parent"], "depth": params["depth"] + 1, "parent_id": params["parent_id"]}
        ################ RETURNS #################
        returns = {'matchValue': 0, 'matchSingleton': 0, 'matchSequence': 1, 'matchMapping': 0, 'matchClass': 0, 'matchStar': 0, 'matchAs': 0, 'matchOr': 0, 'depth': 0}
        ############## PROPAGAR VISIT ############
        childs = []
        index = 0
        for child in node.patterns:
            childs.append(self.visit(child, child_params))
            returns = self.sum_match(returns, childs[index])
            index += 1
        returns["depth"] += 1
        return returns
    
    def visit_MatchMapping(self, node: ast.MatchMapping, params: Dict) -> Dict:  
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": params["parent"], "depth": params["depth"] + 1, "parent_id": params["parent_id"]}
        expr_roles = ["MatchCondition"]
        ################ RETURNS #################
        returns = {'matchValue': 0, 'matchSingleton': 0, 'matchSequence': 0, 'matchMapping': 1, 'matchClass': 0, 'matchStar': 0, 'matchAs': 0, 'matchOr': 0, 'depth': 0}
        ############## PROPAGAR VISIT ############
        childs = []
        exprs = []
        index = 0
        for child in node.patterns:
            childs.append(self.visit(child, child_params))
            returns = self.sum_match(returns, childs[index])
            index += 1
        index = 0
        for child in node.keys:
            exprs.append(self.visit(child, self.add_param(child_params, 'role', expr_roles[0])))
            returns["depth"] = max(returns["depth"], exprs[index]["depth"])
            index += 1
        returns["depth"] += 1
        return returns
    
    def visit_MatchClass(self, node: ast.MatchClass, params: Dict) -> Dict:  
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": params["parent"], "depth": params["depth"] + 1, "parent_id": params["parent_id"]}
        expr_roles = ["MatchCondition"]
        ################ RETURNS #################
        returns = {'matchValue': 0, 'matchSingleton': 0, 'matchSequence': 0, 'matchMapping': 0, 'matchClass': 1, 'matchStar': 0, 'matchAs': 0, 'matchOr': 0, 'depth': 0}
        ############## PROPAGAR VISIT ############
        cls = self.visit(node.cls, self.add_param(child_params, 'role', expr_roles[0]))
        childs = []
        index = 0
        for child in node.patterns:
            childs.append(self.visit(child, child_params))
            returns = self.sum_match(returns, childs[index])
            index += 1
        for child in node.kwd_patterns:
            childs.append(self.visit(child, child_params))
            returns = self.sum_match(returns, childs[index])
            index += 1
        returns["depth"] = max(returns["depth"], cls["depth"])
        returns["depth"] += 1
        return returns

    def visit_MatchStar(self, node: ast.MatchStar, params: Dict) -> Dict:  
        return {'matchValue': 0, 'matchSingleton': 0, 'matchSequence': 0, 'matchMapping': 0, 'matchClass': 0, 'matchStar': 1, 'matchAs': 0, 'matchOr': 0, 'depth': 1}
    
    def visit_MatchAs(self, node: ast.MatchAs, params: Dict) -> Dict:  
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": params["parent"], "depth": params["depth"] + 1, "parent_id": params["parent_id"]}
        ################ RETURNS #################
        returns = {'matchValue': 0, 'matchSingleton': 0, 'matchSequence': 0, 'matchMapping': 0, 'matchClass': 0, 'matchStar': 0, 'matchAs': 1, 'matchOr': 0, 'depth': 0}
        ############## PROPAGAR VISIT ############
        if(node.pattern): 
            child = self.visit(node.pattern, child_params)
            returns["depth"] = max(returns["depth"], child["depth"])
        returns["depth"] += 1
        return returns
    
    def visit_MatchOr(self, node: ast.MatchOr, params: Dict) -> Dict:  
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": params["parent"], "depth": params["depth"] + 1, "parent_id": params["parent_id"]}
        ################ RETURNS #################
        returns = {'matchValue': 0, 'matchSingleton': 0, 'matchSequence': 0, 'matchMapping': 0, 'matchClass': 0, 'matchStar': 0, 'matchAs': 0, 'matchOr': 1, 'depth': 0}
        ############## PROPAGAR VISIT ############
        childs = []
        index = 0
        for child in node.patterns:
            childs.append(self.visit(child, child_params))
            returns = self.sum_match(returns, childs[index])
            index += 1
        returns["depth"] += 1
        return returns
    
    ############################# HANDLER ####################################
    def visit_ExceptHandler(self, node: ast.ExceptHandler, params: Dict) -> Dict:  
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": params["handler"], "depth": params["depth"] + 1, "parent_id": params["parent_id"]}
        expr_roles = ["ExceptType", "ExceptBody"]
        ############## PROPAGAR VISIT ############
        returns = []
        child_ids = []
        index = 0
        depth = 0
        is_catch_all = True
        if node.type:
            self.visit(node.type, self.add_param(child_params, 'role', expr_roles[0]))
            is_catch_all = False
        for child in node.body:
            returns.append(self.visit(child, self.add_param(child_params, 'role', expr_roles[1])))
            child_ids.append(returns[index]['id'])
            depth = max(depth,returns[index]["depth"])
            index += 1
        return {'id': params["parent_id"], 'depth': depth, 'isCatchAll': is_catch_all, 'child_ids': child_ids}

    ####################### Extra Visits ######################
    def visit_comprehension(self, node: ast.comprehension, params: Dict) -> Dict:  
        ############# PARAMS #####################
        expr_roles = ["ComprehensionTarget", "ComprehensionIter", "ComprehensionIf"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        ############## PROPAGAR VISIT ############
        returns = []
        index = 0
        target = self.visit(node.target, self.add_param(params, 'role', expr_roles[0]))
        iter = self.visit(node.iter, self.add_param(params, 'role', expr_roles[1]))
        for child in node.ifs:
            returns.append(self.visit(child, self.add_param(params, 'role', expr_roles[2])))
            depth = max(depth, returns[index]["depth"])
            index += 1
        ########## ENTITY PROPERTIES ############
        depth = max(max(target["depth"], iter["depth"]), depth)
        return {'id': params["parent_id"], 'category': params["parent"].category, 'depth': depth + 1}
    
    def visit_arguments(self, node: ast.arguments, params: Dict) -> Dict:  
        db_params = db_entities.DBParameter()
        ############### IDS ######################
        db_params.parameters_id = params["params_id"]
        db_params.parent_id = params["parent_id"]
        ############## ROLES #####################
        db_params.parametersRole = params["role"]
        ############# PARAMS #####################
        expr_roles = ["DefaultParamValue"]
        ########## ENTITY PROPERTIES ############
        number_of_annotations = 0
        number_of_params = 0
        naming_conventions = {'CamelUp': 0, 'CamelLow': 0, 'SnakeCase': 0, 'Discard': 0, 'Upper': 0, 'Lower': 0, 'NoNameConvention': 0}
        ############## PROPAGAR VISIT ############
        for child in node.posonlyargs:
            arg = self.visit(child, params)
            if arg["typeAnnotation"]:
                number_of_annotations += 1
            number_of_params += 1
            naming_conventions[self.name_convention(child.arg)] += 1
        for child in node.args:
            arg = self.visit(child, params)
            if arg["typeAnnotation"]:
                number_of_annotations += 1
            number_of_params += 1
            naming_conventions[self.name_convention(child.arg)] += 1
        if node.vararg:
            arg =  self.visit(node.vararg, params)
            if(arg["typeAnnotation"]): number_of_annotations += 1
            number_of_params += 1
            naming_conventions[self.name_convention(node.vararg.arg)] += 1
        for child in node.kwonlyargs:
            arg =  self.visit(child, params)
            if(arg["typeAnnotation"]): number_of_annotations += 1
            number_of_params += 1
            naming_conventions[self.name_convention(child.arg)] += 1
        for child in node.kw_defaults:
            self.visit(child, self.add_param(params, 'role', expr_roles[0]))
        if node.kwarg:
            arg = self.visit(node.kwarg, params)
            if(arg["typeAnnotation"]): number_of_annotations += 1
            number_of_params += 1
            naming_conventions[self.name_convention(node.kwarg.arg)] += 1
        for child in node.defaults:
            self.visit(child, self.add_param(params, 'role', expr_roles[0]))
        ########## ENTITY PROPERTIES ############
        db_params.nameConvention = self.get_args_name_convention(naming_conventions)
        db_params.numberOfParams = number_of_params
        db_params.posOnlyParamPct = len(node.posonlyargs)/number_of_params if number_of_params > 0 else 0
        db_params.varParamPct = (1 if node.vararg else 0)/number_of_params if number_of_params > 0 else 0
        db_params.hasVarParam = True if node.vararg else False
        db_params.typeAnnotationPct = number_of_annotations/number_of_params if number_of_params > 0 else 0
        db_params.kwOnlyParamPct = len(node.kwonlyargs)/number_of_params if number_of_params > 0 else 0
        db_params.defaultValuePct = (len(node.kw_defaults) + len(node.defaults))/number_of_params if number_of_params > 0 else 0
        db_params.hasKWParam = True if node.kwarg else False
        db_params.expertise_level = params['expertise_level']
        db_params.user_id = params['user_id']
        ############## VISITOR DB ################
        self.visitor_db.visit(node, {"dbparams": db_params})
        return {"typeAnnotations": number_of_annotations, "numberOfArgs": number_of_params}
    
    def visit_arg(self, node: ast.arg, params: Dict) -> Dict: 
        ############# PARAMS ##################### 
        expr_roles = ["TypeAnnotation"]
        ############## PROPAGAR VISIT ############
        if node.annotation:
            self.visit(node.annotation, self.add_param(params, 'role', expr_roles[0]))
            return {'typeAnnotation': True}
        return {'typeAnnotation': False}
    
    def visit_keyword(self, node: ast.keyword, params: Dict) -> Dict:  
        ############## PROPAGAR VISIT ############
        return self.visit(node.value, params)
    
    def visit_withitem(self, node: ast.withitem, params: Dict) -> Dict:  
        ############# PARAMS #####################
        child_params = {'expertise_level': params["expertise_level"], 'user_id': params['user_id'], "parent": params["parent"], "depth": params["depth"], "parent_id": params["parent_id"]}
        ############## PROPAGAR VISIT ############
        self.visit(node.context_expr, self.add_param(child_params, 'role', params["role_ctx"]))
        if node.optional_vars:
            self.visit(node.optional_vars, self.add_param(child_params, 'role', params["role_vars"]))
        return
    
    def visit_match_case(self, node: ast.match_case, params: Dict) -> Dict:  
        ############# PARAMS #####################
        stmt_roles = ["Case"]
        expr_roles = ["CaseGuard", "CaseBody"]
        ########## ENTITY PROPERTIES ############
        depth = 0
        ############## PROPAGAR VISIT ############
        childs = []
        ids = []
        index = 0
        returns = self.visit(node.pattern, params)
        guards = 0
        if node.guard:
            guard = self.visit(node.guard, self.add_param(params, 'role', expr_roles[0]))
            guards = 1
        for child in node.body:
            if isinstance(child, ast.Expr):
                childs.append(self.visit(child, self.add_param(params, "role", expr_roles[1])))
            else:
                childs.append(self.visit(child, self.add_param(params, "role", stmt_roles[0])))
            depth = max(depth, childs[index]["depth"])
            ids.append(childs[index]["id"])
            index += 1
        ########## ENTITY PROPERTIES ############
        returns = self.add_param(returns, 'guards', guards)
        returns = self.add_param(returns, 'bodyCount', index)
        returns["depth"] = max(returns["depth"], depth)
        returns["ids"] = ids
        return returns
    
    def visit_TypeVar(self, node: ast.TypeVar, params: Dict) -> Dict:  
        ############# PARAMS #####################
        expr_roles = ["TypeVar"]
        ############## PROPAGAR VISIT ############
        if node.bound:
            self.visit(node.bound, self.add_param(params, 'role', expr_roles[0]))
        return
    
    def visit_ParamSpec(self, node: ast.ParamSpec, params: Dict) -> Dict:  
        return
    
    def visit_TypeVarTuple(self, node: ast.TypeVarTuple, params: Dict) -> Dict:  
        return
