# CrewAI Job Search Assistant - Multipage App

## 🚀 RUN

```bash
streamlit run src/app.py
```

Or:

```bash
python -m streamlit run src/app.py
```

## 📁 Project Structure

```
CrewAI/
├── src/
│   ├── app.py                      # Main entry point (multipage app)
│   └── streamlit_pages/
│       ├── home.py                 # Home/landing page
│       ├── job_search.py           # Job search assistant (formerly dashboard.py)
│       ├── analytics.py            # Market analytics & insights
│       └── settings.py             # Configuration & settings
└── README_MULTIPAGE.md             # This file
```

## 📖 Pages Overview

### 🏠 **Home Page** (`home.py`)
- Welcome screen and overview
- System status indicators
- Quick navigation to other features
- Recent activity summary

### 🔍 **Job Search Assistant** (`job_search.py`)
- Main CrewAI job search functionality
- Real AI agents for job analysis
- Interactive search interface
- Resume and interview preparation

### 📊 **Analytics** (`analytics.py`)
- Job market trends and insights
- Salary analysis and benchmarks
- Skills demand visualization
- Company hiring patterns

### ⚙️ **Settings** (`settings.py`)
- API key configuration
- User profile management
- App preferences and customization
- Advanced system settings

## 🛠️ Features

### ✨ **Modern Navigation**
- Uses `st.Page` and `st.navigation` for maximum flexibility
- Organized sidebar navigation with icons
- Shared header across all pages
- Responsive design

### 🤖 **AI Integration**
- Real OpenAI GPT-4 integration
- CrewAI agent orchestration
- Automatic fallback to demo mode
- Environment-aware configuration

### 📊 **Rich Visualizations**
- Interactive Plotly charts
- Real-time market data
- Responsive metrics and KPIs
- Export capabilities

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Dependencies
The app will automatically install required packages:
- `streamlit`
- `crewai`
- `crewai-tools`
- `openai`
- `plotly`
- `pandas`
- `python-dotenv`

## 🔄 Migration from Single Page

Your original `dashboard.py` has been renamed to `job_search.py` and integrated into the multipage structure. All functionality is preserved while gaining:

- Better organization and navigation
- Shared components and styling
- Scalable architecture for future features
- Enhanced user experience

## 🎯 Usage

1. **Start with Home**: Get an overview and system status
2. **Use Job Search**: Main functionality for job hunting
3. **Explore Analytics**: Understand market trends
4. **Configure Settings**: Customize your experience

## 🔍 Development

To add new pages:

1. Create a new Python file in `src/streamlit_pages/`
2. Implement a `main()` function with your page content
3. Add the page to the `pages` dictionary in `app.py`
4. Use `st.Page(your_function, title="Page Title", icon="🎯")`

## 🚀 Next Steps

- Test all pages with real AI integration
- Customize pages based on your specific needs
- Add more advanced analytics features
- Implement user authentication (optional)

---

**Happy job hunting with your AI-powered assistant! 🤖✨**