import time
import json
import customtkinter as ctk
from data.manage_data import open_file

class Observer:
    def __init__(self, path_to_file) -> None:
        self.path_to_file = path_to_file
        self.break_loop = False

    def start(self, interface, reset_parameter):
        point = 1
        self.break_loop = False
        while not self.break_loop:
            result = open_file(self.path_to_file, 'json')
            result = result['observation']
            
            print(result)
            reset_parameter()
            temp = "." * point
            
            interface.tag_config("prog", foreground = "#FF7550")
            interface.insert(ctk.END, "  | Operation in progress : ", "prog")

            interface.insert(ctk.END,str(result) + temp)
            
            time.sleep(1)
            
            point += 1
            if point == 4:
                point = 1
            if result == 'finish':
                break
            
    def stop(self):
        self.break_loop = True
           
if __name__ == "__main__": 
    observer = Observer('o')
    observer.start()