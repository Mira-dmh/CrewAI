"""
Home Page - Main landing page for CrewAI Job Search Assistant
"""

import streamlit as st

def home_page():
    """
    Homepage - Clean entry point to the multipage app with navigation to main sections
    """
    
    # Hero section
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem 2.5rem; max-width: 1000px; margin: 0 auto;">
        <h1 style="color: #2c3e50; margin-bottom: 1.5rem; font-size: 2.8em; font-weight: 700; line-height: 1.2;">
            Transform Your Career Journey<br>with AI Intelligence
        </h1>
        <p style="font-size: 1.2em; color: #6c757d; line-height: 1.8; font-weight: 400; max-width: 800px; margin: 0 auto;">
            Harness the power of multi-agent AI systems to discover opportunities, 
            analyze market trends, and prepare for success with unprecedented precision.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics/stats row
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-top: 4px solid #667eea;">
            <h2 style="color: #667eea; margin: 0; font-size: 2.5em; font-weight: 700;">8+</h2>
            <p style="color: #6c757d; margin: 0.5rem 0 0; font-size: 0.95em;">AI Agents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-top: 4px solid #f5576c;">
            <h2 style="color: #f5576c; margin: 0; font-size: 2.5em; font-weight: 700;">40+</h2>
            <p style="color: #6c757d; margin: 0.5rem 0 0; font-size: 0.95em;">Jobs Per Search</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-top: 4px solid #00f2fe;">
            <h2 style="color: #00f2fe; margin: 0; font-size: 2.5em; font-weight: 700;">92%</h2>
            <p style="color: #6c757d; margin: 0.5rem 0 0; font-size: 0.95em;">Accuracy Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-top: 4px solid #764ba2;">
            <h2 style="color: #764ba2; margin: 0; font-size: 2.5em; font-weight: 700;">24/7</h2>
            <p style="color: #6c757d; margin: 0.5rem 0 0; font-size: 0.95em;">AI Assistance</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main services section
    st.markdown("<div style='margin: 4rem 0 2.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h2 style="color: #2c3e50; font-size: 2.2em; font-weight: 600; margin-bottom: 0.8rem;">
            Our AI-Powered Services
        </h2>
        <p style="color: #6c757d; font-size: 1.1em; font-weight: 400;">
            Explore our comprehensive suite of career intelligence tools
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for the main dashboard sections
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 20px; padding: 2.5rem; color: white; height: 420px; 
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    position: relative; overflow: hidden;">
            <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; 
                        background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="margin-bottom: 1.5rem; color: white; font-size: 1.7em; font-weight: 600;">
                    Career Research
                </h3>
                <p style="color: rgba(255,255,255,0.95); line-height: 1.8; font-size: 1.05em; margin-bottom: 2rem;">
                    Discover new opportunities and explore different career directions with comprehensive 
                    role insights, industry trends, and AI-powered recommendations.
                </p>
                <div style="background: rgba(255,255,255,0.15); padding: 1.2rem; border-radius: 12px; 
                            backdrop-filter: blur(10px);">
                    <strong style="color: white; font-size: 1em; display: block; margin-bottom: 0.8rem;">
                        Key Features
                    </strong>
                    <ul style="color: rgba(255,255,255,0.95); font-size: 0.95em; margin: 0; padding-left: 1.2rem; 
                               line-height: 1.8;">
                        <li>Market trend analysis</li>
                        <li>Role requirements</li>
                        <li>Career pathways</li>
                        <li>Skill recommendations</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        if st.button("Start Exploring", key="explore_jobs", use_container_width=True, type="primary"):
            st.query_params.page = "job_search"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    border-radius: 20px; padding: 2.5rem; color: white; height: 420px; 
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 10px 40px rgba(240, 147, 251, 0.3);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    position: relative; overflow: hidden;">
            <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; 
                        background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="margin-bottom: 1.5rem; color: white; font-size: 1.7em; font-weight: 600;">
                    Job Search
                </h3>
                <p style="color: rgba(255,255,255,0.95); line-height: 1.8; font-size: 1.05em; margin-bottom: 2rem;">
                    Find targeted positions with advanced AI-powered search. Get verified job postings, 
                    market analytics, and quality insights from real LinkedIn data.
                </p>
                <div style="background: rgba(255,255,255,0.15); padding: 1.2rem; border-radius: 12px; 
                            backdrop-filter: blur(10px);">
                    <strong style="color: white; font-size: 1em; display: block; margin-bottom: 0.8rem;">
                        Key Features
                    </strong>
                    <ul style="color: rgba(255,255,255,0.95); font-size: 0.95em; margin: 0; padding-left: 1.2rem; 
                               line-height: 1.8;">
                        <li>Real LinkedIn scraping</li>
                        <li>Market analytics</li>
                        <li>Salary insights</li>
                        <li>Skills analysis</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        if st.button("Find Jobs Now", key="specific_jobs", use_container_width=True, type="primary"):
            st.query_params.page = "Specific_Jobs"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    border-radius: 20px; padding: 2.5rem; color: white; height: 420px; 
                    display: flex; flex-direction: column; justify-content: space-between;
                    box-shadow: 0 10px 40px rgba(79, 172, 254, 0.3);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    position: relative; overflow: hidden;">
            <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; 
                        background: rgba(255,255,255,0.1); border-radius: 50%;"></div>
            <div style="position: relative; z-index: 1;">
                <h3 style="margin-bottom: 1.5rem; color: white; font-size: 1.7em; font-weight: 600;">
                    Career Preparation
                </h3>
                <p style="color: rgba(255,255,255,0.95); line-height: 1.8; font-size: 1.05em; margin-bottom: 2rem;">
                    Optimize your resume and ace interviews with AI coaching. Get personalized feedback 
                    and strategic guidance tailored to your target roles.
                </p>
                <div style="background: rgba(255,255,255,0.15); padding: 1.2rem; border-radius: 12px; 
                            backdrop-filter: blur(10px);">
                    <strong style="color: white; font-size: 1em; display: block; margin-bottom: 0.8rem;">
                        Key Features
                    </strong>
                    <ul style="color: rgba(255,255,255,0.95); font-size: 0.95em; margin: 0; padding-left: 1.2rem; 
                               line-height: 1.8;">
                        <li>Resume optimization</li>
                        <li>Interview coaching</li>
                        <li>Custom feedback</li>
                        <li>Success strategies</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        if st.button("Get Prepared", key="resume_prep", use_container_width=True, type="primary"):
            st.query_params.page = "Resume_Prep"
            st.rerun()
    
    # How it works section
    st.markdown("<div style='margin: 5rem 0 3rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0 3rem;">
        <h2 style="color: #2c3e50; font-size: 2.2em; font-weight: 600; margin-bottom: 0.8rem;">
            How It Works
        </h2>
        <p style="color: #6c757d; font-size: 1.1em; font-weight: 400;">
            Get started in three simple steps
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for the steps
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2.5rem 2rem; background: white; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08); min-height: 300px;
                    display: flex; flex-direction: column; justify-content: center;
                    border-top: 4px solid #667eea; transition: all 0.3s ease;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        margin: 0 auto 1.5rem; color: white; font-size: 2.2em; font-weight: 700; 
                        box-shadow: 0 6px 20px rgba(102,126,234,0.4);">
                1
            </div>
            <h3 style="color: #2c3e50; margin-bottom: 1.2rem; font-size: 1.5em; font-weight: 600; line-height: 1.3;">
                Choose Service
            </h3>
            <p style="color: #6c757d; line-height: 1.8; font-size: 1.05em; margin: 0;">
                Select the AI service that matches your current career goals and needs.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2.5rem 2rem; background: white; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08); min-height: 300px;
                    display: flex; flex-direction: column; justify-content: center;
                    border-top: 4px solid #f5576c; transition: all 0.3s ease;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        margin: 0 auto 1.5rem; color: white; font-size: 2.2em; font-weight: 700; 
                        box-shadow: 0 6px 20px rgba(240,147,251,0.4);">
                2
            </div>
            <h3 style="color: #2c3e50; margin-bottom: 1.2rem; font-size: 1.5em; font-weight: 600; line-height: 1.3;">
                Provide Input
            </h3>
            <p style="color: #6c757d; line-height: 1.8; font-size: 1.05em; margin: 0;">
                Enter your requirements, preferences, and target criteria for personalized results.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2.5rem 2rem; background: white; border-radius: 16px; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08); min-height: 300px;
                    display: flex; flex-direction: column; justify-content: center;
                    border-top: 4px solid #00f2fe; transition: all 0.3s ease;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                        margin: 0 auto 1.5rem; color: white; font-size: 2.2em; font-weight: 700; 
                        box-shadow: 0 6px 20px rgba(79,172,254,0.4);">
                3
            </div>
            <h3 style="color: #2c3e50; margin-bottom: 1.2rem; font-size: 1.5em; font-weight: 600; line-height: 1.3;">
                Get AI Insights
            </h3>
            <p style="color: #6c757d; line-height: 1.8; font-size: 1.05em; margin: 0;">
                Receive intelligent analysis, recommendations, and actionable insights instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Technology section
    st.markdown("<div style='margin: 5rem 0 3rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0 3rem;">
        <h2 style="color: #2c3e50; font-size: 2.2em; font-weight: 600; margin-bottom: 0.8rem;">
            Technology Stack
        </h2>
        <p style="color: #6c757d; font-size: 1.1em; font-weight: 400; max-width: 700px; margin: 0 auto;">
            Built on cutting-edge technologies for maximum performance and reliability
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.8rem; background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%); 
                    border-radius: 12px; border: 2px solid rgba(102,126,234,0.2);">
            <div style="font-size: 1.2em; font-weight: 700; margin-bottom: 0.8rem; color: #667eea;">GPT-4</div>
            <strong style="color: #2c3e50; font-size: 1.05em; display: block; margin-bottom: 0.5rem;">OpenAI</strong>
            <p style="color: #6c757d; font-size: 0.9em; margin: 0;">Advanced Language Model</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.8rem; background: linear-gradient(135deg, rgba(240,147,251,0.1) 0%, rgba(245,87,108,0.1) 100%); 
                    border-radius: 12px; border: 2px solid rgba(240,147,251,0.2);">
            <div style="font-size: 1.2em; font-weight: 700; margin-bottom: 0.8rem; color: #f5576c;">CREW</div>
            <strong style="color: #2c3e50; font-size: 1.05em; display: block; margin-bottom: 0.5rem;">CrewAI</strong>
            <p style="color: #6c757d; font-size: 0.9em; margin: 0;">Multi-Agent Framework</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.8rem; background: linear-gradient(135deg, rgba(79,172,254,0.1) 0%, rgba(0,242,254,0.1) 100%); 
                    border-radius: 12px; border: 2px solid rgba(79,172,254,0.2);">
            <div style="font-size: 1.2em; font-weight: 700; margin-bottom: 0.8rem; color: #4facfe;">PLOT</div>
            <strong style="color: #2c3e50; font-size: 1.05em; display: block; margin-bottom: 0.5rem;">Plotly</strong>
            <p style="color: #6c757d; font-size: 0.9em; margin: 0;">Data Visualization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1.8rem; background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%); 
                    border-radius: 12px; border: 2px solid rgba(102,126,234,0.2);">
            <div style="font-size: 1.2em; font-weight: 700; margin-bottom: 0.8rem; color: #764ba2;">DOCK</div>
            <strong style="color: #2c3e50; font-size: 1.05em; display: block; margin-bottom: 0.5rem;">Docker</strong>
            <p style="color: #6c757d; font-size: 0.9em; margin: 0;">Container Platform</p>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("<div style='margin: 5rem 0 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h3 style="color: #2c3e50; font-size: 1.8em; font-weight: 600; margin-bottom: 1rem;">
            Ready to Transform Your Career?
        </h3>
        <p style="font-size: 1.2em; color: #6c757d; margin-bottom: 2rem; font-weight: 300;">
            Join thousands of professionals using AI to accelerate their career growth
        </p>
        <div style="margin: 2rem 0;">
            <a href="?page=Specific_Jobs" style="text-decoration: none;">
                <button style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; border: none; padding: 1rem 3rem; border-radius: 50px; 
                              font-size: 1.1em; font-weight: 600; cursor: pointer; 
                              box-shadow: 0 6px 25px rgba(102,126,234,0.4); 
                              transition: all 0.3s ease;">
                    Get Started Now→
                </button>
            </a>
        </div>
        <hr style="border: none; height: 1px; background: linear-gradient(to right, transparent, #dee2e6, transparent); margin: 3rem 0 2rem;">
        <p style="margin: 0; font-size: 0.9em; color: #6c757d; font-weight: 300;">
            <strong style="color: #2c3e50;">CrewAI Job Search Assistant</strong> | 
            Version 1.0.0 | 
            ©© 2025 All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    home_page()