# CrewAI Job Search Assistant - Multipage App Documentation

## 🏗️ Multipage App Architecture

This application uses Streamlit's modern multipage framework with `st.Page` and `st.navigation` for a professional, scalable user experience.

### 📁 Project Structure

```
CrewAI/
├── app.py                          # Root entry point
├── src/
│   ├── app.py                      # Main application logic
│   └── streamlit_pages/
│       ├── home.py                 # Homepage with dashboard
│       ├── info_page.py           # Info/exploration page  
│       ├── job_search.py          # Job search functionality
│       ├── analytics.py           # Market analytics
│       └── settings.py            # App configuration
├── src/docker/                     # Docker deployment files
└── README.md                       # Project documentation
```

### 🧭 Navigation System

#### **Page Organization:**
- **Main**: Homepage entry point
- **Services**: Core job search features  
- **Analytics & Settings**: Data insights and configuration

#### **Navigation Methods:**
1. **Sidebar Navigation**: Traditional menu-based navigation
2. **Dashboard Cards**: Direct click-to-navigate from homepage
3. **Breadcrumb Trail**: Shows current location in app hierarchy
4. **URL Routing**: Direct page access via URLs

### 🎯 Page Definitions

```python
pages = {
    "Main": [
        st.Page(home_page, title="Home", icon="🏠", url_path="home"),
    ],
    "Services": [
        st.Page(info_page, title="Info Page", icon="💡", url_path="Info_Page"),
        st.Page(job_search_page, title="Job Search Assistant", icon="🔍", url_path="job_search"),
        st.Page(specific_jobs_page, title="Specific Jobs", icon="🎯", url_path="Specific_Jobs"),
        st.Page(resume_prep_page, title="Resume Prep", icon="📝", url_path="Resume_Prep"),
    ],
    "Analytics & Settings": [
        st.Page(analytics_page, title="Job Market Analytics", icon="📊", url_path="analytics"),
        st.Page(settings_page, title="Settings", icon="⚙️", url_path="settings"),
    ]
}
```

### 🔗 Dashboard Navigation Implementation

The homepage features clickable cards that redirect users to specific pages:

```python
# Example: Navigate to Info Page
if st.button("🚀 Start Exploring", key="explore_jobs"):
    try:
        st.switch_page("Info_Page")
    except Exception as e:
        st.error(f"Navigation error: {e}")
        st.info("💡 Please use the sidebar navigation")
```

### 🎨 Styling and Theme

#### **Global Styles:**
- Custom CSS for professional appearance
- Responsive design for all screen sizes
- Consistent color scheme and typography
- Hover effects and smooth transitions

#### **Component Styling:**
- Gradient cards for dashboard sections
- Material Design icons throughout
- Clean sidebar navigation
- Professional button styling

### 🔧 Session Management

The app maintains user state across pages:

```python
# Session state initialization
if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {
        "theme": "light",
        "show_tips": True,
        "last_visited": None
    }
```

### 🚀 Getting Started

#### **Run Locally:**
```bash
streamlit run app.py
```

#### **Run with Docker:**
```bash
docker-compose -f src/docker/docker-compose.yml up -d
```

#### **Access Points:**
- **Local**: http://localhost:8501
- **Docker**: http://localhost:8501

### 📱 Page Functionality

#### **🏠 Home Page (home.py)**
- Welcome dashboard with service overview
- Three main navigation cards
- Getting started guide
- System status indicators

#### **💡 Info Page (info_page.py)**
- Career exploration and job ideas
- Custom content (your implementation)
- Job market insights

#### **🎯 Specific Jobs (specific_jobs_page)**
- Interactive job search form
- Advanced filtering options
- Placeholder for search results

#### **📝 Resume Prep (resume_prep_page)**
- Tabbed interface for different tools
- File upload functionality
- Interview practice sections

#### **🔍 Job Search Assistant (job_search.py)**
- Main job search functionality
- AI-powered recommendations
- Search history and analytics

#### **📊 Analytics (analytics.py)**
- Job market data visualization
- Session tracking and insights
- Export functionality

#### **⚙️ Settings (settings.py)**
- User preferences configuration
- API key management
- Theme and display options

### 🔄 Navigation Flow

```
Home Dashboard
├── Explore Idea Jobs → Info Page
├── Specific Jobs → Specific Jobs Search
└── Resume Prep → Resume Builder

Sidebar Navigation
├── Main > Home
├── Services
│   ├── Info Page
│   ├── Job Search Assistant  
│   ├── Specific Jobs
│   └── Resume Prep
└── Analytics & Settings
    ├── Job Market Analytics
    └── Settings
```

### 🛡️ Error Handling

- Graceful fallback for navigation errors
- User-friendly error messages
- Alternative navigation suggestions
- Robust exception handling

### 📈 Extensibility

#### **Adding New Pages:**
1. Create new Python file in `src/streamlit_pages/`
2. Define page function
3. Add to `pages` dictionary in `src/app.py`
4. Update navigation references

#### **Customizing Navigation:**
- Modify `pages` structure for different groupings
- Add/remove navigation sections
- Customize icons and titles
- Implement role-based access

### 🐳 Docker Deployment

The multipage app is fully containerized:

- **Dockerfile**: Located in `src/docker/`
- **docker-compose.yml**: Complete orchestration
- **Health checks**: Automatic monitoring
- **Volume persistence**: Data and session storage

### 🎯 Best Practices Implemented

- **Modular Architecture**: Separate page files
- **Clean URLs**: Semantic path naming
- **Responsive Design**: Mobile-friendly layouts
- **Error Recovery**: Multiple navigation methods
- **State Management**: Persistent user preferences
- **Professional Styling**: Corporate-ready appearance

### 🔮 Future Enhancements

- [ ] Role-based page access
- [ ] Dynamic navigation based on user type
- [ ] Advanced theming system
- [ ] Integration with external APIs
- [ ] Real-time notifications
- [ ] Progressive Web App (PWA) features

---

**Your multipage app is production-ready and fully functional!** 🎉