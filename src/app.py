"""
CrewAI Job Search Assistant - Multipage Streamlit Application
Main entry point for the multipage app using st.Page and st.navigation
"""

import streamlit as st
from streamlit_pages.home import home_page
from streamlit_pages.job_search import job_search_page
from streamlit_pages.analytics import analytics_page
from streamlit_pages.settings import settings_page
from streamlit_pages.info_page import info_page
from streamlit_pages.specific_jobs import specific_jobs_page
from streamlit_pages.resume_prep import resume_prep_page

# Configure the main app
st.set_page_config(
    page_title="CrewAI Job Search Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for user preferences
if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {
        "theme": "light",
        "show_tips": True,
        "last_visited": None
    }

# Track current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Define pages using st.Page
pages = {
    "Main": [
        st.Page(home_page, title="Home", icon="🏠", url_path="home"),
    ],
    "Services": [
        st.Page(info_page, title="Info Page", icon="💡", url_path="Info_Page"),
        st.Page(job_search_page, title="Job Search Assistant", icon="🔍", url_path="job_search"),
        st.Page(specific_jobs_page, title="Specific Jobs", icon="🎯", url_path="Specific_Jobs"),
        st.Page(resume_prep_page, title="Resume Prep", icon="📝", url_path="Resume_Prep"),
    ],
    "Analytics & Settings": [
        st.Page(analytics_page, title="Job Market Analytics", icon="📊", url_path="analytics"),
        st.Page(settings_page, title="Settings", icon="⚙️", url_path="settings"),
    ]
}

# Create navigation
pg = st.navigation(pages)

# Add some shared styling and header
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    .nav-section {
        padding: 0.5rem 0;
        border-bottom: 1px solid #e6e9ef;
        margin-bottom: 1rem;
    }
    /* Custom sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Custom button styling */
    .stButton button {
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Shared header for all pages
with st.container():
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🤖 CrewAI Job Search Assistant")
    st.markdown("*Your AI-powered career companion*")
    st.markdown('</div>', unsafe_allow_html=True)

# Add breadcrumb navigation
def show_breadcrumb():
    """Display breadcrumb navigation"""
    current_url = st.query_params.get("page", "home")
    
    breadcrumb_map = {
        "home": "🏠 Home",
        "Info_Page": "🏠 Home > 💡 Info Page",
        "job_search": "🏠 Home > 🔍 Job Search Assistant", 
        "Specific_Jobs": "🏠 Home > 🎯 Specific Jobs",
        "Resume_Prep": "🏠 Home > 📝 Resume Prep",
        "analytics": "🏠 Home > 📊 Analytics",
        "settings": "🏠 Home > ⚙️ Settings"
    }
    
    if current_url in breadcrumb_map:
        st.markdown(f"**{breadcrumb_map[current_url]}**")
        st.markdown("---")

show_breadcrumb()

# Run the selected page
pg.run()