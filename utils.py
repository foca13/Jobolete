import os
import json

def save_content_to_file(content, path, mode='w'):
    """ CAT: Guarda el contingut d'entrada en un arxiu en mode binari o text
        EN: Saves the input content into a file as binary or text mode
       
        arguments: content (str), path (str), mode (char or str: 'r', 'r+', 'w', 'w+', 'a', 'a+', 'rb', 'wb'. Default: 'w')
    """
    
    with open(path, mode) as file:
        file.write(content)

def makedir(path):
    """ CAT: Crea un directori si no existeix
        EN: Creates a directory if it doesn't exist
        
        arguments: path (str)
    """
    
    if not os.path.exists(path):
        os.mkdir(path)

def read_json_file(path, mode='r'):
    """ CAT: llegeix un arxiu en format JSON
        EN: reads a file in JSON format
        
        arguments: path (str), mode (char or str: 'r', 'r+', 'w', 'w+', 'a', 'a+', 'rb', 'wb'. Default: 'r')
        returns: contents of the JSON file
    """
    
    with open(path, mode) as file:
        return json.load(file)

def read_file(path, mode='r'):
    """ CAT: llegeix un arxiu en format .txt
        EN: reads a file in .txt format
        
        arguments: path (str), mode (char or str: 'r', 'r+', 'w', 'w+', 'a', 'a+', 'rb', 'wb'. Default: 'r')
        returns: contents of the .txt file
    """
    
    with open(path, mode) as file:
        return file.read()