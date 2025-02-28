# Importamos las herramientas necesarias para contruir nuestra API
import os
from fastapi import FastAPI, HTTPException # FasrtAPI nos ayuda a crear la API y HTTPException maneja errores dentro de la API.
from fastapi.responses import HTMLResponse, JSONResponse  # HTMLRreponse nos ayuda a crear una respuesta HTML y JSONResponse nos ayuda a crear una respuesta JSON
import pandas as pd # Pandas nos ayuda a mannejar datos en tablas como si fuera excel
import nltk # NLTK es una libreria para PNL
from nltk.tokenize import word_tokenize # NLTK nos ayuda a dividir un texto en palabras
from nltk.corpus import wordnet # Ayuda a encontrar sinónimos de palabras

#print(nltk.data.path)

# Indicamos la ruta donde NLTK buscará los datos 
#nltk.data.path.append('C:\Users\jaime\AppData\Roaming\nltk_data')
nltk.data.path.append(nltk.data.path[0] + '/corpus')

# Se descargan las herramientas necesarias para el análisis de palabras
#nltk.download('punkt') #Punkt divide frases en palabras
#nltk.download('wordnet') #paquete para encontrar sinónimos de palabras

# Funciómn para cargar los datos en csv
#def load_eerr():
    
# Leemos el archivo de eerr y selecionamos las principales columnas
    
def load_eerr():
        df = pd.read_csv("dataset/datos_limpios_eerr.csv", encoding="latin1", delimiter=";", quotechar='"', on_bad_lines="skip")[['NIT', 'EMPRESA', 'TIPO_EMPRESA', 'TIPO_EMPRESA_NOMBRE', 'UTILIDAD']]
        return df.fillna('').to_dict(orient='records')
        

# Cargamos los datos al iniciar la API para no leer el archivo cada vez que se llame a la API
eerr_list = load_eerr()

# Función para obtener el sinonimo de una palabra
#def get_synonyms(word):
#    usamos wordnet para obtener sinonimos
#   return {lemma.name().lower() for synonym in wordnet.synsets(word) for lemma in syn.lemmas()}

# Se valida la lectura correcta del dataset y se forza a que el delimitador sea ;
#try:
#    df = pd.read_csv("dataset/datos_limpios_eerr.csv", encoding="latin1", delimiter=";")
   # df = pd.read_csv("dataset/BOG_EERR_SIIS_2023.csv", encoding="latin1")
#    print("✅ Archivo CSV cargado correctamente")
#    print(df.head())  # Debería imprimir las primeras 5 filas
#except FileNotFoundError:
#    print("❌ ERROR: No se encontró el archivo CSV")
#except Exception as e:
    #print(f"❌ ERROR al leer el CSV: {e}")


# Creamos la API
app = FastAPI(title= "API EERR", description="API para el análisis de EERR", version="1.0.0") # (APLICACIÓN PARA ANÁLISIS DE EERR)

# Ruta de Inicio: cuando se abre la API sin especificar nada, verá un mensaje de bienvenida
@app.get('/', tags=['HOME'])
def home():
    return HTMLResponse('<h1> Bienvenido a la API para consulta y análisis de EERR</h1>'
                        '<h1> Para usar la API, visita la documentación: <a href="/docs">Documentación</h1>'
                        '<h1>Powered by Jaime Arias</h1>')     
 
# Obteniendo la lista de EMPRESAS y se crea una ruta para obtener todas las EMPRESAS

# Ruta para obtener todas las empresas

@app.get('/eerr', tags=['EERR'])
def get_eerr():
    #Si hay datos, se devuelve la lista de las empresas, sino se muestra un mensaje de error
    
    return eerr_list or HTTPException(status_code=500, detail="NO HAY EMPRESAS EN LA LISTA")
    
# Endpoint para obtener las 10 empresas con mayor UTILIDAD
@app.get("/eerr/top10", response_class=JSONResponse)
async def top_10_utilidades():
    # Ordenar la lista por UTILIDAD en orden descendente y tomar las 10 primeras
    top_empresas = sorted(eerr_list, key=lambda x: float(x["UTILIDAD"]), reverse=True)[:10]
    
    return top_empresas
  
# Ruta para obtener una EMPRESA por NIT

@app.get('/eerr/{NIT}', tags=['EERR'])
def get_eerr(NIT: int):
    empresa = next((m for m in eerr_list if m['NIT'] == NIT), None)
    
    if empresa is None:
        raise HTTPException(status_code=404, detail="EMPRESA NO ENCONTRADA")

    return empresa


#@app.get('/eerr/{NIT}', tags=['EERR'])
#def get_eerr(NIT: int):
    
   
 #       empresa = next((m for m in eerr_list if m['NIT'] == NIT), None)
 #       #if empresa:
 #       return empresa
 #       raise HTTPException(status_code=404, detail="EMPRESA NO ENCONTRADA")

# Ruta del chatbot que responde con empresas según palabras clave del nombre de empresa
@app.get("/eerr/search/{query}", response_class=JSONResponse)
async def search_empresa(query: str):
    resultado = [e for e in eerr_list if query.upper() in e["EMPRESA"].upper()]
    
    if not resultado:
        raise HTTPException(status_code=404, detail="No se encontraron empresas con esa palabra")
    
    return resultado

