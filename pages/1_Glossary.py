import streamlit as st
from layout import footer

st.set_page_config(
    page_title="Glossary|Consultant Dost",
    page_icon="https://cdn-icons-png.flaticon.com/128/1189/1189175.png",
)
st.title("Glossary of Model Settings")
# Model Section
st.header("Model")
st.markdown("""
The language model to use for generating output. The following models are available:

1. **Llama3–70b-8192**: Best overall model with high performance.
2. **Llama3–8b-8192**: A smaller variant of Llama3, optimized for efficiency.
3. **Mixtral-8x7b-32768**: Best for long contexts, capable of handling extensive inputs.
4. **Gemma2-9b-It**: An advanced model with improved capabilities.
5. **Gemma-7b-It**: A versatile model suitable for a variety of tasks.
6. **Llama-3.2-11b-Text-Preview**: A preview model for text generation tasks.
7. **Llama-3.1-70b-Versatile**: A highly versatile model for diverse applications.
""")

# Temperature Section
st.header("Temperature")
st.markdown("""
Controls the randomness of the response. This ranges from 0.0 to 1.0:
- **0.0**: Deterministic responses, less creative.
- **1.0**: Highly random and creative responses.
""")

# Maximum Tokens Section
st.header("Maximum Tokens")
st.markdown("""
The maximum number of tokens to generate in the response. This limits the length of the generated text & varies from one model to another. 
- **Example**: Setting this to 100 will generate up to 100 tokens.
""")

# Top-p Section
st.header("Top-p")
st.markdown("""
The top-p sampling strategy to use. This controls the cumulative probability of token selection:
- **0.1**: Only the top 10% probability mass is considered.
- **1.0**: Equivalent to using all tokens, similar to greedy sampling.
""")

# Stop Sequence Section
st.header("Stop Sequence")
st.markdown("""
List of strings to end the text generation. The model will stop generating text when any of these strings are encountered.
- **Example**: Setting this to `["\n", ".", "!"]` will stop generation at a newline, period, or exclamation mark.
""")

# Seed Section
st.header("Seed")
st.markdown("""
Useful for reproducing the same response. Setting a seed ensures that the model generates the same output for the same input.
- **Example**: Setting `seed=42` will produce consistent results across runs.
""")

# Frequency & Presence Penalty Section
st.header("Frequency & Presence Penalty")
st.markdown("""
Useful for controlling the frequency and presence of words in the response:
1. **Frequency Penalty**: Reduces the likelihood of repeated tokens.
2. **Presence Penalty**: Encourages the model to introduce new tokens.
- **Example**: Setting a high frequency penalty will make the model less likely to repeat words.
- **Example**: Setting a high presence penalty will make the model more likely to use new words it hasn't used before in the response.
""")

footer()
