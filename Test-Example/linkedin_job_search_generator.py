"""
LinkedIn Job Search Link Generator
Generate effective LinkedIn search URLs without data scraping
Perfect for quickly generating search links for manual browsing
"""

import pandas as pd
import urllib.parse
from datetime import datetime
import json
import os

def generate_linkedin_job_links(keywords, locations, companies=None):
    """
    Generate LinkedIn job search links
    
    Parameters:
    - keywords: List of search keywords
    - locations: List of locations
    - companies: List of company names (optional)
    
    Returns: Dictionary containing all search combinations
    """
    
    search_links = []
    
    for keyword in keywords:
        for location in locations:
            # URL encoding
            keyword_encoded = urllib.parse.quote(keyword)
            location_encoded = urllib.parse.quote(location)
            
            # Basic search links
            base_link = {
                'keyword': keyword,
                'location': location,
                'basic_search': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}",
                'recent_posts': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&sortBy=DD",
                'easy_apply': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_AL=true",
                'remote_jobs': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_WT=2",
                'full_time': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_JT=F",
                'entry_level': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_E=1",
                'mid_level': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_E=3",
                'senior_level': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_E=4"
            }
            
            # Combine links
            combined_links = base_link
            
            # Add company-specific searches if companies provided
            if companies:
                company_links = {}
                for company in companies:
                    company_encoded = urllib.parse.quote(company)
                    company_slug = company.lower().replace(' ', '-').replace('&', 'and')
                    
                    company_links[f'company_{company}'] = {
                        'jobs_page': f"https://www.linkedin.com/company/{company_slug}/jobs/",
                        'jobs_search': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_C={company_encoded}"
                    }
                
                combined_links['companies'] = company_links
            
            search_links.append(combined_links)
    
    return search_links

