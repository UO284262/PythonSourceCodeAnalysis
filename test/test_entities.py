# CONSTANT
123

# JOINED STR
f"1+1 is {(1+1):.3}"

# LIST
[1, 2, 3]

# TUPLE
(1, 2, 3)

# SET
{1, 2, 3}

# DICT
{'A' : 1, **1}

# NAME
a = 1
a
del a

# STARRED
a, *b = 5

# UNARY OP
not a

# BIN OP
a + a

# BOOL OP
a or a

# COMPARE
a > 1 in [1,2] <= 1

# FUNCTION DEF
def f():
    pass

# CALL
f()

# IF EXP
a if True else f()

# CLASS DEF
class obj():
    def __init__(self):
        self.a = 1

# ATTRIBUTE
obj1 = obj()
obj1.a

# NAMED EXPR
(x := 4)

# SUBSCRIPT
l = [1,2,3,4,5,6,7,8,9,10]
l[1:2, 3]

# SLICE
l[1:2]

# LIST COMP
[x for x in l]

# DICT COMP
{x: x**2 for x in l}

# SET COMP
{x for x in l}

# GENERATOR EXP
(x for x in l)

# ASSIGN 
a = b = 1

# ANN ASSIGN
c: int

# AUG ASSIGN
c += 1

# RAISE
try:
    raise Exception from None 
except Exception as e:
    pass

# ASSERT
assert x, y

# DELETE
del b, c

# PASS
pass

# TYPE ALIAS
type Alias = int

# IMPORT
import visitors

# IMPORT FROM
from visitors import visitor_db as v

# IF
if(1):
    pass
else:
    pass

# FOR
for i in range(10):
    pass

# WHILE
while 1:
    pass

# BREAK
while 1:
    break

# CONTINUE
while 1:
    continue

# TRY
try:
    pass
except:
    pass

# TRY STAR
try:
    pass
except* Exception:
    pass

# EXCEPT HANDLER
try:
    pass
except TypeError:
    pass

# WITH
with a as b, c as d:
    pass

# MATCH:
match a:
    case [x] if x > 0:
        pass
    case tuple():
        pass
    case 1:
        pass
    case None:
        pass
    case [1,2]:
        pass
    case [*_]:
        pass
    case {1: _, 2: _}:
        pass
    case {**rest}:
        pass
    case [x] as y:
        pass
    case 1 | 2:
        pass

# TYPE VAR
type Alias[T: int] = list[T]

# PARAM SPEC
type Alias[**P] = callable[P, int]

# TYPE VAR TUPLE
type Alias[*Ts] = tuple[*Ts]

# LAMBDA
lambda x,y: x+y

# RETURN
def a():
    return

# YIELD
def a():
    yield

# YIELD FROM
def a():
    yield from l

# GLOBAL
global g1,g2,g3

# NON LOCAL
def a():
    nl1 = nl2 = nl3 = 1
    def b():
        nonlocal nl1, nl2, nl3 

# ASYNC FUNCTION DEF
async def a():
    pass

# AWAIT
async def b():
    await a()

# ASYNC FOR
async def a():
    async for a in l:
        pass

# ASYNC WITH
async def a():
    async with a as b:
        pass

