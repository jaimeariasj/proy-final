# Importamos las herramientas necesarias para contruir nuestra API

from fastapi import FastAPI, HTTPException # FasrtAPI nos ayuda a crear la API y HTTPException maneja errores dentro de la API.
from fastapi.responses import HTMLResponse, JSONResponse  # HTMLRreponse nos ayuda a crear una respuesta HTML y JSONResponse nos ayuda a crear una respuesta JSON
import pandas as pd # Pandas nos ayuda a mannejar datos en tablas como si fuera excel
import nltk # NLTK es una libreria para PNL
from nltk.tokenize import word_tokenize # NLTK nos ayuda a dividir un texto en palabras
from nltk.corpus import wordnet # Ayuda a encontrar sinónimos de palabras

#print(nltk.data.path)

# Indicamos la ruta donde NLTK buscará los datos 
nltk.data.path.append('C:\\Users\\jaime\\AppData\\Local\\Programs\\Python\\Python311\\nltk_data')

# Se descargan las herramientas necesarias para el análisis de palabras
nltk.download('punkt') #Punkt divide frases en palabras
nltk.download('wordnet') #paquete para encontrar sinónimos de palabras

# Funciómn para cargar los datos en csv
def load_eerr():
    
    # Leemos el archivo de eerr y selecionamos las principales columnas
    
    def load_eerr():
        df = pd.read_csv("dataset/BOG_EERR_SIIS_2023.csv", encoding="latin1")[['NIT', 'EMPRESA', 'TIPO_EMPRESA', 'TIPO EMPRESA_NOMBRE', 'UTILIDAD']]
        return df.fillna(0).to_dict(orient='records')
        

# Cargamos los datos al iniciar la API para no leer el archivo cada vez que se llame a la API
eerr_list = load_eerr()

# Función para obtener el sinonimo de una palabra
#def get_synonyms(word):
#    usamos wordnet para obtener sinonimos
#   return {lemma.name().lower() for synonym in wordnet.synsets(word) for lemma in syn.lemmas()}

# Se valida la lectura correcta del dataset y se forza a que el delimitador sea ;
try:
    df = pd.read_csv("dataset/BOG_EERR_SIIS_2023.csv", encoding="latin1", delimiter=";")
   # df = pd.read_csv("dataset/BOG_EERR_SIIS_2023.csv", encoding="latin1")
    print("✅ Archivo CSV cargado correctamente")
    print(df.head())  # Debería imprimir las primeras 5 filas
except FileNotFoundError:
    print("❌ ERROR: No se encontró el archivo CSV")
except Exception as e:
    print(f"❌ ERROR al leer el CSV: {e}")


# Creamos la API
app = FastAPI(title= "API EERR", description="API para el análisis de EERR", version="1.0.0") # (APLICACIÓN PARA ANÁLISIS DE EERR)

# Ruta de Inicio: cuando se abre la API sin especificar nada, verá un mensaje de bienvenida
@app.get('/', tags=['HOME'])
def home():
    return HTMLResponse('<h1>Bienvenido a la API para consulta y análisis de EERR</h1>')


# Obteniendo la lista de EMPRESAS y se crea una ruta para obtener todas las EMPRESAS

# Ruta para obtener todas las empresas

@app.get('/eerr', tags=['EERR'])
def get_eerr():
    #Si hay datos, se devuelve la lista de las empresas, se muestra un mensaje de error
    
    return eerr_list or HTTPException(status_code=500, detail="EMPRESA NO ENCONTRADA")
    
  
# Ruta para obtener una EMPRESA por NIT
@app.get('/eerr/{NIT}', tags=['EERR'])
def get_eerr(NIT: int):
    
    # Buscar la empresa en la lista de empresas según NIT
    #Return next(m for m in eerr_list if m['NIT'] == NIT), {"detalle": "EMPRESA NO ENCONTRADA"}

    # Código sugerido por GPT.
    from fastapi import HTTPException

    @app.get('/eerr/{NIT}', tags=['EERR'])
    def get_eerr(NIT: int):
        empresa = next((m for m in eerr_list if m['NIT'] == NIT), None)
        if empresa:
            return empresa
        raise HTTPException(status_code=404, detail="EMPRESA NO ENCONTRADA")

# Ruta del chatbot que responde con empresas según palabras clave del nombre de empresa

@app.get('/chatbot', tags=['Chatbot'])
def chatbot(query: str):
    # Dividimos la consulta en palabras clave, para entender mejor la intención del usuario
    query_words = word_tokenize(query.lower())
    
    # Si encontramos los datos de la empresa, enviamos la lista; si no, mostramos un mensaje de que no se encontraron coincidencias
    
    # Sugerencia de GPT
    
    results = [empresa for empresa in eerr_list if any(word in empresa['EMPRESA'].lower() for word in query_words)]

    return JSONResponse(content={
        "respuesta": "Aquí tienes algunas empresas." if results else "No encontré Empresas con esa palabra en la razón social",
        "empresas": results
    })
  
