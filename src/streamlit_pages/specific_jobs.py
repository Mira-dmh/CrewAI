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


# ----------------------------------------------------------------------------
# Helpers: JSON safe loading and salary parsing
# ----------------------------------------------------------------------------
def safe_load_json(path: str):
    """Safely load JSON, returning None on empty/invalid files with guardrails."""
    try:
        if not os.path.exists(path):
            return None
        if os.path.getsize(path) == 0:
            return None
        with open(path, 'r', encoding='utf-8') as f:
            txt = f.read().strip()
            if not txt:
                return None
            return json.loads(txt)
    except Exception:
        return None


# ============================================================================
# MAIN PAGE
# ============================================================================

def specific_jobs_page():
    """Main entry point for the specific jobs search page"""
    
    # Page Header
    st.markdown("#  LinkedIn Job Search")
    st.markdown("*AI-powered job discovery with real-time market analysis*")
    st.markdown("---")
    
    # Check system readiness
    system_ready, error_msg = check_system_status()
    
    if not system_ready:
        display_system_error(error_msg)
        return
    
    # Advanced Search section
    render_advanced_search()
    
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
    st.error(" **System Configuration Required**")
    st.error(error_msg)
    
    with st.expander(" Setup Instructions", expanded=True):
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
    with st.expander(" Diagnostic Information"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**CrewAI Status:**")
            st.markdown(f"- Available: {'' if CREWAI_AVAILABLE else ''}")
            if IMPORT_ERROR:
                st.code(IMPORT_ERROR, language="text")
        
        with col2:
            st.markdown("**Environment Variables:**")
            st.markdown(f"- OPENAI_API_KEY: {' Set' if os.getenv('OPENAI_API_KEY') else ' Not set'}")
            st.markdown(f"- SERPER_API_KEY: {' Set' if os.getenv('SERPER_API_KEY') else ' Optional'}")


# ============================================================================
# ADVANCED SEARCH TAB
# ============================================================================

def render_advanced_search():
    """Render the advanced search form with all filters"""
    st.markdown("###  Advanced Search Options")
    st.markdown("*Use detailed filters for precise job discovery*")
    st.markdown("")
    
    # Check for pending search (from form submission)
    if 'pending_search' in st.session_state:
        pending = st.session_state.pop('pending_search')
        
        # Show search summary
        st.markdown("####  Your Search Criteria:")
        display_search_summary(pending['job_title'], pending['location'], pending['search_params'])
        
        # Execute search
        st.markdown("---")
        execute_linkedin_search(pending['job_title'], pending['location'], pending['search_params'])
        
        # Stop here - results will be shown
        return
    
    # API Status Check - Collapsible diagnostic panel
    with st.expander("🔍 API Configuration & Diagnostics", expanded=False):
        serper_key = os.getenv("SERPER_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**SerperDev API**")
            if serper_key:
                st.success("✅ SERPER_API_KEY configured")
                # Test API connection
                if st.button("Test SerperDev Connection"):
                    with st.spinner("Testing SerperDev API..."):
                        try:
                            import requests
                            response = requests.post(
                                "https://google.serper.dev/search",
                                headers={
                                    "X-API-KEY": serper_key,
                                    "Content-Type": "application/json"
                                },
                                json={"q": "test query", "num": 1},
                                timeout=5
                            )
                            if response.status_code == 200:
                                st.success(f"✅ API Connected! (Status: {response.status_code})")
                            else:
                                st.error(f"❌ API Error: {response.status_code}")
                                st.code(response.text)
                        except Exception as e:
                            st.error(f"❌ Connection Failed: {str(e)}")
            else:
                st.error("❌ SERPER_API_KEY not set")
                st.info("Add to `.env`: SERPER_API_KEY=your-key-here")
                
        with col2:
            st.markdown("**OpenAI API**")
            if openai_key:
                st.success("✅ OPENAI_API_KEY configured")
            else:
                st.error("❌ OPENAI_API_KEY not set")
    
    with st.form("advanced_search_form"):
        # Basic info section
        st.markdown("####  Basic Information")
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
        st.markdown("####  Additional Filters")
        col3, col4 = st.columns(2)
        
        with col3:
            job_type = st.selectbox(
                "Job Type",
                ["Any", "Full-time", "Part-time", "Contract", "Freelance"]
            )
            remote_option = st.selectbox(
                "Remote Work",
                ["Any", "Remote", "Hybrid", "On-site"]
            )
        
        with col4:
            industry = st.selectbox(
                "Industry",
                ["Any", "Technology", "Finance", "Healthcare", "Marketing", "Education"]
            )
            work_authorization = st.selectbox(
                "Work Authorization",
                [
                    "Any",
                    "Open to US visa sponsorship",
                    "Open to Optional Practical Training (OPT)",
                    "Open to Curricular Practical Training (CPT)",
                    "No US work authorization required",
                    "Unknown"
                ]
            )
        
        # Submit button
        st.markdown("---")
        submitted = st.form_submit_button(
            " Search with Filters",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if not job_title:
                st.error(" Job title is required")
            else:
                # Build search params
                search_params = {
                    "company": company,
                    "experience_level": experience,
                    "job_type": job_type,
                    "remote_option": remote_option,
                    "industry": industry,
                    "work_authorization": work_authorization
                }
                
                # Save to session state and trigger search
                st.session_state['pending_search'] = {
                    'job_title': job_title,
                    'location': location,
                    'search_params': search_params
                }
                st.rerun()


# ============================================================================
# SEARCH EXECUTION
# ============================================================================

def execute_linkedin_search(job_title, location="", search_params=None):
    """Execute the LinkedIn search with AI agents"""
    
    st.markdown("###  AI Search in Progress")
    st.markdown("")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize
        status_text.text(" Initializing AI agents...")
        progress_bar.progress(20)
        
        llm = LLM(model="gpt-4o-mini", temperature=0.7)
        linkedin_crew = LinkedInSearchCrew(llm=llm)
        
        # Start search
        status_text.text(f" Searching LinkedIn for '{job_title}'...")
        progress_bar.progress(40)
        
        # Execute
        status_text.text(" AI agents analyzing job market...")
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
        status_text.text(" Analysis complete!")
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
        
        st.error(f" **Search Error:** {str(e)}")
        st.error(f"**Error Type:** {type(e).__name__}")
        
        with st.expander(" View Error Details"):
            import traceback
            st.code(traceback.format_exc(), language="python")
        
        display_troubleshooting_tips()


# ============================================================================
# RESULTS DISPLAY
# ============================================================================

def display_search_results(job_title, location, result):
    """Display formatted search results in organized tabs"""
    
    st.success(f" **Search Complete:** {job_title}" + (f" in {location}" if location else ""))
    
    # Display job postings directly without tabs
    display_job_postings_section(result)
    
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
    
    # Priority 2: Fallback to saved JSON files (try multiple sources)
    if postings is None:
        # Try scraping_task_output.json first (has complete job data with URLs)
        search_files = [
            "src/outputs/linkedin/scraping_task_output.json",
            "src/outputs/linkedin/latest_search_results.json",
            "src/outputs/linkedin/job_postings.json",
        ]
        
        # Also check for timestamped search_results files
        linkedin_dir = "src/outputs/linkedin"
        if os.path.exists(linkedin_dir):
            import glob
            timestamped_files = sorted(
                glob.glob(f"{linkedin_dir}/search_results_*.json"),
                reverse=True  # Most recent first
            )
            search_files.extend(timestamped_files[:3])  # Add top 3 recent
        
        for job_file in search_files:
            if not os.path.exists(job_file):
                continue
                
            try:
                with open(job_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                    # Skip empty files
                    if not content:
                        continue
                    
                    # Try to parse JSON
                    data = json.loads(content)
                    
                    # Check different possible structures
                    if isinstance(data, dict):
                        # Method 1: Direct job_postings array (from LinkedInJobSearchTool)
                        if "job_postings" in data:
                            postings = data["job_postings"]
                            if postings:  # Found valid data
                                break
                        
                        # Method 2: verified_jobs from verification specialist
                        if "verified_jobs" in data:
                            # Filter: only include jobs with MATCH location or verification_status = VERIFIED
                            verified_postings = data["verified_jobs"]
                            postings = []
                            for job in verified_postings:
                                # Check location verification
                                loc_verification = job.get("location_verification", {})
                                match_status = loc_verification.get("match_status", "UNCERTAIN")
                                verification_status = job.get("verification_status", "UNKNOWN")
                                
                                # Include job if:
                                # 1. Location matches OR
                                # 2. Verification status is VERIFIED (passed all checks)
                                # 3. NOT if verification_status is REJECTED or FLAGGED with location mismatch
                                if match_status == "MATCH" or (verification_status == "VERIFIED" and match_status != "MISMATCH"):
                                    # Add missing URLs from job_id
                                    if not job.get('application_url') and job.get('job_id'):
                                        job['application_url'] = f"https://www.linkedin.com/jobs/view/{job['job_id']}"
                                    postings.append(job)
                            
                            if postings:  # Found valid verified jobs
                                break
                        
                        # Method 3: Nested in crew_output (CrewAI format)
                        if "crew_output" in data:
                            try:
                                crew_data = json.loads(data["crew_output"]) if isinstance(data["crew_output"], str) else data["crew_output"]
                                if isinstance(crew_data, dict):
                                    # Try job_postings first
                                    if "job_postings" in crew_data:
                                        postings = crew_data["job_postings"]
                                        if postings:
                                            break
                                    # Try verified_jobs
                                    if "verified_jobs" in crew_data:
                                        # Filter: only include jobs with MATCH location
                                        verified_postings = crew_data["verified_jobs"]
                                        postings = []
                                        for job in verified_postings:
                                            loc_verification = job.get("location_verification", {})
                                            match_status = loc_verification.get("match_status", "UNCERTAIN")
                                            verification_status = job.get("verification_status", "UNKNOWN")
                                            
                                            if match_status == "MATCH" or (verification_status == "VERIFIED" and match_status != "MISMATCH"):
                                                # Add missing URLs
                                                if not job.get('application_url') and job.get('job_id'):
                                                    job['application_url'] = f"https://www.linkedin.com/jobs/view/{job['job_id']}"
                                                postings.append(job)
                                        
                                        if postings:
                                            break
                            except:
                                pass
                    
            except json.JSONDecodeError as e:
                # File contains invalid JSON (like CrewAI logs)
                continue
            except Exception as e:
                # Other errors - continue to next file
                continue
    
    if not postings:
        st.warning("⚠️ **No job postings found!**")
        st.markdown("""
        **Possible reasons:**
        1. **SerperDev API issue** - The LinkedIn scraper might not have API access
        2. **Too restrictive filters** - Try broader search criteria (change Part-time to Any, On-site to Any)
        3. **API rate limits** - You may have hit SerperDev's usage limits
        4. **Search query issues** - The automated search might need adjustment
        5. **JSON file corruption** - The result files might contain invalid data
        
        **Troubleshooting:**
        - Use the "🔍 API Configuration & Diagnostics" panel above to test SerperDev
        - Try a simpler search (just job title, Any for all other filters)
        - Check the Raw Data tab to see what the AI agents returned
        - Look for `latest_search_results.json` in `src/outputs/linkedin/`
        """)
        
        # Debug: Show which files were checked
        with st.expander("🔍 Debug: Files Checked", expanded=False):
            linkedin_dir = "src/outputs/linkedin"
            if os.path.exists(linkedin_dir):
                files = os.listdir(linkedin_dir)
                st.write(f"Files in {linkedin_dir}:")
                for f in sorted(files):
                    file_path = os.path.join(linkedin_dir, f)
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        st.text(f"  - {f} ({size} bytes)")
            else:
                st.error(f"Directory not found: {linkedin_dir}")
        
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
    
    st.markdown(f"###  Job Listings (Showing {len(display_postings)} of {len(limited_postings)})")
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
                    " Download CSV (50 jobs)",
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
                    " Download Excel (50 jobs)",
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
        if st.button(" Refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    # AI Assistant Chat Box
    with st.expander(" AI Assistant - Ask for custom analysis or exports", expanded=False):
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
            execute_btn = st.button(" Execute", type="primary", use_container_width=True)
        with col_b:
            if execute_btn and user_instruction:
                st.info(" AI Assistant is processing your request...")
                # Process AI instruction
                process_ai_instruction(user_instruction, limited_postings)
            elif execute_btn:
                st.warning(" Please enter an instruction first")
    
    st.markdown("---")
    
    # Display jobs
    for i, job in enumerate(display_postings, 1):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            # Extract fields with multiple fallback keys
            job_title = job.get('job_title') or job.get('title') or 'Job Title'
            company = job.get('company_name') or job.get('company') or 'Company'
            location = job.get('location') or job.get('job_location') or 'Not specified'
            posted = job.get('date_posted') or job.get('posted') or 'Recent'
            employment_type = job.get('employment_type') or job.get('job_type')
            experience_level = job.get('experience_level')
            
            # Build LinkedIn URL from job_id if not provided
            job_url = (job.get('application_url') or job.get('job_url') or 
                      job.get('url') or job.get('link'))
            if not job_url and job.get('job_id'):
                job_url = f"https://www.linkedin.com/jobs/view/{job.get('job_id')}"
            
            # Date information - distinguish original post vs repost
            is_repost = job.get('is_repost', False)
            repost_date = job.get('repost_date')
            date_info_raw = job.get('date_info_raw')
            
            # Build date display string
            date_display = ""
            if is_repost:
                if posted and repost_date:
                    date_display = f" Originally: {posted} |  Reposted: {repost_date}"
                elif repost_date:
                    date_display = f" Reposted: {repost_date}"
                elif date_info_raw:
                    date_display = f" {date_info_raw}"
                else:
                    date_display = f" Reposted: {posted}"
            else:
                date_display = f" Posted: {posted}"
            
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
                st.markdown(f" **Company:** {company}")
                st.markdown(f" **Location:** {location}")
                
                # Display employment info in one line
                info_parts = []
                if employment_type:
                    info_parts.append(f" {employment_type}")
                if experience_level:
                    info_parts.append(f" {experience_level}")
                if info_parts:
                    st.caption(" | ".join(info_parts))
                
                # NEW: Short intro
                if short_intro:
                    st.markdown(f"** Summary:** {short_intro}")
                
                # NEW: Company business intro (truncated for readability)
                if company_desc:
                    desc_preview = (company_desc[:300] + '...') if len(str(company_desc)) > 300 else company_desc
                    with st.expander(" About Company"):
                        st.write(desc_preview)
                
                # NEW: Job role description (truncated for readability)
                if job_desc:
                    role_preview = (job_desc[:500] + '...') if len(str(job_desc)) > 500 else job_desc
                    with st.expander(" Role Details"):
                        st.write(role_preview)
            
            with col2:
                st.markdown(f"**{date_display}**")
                if job_url:
                    st.link_button(" View Job", job_url, use_container_width=True, type="primary")
                else:
                    st.caption(" Link unavailable")
            
            st.divider()


def display_market_trends_section():
    """Load and display market trends from JSON"""
    trends_file = "src/outputs/linkedin/market_trends.json"
    
    if not os.path.exists(trends_file):
        st.info(" Market trends will appear here after the search completes")
        return
    
    try:
        with open(trends_file, 'r') as f:
            data = json.load(f)
        
        # Market overview
        if "market_overview" in data:
            st.markdown("###  Market Overview")
            overview = data["market_overview"]
            
            cols = st.columns(3)
            with cols[0]:
                st.metric(" Market Health", overview.get("market_health", "N/A").upper())
            with cols[1]:
                st.metric(" Analysis Date", overview.get("analysis_date", "N/A"))
            with cols[2]:
                st.metric(" Position", overview.get("job_title", "N/A"))
            
            st.markdown("")
        
        # Salary trends
        if "salary_trends" in data and "salary_ranges" in data["salary_trends"]:
            st.markdown("###  Salary Ranges")
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
                            st.markdown(f" ${info.get('min', 0):,} - ${info.get('max', 0):,}")
                            st.markdown(f" Avg: ${info.get('average', 0):,}")
            
            st.markdown("")
        
        # Top skills
        if "skills_analysis" in data:
            st.markdown("###  Top In-Demand Skills")
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
        st.warning(f" JSON parsing error: {e}")
    except Exception as e:
        st.error(f" Error loading market trends: {e}")


def display_verification_section():
    """Load and display verification report from JSON"""
    verify_file = "src/outputs/linkedin/verification_report.json"
    
    if not os.path.exists(verify_file):
        st.info(" Verification report will appear here after the search completes")
        return
    
    try:
        with open(verify_file, 'r') as f:
            data = json.load(f)
        
        # Status metrics
        cols = st.columns(3)
        
        with cols[0]:
            status = data.get("verification_status", "unknown")
            emoji = "" if status == "verified" else ""
            st.metric(" Status", f"{emoji} {status.upper()}")
        
        with cols[1]:
            st.metric(" Accuracy", data.get("accuracy_score", "N/A"))
        
        with cols[2]:
            confidence = data.get("confidence_level", "N/A")
            emoji_conf = "🟢" if confidence == "high" else "🟡" if confidence == "medium" else ""
            st.metric(" Confidence", f"{emoji_conf} {str(confidence).upper()}")
        
        st.markdown("")
        
        # Verified fields
        if "verified_fields" in data:
            verified = data["verified_fields"]
            if verified:
                st.markdown("###  Verified Data Points")
                cols = st.columns(3)
                for idx, field in enumerate(verified):
                    with cols[idx % 3]:
                        st.markdown(f" {field}")
        
        # Issues
        if "flagged_issues" in data:
            issues = data["flagged_issues"]
            if issues:
                st.markdown("###  Flagged Issues")
                for issue in issues:
                    st.warning(issue)
        
        # Corrections
        if "corrections" in data:
            corrections = data["corrections"]
            if corrections:
                st.markdown("###  Suggested Corrections")
                for correction in corrections:
                    st.info(correction)
        
    except json.JSONDecodeError as e:
        st.warning(f" JSON parsing error: {e}")
    except Exception as e:
        st.error(f" Error loading verification: {e}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def display_search_summary(job_title, location, search_params):
    """Display a formatted search summary"""
    cols = st.columns(5)
    
    with cols[0]:
        st.markdown("** Position**")
        st.markdown(job_title)
    
    with cols[1]:
        st.markdown("** Location**")
        st.markdown(location or "Any")
    
    with cols[2]:
        st.markdown("** Experience**")
        st.markdown(search_params.get("experience_level", "Any"))
    
    with cols[3]:
        st.markdown("** Type**")
        st.markdown(search_params.get("job_type", "Any"))
    
    with cols[4]:
        st.markdown("** Work Auth**")
        st.markdown(search_params.get("work_authorization", "Any"))


def render_search_metrics():
    """Display search performance metrics"""
    cols = st.columns(4)
    
    with cols[0]:
        st.metric(" AI Agents", "4 Active")
    
    with cols[1]:
        st.metric(" Data Source", "LinkedIn")
    
    with cols[2]:
        st.metric(" Analysis", "Real-time")
    
    with cols[3]:
        st.metric(" Output", "JSON")


def display_troubleshooting_tips():
    """Display troubleshooting information"""
    st.markdown("###  Troubleshooting Tips")
    st.markdown("""
    -  Verify your OpenAI API key has available credits
    -  Check SERPER_API_KEY is configured in .env
    -  Ensure stable internet connection
    -  Try with a simpler job title first
    -  Check the terminal output for detailed logs
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
            st.error(" OpenAI API key not found. Please configure it in .env file.")
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
        
        with st.spinner(" AI is analyzing your request..."):
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
            with st.expander(" Generated Processing Code", expanded=False):
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
                    st.success(f" {display_message}")
                else:
                    st.success(f" Processed {len(filtered_jobs)} jobs")
                
                # Show preview
                if filtered_jobs:
                    st.markdown("####  Results Preview (First 5)")
                    df = pd.DataFrame(filtered_jobs[:5])
                    st.dataframe(df, use_container_width=True)
                    
                    # Offer export
                    st.markdown("####  Download Results")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = pd.DataFrame(filtered_jobs).to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            " Download as CSV",
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
                                " Download as Excel",
                                buffer,
                                file_name=f"filtered_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                        except:
                            st.caption("Excel export requires openpyxl")
                else:
                    st.warning(" No jobs matched your criteria")
                    
            except Exception as exec_error:
                st.error(f" Error executing generated code: {exec_error}")
                st.code(code, language="python")
                
    except Exception as e:
        st.error(f" Error processing instruction: {e}")
        st.markdown("**Please try:**")
        st.markdown("- Being more specific with your request")
        st.markdown("- Using simpler filtering criteria")
        st.markdown("- Checking that your OpenAI API key is valid")


def render_page_footer():
    """Render page footer with helpful information"""
    st.markdown("---")
    
    with st.expander("How to Use This Page"):
        st.markdown("""
        ###  Advanced Search
        - Use detailed filters for precise job discovery
        - Filter by experience level, job type, remote options, industry
        - Enter job title and optionally specify location
        - Results appear with company and job descriptions
        
###  Automatic Saving
        - All search results are automatically saved as JSON files
        - Find them in `src/outputs/linkedin/`
        - Easy to share, analyze, or process further
        """)
    
    st.caption("Powered by CrewAI + OpenAI GPT-4o | LinkedIn Job Search Engine")


