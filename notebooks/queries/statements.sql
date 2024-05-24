SELECT
    category as statement__category,
    parent as statement__parent,
    statement_role as statement__statement_role,
    first_child_category as statement__first_child_category,
    second_child_category as statement__second_child_category,
    third_child_category as statement__third_child_category,
    height as statement__height,
    depth as statement__depth,
    has_or_else as statement__has_or_else,
    body_size as statement__body_size,
    expertise_level as statement__expertise_level
FROM statements;