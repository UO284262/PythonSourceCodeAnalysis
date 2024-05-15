SELECT
    parameters_role as parameters__parameters_role,
    number_of_params as parameters__number_of_params,
    pos_only_param_pct as parameters__pos_only_param_pct,
    var_param_pct as parameters__var_param_pct,
    has_var_param as parameters__has_var_param,
    type_annotation_pct as parameters__type_annotation_pct,
    kw_only_param_pct as parameters__kw_only_param_pct,
    has_kw_param as parameters__has_kw_param,
    default_value_pct as parameters__default_value_pct,
    name_convention as parameters__name_convention,
    expertise_level as parameters__expertise_level
FROM parameters;