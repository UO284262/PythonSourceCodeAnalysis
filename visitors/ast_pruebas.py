import ast
from visitor_print import Visitor_print
from visitor_info import Visitor_info
from db_utils import init_db
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
        return
        #return uuid.uuid4().int #PREGUNTAR SI HAY QUE DEVOLVER UN USER_ID CUANDO NO HAY NINGUN ALUMNO ASOCIADO

def getSourcePackage(ruta):
    for directorio_actual, subdirectorios, archivos in os.walk(ruta):
        if not archivos and len(subdirectorios) == 1:
            return getSourcePackage(os.path.join(directorio_actual, subdirectorios[0]))
        elif not archivos and len(subdirectorios) == 0:
            return
        elif archivos or len(subdirectorios) > 1:
            return directorio_actual

# Recorrer directorios y archivos usando os.walk
def visit():
    for directorio_actual, subdirectorios, archivos in os.walk(directorio_principal):
        id = controlUsers(directorio_actual)
        if id:
            project = getSourcePackage(directorio_actual)
            for directorio_actual, subdirectorios, archivos in os.walk(project):
                for archivo in archivos:
                    ruta_completa = os.path.join(directorio_actual, archivo)
                    id = controlUsers(ruta_completa)
                    if(archivo.endswith('.py') and not 'MACOSX' in ruta_completa):
                        with open(ruta_completa, "r",  encoding='utf-8') as f:
                            try:
                                contenido = f.read()
                                module_ast = ast.parse(contenido)
                                #Visitor_info.visit_Module(module_ast)
                                print('Formato correcto')
                            except: 
                                # NO COMPILAN
                                pass
                                print('Formato del archivo {0}'.format(ruta_completa))

    print(users)



#Visitor_info.visit(ast_1)
if __name__ == '__main__':
    #init_db()
    ast_1 = ast.parse(
    """a = 1""")

    visitor = Visitor_info()

    visitor.visit(ast_1, {"filename" : "prueba", "path" : "/prueba"})

    
