"""
Jai Riley -> jrbuhr
Mohammad Tavakoli -> tavakol5
"""

import requests
import csv

# API_KEY = "1b77e7f0-502e-4fa8-9936-886d7c21aa5e"
# API_KEY = "5feb7e35-df63-47cc-8580-2dd604a8a99e"
API_KEY = "c025306c-4a1f-4114-8110-f7709dc1b259"
TARGET_LANGUAGE = "EN"

data = []
data_without_nan = []


def get_wordnet_ids(babel_id: str):
    """
    Sends a request to babelnet api in order to retrieve synset of a babelId.
    Args:
    - babel_id (str): Babel_id.
    Returns:
    - list: A list containing WordNet IDs related to that babel ID.
    """
    # BabelNet API endpoint for retrieving WordNet IDs
    url = f'https://babelnet.io/v9/getSynset?id={babel_id}&key={API_KEY}&targetLang={TARGET_LANGUAGE}'

    try:
        # Make a GET request to the BabelNet API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP error
        data = response.json()  # Parse JSON response

        Word_Net_Ids = []
        for sense in data['senses']:
            if sense['properties']['source'] == "WN":
                Word_Net_Ids.append("wn:" + sense['properties']['senseKey'])
        return Word_Net_Ids
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def create_data():
    """
    Reads from farsi.key.txt file and adds WordNet IDs to a list.
    Args:
    - None.
    Returns:
    - None.
    """
    with open("farsi.key.txt", 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        count = 0

        for row in reader:
            print(count)
            count += 1
            data_temp = row[:-1]
            babel_id = data_temp[2]
            if babel_id != 'O':
                WordNet_Ids = get_wordnet_ids(babel_id)
                if WordNet_Ids == None:
                    data.append([data_temp[0], data_temp[1], data_temp[2], 'n/a'])
                    data_without_nan.append([data_temp[0], data_temp[1], data_temp[2], 'n/a'])
                else:
                    data_temp += WordNet_Ids
                    data.append(data_temp)
                    data_without_nan.append(data_temp)
            else:
                data.append([data_temp[0], data_temp[1], 'n/a', 'n/a'])


def create_key_file(filename: str, data: list):
    """
    This function, creates a .key file.
    Args:
    - filename (str): The path to the .key file to be written.
    - data (list): The data we want to store.
    Returns:
    - None.
    """
    try:
        with open(filename, 'w') as key_file:
            for row in data:
                main_value = ""
                for value in row:
                    main_value += value + "\t"
                main_value = main_value.strip()
                main_value += "\n"
                key_file.write(main_value)
        print(f"Key file '{filename}' created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_text_file(filename: str, data: list):
    """
    This function, creates a .text file.
    Args:
    - filename (str): The path to the .text file to be written.
    - data (list): The data we want to store.
    Returns:
    - None.
    """
    try:
        with open(filename, 'w') as key_file:
            for row in data:
                main_value = ""
                for value in row:
                    main_value += value + "\t"
                main_value = main_value.strip()
                main_value += "\n"
                key_file.write(main_value)
        print(f"Key file '{filename}' created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_key_file_line_by_line(filename: str):
    """
    This function, reads from a .key file.
    Args:
    - filename (str): The path to the .key file to be written.
    Returns:
    - lines (list): Content of a .key file.
    """
    try:
        lines = []
        with open(filename, 'r') as key_file:
            for line in key_file:
                lines.append(line)
        return lines
    except Exception as e:
        print(f"An error occurred while reading the key file: {e}")
        return None


create_data()

create_key_file(filename="Farsi.key", data=data)
create_text_file(filename="Farsi.text", data=data)
create_key_file(filename="Farsi_2.key", data=data_without_nan)
create_text_file(filename="Farsi_2.text", data=data_without_nan)
