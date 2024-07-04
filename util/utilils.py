import json

observation__ = "start"

def write_progress(text):
    global observation__
    observation__ = text
    
def return_obser():
    return observation__


def open_file(name, type_file):
    """
        Cette fonction prend deux parametres : le nom et le type du fichier et procede a l'ouverture du fichier
        Args:
            name (str) premier parametre
            type_file (str) second parametre
            
        Return:
            (str or dict or list...) 
    """
    with open(f"{name}.{type_file}", encoding='utf-8') as file:
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
            with open(f"{name}.{type_file}", 'w', encoding='utf-8') as file:
                if type_file == 'txt':
                    file.write(data)
                else:
                    json.dump(data, file, indent = 4)
                file.close()
        except FileNotFoundError as e:
            print(e)
                    