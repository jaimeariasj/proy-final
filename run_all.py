import subprocess

# Ejecutar Uvicorn
uvicorn_process = subprocess.Popen(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"])

# Ejecutar Streamlit
streamlit_process = subprocess.Popen(["streamlit", "run", "chatbot.py"])

# Esperar a que los procesos terminen
uvicorn_process.wait()
streamlit_process.wait()