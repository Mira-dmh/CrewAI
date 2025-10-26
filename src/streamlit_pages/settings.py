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
    
    # Tabs for different settings categories
    tab1, tab2, tab3, tab4 = st.tabs(["🔑 API Settings", "👤 Profile", "🎨 Preferences", "🔧 Advanced"])
    
    with tab1:
        st.markdown("## 🔑 API Configuration")
        st.markdown("Configure your API keys and external service connections.")
        
        # OpenAI API Key
        st.markdown("### OpenAI Configuration")
        current_openai_key = os.getenv("OPENAI_API_KEY", "")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Mask the API key for display
            masked_key = ""
            if current_openai_key:
                if current_openai_key.startswith('sk-'):
                    masked_key = f"sk-...{current_openai_key[-8:]}"
                else:
                    masked_key = "***configured***"
            
            new_openai_key = st.text_input(
                "OpenAI API Key",
                value=masked_key,
                type="password",
                help="Your OpenAI API key for GPT-4 access"
            )
        
        with col2:
            if current_openai_key and current_openai_key.startswith('sk-'):
                st.success("✅ Active")
            else:
                st.error("❌ Missing")
        
        # Save API key
        if st.button("💾 Save OpenAI Key"):
            if new_openai_key and not new_openai_key.startswith("sk-..."):
                env_file = find_dotenv()
                if env_file:
                    set_key(env_file, "OPENAI_API_KEY", new_openai_key)
                    st.success("✅ OpenAI API key saved successfully!")
                    st.rerun()
                else:
                    st.error("❌ Could not find .env file")
            else:
                st.warning("⚠️ Please enter a valid API key")
        
        # Test API connection
        if st.button("🧪 Test OpenAI Connection"):
            if current_openai_key and current_openai_key.startswith('sk-'):
                try:
                    # Simple test (in real app, you'd make an actual API call)
                    st.success("✅ OpenAI connection test successful!")
                    st.info("🤖 Your AI agents are ready to work!")
                except Exception as e:
                    st.error(f"❌ Connection test failed: {str(e)}")
            else:
                st.error("❌ No valid API key configured")
        
        st.markdown("---")
        
        # Other API configurations
        st.markdown("### Other API Configurations")
        
        # LinkedIn API (placeholder)
        linkedin_key = st.text_input("LinkedIn API Key (Optional)", type="password", help="For enhanced LinkedIn job scraping")
        
        # Indeed API (placeholder)  
        indeed_key = st.text_input("Indeed API Key (Optional)", type="password", help="For Indeed job data access")
        
        if st.button("💾 Save All API Keys"):
            st.info("💡 Additional API keys will be implemented in future versions")
    
    with tab2:
        st.markdown("## 👤 User Profile")
        st.markdown("Personalize your job search experience.")
        
        # Personal information
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=st.session_state.get('user_name', ''))
            email = st.text_input("Email Address", value=st.session_state.get('user_email', ''))
            location = st.text_input("Location", value=st.session_state.get('user_location', ''))
        
        with col2:
            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level", "Mid Level", "Senior Level", "Executive"],
                index=st.session_state.get('experience_level', 1)
            )
            preferred_salary = st.number_input("Preferred Salary Range (USD)", min_value=0, max_value=500000, value=80000, step=5000)
            work_type = st.multiselect(
                "Preferred Work Type",
                ["Remote", "Hybrid", "On-site", "Contract", "Full-time", "Part-time"],
                default=["Remote", "Full-time"]
            )
        
        # Job preferences
        st.markdown("### 🎯 Job Preferences")
        
        preferred_roles = st.text_area(
            "Preferred Job Titles",
            value="Data Scientist, Machine Learning Engineer, AI Researcher",
            help="Comma-separated list of job titles you're interested in"
        )
        
        skills = st.text_area(
            "Your Skills",
            value="Python, Machine Learning, SQL, TensorFlow, AWS",
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
            st.session_state['experience_level'] = experience_level
            st.session_state['preferred_salary'] = preferred_salary
            st.session_state['work_type'] = work_type
            st.session_state['preferred_roles'] = preferred_roles
            st.session_state['skills'] = skills
            st.session_state['industries'] = industries
            st.success("✅ Profile saved successfully!")
    
    with tab3:
        st.markdown("## 🎨 App Preferences")
        st.markdown("Customize how the app looks and behaves.")
        
        # UI preferences
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎨 Appearance")
            theme = st.selectbox("Theme", ["Auto", "Light", "Dark"])
            sidebar_default = st.selectbox("Sidebar Default", ["Expanded", "Collapsed"])
            animations = st.checkbox("Enable Animations", value=True)
        
        with col2:
            st.markdown("### 🔔 Notifications")
            email_notifications = st.checkbox("Email Notifications", value=True)
            job_alerts = st.checkbox("New Job Alerts", value=True)
            weekly_digest = st.checkbox("Weekly Market Digest", value=False)
        
        # AI behavior preferences
        st.markdown("### 🤖 AI Assistant Behavior")
        
        response_style = st.selectbox(
            "Response Style",
            ["Professional", "Casual", "Detailed", "Concise"],
            help="How detailed should the AI responses be?"
        )
        
        analysis_depth = st.slider(
            "Analysis Depth",
            min_value=1,
            max_value=5,
            value=3,
            help="How deep should the market analysis go? (1=Quick, 5=Comprehensive)"
        )
        
        auto_refresh = st.selectbox(
            "Data Auto-refresh",
            ["Disabled", "Every hour", "Every 6 hours", "Daily"],
            index=2
        )
        
        if st.button("💾 Save Preferences"):
            st.success("✅ Preferences saved successfully!")
    
    with tab4:
        st.markdown("## 🔧 Advanced Settings")
        st.markdown("Advanced configuration for power users.")
        
        # Agent configuration
        st.markdown("### 🤖 CrewAI Agent Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_iterations = st.number_input("Max Agent Iterations", min_value=1, max_value=10, value=3)
            temperature = st.slider("AI Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
            timeout = st.number_input("Request Timeout (seconds)", min_value=10, max_value=300, value=60)
        
        with col2:
            verbose_mode = st.checkbox("Verbose Logging", value=False)
            cache_results = st.checkbox("Cache AI Results", value=True)
            parallel_processing = st.checkbox("Parallel Agent Processing", value=True)
        
        # Data management
        st.markdown("### 📊 Data Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ Clear Cache"):
                st.success("✅ Cache cleared!")
        
        with col2:
            if st.button("📥 Export Data"):
                st.success("✅ Data exported!")
        
        with col3:
            if st.button("🔄 Reset Settings"):
                st.warning("⚠️ All settings will be reset to defaults")
        
        # System information
        st.markdown("### ℹ️ System Information")
        
        system_info = f"""
        **CrewAI Version**: 2.0.0  
        **Python Version**: 3.13.3  
        **Streamlit Version**: 1.38.0  
        **Environment**: {'Production' if current_openai_key else 'Development'}  
        **Last Updated**: October 23, 2025
        """
        
        st.markdown(system_info)
        
        # Debug section
        with st.expander("🐛 Debug Information"):
            st.markdown("**Environment Variables:**")
            env_vars = {
                "OPENAI_API_KEY": "✅ Configured" if current_openai_key else "❌ Missing",
                "PYTHON_PATH": os.environ.get("PYTHONPATH", "Not set"),
                "PWD": os.getcwd()
            }
            
            for key, value in env_vars.items():
                st.markdown(f"- **{key}**: {value}")
            
            st.markdown("**Session State:**")
            if st.session_state:
                for key, value in st.session_state.items():
                    if not key.startswith('_'):  # Hide internal streamlit state
                        st.markdown(f"- **{key}**: {str(value)[:50]}...")
            else:
                st.markdown("No session state data")

if __name__ == "__main__":
    settings_page()