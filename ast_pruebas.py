import ast
from python_tfg.util.util import IDGetter
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
idGetter = IDGetter()

def controlUsers(directorio: str):
    user_id = None
    patron = re.compile(r"[0-9]{8}[A-Z]")
    coincidencia = patron.search(directorio)
    if coincidencia:
        user = coincidencia.group()
        if user in users:
            user_id = users[user]
        else:
            user_id = idGetter.getID
            users[user] = user_id
    else:
        proyecto = directorio.split('\\')[-1].replace(' ','')
        if proyecto in desconocido:
            user_id = desconocido[proyecto]
        else:
            user_id = idGetter.getID
            desconocido[proyecto] = user_id
    return user_id

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
                    visitor.visit_Program({ "path" : project, "user_id" : user_id, "expertise_level" : "BEGGINER" })
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
    init_db()
    warnings.filterwarnings("error")

    #PROBAR VISITOR DE RECOGIDA DE INFORMACIÓN
    visitor = Visitor_info(idGetter)
    visit(visitor)

     
    #PROBAR VISITOR DE PRINTEO DE INFORMACIÓN
    #visitor = Visitor_print()
    #ruta = './python_tfg/test/test_entities.py'
    #file = ''
    #with open(ruta, "r",  encoding='utf-8') as f:
    #    file = f.read()
    #ast_prueba = ast.parse(file)
    #visitor.visit(ast_prueba, {})

    
