from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables
import webbrowser
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-1.5-flash") 
chat = model.start_chat(history=[])
def get_gemini_response(question):
    
    response=chat.send_message(question,stream=True)
    return response


# Set Streamlit page configuration as the first command
st.set_page_config(
    page_title="Bookings",
    page_icon="💬",
    layout="centered"
)

# Define URLs for navigation
home_page_url = 'http://127.0.0.1:8000/'
bookings_page_url = 'http://127.0.0.1:8000/trips/'
tracking_page_url = 'http://127.0.0.1:8000/track/'


# Add a sidebar with navigation buttons and title
st.sidebar.markdown("""
    <style>
   
    .sidebar-content {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 30px; /* Adjust margin as needed */
    }
    

    .sidebar-icon {
        margin-right: 20px; 
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar title and navigation buttons
st.sidebar.markdown('<h1 class="sidebar-content"><span class="sidebar-icon"></span>Bookings Site.</h1>', unsafe_allow_html=True)

button_style = """
    <style>
    .stButton > button {
        height: 50px;
        width: 250px;
        font-size: 138px;
    }
    </style>
"""

# Inject the button style into the sideb
st.sidebar.markdown(button_style, unsafe_allow_html=True)

# Navigation buttons
if st.sidebar.button('🏠 Home Dashboard'):
    webbrowser.open(home_page_url)

if st.sidebar.button('📊 Busbooking page'):
    webbrowser.open(bookings_page_url)

if st.sidebar.button('📄 Tracking page'):
    webbrowser.open(tracking_page_url)



# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input=st.text_input("Input: ",key="input")
submit=st.button("Submit")

if submit and input:
    response=get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("The Chat History is")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
    





