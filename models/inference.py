import customtkinter
from data.manage_data import open_file, save_file
import time

from services.calculation import Calculation
from threading import Thread
from services.Optimizer import Optimizer
from services.observer import Observer
from util.utilils import write_progress
from configs.settings import *
from models.model import GPT2PPL

class Inference(Calculation):
    
    def __init__(self) -> None:
        pass
    
    def initial(self):
        self.optimizer = Optimizer()
        self.observer = Observer("observation")
        self.model = GPT2PPL()
        self.info_inference = {'probability_ai' : 0.0,
                               'probability_human': 0.0}

        super()      

    def inference(self, lines, use_multiprocessing):
        result = self.model(self.input_text.get(1.0, customtkinter.END), int(self.critical_level_ai.get()), int(self.critical_level_mixte.get()), lines)
        self.progress.configure(progress_color = "#672DF2")
        self.progress.set(20)
        self.progress.stop()
        
        
        res_of_open = open_file('process', 'json')
        plx = res_of_open['perplexity']
        sentences = res_of_open['sentences']
        
        
        if self.process_done < self.number_of_process-1 and use_multiprocessing:
            save_file('process', 'json', {"perplexity" : plx + result[2], 'sentences' : sentences + result[1]})
            print("re", self.number_of_process, self.process_done)
            self.process_done += 1
            return 1
    
        print(result.__len__(), isinstance(plx, list))
        if result.__len__() > 2 and (isinstance(plx, list) or not use_multiprocessing) and (self.number_of_process-1 == self.process_done or not use_multiprocessing): 
            print("indjjdjd")
            sentences += result[1]
            if not plx:
                plx = []
            
            
            perplexity = plx + result[2]
            optimized = []
            if self.use_optimizer_:
                save_file('observation', 'json', {"observation" : 'use Optimizer'})

                self.optimizer(perplexity, 200)
                result_of_opt =  self.optimizer.exclusion_inclusion()
                perplexity = result_of_opt["perplexity"]
                optimized = result_of_opt["optimized"]
            
            get_prob = self.probability_calculation(perplexity)
            pbt = get_prob
            print("probabiltys", get_prob)
            save_file('observation', 'json', {"observation" : 'start'})

            label = int(result[0].get('label'))  
            verdict = result[-1]
            probability = get_prob[0] if label == 0 else get_prob[1]
            print("befire")
            if label ==  1 and get_prob[0] < 50 and get_prob[1] >= 55:
                probability = get_prob[1]
                verdict = "Texte generé par un Humain."
                verdict_info = 1
                print("kmdsfgderdmkflvmkld")
                
            elif label == 0 and get_prob[1] < 50 and get_prob[0] >= 55:
                probability = get_prob[0]
                verdict = "Texte generé par une IA."
                verdict_info = 0
                print("22")

                
            elif (get_prob[0] >= 50 and get_prob[0] <= 55) or (get_prob[1] >= 50 and get_prob[1] <= 55):
                
                if get_prob[0] > get_prob[1]:
                    verdict = "Texte Mixte(Ai predominent)"
                    probability = get_prob[0]
                    verdict_info = 3
                    print("33")

                else:  
                    verdict = "Texte Mixte(Humain predominent)"
                    probability = get_prob[1]
                    verdict_info = 4
                    print("jw")

                    
            # if label == 1:
            #     verdict = "Texte generé par un Humain."
            # else:
            #     verdict = "Texte generé par une IA."
            print("after")
            self.observer.stop()
            self.parameter.delete(1.0, customtkinter.END)
            self.parameter.tag_config("token", foreground = "blue")
            self.parameter.insert(1.0, "Tokens : ", 'token')
            self.parameter.insert(customtkinter.END, str(len(self.tokenizer.tokenize(self.input_text.get(
                        1.0, customtkinter.END )))))

            self.parameter.tag_config("result", foreground = "green")

            self.parameter.insert(customtkinter.END, "\tResult : ", 'result')        
            #self.parameter.insert(customtkinter.END, verdict + '\t')  
            self.typing_effect(verdict)
            self.parameter.tag_config("prob", foreground = "#993997")
            self.parameter.insert(customtkinter.END, " Probability : ", 'prob') 
            
            if self.surligner:
                print(len(perplexity), len(sentences))
                for index in range(len(perplexity)):
                    
                    try : sentence = sentences[index]
                    except : sentence = ""
                        
                    if perplexity[index] <= 200:
                        if len(sentence.split()) == 1:
                            continue
                        
                        if index in optimized:
                            self.rechercher_occurrences(sentence, souligner=True, tag__ = "souligner")
                            
                        self.rechercher_occurrences(sentence)

                        time.sleep(0.1)
                    
            # diviseur = 0
            # try:
            #     label = int(result[0].get('label'))
            #     diviseur = self.critical_level_ai.get()

            # except TypeError:
            #     diviseur = 1
                
            # try:
            #     probability = ((int(result[0]['Perplexity per line']) * MULTIPLICATEUR) / diviseur ) % diviseur
            # except KeyError:
            #     probability = 0.0
            # print("probability : ",  probability)
            # if label == 1:
            #     probability = float((probability))

            self.parameter.insert(customtkinter.END, str(round(probability, 1)) + "%")
            self.probability_ai.set(0)
            self.probability_human.set(0)

            self.graph_progress(self.probability_ai, int(pbt[0]))
            self.graph_progress(self.probability_human, int(pbt[1]))
            self.label_graph_humain.configure(text = f" Graph Humain ({pbt[1]}%)")
            self.label_graph_ai.configure(text = f" Graph AI ({pbt[0]}%)")
            print("end")


        else:
            print("esle")
            self.observer.stop()
            #self.reset_parameter()
            self.parameter.delete(1.0, customtkinter.END)
            self.parameter.tag_config("token", foreground = "blue")
            self.parameter.insert(1.0, "Tokens : None", 'token')

            self.parameter.tag_config("result", foreground = "green")

            self.parameter.insert(customtkinter.END, "\tResult : ", 'result')        
            #self.parameter.insert(customtkinter.END, verdict + '\t')  
            self.typing_effect(result[1])
            self.parameter.tag_config("prob", foreground = "#993997")
            self.parameter.insert(customtkinter.END, " Probability : unavailable", 'prob') 
            
            
        self.info_inference['probability_ai'] = pbt[0]
        self.info_inference['probability_human'] = pbt[1]
        self.info_inference['verdict'] = verdict_info
        
        if self.bascule_summary:
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
                    
        return result


    def amorce_infer(self):
        thread_observer = Thread(target=lambda: self.observer.start( self.parameter, self.reset_parameter)) # None indique au modele qu'il recoit un texte brute
        thread_observer.start()
             
        self.process_done = 0
        self.number_of_process = 0
        save_file('process', 'json', {"perplexity" : [], 'sentences' : []})
        tokens_number = len(self.tokenizer.tokenize(self.input_text.get(1.0, customtkinter.END)))
        
        if tokens_number > MAX_TOKENS:
            all_lines = self.condenser(self.input_text.get(1.0, customtkinter.END))
        
        try:
            self.input_text.tag_remove("highlight", "1.0", customtkinter.END)
            self.input_text.tag_remove("souligner", "1.0", customtkinter.END)

        except: pass
        
        self.progress.start()
   
        #self.probability_human.set(0.8)
        self.progress.configure(progress_color = "#F27085")
        
        self.reset_parameter()
        
        
        
        
        if tokens_number > MAX_TOKENS:
            #thread_inference = Thread(target=lambda: self.multiprocessing_(all_lines))
            #thread_inference.start()          
            
            for line in all_lines:
                print("process")
                thread_inference = Thread(target=lambda: self.inference(line, True))
                thread_inference.start()
                self.number_of_process += 1
                # utiliser multiprocessing a la place de threading
                #thread_inference = Thread(target=lambda: self.multiprocessing_(line))
                #thread_inference.start()    
                
                
        else: 
            #lines = re.split(r'(?<=[.?!][ \[\(])|(?<=\n)\s*',self.input_text.get(1.0, customtkinter.END))

            print("not process")
            thread_inference = Thread(target=lambda: self.inference(None, False)) # None indique au modele qu'il recoit un texte brute
            thread_inference.start()
           