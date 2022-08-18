import os
import json
import datetime
import data_encription as de


def create_main_folder():
    try:
        os.mkdir(
            f"{ROOT_DIR}SQL LAB"
        )
    except FileExistsError:
        pass
    os.system(f'attrib +h "{ROOT_DIR}SQL LAB"')


def create_sub_folders_of_main_folder():
    try:
        os.mkdir(
            f"{ROOT_DIR}SQL LAB\\System_folder"
        )
    except FileExistsError:
        pass

    try:
        os.mkdir(
            f'{PATH_OF_USER_DATABASE_FOLDERS}'
        )
    except FileExistsError:
        pass


def create_sub_folders_of_system_folder():
    try:
        os.mkdir(
            f"{ROOT_DIR}SQL LAB\\System_folder\\"
            "Credentials_of_standard_anonymous_guest_account"
        )
    except FileExistsError:
        pass

    try:
        os.mkdir(
            f"{ROOT_DIR}SQL LAB\\System_folder\\"
            "Credentials_of_adminstrator_account"
        )
    except FileExistsError:
        pass


def create_sub_folders_of_Credentials_of_standard_anonymous_guest_account():
    try:
        os.mkdir(
            PATH_OF_CREDENTIALS_FOLDER_OF_USERS
        )
    except FileExistsError:
        pass


def create_sub_folders_of_user_folder(
    type_of_account="standard", user_name="test_user"
):
    if type_of_account == "anonymous":
        try:
            os.mkdir(
                f'{PATH_OF_USER_DATABASE_FOLDERS}'
                f"anonymous_{user_name}_database_folder"
            )
        except FileExistsError:
            pass
    else:
        try:
            os.mkdir(
                f'{PATH_OF_USER_DATABASE_FOLDERS}'
                f"{user_name}_database_folder"
            )
        except FileExistsError:
            pass


def create_files_for_credential_of_adminstrator_account_folder():
    FILES_NAME_LIST = [
        "admin_credential.json"
    ]

    for file_name in FILES_NAME_LIST:
        file = open(
            f"{PATH_OF_CREDENTIALS_FOLDER_OF_ADMIN}{file_name}", "a"
        )


def create_files_for_credential_of_user_account_folder():
    FILES_NAME_LIST = [
        "user_names.json", "anonymous_user_names.json"
    ]

    for file_name in FILES_NAME_LIST:
        file = open(
            f"{PATH_OF_CREDENTIALS_FOLDER_OF_USERS}{file_name}", "a"
        )


def create_files_and_folder_of_particular_user_account(
    user_name="test_user", type="standard"
):
    FILES_NAME_LIST = [
        'user_credential.json', 'user_connections.json'
    ]
    if type == "anonymous":
        user_name = "anonymous_" + user_name

    try:
        os.mkdir(
            f'{PATH_OF_CREDENTIALS_FOLDER_OF_USERS}{user_name}_folder')
    except FileExistsError:
        pass

    try:
        os.mkdir(
            f"{PATH_OF_CREDENTIALS_FOLDER_OF_USERS}{user_name}"
            "_folder\\Upanel_folder"
        )
    except FileExistsError:
        pass

    for file_name in FILES_NAME_LIST:
        file = open(
            f"{PATH_OF_CREDENTIALS_FOLDER_OF_USERS}{user_name}"
            f"_folder\\{file_name}", "a"
        )

    file = open(
        f"{PATH_OF_CREDENTIALS_FOLDER_OF_USERS}{user_name}"
        f"_folder\\Upanel_folder\\user_actions.json", "a"
    )


def add_credentials_of_administrator():
    data = {
        de.USER_NAME: de.convert_orignal_data_to_hashes('admin'),
        de.PASSWORD: de.convert_orignal_data_to_hashes('root'),
        de.PROFILE: de.convert_orignal_data_to_hashes('Adminstrator'),
        de.DATE: de.convert_orignal_data_to_hashes(
            datetime.datetime.now().strftime('%d %b, %Y')
        ),
        de.TIME: de.convert_orignal_data_to_hashes(
            datetime.datetime.now().strftime('%X')
        )
    }

    try:

        with open(
            f"{PATH_OF_CREDENTIALS_FOLDER_OF_ADMIN}admin_credential.json"
        ) as file:
            json.load(file)

    except json.decoder.JSONDecodeError:

        with open(
            f"{PATH_OF_CREDENTIALS_FOLDER_OF_ADMIN}admin_credential.json", 'w'
        ) as file:
            json.dump(data, file)


FUNCTION_FLOW = [
    create_main_folder, create_sub_folders_of_main_folder,
    create_sub_folders_of_system_folder,
    create_sub_folders_of_Credentials_of_standard_anonymous_guest_account,
    create_files_for_credential_of_adminstrator_account_folder,
    add_credentials_of_administrator,
    create_files_for_credential_of_user_account_folder
]

ROOT_DIR = "C:\\"

PATH_OF_CREDENTIALS_FOLDER_OF_USERS = (
    f"{ROOT_DIR}SQL LAB\\System_folder\\Credentials_of_standard_anonymous_"
    "guest_account\\"
)

PATH_OF_CREDENTIALS_FOLDER_OF_ADMIN = (
    f"{ROOT_DIR}SQL LAB\\System_folder\\"
    "Credentials_of_adminstrator_account\\"
)

PATH_OF_USER_DATABASE_FOLDERS = (
    f"{ROOT_DIR}SQL LAB\\User_folder\\"
)

for function in FUNCTION_FLOW:
    function()
