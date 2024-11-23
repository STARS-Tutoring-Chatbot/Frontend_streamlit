import bson
import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import io
import credentials
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


uri = "mongodb+srv://rchon008:FiuStarsGPT2024@stargpt-database.h9cbh.mongodb.net/"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['user-data']
collection = db['data']



# Helper function to convert an image to Base64
def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


# Define CSS for centering and circular profile image
st.markdown(
    """
    <style>
    .center-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-top: 20px;
    }
    .profile-image {
        width: 250px;
        height: 250px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 20px;
    }
    .title {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the title in a centered style
st.markdown('<h1 class="title">Profile</h1>', unsafe_allow_html=True)
retrieved_image = None

for doc in collection.find({'email': credentials.email}):
        if doc['uploaded_image'] != "":
            image_data = doc["uploaded_image"]
            image_stream = io.BytesIO(image_data)
            retrieved_image = Image.open(image_stream)
            credentials.uploaded_image = retrieved_image

# Initialize the session state for profile image
if "profile_image" not in st.session_state:
    if retrieved_image:
        st.session_state.profile_image = image_to_base64(retrieved_image)
    else:
        # Use default image
        with open("images/profile-user-gray.png", "rb") as f:
            default_image = Image.open(f)
            st.session_state.profile_image = image_to_base64(default_image)



# Display the profile image in a circular format
st.markdown(
    f"""
    <div class="center-container">
        <img src="data:image/png;base64,{st.session_state.profile_image}" class="profile-image">
    </div>
    """,
    unsafe_allow_html=True,
)

# Create a file uploader for image files
uploaded_file = st.file_uploader("Choose a profile picture", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open the uploaded image file using PIL
    image = Image.open(uploaded_file)

    # Save the uploaded image in session state
    st.session_state.profile_image = uploaded_file

    # convert image to binary
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)
    image_binary = bson.Binary(image_bytes.getvalue())

    # Update the profile image
    upload_image = st.button("Upload", use_container_width=True)
    if upload_image:
        st.session_state.profile_image = uploaded_file
        credentials.uploaded_image = image_binary
        collection.update_one({'email': credentials.email}, {'$set': {'uploaded_image': image_binary}})

        st.success("Profile picture updated successfully!")
    


with st.expander("Edit Username"):
    with st.form("edit_username"):
        st.markdown('<h4 class="subheader">Username:</h4>', unsafe_allow_html=True)
        st.write(credentials.username)
        edited_username = st.text_input("New Username", )
        credentials.username = edited_username
        edited = st.form_submit_button("Done", use_container_width=True)
        if edited:
            collection.update_one({"email": credentials.email}, {"$set": {"username": edited_username}})
            st.success("Username updated successfully!")


with st.expander("Edit Password"):
    with st.form("edit_password"):
        st.markdown('<h4 class="subheader">Password:</h4>', unsafe_allow_html=True)
        current_password = st.text_input("Current Password")
        edited_password = st.text_input("New Password",)
        retyped_password = st.text_input("Retype New Password",)
        edited = st.form_submit_button("Done", use_container_width=True)
        if current_password == credentials.password and edited_password == retyped_password:
            if edited:
                collection.update_one({"password": credentials.password}, {"$set": {"password": edited_password}})
        else:
            st.write("Password does not match")

main_page = st.button('Back to main page', use_container_width=True)
if main_page:
    st.switch_page("pages/streamlit_app2.py")

