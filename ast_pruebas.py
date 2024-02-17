import ast
from visitors.visitor_print import Visitor_print
#from visitors.visitor_info import Visitor_info
import os
import re
import uuid

directorio_principal = './20-21'

users = {}

def controlUsers(directorio):
    patron = re.compile(r"[0-9]{8}[A-Z]")
    coincidencia = patron.search(directorio)
    if coincidencia:
        user = coincidencia.group()
        if user in users:
            id = users[user]
        else:
            id = uuid.uuid4().int
            users[user] = id
        return id
    else:
        return uuid.uuid4().int #PREGUNTAR SI HAY QUE DEVOLVER UN USER_ID CUANDO NO HAY NINGUN ALUMNO ASOCIADO

# Recorrer directorios y archivos usando os.walk
for directorio_actual, subdirectorios, archivos in os.walk(directorio_principal):
    for archivo in archivos:
        ruta_completa = os.path.join(directorio_actual, archivo)
        id = controlUsers(ruta_completa)
        if(archivo.endswith('.py') and not 'MACOSX' in ruta_completa):
            with open(ruta_completa, "r",  encoding='utf-8') as f:
                try:
                    contenido = f.read()
                    module_ast = ast.parse(contenido)
                    #Visitor_info.visit_Module(module_ast)
                    #print('Formato correcto')
                except:
                    pass
                    #print('Formato del archivo {0}'.format(ruta_completa))

print(users)

ast_1 = ast.parse("""\
@decorator1
@decorator2
class Foo(Enum, base2, metaclass=meta):
    @absact
    def a(a: str):
        b = 0
        c = 0
        return a, b, c
    pass
""")

