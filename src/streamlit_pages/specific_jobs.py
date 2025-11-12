"""
Specific Jobs Page - LinkedIn Job Search with AI-Powered Analysis
Streamlined and organized interface for targeted job discovery
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from io import BytesIO
import pandas as pd

# Try to import plotly for analytics visualizations
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Import CrewAI components
try:
    from crewai import LLM
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from Crew.linkedin_search_crew import LinkedInSearchCrew
    CREWAI_AVAILABLE = True
    IMPORT_ERROR = None
except (ImportError, Exception) as e:
    CREWAI_AVAILABLE = False
    IMPORT_ERROR = str(e)


# ============================================================================
# MAIN PAGE
# ============================================================================

def get_latest_session_folder():
    """Get the most recent session folder from LinkedIn outputs"""
    linkedin_output_dir = "src/outputs/linkedin"
    
    if not os.path.exists(linkedin_output_dir):
        return None
    
    # Get all subdirectories (session folders)
    try:
        session_folders = [
            f for f in os.listdir(linkedin_output_dir)
            if os.path.isdir(os.path.join(linkedin_output_dir, f))
        ]
        
        if not session_folders:
            return None
        
        # Get the most recently modified folder
        session_paths = [os.path.join(linkedin_output_dir, f) for f in session_folders]
        latest_session = max(session_paths, key=os.path.getmtime)
        
        return latest_session
    except Exception:
        return None


def specific_jobs_page():
    """Main entry point for the specific jobs search page"""
    
    # Page Header
    st.markdown("# 🎯 LinkedIn Job Search")
    st.markdown("*AI-powered job discovery with real-time market analysis*")
    st.markdown("---")
    
    # Check system readiness
    system_ready, error_msg = check_system_status()
    
    if not system_ready:
        display_system_error(error_msg)
        return
    
    # Main tabs for organized content
    tab1, tab2, tab3 = st.tabs([
        "🎯 Advanced Search",
        "� Job Market Analytics",
        "�📚 Search History"
    ])
    
    with tab1:
        render_advanced_search()
    
    with tab2:
        render_job_market_analytics()
    
    with tab3:
        render_search_history()
    
    # Footer
    render_page_footer()


# ============================================================================
# SYSTEM STATUS
# ============================================================================

def check_system_status():
    """Check if all required components are available"""
    if not CREWAI_AVAILABLE:
        return False, f"CrewAI not available: {IMPORT_ERROR}"
    
    if not os.getenv("OPENAI_API_KEY"):
        return False, "OpenAI API key not configured"
    
    return True, None


def display_system_error(error_msg):
    """Display system configuration errors with setup instructions"""
    st.error("⚠️ **System Configuration Required**")
    st.error(error_msg)
    
    with st.expander("🔧 Setup Instructions", expanded=True):
        if "CrewAI" in error_msg:
            st.markdown("""
            ### Install CrewAI Dependencies
            ```bash
            pip install crewai crewai-tools
            ```
            """)
        
        if "API key" in error_msg:
            st.markdown("""
            ### Configure OpenAI API Key
            1. Create a `.env` file in the project root
            2. Add your API key:
            ```
            OPENAI_API_KEY=sk-your-key-here
            SERPER_API_KEY=your-serper-key-here
            ```
            3. Restart the application
            """)
    
    # Diagnostic info
    with st.expander("🔍 Diagnostic Information"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**CrewAI Status:**")
            st.markdown(f"- Available: {'✅' if CREWAI_AVAILABLE else '❌'}")
            if IMPORT_ERROR:
                st.code(IMPORT_ERROR, language="text")
        
        with col2:
            st.markdown("**Environment Variables:**")
            st.markdown(f"- OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")
            st.markdown(f"- SERPER_API_KEY: {'✅ Set' if os.getenv('SERPER_API_KEY') else '⚠️ Optional'}")


# ============================================================================
# ADVANCED SEARCH TAB
# ============================================================================

def render_advanced_search():
    """Render the advanced search form with all filters"""
    st.markdown("### 🎯 Advanced Search Options")
    st.markdown("*Use detailed filters for precise job discovery*")
    st.markdown("")
    
    with st.form("advanced_search_form"):
        # Basic info section
        st.markdown("#### 📋 Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input(
                "Job Title *",
                placeholder="e.g., Machine Learning Engineer"
            )
            company = st.text_input(
                "Company (Optional)",
                placeholder="e.g., Google, Microsoft"
            )
        
        with col2:
            location = st.text_input(
                "Location",
                placeholder="e.g., New York, Remote"
            )
            experience = st.selectbox(
                "Experience Level",
                ["Any", "Entry Level", "Mid Level", "Senior Level", "Executive"]
            )
        
        # Filters section
        st.markdown("---")
        st.markdown("#### 🔧 Additional Filters")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            job_type = st.selectbox(
                "Job Type",
                ["Any", "Full-time", "Part-time", "Contract", "Freelance"]
            )
        
        with col4:
            remote_option = st.selectbox(
                "Remote Work",
                ["Any", "Remote", "Hybrid", "On-site"]
            )
        
        with col5:
            industry = st.selectbox(
                "Industry",
                ["Any", "Technology", "Finance", "Healthcare", "Marketing", "Education"]
            )
        
        # Submit button
        st.markdown("---")
        submitted = st.form_submit_button(
            "🔍 Search with Filters",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if not job_title:
                st.error("❌ Job title is required")
            else:
                # Build search params
                search_params = {
                    "company": company,
                    "experience_level": experience,
                    "job_type": job_type,
                    "remote_option": remote_option,
                    "industry": industry
                }
                
                # Show search summary
                st.markdown("---")
                st.markdown("#### 📊 Your Search Criteria:")
                display_search_summary(job_title, location, search_params)
                
                # Execute search
                st.markdown("---")
                execute_linkedin_search(job_title, location, search_params)


# ============================================================================
# SEARCH HISTORY TAB
# ============================================================================

def render_search_history():
    """Render the search history interface"""
    st.markdown("### 📚 Your Search History")
    st.markdown("*View and reload previous LinkedIn searches*")
    st.markdown("")
    
    # Get all search results
    all_results = LinkedInSearchCrew.get_all_search_results()
    
    if not all_results:
        st.info("📝 No search history yet. Run a search to get started!")
        return
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total Searches", len(all_results))
    
    with col2:
        latest = LinkedInSearchCrew.load_latest_search_results()
        if latest:
            metadata = latest.get("search_metadata", {})
            st.metric("🔍 Latest Search", metadata.get("job_title", "N/A"))
    
    with col3:
        if st.button("🔄 Refresh History", use_container_width=True):
            st.rerun()
    
    # Display search history
    st.markdown("---")
    st.markdown("#### 📋 Recent Searches")
    
    for i, file_path in enumerate(all_results[:10], 1):
        results = LinkedInSearchCrew.load_search_results_by_file(file_path)
        if results:
            display_search_history_item(i, file_path, results)


def display_search_history_item(index, file_path, results):
    """Display a single search history item"""
    metadata = results.get("search_metadata", {})
    job_title = metadata.get("job_title", "Unknown")
    location = metadata.get("location", "Any")
    timestamp = metadata.get("search_timestamp", "")
    
    try:
        dt = datetime.fromisoformat(timestamp)
        display_time = dt.strftime("%Y-%m-%d %H:%M")
    except:
        display_time = "Unknown time"
    
    with st.expander(f"**{index}.** {job_title} | {display_time}"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**📋 Position:** {job_title}")
            st.markdown(f"**📍 Location:** {location}")
            st.markdown(f"**⏰ Time:** {display_time}")
        
        with col2:
            filename = os.path.basename(file_path)
            st.markdown(f"**📄 File:** `{filename}`")
            
            if st.button(f"📂 Load Results", key=f"view_{index}", use_container_width=True):
                st.markdown("---")
                crew_output = results.get("crew_output", "No data available")
                output_str = str(crew_output)
                st.markdown("### 📊 Search Results:")
                if len(output_str) > 1000:
                    st.text(output_str[:1000] + "...")
                    with st.expander("View Full Output"):
                        st.text(output_str)
                else:
                    st.text(output_str)


# ============================================================================
# SEARCH EXECUTION
# ============================================================================

def execute_linkedin_search(job_title, location="", search_params=None):
    """Execute the LinkedIn search with AI agents"""
    
    st.markdown("### 🤖 AI Search in Progress")
    st.markdown("")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize
        status_text.text("🔧 Initializing AI agents...")
        progress_bar.progress(20)
        
        llm = LLM(model="gpt-4o-mini", temperature=0.7)
        linkedin_crew = LinkedInSearchCrew(llm=llm)
        
        # Start search
        status_text.text(f"🌐 Searching LinkedIn for '{job_title}'...")
        progress_bar.progress(40)
        
        # Execute
        status_text.text("🤖 AI agents analyzing job market...")
        progress_bar.progress(60)
        
        if search_params:
            result = linkedin_crew.search_jobs(
                job_title=job_title,
                location=location,
                **search_params
            )
        else:
            result = linkedin_crew.search_jobs(
                job_title=job_title,
                location=location
            )
        
        # Complete
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(100)
        
        # Clear progress
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        st.markdown("---")
        display_search_results(job_title, location, result)
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        
        st.error(f"❌ **Search Error:** {str(e)}")
        st.error(f"**Error Type:** {type(e).__name__}")
        
        with st.expander("🔍 View Error Details"):
            import traceback
            st.code(traceback.format_exc(), language="python")
        
        display_troubleshooting_tips()


# ============================================================================
# RESULTS DISPLAY
# ============================================================================

def display_search_results(job_title, location, result):
    """Display formatted search results in organized tabs"""
    
    st.success(f"✅ **Search Complete:** {job_title}" + (f" in {location}" if location else ""))
    
    # Results tabs
    tabs = st.tabs([
        "💼 Job Postings",
        "📈 Market Trends",
        "✅ Verification",
        "📄 Raw Data"
    ])
    
    with tabs[0]:
        display_job_postings_section(result)  # Pass runtime result
    
    with tabs[1]:
        display_market_trends_section()
    
    with tabs[2]:
        display_verification_section()
    
    with tabs[3]:
        st.markdown("### 🤖 Complete AI Output")
        st.text_area("Raw Result", str(result), height=400)
    
    # Metrics footer
    st.markdown("---")
    render_search_metrics()


def display_job_postings_section(result=None):
    """Load and display job postings from JSON or runtime result
    
    Optimized to show top 50 latest posts with enhanced information:
    - Short intro summary
    - Company business description  
    - Job role description
    - Direct link to original post
    """
    # Priority 1: Use runtime result for real-time data
    postings = None
    if result:
        # Try to extract postings from crew result
        if isinstance(result, dict):
            postings = result.get("job_postings")
        elif hasattr(result, 'raw'):
            # CrewAI output object
            try:
                raw_data = json.loads(result.raw) if isinstance(result.raw, str) else result.raw
                postings = raw_data.get("job_postings") if isinstance(raw_data, dict) else None
            except:
                pass
    
    # Priority 2: Fallback to saved JSON file
    job_file = "src/outputs/linkedin/job_postings.json"
    if postings is None and os.path.exists(job_file):
        try:
            with open(job_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            postings = data.get("job_postings") if isinstance(data, dict) else None
        except Exception as e:
            st.error(f"❌ Error loading job postings: {e}")
            return
    
    if not postings:
        st.info("💡 Job postings will appear here after the search completes")
        return
    
    # Sort by date (latest first) and limit to 50
    def safe_date_parse(date_str):
        """Parse date without external dependencies"""
        if not date_str:
            return datetime.min
        try:
            # Try ISO format
            if 'T' in str(date_str):
                return datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
            # Try basic format
            return datetime.strptime(str(date_str).split()[0], '%Y-%m-%d')
        except:
            return datetime.min
    
    try:
        sorted_postings = sorted(
            postings,
            key=lambda p: safe_date_parse(p.get('date_posted', '')),
            reverse=True
        )
    except:
        sorted_postings = list(postings)
    
    # Limit to top 50 latest for file export
    limited_postings = sorted_postings[:50]
    
    # Default display: top 10
    display_count = st.session_state.get('job_display_count', 10)
    display_postings = limited_postings[:display_count]
    
    st.markdown(f"### 📋 Job Listings (Showing {len(display_postings)} of {len(limited_postings)})")
    st.markdown("")
    
    # Export buttons and display controls
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        if len(limited_postings) > 0:
            try:
                import pandas as pd
                # Prepare data for export (all 50 jobs)
                df = pd.DataFrame(limited_postings)
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    "📥 Download CSV (50 jobs)",
                    csv,
                    file_name=f"linkedin_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.caption(f"CSV export unavailable: {e}")
    
    with col2:
        if len(limited_postings) > 0:
            try:
                import pandas as pd
                from io import BytesIO
                # Prepare Excel export (all 50 jobs)
                df = pd.DataFrame(limited_postings)
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='LinkedIn Jobs')
                buffer.seek(0)
                st.download_button(
                    "📊 Download Excel (50 jobs)",
                    buffer,
                    file_name=f"linkedin_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.caption(f"Excel export unavailable: {e}")
    
    with col3:
        # Display count selector
        count_options = [10, 20, 30, 50]
        selected = st.selectbox(
            "Display",
            count_options,
            index=count_options.index(display_count) if display_count in count_options else 0,
            key="display_selector"
        )
        if selected != display_count:
            st.session_state['job_display_count'] = selected
            st.rerun()
    
    with col4:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    # AI Assistant Chat Box
    with st.expander("💬 AI Assistant - Ask for custom analysis or exports", expanded=False):
        st.markdown("**Ask the AI to help you with:**")
        st.markdown("""
        - Filter jobs by specific criteria
        - Export customized data
        - Analyze job trends
        - Generate reports
        - Sort or rank jobs
        """)
        
        user_instruction = st.text_area(
            "Enter your instruction:",
            placeholder="Example: Export only remote jobs with salary > 100k\nExample: Show me jobs from top tech companies\nExample: Rank jobs by best benefits",
            height=100,
            key="ai_instruction_input"
        )
        
        col_a, col_b = st.columns([1, 4])
        with col_a:
            execute_btn = st.button("🚀 Execute", type="primary", use_container_width=True)
        with col_b:
            if execute_btn and user_instruction:
                st.info("🤖 AI Assistant is processing your request...")
                # Process AI instruction
                process_ai_instruction(user_instruction, limited_postings)
            elif execute_btn:
                st.warning("⚠️ Please enter an instruction first")
    
    st.markdown("---")
    
    # Display jobs
    for i, job in enumerate(display_postings, 1):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            # Extract fields with multiple fallback keys
            job_title = job.get('job_title') or job.get('title') or 'Job Title'
            company = job.get('company_name') or job.get('company') or 'Company'
            location = job.get('location') or job.get('job_location') or 'Location'
            posted = job.get('date_posted') or job.get('posted') or 'Recent'
            employment_type = job.get('employment_type')
            experience_level = job.get('experience_level')
            job_url = job.get('job_url') or job.get('url') or job.get('link')
            
            # Date information - distinguish original post vs repost
            is_repost = job.get('is_repost', False)
            repost_date = job.get('repost_date')
            date_info_raw = job.get('date_info_raw')
            
            # Build date display string
            date_display = ""
            if is_repost:
                if posted and repost_date:
                    date_display = f"📅 Originally: {posted} | 🔄 Reposted: {repost_date}"
                elif repost_date:
                    date_display = f"🔄 Reposted: {repost_date}"
                elif date_info_raw:
                    date_display = f"🔄 {date_info_raw}"
                else:
                    date_display = f"🔄 Reposted: {posted}"
            else:
                date_display = f"📅 Posted: {posted}"
            
            # NEW: Enhanced information for job seekers
            # 1. Short intro/summary
            short_intro = job.get('short_intro') or job.get('summary')
            if not short_intro and job_title and company:
                short_intro = f"{employment_type or 'Position'} at {company} in {location}"
            
            # 2. Company business description
            company_desc = (job.get('company_description') or 
                          job.get('company_overview') or 
                          job.get('about_company'))
            
            # 3. Job role description
            job_desc = (job.get('job_description') or 
                       job.get('description') or 
                       job.get('role_description'))
            
            with col1:
                st.markdown(f"#### {i}. {job_title}")
                st.markdown(f"🏢 **Company:** {company}")
                st.markdown(f"📍 **Location:** {location}")
                
                # Display employment info in one line
                info_parts = []
                if employment_type:
                    info_parts.append(f"💼 {employment_type}")
                if experience_level:
                    info_parts.append(f"⭐ {experience_level}")
                if info_parts:
                    st.caption(" | ".join(info_parts))
                
                # NEW: Short intro
                if short_intro:
                    st.markdown(f"**📝 Summary:** {short_intro}")
                
                # NEW: Company business intro (truncated for readability)
                if company_desc:
                    desc_preview = (company_desc[:300] + '...') if len(str(company_desc)) > 300 else company_desc
                    with st.expander("🏢 About Company"):
                        st.write(desc_preview)
                
                # NEW: Job role description (truncated for readability)
                if job_desc:
                    role_preview = (job_desc[:500] + '...') if len(str(job_desc)) > 500 else job_desc
                    with st.expander("💼 Role Details"):
                        st.write(role_preview)
            
            with col2:
                st.markdown(f"**{date_display}**")
                if job_url:
                    st.link_button("🔗 View Job", job_url, use_container_width=True, type="primary")
                else:
                    st.caption("🔗 Link unavailable")
            
            st.divider()


def display_market_trends_section():
    """Load and display market trends from JSON"""
    trends_file = "src/outputs/linkedin/market_trends.json"
    
    if not os.path.exists(trends_file):
        st.info("💡 Market trends will appear here after the search completes")
        return
    
    try:
        with open(trends_file, 'r') as f:
            data = json.load(f)
        
        # Market overview
        if "market_overview" in data:
            st.markdown("### 📊 Market Overview")
            overview = data["market_overview"]
            
            cols = st.columns(3)
            with cols[0]:
                st.metric("🎯 Market Health", overview.get("market_health", "N/A").upper())
            with cols[1]:
                st.metric("📅 Analysis Date", overview.get("analysis_date", "N/A"))
            with cols[2]:
                st.metric("💼 Position", overview.get("job_title", "N/A"))
            
            st.markdown("")
        
        # Salary trends
        if "salary_trends" in data and "salary_ranges" in data["salary_trends"]:
            st.markdown("### 💰 Salary Ranges")
            salary_data = data["salary_trends"]["salary_ranges"]
            
            cols = st.columns(3)
            levels = ["entry_level", "mid_level", "senior_level"]
            
            for idx, level in enumerate(levels):
                if level in salary_data:
                    info = salary_data[level]
                    with cols[idx]:
                        level_name = level.replace('_', ' ').title()
                        st.markdown(f"**{level_name}**")
                        if isinstance(info, dict):
                            st.markdown(f"💵 ${info.get('min', 0):,} - ${info.get('max', 0):,}")
                            st.markdown(f"📊 Avg: ${info.get('average', 0):,}")
            
            st.markdown("")
        
        # Top skills
        if "skills_analysis" in data:
            st.markdown("### 💡 Top In-Demand Skills")
            skills = data["skills_analysis"].get("top_demanded_skills", [])
            
            if skills:
                cols = st.columns(2)
                for idx, skill in enumerate(skills[:8]):
                    with cols[idx % 2]:
                        if isinstance(skill, dict):
                            st.markdown(f"**{skill.get('skill_name', 'N/A')}**")
                            st.caption(f"Demand: {skill.get('demand_frequency', 'N/A')}")
                        else:
                            st.markdown(f"• {skill}")
        
    except json.JSONDecodeError as e:
        st.warning(f"⚠️ JSON parsing error: {e}")
    except Exception as e:
        st.error(f"❌ Error loading market trends: {e}")


def display_verification_section():
    """Load and display verification report from JSON"""
    verify_file = "src/outputs/linkedin/verification_report.json"
    
    if not os.path.exists(verify_file):
        st.info("💡 Verification report will appear here after the search completes")
        return
    
    try:
        with open(verify_file, 'r') as f:
            data = json.load(f)
        
        # Status metrics
        cols = st.columns(3)
        
        with cols[0]:
            status = data.get("verification_status", "unknown")
            emoji = "✅" if status == "verified" else "⚠️"
            st.metric("📋 Status", f"{emoji} {status.upper()}")
        
        with cols[1]:
            st.metric("📊 Accuracy", data.get("accuracy_score", "N/A"))
        
        with cols[2]:
            confidence = data.get("confidence_level", "N/A")
            emoji_conf = "🟢" if confidence == "high" else "🟡" if confidence == "medium" else "🔴"
            st.metric("🎯 Confidence", f"{emoji_conf} {str(confidence).upper()}")
        
        st.markdown("")
        
        # Verified fields
        if "verified_fields" in data:
            verified = data["verified_fields"]
            if verified:
                st.markdown("### ✅ Verified Data Points")
                cols = st.columns(3)
                for idx, field in enumerate(verified):
                    with cols[idx % 3]:
                        st.markdown(f"✓ {field}")
        
        # Issues
        if "flagged_issues" in data:
            issues = data["flagged_issues"]
            if issues:
                st.markdown("### ⚠️ Flagged Issues")
                for issue in issues:
                    st.warning(issue)
        
        # Corrections
        if "corrections" in data:
            corrections = data["corrections"]
            if corrections:
                st.markdown("### 🔧 Suggested Corrections")
                for correction in corrections:
                    st.info(correction)
        
    except json.JSONDecodeError as e:
        st.warning(f"⚠️ JSON parsing error: {e}")
    except Exception as e:
        st.error(f"❌ Error loading verification: {e}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def display_search_summary(job_title, location, search_params):
    """Display a formatted search summary"""
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown("**📋 Position**")
        st.markdown(job_title)
    
    with cols[1]:
        st.markdown("**📍 Location**")
        st.markdown(location or "Any")
    
    with cols[2]:
        st.markdown("**⭐ Experience**")
        st.markdown(search_params.get("experience_level", "Any"))
    
    with cols[3]:
        st.markdown("**💼 Type**")
        st.markdown(search_params.get("job_type", "Any"))


def render_search_metrics():
    """Display search performance metrics"""
    cols = st.columns(4)
    
    with cols[0]:
        st.metric("🤖 AI Agents", "4 Active")
    
    with cols[1]:
        st.metric("🌐 Data Source", "LinkedIn")
    
    with cols[2]:
        st.metric("⚡ Analysis", "Real-time")
    
    with cols[3]:
        st.metric("💾 Output", "JSON")


def display_troubleshooting_tips():
    """Display troubleshooting information"""
    st.markdown("### 💡 Troubleshooting Tips")
    st.markdown("""
    - ✅ Verify your OpenAI API key has available credits
    - ✅ Check SERPER_API_KEY is configured in .env
    - ✅ Ensure stable internet connection
    - ✅ Try with a simpler job title first
    - ✅ Check the terminal output for detailed logs
    """)


def process_ai_instruction(instruction: str, job_postings: list):
    """
    Process user AI instructions to manipulate job data
    
    Args:
        instruction: User's natural language instruction
        job_postings: List of job posting dictionaries
    """
    try:
        import pandas as pd
        from io import BytesIO
        import openai
        import os
        
        # Use OpenAI to interpret the instruction
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("❌ OpenAI API key not found. Please configure it in .env file.")
            return
        
        client = openai.OpenAI(api_key=api_key)
        
        # Create a prompt for GPT to generate filtering/processing logic
        system_prompt = """You are a data processing assistant for LinkedIn job postings. 
        Analyze the user's instruction and provide Python code to filter, sort, or process the job data.
        
        The data is in a list called 'job_postings' where each item is a dictionary with fields like:
        - job_title, company_name, location, date_posted, employment_type, experience_level
        - job_url, salary, benefits, remote_option, etc.
        
        Return ONLY valid Python code that:
        1. Filters/processes 'job_postings' and stores result in 'filtered_jobs'
        2. Optionally sets 'export_format' to 'csv' or 'excel' if user wants export
        3. Optionally sets 'display_message' with a summary message
        
        Example code format:
        ```python
        # Filter remote jobs
        filtered_jobs = [job for job in job_postings if job.get('remote_option') == 'Remote']
        display_message = f"Found {len(filtered_jobs)} remote positions"
        export_format = 'csv'
        ```
        
        Return ONLY the Python code, no explanations."""
        
        with st.spinner("🤖 AI is analyzing your request..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User instruction: {instruction}\n\nGenerate Python code to process the job_postings list."}
                ],
                temperature=0.3
            )
            
            code = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if code.startswith("```python"):
                code = code[9:]
            if code.startswith("```"):
                code = code[3:]
            if code.endswith("```"):
                code = code[:-3]
            code = code.strip()
            
            # Display generated code
            with st.expander("🔍 Generated Processing Code", expanded=False):
                st.code(code, language="python")
            
            # Execute the code in a safe environment
            local_vars = {
                'job_postings': job_postings,
                'filtered_jobs': job_postings,  # Default
                'export_format': None,
                'display_message': None
            }
            
            try:
                exec(code, {"__builtins__": {}}, local_vars)
                
                filtered_jobs = local_vars.get('filtered_jobs', job_postings)
                export_format = local_vars.get('export_format')
                display_message = local_vars.get('display_message')
                
                # Display results
                if display_message:
                    st.success(f"✅ {display_message}")
                else:
                    st.success(f"✅ Processed {len(filtered_jobs)} jobs")
                
                # Show preview
                if filtered_jobs:
                    st.markdown("#### 📊 Results Preview (First 5)")
                    df = pd.DataFrame(filtered_jobs[:5])
                    st.dataframe(df, use_container_width=True)
                    
                    # Offer export
                    st.markdown("#### 💾 Download Results")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = pd.DataFrame(filtered_jobs).to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            "📥 Download as CSV",
                            csv,
                            file_name=f"filtered_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col2:
                        try:
                            buffer = BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                pd.DataFrame(filtered_jobs).to_excel(writer, index=False, sheet_name='Filtered Jobs')
                            buffer.seek(0)
                            st.download_button(
                                "📊 Download as Excel",
                                buffer,
                                file_name=f"filtered_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                        except:
                            st.caption("Excel export requires openpyxl")
                else:
                    st.warning("⚠️ No jobs matched your criteria")
                    
            except Exception as exec_error:
                st.error(f"❌ Error executing generated code: {exec_error}")
                st.code(code, language="python")
                
    except Exception as e:
        st.error(f"❌ Error processing instruction: {e}")
        st.markdown("**Please try:**")
        st.markdown("- Being more specific with your request")
        st.markdown("- Using simpler filtering criteria")
        st.markdown("- Checking that your OpenAI API key is valid")


# ============================================================================
# JOB MARKET ANALYTICS TAB
# ============================================================================

def render_job_market_analytics():
    """Render job market analytics based on LinkedIn search results"""
    st.markdown("### 📊 Job Market Analytics")
    st.markdown("*Insights from your LinkedIn job search results*")
    st.markdown("")
    
    # Get latest session data
    latest_session = get_latest_session_folder()
    
    if not latest_session:
        st.info("💡 No search data available yet. Run a job search first to see market analytics.")
        st.markdown("""
        **To get started:**
        1. Go to the "🎯 Advanced Search" tab
        2. Enter your job criteria and run a search
        3. Come back here to view analytics based on your results
        """)
        return
    
    # Load session files
    job_postings_file = f"{latest_session}/job_postings.json"
    market_trends_file = f"{latest_session}/market_trends.json"
    verification_file = f"{latest_session}/verification_report.json"
    
    # Display session info
    try:
        with open(f"{latest_session}/session_info.json", 'r') as f:
            session_info = json.load(f)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📁 Session ID", session_info.get("session_id", "N/A"))
        with col2:
            created_at = session_info.get("created_at", "")
            if created_at:
                dt = datetime.fromisoformat(created_at)
                st.metric("📅 Search Date", dt.strftime("%Y-%m-%d %H:%M"))
            else:
                st.metric("📅 Search Date", "N/A")
        with col3:
            st.metric("✅ Status", session_info.get("status", "completed"))
        
        st.markdown("---")
    except:
        pass
    
    # Create sub-tabs for different analytics sections
    analytics_tab1, analytics_tab2, analytics_tab3 = st.tabs([
        "📈 Overview & Trends",
        "💼 Job Postings Analysis", 
        "✅ Data Quality Report"
    ])
    
    with analytics_tab1:
        render_market_overview_and_trends(market_trends_file)
    
    with analytics_tab2:
        render_job_postings_analytics(job_postings_file)
    
    with analytics_tab3:
        render_verification_report(verification_file)


def render_market_overview_and_trends(market_trends_file):
    """Render market overview and trends from market_trends.json"""
    if not os.path.exists(market_trends_file):
        st.info("💡 Market trends data not available for this session")
        return
    
    try:
        with open(market_trends_file, 'r') as f:
            data = json.load(f)
        
        # Market Overview Section
        if "market_overview" in data:
            st.markdown("### 📊 Market Overview")
            overview = data["market_overview"]
            
            cols = st.columns(4)
            with cols[0]:
                st.metric("🎯 Market Health", overview.get("market_health", "N/A").upper())
            with cols[1]:
                st.metric("📅 Analysis Date", overview.get("analysis_date", "N/A"))
            with cols[2]:
                job_title = overview.get("job_title", "N/A")
                st.metric("💼 Job Title", job_title.title() if job_title != "N/A" else "N/A")
            with cols[3]:
                total_jobs = overview.get("total_jobs_analyzed", "N/A")
                st.metric("📊 Jobs Analyzed", total_jobs)
            
            st.markdown("---")
        
        # Salary Data Section
        if "salary_data" in data:
            st.markdown("### 💰 Salary Insights")
            salary = data["salary_data"]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                avg_salary = salary.get("average_salary", "N/A")
                st.metric("📊 Average Salary", avg_salary)
                
                if "salary_range" in salary:
                    salary_range = salary["salary_range"]
                    st.markdown(f"**Range:** {salary_range.get('min', 'N/A')} - {salary_range.get('max', 'N/A')}")
            
            with col2:
                jobs_with_salary = salary.get("jobs_with_salary_info", 0)
                jobs_without = salary.get("jobs_without_salary", 0)
                total = jobs_with_salary + jobs_without if isinstance(jobs_with_salary, int) else 0
                if total > 0:
                    pct = round((jobs_with_salary / total) * 100, 1)
                    st.metric("📋 Jobs with Salary", f"{jobs_with_salary} ({pct}%)")
                else:
                    st.metric("� Jobs with Salary", str(jobs_with_salary))
            
            with col3:
                # Salary distribution chart
                if "salary_distribution" in salary:
                    st.markdown("**Salary Distribution:**")
                    dist = salary["salary_distribution"]
                    for range_name, count in dist.items():
                        range_label = range_name.replace('_', ' ').title()
                        st.caption(f"{range_label}: {count} jobs")
            
            st.markdown("---")
        
        # Skills Demand Section
        if "in_demand_skills" in data:
            st.markdown("### 🎯 In-Demand Skills")
            skills_data = data["in_demand_skills"]
            
            # Display key metrics
            col1, col2 = st.columns(2)
            with col1:
                total_skills = skills_data.get("total_unique_skills_found", "N/A")
                st.metric("🔢 Unique Skills Found", total_skills)
            with col2:
                if "top_skills" in skills_data:
                    top_count = len(skills_data["top_skills"])
                    st.metric("⭐ Top Skills Tracked", top_count)
            
            # Display skills by category
            if "technical_skills" in skills_data or "tools_and_platforms" in skills_data or "soft_skills" in skills_data:
                st.markdown("**Skills by Category:**")
                cat_col1, cat_col2, cat_col3 = st.columns(3)
                
                with cat_col1:
                    if "technical_skills" in skills_data:
                        st.markdown("🖥️ **Technical Skills:**")
                        for skill in skills_data["technical_skills"][:10]:
                            st.caption(f"• {skill}")
                
                with cat_col2:
                    if "tools_and_platforms" in skills_data:
                        st.markdown("🛠️ **Tools & Platforms:**")
                        for tool in skills_data["tools_and_platforms"][:10]:
                            st.caption(f"• {tool}")
                
                with cat_col3:
                    if "soft_skills" in skills_data:
                        st.markdown("💡 **Soft Skills:**")
                        for skill in skills_data["soft_skills"][:10]:
                            st.caption(f"• {skill}")
                
                st.markdown("")
            
            # Display top skills as badges
            if "top_skills" in skills_data:
                top_skills = skills_data["top_skills"]
                st.markdown("**Top In-Demand Skills:**")
                skill_html = " ".join([
                    f'<span style="background-color:#0066cc;color:white;padding:5px 15px;border-radius:15px;margin:5px;display:inline-block;font-size:14px;">{skill}</span>'
                    for skill in top_skills[:15]
                ])
                st.markdown(skill_html, unsafe_allow_html=True)
                st.markdown("")
            
            # Skill frequency visualization
            if "skill_frequency" in skills_data and PLOTLY_AVAILABLE:
                skill_freq = skills_data["skill_frequency"]
                
                # Sort by frequency and take top 15
                sorted_skills = sorted(skill_freq.items(), key=lambda x: float(x[1].rstrip('%')), reverse=True)[:15]
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=[skill[0] for skill in sorted_skills],
                        y=[float(skill[1].rstrip('%')) for skill in sorted_skills],
                        marker_color='#0066cc',
                        text=[skill[1] for skill in sorted_skills],
                        textposition='auto',
                    )
                ])
                
                fig.update_layout(
                    title="Top Skills Demand Frequency",
                    xaxis_title="Skills",
                    yaxis_title="Percentage of Jobs (%)",
                    height=450,
                    xaxis_tickangle=-45
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
        
        # Hiring Patterns Section
        if "hiring_patterns" in data:
            st.markdown("### 🏢 Hiring Patterns")
            hiring = data["hiring_patterns"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                if "top_hiring_companies" in hiring:
                    st.markdown("**Top Hiring Companies:**")
                    companies = hiring["top_hiring_companies"]
                    
                    # Show with job counts if available
                    if "company_job_counts" in hiring:
                        counts = hiring["company_job_counts"]
                        for i, company in enumerate(companies[:10], 1):
                            count = counts.get(company, "")
                            st.markdown(f"{i}. **{company}** {f'({count} jobs)' if count else ''}")
                    else:
                        for i, company in enumerate(companies[:10], 1):
                            st.markdown(f"{i}. {company}")
            
            with col2:
                if "geographic_distribution" in hiring:
                    geo = hiring["geographic_distribution"]
                    if "high_demand_areas" in geo:
                        st.markdown("**High Demand Locations:**")
                        areas = geo["high_demand_areas"]
                        
                        # Show with job counts if available
                        if "location_job_counts" in geo:
                            counts = geo["location_job_counts"]
                            for i, area in enumerate(areas[:10], 1):
                                count = counts.get(area, "")
                                st.markdown(f"{i}. 📍 **{area}** {f'({count} jobs)' if count else ''}")
                        else:
                            for i, area in enumerate(areas[:10], 1):
                                st.markdown(f"{i}. 📍 {area}")
            
            # Remote work breakdown
            if "remote_work_breakdown" in hiring and PLOTLY_AVAILABLE:
                st.markdown("---")
                st.markdown("**Remote Work Options:**")
                remote_data = hiring["remote_work_breakdown"]
                
                labels = []
                values = []
                for key, value in remote_data.items():
                    if value and value != "0" and value != 0:
                        labels.append(key.replace('_', ' ').title())
                        values.append(int(value) if isinstance(value, str) and value.isdigit() else value)
                
                if labels and values:
                    fig = go.Figure(data=[go.Pie(
                        labels=labels,
                        values=values,
                        hole=.3,
                        marker_colors=['#0066cc', '#4d94ff', '#99c2ff', '#cce0ff']
                    )])
                    
                    fig.update_layout(
                        title="Remote Work Distribution",
                        height=350
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
        
        # Job Posting Trends
        if "job_posting_trends" in data:
            st.markdown("### 📈 Job Posting Trends")
            trends = data["job_posting_trends"]
            
            cols = st.columns(4)
            with cols[0]:
                st.metric("📊 Total Postings", trends.get("total_postings_found", "N/A"))
            with cols[1]:
                if "posting_freshness" in trends:
                    fresh = trends["posting_freshness"]
                    st.metric("🆕 Last 7 Days", fresh.get("posted_last_7_days", "N/A"))
            with cols[2]:
                if "posting_freshness" in trends:
                    fresh = trends["posting_freshness"]
                    st.metric("📅 Last 30 Days", fresh.get("posted_last_30_days", "N/A"))
            with cols[3]:
                if "industries_represented" in trends:
                    industries = trends["industries_represented"]
                    st.metric("🏭 Industries", len(industries) if isinstance(industries, list) else "N/A")
            
            # Company sizes if available
            if "company_sizes" in trends:
                st.markdown("**Company Size Distribution:**")
                sizes = trends["company_sizes"]
                size_col1, size_col2, size_col3 = st.columns(3)
                with size_col1:
                    st.caption(f"Small (0-50): {sizes.get('small_0_50', 0)} jobs")
                with size_col2:
                    st.caption(f"Medium (51-500): {sizes.get('medium_51_500', 0)} jobs")
                with size_col3:
                    st.caption(f"Large (500+): {sizes.get('large_500_plus', 0)} jobs")
        
        # Experience Level Requirements
        if "experience_level_requirements" in data:
            st.markdown("---")
            st.markdown("### 👔 Experience Level Distribution")
            exp_levels = data["experience_level_requirements"]
            
            # Show counts if available
            if "counts" in exp_levels:
                counts = exp_levels["counts"]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🎓 Entry Level", f"{counts.get('entry', 0)} ({exp_levels.get('entry_level', 'N/A')})")
                with col2:
                    st.metric("💼 Mid Level", f"{counts.get('mid', 0)} ({exp_levels.get('mid_level', 'N/A')})")
                with col3:
                    st.metric("🏆 Senior Level", f"{counts.get('senior', 0)} ({exp_levels.get('senior_level', 'N/A')})")
            
            # Pie chart
            if PLOTLY_AVAILABLE:
                labels = []
                values = []
                for key, val in exp_levels.items():
                    if key != "counts" and key != "not_specified" and val and val != "0%":
                        label = key.replace('_', ' ').title().replace(' Level', '')
                        try:
                            pct = float(val.rstrip('%'))
                            labels.append(label)
                            values.append(pct)
                        except:
                            pass
                
                if labels and values:
                    fig = go.Figure(data=[go.Pie(
                        labels=labels,
                        values=values,
                        hole=.3,
                        marker_colors=['#0066cc', '#4d94ff', '#99c2ff']
                    )])
                    
                    fig.update_layout(
                        title="Job Distribution by Experience Level",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        # Data Completeness
        if "data_completeness" in data:
            st.markdown("---")
            st.markdown("### 📋 Data Quality Metrics")
            completeness = data["data_completeness"]
            
            cols = st.columns(5)
            metrics = [
                ("💰 With Salary", "jobs_with_salary"),
                ("🎯 With Skills", "jobs_with_skills"),
                ("📝 With Description", "jobs_with_description"),
                ("📍 With Location", "jobs_with_location"),
                ("⭐ Avg Quality", "average_data_quality")
            ]
            
            for col, (label, key) in zip(cols, metrics):
                with col:
                    value = completeness.get(key, "N/A")
                    st.metric(label, value)
            
            st.markdown("---")
        
    except json.JSONDecodeError:
        st.error("❌ Error: Invalid JSON format in market trends file")
    except Exception as e:
        st.error(f"❌ Error rendering market trends: {e}")
        st.exception(e)
            
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error loading market trends: {e}")


def render_job_postings_analytics(job_postings_file):
    """Render analytics from job_postings.json"""
    if not os.path.exists(job_postings_file):
        st.info("💡 Job postings data not available for this session")
        return
    
    try:
        with open(job_postings_file, 'r') as f:
            data = json.load(f)
        
        postings = data.get("job_postings", [])
        metadata = data.get("search_metadata", {})
        
        if not postings:
            st.warning("⚠️ No job postings found in this session")
            return
        
        # Search Summary
        st.markdown("### 🔍 Search Summary")
        cols = st.columns(4)
        with cols[0]:
            st.metric("📊 Total Jobs", len(postings))
        with cols[1]:
            st.metric("🎯 Job Title", metadata.get("job_title", "N/A").title())
        with cols[2]:
            st.metric("📍 Location", metadata.get("location", "Any"))
        with cols[3]:
            search_date = metadata.get("search_date", "")
            if search_date:
                try:
                    dt = datetime.fromisoformat(search_date)
                    st.metric("📅 Search Date", dt.strftime("%Y-%m-%d"))
                except:
                    st.metric("📅 Search Date", "N/A")
            else:
                st.metric("📅 Search Date", "N/A")
        
        st.markdown("---")
        
        # Company Distribution
        st.markdown("### 🏢 Top Companies Hiring")
        company_counts = {}
        for job in postings:
            company = job.get("company_name", "Unknown")
            company_counts[company] = company_counts.get(company, 0) + 1
        
        sorted_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[
            go.Bar(
                x=[count for _, count in sorted_companies],
                y=[company for company, _ in sorted_companies],
                orientation='h',
                marker_color='#0066cc',
                text=[count for _, count in sorted_companies],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Top 10 Companies by Job Postings",
            xaxis_title="Number of Postings",
            yaxis_title="Company",
            height=400,
            yaxis={'categoryorder':'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Location Distribution
        st.markdown("### 📍 Geographic Distribution")
        location_counts = {}
        for job in postings:
            location = job.get("location", "Unknown")
            location_counts[location] = location_counts.get(location, 0) + 1
        
        sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        
        fig = go.Figure(data=[go.Pie(
            labels=[loc for loc, _ in sorted_locations],
            values=[count for _, count in sorted_locations],
            hole=.3
        )])
        
        fig.update_layout(
            title="Job Distribution by Location",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Recent vs Older Postings
        st.markdown("### 📅 Posting Freshness")
        recent_count = sum(1 for job in postings if job.get("date_posted") == "Recent")
        older_count = len(postings) - recent_count
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🆕 Recent Postings", recent_count, 
                     delta=f"{(recent_count/len(postings)*100):.1f}%")
        with col2:
            st.metric("📆 Older Postings", older_count,
                     delta=f"{(older_count/len(postings)*100):.1f}%")
    
    except Exception as e:
        st.error(f"❌ Error analyzing job postings: {e}")


def render_verification_report(verification_file):
    """Render verification report from verification_report.json"""
    if not os.path.exists(verification_file):
        st.info("💡 Verification report not available for this session")
        return
    
    try:
        with open(verification_file, 'r') as f:
            data = json.load(f)
        
        # Verification Summary
        st.markdown("### ✅ Data Quality Report")
        
        if "verification_summary" in data:
            summary = data["verification_summary"]
            
            cols = st.columns(4)
            with cols[0]:
                st.metric("📊 Total Jobs Verified", summary.get("total_jobs_verified", 0))
            with cols[1]:
                avg_score = summary.get("average_confidence_score", 0)
                st.metric("🎯 Avg Confidence", f"{avg_score:.2f}")
            with cols[2]:
                high_conf = summary.get("high_confidence_jobs", 0)
                st.metric("✅ High Confidence", high_conf)
            with cols[3]:
                flagged = summary.get("flagged_for_review", 0)
                st.metric("⚠️ Flagged", flagged)
            
            st.markdown("---")
            
            # Confidence Distribution
            st.markdown("### 📊 Confidence Distribution")
            
            high = summary.get("high_confidence_jobs", 0)
            medium = summary.get("medium_confidence_jobs", 0)
            low = summary.get("low_confidence_jobs", 0)
            
            import plotly.graph_objects as go
            
            fig = go.Figure(data=[
                go.Bar(
                    x=['High', 'Medium', 'Low'],
                    y=[high, medium, low],
                    marker_color=['#28a745', '#ffc107', '#dc3545'],
                    text=[high, medium, low],
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="Job Confidence Levels",
                xaxis_title="Confidence Level",
                yaxis_title="Number of Jobs",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Ground Truth Sources
        if "ground_truth_sources_used" in data:
            st.markdown("---")
            st.markdown("### 📚 Verification Sources")
            sources = data["ground_truth_sources_used"]
            
            source_html = " ".join([
                f'<span style="background-color:#28a745;color:white;padding:5px 12px;border-radius:12px;margin:5px;display:inline-block;font-size:0.9em;">✓ {source}</span>'
                for source in sources
            ])
            st.markdown(source_html, unsafe_allow_html=True)
        
        # Data Quality Assessment
        if "overall_data_quality" in data:
            st.markdown("---")
            st.markdown("### 🎯 Overall Data Quality")
            quality = data["overall_data_quality"]
            
            quality_colors = {
                "HIGH": "#28a745",
                "MEDIUM": "#ffc107",
                "LOW": "#dc3545"
            }
            
            color = quality_colors.get(quality, "#6c757d")
            st.markdown(f'<h2 style="color:{color};text-align:center;">{quality}</h2>', 
                       unsafe_allow_html=True)
        
        # User Recommendations
        if "user_recommendations" in data:
            st.markdown("---")
            st.markdown("### 💡 Recommendations")
            recommendations = data["user_recommendations"]
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
    
    except Exception as e:
        st.error(f"❌ Error loading verification report: {e}")


def render_page_footer():
    """Render page footer with helpful information"""
    st.markdown("---")
    
    with st.expander("ℹ️ How to Use This Page"):
        st.markdown("""
        ### 🎯 Advanced Search
        - Use detailed filters for precise job discovery
        - Filter by experience level, job type, remote options, industry
        - Enter job title and optionally specify location
        - Results appear with company and job descriptions
        
        ### 📚 Search History
        - View all your previous searches
        - Reload and compare past results
        - Track your job search journey over time
        
        ### 💾 Automatic Saving
        - All search results are automatically saved as JSON files
        - Find them in `src/outputs/linkedin/`
        - Easy to share, analyze, or process further
        """)
    
    st.caption("Powered by CrewAI + OpenAI GPT-4o | LinkedIn Job Search Engine")
