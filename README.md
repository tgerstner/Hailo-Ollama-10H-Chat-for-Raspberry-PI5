# Hailo-Ollama-10H-Chat-for-Raspberry-PI5


April 7, 2026 
Todd Gerstner 

Firstly, thank you for your interest in my little project. I did install  
OpenWebUI and wanted something that was simplier to use. So I developed this 
app. I hope you enjoy using it and if you want to make enhancements, please do, 
thats the best part of being open-source. 

Developed for Hailo-Ollama running on Raspberry PI 5 
to simplify accessing Hailo 10H on the PI 5 instead of 
installing OpenWebUI.

There are two apps included with this package. 
 1) pyhailo_txt.py     --- This is a text version which interfaces with the Hailo 10H.  
                           This is great for testing out your interface. It includes 
                           a verbose mode. 
 2) pyhailo_server.py  --- This is the flask driven web chat

The following python packages are required to run pyhailo_txt.py 
- requests
- json 

The following pyhton packages are required to run pyhailo_server.py 
- flask 
- requests 
- json  

The included shell script, getHailo-Ollama_models.sh 
requires jq to be installed on your linux machiine.  

***  sudo apt instal jq 


To list the models your Hailo-Ollama server supports,
you can run the getHailo-Ollama_models.sh shell script or
run the this command in a terminal: 
   curl http://localhost:8000/hailo/v1/list

Before you can use the models, they need to be downloaded. 
You will need to run this command in a terminal for each model you wish to use:

   Change MODEL-NAME to the model you wish to download from the list.

   curl http://localhost:8000/api/pull   -H "Content-Type: application/json"   -d '{ "model": "MODEL-NAME" }'

**********************************************************************************
Important: This app does not automatically know which models have been 
           downloaded or not. The models listed in the dropdown are static.
           The <select> tag has the model names hard coded. Please make
           sure the names in the <select> tag matches the your model names.   
           if not, then the app will not work. 
           The <select> tag is located in the templates folder in the index.html 
           file.
**********************************************************************************

If your Hailo-Ollama server is running on a different port, 
then you will need to change the hailo_port below.  

Also, this system is designed to run on the Raspberry PI5 which has the 
Hailo 10H board attached via the PCIe port. If you wish run this app 
on a different machine, then you will need to change the hailo_host IP 
address. Please note this has not been tested.   

This app assumes that you have the Hailo-Ollama server running on the
host specified by hailo_host and the port specified by hailo_port.

Observed Model Issues: 
In the testing I have performed, I have noticed that the llama3.2:1b model does not 
handle large requests. It may return jumbled text.


**********************************************************************************
Suggestions: 

   1)  Create a hailo-ollama.service file in /etc/systemd/system to 
       run the Hailo-Ollama server as a service  

   2)  Create another service file for this app, hailo-chat.service and 
       place it in the /etc/systemd/system folder 

Enjoy!!!!


