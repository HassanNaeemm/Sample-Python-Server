
import streamlit as st
from groq import Groq

st.title("Groq Available Models")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    models = client.models.list()

    for model in models.data:
        if "llama" in model.id.lower():
            st.write(model.id)

except Exception as e:
    st.error(str(e))
