import streamlit as st
from groq import Groq
import os
import pyperclip
from layout import footer
from kivy.core.clipboard import Clipboard

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
                api_key=os.environ.get("api_key") #API KEY 
        )

agent_name="Consultant Dost"
other_qualities = "As a 54-year-old leader of a top-performing multinational corporation (MNC), your journey to this esteemed position has been shaped by a unique set of qualities and experiences. You possess visionary thinking, allowing you to anticipate market trends and steer your organization towards innovative solutions and long-term growth. Your resilience helps you navigate challenges effectively, embracing setbacks as learning opportunities. Strong communication skills foster an environment of open idea-sharing, enhancing collaboration and team cohesion. Your emotional intelligence enables you to build strong relationships, connect with diverse teams, and motivate individuals, leading to a high-performing culture. You excel in strategic decision-making, making informed choices based on data analysis and market research, ensuring your company stays ahead of the competition. Your adaptability allows you to quickly embrace new technologies and changing circumstances, maintaining the MNC's relevance in a fast-paced global market. Committed to diversity and inclusion, you advocate for diverse hiring practices and inclusion initiatives, fostering a culture where every voice is heard and valued. Your dedication to continuous learning inspires your team to pursue their own development, creating a culture of excellence. With a global perspective gained from working in various countries, you lead diverse teams and navigate international markets successfully. Prioritizing ethical leadership, you establish trust with stakeholders and cultivate a corporate culture that values integrity and transparency. These qualities, combined with your passion for driving success and making a positive impact, have led you to this pivotal leadership role in a top-performing MNC."

if user_query != "":
    llm_model = groq_client.chat.completions.create(
            messages = [
                    {
                            "role" : "system", #system role 
                            "content" : f"Imagine you are a 54 yoe who leads a top performing MNC. \
                                You have gone through all the level like associate analyst, analyst, consultant, manager, \
                                    senior manager etc., You are a very helpful, empathetic mentor who guides and loves to help \
                                    everyone in this consulatncy career. You explain, mentor and guide effectively with \
                                    high efficiency, skilled at everything that MNCs need including excellent character & positivity. feel free to use your name that is {agent_name} and your mentee name that is {name} if needed \
                                to make reponse personal to enhance interaction + {other_qualities}. Maintain neat, clear and precise formatting of text", #system role msg
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
    
    st.write("#### Copy Options")
    c1, c2, c3 = st.tabs(["Copy Conversation","Copy Query","Copy Response"])
    brk = "\n-----------------------------------------------------------------------------------------------------\n"
    creds = brk+f"Source: [Consultant Dost](https://consultant-dost-chanpie.streamlit.app/)\nMade with ❤️ by [@ChanPie](https://twitter.com/cosmosco_wand)"+brk

    with c2:
        if st.button("Copy Query to Clipboard"):
                Clipboard.copy("Query:\n"+user_query+"\n\n"+creds)
                st.success("Query copied successfully!")
    with c3:
        if st.button("Copy Response to Clipboard"):
                Clipboard.copy("Response:\n"+f"{llm_model.choices[0].message.content}\n\n"+creds)
                st.success("Response copied successfully!")
    with c1:
        if st.button("Copy Conversation to Clipboard"):
                qa = f"Your Query:\n{user_query}\n\n"+f"Consultant Dost's Response:\n{llm_model.choices[0].message.content}+\n\n"+creds
                Clipboard.copy(qa)
                st.success("Conversation copied successfully!")
footer()
