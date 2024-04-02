import psycopg2

connection_string = {
    'dbname': 'python_tfg',
    'user': 'postgres',
    'password': 'ayneastq2219',
    'host': '156.35.95.39',
    'port': '5432',
}


def write_on_db(sql_nodes_to_insert, nodes_data_to_insert, sql_insert, data_to_insert, modules):
    inserts_size = 50
    final_sql_insert = sql_insert + sql_nodes_to_insert
    final_data_to_insert = data_to_insert + nodes_data_to_insert
    current_inserted = 0
    try:
        connection = psycopg2.connect(**connection_string)
        cursor = connection.cursor()
        size = len(final_sql_insert)
        # Execute query
        for i in range(size):
            cursor.execute(final_sql_insert[size - i - 1], final_data_to_insert[size - i - 1])
            current_inserted += 1
            if current_inserted == inserts_size:
                connection.commit()
                current_inserted = 0
        # Close cursor and connection
        connection.commit()

    except Exception as e:
        # Error handler
        print(f"Error: {e.with_traceback(None)}")
        print(final_data_to_insert[size - i - 1])
        print(final_sql_insert[size - i - 1])
        print(modules[size - i - 1])
        connection.rollback()

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()


def init_db():
    connection = psycopg2.connect(**connection_string)
    cursor = connection.cursor()
    try:
        with open("./python_tfg/db/script_bd.sql", "r") as script_file:
            script = script_file.read()
        cursor.execute(script)
        # Commit transaction
        connection.commit()

    except Exception as e:
        # Error handler
        print(f"Error: {e}")
        connection.rollback()

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()


def get_db_current_id() -> int:
    connection = psycopg2.connect(**connection_string)
    cursor = connection.cursor()
    current_id = -1
    try:
        # Execute query
        cursor.execute("SELECT MAX(node_id) FROM NODES;")
        aux = cursor.fetchone()[0]
        current_id = aux if aux else 0
        # Commit transaction
        connection.commit()
    except Exception as e:
        # Error handler
        print(f"Error: {e.with_traceback(None)}")
        connection.rollback()
    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()
        return current_id
