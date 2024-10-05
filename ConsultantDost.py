import streamlit as st
from groq import Groq
import os

# def string_to_list(x):
#        splitted
#        y=[lambda i:i.split(",") for i in x]
#        return y

# def upd_session_state(st.session_state(), parameter, value):
#        if parameter not in st.session_state:
#               st.session_state['parameter'] = value
#        else:
#               st.session_state['parameter'] = None

st.set_page_config(
    page_title="Consultant Dost",
    page_icon="![alt-text](https://cdn-icons-png.flaticon.com/128/1189/1189175.png)",
)
            
        

st.title("Consultant Dost")
st.write("""
###### Meet Your Friend who can help you in your Consultancy career.
""")
name = st.text_input("Enter Your Name Here")
st.write(f"""## ![alt-text](https://cdn-icons-png.flaticon.com/128/1189/1189175.png) Welcome {name}:smiley:""")
st.write("""### How can I help you today?""")
st.write("""###### *Navigate to the left sidebar for more settings and info* """)
user_query = st.text_input("Ask off here")

# tabs = ["Home", "Page 1", "Page 2"]
# page = st.tabs(tabs)


#connect with groq api
with st.sidebar:
        st.title("Settings")
        model = st.selectbox("Select model", ("mixtral-8x7b-32768", "llama3–70b-8192", "llama3-8b-8192", "gemma-7b-it"))

        max_tokens = st.slider("Maximum Tokens",1,35000,2048)
        temp = st.slider("Temperature",0.0,1.0,0.0)
        # st.write(st.session_state.temp)
        # if 'previous_slider_value' not in st.session_state:
        #         st.session_state['previous_slider_value'] = temp

        # if temp != st.session_state['previous_slider_value']:
        #     # Execute code when the slider value changes
        #     st.write("Slider value changed to:", temp)
        #     st.session_state['previous_slider_value'] = temp
        

        #advanced settings shall i consider topk and top p also in this?
        

        #exapnd feature
        with st.expander("Advanced Settings"):
                top_p = st.slider("Top-p",0.0,1.0,0.8) #takes whatever you mention 
                # top_k = st.slider("Top-k",1,1000,40)
                freq_penalty = st.slider("Frequency Penalty",0.0,2.0,0.0)
                pres_penalty = st.slider("Presence Penalty",-2.0,2.0,0.0)
                stop_list = st.text_input("Stop sequence (words seperated by comma;\n for ex: end,bye):")
                seed = st.number_input("Seed",0,200000,1)
                # more_context = st.text_input("Enter your custom context here")
        if stop_list != "":
               splitted_str = stop_list.split(",")
               stop_list = [x.strip() for x in splitted_str] #look into - lambda func vs list comprehensions
               print(f"stop list after splitting: {splitted_str}, {type(splitted_str)}") #returns list
        
#set the key on os env (windows powershell: $env:GROQ_API_KEY=<key>)
groq_client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
)

agent_name="Consultant Dost"
other_qualities = "As a 54-year-old leader of a top-performing multinational corporation (MNC), your journey to this esteemed position has been shaped by a unique set of qualities and experiences. You possess visionary thinking, allowing you to anticipate market trends and steer your organization towards innovative solutions and long-term growth. Your resilience helps you navigate challenges effectively, embracing setbacks as learning opportunities. Strong communication skills foster an environment of open idea-sharing, enhancing collaboration and team cohesion. Your emotional intelligence enables you to build strong relationships, connect with diverse teams, and motivate individuals, leading to a high-performing culture. You excel in strategic decision-making, making informed choices based on data analysis and market research, ensuring your company stays ahead of the competition. Your adaptability allows you to quickly embrace new technologies and changing circumstances, maintaining the MNC's relevance in a fast-paced global market. Committed to diversity and inclusion, you advocate for diverse hiring practices and inclusion initiatives, fostering a culture where every voice is heard and valued. Your dedication to continuous learning inspires your team to pursue their own development, creating a culture of excellence. With a global perspective gained from working in various countries, you lead diverse teams and navigate international markets successfully. Prioritizing ethical leadership, you establish trust with stakeholders and cultivate a corporate culture that values integrity and transparency. These qualities, combined with your passion for driving success and making a positive impact, have led you to this pivotal leadership role in a top-performing MNC."

# print(f"user query: {user_query==None}")
print(f"user query: {user_query==""}")
#cehcking the default values:
print(f"temp value : {temp}")
print(f"top p value : {top_p}")
# print(f"top k value : {top_k}")
print(f"freq penalty value : {freq_penalty}")
print(f"presence penalty : {pres_penalty}")
print(f"stop sequence words (seperated by comma ex: end,bye): {stop_list}")
# print(f"custom context : {more_context}")


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
        #     top_k = top_k, #not valid as a paramtere here
            frequency_penalty = freq_penalty,
            presence_penalty = pres_penalty,
            stop = stop_list, #stop sequence,
            stream = False, #default-False | generates real time data for user - Setting stream=False ensures that you receive the entire response from the service in one complete message, rather than in partial updates. 
            seed = seed,

    )

    st.header("Your Dost says: ")
    st.write(llm_model.choices[0].message.content) #for stream=False
#     for chunk in llm_model: #for stream=True
#         st.write(chunk.choices[0].delta.content,end='')


st.write("""###### 
         Glossary:
         max_tokens => maximum number of tokens generated in the response
         temperature => controls randomness. more temp => more randomness of output
         top_p => sampling pool limit to smallest set of tokens with cumulative probability of atleast p. high top_p => more diverse response.

         """)