import streamlit as st
import requests

# Configuração do Streamlit
st.set_page_config(layout="wide")
st.title("UNIFAGOC Chatbot")
st.write("Este é um chatbot que responde perguntas com base em documentos da UNIFAGOC.")

API_URL = "http://localhost:8081/v1/ask"

def get_answer(question: str):
    
    response = requests.post(API_URL, json={"question": question})
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        return f"Erro: {response.status_code} - {response.text}"

# Interface
st.write("Digite sua pergunta abaixo:")
question = st.text_input("Pergunta:")

if question:
    answer = get_answer(question)

    st.subheader("Resposta:")
    st.write(answer)

