SELECT
    expression_id as expression__expression_id,
    category as expression__category,
    parent as expression__parent,
    first_child_category as expression__first_child_category,
    second_child_category as expression__second_child_category,
    third_child_category as expression__third_child_category,
    fourth_child_category as expression__fourth_child_category,
    expression_role as expression__expression_role,
    height as expression__height,
    depth as expression__depth,
    expertise_level as expression__expertise_level
FROM expressions;