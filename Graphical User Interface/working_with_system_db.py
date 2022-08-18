import datetime
import os
import sqlite3
import time

import file_branching_module as fbm
import select_pop_up


def path_generater():
    connection_type = current_connection_details[1].lower()
    user = current_connection_details[5]
    database_name = current_connection_details[6]

    if connection_type == 'anonymous':
        path = (
            f'{fbm.PATH_OF_USER_DATABASE_FOLDERS}'
            f'anonymous_{user}_database_folder\\{database_name}.sqllab'
        )
    else:
        path = (
            f'{fbm.PATH_OF_USER_DATABASE_FOLDERS}'
            f'{(user)}_database_folder\\{database_name}.sqllab'
        )

    return path


def connection():
    path_of_db = path_generater()
    connectionObject = sqlite3.connect(path_of_db)
    cursor = connectionObject.cursor()

    return connectionObject, cursor


def fetch_table_info(connection_detail):
    global current_connection_details

    current_connection_details = connection_detail

    connection_obj, cursor = connection()

    fetch_info = cursor.execute(
        '''
            SELECT tbl_name, rootpage FROM sqlite_master 
            WHERE type='table'
            ORDER BY tbl_name;
        '''
    ).fetchall()

    table_info = [
        [
            fetch_info.index(element) + 1,
            element[0].capitalize(),
            len(
                cursor.execute(
                    f'''
                        SELECT c.name FROM pragma_table_info('{element[0]}') c
                    '''
                ).fetchall()
            )
        ]
        for element in fetch_info
    ]

    cursor.close()
    connection_obj.close()

    return table_info


def fetch_schema_info(connection_detail):
    global current_connection_details

    current_connection_details = connection_detail

    path = path_generater()
    databases_details = [
        ['Database name', current_connection_details[4].capitalize()],
        [
            'Date of creation',
            ' '.join(
                time.ctime(
                    os.path.getctime(
                        path
                    )
                ).split()[1:3]
            ) + "," +
            time.ctime(
                os.path.getctime(
                    path
                )
            ).split()[4]
        ],
        [
            'Last date of modification',
            ' '.join(
                time.ctime(
                    os.path.getmtime(
                        path
                    )
                ).split()[1:3]
            ) + "," +
            time.ctime(
                os.path.getmtime(
                    path
                )
            ).split()[4]
        ],
        ['Size', f"{(os.path.getsize(path)/1000):.2f}" + " Kb"]
    ]

    return databases_details


