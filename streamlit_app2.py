import streamlit as st
from groq import Groq
from langchain_openai import ChatOpenAI
import openai

#from src.langchainAPI.ModelSingleton import ChatChainSingleton

hidden_items = """
    <style>
    .st-emotion-cache-79elbk {visibility: hidden;}
    </style>
    """
st.markdown(hidden_items, unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state.messages = []

st.title("StarsGPT")
st.logo("images/profile-user-gray.png")

with st.sidebar.expander("Profile", icon=":material/account_circle:"):
    profilePic = st.button("Edit Profile",use_container_width=True)
    if profilePic == True:
        st.switch_page("pages/profile_page.py")


api_choice = st.sidebar.selectbox("Select API Provider", ["Groq", "OpenAI"])
api_key = ""
if api_choice == "Groq":
    groqApi = st.sidebar.text_input("Groq API Key", type="password")
    if groqApi:
        client = Groq(api_key=groqApi)
        api_key = groqApi

elif api_choice == "OpenAI":
    openaiApi = st.sidebar.text_input("OpenAI API Key", type="password")
    if openaiApi:
        openai.api_key = openaiApi
        api_key = openaiApi
        #chain_instance = ChatChainSingleton(model=api_choice, api_key=api_key)
        #st.success(f"Initialized chain for model: {chain_instance.model}")

logout = st.sidebar.button("Logout",use_container_width=True)
if logout:
    st.switch_page("Login.py")

message_container = st.container()
user_input = st.text_area("Please enter your message below:", "")

if st.button("Submit"):
    if user_input:
        with st.spinner("Generating response..."):
            try:
                st.session_state.messages.append({"role": "user", "content": user_input})

                if api_choice == "Groq" and groqApi:
                    completion = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=st.session_state.messages,
                        temperature=1,
                        max_tokens=1024,
                        top_p=1,
                        stream=True,
                        stop=None,
                    )
                    response_text = ""
                    for chunk in completion:
                        response_text += chunk.choices[0].delta.content or ""

                #elif api_choice == "OpenAI" and openaiApi:
                #response_text = chain_instance.chain.run(input=st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                with message_container:
                    for msg in st.session_state.messages:
                        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

                user_input = ""

            except Exception as e:
                st.error(f"Error occurred: {e}")
    else:
        st.warning("Please enter a message.")
else:
    if api_choice == "Groq" and not groqApi:
        st.warning("Please enter your Groq API key.")
    elif api_choice == "OpenAI" and not openaiApi:
        st.warning("Please enter your OpenAI API key.")
