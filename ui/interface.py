import os
import sys
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(chemin_parent)

from typing import Any
import customtkinter
from models.inference import Inference
import time
from transformers import GPT2Tokenizer
import re
from configs.settings import *

if DEFINE_THEME:
    customtkinter.set_appearance_mode(THEME)

class Interface(Inference):
    def __init__(self) -> None:
        super().initial()
        self.window = customtkinter.CTk()
        self.window.title("StopLMM")
        self.window.geometry("1280x800")
        self.window.resizable(False, False)
        self.contenair_title = customtkinter.CTkFrame(self.window, fg_color="transparent")
        self.contenair_title.pack(expand = True)       
        self.contenair = customtkinter.CTkFrame(self.window)
        self.contenair.pack(expand = True)
        
        self.frame_interaction = customtkinter.CTkFrame(self.contenair, fg_color="transparent")
        self.frame_interaction.grid(row = 0, column = 0, padx = 10)
        
        self.frame_option = customtkinter.CTkFrame(self.contenair, fg_color="transparent")
        self.frame_option.grid(row = 0, column = 1)
        #self.frame_option.grid_forget()
        
        self.generate_label("  ", 0, self.contenair, column=2)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.surligner = False
        self.use_optimizer_ = False
        self.number_of_process = 0
        self.process_done = 0
        self.bascule_summary = False

    def condenser(self, sentence):
        lines = re.split(r'(?<=[.?!][ \[\(])|(?<=\n)\s*',sentence)
        all_lines = []
        temp = []
        compteur = 0
        for line in lines:
            if compteur < MAX_TOKENS:
                temp.append(line)
                compteur += len(self.tokenizer.tokenize(line))

                
            else:
                compteur = 0
                all_lines.append(temp)
                temp = []
        if compteur != 0 and  temp.__len__() != 0:
            all_lines.append(temp)
                
        return all_lines

    def rechercher_occurrences(self, mot, souligner = False, color = "gray", tag__ = "highlight"):
            # Efface toutes les balises de mise en surbrillance précédentes
            #self.input_text.tag_remove("highlight", "1.0", customtkinter.END)

            texte = self.input_text.get("1.0", "end-1c")  # Obtient le texte du widget texte
            mot_a_rechercher = mot  # Obtient le mot à rechercher
            occurrences = []

            # Recherche toutes les occurrences du mot dans le texte
            index = 1.0
            if mot.__len__() != 0:
                while True:
                    index = self.input_text.search(mot_a_rechercher, index, stopindex=customtkinter.END)
                    if not index:
                        break
                    occurrences.append(index)
                    index = self.input_text.index(f"{index}+{len(mot_a_rechercher)}c")
                # Met en surbrillance les occurrences trouvées
                for index in occurrences:
                    self.input_text.tag_add(tag__, index, f"{index}+{len(mot_a_rechercher)}c")
                    
                if occurrences:
                    
                    if souligner:
                        self.input_text.see(occurrences[0])
                        self.input_text.tag_config(tag__, underline = True)
                    else:
                        self.input_text.see(occurrences[0])
                        self.input_text.tag_config(tag__, background=color)
                    

    def typing_effect(self, string1):
        for char in string1:
            self.parameter.tag_config('color_i', foreground = '#666666')
            self.parameter.insert("end",char , "color_i")
            self.parameter.update()
            self.parameter.see("end")
            time.sleep(0.05)

    def on_get(self, event):
        self.input_text.configure(border_color='blue', border_width = 2)
        
    def out_get(self, event):
        self.input_text.configure(border_color='#969696', border_width = 1)
          
    def multiprocessing_(self, lines):
        for line in lines:
            print("pcs")
            self.inference(line, False)

    def reset_parameter(self):
        self.parameter.delete(1.0, customtkinter.END)
        
        self.parameter.tag_config("token", foreground = "blue")
        self.parameter.insert(1.0, "Tokens : ", 'token')
        self.parameter.insert(customtkinter.END, str(len(self.tokenizer.tokenize(self.input_text.get(
                    1.0, customtkinter.END )))))

        self.parameter.tag_config("result", foreground = "green")

        self.parameter.insert(customtkinter.END, "\tResult : ", 'result')        
        self.parameter.insert(customtkinter.END, "None\t")   

        self.parameter.tag_config("prob", foreground = "#993997")
        self.parameter.insert(customtkinter.END, "Probability : ", 'prob')   
        self.parameter.insert(customtkinter.END, "0.0")
    
                   
    def generate_label(self,text,row, contenair , column = 0):
        self.label_ = customtkinter.CTkLabel(contenair, text=text,  font=("courier", 14))
        self.label_.grid(row=row, column=column,pady=2)
        
        
    def stop_progress(self, progressbar):
        progressbar.stop()

    def graph_progress(self, progressbar, value):
        progressbar.start()
        temps = (TIME * value) / 100
        self.window.after(int(temps), lambda : self.stop_progress(progressbar))

    def generate_frame(self, row, contenair = None, border = 1):
        if contenair is None:
            contenair = self.frame_option
        self.frame_ = customtkinter.CTkFrame(contenair, fg_color="transparent", border_width=border)
        self.frame_.grid(row = row, column=0, pady= 10)
        return self.frame_
         
    def critical_meth_human(self, event):
        
        value_ = int(self.critical_level_human.get())
        self.label_slider_human.configure(text = str(value_))
        
    def critical_meth_ai(self, event):
        
        value_ = int(self.critical_level_ai.get())
        self.label_slider_ai.configure(text = str(value_))

    def critical_meth_mixte(self, event):
        
        value_ = int(self.critical_level_mixte.get())
        self.label_slider_mixte.configure(text = str(value_))
    
    def surligner_text(self):
        if self.surligner:
            self.surligner = False
        else:
            self.surligner = True

    def use_optimizer_meth(self):
        if self.use_optimizer_:
            self.use_optimizer_ = False
        else:
            self.use_optimizer_ = True
    
    def summary_funct(self):
        
        if not self.bascule_summary:
            
            self.input_text.configure(width=SIZE_OF_WDT)
            self.summary_box.grid(row=1, column=1)
            self.button_summary.configure(text='hide summary')
            self.bascule_summary = True
            
            pbt_ai = self.info_inference['probability_ai']
            pbt_h = self.info_inference['probability_human']
            verdict_ = self.info_inference['verdict']
            print(verdict_)
            if verdict_ == 0 : sujet, sujet_2, sujet_3, one, sec = "par une IA", "de l'AI", "humaine", pbt_ai, pbt_h
            elif verdict_ == 1 : sujet, sujet_2, sujet_3, one, sec = "par un Humain", "Humaine", "d'une IA", pbt_h, pbt_ai
            elif verdict_ == 3 : sujet, sujet_2, sujet_3, one, sec, = "de l'IA", "de l'AI", "humaine", pbt_ai, pbt_h
            elif verdict_ == 4 : sujet, sujet_2, sujet_3, one, sec, = "de l'Humain", "de l'AI", "humaine", pbt_h, pbt_h
            
            if verdict_ in (0,1) : text_summary_ = f"le texte soumit est un texte generé par {sujet}. la participation {sujet_2} dans la redaction du texte est estimée à {one}% pour seulement {sec}% de participation {sujet_3} "
            
            else : text_summary_ = f"le texte soumit est un texte qui presente de variante mixte, il s'agit là d'un texte presentant un equilibre dans la participation de l'Humain et L'IA, mais avec une predominence {sujet} presentant un taux de participation de {one}%"
            self.summary_box.delete(1.0, customtkinter.END)
            self.summary_box.insert(customtkinter.END, text_summary_)
            
            
        else:
            self.input_text.configure(width = 1000)
            self.summary_box.grid_forget()
            self.button_summary.configure(text='summary')
            self.bascule_summary = False
                
    def __call__(self, call) -> Any:
        label_title = customtkinter.CTkLabel(self.contenair_title, text="ZeroBot",  font=("courier", 40))
        label_title.grid(row=0, column=0, padx = 5)
        label_title2 = customtkinter.CTkLabel(self.contenair_title, text="Experimental",  font=("courier", 12, 'italic'), text_color='blue')
        label_title2.grid(row=0, column=1)
        
        self.generate_label("", 0, self.frame_interaction)

        
        self.generate_frame(1, self.frame_interaction, border=0)
        
        self.input_text = customtkinter.CTkTextbox(self.frame_, width=1000, height=500,  wrap=customtkinter.WORD,insertwidth=8 , font=("courier", 15, 'italic'), corner_radius=0, border_width=1, border_color='gray')
        self.input_text.grid(row=1, column=0, padx=10)
        

        self.summary_box = customtkinter.CTkTextbox(self.frame_, width=SIZE_OF_WDT, height=500,  wrap=customtkinter.WORD,insertwidth=8 , font=("courier", 15, 'italic'), corner_radius=10, border_width=0, border_color='gray')
        #self.summary_box.grid(row=1, column=1)
        #self.summary_box.grid_forget()
        
    
        self.progress = customtkinter.CTkProgressBar(self.frame_interaction, orientation=customtkinter.HORIZONTAL, width=1000, determinate_speed=5, corner_radius=0, height=3, progress_color= "blue")
        self.progress.grid(row = 2, column = 0)
        self.progress.set(0)

        self.parameter = customtkinter.CTkTextbox(self.frame_interaction, width=1000, height=20, fg_color='transparent', border_width=2, wrap=customtkinter.WORD,insertwidth=2 , corner_radius=0, font=("courier", 15, 'italic'))
        self.parameter.grid(row=3, column=0, pady = 10)

        self.generate_frame(4, self.frame_interaction)

        self.generate_label("   ", 0, self.frame_, 0)
        self.probability_human = customtkinter.CTkProgressBar(self.frame_, orientation=customtkinter.HORIZONTAL, width=700, determinate_speed=0.5, corner_radius=0, height=16, progress_color= "blue")
        self.probability_human.grid(row=0, column=1, pady = 10)
        self.probability_human.set(0)
        self.label_graph_humain = customtkinter.CTkLabel(self.frame_, text="  Graph Humain ",  font=("courier", 13))
        self.label_graph_humain.grid(row=0, column=2)
        #self.generate_label("  Graph Humain ", 0, self.frame_, 2)

        self.generate_label("   ", 0, self.frame_, 0)
        self.probability_ai = customtkinter.CTkProgressBar(self.frame_, orientation=customtkinter.HORIZONTAL, width=700, determinate_speed=0.5, corner_radius=0, height=16, progress_color= "#c11595")
        self.probability_ai.grid(row=1, column=1, pady = 10)
        self.probability_ai.set(0)
        
        self.label_graph_ai = customtkinter.CTkLabel(self.frame_, text="  Graph IA ",  font=("courier", 13))
        self.label_graph_ai.grid(row=1, column=2)
        
        #self.generate_label(" Graph AI    ", 1, self.frame_, 2)


        self.parameter.tag_config("token", foreground = "blue")
        self.parameter.insert(1.0, "Tokens : ", 'token')
        self.parameter.insert(customtkinter.END, "0")

        self.parameter.tag_config("result", foreground = "green")
        self.parameter.insert(customtkinter.END, "\tResult : ", 'result')   
        self.parameter.insert(customtkinter.END, "None\t")
        
        self.parameter.tag_config("prob", foreground = "#993997")
        self.parameter.insert(customtkinter.END, "Probability : ", 'prob')   
        self.parameter.insert(customtkinter.END, "0.0")
        
        self.parameter.insert(customtkinter.END, "\tModel : ChatGPT-3.5")

                   
        self.submit = customtkinter.CTkButton(self.frame_interaction, text="submit", command= self.amorce_infer)
        self.submit.grid(row=5, column=0, padx=5)
        

        self.generate_label("    ", 6, self.frame_interaction, column=0)

        
        # Creation des slider parametriques
        self.label_ = customtkinter.CTkLabel(self.frame_option, text="Custom",  font=("courier", 20, 'bold'))
        self.label_.grid(row=0, column=0,pady=2)
        
        self.generate_frame(1)
        self.generate_label("Critical Human", 0, self.frame_)
        self.critical_level_human = customtkinter.CTkSlider(self.frame_, to=1000, command=self.critical_meth_human, width=166, height=16, progress_color="blue")
        self.critical_level_human.grid(row=1, column = 0, pady = 10)
        self.critical_level_human.set(500)
        self.label_slider_human = customtkinter.CTkLabel(self.frame_, text=str(int(self.critical_level_human.get())),  font=("courier", 14, 'italic'))
        self.label_slider_human.grid(row=2, column=0,pady=2)

        self.generate_frame(2)
        self.generate_label("Critical AI", 0, self.frame_)
        self.critical_level_ai = customtkinter.CTkSlider(self.frame_, to=1000, command= self.critical_meth_ai, width=166, height=16, progress_color="blue")
        self.critical_level_ai.grid(row=1, column = 0, pady = 10)
        self.critical_level_ai.set(200)
        self.label_slider_ai = customtkinter.CTkLabel(self.frame_, text=str(int(self.critical_level_ai.get())),  font=("courier", 14, 'italic'))
        self.label_slider_ai.grid(row=2, column=0,pady=2)
        
        self.generate_frame(3)
        self.generate_label("Critical Mixte", 0, self.frame_)
        self.critical_level_mixte = customtkinter.CTkSlider(self.frame_, to=1000, command= self.critical_meth_mixte, width=166, height=16, progress_color="blue")
        self.critical_level_mixte.grid(row=1, column = 0, pady = 10)
        self.critical_level_mixte.set(280)
        self.label_slider_mixte = customtkinter.CTkLabel(self.frame_, text=str(int(self.critical_level_mixte.get())),  font=("courier", 14, 'italic'))
        self.label_slider_mixte.grid(row=2, column=0,pady=2)
        
        self.generate_frame(4)
        self.surligner_texte_ai = customtkinter.CTkSwitch(self.frame_, text="Surligner" , command=self.surligner_text)
        self.surligner_texte_ai.grid(row = 0, column=0, pady=5)

        self.use_optimizer = customtkinter.CTkSwitch(self.frame_, text="Optimizer" , command=self.use_optimizer_meth)
        self.use_optimizer.grid(row = 1, column=0, pady=5)

        self.generate_label("Charger fichier", 2, self.frame_)

        self.charger_fichier = customtkinter.CTkOptionMenu(self.frame_, values=["", "pdf", "txt", "word"], width=100 , command=None)
        self.charger_fichier.grid(row = 3, column=0, pady = 5)
        self.button_summary = customtkinter.CTkButton(self.frame_, text="summary", command= self.summary_funct, fg_color='pink', width=50, text_color='black', state='disable')
        self.button_summary.grid(row=4, column=0)
        
        self.generate_label("", 5, self.frame_)


        
        self.input_text.bind("<FocusIn>", self.on_get)
        self.input_text.bind("<FocusOut>", self.out_get)
        self.window.mainloop()


if __name__ == "__main__":
    inter = Interface()
    inter(True)