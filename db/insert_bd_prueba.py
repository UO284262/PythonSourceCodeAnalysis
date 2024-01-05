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

# Ejemplo de inserción de datos
try:
    # Definir la consulta SQL para la inserción
    sql_insert = "INSERT INTO module (prueba) VALUES (%s);"

    # Datos a insertar
    datos_a_insertar = ('valor1',)

    # Ejecutar la consulta
    cursor.execute(sql_insert, datos_a_insertar)

    # Confirmar la transacción
    conexion.commit()

    print("Datos insertados correctamente.")

except Exception as e:
    # Manejar cualquier error
    print(f"Error: {e}")
    conexion.rollback()

finally:
    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()