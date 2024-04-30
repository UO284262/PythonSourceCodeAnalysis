import ast
from typing import List
from util.util import IDManager
from visitors.visitorintrospector import VisitorIntrospector
from visitors.visitorprint import VisitorPrint
from visitors.visitorinfo import VisitorInfo
import os
import re
import warnings
import sys

users = {}
unknown = {}
id_manager = None


def control_users(folder: str) -> int:
    user_id = None
    result = re.compile(r"[0-9]{8}[A-Z]").search(folder)
    if result:
        user = result.group()
        if user in users:
            user_id = users[user]
        else:
            user_id = id_manager.get_id()
            users[user] = user_id
    else:
        project = folder.split('\\')[-1].replace(' ', '')
        if project in unknown:
            user_id = unknown[project]
        else:
            user_id = id_manager.get_id()
            unknown[project] = user_id
    return user_id


def get_source_package(path: str) -> str:
    for current_folder, folders, files in os.walk(path):
        has_py_files = False
        for file in files:
            if file.endswith('.py'):
                has_py_files = True
                break
        if not has_py_files and len(folders) == 1:
            yield next(get_source_package(os.path.join(current_folder, folders[0])))
        elif not has_py_files and len(folders) == 0:
            yield ' '
        elif has_py_files:
            yield current_folder


def not_read(project: str, projects: List[str]) -> bool:
    for p in projects:
        if (p in project) or (project in p):
            return False
    return True


# Walk through directories and files using os.walk
def run(visitor: ast.NodeVisitor, source_folder: str):
    projects = []
    if(not project_folder):
        for project in get_source_package(source_folder):
            if project != ' ':
                user_id = control_users(project)
                if not_read(project, projects):
                    projects.append(project)
                    visitor.visit_Program({"path": project, "user_id": user_id, "expertise_level": expertice_level})
    else:
        user_id = control_users(project_folder)
        if not_read(project_folder, projects):
            projects.append(project_folder)
            visitor.visit_Program({"path": project_folder, "user_id": user_id, "expertise_level": expertice_level})

def pretty_print(path: str):
    visitor = VisitorPrint()
    with open(path, "r", encoding='utf-8') as f:
        test_file = f.read()
    visitor.visit(ast.parse(test_file), {})


if __name__ == '__main__':
    # init_db()
    id_manager = IDManager()
    warnings.filterwarnings("error")
    source_folder = './dataset/test/test_file'
    expertice_level = 'BEGINNER'
    project_folder = None
    if len(sys.argv) == 2:
        source_folder = sys.argv[1]
    elif len(sys.argv) == 3:
        source_folder = sys.argv[1]
        expertice_level = sys.argv[2]
    elif len(sys.argv) == 4:
        source_folder = sys.argv[1]
        expertice_level = sys.argv[2]
        project_folder = sys.argv[3]

    # Testing VisitorIntrospector
    visitor = VisitorInfo(id_manager, VisitorIntrospector())

    # Testing VisitorDataBase
    # visitor = VisitorInfo(id_manager, VisitorDataBase())
    run(visitor, source_folder)

    # Pretty print the AST
    # pretty_print('./python_tfg/test/test.py')







    
