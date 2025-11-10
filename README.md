
# CrewAI Job Assistant 🚀
# use this term to run : streamlit run src/app.py

A powerful job search and career development platform powered by AI agents using CrewAI and Streamlit.

## Features

- **🔍 Explore Idea Jobs**: Discover trending career opportunities and market insights
- **🎯 Specific Jobs**: Get detailed analysis for specific job positions with real LinkedIn job postings
- **📄 Resume & Interview Prep**: AI-powered resume optimization and interview coaching

## LinkedIn Job Search System

### System Architecture

The LinkedIn job search system uses **4 specialized agents** working in sequence to deliver verified job postings:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INPUT (Streamlit UI)                    │
│  Job Title: "Data Analyst" | Location: "San Francisco" | Level: Entry│
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ TASK 1: Dashboard Input Processing                                  │
│ Agent: dashboard_input_processor                                     │
│ Output: src/outputs/linkedin/user_search_params.json                 │
│ Content: {job_title, location, experience_level, search_query}      │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ TASK 2: LinkedIn Job Scraping ⭐ CORE TASK                          │
│ Agent: LinkedIn_Scraper                                              │
│ Tools: SerperDevTool (Google search for LinkedIn)                    │
│ Query: "Data Analyst site:linkedin.com/jobs"                         │
│ Output: src/outputs/linkedin/job_postings.json                       │
│ Content: {search_metadata, job_postings[18 fields per job]}         │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ TASK 3: Market Trends Analysis                                      │
│ Agent: linkedin_market_trends_analyst                                │
│ Input: job_postings.json data                                        │
│ Output: src/outputs/linkedin/market_trends.json                      │
│ Content: {average_salary, top_skills, employment_trends, insights}  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ TASK 4: Verification & Quality Check                                │
│ Agent: verification_specialist                                       │
│ Input: job_postings.json data                                        │
│ Checks: Company names, URLs, salaries, dates, data completeness     │
│ Output: src/outputs/linkedin/verification_report.json                │
│ Content: {verification_summary, flagged_issues, verified_fields}    │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI DISPLAY                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │ Job Cards   │  │Verification │  │Market Trends│                │
│  │ Section     │  │   Badge     │  │   Charts    │                │
│  └─────────────┘  └─────────────┘  └─────────────┘                │
│  Reads: job_postings.json + verification_report.json + trends.json  │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Points**:
- **Sequential Execution**: Tasks run in order 1→2→3→4
- **JSON Output**: All tasks output structured JSON files
- **Data Flow**: Each task uses output from previous tasks
- **UI Integration**: Streamlit reads all 4 JSON files for display

### The 4-Task Workflow

#### **Task 1: Dashboard Input Processing**
- **Agent**: Dashboard Input Processor
- **Input**: User's search criteria from Streamlit form
- **Processing**: 
  - Extracts job title, location, experience level
  - Structures search parameters
  - Prepares query for LinkedIn scraping
- **Output**: `src/outputs/linkedin/user_search_params.json`
  ```json
  {
    "job_title": "Data Analyst",
    "location": "San Francisco",
    "experience_level": "entry",
    "search_query": "structured query for search"
  }
  ```

#### **Task 2: LinkedIn Job Scraping** ⭐ **Core Task**
- **Agent**: LinkedIn Scraper
- **Tools**: SerperDevTool (searches Google for LinkedIn jobs)
- **Processing**:
  - Uses simplified search queries (no date filters)
  - Searches for: `"{job_title}" site:linkedin.com/jobs`
  - Extracts up to 50 results
  - Parses job details: title, company, salary, location, etc.
- **Output**: `src/outputs/linkedin/job_postings.json`
  ```json
  {
    "search_metadata": {
      "job_title": "Data Analyst",
      "location": "San Francisco",
      "total_results_found": 3
    },
    "job_postings": [
      {
        "job_id": "unique_id",
        "job_title": "Data Analyst",
        "company_name": "Tech Corp",
        "location": "San Francisco, CA",
        "salary_range": "$80,000 - $100,000",
        "employment_type": "Full-time",
        "experience_level": "Entry level",
        "application_url": "https://linkedin.com/jobs/...",
        "date_posted": "2025-01-08",
        "job_description": "...",
        "required_skills": ["Python", "SQL"],
        "preferred_qualifications": ["Bachelor's degree"],
        "benefits": ["Health insurance"],
        "company_description": "...",
        "responsibilities": ["Analyze data"],
        "industry": "Technology",
        "company_size": "1000-5000",
        "remote_option": "Hybrid"
      }
    ]
  }
  ```