def execute_query(query, connection_detail):
    global current_connection_details

    current_connection_details = connection_detail
    orignal_query = query
    error_not_found = False
    connection_obj, cursor = connection()
    process_start_time = datetime.datetime.now().strftime('%H:%M:%S')

    if (
        query == 'desc database;'
        or
        query == 'DESC DATABASE;'
    ):
        query = (
            'select type, tbl_name as Name, sql from sqlite_master '
            'where sql is not null;'
        )

    if (
        query.startswith('desc table')
        or
        query.startswith('DESC TABLE')
    ):
        table_name = query.rstrip(';').split()[2].lower()
        query = f"PRAGMA table_info('{table_name}');"

    if (
        query.startswith('truncate table')
        or
        query.startswith('TRUNCATE TABLE')
    ):
        table_name = query.rstrip(';').split()[2].lower()
        query = f"delete from {table_name};"

    if query.startswith('PRAGMA'):

        try:
            table_found = [
                data[1].lower()
                for data in fetch_table_info(current_connection_details)
            ].count(table_name)

            if table_found:
                query_execution_start_time = time.time()

                cursor.execute(
                    f'''
                        {query}
                    '''
                )

                query_execution_end_time = time.time()

                time_of_execution = (
                    query_execution_end_time - query_execution_start_time
                )

                message = 'Query executed successfully'
                error_not_found = True
            else:
                time_of_execution = 0.00
                message = f'no such table: {table_name}'
                error_not_found = False

        except Exception as error:
            time_of_execution = 0.00
            message = error
            error_not_found = False

    elif (
        query.startswith('select')
    ):
        try:
            query_execution_start_time = time.time()

            cursor.execute(
                f'''
                    {query}
                '''
            )

            query_execution_end_time = time.time()

            time_of_execution = (
                query_execution_end_time - query_execution_start_time
            )

            message = 'Query executed successfully'
            error_not_found = True

        except Exception as error:
            time_of_execution = 0.00
            message = error
            error_not_found = False

    if (
        error_not_found
        and
        query.startswith('select')
    ):

        try:
            cursor.execute(
                '''
                    drop view sqllab_temporary_view;
                '''
            )
        except sqlite3.OperationalError:
            pass

        cursor.execute(
            f'''
                CREATE VIEW sqllab_temporary_view AS
                {query}
            '''
        )

        columns_name = cursor.execute(
            '''
                SELECT c.name FROM pragma_table_info
            '''
            '''
                ('sqllab_temporary_view') c
            '''
        ).fetchall()
        columns_name = [element[0] for element in columns_name]

        fetch_data = cursor.execute(
            '''
                SELECT * FROM sqllab_temporary_view;
            '''
        ).fetchall()

        if (
            orignal_query == 'desc database;'
            or
            orignal_query == 'DESC DATABASE;'
        ):
            fetch_data = [
                list(element) for element in fetch_data
                if element[0] != 'view' and
                element[1] != 'sqllab_temporary_view'
            ]

        cursor.execute(
            '''
                drop view sqllab_temporary_view;
            '''
        )

        select_pop_up.select_output(columns_name, fetch_data)

    elif error_not_found and (
        orignal_query.startswith('desc table')
        or
        orignal_query.startswith('DESC TABLE')
    ):
        query_execution_start_time = time.time()

        table_info = cursor.execute(
            f'''
                {query}
            '''
        ).fetchall()

        fetch_table_info_ = [
            [data[1], data[2].upper(), str(data[4]).strip("'")]
            for data in cursor.execute(
                query
            ).fetchall()
        ]

        table_query = cursor.execute(
            "select sql from sqlite_master "
            f"where tbl_name = '{table_name}'"
        ).fetchall()[0][0].lower()

        for i in fetch_table_info_:

            if i[2].count(','):
                table_query = (
                    table_query.replace(
                        i[2].lower(), i[2].replace(',', ' ').lower()
                    ).replace('  ', ' ')
                )

        column_constraints = []

        table_query = table_query[table_query.index("(")+1:-1].split(",")

        for column in table_query:

            if column.count('default'):

                if column.count("'"):
                    column = (
                        column[:column.index("'") - 8] +
                        column[
                            column.index("'", column.index("'")+1)+1:
                        ]
                    ).replace('  ', ' ').split()
                    column.pop(0)
                    column.pop(0)
                else:
                    column = column.strip().split()
                    column.pop(column.index('default')+1)
                    column.pop(column.index('default'))
                    column.pop(0)
                    column.pop(0)

            else:
                column = column.strip().split()
                column.pop(0)
                column.pop(0)

            constraints = ""

            for i in column:
                constraints += i.capitalize() + " "

            column_constraints.append(constraints)

        table_info = [
            data_1 + [data_2]
            for data_1, data_2 in zip(
                fetch_table_info_, column_constraints
            )
        ]

        query_execution_end_time = time.time()

        columns_name = ['Field', 'Type', 'Default', 'Constraint']

        select_pop_up.select_output(columns_name, table_info)

        time_of_execution = (
            query_execution_end_time - query_execution_start_time
        )

        message = 'Query executed successfully'
        error_not_found = True
    elif (
        not error_not_found
        and
        not
        (
            orignal_query.startswith('desc table')
            or
            orignal_query.startswith('DESC TABLE')
        )
        and
        not
        (
            query.startswith('select')
        )
    ):
        try:
            query_execution_start_time = time.time()

            cursor.execute(
                f'''
                    {query}
                '''
            )
            connection_obj.commit()

            query_execution_end_time = time.time()

            time_of_execution = (
                query_execution_end_time - query_execution_start_time
            )

            message = 'Query executed successfully'
            error_not_found = True
        except Exception as error:
            time_of_execution = 0.00
            message = error
            error_not_found = False

    cursor.close()
    connection_obj.close()

    return [
        process_start_time, orignal_query.rstrip(';').capitalize(), message,
        f'{time_of_execution:.6f} sec'
    ]


current_connection_details = []
