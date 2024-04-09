class DBNode:
    def __init__(self, parent_table=None, parent_id=None, node=None, user_id=None, expertise_level=None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Nodes"
        self.parent_table = parent_table
        self.parent_id = parent_id
        self.node_id = 0


class DBProgram:
    def __init__(self, category=None, name: str = None,  has_sub_dirs_with_code: bool = None,  has_packages: bool = None, number_of_modules: int = None,
                 number_of_sub_dirs_with_code: int = None,  number_of_packages: int = None,  class_defs_pct: int = None, function_defs_pct: int = None,
                 enum_defs_pct: int = None, has_code_root_package: bool = None, average_defs_per_module: int = None, node=None, user_id=None, expertise_level=None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Programs"
        self.name = name
        self.has_sub_dirs_with_code = has_sub_dirs_with_code
        self.has_packages = has_packages
        self.number_of_modules = number_of_modules
        self.number_of_sub_dirs_with_code = number_of_sub_dirs_with_code
        self.number_of_packages = number_of_packages
        self.class_defs_pct = class_defs_pct
        self.function_defs_pct = function_defs_pct
        self.enum_defs_pct = enum_defs_pct
        self.has_code_root_package = has_code_root_package
        self.average_defs_per_module = average_defs_per_module
        self.program_id = 0


class DBModule:
    def __init__(self, category=None, module_id=None, name: str = None, name_convention: str = None, has_doc_string: bool = None,
                 global_stmt_pct: float = None, global_expressions: float = None, number_of_classes: int = None,
                 number_of_functions: int = None, class_defs_pct: float = None, function_defs_pct: float = None,
                 enum_defs_pct: float = None, average_stmts_function_body: float = None,
                 average_stmts_method_body: float = None, type_annotations_pct: float = None,
                 has_entry_point: bool = None, path: str = None, program_id=None, import_id=None, node=None, user_id=None, expertise_level=None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Modules"
        self.category = "Module"
        self.module_id = module_id
        self.name = name
        self.name_convention = name_convention
        self.has_doc_string = has_doc_string
        self.global_stmts_pct = global_stmt_pct
        self.global_expressions = global_expressions
        self.number_of_classes = number_of_classes
        self.number_of_functions = number_of_functions
        self.class_defs_pct = class_defs_pct
        self.function_defs_pct = function_defs_pct
        self.enum_defs_pct = enum_defs_pct
        self.average_stmts_function_body = average_stmts_function_body
        self.average_stmts_method_body = average_stmts_method_body
        self.type_annotations_pct = type_annotations_pct
        self.has_entry_point = has_entry_point
        self.path = path
        self.program_id = program_id
        self.import_id = import_id


class DBImport:
    def __init__(self, number_imports: int = None,  module_imports_pct: float = None, 
                 average_imported_modules: float = None,  from_imports_pct: float = None, average_from_imported_modules: float = None,
                 average_as_in_imported_modules: float = None,  local_imports_pct: float = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.category = "Import"
        self.table = "Imports"
        self.number_imports = number_imports
        self.module_imports_pct = module_imports_pct
        self.average_imported_modules = average_imported_modules
        self.average_from_imported_modules = average_from_imported_modules
        self.from_imports_pct = from_imports_pct
        self.average_as_in_imported_modules = average_as_in_imported_modules
        self.local_imports_pct = local_imports_pct
        self.import_id = 0


class DBClassDef:
    def __init__(self, category = None, classdef_id=None, name_convention: str = None,  is_enum_class: bool = None,
                 number_of_characters: int = None, number_of_methods: int = None, number_of_decorators: int = None, 
                 number_of_base_classes: int = None, has_generic_type_annotations: bool = None,
                 has_doc_string: bool = None, body_count: int = None,  assignments_pct: float = None,
                 expressions_pct: float = None, uses_meta_class: bool = None,
                 number_of_keywords: int = None, height: int = None,
                 average_stmts_method_body: float = None, type_annotations_pct: float = None,
                 private_methods_pct: float = None, magic_methods_pct: float = None,
                 async_methods_pct: float = None, class_methods_pct: float = None,
                 static_methods_pct: float = None, abstract_methods_pct: float = None,
                 property_methods_pct: float = None, source_code: str = None, module_id=None, parent_id=None, node=None, user_id=None, expertise_level=None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "ClassDefs"
        self.category = "ClassDef"
        self.classdef_id = classdef_id
        self.name_convention = name_convention
        self.is_enum_class = is_enum_class
        self.number_of_characters = number_of_characters
        self.number_of_decorators = number_of_decorators
        self.number_of_methods = number_of_methods
        self.number_of_base_classes = number_of_base_classes
        self.has_generic_type_annotations = has_generic_type_annotations
        self.has_doc_string = has_doc_string
        self.body_count = body_count
        self.assignments_pct = assignments_pct
        self.expressions_pct = expressions_pct
        self.uses_meta_class = uses_meta_class
        self.number_of_keywords = number_of_keywords
        self.height = height
        self.average_stmts_method_body = average_stmts_method_body
        self.type_annotations_pct = type_annotations_pct
        self.private_methods_pct = private_methods_pct
        self.magic_methods_pct = magic_methods_pct
        self.async_methods_pct = async_methods_pct
        self.class_methods_pct = class_methods_pct
        self.static_methods_pct = static_methods_pct
        self.abstract_methods_pct = abstract_methods_pct
        self.property_methods_pct = property_methods_pct
        self.source_code = source_code
        self.module_id = module_id
        self.parent_id = parent_id


class DBFunctionDef:
    def __init__(self, category = None, functiondef_id = None,  name_convention: str = None, 
                 number_of_characters: int = None,  is_private: bool = None,  is_magic: bool = None, 
                 body_count: int = None,  expressions_pct: float = None, 
                 is_async: bool = None,  number_of_decorators: int = None, 
                 has_return_type_annotation: bool = None,  has_doc_string: bool = None, 
                 height: int = None,  type_annotations_pct: float = None, 
                 source_code: str = None,  module_id = None, parent_id = None,  parameters_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.parent_id = parent_id
        self.table = "FunctionDefs"
        self.category = "FunctionDef"
        self.functiondef_id = functiondef_id
        self.name_convention = name_convention
        self.number_of_characters = number_of_characters
        self.is_private = is_private
        self.is_magic = is_magic
        self.body_count = body_count
        self.expressions_pct = expressions_pct
        self.is_async = is_async
        self.number_of_decorators = number_of_decorators
        self.has_return_type_annotation = has_return_type_annotation
        self.has_doc_string = has_doc_string
        self.height = height
        self.type_annotations_pct = type_annotations_pct
        self.source_code = source_code
        self.module_id = module_id
        self.parameters_id = parameters_id


class DBMethodDef:
    def __init__(self, category = None, methoddef_id = None,  classdef_id = None, 
                 is_class_method: bool = None,  is_static_method: bool = None, 
                 is_constructor_method: bool = None,  is_abstract_method: bool = None, 
                 is_property: bool = None,  is_wrapper: bool = None,  is_cached: bool = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "MethodDefs"
        self.category = "MethodDef"
        self.methoddef_id = methoddef_id
        self.classdef_id = classdef_id
        self.is_class_method = is_class_method
        self.is_static_method = is_static_method
        self.is_constructor_method = is_constructor_method
        self.is_abstract_method = is_abstract_method
        self.is_property = is_property
        self.is_wrapper = is_wrapper
        self.is_cached = is_cached


class DBParameter:
    def __init__(self,  number_of_params: int = None, parent_id: int = None,
                 pos_only_param_pct: float = None,  var_param_pct: float = None, 
                 has_var_param: bool = None,  type_annotation_pct: float = None, 
                 kw_only_param_pct: float = None,  default_value_pct: float = None, 
                 has_KW_param: bool = None,  name_convention: str = None,  node = None,
                 user_id = None, expertise_level = None, parameters_role : str = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Parameters"
        self.category = "Parameter"
        self.number_of_params = number_of_params
        self.pos_only_param_pct = pos_only_param_pct
        self.var_param_pct = var_param_pct
        self.has_var_param = has_var_param
        self.type_annotation_pct = type_annotation_pct
        self.kw_only_param_pct = kw_only_param_pct
        self.default_value_pct = default_value_pct
        self.has_KW_param = has_KW_param
        self.name_convention = name_convention
        self.parameters_id = 0
        self.parent_id = parent_id
        self.parameters_role = parameters_role


class DBStatement:
    def __init__(self,  statement_id = None,  category: str = None,  parent: str = None,  statement_role: str = None, 
                 height: int = None,  depth: int = None,  source_code: str = None,  parent_id = None,  node = None, 
                 has_or_else: bool = None,  body_size: int = None, 
                 first_child_id: int = None,  second_child_id: int = None, 
                 third_child_id: int = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Statements"
        self.statement_id = statement_id
        self.category = category
        self.parent = parent
        self.statement_role = statement_role
        self.height = height
        self.depth = depth
        self.source_code = source_code
        self.has_or_else = has_or_else
        self.body_size = body_size
        self.first_child_id = first_child_id
        self.second_child_id = second_child_id
        self.third_child_id = third_child_id
        self.parent_id = parent_id


class DBExpression:
    def __init__(self,  expression_id = None,  category: str = None, 
                 first_child_category: str = None,  second_child_category: str = None, 
                 third_child_category: str = None,  fourth_child_category: str = None,
                 first_child_id: str = None, second_child_id: str = None,
                 third_child_id: str = None, fourth_child_id: str = None,
                 parent: str = None,  expression_role: str = None,  height: int = None, 
                 depth: int = None,  source_code: str = None,  parent_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Expressions"
        self.expression_id = expression_id
        self.category = category
        self.first_child_category = first_child_category
        self.second_child_category = second_child_category
        self.third_child_category = third_child_category
        self.fourth_child_category = fourth_child_category
        self.first_child_id = first_child_id
        self.second_child_id = second_child_id
        self.third_child_id = third_child_id
        self.fourth_child_id = fourth_child_id
        self.parent = parent
        self.expression_role = expression_role
        self.height = height
        self.depth = depth
        self.source_code = source_code
        self.parent_id = parent_id


class DBComprehension:
    def __init__(self,  category: str = None,  number_of_ifs: int = None, 
                 number_of_generators: int = None,  is_async: bool = None, 
                 expression_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Comprehensions"
        self.category = category
        self.number_of_ifs = number_of_ifs
        self.number_of_generators = number_of_generators
        self.is_async = is_async
        self.expression_id = expression_id


class DBFString:
    def __init__(self,  number_of_elements: int = None,  constants_pct: float = None, 
                 expressions_pct: float = None,  expression_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "FStrings"
        self.category = "FString"
        self.number_of_elements = number_of_elements
        self.constants_pct = constants_pct
        self.expressions_pct = expressions_pct
        self.expression_id = expression_id


class DBVariable:
    def __init__(self,  name_convention: str = None,  number_of_characters: int = None, 
                 is_private: bool = None,  is_magic: bool = None,  expression_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Variables"
        self.name_convention = name_convention
        self.number_of_characters = number_of_characters
        self.is_private = is_private
        self.is_magic = is_magic
        self.expression_id = expression_id

class DBVector:
    def __init__(self,  category: str = None,  number_of_elements: int = None, 
                 homogeneous: bool = None,  expression_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Vectors"
        self.category = category
        self.number_of_elements = number_of_elements
        self.homogeneous = homogeneous
        self.expression_id = expression_id


class DBCallArg:
    def __init__(self,  number_args: int = None, 
                 named_args_pct: float = None,  double_star_args_pct: float = None, 
                 expression_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "CallArgs"
        self.number_args = number_args
        self.named_args_pct = named_args_pct
        self.double_star_args_pct = double_star_args_pct
        self.expression_id = expression_id
        self.callArgs_id = 0

class DBCase:
    def __init__(self,  number_of_cases: int = None,  guards: float = None, 
                 average_body_count: float = None,  average_match_value: float = None, 
                 average_match_singleton: float = None,  average_match_sequence: float = None, 
                 average_match_mapping: float = None,  average_match_class: float = None, 
                 average_match_star: float = None,  average_match_as: float = None, 
                 average_match_or: float = None,  statement_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Cases"
        self.number_of_cases = number_of_cases
        self.guards = guards
        self.average_body_count = average_body_count
        self.average_match_value = average_match_value
        self.average_match_singleton = average_match_singleton
        self.average_match_sequence = average_match_sequence
        self.average_match_mapping = average_match_mapping
        self.average_match_class = average_match_class
        self.average_match_star = average_match_star
        self.average_match_as = average_match_as
        self.average_match_or = average_match_or
        self.statement_id = statement_id


class DBHandler:
    def __init__(self,  number_of_handlers: int = None, category: str = None, 
                 has_finally: bool = None,  has_catch_all: bool = None, 
                 average_body_count: float = None,  has_star: bool = None, 
                 statement_id = None,  node = None, user_id = None, expertise_level = None):
        self.user_id = user_id
        self.expertise_level = expertise_level
        self.node = node
        self.table = "Handler"
        self.category = "ExceptHandler"
        self.number_of_handlers = number_of_handlers
        self.has_finally = has_finally
        self.has_catch_all = has_catch_all
        self.average_body_count = average_body_count
        self.has_star = has_star
        self.statement_id = statement_id
