import ast
from db.db_utils import get_db_current_id


def op_category(node):
    op = node.op.__doc__
    match op:
        case 'Add' | 'Sub' | 'Mult' | 'Div' | 'FloorDiv' | 'Mod': return 'Arithmetic'
        case 'Pow': return 'Pow'
        case 'LShift' | 'RShift': return 'Shift'
        case 'BitOr' | 'BitXor' | 'BitAnd': return 'BW1Logical'
        case 'MatMult': return 'MatMult'
        case 'UAdd' | 'USub': return 'UnaryArithmetic'
        case 'Not': return 'UnaryNot'
        case 'Invert': return 'UnaryBWNot' 


def const_category(node: ast.Constant):
    const_type = str(type(node.value)).split('\'')[1]
    match const_type:
        case 'int': return 'IntLiteral'
        case 'float': return 'FloatLiteral'
        case 'NoneType': return 'NoneLiteral'
        case 'bool': return 'BoolLiteral'
        case 'str': return 'StringLiteral'
        case 'ellipsis': return 'EllipsisLiteral'
        case _: return 'ComplexLiteral'


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