#### **Task 3: Market Trends Analysis**
- **Agent**: LinkedIn Market Trends Analyst
- **Input**: Job postings from Task 2
- **Processing**:
  - Analyzes salary ranges across all jobs
  - Identifies most in-demand skills
  - Compares employment types (remote/hybrid/onsite)
  - Detects hiring trends
- **Output**: `src/outputs/linkedin/market_trends.json`
  ```json
  {
    "average_salary": "$85,000",
    "top_skills": ["Python", "SQL", "Tableau"],
    "employment_trends": {
      "remote": 20,
      "hybrid": 50,
      "onsite": 30
    },
    "insights": "Hybrid work is dominant in this market"
  }
  ```

#### **Task 4: Verification & Quality Check**
- **Agent**: Verification Specialist
- **Input**: Job postings from Task 2
- **Processing**:
  - Validates company names exist
  - Checks LinkedIn URLs are active
  - Verifies salary ranges are reasonable
  - Ensures dates are current (2025)
  - Flags suspicious or incomplete data
- **Output**: `src/outputs/linkedin/verification_report.json`
  ```json
  {
    "verification_summary": {
      "total_jobs_checked": 3,
      "verified_jobs": 3,
      "flagged_jobs": 0,
      "confidence_level": "high"
    },
    "flagged_issues": [],
    "verified_fields": {
      "company_names": "all valid",
      "linkedin_urls": "all active",
      "salary_ranges": "reasonable",
      "dates": "current (2025)"
    },
    "corrections": []
  }
  ```

### Streamlit UI Integration

The UI (`src/streamlit_pages/specific_jobs.py`) displays the results:

1. **Job Postings Section**:
   - Reads from `tasks_output[1]` or `job_postings.json`
   - Displays job cards with title, company, salary
   - Shows application links and job details

2. **Verification Section**:
   - Reads from `verification_report.json`
   - Shows verification status badge
   - Lists any flagged issues
   - Displays confidence level

3. **Market Trends Section**:
   - Reads from `market_trends.json`
   - Shows salary averages
   - Displays top skills chart
   - Employment type distribution

### File System Structure

All LinkedIn search outputs are stored in:
```
src/outputs/linkedin/
├── user_search_params.json    # Task 1 output
├── job_postings.json           # Task 2 output (main data)
├── market_trends.json          # Task 3 output
└── verification_report.json    # Task 4 output
```

### Key Implementation Files

- **Crew Orchestration**: `src/Crew/linkedin_search_crew.py` (395 lines)
  - Defines 4 agents with tools and configurations
  - Creates 4 sequential tasks
  - Manages workflow execution

- **Agent Definitions**: `src/config/linkedin_agents.yaml`
  - Role, goal, and backstory for each agent
  - Tool assignments (SerperDevTool for scraper)

- **Task Definitions**: `src/config/linkedin_tasks.yaml`
  - Detailed task descriptions
  - Expected output formats (JSON schemas)
  - Agent assignments

- **UI Display**: `src/streamlit_pages/specific_jobs.py`
  - Reads all 4 JSON outputs
  - Renders job cards and verification badges
  - Handles user interactions

### Search Flow Example

1. User enters "Data Analyst" + "San Francisco" in Streamlit
2. Task 1 processes input → saves to `user_search_params.json`
3. Task 2 searches LinkedIn → saves 3 jobs to `job_postings.json`
4. Task 3 analyzes jobs → saves trends to `market_trends.json`
5. Task 4 verifies data → saves report to `verification_report.json`
6. Streamlit UI loads all 4 JSON files and displays results

### Important Notes

- **No External APIs Required**: Uses SerperDevTool (Google search) to find LinkedIn jobs
- **Simple Search Queries**: Removed date filters for better results
- **JSON Output Only**: All tasks output structured JSON (no text files)
- **Sequential Execution**: Tasks run in order (1→2→3→4)
- **Verification**: Basic quality checks ensure data reliability

## AI Agents

Our platform includes 8 specialized AI agents:

1. **Lead Research Analyst** - Job market research and analysis
2. **LinkedIn Market Trends Analyst** - LinkedIn market intelligence
3. **Technology Expert** - Technical skills and trends analysis
4. **Content Editor** - Content optimization and editing
5. **Resume Coach** - Resume enhancement and feedback
6. **Interview Coach** - Interview preparation and practice
7. **Career Development Specialist** - Career guidance and planning
8. **Industry Insights Analyst** - Industry trends and forecasting

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- Docker (optional)

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd CrewAI
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

5. **Run the application**:
   ```bash
   streamlit run src/app.py
   ```

   Access the app at: http://localhost:8501

### Docker Deployment

