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

        # Ejecutar la consulta
        for i in range(len(sql_insert)):
            cursor.execute(sql_insert[i], datos_a_insertar[i])

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

def init_db():
    try:
        with open("script_db.sql", "r") as script_file:
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