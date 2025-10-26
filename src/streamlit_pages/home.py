"""
Home Page - Main landing page for CrewAI Job Search Assistant
"""

import streamlit as st

def home_page():
    """
    Homepage - Clean entry point to the multipage app with navigation to main sections
    """
    
    # Header section
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 3rem;">
        <h1 style="color: #1f77b4; margin-bottom: 1rem; font-size: 3em;">🤖 CrewAI Job Search Assistant</h1>
        <h2 style="color: #666; font-weight: 300; margin-bottom: 2rem; font-size: 1.5em;">
            Your AI-Powered Career Intelligence Platform
        </h2>
        <p style="font-size: 1.2em; color: #555; max-width: 700px; margin: 0 auto; line-height: 1.7;">
            Leverage the power of artificial intelligence to discover career opportunities, 
            find targeted job listings, and prepare for your next career move with confidence.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main dashboard sections
    st.markdown("## 🎯 Choose Your Path")
    st.markdown("Select one of the three main services to get started with your career journey:")
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Create three columns for the main dashboard sections
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 20px; padding: 2.5rem; color: white; height: 350px; 
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
                    transition: transform 0.3s ease;">
            <div>
                <h3 style="margin-bottom: 1.5rem; color: white; font-size: 1.5em;">💡 Explore Idea Jobs</h3>
                <p style="color: #f0f0f0; line-height: 1.7; font-size: 1em; margin-bottom: 2rem;">
                    Discover new career paths and related job opportunities. 
                    Get comprehensive introductions to different job roles and explore industry trends 
                    to find inspiration for your next career move.
                </p>
                <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                    <strong style="color: white; font-size: 0.95em;">Perfect for:</strong>
                    <ul style="color: #f0f0f0; font-size: 0.9em; margin: 0.5rem 0 0 1rem; list-style-type: none;">
                        <li>• Career exploration</li>
                        <li>• Role discovery</li>
                        <li>• Industry insights</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
        if st.button("🚀 Start Exploring", key="explore_jobs", use_container_width=True, type="primary"):
            try:
                st.switch_page("Info_Page")
            except Exception as e:
                st.error(f"Navigation error: {e}")
                st.info("💡 Please use the sidebar navigation to access 'Info Page'")
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    border-radius: 20px; padding: 2.5rem; color: white; height: 350px; 
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);
                    transition: transform 0.3s ease;">
            <div>
                <h3 style="margin-bottom: 1.5rem; color: white; font-size: 1.5em;">🎯 Specific Jobs</h3>
                <p style="color: #f0f0f0; line-height: 1.7; font-size: 1em; margin-bottom: 2rem;">
                    Find targeted job listings by specifying your preferences. 
                    Input job position, location, and company criteria to get 
                    relevant LinkedIn posts and job listings tailored to your needs.
                </p>
                <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                    <strong style="color: white; font-size: 0.95em;">Search by:</strong>
                    <ul style="color: #f0f0f0; font-size: 0.9em; margin: 0.5rem 0 0 1rem; list-style-type: none;">
                        <li>• Job position/title</li>
                        <li>• Geographic location</li>
                        <li>• Target companies</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
        if st.button("🔍 Find Jobs", key="specific_jobs", use_container_width=True, type="primary"):
            try:
                st.switch_page("Specific_Jobs")
            except Exception as e:
                st.error(f"Navigation error: {e}")
                st.info("🎯 Please use the sidebar navigation to access 'Specific Jobs'")
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    border-radius: 20px; padding: 2.5rem; color: white; height: 350px; 
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 8px 32px rgba(79, 172, 254, 0.3);
                    transition: transform 0.3s ease;">
            <div>
                <h3 style="margin-bottom: 1.5rem; color: white; font-size: 1.5em;">📝 Resume & Interview Prep</h3>
                <p style="color: #f0f0f0; line-height: 1.7; font-size: 1em; margin-bottom: 2rem;">
                    Get AI-powered assistance in building compelling resumes 
                    and preparing for interviews. Receive personalized feedback 
                    and actionable recommendations for your applications.
                </p>
                <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                    <strong style="color: white; font-size: 0.95em;">Tools include:</strong>
                    <ul style="color: #f0f0f0; font-size: 0.9em; margin: 0.5rem 0 0 1rem; list-style-type: none;">
                        <li>• Resume optimization</li>
                        <li>• Interview practice</li>
                        <li>• Industry tips</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
        if st.button("📚 Get Prepared", key="resume_prep", use_container_width=True, type="primary"):
            try:
                st.switch_page("Resume_Prep")
            except Exception as e:
                st.error(f"Navigation error: {e}")
                st.info("📝 Please use the sidebar navigation to access 'Resume Prep'")
    
    # How to get started section
    st.markdown("---")
    st.markdown("## 🚀 How to Get Started")
    
    st.markdown("### Simple 3-Step Process")
    st.markdown("Get started with your AI-powered job search in minutes")
    
    # Create columns for the steps
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 1️⃣ Choose Your Path")
        st.markdown("Select one of the three main services above based on your needs and career goals.")
    
    with col2:
        st.markdown("#### 2️⃣ Navigate to Page")
        st.markdown("Use the sidebar navigation to access your chosen service and start exploring.")
    
    with col3:
        st.markdown("#### 3️⃣ Let AI Assist")
        st.markdown("Our intelligent agents will provide personalized insights and recommendations.")

    st.markdown("---")

    # Footer
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 2rem 0;">
        <h4 style="color: #1f77b4; margin-bottom: 1rem;">Ready to Transform Your Career?</h4>
        <p style="font-size: 1.1em; margin-bottom: 1rem;">
            Choose one of the options above to get started with AI-powered job search assistance.
        </p>
        <hr style="border: none; height: 1px; background: linear-gradient(to right, transparent, #dee2e6, transparent); margin: 2rem 0;">
        <p style="margin: 0; font-size: 0.9em;">
            <strong>CrewAI Job Search Assistant</strong> | 
            Powered by OpenAI GPT-4 & CrewAI | 
            Docker-ready deployment
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    home_page()