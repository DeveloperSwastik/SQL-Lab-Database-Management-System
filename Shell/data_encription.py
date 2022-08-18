VALUES = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
    "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
    "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
    "T", "U", "V", "W", "X", "Y", "Z", "!", "#", "$", "%", "&", "'", "_", '"',
    "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@",
    "[", "]", "^", "`", "{", "|", "}", "~", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "0", " ", "\\", "\n"
]

REVERSE_OF_VALUES = VALUES[::-1]

VALUES_B = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
    "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
    "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
    "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8",
    "9", "0", "_"
]

REVERSE_OF_VALUES_B = [
    'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c',
    '0', '9', '8', '7', '6', '5', '4', '3', '2', '1', 'Z', 'Y', 'X', 'W', 'V',
    'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', 'I', 'H', 'G',
    'F', 'E', 'D', 'C', 'B', 'A', 'z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r',
    'b', 'a', "_"
]

hashes = {}

temp_7 = 0
temp_6 = 0
temp_5 = 0
temp_4 = 0
temp_3 = 0
temp_2 = 0


def create_hashes():
    def first_digit():

        if VALUES.index(element) % 2 == 0:
            hash_value.insert(0, "0")
        else:
            hash_value.insert(0, "1")

    def secound_digit():
        global temp_2

        if temp_2 <= 1:
            hash_value.insert(0, "0")
            first_digit()
            temp_2 += 1
        elif temp_2 <= 3:
            hash_value.insert(0, "1")
            first_digit()
            temp_2 += 1

            if temp_2 == 4:
                temp_2 = 0

    def third_digit():
        global temp_3

        if temp_3 <= 3:
            hash_value.insert(0, "0")
            secound_digit()
            temp_3 += 1
        elif temp_3 <= 7:
            hash_value.insert(0, "1")
            secound_digit()
            temp_3 += 1

            if temp_3 == 8:
                temp_3 = 0

    def fourth_digit():
        global temp_4

        if temp_4 <= 7:
            hash_value.insert(0, "0")
            third_digit()
            temp_4 += 1
        elif temp_4 <= 15:
            hash_value.insert(0, "1")
            third_digit()
            temp_4 += 1

            if temp_4 == 16:
                temp_4 = 0

    def fifth_digit():
        global temp_5

        if temp_5 <= 15:
            hash_value.insert(0, "0")
            fourth_digit()
            temp_5 += 1
        elif temp_5 <= 31:
            hash_value.insert(0, "1")
            fourth_digit()
            temp_5 += 1

            if temp_5 == 32:
                temp_5 = 0

    def sixth_digit():
        global temp_6

        if temp_6 <= 31:
            hash_value.insert(0, "0")
            fifth_digit()
            temp_6 += 1
        elif temp_6 <= 63:
            hash_value.insert(0, "1")
            fifth_digit()
            temp_6 += 1

            if temp_6 == 64:
                temp_6 = 0

    def seventh_digit():
        global temp_7

        if temp_7 <= 63:
            hash_value.insert(0, "0")
            sixth_digit()
            temp_7 += 1
        elif temp_7 <= 127:
            hash_value.insert(0, "1")
            sixth_digit()
            temp_7 += 1

            if temp_7 == 128:
                temp_7 = 0

    count = 0

    for element in VALUES:
        hash_value = []
        seventh_digit()
        count += 1
        hash_value = "".join(hash_value)
        hashes[element] = hash_value


def convert_orignal_data_to_hashes(orignal_data):
    hashed_data = ""

    for element in orignal_data:
        hashed_value = hashes[element]
        hashed_data = f"{hashed_data}{hashed_value}"
    hashed_data = hashed_data.strip()

    return hashed_data


def convert_hashes_to_orignal_data(hashed_data):
    orignal_data = ""
    heshed_data_splited_values = []

    while len(hashed_data) != 0:
        heshed_data_splited_values.append(hashed_data[0:7])
        hashed_data = hashed_data[7:]

    for hash in heshed_data_splited_values:

        for hash_value in hashes:

            if hashes[hash_value] == hash:
                orignal_data = orignal_data + hash_value

    return orignal_data


def convert_orignal_data_to_modifide_data(oringanl_data):
    modified_data = ''

    for element in oringanl_data:
        modified_data += REVERSE_OF_VALUES_B[VALUES_B.index(element)]

    return modified_data


def convert_modifide_data_to_orignal_data(modified_data):
    oringanl_data = ''

    for element in modified_data:
        oringanl_data += VALUES_B[REVERSE_OF_VALUES_B.index(element)]

    return oringanl_data


create_hashes()

PASSWORD = convert_orignal_data_to_hashes('Password')
USER_NAME = convert_orignal_data_to_hashes('User Name')
PROFILE = convert_orignal_data_to_hashes('Profile')
DATE = convert_orignal_data_to_hashes('Date')
TIME = convert_orignal_data_to_hashes('Time')
CONNECTION_NAME = convert_orignal_data_to_hashes('Connection name')
CONNECTION_TYPE = convert_orignal_data_to_hashes('Connection type')
ID = convert_orignal_data_to_hashes('ID')
USER = convert_orignal_data_to_hashes('User')
SCHEMA = convert_orignal_data_to_hashes('Schema')
DESCRIPTION = convert_orignal_data_to_hashes('Description')
UACL = convert_orignal_data_to_hashes('UACL')
ACTION = convert_orignal_data_to_hashes('Action')
MESSAGE = convert_orignal_data_to_hashes('Message')