import streamlit as st

import streamlit as st

st.write("Welcome to the app!")

# Using an expander as a pop-up
with st.expander("Click here for more information"):
    st.write("This is a pop-up with more details. You can close it by clicking the arrow again.")
    st.write("Add any other content you'd like here.")
