"""
CrewAI Job Search Assistant - AI-Powered Job Search Platform
Main entry point for the multipage app with integrated CrewAI agents and tasks
"""

import streamlit as st
from streamlit_pages.home import home_page
from streamlit_pages.job_search import job_search_page
from streamlit_pages.analytics import analytics_page
from streamlit_pages.specific_jobs import specific_jobs_page
from streamlit_pages.resume_prep import resume_prep_page

# Configure the main app
st.set_page_config(
    page_title="CrewAI Job Search Assistant | AI-Powered Career Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Mira-dmh/CrewAI',
        'Report a bug': 'https://github.com/Mira-dmh/CrewAI/issues',
        'About': "# CrewAI Job Search Assistant\nAI-powered career intelligence platform using multi-agent systems."
    }
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

# URL-based page routing - no need for st.Page definitions

# Handle URL-based navigation
current_page = st.query_params.get("page", "home")

# Create sidebar navigation
with st.sidebar:
    # Logo and branding
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1rem; margin-bottom: 2rem; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin: -1rem -1rem 2rem;">
        <h2 style="color: white; margin: 0; font-size: 1.8em; font-weight: 700; letter-spacing: -0.5px;">CrewAI</h2>
        <p style="color: rgba(255,255,255,0.95); margin: 0.5rem 0 0; font-size: 0.9em; font-weight: 400;">
            Career Intelligence Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Navigation")
    
    # Main section
    st.markdown("### Main Dashboard")
    home_button_type = "primary" if current_page == "home" else "secondary"
    if st.button("Home", key="nav_home", use_container_width=True, type=home_button_type):
        st.query_params.page = "home"
        st.rerun()
    
    # Services section
    st.markdown("### Services")   
    job_search_button_type = "primary" if current_page == "job_search" else "secondary"
    if st.button("Career Research", key="nav_info_page", use_container_width=True, type=job_search_button_type):
        st.query_params.page = "job_search"
        st.rerun()
    
    specific_button_type = "primary" if current_page == "Specific_Jobs" else "secondary"
    if st.button("Job Search", key="nav_specific", use_container_width=True, type=specific_button_type):
        st.query_params.page = "Specific_Jobs"
        st.rerun()
    
    resume_button_type = "primary" if current_page == "Resume_Prep" else "secondary"
    if st.button("Career Preparation", key="nav_resume", use_container_width=True, type=resume_button_type):
        st.query_params.page = "Resume_Prep"
        st.rerun()
    
    # Footer info
    st.markdown("---")
    st.markdown("""
    <div style="padding: 1.5rem; background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); 
                border-radius: 12px; margin-top: 2rem; border: 1px solid #e9ecef;">
        <p style="margin: 0; font-size: 0.8em; color: #495057; text-align: center; line-height: 1.8;">
            <strong style="color: #2c3e50; font-size: 1.1em; display: block; margin-bottom: 0.5rem;">Technology Stack</strong>
            OpenAI GPT-4<br>
            CrewAI Framework<br>
            Streamlit Platform<br>
            <br>
            <span style="font-size: 0.85em; color: #6c757d;">Version 1.0.0</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Page routing function
def route_to_page():
    """Route to the appropriate page based on URL parameter"""
    if current_page == "job_search":
        job_search_page()
    elif current_page == "Specific_Jobs":
        specific_jobs_page()
    elif current_page == "Resume_Prep":
        resume_prep_page()
    else:  # Default to home
        home_page()

# Add some shared styling and header
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main header */
    .main-header {
        text-align: center;
        padding: 2rem 0 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: -1rem -1rem 2rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
    }
    
    .main-header h1 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 2.5em !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95) !important;
        font-size: 1.1em !important;
        font-weight: 300 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 1px solid #e9ecef;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #2c3e50;
        font-weight: 600;
        font-size: 1.3em;
        padding: 0 1rem;
        margin-bottom: 1rem;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #6c757d;
        font-weight: 500;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 0 1rem;
        margin: 1.5rem 0 0.5rem;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 12px;
        border: none;
        font-weight: 500;
        padding: 0.6rem 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton button[kind="secondary"] {
        background: white;
        color: #495057;
        border: 1px solid #dee2e6;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: #f8f9fa;
        border-color: #667eea;
        color: #667eea;
    }
    
    /* Breadcrumb styling */
    .breadcrumb {
        background: linear-gradient(90deg, rgba(102,126,234,0.05) 0%, rgba(118,75,162,0.05) 100%);
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }
    
    .breadcrumb strong {
        color: #495057;
        font-weight: 500;
    }
    
    /* Card styling */
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        box-shadow: 0 4px 20px rgba(102,126,234,0.15);
        transform: translateY(-2px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px;
        padding: 0 24px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Input fields */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        border-radius: 10px;
        border: 1.5px solid #dee2e6;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 12px;
        border-left-width: 4px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(102,126,234,0.05) 0%, rgba(118,75,162,0.05) 100%);
        border-radius: 10px;
        font-weight: 500;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-weight: 500;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 12px;
        background: #2d2d2d;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

# Shared header for all pages
with st.container():
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown("""
        <h1>CrewAI Job Search Assistant</h1>
        <p>AI-Powered Career Intelligence Platform</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Add breadcrumb navigation
def show_breadcrumb():
    """Display breadcrumb navigation"""
    current_url = st.query_params.get("page", "home")
    
    breadcrumb_map = {
        "home": "Home",
        "job_search": "Home > Career Research", 
        "Specific_Jobs": "Home > Job Search",
        "Resume_Prep": "Home > Career Preparation"
    }
    
    if current_url in breadcrumb_map:
        st.markdown(f'<div class="breadcrumb"><strong>{breadcrumb_map[current_url]}</strong></div>', unsafe_allow_html=True)

show_breadcrumb()

# Run the selected page
route_to_page()