1. **Using Docker Compose (Recommended)**:
   ```bash
   # Copy environment file
   cp .env.example .env
   # Edit .env with your API keys
   
   # Build and run from project root
   docker-compose -f src/docker/docker-compose.yml up -d
   ```

2. **Using Docker directly**:
   ```bash
   # Build image from project root
   docker build -f src/docker/Dockerfile -t crewai-job-assistant .
   
   # Run container
   docker run -d \
     -p 8501:8501 \
     --env-file .env \
     --name crewai-app \
     crewai-job-assistant
   ```

3. **Access the application**:
   - Open your browser to: http://localhost:8501

For detailed Docker deployment instructions, see `src/docker/README.md`.

## Project Structure

```
CrewAI/
├── app.py                    # Main Streamlit application
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── src/
│   ├── crew.py             # CrewAI agents and tasks
│   ├── main.py             # Core logic
│   ├── run_demo.py         # Demo runner
│   ├── docker/
│   │   ├── Dockerfile      # Docker configuration
│   │   ├── docker-compose.yml # Docker Compose setup
│   │   └── README.md       # Docker deployment guide
│   ├── streamlit_pages/
│   │   ├── home.py         # Homepage
│   │   ├── analytics.py    # Analytics dashboard
│   │   ├── settings.py     # Settings page
│   │   └── job_search.py   # Job search functionality
│   ├── config/
│   │   ├── agents.yaml     # Agent configurations
│   │   └── tasks.yaml      # Task definitions
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── src/
│   ├── crew.py             # CrewAI agents and tasks
│   ├── main.py             # Core logic
│   ├── run_demo.py         # Demo runner
│   ├── config/
│   │   ├── agents.yaml     # Agent configurations
│   │   └── tasks.yaml      # Task definitions
│   ├── coaches/
│   │   ├── interview_coach.py
│   │   └── resume_coach.py
│   ├── data/
│   │   ├── sample_job_data.json
│   │   └── user_resume.txt
│   ├── outputs/            # Generated outputs
│   ├── Tools/
│   │   └── BrowserTools.py
│   └── utils/
│       └── session_manager.py
├── Dashboard/
│   └── dashboard.py        # Legacy dashboard
└── files/                  # Session data and exports
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Agent Configuration

Edit `src/config/agents.yaml` to customize AI agents:
- Modify agent roles and goals
- Add new specialized agents
- Configure agent backstories

### Task Configuration

Edit `src/config/tasks.yaml` to customize tasks:
- Define task descriptions and expected outputs
- Configure task dependencies
- Set output formats (JSON, Markdown, etc.)

## Usage

1. **Home Page**: Overview of platform capabilities
2. **Job Search**: Main job search and analysis functionality
3. **Analytics**: View session history and insights
4. **Settings**: Configure application preferences

## Development

### Adding New Pages

1. Create a new Python file (e.g., `new_page.py`)
2. Implement the page function
3. Add to `app.py` navigation

### Adding New Agents

1. Define agent in `src/config/agents.yaml`
2. Create corresponding task in `src/config/tasks.yaml`
3. Update `src/crew.py` with new agent and task

### Session Management

Sessions are automatically tracked and stored in JSON format:
- View recent sessions in Analytics
- Session data includes timestamps and search criteria
- Export functionality available

## Deployment

### Production Deployment

1. **Environment Setup**:
   ```bash
   # Production environment file
   cp .env.example .env.production
   # Configure production settings
   ```

2. **Docker Production**:
   ```bash
   # Build for production
   docker-compose -f src/docker/docker-compose.yml up -d
   ```

3. **Health Checks**:
   - Application health: http://localhost:8501/_stcore/health
   - Container logs: `docker-compose logs -f`

### Scaling

For high-traffic deployments:
- Use load balancer (nginx configuration included)
- Scale containers: `docker-compose -f src/docker/docker-compose.yml up -d --scale crewai-job-assistant=3`
- Consider using cloud platforms (AWS, GCP, Azure)

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   - Verify API key in `.env` file
   - Check API key permissions and billing

2. **Import Errors**:
   - Ensure all dependencies installed: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Port Already in Use**:
   - Change port in docker-compose.yml or .env
   - Kill existing processes: `lsof -ti:8501 | xargs kill`

### Logs and Debugging

```bash
# View application logs
docker-compose -f src/docker/docker-compose.yml logs -f crewai-job-assistant

# Debug mode
streamlit run src/app.py --logger.level=debug

# Check container health
docker inspect crewai-job-assistant | grep -i health
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review logs for error details

---

**Made with ❤️ using CrewAI and Streamlit**