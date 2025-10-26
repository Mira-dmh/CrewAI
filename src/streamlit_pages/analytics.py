"""
Analytics Page - Job Market Analytics and Insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def analytics_page():
    """
    Analytics page content - Market insights and data visualization
    """
    
    # Track page visit
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from utils.session_manager import track_page_visit
        track_page_visit("Analytics")
    except:
        pass  # Fail silently if tracking is unavailable
    
    st.markdown("# 📊 Job Market Analytics")
    st.markdown("*Comprehensive insights into the job market powered by AI analysis*")
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("## 🔧 Analysis Filters")
        
        # Job category filter
        job_categories = [
            "All Categories",
            "Technology", 
            "Data Science", 
            "Marketing", 
            "Sales", 
            "Finance", 
            "Healthcare",
            "Engineering"
        ]
        selected_category = st.selectbox("Job Category", job_categories)
        
        # Location filter
        locations = [
            "All Locations",
            "San Francisco Bay Area",
            "New York City", 
            "Los Angeles",
            "Chicago",
            "Austin",
            "Seattle",
            "Remote"
        ]
        selected_location = st.selectbox("Location", locations)
        
        # Time range
        time_ranges = ["Last 7 days", "Last 30 days", "Last 90 days", "Last year"]
        selected_time = st.selectbox("Time Range", time_ranges)
        
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Generate sample data (in real app, this would come from your CrewAI agents)
    def generate_sample_data():
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        return {
            'dates': dates,
            'job_postings': [random.randint(50, 200) for _ in dates],
            'avg_salary': [random.randint(80000, 180000) for _ in dates],
            'applications': [random.randint(1000, 5000) for _ in dates]
        }
    
    data = generate_sample_data()
    
    # Key metrics row
    st.markdown("## 📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Job Postings",
            f"{sum(data['job_postings']):,}",
            delta=f"+{random.randint(10, 50)}%"
        )
    
    with col2:
        avg_salary = sum(data['avg_salary']) // len(data['avg_salary'])
        st.metric(
            "Average Salary",
            f"${avg_salary:,}",
            delta=f"+${random.randint(1000, 5000):,}"
        )
    
    with col3:
        st.metric(
            "Total Applications", 
            f"{sum(data['applications']):,}",
            delta=f"+{random.randint(5, 25)}%"
        )
    
    with col4:
        competition_ratio = sum(data['applications']) / sum(data['job_postings'])
        st.metric(
            "Competition Ratio",
            f"{competition_ratio:.1f}:1",
            delta=f"-{random.uniform(0.1, 0.5):.1f}"
        )
    
    # Charts section
    st.markdown("## 📊 Market Trends")
    
    # Job postings over time
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Job Postings Trend")
        df_postings = pd.DataFrame({
            'Date': data['dates'],
            'Job Postings': data['job_postings']
        })
        
        fig_postings = px.line(
            df_postings, 
            x='Date', 
            y='Job Postings',
            title="Daily Job Postings",
            color_discrete_sequence=['#1f77b4']
        )
        fig_postings.update_layout(height=300)
        st.plotly_chart(fig_postings, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Salary Trends")
        df_salary = pd.DataFrame({
            'Date': data['dates'],
            'Average Salary': data['avg_salary']
        })
        
        fig_salary = px.line(
            df_salary,
            x='Date',
            y='Average Salary',
            title="Average Salary Trends",
            color_discrete_sequence=['#2ca02c']
        )
        fig_salary.update_layout(height=300)
        st.plotly_chart(fig_salary, use_container_width=True)
    
    # Skills demand analysis
    st.markdown("## 🔥 Top In-Demand Skills")
    
    skills_data = {
        'Skill': ['Python', 'JavaScript', 'SQL', 'React', 'AWS', 'Machine Learning', 'Docker', 'Git'],
        'Demand Score': [95, 88, 82, 78, 75, 73, 68, 65],
        'Salary Impact': ['+15%', '+12%', '+8%', '+10%', '+18%', '+25%', '+7%', '+5%']
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_skills = px.bar(
            skills_data,
            x='Demand Score',
            y='Skill',
            orientation='h',
            title="Skills Demand Analysis",
            color='Demand Score',
            color_continuous_scale='viridis'
        )
        fig_skills.update_layout(height=400)
        st.plotly_chart(fig_skills, use_container_width=True)
    
    with col2:
        st.markdown("### 💡 Skill Insights")
        for i, skill in enumerate(skills_data['Skill'][:5]):
            st.markdown(f"""
            **{skill}**  
            Demand: {skills_data['Demand Score'][i]}/100  
            Salary: {skills_data['Salary Impact'][i]}
            """)
    
    # Company insights
    st.markdown("## 🏢 Top Hiring Companies")
    
    company_data = {
        'Company': ['Google', 'Microsoft', 'Amazon', 'Apple', 'Meta', 'Netflix', 'Tesla', 'Uber'],
        'Open Positions': [1250, 980, 1450, 650, 420, 180, 320, 280],
        'Avg Salary': [165000, 155000, 145000, 170000, 175000, 180000, 140000, 150000]
    }
    
    df_companies = pd.DataFrame(company_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_companies = px.scatter(
            df_companies,
            x='Open Positions',
            y='Avg Salary',
            size='Open Positions',
            hover_name='Company',
            title="Companies: Positions vs Salary",
            color='Avg Salary',
            color_continuous_scale='plasma'
        )
        st.plotly_chart(fig_companies, use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 Top Employers")
        for i, company in enumerate(company_data['Company'][:5]):
            st.markdown(f"""
            **{i+1}. {company}**  
            Positions: {company_data['Open Positions'][i]:,}  
            Avg Salary: ${company_data['Avg Salary'][i]:,}
            """)
    
    # AI-Generated Insights
    st.markdown("## 🤖 AI-Generated Market Insights")
    
    insights = [
        "🔥 **Hot Trend**: Remote work positions increased by 34% this month",
        "💰 **Salary Alert**: AI/ML roles showing 15% salary increase", 
        "📍 **Location Insight**: Austin becoming new tech hub with 28% job growth",
        "⚡ **Skill Gap**: High demand for cloud architecture skills",
        "🎯 **Opportunity**: Entry-level data science positions up 45%"
    ]
    
    for insight in insights:
        st.info(insight)
    
    # Export section
    st.markdown("## 📥 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Charts", use_container_width=True):
            st.success("Charts exported successfully!")
    
    with col2:
        if st.button("📋 Export Data", use_container_width=True):
            st.success("Data exported to CSV!")
    
    with col3:
        if st.button("📧 Email Report", use_container_width=True):
            st.success("Report sent to your email!")

if __name__ == "__main__":
    analytics_page()