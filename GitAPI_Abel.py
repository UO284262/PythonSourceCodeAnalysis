from github import Github
from github import RateLimitExceededException
from github import UnknownObjectException
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import time
import os
import subprocess

"""
POSTGRES_USERNAME = "postgres"
POSTGRES_PASSWORD = "secreto"
POSTGRES_ADDRESS = "127.0.0.1"
POSTGRES_PORT = 5432
POSTGRES_DBNAME = "progquery"


SOURCES_PATH = "/home/jorge/sources"
"""

def insertProcessedProgram(session = None, git_owner = None, git_name = None, url = None, pom_file=False, multi_pom=False, compilable=False, progquery=False, program_non=0, program_nof=0, program_loc=0):
    """
    session.execute(
        "INSERT INTO Processed_Program (git_owner, git_name, url) values ("
        ":git_owner, :git_name, :url)",
        {"git_owner": git_owner, "git_name": git_name, "url": url}
    )
    """
    print("{};{};{}".format(git_owner, git_name, url))


def checkProgramProcessedIsProcessed(session, git_name, git_owner):
    """
    result = session.execute(
        "SELECT * FROM Processed_Program WHERE git_name=:git_name and git_owner=:git_owner",
        {"git_name": git_name, "git_owner": git_owner}
    )

    # Si no hay resultado, no esta procesado, por lo que hay que procesarlo
    if result.first() is None:
        return False
    return True
    """


def main():

    token = "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"
    g = Github(token)

    delay = 3600  # 60 min

    # Postgres connection and sessionmaker ORM instance
    """
    session_maker = sessionmaker()
    postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                            password=POSTGRES_PASSWORD,
                                                                                            ipaddress=POSTGRES_ADDRESS,
                                                                                            port=POSTGRES_PORT,
                                                                                            dbname=POSTGRES_DBNAME))
    engine = create_engine(postgres_str)
    session_maker.configure(bind=engine, autocommit=True)
    session = session_maker()
    """


    # Path donde se descargaran los programas    
    """"
    path = SOURCES_PATH
    os.chdir(path)
    """
    count = 0
    repos = g.search_repositories(query="language:python")
    for repo in repos:
        count += 1
        git_name = repo.name
        git_owner = repo.owner.login
        url = repo.clone_url
        print("[" + str(datetime.now()) +  "] Proccessing " + git_owner + ":" + git_name + " ...")

        """
        if not checkProgramProcessedIsProcessed(session, git_name, git_owner):
            try:
                insert_path = path + "/" + git_owner + "_" + git_name
                if not os.path.isdir(insert_path):
                    clone = "git clone " + url + " " + git_owner + "_" + git_name  # Path del sistema donde guardar el repositorio. Creado a partir del owner y el name
                    os.system(clone)  # Llamada al sistema para ejecutar el clone del repo
        """
        insertProcessedProgram(None, git_owner, git_name, url) # session
        """
                else:
                    print("Fail :(")
                    removeFromSystem(insert_path)
            except RateLimitExceededException:
                print("Se ha excedido el tiempo de peticiones, en espera por 60 min")
                time.sleep(delay)
        """
        if count == 50:
            break
    print("Finish!!")

if __name__ == '__main__':
    main()