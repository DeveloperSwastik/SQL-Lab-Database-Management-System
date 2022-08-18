import argparse
import getpass
import json
import os
import random
import string
import sys
import time
from datetime import datetime

import data_encription as de
import file_branching_module as fbm
import query_handler as qh
import select_output as so
import working_with_system_db as wwsdb


def about_display():
    about_test = [
        "~"*58,
        " #####     ###    #             #           #     #####   ",
        "#     #   #   #   #             #          # #    #    #  ",
        "#        #     #  #             #         #   #   #     # ",
        " #####   #     #  #             #        #     #  ######  ",
        "      #  #   # #  #             #        #######  #     # ",
        "#     #   #   #   #             #        #     #  #    #  ",
        " #####     ### #  #######       #######  #     #  #####   ",
        "~"*58,
        "Software Name : SQL Lab",
        "Type          : Application",
        "Version       : 1.0.0",
        "Licence       : BSD 3-Clause License",
        "Developer     : Swastik Sharma",
        "",
        "Copyright (c) 2022, Swastik Sharma",
        "All rights reserved.",
        "~"*58,
    ]

    i = 0

    while (
        i < len(about_test)
    ):
        print(about_test[i], flush=True)

        if i < 6:
            time.sleep(0.2)
        else:
            time.sleep(0.3)

        i += 1

    sys.exit()


def verify(link):
    global current_connection_details, current_user_details
    link_verified = False
    orignal_link = link
    link = link.strip().split('.')

    if (
        len(link) == 7 and link[0] == 'sqllab' and
        link[1] == 'system' and link[6] == 'uacl'
    ):
        connection_type = de.convert_hashes_to_orignal_data(link[2])
        user_name = de.convert_modifide_data_to_orignal_data(link[3])

        if connection_type == 'Anonymous' or connection_type == 'General':

            if connection_type == 'Anonymous':
                path_of_cre_folder = (
                    f'{path_1}anonymous_{link[3]}_folder'
                )
                username_file = 'anonymous_user_names.json'
            elif connection_type == 'General':
                path_of_cre_folder = (
                    f'{path_1}{link[3]}_folder'
                )
                username_file = 'user_names.json'

            try:

                with open(
                    f'{path_1}{username_file}'
                ) as file:
                    user_names = json.load(file)

            except json.decoder.JSONDecodeError:
                user_names = {de.USER_NAME: []}

            for user_name_ in user_names[de.USER_NAME]:

                if (
                    de.convert_modifide_data_to_orignal_data(
                        user_name_
                    ) == user_name
                ):
                    try:

                        with open(
                            f'{path_of_cre_folder}\\'
                            'user_connections.json'
                        ) as file:
                            connection_details = json.load(file)

                    except json.decoder.JSONDecodeError:
                        connection_details = {}

                    if not len(connection_details):
                        print('The entered UACL is invalid.')
                    else:
                        _ = de.convert_modifide_data_to_orignal_data
                        __ = de.convert_orignal_data_to_modifide_data

                        for uacls in connection_details[de.UACL]:

                            if (
                                de.convert_hashes_to_orignal_data(uacls)
                                == orignal_link
                            ):
                                index = connection_details[de.UACL].index(
                                    uacls
                                )
                                link_verified = True

                                current_connection_details = [
                                    de.convert_hashes_to_orignal_data(
                                        connection_details[
                                            de.CONNECTION_NAME
                                        ][index]
                                    ).capitalize(),
                                    de.convert_hashes_to_orignal_data(
                                        connection_details[
                                            de.CONNECTION_TYPE
                                        ][index],
                                    ),
                                    _(
                                        connection_details[de.USER][index]
                                    ).capitalize(),
                                    de.convert_hashes_to_orignal_data(
                                        connection_details[de.ID][index]
                                    ),
                                    de.convert_hashes_to_orignal_data(
                                        connection_details[
                                            de.SCHEMA
                                        ][index]
                                    ),
                                    connection_details[de.USER][index],
                                    __(
                                        de.convert_hashes_to_orignal_data(
                                            connection_details[
                                                de.SCHEMA
                                            ][index],
                                        )
                                    )
                                ]
                                break

                        else:
                            print('The entered UACL is invalid.')

                    break

            else:
                print('The entered - UACL is invalid.')

        else:
            print('The entered connection type is invalid.')

    else:
        print('The entered UACL is invalid.')

    if link_verified:
        os.system('cls')
        current_user_details = [
            current_connection_details[5],
            current_connection_details[2],
            current_connection_details[1]
        ]
        add_user_action_info(
            'Connect with database by connection "'
            f'{current_connection_details[0]}" using SQL Lab Shell.',
            'Action completed successfully.'
        )
        print(
            '\nWelcome to the SQL Lab Shell.\n'
            'Your SQL Lab connection id is '
            f'{current_connection_details[3]}\n'
            'Shell version: 1.0.0\n\n'

            'Copyright (c) 2022, '
            'Swastik sharma.\n\n'

            "Type 'quit;' to end connection.\n"
            "Type 'clear;' to clear screen.\n"
            "Commands end with ';'.\n"
        )

        with open(
            f'{path_1}{link[3]}_folder\\user_credential.json'
        ) as file:
            profile = de.convert_hashes_to_orignal_data(
                json.load(file)[de.PROFILE]
            )

        quer_input_loop(
            current_connection_details[2], profile
        )


