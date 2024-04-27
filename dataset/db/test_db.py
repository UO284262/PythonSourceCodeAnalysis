from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

POSTGRES_USERNAME = "postgres"
POSTGRES_PASSWORD = "ayneastq2219"
POSTGRES_ADDRESS = "156.35.95.39"
POSTGRES_PORT = 5432
POSTGRES_DBNAME = "python_tfg"


def get_programs(session):
    result = session.execute(
        text('Select * from module')
    )
    return result


def main():
    session_maker = sessionmaker()
    postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                            password=POSTGRES_PASSWORD,
                                                                                            ipaddress=POSTGRES_ADDRESS,
                                                                                            port=POSTGRES_PORT,
                                                                                            dbname=POSTGRES_DBNAME))
    engine = create_engine(postgres_str)
    session_maker.configure(bind=engine)
    session = session_maker()
    programs = get_programs(session)

    for program in programs:
        name = program[0]
        print("Proccessing " + name + " ...")


if __name__ == '__main__':
    main()
