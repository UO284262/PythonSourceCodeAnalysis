-- Creación de la tabla NODES
CREATE TABLE NODES (
    node_id BIGINT PRIMARY KEY,
    parent_table VARCHAR(255),
    parent_id BIGINT,
    FOREIGN KEY (parent_id) REFERENCES NODES(node_id)
);

-- Creación de la tabla PROGRAMS
CREATE TABLE PROGRAMS (
    program_id BIGINT PRIMARY KEY,
    name VARCHAR(1000),
    has_sub_dirs_with_code BOOLEAN,
    has_packages BOOLEAN,
    number_of_modules INTEGER,
    number_of_sub_dirs_with_code INTEGER,
    number_of_packages INTEGER,
    class_defs_pct REAL CHECK (class_defs_pct >= 0 AND class_defs_pct <= 1),
    function_defs_pct REAL CHECK (function_defs_pct >= 0 AND function_defs_pct <= 1),
    enum_defs_pct REAL CHECK (enum_defs_pct >= 0 AND enum_defs_pct <= 1),
    has_code_root_package BOOLEAN,
    average_defs_per_module REAL,
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla PARAMETERS
CREATE TABLE PARAMETERS (
    parameters_id BIGINT PRIMARY KEY,
    parent_id BIGINT,
    parameters_role VARCHAR(255),
    number_of_params INTEGER,
    pos_only_param_pct REAL CHECK (pos_only_param_pct >= 0 AND pos_only_param_pct <= 1),
    var_param_pct REAL CHECK (var_param_pct >= 0 AND var_param_pct <= 1),
    has_var_param BOOLEAN,
    type_annotation_pct REAL CHECK (type_annotation_pct >= 0 AND type_annotation_pct <= 1),
    kw_only_param_pct REAL CHECK (kw_only_param_pct >= 0 AND kw_only_param_pct <= 1),
    default_value_pct REAL CHECK (default_value_pct >= 0 AND default_value_pct <= 1),
    has_KW_param BOOLEAN,
    name_convention VARCHAR(255),
    user_id BIGINT,
    expertise_level VARCHAR(20),
    FOREIGN KEY (parent_id) REFERENCES NODES(node_id),
    FOREIGN KEY (parameters_id) REFERENCES NODES(node_id)
);

-- Creación de la tabla MODULES
CREATE TABLE MODULES (
    module_id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    name_convention VARCHAR(255),
    has_doc_string BOOLEAN,
    global_stmts_pct REAL CHECK (global_stmts_pct >= 0 AND global_stmts_pct <= 1),
    global_expressions REAL CHECK (global_expressions >= 0 AND global_expressions <= 1),
    number_of_classes INTEGER,
    number_of_functions INTEGER,
    class_defs_pct REAL CHECK (class_defs_pct >= 0 AND class_defs_pct <= 1),
    function_defs_pct REAL CHECK (function_defs_pct >= 0 AND function_defs_pct <= 1),
    enum_defs_pct REAL CHECK (enum_defs_pct >= 0 AND enum_defs_pct <= 1),
    average_stmts_function_body REAL,
    average_stmts_method_body REAL,
    type_annotations_pct REAL CHECK (type_annotations_pct >= 0 AND type_annotations_pct <= 1),
    has_entry_point BOOLEAN,
    path VARCHAR(1000),
    program_id BIGINT,
    import_id BIGINT UNIQUE,
    FOREIGN KEY (module_id) REFERENCES NODES(node_id),
    FOREIGN KEY (program_id) REFERENCES PROGRAMS(program_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla IMPORTS
CREATE TABLE IMPORTS (
    import_id BIGINT PRIMARY KEY,
    number_imports INTEGER,
    module_imports_pct REAL CHECK (module_imports_pct >= 0 AND module_imports_pct <= 1),
    average_imported_modules REAL,
    from_imports_pct REAL CHECK (from_imports_pct >= 0 AND from_imports_pct <= 1),
    average_from_imported_modules REAL,
    average_as_in_imported_modules REAL,
    local_imports_pct REAL CHECK (local_imports_pct >= 0 AND local_imports_pct <= 1),
    user_id BIGINT,
    expertise_level VARCHAR(20),
    FOREIGN KEY (import_id) REFERENCES MODULES(import_id)
);

-- Creación de la tabla CLASSDEFS
CREATE TABLE CLASSDEFS (
    classdef_id BIGINT PRIMARY KEY,
    name_convention VARCHAR(255),
    is_enum_class BOOLEAN,
    number_of_characters INTEGER,
    number_of_decorators INTEGER,
    number_of_methods INTEGER,
    number_of_base_classes INTEGER,
    has_generic_type_annotations BOOLEAN,
    has_doc_string BOOLEAN,
    body_count INTEGER,
    assignments_pct REAL CHECK (assignments_pct >= 0 AND assignments_pct <= 1),
    expressions_pct REAL CHECK (expressions_pct >= 0 AND expressions_pct <= 1),
    uses_meta_class BOOLEAN,
    number_of_keywords INTEGER,
    height INTEGER,
    average_stmts_method_body REAL,
    type_annotations_pct REAL CHECK (type_annotations_pct >= 0 AND type_annotations_pct <= 1),
    private_methods_pct REAL CHECK (private_methods_pct >= 0 AND private_methods_pct <= 1),
    magic_methods_pct REAL CHECK (magic_methods_pct >= 0 AND magic_methods_pct <= 1),
    async_methods_pct REAL CHECK (async_methods_pct >= 0 AND async_methods_pct <= 1),
    class_methods_pct REAL CHECK (class_methods_pct >= 0 AND class_methods_pct <= 1),
    static_methods_pct REAL CHECK (static_methods_pct >= 0 AND static_methods_pct <= 1),
    abstract_methods_pct REAL CHECK (abstract_methods_pct >= 0 AND abstract_methods_pct <= 1),
    property_methods_pct REAL CHECK (abstract_methods_pct >= 0 AND abstract_methods_pct <= 1),
    source_code text,
    module_id BIGINT,
    parent_id BIGINT,
    FOREIGN KEY (classdef_id) REFERENCES NODES(node_id),
    FOREIGN KEY (module_id) REFERENCES MODULES(module_id),
    FOREIGN KEY (parent_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla FUNCTIONDEFS
CREATE TABLE FUNCTIONDEFS (
    functiondef_id BIGINT PRIMARY KEY,
    name_convention VARCHAR(255),
    number_of_characters INTEGER,
    is_private BOOLEAN,
    is_magic BOOLEAN,
    body_count INTEGER,
    expressions_pct REAL CHECK (expressions_pct >= 0 AND expressions_pct <= 1),
    is_async BOOLEAN,
    number_of_decorators INTEGER,
    has_return_type_annotation BOOLEAN,
    has_doc_string BOOLEAN,
    height INTEGER,
    type_annotations_pct REAL CHECK (type_annotations_pct >= 0 AND type_annotations_pct <= 1),
    source_code text,
    module_id BIGINT,
    parent_id BIGINT,
    parameters_id BIGINT,
    FOREIGN KEY (functiondef_id) REFERENCES NODES(node_id),
    FOREIGN KEY (module_id) REFERENCES MODULES(module_id),
    FOREIGN KEY (parent_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla METHODDEFS
CREATE TABLE METHODDEFS (
    methoddef_id BIGINT PRIMARY KEY,
    is_class_method BOOLEAN,
    is_static_method BOOLEAN,
    is_constructor_method BOOLEAN,
    is_abstract_method BOOLEAN,
    is_property BOOLEAN,
    is_wrapper BOOLEAN,
    is_cached BOOLEAN,
    classdef_id BIGINT,
    FOREIGN KEY (methoddef_id) REFERENCES FUNCTIONDEFS(functiondef_id),
    FOREIGN KEY (classdef_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla STATEMENTS
CREATE TABLE STATEMENTS (
    statement_id BIGINT PRIMARY KEY,
    category VARCHAR(255),
    parent VARCHAR(255),
    statement_role VARCHAR(255),
    height INTEGER,
    depth INTEGER,
    source_code text,
    has_or_else BOOLEAN,
    body_size INTEGER,
    first_child_id BIGINT,
    second_child_id BIGINT,
    third_child_id BIGINT,
    parent_id BIGINT,
    FOREIGN KEY (statement_id) REFERENCES NODES(node_id),
    FOREIGN KEY (first_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (second_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (third_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (parent_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla CASES
CREATE TABLE CASES (
    statement_id BIGINT PRIMARY KEY,
    number_of_cases INTEGER,
    guards REAL CHECK (guards >= 0 AND guards <= 1),
    average_body_count REAL,
    average_match_value REAL CHECK (average_match_value >= 0 AND average_match_value <= 1),
    average_match_singleton REAL CHECK (average_match_singleton >= 0 AND average_match_singleton <= 1),
    average_match_sequence REAL CHECK (average_match_sequence >= 0 AND average_match_sequence <= 1),
    average_match_mapping REAL CHECK (average_match_mapping >= 0 AND average_match_mapping <= 1),
    average_match_class REAL CHECK (average_match_class >= 0 AND average_match_class <= 1),
    average_match_star REAL CHECK (average_match_star >= 0 AND average_match_star <= 1),
    average_match_as REAL CHECK (average_match_as >= 0 AND average_match_as <= 1),
    average_match_or REAL CHECK (average_match_or >= 0 AND average_match_or <= 1),
    FOREIGN KEY (statement_id) REFERENCES STATEMENTS(statement_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla HANDLERS
CREATE TABLE HANDLERS (
    statement_id BIGINT PRIMARY KEY,
    number_of_handlers INTEGER,
    has_finally BOOLEAN,
    has_catch_all BOOLEAN,
    average_body_count REAL,
    has_star BOOLEAN,
    FOREIGN KEY (statement_id) REFERENCES STATEMENTS(statement_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla EXPRESSIONS
CREATE TABLE EXPRESSIONS (
    expression_id BIGINT PRIMARY KEY,
    category VARCHAR(255),
    parent VARCHAR(255),
    first_child_category VARCHAR(255),
    second_child_category VARCHAR(255),
    third_child_category VARCHAR(255),
    fourth_child_category VARCHAR(255),
    first_child_id BIGINT,
    second_child_id BIGINT,
    third_child_id BIGINT,
    fourth_child_id BIGINT,
    expression_role VARCHAR(255),
    height INTEGER,
    depth INTEGER,
    source_code text,
    parent_id BIGINT,
    FOREIGN KEY (expression_id) REFERENCES NODES(node_id),
    FOREIGN KEY (first_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (second_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (third_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (fourth_child_id) REFERENCES NODES(node_id),
    FOREIGN KEY (parent_id) REFERENCES NODES(node_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla COMPREHENSIONS
CREATE TABLE COMPREHENSIONS (
    expression_id BIGINT PRIMARY KEY,
    category VARCHAR(255),
    number_of_ifs INTEGER,
    number_of_generators INTEGER,
    is_async BOOLEAN,
    FOREIGN KEY (expression_id) REFERENCES EXPRESSIONS(expression_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla CALLARGS
CREATE TABLE CALLARGS (
    expression_id BIGINT PRIMARY KEY,
    number_args INTEGER,
    named_args_pct REAL CHECK (named_args_pct >= 0 AND named_args_pct <= 1),
    double_star_args_pct REAL CHECK (double_star_args_pct >= 0 AND double_star_args_pct <= 1),
    FOREIGN KEY (expression_id) REFERENCES EXPRESSIONS(expression_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla FSTRINGS
CREATE TABLE FSTRINGS (
    expression_id BIGINT PRIMARY KEY,
    number_of_elements INTEGER,
    constants_pct REAL CHECK (constants_pct >= 0 AND constants_pct <= 1),
    expressions_pct REAL CHECK (expressions_pct >= 0 AND expressions_pct <= 1),
    FOREIGN KEY (expression_id) REFERENCES EXPRESSIONS(expression_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla VARIABLES
CREATE TABLE VARIABLES (
    expression_id BIGINT PRIMARY KEY,
    name_convention VARCHAR(255),
    number_of_characters INTEGER,
    is_private BOOLEAN,
    is_magic BOOLEAN,
    FOREIGN KEY (expression_id) REFERENCES EXPRESSIONS(expression_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);

-- Creación de la tabla VECTORS
CREATE TABLE VECTORS (
    expression_id BIGINT PRIMARY KEY,
    category VARCHAR(255),
    number_of_elements INTEGER,
    homogeneous BOOLEAN,
    FOREIGN KEY (expression_id) REFERENCES EXPRESSIONS(expression_id),
    user_id BIGINT,
    expertise_level VARCHAR(20)
);