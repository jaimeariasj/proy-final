import streamlit as st
import requests

# URL de la API
API_URL = "http://127.0.0.1:8000"

# Configuración de la interfaz
st.title("🤖 Chatbot de Empresas 📊")
st.write("Consulta información de empresas por NIT o sector económico.")

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostrar mensajes previos
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
user_input = st.chat_input("Pregúntame algo sobre empresas...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Procesar la entrada del usuario
    response_text = "No entendí la pregunta. Intenta con: 'Buscar NIT 800007367' o 'Top 10 empresas'."

    if user_input.lower().startswith("buscar nit"):
        try:
            nit = user_input.split(" ")[-1]
            response = requests.get(f"{API_URL}/eerr/{nit}")
            if response.status_code == 200:
                empresa = response.json()
                response_text = f"📌 Empresa encontrada: **{empresa['EMPRESA']}**\n🏢 Tipo: {empresa['TIPO_EMPRESA_NOMBRE']}\n💰 Utilidad: {empresa['UTILIDAD']}"
            else:
                response_text = "❌ Empresa no encontrada."
        except Exception as e:
            response_text = "⚠ Error en la búsqueda."

    elif "top 10" in user_input.lower():
        response = requests.get(f"{API_URL}/eerr/top10")
        if response.status_code == 200:
            empresas = response.json()
            response_text = "🏆 **Top 10 Empresas con Mayor Utilidad:**\n"
            for i, empresa in enumerate(empresas):
                response_text += f"{i+1}. {empresa['EMPRESA']} - 💰 {empresa['UTILIDAD']}\n"
        else:
            response_text = "⚠ No se pudo obtener el ranking."

    # Mostrar la respuesta del chatbot
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Guardar en el historial de conversación
    st.session_state["messages"].append({"role": "assistant", "content": response_text})