import psycopg2

# Parámetros de conexión a la base de datos
conexion_params = {
    'dbname': 'python_tfg',
    'user': 'postgres',
    'password': 'ayneastq2219',
    'host': '156.35.95.39',
    'port': '5432',
}

# Establecer la conexión a la base de datos
conexion = psycopg2.connect(**conexion_params)

# Crear un objeto cursor
cursor = conexion.cursor()

def writeOnDB(sql_insert, datos_a_insertar):
    # Ejemplo de inserción de datos
    try:
        size = len(sql_insert)
        # Ejecutar la consulta
        for i in range(size):
            cursor.execute(sql_insert[size - i - 1], datos_a_insertar[size - i - 1])

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

def init_db():
    try:
        with open("visitors/script_bd.sql", "r") as script_file:
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