SELECT
    name_convention as module__name_convention,
    has_doc_string as module__has_doc_string,
    global_stmts_pct as module__global_stmts_pct,
    global_expressions as module__global_expressions,
    number_of_classes as module__number_of_classes,
    number_of_functions as module__number_of_functions,
    class_defs_pct as module__class_defs_pct,
    function_defs_pct as module__function_defs_pct,
    enum_defs_pct as module__enum_defs_pct,
    average_stmts_function_body as module__average_stmts_function_body,
    average_stmts_method_body as module__average_stmts_method_body,
    type_annotations_pct as module__type_annotations_pct,
    has_entry_point as module__has_entry_point,
    expertise_level as module__expertise_level
FROM modules;
