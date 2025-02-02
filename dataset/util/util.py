import ast
import re
from typing import Dict
from dataset.db.db_utils import get_db_current_id


def op_category(node: ast.BinOp) -> str:
    op = node.op.__doc__
    match op:
        case 'Add' | 'Sub' | 'Mult' | 'Div' | 'FloorDiv' | 'Mod': return 'Arithmetic'
        case 'Pow': return 'Pow'
        case 'LShift' | 'RShift': return 'Shift'
        case 'BitOr' | 'BitXor' | 'BitAnd': return 'BWLogical'
        case 'MatMult': return 'MatMult'
        case 'UAdd' | 'USub': return 'UnaryArithmetic'
        case 'Not': return 'UnaryNot'
        case 'Invert': return 'UnaryBWNot' 


def const_category(node: ast.Constant) -> str:
    const_type = str(type(node.value)).split('\'')[1]
    match const_type:
        case 'int': return 'IntLiteral'
        case 'float': return 'FloatLiteral'
        case 'NoneType': return 'NoneLiteral'
        case 'bool': return 'BoolLiteral'
        case 'str': return 'StringLiteral'
        case 'ellipsis': return 'EllipsisLiteral'
        case _: return 'ComplexLiteral'


def name_convention(name: str) -> str:
    lower_pattern = re.compile(r'^[a-z0-9]+$')
    upper_pattern = re.compile(r'^[A-Z_0-9]+$')
    camel_low_pattern = re.compile(r'^[a-z][a-zA-Z0-9]*$')
    camel_up_pattern = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
    snake_case_pattern = re.compile(r'^[a-z_0-9]+$')
    discard_pattern = re.compile(r'^_+$')
    if discard_pattern.match(name):
        return 'Discard'
    elif lower_pattern.match(name):
        return 'Lower'
    elif snake_case_pattern.match(name):
        return 'SnakeCase'
    elif upper_pattern.match(name):
        return 'Upper'
    elif camel_low_pattern.match(name):
        return 'CamelLow'
    elif camel_up_pattern.match(name):
        return 'CamelUp'
    else: 
        return 'NoNameConvention'


def add_param(dict_1: Dict, param, value) -> Dict:
    new_dict = dict_1.copy()
    new_dict[param] = value
    return new_dict


def sum_match(dict_1: Dict, dict_2: Dict) -> Dict:
    return {
        'match_value': dict_1["match_value"] + dict_2["match_value"],
        'match_singleton': dict_1["match_singleton"] + dict_2["match_singleton"],
        'match_sequence': dict_1["match_sequence"] + dict_2["match_sequence"],
        'match_mapping': dict_1["match_mapping"] + dict_2["match_mapping"],
        'match_class': dict_1["match_class"] + dict_2["match_class"],
        'match_star': dict_1["match_star"] + dict_2["match_star"],
        'match_as': dict_1["match_as"] + dict_2["match_as"],
        'match_or': dict_1["match_or"] + dict_2["match_or"],
        'depth': max(dict_1["depth"], dict_2["depth"])
    }


def get_method_info(method):
    method_info = {'magic': False, 'private': False, 'abstract': False, 'wrapper': False, 'cached': False, 'static': False, 'class_method': False, 'property': False}
    magic_pattern = re.compile(r'^__\w+__$')
    private_pattern = re.compile(r'^_\w+$')
    method_info["magic"] = True if magic_pattern.match(method.name) else False
    method_info["private"] = True if private_pattern.match(method.name) and not method_info["magic"] else False
    for decorator in method.decorator_list:
        if isinstance(decorator, ast.Name):
            if decorator.id == "abstractmethod":
                method_info["abstract"] = True
            if decorator.id == "cache":
                method_info["cached"] = True
            if decorator.id == "staticmethod":
                method_info["static"] = True
            if decorator.id == "classmethod":
                method_info["class_method"] = True
            if decorator.id == "property":
                method_info["property"] = True
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                if decorator.func.id == "wraps":
                    method_info["wrapper"] = True
    return method_info


def get_args_name_convention(naming_conventions: Dict) -> str:
    name_convention = None
    max = 0
    for nc in naming_conventions.keys():
        if naming_conventions[nc] > max:
            max = naming_conventions[nc]
            name_convention = nc
    return name_convention


class IDManager:
    def __init__(self):
        self.current_id = self.get_current_id()

    @staticmethod
    def get_current_id() -> int:
        current_id = get_db_current_id()
        if current_id == -1:
            raise RuntimeError("ID getter not working")
        return current_id

    def get_id(self) -> int:
        next_id = self.current_id
        self.current_id += 1
        return next_id
