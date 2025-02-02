SELECT
    name_convention as classdef__name_convention,
    is_enum_class as classdef__is_enum_class,
    number_of_characters as classdef__number_of_characters,
    number_of_decorators as classdef__number_of_decorators,
    number_of_methods as classdef__number_of_methods,
    number_of_base_classes as classdef__number_of_base_classes,
    has_generic_type_annotations as classdef__has_generic_type_annotations,
    has_doc_string as classdef__has_doc_string,
    body_count as classdef__body_count,
    assignments_pct as classdef__assignments_pct,
    expressions_pct as classdef__expressions_pct,
    uses_meta_class as classdef__uses_meta_class,
    number_of_keywords as classdef__number_of_keywords,
    height as classdef__height,
    average_stmts_method_body as classdef__average_stmts_method_body,
    type_annotations_pct as classdef__type_annotations_pct,
    private_methods_pct as classdef__private_methods_pct,
    magic_methods_pct as classdef__magic_methods_pct,
    async_methods_pct as classdef__async_methods_pct,
    class_methods_pct as classdef__class_methods_pct,
    static_methods_pct as classdef__static_methods_pct,
    abstract_methods_pct as classdef__abstract_methods_pct,
    property_methods_pct as classdef__property_methods_pct,
    expertise_level as classdef__expertise_level
FROM classdefs;