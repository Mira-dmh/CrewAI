"""
Job Search Hub - Job Market Research Platform
Displays comprehensive job market insights and data
"""

import streamlit as st

# Import separate page functions
from .info_page import info_page as job_market_insights_core

def job_market_insights():
    """Job Market Research Dashboard - Info Section"""
    
    # Call the imported info_page function
    job_market_insights_core()

def job_search_page():
    """
    Complete Job Search Hub - Main page function for multipage app
    """
    
    
    # Display job market insights directly
    job_market_insights()
    
    # Footer with navigation tips
    st.markdown("---")
    with st.expander("ℹ How to Use This Page"):
        st.markdown("""
        ###  Market Insights
        View comprehensive job market data and trends from AI-generated research reports.
        
        **Pro Tip**: Use the insights to understand market trends and discover opportunities!
        """)

# Main function for standalone use
def main():
    """Main function for Streamlit app"""
    st.set_page_config(
        page_title="Job Search Hub", 
        page_icon="", 
        layout="wide"
    )
    
    job_search_page()

if __name__ == "__main__":
    main()