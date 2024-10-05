import streamlit as st

st.header("Glossary of the settings of the model")

st.write("## Model")
st.markdown("The language model to use for generating output. The following models are made available:\n\n1.Gemma-7b-It\n\n2.Llama3–70b-8192\n\n3.Llama3–8b-8192\n\n4.Mixtral-8x7b-32768")

st.write("## Temperature")
st.markdown("Controls the randomness of the response. This ranges from 0.0 to 1.0")

st.write("## Maximum tokens")
st.markdown("The maximum number of tokens to generate in the response.")

st.write("## Top-p")
st.markdown("The top-p sampling strategy to use.")

st.write("## Stop sequence")
st.markdown("List of strings to end the text generation.")

st.write("## Seed")
st.markdown("Useful in reproducing same response.")

st.write("## Frequency & Presence Penalty ")
st.markdown("Useful for controlling frequency & presence of words in the response.")

