"""
Settings Page - Configuration and preferences for CrewAI Job Search Assistant
"""

import streamlit as st
import os
from dotenv import load_dotenv, set_key, find_dotenv

def settings_page():
    """
    Settings page content - API configuration and user preferences
    """
    
    # Track page visit
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from utils.session_manager import track_page_visit
        track_page_visit("Settings")
    except:
        pass  # Fail silently if tracking is unavailable
    
    st.markdown("# ⚙️ Settings & Configuration")
    st.markdown("*Configure your AI assistant and personalize your experience*")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key for system info (even though we removed API settings tab)
    current_openai_key = os.getenv("OPENAI_API_KEY", "")
    
    # Tabs for different settings categories
    tab1, tab2 = st.tabs(["👤 Profile", "🤖 AI Settings"])
    
    with tab1:
        st.markdown("## 👤 User Profile")
        st.markdown("Personalize your job search experience.")
        
        # Personal information
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=st.session_state.get('user_name', ''))
            email = st.text_input("Email Address", value=st.session_state.get('user_email', ''))
            location = st.text_input("Location", value=st.session_state.get('user_location', ''))
        
        with col2:
            preferred_salary = st.number_input(
                "Preferred Salary Range (USD)", 
                min_value=0, 
                max_value=500000, 
                value=st.session_state.get('preferred_salary', 100000), 
                step=5000
            )
            work_type = st.multiselect(
                "Preferred Work Type",
                ["Remote", "Hybrid", "On-site", "Contract", "Full-time", "Part-time", "Internship"],
                default=st.session_state.get('work_type', ["Remote", "Full-time"])
            )
        
        # Job preferences
        st.markdown("### 🎯 Job Preferences")
        
        preferred_roles = st.text_area(
            "Preferred Job Titles",
            value="Software Engineer, Data Scientist, Product Manager",
            help="Comma-separated list of job titles you're interested in"
        )
        
        skills = st.text_area(
            "Your Skills",
            value="Python, JavaScript, SQL, React, AWS",
            help="Comma-separated list of your key skills"
        )
        
        industries = st.multiselect(
            "Preferred Industries",
            ["Technology", "Healthcare", "Finance", "Education", "Retail", "Manufacturing", "Media", "Government"],
            default=["Technology"]
        )
        
        if st.button("💾 Save Profile"):
            # Save to session state (in real app, save to database)
            st.session_state['user_name'] = name
            st.session_state['user_email'] = email
            st.session_state['user_location'] = location
            st.session_state['preferred_salary'] = preferred_salary
            st.session_state['work_type'] = work_type
            st.session_state['preferred_roles'] = preferred_roles
            st.session_state['skills'] = skills
            st.session_state['industries'] = industries
            st.success("✅ Profile saved successfully!")
    
    with tab2:
        st.markdown("## 🤖 AI Assistant Configuration")
        st.markdown("*Customize AI behavior for job search and analysis*")
        
        # AI response settings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Response Style")
            response_style = st.selectbox(
                "How should the AI respond?",
                ["Professional", "Casual", "Detailed", "Concise"],
                help="Choose the tone and level of detail in AI responses"
            )
            
            analysis_depth = st.slider(
                "Analysis Depth",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Quick overview | 5 = Comprehensive analysis"
            )
        
        with col2:
            st.markdown("### ⚡ Performance")
            auto_refresh = st.selectbox(
                "Data Auto-refresh",
                ["Disabled", "Every hour", "Every 6 hours", "Daily"],
                index=2,
                help="How often to automatically refresh job search data"
            )
            
            max_results = st.number_input(
                "Max Results per Search",
                min_value=10,
                max_value=100,
                value=50,
                step=10,
                help="Maximum number of job postings to display"
            )
        
        st.markdown("---")
        
        # Save button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("💾 Save AI Settings", use_container_width=True, type="primary"):
                st.session_state['response_style'] = response_style
                st.session_state['analysis_depth'] = analysis_depth
                st.session_state['auto_refresh'] = auto_refresh
                st.session_state['max_results'] = max_results
                st.success("✅ AI settings saved successfully!")

if __name__ == "__main__":
    settings_page()