def create_quick_access_csv(keywords, locations, companies=None):
    """
    Create quick access CSV file
    """
    
    print("🔗 Generating LinkedIn search links...")
    
    all_links = []
    
    for keyword in keywords:
        for location in locations:
            # URL encoding
            keyword_encoded = urllib.parse.quote(keyword)
            location_encoded = urllib.parse.quote(location)
            
            # Create basic search records
            searches = [
                {
                    'search_type': 'Basic Search',
                    'keyword': keyword,
                    'location': location,
                    'description': 'Standard LinkedIn job search',
                    'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}",
                    'category': 'linkedin_direct'
                },
                {
                    'search_type': 'Recent Jobs',
                    'keyword': keyword,
                    'location': location,
                    'description': 'Jobs sorted by posting date',
                    'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&sortBy=DD",
                    'category': 'linkedin_direct'
                },
                {
                    'search_type': 'Easy Apply',
                    'keyword': keyword,
                    'location': location,
                    'description': 'Jobs with one-click application',
                    'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_AL=true",
                    'category': 'linkedin_direct'
                },
                {
                    'search_type': 'Remote Jobs',
                    'keyword': keyword,
                    'location': location,
                    'description': 'Remote work positions',
                    'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_WT=2",
                    'category': 'linkedin_direct'
                },
                {
                    'search_type': 'Full-time Jobs',
                    'keyword': keyword,
                    'location': location,
                    'description': 'Full-time positions only',
                    'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_JT=F",
                    'category': 'linkedin_direct'
                },
                {
                    'search_type': 'Entry Level',
                    'keyword': keyword,
                    'location': location,
                    'description': 'Entry-level positions',
                    'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_E=1",
                    'category': 'linkedin_direct'
                },

            ]
            
            all_links.extend(searches)
            
            # Add company-specific searches if companies provided
            if companies:
                for company in companies:
                    company_encoded = urllib.parse.quote(company)
                    company_slug = company.lower().replace(' ', '-').replace('&', 'and')
                    
                    company_searches = [
                        {
                            'search_type': f'{company} - Company Jobs Page',
                            'keyword': keyword,
                            'location': location,
                            'description': f'{company} company LinkedIn jobs page',
                            'url': f"https://www.linkedin.com/company/{company_slug}/jobs/",
                            'category': 'company_page'
                        },
                        {
                            'search_type': f'{company} - Targeted Search',
                            'keyword': keyword,
                            'location': location,
                            'description': f'LinkedIn search for {keyword} jobs at {company}',
                            'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_C={company_encoded}",
                            'category': 'company_targeted'
                        },

                    ]
                    
                    all_links.extend(company_searches)
    
    # Add creation time
    for link in all_links:
        link['created_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return all_links

def main():
    """
    Main function - Quick LinkedIn search link generator
    """
    print("🔗 LinkedIn Job Search Link Generator")
    print("=" * 50)
    print("Generate various LinkedIn search links without API or data scraping")
    print()
    
    # User input
    keywords_input = input("Enter search keywords (comma-separated): ").strip()
    if not keywords_input:
        keywords = ["data scientist", "python developer", "machine learning engineer"]
        print(f"Using default keywords: {keywords}")
    else:
        keywords = [k.strip() for k in keywords_input.split(',')]
    
    locations_input = input("Enter search locations (comma-separated): ").strip()
    if not locations_input:
        locations = ["United States", "New York", "San Francisco", "Remote"]
        print(f"Using default locations: {locations}")
    else:
        locations = [l.strip() for l in locations_input.split(',')]
    
    companies_input = input("Enter target companies (comma-separated, optional): ").strip()
    companies = [c.strip() for c in companies_input.split(',')] if companies_input else None
    
    print(f"\n🎯 Generation Configuration:")
    print(f"Number of keywords: {len(keywords)}")
    print(f"Number of locations: {len(locations)}")
    print(f"Target companies: {len(companies) if companies else 0}")
    
    # Generate all search links
    search_data = create_quick_access_csv(keywords, locations, companies)
    
    # Create files folder if it doesn't exist
    files_folder = "files"
    if not os.path.exists(files_folder):
        os.makedirs(files_folder)
        print(f"📁 Created {files_folder} folder")
    
    # Save as CSV in files folder
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f"{files_folder}/linkedin_job_search_links_{timestamp}.csv"
    
    df = pd.DataFrame(search_data)
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Search links saved to: {csv_filename}")
    print(f"📊 Generated {len(search_data)} search links")
    
    # Display statistics
    category_counts = df['category'].value_counts()
    print(f"\n📈 Link Type Statistics:")
    for category, count in category_counts.items():
        print(f"  {category}: {count} links")
    
    # Display first 10 links as examples
    print(f"\n🔝 First 10 Search Links:")
    for i, row in df.head(10).iterrows():
        print(f"{i+1:2d}. {row['search_type']} | {row['keyword']} @ {row['location']}")
        print(f"    {row['url'][:80]}...")
    
    # Generate JSON format (structured data) in files folder
    json_filename = f"{files_folder}/linkedin_searches_structured_{timestamp}.json"
    structured_data = generate_linkedin_job_links(keywords, locations, companies)
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Structured data saved to: {json_filename}")
    
    print(f"\n💡 Usage Tips:")
    print(f"1. Open the CSV file in Excel or Google Sheets")
    print(f"2. Click on URL column links to directly access LinkedIn searches")
    print(f"3. Filter by different search types as needed")
    print(f"4. Use different LinkedIn search filters for comprehensive results")
    
    # Test accessibility of a few links
    print(f"\n🔍 Testing Link Accessibility...")
    import requests
    
    test_urls = df.head(3)['url'].tolist()
    
    for i, url in enumerate(test_urls):
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            status = "✅" if response.status_code in [200, 302] else f"❌ {response.status_code}"
            print(f"{i+1}. {status} - {url[:60]}...")
        except Exception as e:
            print(f"{i+1}. ❌ Network error - {url[:60]}...")

if __name__ == "__main__":
    main()