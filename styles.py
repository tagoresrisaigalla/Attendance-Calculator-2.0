# Add this function to your styles.py file

def add_google_analytics(tracking_id):
    """
    Adds Google Analytics tracking to the Streamlit app.
    
    Args:
        tracking_id (str): Your Google Analytics tracking ID (format: G-XXXXXXXXXX)
    """
    # Google Analytics 4 tracking script
    ga_script = f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={tracking_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{tracking_id}');
    </script>
    """
    
    # Inject the script using st.components.html
    import streamlit as st
    from streamlit.components.v1 import html
    
    # Use minimal height to avoid taking up space
    html(ga_script, height=0)

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