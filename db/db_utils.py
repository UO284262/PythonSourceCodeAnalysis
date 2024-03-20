import psycopg2
import math

# Parámetros de conexión a la base de datos
conexion_params = {
    'dbname': 'python_tfg',
    'user': 'postgres',
    'password': 'ayneastq2219',
    'host': '156.35.95.39',
    'port': '5432',
}

def writeOnDB(sql_nodes_insert, datos_nodes_a_insertar, sql_insert, datos_a_insertar):
    # Establecer la conexión a la base de datos
    
    # Ejemplo de inserción de datos

    insertedPerConnexion = 50
    final_sql_insert = sql_insert + sql_nodes_insert
    final_datos_a_insertar = datos_a_insertar + datos_nodes_a_insertar
    for node in final_datos_a_insertar:
        if(node[0] == 161): 
            print('a')
    currentInserted = 0
    try:
        conexion = psycopg2.connect(**conexion_params)
        cursor = conexion.cursor()
        size = len(final_sql_insert)
        # Ejecutar la consulta
        for i in range(size):
            cursor.execute(final_sql_insert[size - i - 1], final_datos_a_insertar[size - i - 1])
            currentInserted += 1
            if(currentInserted == insertedPerConnexion):
                conexion.commit()
                currentInserted = 0

        # Confirmar la transacción
        conexion.commit()

    except Exception as e:
        # Manejar cualquier error
        print(f"Error: {e.with_traceback(None)}")
        print(final_datos_a_insertar[size - i - 1])
        print(final_sql_insert[size - i - 1])
        conexion.rollback()

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conexion.close()

def init_db():
    # Establecer la conexión a la base de datos
    conexion = psycopg2.connect(**conexion_params)

    # Crear un objeto cursor
    cursor = conexion.cursor()
    try:
        with open("./python_tfg/db/script_bd.sql", "r") as script_file:
            script = script_file.read()
        cursor.execute(script)

        # Confirmar la transacción
        conexion.commit()

    except Exception as e:
        # Manejar cualquier error
        print(f"Error: {e}")
        conexion.rollback()

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conexion.close()

def getCurrentID():
    # Establecer la conexión a la base de datos
    conexion = psycopg2.connect(**conexion_params)

    # Crear un objeto cursor
    cursor = conexion.cursor()
    currentID = -1
    try:
        # Ejecutar la consulta
        cursor.execute("SELECT MAX(node_id) FROM NODES;")
        aux = cursor.fetchone()[0]
        currentID = aux if aux else 0
        # Confirmar la transacción
        conexion.commit()
    except Exception as e:
        # Manejar cualquier error
        print(f"Error: {e.with_traceback(None)}")
        conexion.rollback()
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conexion.close()
        return currentID