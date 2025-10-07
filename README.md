# LinkedIn Job Search Link Generator

A powerful and safe tool to generate comprehensive LinkedIn job search links without API requirements or data scraping. Perfect for job seekers who want to efficiently search LinkedIn across multiple keywords, locations, and companies.

## 🌟 Features

- ✅ **No API Required**: Generate search links without LinkedIn API access
- ✅ **Safe & Legal**: No data scraping or terms of service violations
- ✅ **Multiple Search Types**: Basic, recent, easy apply, remote, full-time, entry-level searches
- ✅ **Google Integration**: Include Google searches for LinkedIn jobs
- ✅ **Company-Specific**: Target specific companies with dedicated search links
- ✅ **Export Formats**: CSV for Excel and JSON for structured data
- ✅ **Link Validation**: Test generated links for accessibility

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas requests
```

### Basic Usage
```bash
python linkedin_job_search_generator.py
```

### Interactive Setup
The script will prompt you for:
- **Keywords**: Job titles or skills (e.g., "data scientist, python developer")
- **Locations**: Geographic locations (e.g., "United States, New York, Remote")
- **Companies**: Target companies (optional, e.g., "Google, Microsoft, Amazon")

## 📊 Generated Output

### CSV File Structure
| Column | Description |
|--------|-------------|
| `search_type` | Type of search (Basic Search, Easy Apply, etc.) |
| `keyword` | Search keyword used |
| `location` | Search location |
| `description` | Human-readable description of the search |
| `url` | Direct clickable LinkedIn search URL |
| `category` | Search category (linkedin_direct, google_search, etc.) |
| `created_time` | Timestamp when link was generated |

### Search Types Generated

#### LinkedIn Direct Searches
- **Basic Search**: Standard LinkedIn job search
- **Recent Jobs**: Jobs sorted by posting date
- **Easy Apply**: Jobs with one-click application
- **Remote Jobs**: Remote work positions only
- **Full-time Jobs**: Full-time positions only
- **Entry Level**: Entry-level positions

#### Google-Powered Searches
- **Google LinkedIn Search**: Search LinkedIn jobs via Google
- **Google Recent Week**: Google search for recent LinkedIn jobs

#### Company-Specific Searches (when companies provided)
- **Company Jobs Page**: Direct company career page
- **Targeted Search**: LinkedIn search filtered by specific company
- **Google Company Search**: Google search for company jobs on LinkedIn

## 🔧 Advanced Usage

### Programmatic Usage
```python
from linkedin_job_search_generator import generate_linkedin_job_links

keywords = ["data scientist", "machine learning engineer"]
locations = ["San Francisco", "New York"]
companies = ["Google", "Microsoft"]

search_links = generate_linkedin_job_links(keywords, locations, companies)
```

### Batch Processing
```python
from linkedin_job_search_generator import create_quick_access_csv

# Generate large batch of search links
search_data = create_quick_access_csv(
    keywords=["python", "java", "javascript", "react", "nodejs"],
    locations=["US", "UK", "Canada", "Remote"],
    companies=["FAANG companies list..."]
)
```

## 📈 Use Cases

### Job Seekers
- Generate comprehensive search links for daily job hunting
- Target specific companies and locations efficiently
- Access both LinkedIn direct and Google-powered searches

### Recruiters
- Create search templates for common positions
- Monitor job market trends across different platforms
- Generate candidate sourcing links

### Career Counselors
- Provide students with comprehensive job search resources
- Create location-specific job search guides
- Monitor industry hiring trends

## 🛡️ Safety & Compliance

### What This Tool Does ✅
- Generates public search URLs
- Uses official LinkedIn search parameters
- Leverages Google's public search functionality
- No data scraping or automated requests

### What This Tool Doesn't Do ❌
- No unauthorized data extraction
- No violation of LinkedIn's terms of service
- No automated job application submission
- No personal data collection

## 🔍 Example Output

### Sample Generated Links
```
Basic Search | Data Scientist @ New York
https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&location=New%20York

Google LinkedIn Search | Data Scientist @ New York  
https://www.google.com/search?q=site:linkedin.com/jobs+Data%20Scientist+New%20York

Google Company Search | Python Developer @ San Francisco
https://www.google.com/search?q=Google+Python%20Developer+site:linkedin.com/jobs
```

## 📋 File Structure

```
linkedin-job-search-generator/
├── linkedin_job_search_generator.py    # Main English version
├── quick_linkedin_links.py            # Chinese version (legacy)
├── README.md                          # This file
├── output/
│   ├── linkedin_job_search_links_YYYYMMDD_HHMMSS.csv
│   └── linkedin_searches_structured_YYYYMMDD_HHMMSS.json
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Changelog

### Version 2.0 (Current)
- ✅ Fixed Google search link encoding issues
- ✅ Added full English language support
- ✅ Enhanced company-specific search options
- ✅ Improved link validation and testing
- ✅ Added comprehensive documentation

### Version 1.0
- ✅ Initial release with basic link generation
- ✅ CSV export functionality
- ✅ Multi-keyword and multi-location support

## 🆘 Troubleshooting

### Common Issues

**Q: Generated links don't work properly**
A: Make sure you're using the latest version. We fixed URL encoding issues in v2.0.

**Q: Google search links show "no results"**
A: Try using more specific keywords or check if LinkedIn has changed their URL structure.

**Q: Company-specific searches not working**
A: Verify company names are spelled correctly and exist on LinkedIn.

### Getting Help
- Create an issue on GitHub
- Check existing issues for solutions
- Ensure you're using the latest version

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⭐ Acknowledgments

- LinkedIn for providing robust job search functionality
- Google for enabling site-specific searches
- The job-seeking community for feedback and feature requests

---

**Happy Job Hunting! 🎯**

*This tool is designed to make your LinkedIn job search more efficient and comprehensive. Use it responsibly and in accordance with all platform terms of service.*
