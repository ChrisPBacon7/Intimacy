import subprocess
import time
import requests

# Start the Streamlit app in the background
proc = subprocess.Popen(["pdm", "run", "streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"])
time.sleep(5)  # Wait for it to start

try:
    response = requests.get("http://localhost:8501/_stcore/health")
    if response.status_code == 200:
        print("Streamlit app is up and healthy.")
    else:
        print(f"Streamlit app returned status code {response.status_code}")
except Exception as e:
    print(f"Failed to connect to Streamlit app: {e}")

# Kill the process
proc.terminate()
