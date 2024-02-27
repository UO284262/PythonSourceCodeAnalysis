import ast
from db_utils import getCurrentID

def opCategory(node):
    op = node.op.__doc__
    match op:
        case 'Add', 'Sub', 'Mult', 'Div', 'FloorDiv', 'Mod': return 'Arithmetic'
        case 'Pow': return 'Pow'
        case 'LShift', 'RShift': return 'Shift'
        case 'BitOr', 'BitXor', 'BitAnd': return 'BW1Logical'
        case 'MatMult': return 'MatMult'
        case 'UAdd', 'USub': return 'UnaryArithmetic'
        case 'Not': return 'UnaryNot'
        case 'Invert': return 'UnaryBWNot' 

def constCategory(node: ast.Constant):
    const_type = type(node.value) #.split('')[1]
    match const_type:
        case 'int': return 'IntLiteral'
        case 'float': return 'FloatLiteral'
        case 'NoneType': return 'NoneLiteral'
        case 'bool': return 'BoolLiteral'
        case 'str': return 'StringLiteral'
        case 'ellipsis': return 'EllipsisLiteral'
        case _: return 'ComplexLiteral'

class IDGetter():

    def __init__(self):
        self.currentID = self.getCurrentID()

    def getCurrentID(self):
        currentID = getCurrentID()
        if currentID == -1: raise RuntimeError("ID getter not working")
        return currentID

    def getID(self):
        aux = self.currentID + 1
        self.currentID += 1
        return aux