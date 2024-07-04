import os
import sys
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(chemin_parent)

import json

def open_file(name, type_file):
    """
        Cette fonction prend deux parametres : le nom et le type du fichier et procede a l'ouverture du fichier
        Args:
            name (str) premier parametre
            type_file (str) second parametre
            
        Return:
            (str or dict or list...) 
    """
    with open(f"{chemin_parent}\data\{name}.{type_file}", encoding='utf-8') as file:
        if type_file == 'txt': # Verifie si le fichier est du type txt
            data = file.read()
            file.close()
            return data
        else:                   # Sinon il suppose que c'est un Json
            data = json.load(file)
            file.close()
            return data
        
        
def save_file(name : str, type_file : str, data) -> None:
        try:
            with open(f"{chemin_parent}\data\{name}.{type_file}", 'w', encoding='utf-8') as file:
                if type_file == 'txt':
                    file.write(data)
                else:
                    json.dump(data, file, indent = 4)
                file.close()
        except FileNotFoundError as e:
            print(e)
                    