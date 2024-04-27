SELECT
    program_id as program__program_id,
    name as program__name,
    has_sub_dirs_with_code as program__has_sub_dirs_with_code,
    has_packages as program__has_packages,
    number_of_modules as program__number_of_modules,
    number_of_sub_dirs_with_code as program__number_of_sub_dirs_with_code,
    number_of_packages as program__number_of_packages,
    class_defs_pct as program__class_defs_pct,
    function_defs_pct as program__function_defs_pct,
    enum_defs_pct as program__enum_defs_pct,
    has_code_root_package as program__has_code_root_package,
    average_defs_per_module as program__average_defs_per_module,
    user_id as program__user_id,
    expertise_level as program__expertise_level
FROM programs;



