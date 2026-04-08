
""" 
Developed for Hailo-Ollama running on Raspberry PI 5
April 7, 2026  

To list the models your Hailo-Ollama server supports, 
run the this command in a terminal:  
   curl http://localhost:8000/hailo/v1/list

To download the models into your Hailo-Ollama server, 
run this command in a terminal for each model you wish to use: 
   Change MODEL-NAME-FROM-LIST-HERE to the model you wish to download
   curl http://localhost:8000/api/pull   -H "Content-Type: application/json"   -d '{ "model": "MODEL-NAME-FROM-LIST-HERE" }'

"""

import requests 
import json

class HailoClient: 

    hailo_host = "127.0.0.1" 
    hailo_port = "8000"

    answers = []

    answer_file = "HAILO_H10_ANSWERS.txt"

    def send_prompt(self, prompt, model, verbose): 

        try:
           msg = {
                   "model": model, 
                   "messages": 
                               [{ "role": "user", 
                                  "content": prompt }], 
                   "stream": False, 
                   "min_output_tokens": 50, 
                   "max_output_tokens": 500, 
                   "temperature": 0.7 
                 }

           if verbose: 
              print("Input", msg)

           url = f"http://{self.hailo_host}:{self.hailo_port}/api/chat"
           response = requests.post(url, json=msg) 

           output =  response.json() 

           if len(output) > 0:  
              if verbose: 
                 print("Output:", output)

              if "message" in output:  
                 response = output["message"]["content"]
                 print("Hailo says...")
                 ans = {"PROMPT": prompt, "OUTPUT": response, "MODEL": model}  
                 self.answers.append(ans) 
                 print(response) 
           else: 
              print("Hailo model may not be downloaded.")
        except Exception as e: 
           print("Error processing command" + str(e) )

    def get_models(self): 
        try:
           url = f"http://{self.hailo_host}:{self.hailo_port}/hailo/v1/list"
           response = requests.get(url) 

           models = response.json() 
           model_list = models["models"]  
           return model_list 
        except Exception as e: 
           print("Error processing command" + str(e) )
           return "ERROR. No Response"
    def get_previous_answer_count(self):  
        return len(self.answers) 
    
    def save_answers(self):
 
        f = open(self.answer_file, "w") 

        f.write("--------------------------------------------------- \n")
        f.write("         HAILO 10H QUESTIONS AND ANSWERS\n")
        f.write("--------------------------------------------------- \n")

        for item in self.answers: 
            f.write(f"\nQuestion: {item['PROMPT']} ")
            f.write(f"Model:    {item['MODEL']}\n")  
            f.write("Answer:\n")
            f.write(f"{item['OUTPUT']}\n")   
            f.write("--------------------------------------------------- \n")
 

        f.close()  
      
        print(f"Answers have been saved to file: {self.answer_file}") 

    def show_answers(self): 
        print("-------------------------------") 
        print("Previous Answers               ") 
        print("-------------------------------") 

        if len(self.answers) > 0: 
        
           for ans in self.answers: 
               print(f"Question:  {ans["PROMPT"]}") 
               print("---------------------------")
               print(f"Answer:    {ans["OUTPUT"]}")  
        else: 
           print("No previous answers.") 

#/////////////////////////////////////////////////////
#                       MAIN 
#/////////////////////////////////////////////////////

client = HailoClient()


current_model="deepseek_r1:1.5b"  
models = client.get_models() 

verbose = False
last_question = ""


print("********************************")
print("** Hailo 10H Python Interface **") 
print("********************************")

while True: 

   print("")
   print("Enter q to Quit, h for Help")
   print("--------------------------------")
   question = input("What do you want to know? ") 

   question = question.strip() 

   if question.lower() == "q": 
      break

   if question.lower() == "h": 
      print("-------------------------------") 
      print("Hailo 10H Python Interface Help") 
      print("-------------------------------") 
      print("m = Show Models                ") 
      print("c = Change Model               ") 
      print("p = Show Previous Answers      ") 
      print("s = Show Status                ") 
      print("r = Repeat Last Question       ") 
      print("v = Toggle Verbose Mode        ") 
      print("w = Write Answers              ") 
      print("h = Help                       ") 
      print("q = Quit                       ") 

   elif question.lower() == "m": 
      print("-------------------------------")   
      print("Hailo 10H Models:")   
      print("-------------------------------")   
      
      for index, model in enumerate(models):          
          if model == current_model: 
             print(f"{model} (Default)")
          else:
             print(f"{model}")

   elif question.lower() == "s": 
      print("-------------------------------")   
      print("Hailo 10H Status:")   
      print("-------------------------------")   

      print(f"Current Model: {current_model}") 

      if verbose: 
         print("Verbose Mode is Enabled")  
      else:
         print("Verbose Mode is Disabled")   

      previous_ans_count = client.get_previous_answer_count()

      print("Previous Answers:", str(previous_ans_count))

   elif question.lower() == "v": 
      if verbose:    
         verbose = False 
         print("-------------------------------")   
         print("Verbose Mode is Disabled")
         print("-------------------------------")   
      else: 
         verbose = True 
         print("-------------------------------")   
         print("Verbose Mode is Enabled")
         print("-------------------------------")   

   elif question.lower() == "c": 
      print("-------------------------------")   
      print("Hailo 10H Models:")   
      print("-------------------------------")   
      
      for index, model in enumerate(models):          
          if model == current_model: 
             print(f"({index}) --- {model} (Default)")
          else:
             print(f"({index}) --- {model}")

      select_model = input("Select new model to use: ")  
      select_model = int(select_model) 

      if select_model < len(models): 
         current_model = models[select_model] 
         print(f"Hailo 10H is using {current_model} model.")
         print("------------------------------------")   
      
   elif question.lower() == "w": 
      client.save_answers()

   elif question.lower() == "p": 
      client.show_answers()

   elif question.lower() == "r": 

      if len(last_question) > 3: 
         question = last_question 
         print("Repeating Last Question ", question) 
         client.send_prompt(question, current_model, verbose) 
      else: 
         print("No questions have been asked yet.")

      print("************************************************************************************")

   else:
      last_question = question 
      client.send_prompt(question, current_model, verbose) 
      print("************************************************************************************")

print("Shutting Down Hailo 10H Python Interface") 