def quer_input_loop(user_name, profile):
    query = ''

    while(
        not query.startswith('quit')
    ):
        query = qh.input_query(user_name.replace(' ', ''), profile)

        if query.startswith('clear'):
            os.system('cls')
        elif query.startswith('help'):
            print(
                '\nList of all SQL Lab Shell commands:\n'
                "Note that all text commands must be "
                "first on line and end with ';'\n\n"
                "quit      : Quit SQL Lab Shell.\n"
                "help      : Display this help.\n"
                "clear     : Clear the screen.\n"
            )
        elif not query.startswith('quit'):
            raw_queries = query.strip().split(';')

            queries = [
                f'{raw_query.strip().lower()};'
                for raw_query in raw_queries
                if raw_query != ''
            ]

            for query_ in queries:
                executable_query = query_.replace('"', "'").strip()
                output = wwsdb.execute_query(
                    executable_query, current_connection_details
                )
                print(
                    f'\nAction/Task: {output[1]};'
                    f'\nMessage    : {output[2]}'
                    f'\nDuration   : {output[3]}\n'
                )

                if output[2] != 'Query executed successfully':
                    break

    if query.startswith('quit'):
        add_user_action_info(
            'Disconnect from SQL Lab Shell.',
            'Action not completed successfully.'
        )
        print("\n<- BYE ->\n")
        sys.exit()


def punctuation_checker(_string_, conditional_number=0):
    punctuation = list(map(str, string.punctuation))

    if conditional_number:
        punctuation.remove('_')
    else:
        pass

    for element in _string_:

        if punctuation.count(element):
            punctuation_found = True
            break

    else:
        punctuation_found = False

    return punctuation_found


def add_user_action_info(action, message):
    action_details = {}

    if current_user_details[2].lower() == "anonymous":
        profile = "anonymous_"
    else:
        profile = ""

    try:
        with open(
            f"{path_1}{profile}{current_user_details[0]}_folder\\"
            "Upanel_folder\\user_actions.json"
        ) as file:
            action_details = json.load(file)

    except json.decoder.JSONDecodeError:
        pass

    if not len(action_details):
        action_details[de.DATE] = [
            de.convert_orignal_data_to_hashes(
                datetime.now().strftime('%d %b, %Y')
            )
        ]
        action_details[de.TIME] = [
            de.convert_orignal_data_to_hashes(
                datetime.now().strftime('%X')
            )
        ]
        action_details[de.ACTION] = [
            de.convert_orignal_data_to_hashes(
                action
            )
        ]
        action_details[de.MESSAGE] = [
            de.convert_orignal_data_to_hashes(
                message
            )
        ]
    else:
        action_details[de.DATE].append(
            de.convert_orignal_data_to_hashes(
                datetime.now().strftime('%d %b, %Y')
            )
        )
        action_details[de.TIME].append(
            de.convert_orignal_data_to_hashes(
                datetime.now().strftime('%X')
            )
        )
        action_details[de.ACTION].append(
            de.convert_orignal_data_to_hashes(
                action
            )
        )
        action_details[de.MESSAGE].append(
            de.convert_orignal_data_to_hashes(
                message
            )
        )

    with open(
        f"{path_1}{profile}{current_user_details[0]}_folder\\"
        "Upanel_folder\\user_actions.json", 'w'
    ) as file:
        json.dump(action_details, file)


