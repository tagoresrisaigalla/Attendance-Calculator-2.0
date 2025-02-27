# Add this import at the top with your other imports
from styles import apply_custom_styles, local_css, add_google_analytics
import streamlit as st
import plotly.graph_objects as go
from calculator import (
    calculate_current_percentage,
    calculate_future_percentage,
    calculate_classes_needed,
    calculate_classes_can_bunk,
    generate_scenarios
)
from styles import apply_custom_styles, local_css
from scraper import AttendanceScraper
import time

# Add these at the top after imports
@st.cache_resource
def create_scraper():
    scraper = AttendanceScraper()
    scraper.setup_driver()
    return scraper

# Optimize calculations with caching
@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_cached_calculations(current_attended, current_total, classes_to_attend, total_future_classes, target_percentage):
    return {
        'current_percentage': calculate_current_percentage(current_attended, current_total),
        'future_percentage': calculate_future_percentage(
            current_attended, current_total, classes_to_attend, total_future_classes
        ) if total_future_classes > 0 else calculate_current_percentage(current_attended, current_total),
        'result': calculate_classes_needed(current_attended, current_total, target_percentage) 
                 if target_percentage > calculate_current_percentage(current_attended, current_total)
                 else calculate_classes_can_bunk(current_attended, current_total, target_percentage)
    }

# Use callback for input changes
def on_input_change():
    st.session_state.needs_update = True

# Page configuration
st.set_page_config(
    page_title="BTech Attendance Calculator",
    page_icon="📊",
    layout="wide"
)

# Apply Google Analytics tracking
add_google_analytics("G-DDP8RPPKGF")  # Replace with your actual tracking ID

# Apply custom styles
apply_custom_styles()
local_css("custom.css")

# Initialize session state with more fields and defaults
if 'current_attended' not in st.session_state:
    st.session_state.current_attended = 0
if 'current_total' not in st.session_state:
    st.session_state.current_total = 0
if 'needs_update' not in st.session_state:
    st.session_state.needs_update = False
if 'classes_to_skip' not in st.session_state:
    st.session_state.classes_to_skip = 0
if 'classes_to_attend' not in st.session_state:
    st.session_state.classes_to_attend = 0

# Add login section to the sidebar BEFORE the main calculator
with st.sidebar:
    st.header("Portal Login For VNRVJIET's")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Fetch Attendance")
        
        if submit_button and username and password:
            with st.spinner("Fetching attendance data..."):
                scraper = AttendanceScraper()
                try:
                    scraper.setup_driver()
                    if scraper.login(username, password):
                        attendance_data = scraper.get_attendance_data()
                        if attendance_data:
                            # Update session state
                            st.session_state.current_attended = attendance_data['attended']
                            st.session_state.current_total = attendance_data['total']
                            st.session_state.needs_update = True
                            
                            # Display success message
                            st.success(f"""
                                Attendance data fetched successfully!
                                Current attendance: {attendance_data['attended']}/{attendance_data['total']} 
                                ({(attendance_data['attended']/attendance_data['total']*100):.2f}%)
                            """)
                            st.rerun()  # Rerun the app to update all components
                        else:
                            st.error("Could not fetch attendance data")
                    else:
                        st.error("Login failed. Please check your credentials.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                finally:
                    scraper.close()

# Main title
st.markdown("<h1 style='text-align: center'>📚 BTech Attendance Calculator</h1>", unsafe_allow_html=True)

# Create three columns for the main layout
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown('<h3>Current Attendance</h3>', unsafe_allow_html=True)
    current_attended = st.number_input("Classes Attended", 
                                     min_value=0,
                                     step=1,
                                     value=st.session_state.current_attended,
                                     key="current_attended_input",
                                     on_change=on_input_change)
    
    current_total = st.number_input("Total Classes", 
                                   min_value=0,
                                   step=1, 
                                   value=st.session_state.current_total,
                                   key="current_total_input",
                                   on_change=on_input_change)
    current_percentage = calculate_current_percentage(current_attended, current_total)
    st.markdown(f'<div class="percentage-display">{current_percentage:.2f}%</div>', 
                unsafe_allow_html=True)

# Update session state for next run
if st.session_state.needs_update:
    st.session_state.needs_update = False

with col2:
    st.markdown('<h3>Future Scenario Planning</h3>', unsafe_allow_html=True)
    classes_to_skip = st.number_input("Classes Planning to Skip", 
                                    min_value=0,
                                    step=1,
                                    value=st.session_state.classes_to_skip,
                                    key="classes_to_skip_input",
                                    on_change=on_input_change)
    
    classes_to_attend = st.number_input("Classes Planning to Attend", 
                                      min_value=0,
                                      step=1,
                                      value=st.session_state.classes_to_attend,
                                      key="classes_to_attend_input",
                                      on_change=on_input_change)
    
    total_future_classes = classes_to_skip + classes_to_attend
    if total_future_classes > 0:
        future_percentage = calculate_future_percentage(
            current_attended, current_total, classes_to_attend, total_future_classes
        )
        st.markdown(f'<div class="percentage-display">{future_percentage:.2f}%</div>', 
                    unsafe_allow_html=True)
    else:
        st.info("Enter the number of classes you plan to attend or skip")
        future_percentage = current_percentage

with col3:
    st.markdown('<h3>Target Calculator</h3>', unsafe_allow_html=True)
    target_percentage = st.slider("Target Percentage", 0, 100, 75)
    calculations = get_cached_calculations(
        current_attended, 
        current_total, 
        classes_to_attend, 
        total_future_classes, 
        target_percentage
    )
    
    # Use the cached results
    current_percentage = calculations['current_percentage']
    future_percentage = calculations['future_percentage']
    result = calculations['result']
    
    if target_percentage > current_percentage:
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 1.2rem;">Classes needed to reach {target_percentage}%:</div>
                <div class="percentage-display">{result}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 1.2rem;">Classes you can bunk while staying above {target_percentage}%:</div>
                <div class="percentage-display">{result}</div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 10px; margin-top: 20px; display: flex; align-items: center; justify-content: center; gap: 10px;">
        <img src="https://media.licdn.com/dms/image/v2/D4E03AQGAeZ9yC9NdAA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1714447572237?e=1746057600&v=beta&t=GMa7oOCwxwspFGgAJ7YPR0MiVr_IWuj2KGC1cmAdysE" 
             style="width: 40px; height: 40px; border-radius: 50%;">
        <div style="display: flex; align-items: center; gap: 5px;">
            <span style="color: #2C3E50;">Made 😎 by</span>
            <a href="https://www.linkedin.com/in/tagoresrisai-galla" 
               target="_blank" 
               style="text-decoration: none; color: #0A66C2; font-weight: 500; display: flex; align-items: center; gap: 5px;">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="#0A66C2">
                    <path d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.3 6.5a1.78 1.78 0 01-1.8 1.75zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.74 1.74 0 0013 14.19a.66.66 0 000 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 012.7-1.4c1.55 0 3.36.86 3.36 3.66z"></path>
                </svg>
                Tagore Sri Sai Galla
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)