import ast
from visitors.visitor_print import Visitor_print
from visitors.visitor_info import Visitor_info
from db.db_utils import init_db
import os
import re
import uuid
import warnings

directorio_principal = '.\\python_tfg\\20-21'

users = {}
desconocido = {}

def controlUsers(directorio: str):
    patron = re.compile(r"[0-9]{8}[A-Z]")
    coincidencia = patron.search(directorio)
    if coincidencia:
        user = coincidencia.group()
        if user in users:
            id = users[user]
        else:
            id = uuid.uuid4().int
            users[user] = id
    else:
        proyecto = directorio.split('\\')[-1].replace(' ','')
        if proyecto in desconocido:
            id = desconocido[proyecto]
        else:
            id = uuid.uuid4().int
            desconocido[proyecto] = id
    return id

def getSourcePackage(ruta):
    for directorio_actual, subdirectorios, archivos in os.walk(ruta):
        hasPyFiles = False
        for archivo in archivos:
            if archivo.endswith('.py'): 
                hasPyFiles = True
                break
        if not hasPyFiles and len(subdirectorios) == 1:
            yield next(getSourcePackage(os.path.join(directorio_actual, subdirectorios[0])))
        elif not hasPyFiles and len(subdirectorios) == 0:
            yield ' '
        elif hasPyFiles:
            yield directorio_actual

# Recorrer directorios y archivos usando os.walk
def visit(visitor):
    projects = []
    for project in getSourcePackage(directorio_principal):
        if project != ' ':
            user_id = controlUsers(project)
            if(project not in projects):
                    projects.append(project)
                    visitor.visit_Program({ "path" : project, "user_id" : user_id, "experticeLevel" : "BEGGINER" })
    """
    for directorio_actual, subdirectorios, archivos in os.walk(directorio_principal):
        id = controlUsers(directorio_actual)
        if id:
            project = getSourcePackage(directorio_actual)
            if(project not in projects):
                projects.append(project)
                visitor.visit_Program({ "path" : project, "id" : "id", "user_id" : id, "experticeLevel" : "BEGGINER" })
    """


#Visitor_info.visit(ast_1)
if __name__ == '__main__':
    #init_db()
    warnings.filterwarnings("error")


    #PROBAR VISITOR DE RECOGIDA DE INFORMACIÓN
    #visitor = Visitor_info()
    #visit(visitor)

     
    #PROBAR VISITOR DE PRINTEO DE INFORMACIÓN
    visitor = Visitor_print()
    ruta = './python_tfg/test/test.py'
    file = ''
    with open(ruta, "r",  encoding='utf-8') as f:
        file = f.read()
    ast_prueba = ast.parse(file)
    visitor.visit(ast_prueba, {})

    
