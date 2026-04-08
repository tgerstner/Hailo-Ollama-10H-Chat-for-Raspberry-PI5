
"""
Flask driven app for Hailo-Ollam 10H  

Please read the README file as it contains important information.  

Enjoy!!

"""

from flask import Flask, render_template, jsonify, request
import requests
import json 

app = Flask(__name__)

hailo_host = "127.0.0.1"
hailo_port = "8000" 


# AI response function 
def generate_response(prompt, model): 


     if len(prompt) <=0: 
        return "No question was provided" 

     if len(model) <= 0: 
        return "No model was selected" 

     response = "Hailo could not determine an answer."

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

        url = f"http://{hailo_host}:{hailo_port}/api/chat"

        hailo_response = requests.post(url, json=msg)

        output =  hailo_response.json()

        if len(output) > 0:

           if "message" in output:
              response = output["message"]["content"]
        else:
           response = "Hailo model may not be downloaded."
     except Exception as e:
        response = "Error processing command" + str(e) 

     return response 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    model = data.get("model") 

    response = generate_response(user_message, model)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)    
