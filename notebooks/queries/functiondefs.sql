select
	functiondef_id,
    name_convention as functiondef__name_convention,
    number_of_characters as functiondef__number_of_characters,
    is_private as functiondef__is_private,
    is_magic as functiondef__is_magic,
    body_count as functiondef__body_count,
    expressions_pct as functiondef__expressions_pct,
    is_async as functiondef__is_async,
    number_of_decorators as functiondef__number_of_decorators,
    has_return_type_annotation as functiondef__has_return_type_annotation,
    has_doc_string as functiondef__has_doc_string,
    height as functiondef__height,
    type_annotations_pct as functiondef__type_annotations_pct,
    expertise_level as functiondef__expertise_level
FROM functiondefs
    WHERE  functiondef_id NOT IN (
    SELECT methoddef_id
    FROM methoddefs
);