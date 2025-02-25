import streamlit as st

def apply_custom_styles():
    """Apply custom styles to the Streamlit app"""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&family=Roboto:wght@400;500;700&display=swap');
            
            .reportview-container {
                background: #F5F7FA;
            }
            
            .main {
                background-color: #F5F7FA;
            }
            
            h1, h2, h3 {
                color: #2C3E50;
                font-family: 'Roboto', sans-serif;
            }
            
            .stButton>button {
                background-color: #1E88E5;
                color: white;
                border-radius: 5px;
                border: none;
                padding: 10px 24px;
                font-weight: 500;
            }
            
            .stButton>button:hover {
                background-color: #1976D2;
            }
        </style>
    """, unsafe_allow_html=True)

def local_css(file_name):
    """Load local CSS file"""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)