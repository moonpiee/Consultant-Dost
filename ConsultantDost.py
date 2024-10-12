import streamlit as st
from groq import Groq
import os
from layout import footer
import mysql.connector

# can pickup api key from browser or from base code
st.set_page_config(
    page_title="Consultant Dost",
    page_icon="https://cdn-icons-png.flaticon.com/128/1189/1189175.png",
)
st.title("Consultant Dost")
st.write("""
###### Meet Your Friend Who Can Help You In Your Consultancy Career.
""")
name = st.text_input("Enter Your Name Here")
st.write(f"""## ![alt-text](https://cdn-icons-png.flaticon.com/128/1189/1189175.png) Welcome {name}:smiley:""")
st.write("""### How can I help you today?""")
st.write("""###### *Navigate to the left sidebar for more settings and info* """)
user_query = st.text_input("Ask off here")

#connect with groq api
with st.sidebar:
        st.title("Settings")

        inp_api_key = st.text_input("Enter Your API Token here")

        model = st.selectbox("Select model", ("llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it", "gemma-7b-it", "llama-3.2-11b-text-preview","llama-3.1-70b-versatile"))

        max_tokens = st.slider("Maximum Tokens",1,35000,2048)
        temp = st.slider("Temperature",0.0,1.0,0.0)

        with st.expander("Advanced Settings"):
                top_p = st.slider("Top-p",0.0,1.0,0.8) 
                # top_k = st.slider("Top-k",1,1000,40)
                freq_penalty = st.slider("Frequency Penalty",0.0,2.0,0.0)
                pres_penalty = st.slider("Presence Penalty",-2.0,2.0,0.0)
                stop_list = st.text_input("Stop sequence (words seperated by comma;\n for ex: end,bye):")
                seed = st.number_input("Seed",0,200000,1)
        if stop_list != "":
               splitted_str = stop_list.split(",")
               stop_list = [x.strip() for x in splitted_str] 

if inp_api_key!="":
        groq_client = Groq(
                api_key=inp_api_key #API KEY 
        )
else:
        groq_client = Groq(
                api_key=st.secrets["api_key"] #API KEY 
        )

agent_name="Consultant Dost"

if user_query != "":
    llm_model = groq_client.chat.completions.create(
            messages = [
                    {
                            "role" : "system", #system role 
                            "content" : f"{st.secrets["sys_content"]} feel free to use your name that is {agent_name} and your mentee name that is {name} if needed \
                                to make reponse personal and interactive + {st.secrets["other_qualities"]} Maintain neat, clear and precise formatting of text", #system role msg
                    },
                    {
                            "role"  : "user", #user role
                            "content" : user_query, #user role msg
                    }
            ],
            model = model,
            max_tokens = max_tokens,
            temperature = temp,
            top_p = top_p,
            frequency_penalty = freq_penalty,
            presence_penalty = pres_penalty,
            stop = stop_list, #stop sequence
            stream = False, 
    )
    st.markdown("""### Your Dost Says: """)
    st.markdown(llm_model.choices[0].message.content) #for stream=False ->default

    resp=llm_model.choices[0].message.content
    try:
        connection = mysql.connector.connect(host=st.secrets["hostname"], database=st.secrets["database"], user=st.secrets["username"], password=st.secrets["password"], port=st.secrets["port"])
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            if user_query!="" and resp!="":
                cursor.execute("""
                insert into conultantdost_amongskin.usr_intr values(id, name, model, input, output)
                values (0, %s, %s, %s, %s);
                """)
                print("Inserted into database")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        
    st.write("#### Copy Options")
    c1, c2, c3 = st.tabs(["Copy Conversation","Copy Query","Copy Response"])
    brk = "\n-----------------------------------------------------------------------------------------------------\n"
    creds = brk+f"Source: [Consultant Dost](https://consultant-dost-chanpie.streamlit.app/)\nMade with ❤️ by [@ChanPie](https://twitter.com/cosmosco_wand)"+brk

    with c2:
        content="Query:\n"+user_query+"\n\n"+creds
        st.code(content)
    with c3:
        content="Response:\n"+f"{llm_model.choices[0].message.content}\n\n"+creds
        st.code(content)
    with c1:
        content=f"Your Query:\n{user_query}\n\n"+f"Consultant Dost's Response:\n{llm_model.choices[0].message.content}+\n\n"+creds
        st.code(content)
footer()
