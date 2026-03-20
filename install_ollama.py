import os
import urllib.request
import subprocess
import time

ollama_path = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe")

if os.path.exists(ollama_path):
    print("Ollama is already installed.")
else:
    print("Downloading Ollama setup...")
    urllib.request.urlretrieve("https://ollama.com/download/OllamaSetup.exe", "OllamaSetup.exe")
    print("Installing Ollama silently...")
    subprocess.run(["OllamaSetup.exe", "/silent"], check=True)

print("Starting server...")
subprocess.Popen([ollama_path, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(5) # Give it time to bind port 11434

print("Pulling llama3.2... This will download the 2GB LLM quickly.")
subprocess.run([ollama_path, "pull", "llama3.2"])
print("Local LLM model pulled successfully! Ready!")