current_connection_details = [
    None, None, None, None, None, None, None
]
current_user_details = []
login_attempts = 0
path_1 = fbm.PATH_OF_CREDENTIALS_FOLDER_OF_USERS
path_2 = fbm.PATH_OF_USER_DATABASE_FOLDERS
path_3 = fbm.PATH_OF_CREDENTIALS_FOLDER_OF_ADMIN

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=('SQL LAB SHELL')
    )

    parser.version = (
        'SQL Lab Version: 1.0.0'
    )

    parser.add_argument(
        '--u', '--user', type=str,
        help='This argument take user name as input.'
    )

    parser.add_argument(
        '--uacl', '--universally-authenticated-connection-link', type=str,
        help=(
            'This argument take Universally '
            'Authenticated Connection Link as input.'
        )
    )

    parser.add_argument(
        '--version', action="version",
        help="This argument show the current version of utility",
    )

    parser.add_argument(
        '--about', action="store_true",
        help="This argument show the current version of utility",
    )

    arguments = parser.parse_args()

    os.system('title SQL Lab Shell')

    if arguments.about:
        about_display()

    if arguments.uacl:
        verify(arguments.uacl)
        sys.exit()

    if arguments.u:
        user_name = arguments.u.lower().replace(' ', '')
        profile = getpass.getpass(
            'Enter user profile (Standard/Guest/Anonymous) :'
        ).strip().lower()
        user_name_list = {}

        try:

            if profile != 'anonymous':

                with open(
                    f"{path_1}user_names.json", 'r'
                ) as file:
                    user_name_list = json.load(file)

            else:

                with open(
                    f"{path_1}anonymous_user_names.json", 'r'
                ) as file:
                    user_name_list = json.load(file)

        except json.decoder.JSONDecodeError:
            user_name_list[de.USER_NAME] = []

        profile = profile.lower().replace(' ', '')

        profile_type_exists = [
            profile == 'standard',
            profile == 'anonymous',
            profile == 'guest'
        ]

        user_name_present = user_name_list[de.USER_NAME].count(user_name)

        if len(user_name) > 70:
            print(
                'The entered user name cross the maximum lenght of 70 words'
            )
        elif punctuation_checker(user_name):
            print(
                'The entered user name contain puntuation '
                'marks or special symbol which is not allowed'
            )
        elif not any(profile_type_exists):
            print(
                'The entered profile type not exists'
            )
        else:
            user_name_list = {}
            user_name = de.convert_orignal_data_to_modifide_data(user_name)

            try:

                if profile != 'anonymous':

                    with open(
                        f"{path_1}user_names.json", 'r'
                    ) as file:
                        user_name_list = json.load(file)

                else:

                    with open(
                        f"{path_1}anonymous_user_names.json", 'r'
                    ) as file:
                        user_name_list = json.load(file)

            except json.decoder.JSONDecodeError:
                user_name_list[de.USER_NAME] = []

            user_name_present = user_name_list[de.USER_NAME].count(user_name)

            if user_name_present:
                credentials = {}

                if profile == 'anonymous':

                    with open(
                        f"{path_1}anonymous_{user_name}_folder\\"
                        "user_credential.json", 'r'
                    ) as file:
                        credentials = json.load(file)

                else:

                    with open(
                        f"{path_1}{user_name}_folder\\user_credential.json",
                        'r'
                    ) as file:
                        credentials = json.load(file)

                orignal_user_name = arguments.u
                password_of_user = credentials[de.PASSWORD]
                user_profile = de.convert_hashes_to_orignal_data(
                    credentials[de.PROFILE]
                ).lower().replace(' ', '')

                while(
                    orignal_user_name.count('  ')
                ):
                    orignal_user_name = orignal_user_name.replace('  ', ' ')

                orignal_user_name = orignal_user_name.capitalize()

                if profile == user_profile:

                    for i in range(3):
                        password = getpass.getpass(
                            'Enter password :'
                        )
                        
                        wrong_pass = False

                        try:
                            de.convert_orignal_data_to_hashes(password)
                        except KeyError:

                            if login_attempts < 2:
                                print(
                                    "The entered password didn't match."
                                )
                            else:
                                print(
                                    "You cross maximum login attempt limit. "
                                    "You are not an authenticate user.\n"
                                    "Note: Information about unauthenticate "
                                    "attempts of login is send to user."
                                )
                                login_attempts = -1

                                current_user_details = [
                                    user_name, orignal_user_name, profile,
                                ]

                                add_user_action_info(
                                    'Connect with database using '
                                    'SQL Lab Shell.',
                                    'Action not completed '
                                    'successfully.'
                                )

                                current_user_details = []

                            login_attempts += 1

                            continue

                        if (
                            de.convert_orignal_data_to_hashes(
                                password
                            ) == password_of_user
                        ):
                            current_user_details = [
                                user_name, orignal_user_name, profile,
                            ]
                            add_user_action_info(
                                'Connect with database using '
                                'SQL Lab Shell.',
                                'Action completed successfully.'
                            )
                            database_not_existes = True

                            if profile == 'anonymous':
                                list_of_db = os.listdir(
                                    f'{path_2}anonymous_{user_name}'
                                    '_database_folder'
                                )
                            else:
                                list_of_db = os.listdir(
                                    f'{path_2}{user_name}_database_folder'
                                )

                            print(
                                "Use 'show databases' "
                                "use see list of databases"
                            )

                            while(
                                database_not_existes
                            ):
                                database = input(
                                    'Enter database name you want to use :'
                                ).lower()
                                _ = de.convert_modifide_data_to_orignal_data
                                __ = de.convert_orignal_data_to_modifide_data

                                if database == 'show databases':
                                    print()
                                    so.select_output(
                                        ['Databases'],
                                        [
                                            [_(db.rstrip('.sqllab'))]
                                            for db in list_of_db
                                        ]
                                    )
                                    print()
                                elif punctuation_checker(database, 1):
                                    print('\nDatabase not exists.\n')
                                else:
                                    orignal_db_name = database
                                    database = database.replace(' ', '')
                                    database = (
                                        __(database)
                                    )

                                    if list_of_db.count(f'{database}.sqllab'):
                                        database_not_existes = False

                                        current_connection_details = [
                                            None, profile, orignal_user_name,
                                            None, orignal_db_name, user_name,
                                            database
                                        ]

                                        os.system('cls')
                                        print(
                                            '\nWelcome to the SQL Lab Shell.\n'
                                            'Your SQL Lab connection id is '
                                            f'{int(random.randrange(10,99))}\n'
                                            'Shell version: 1.0.0\n\n'

                                            'Copyright (c) 2022, '
                                            'Swastik sharma.\n\n'

                                            "Type 'quit;' to end connection.\n"
                                            "Type 'clear;' to clear screen.\n"
                                            "Commands end with ';'.\n"
                                        )

                                        quer_input_loop(
                                            orignal_user_name, profile
                                        )
                                    else:
                                        print('\nDatabase not exists.\n')

                        else:

                            if login_attempts < 2:
                                print(
                                    "The entered password didn't match."
                                )
                            else:
                                print(
                                    "You cross maximum login attempt limit. "
                                    "You are not an authenticate user.\n"
                                    "Note: Information about unauthenticate "
                                    "attempts of login is send to user."
                                )
                                login_attempts = -1

                                current_user_details = [
                                    user_name, orignal_user_name, profile,
                                ]

                                add_user_action_info(
                                    'Connect with database using '
                                    'SQL Lab Shell.',
                                    'Action not completed '
                                    'successfully.'
                                )

                                current_user_details = []

                            login_attempts += 1
                else:
                    print(
                        "The entered user name didn't exists"
                    )
            else:
                print(
                    "The entered user name didn't exists"
                )

    if (
        arguments.u == None
        and
        arguments.uacl == None
        and
        arguments.about == False
    ):
        print(
            "\n",
            "-"*57,
            "\nArgumentNotPassError: You doesn't pass any argument .....\n",
            "-"*57,
            "\n", sep=""
        )
