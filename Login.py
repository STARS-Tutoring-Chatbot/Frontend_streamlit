import streamlit as st
import re
import bcrypt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

hide_stSidebar = """
    <style>
    .st-emotion-cache-1wqrzgl {visibility: hidden;min-width: 0px;max-width: 0px;}
    .st-emotion-cache-1f3w014 {visibility: hidden;}
    .st-emotion-cache-hzo1qh {visibility: hidden;}
    aria-expanded: false;
    </style>
    """
st.markdown(hide_stSidebar, unsafe_allow_html=True)

st.title('Welcome to STARSGPT')
selection = st.selectbox('Login/Sign up', ('Login', 'Sign up'),)

uri = "mongodb+srv://rchon008:FiuStarsGPT2024@stargpt-database.h9cbh.mongodb.net/"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['user-data']
collection = db['data']


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Helper function to verify passwords
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def is_valid_email(email): #https://www.zerobounce.net/email-guides/python-email-verification/#:~:text=The%20quickest%20way%20to%20check,a%2Dz0%2D9%5D%2B%5B.
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

with st.form("login_form"):
    if selection == 'Login':
        st.header('Login')
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Sign In')
        if email != '' and password != '':
            if is_valid_email(email) != True:
                st.write('Please enter a valid email address')
            if len(password) < 7:
                st.write('Password must be at least 8 characters')
            if is_valid_email(email) and len(password) > 7:
                database_email = collection.find_one({'email': email})
                database_password = collection.find_one({'password': password})
                if database_email is not None:
                    st.write('Email address matches')
                    if database_password is not None:
                        st.write('Password matches')
                        if submitted == True:
                            st.switch_page("pages/streamlit_app2.py")
                    else: st.write('password does not match')
                else:
                    st.write('Please enter a valid email address')

        else:
            if submitted == True:
                st.write('Email and password are required.')

    else:
        st.header('Sign up')
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Sign Up')
        if email != '' and password != '':
            if is_valid_email(email) != True:
                st.write('Please enter a valid email address')
            if len(password) < 7:
                st.write('Password must be at least 8 characters')
            if is_valid_email(email) and len(password) > 7:
                if submitted == True:
                    collection.insert_one({'email': email, 'password': password})
                    st.switch_page("pages/streamlit_app2.py")
        else:
            if submitted == True:
                st.write('Email and password are required.')

