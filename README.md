
# CrewAI Job Assistant 🚀
# use this term to run : streamlit run src/app.py

A powerful job search and career development platform powered by AI agents using CrewAI and Streamlit.

## Features

- **🔍 Explore Idea Jobs**: Discover trending career opportunities and market insights
- **🎯 Specific Jobs**: Get detailed analysis for specific job positions  
- **📄 Resume & Interview Prep**: AI-powered resume optimization and interview coaching

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