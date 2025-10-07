"""
快速LinkedIn搜索链接生成器
专注于生成有效的LinkedIn搜索URL，不涉及数据抓取
适用于快速生成搜索链接进行手动浏览
"""

import pandas as pd
import urllib.parse
from datetime import datetime
import json

def generate_linkedin_job_links(keywords, locations, companies=None):
    """
    生成LinkedIn职位搜索链接
    
    参数:
    - keywords: 搜索关键词列表
    - locations: 地点列表
    - companies: 公司名称列表（可选）
    
    返回: 包含所有搜索组合的字典
    """
    
    search_links = []
    
    for keyword in keywords:
        for location in locations:
            # URL编码
            keyword_encoded = urllib.parse.quote(keyword)
            location_encoded = urllib.parse.quote(location)
            
            # 基础搜索链接
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
            
            # Google搜索LinkedIn的链接
            google_searches = {
                'google_basic': f"https://www.google.com/search?q=site:linkedin.com/jobs+{keyword_encoded}+{location_encoded}",
                'google_recent': f"https://www.google.com/search?q=site:linkedin.com/jobs+{keyword_encoded}+{location_encoded}&tbs=qdr:w",
                'google_exact': f"https://www.google.com/search?q=site:linkedin.com/jobs/view+{keyword_encoded}+location:{location_encoded}"
            }
            
            # 合并链接
            combined_links = {**base_link, **google_searches}
            
            # 如果提供了公司列表，添加公司特定搜索
            if companies:
                company_links = {}
                for company in companies:
                    company_encoded = urllib.parse.quote(company)
                    company_slug = company.lower().replace(' ', '-').replace('&', 'and')
                    
                    company_links[f'company_{company}'] = {
                        'jobs_page': f"https://www.linkedin.com/company/{company_slug}/jobs/",
                        'jobs_search': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_C={company_encoded}",
                        'google_company': f"https://www.google.com/search?q={company_encoded}+{keyword_encoded}+site:linkedin.com/jobs"
                    }
                
                combined_links['companies'] = company_links
            
            search_links.append(combined_links)
    
    return search_links

def create_quick_access_csv(keywords, locations, companies=None):
    """
    创建快速访问的CSV文件
    """
    
    print("🔗 生成LinkedIn搜索链接...")
    
    all_links = []
    
    for keyword in keywords:
        for location in locations:
            # URL编码
            keyword_encoded = urllib.parse.quote(keyword)
            location_encoded = urllib.parse.quote(location)
            
            # 创建基础搜索记录
            searches = [
                {
                    'search_type': '基础搜索',
                    'keyword': keyword,
                    'location': location,
                    'description': '标准LinkedIn职位搜索',
                    'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}",
                    'category': 'linkedin_direct'
                },
                {
                    'search_type': '最新职位',
                    'keyword': keyword,
                    'location': location,
                    'description': '按时间排序的最新职位',
                    'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&sortBy=DD",
                    'category': 'linkedin_direct'
                },
                {
                    'search_type': '快速申请',
                    'keyword': keyword,
                    'location': location,
                    'description': '支持一键申请的职位',
                    'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_AL=true",
                    'category': 'linkedin_direct'
                },
                {
                    'search_type': '远程工作',
                    'keyword': keyword,
                    'location': location,
                    'description': '远程办公职位',
                    'url': f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&f_WT=2",
                    'category': 'linkedin_direct'
                },
                {
                    'search_type': 'Google搜索LinkedIn',
                    'keyword': keyword,
                    'location': location,
                    'description': '通过Google搜索LinkedIn职位',
                    'url': f"https://www.google.com/search?q=site:linkedin.com/jobs+{keyword_encoded}+{location_encoded}",
                    'category': 'google_search'
                },
                {
                    'search_type': 'Google最近一周',
                    'keyword': keyword,
                    'location': location,
                    'description': 'Google搜索最近一周的LinkedIn职位',
                    'url': f"https://www.google.com/search?q=site:linkedin.com/jobs+{keyword_encoded}+{location_encoded}&tbs=qdr:w",
                    'category': 'google_search'
                }
            ]
            
            all_links.extend(searches)
            
            # 如果提供了公司，添加公司特定搜索
            if companies:
                for company in companies:
                    company_slug = company.lower().replace(' ', '-').replace('&', 'and')
                    
                    company_searches = [
                        {
                            'search_type': f'{company} - 公司职位页',
                            'keyword': keyword,
                            'location': location,
                            'description': f'{company}公司的LinkedIn职位页面',
                            'url': f"https://www.linkedin.com/company/{company_slug}/jobs/",
                            'category': 'company_page'
                        },
                        {
                            'search_type': f'{company} - Google搜索',
                            'keyword': keyword,
                            'location': location,
                            'description': f'Google搜索{company}在LinkedIn的{keyword}职位',
                            'url': f"https://www.google.com/search?q={urllib.parse.quote(company)}+{keyword_encoded}+site:linkedin.com/jobs",
                            'category': 'company_google'
                        }
                    ]
                    
                    all_links.extend(company_searches)
    
    # 添加创建时间
    for link in all_links:
        link['created_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return all_links

def main():
    """
    主函数 - 快速生成LinkedIn搜索链接
    """
    print("🔗 LinkedIn快速搜索链接生成器")
    print("=" * 50)
    print("生成各种LinkedIn搜索链接，无需API或数据抓取")
    print()
    
    # 用户输入
    keywords_input = input("请输入搜索关键词 (用逗号分隔): ").strip()
    if not keywords_input:
        keywords = ["data scientist", "python developer", "machine learning engineer"]
        print(f"使用默认关键词: {keywords}")
    else:
        keywords = [k.strip() for k in keywords_input.split(',')]
    
    locations_input = input("请输入搜索地点 (用逗号分隔): ").strip()
    if not locations_input:
        locations = ["United States", "New York", "San Francisco", "Remote"]
        print(f"使用默认地点: {locations}")
    else:
        locations = [l.strip() for l in locations_input.split(',')]
    
    companies_input = input("请输入目标公司 (用逗号分隔, 可选): ").strip()
    companies = [c.strip() for c in companies_input.split(',')] if companies_input else None
    
    print(f"\n🎯 生成配置:")
    print(f"关键词数量: {len(keywords)}")
    print(f"地点数量: {len(locations)}")
    print(f"目标公司: {len(companies) if companies else 0}")
    
    # 生成所有搜索链接
    search_data = create_quick_access_csv(keywords, locations, companies)
    
    # 保存为CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f"linkedin_search_links_{timestamp}.csv"
    
    df = pd.DataFrame(search_data)
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ 搜索链接已保存到: {csv_filename}")
    print(f"📊 生成了 {len(search_data)} 个搜索链接")
    
    # 显示统计
    category_counts = df['category'].value_counts()
    print(f"\n📈 链接类型统计:")
    for category, count in category_counts.items():
        print(f"  {category}: {count} 个链接")
    
    # 显示前10个链接示例
    print(f"\n🔝 前10个搜索链接:")
    for i, row in df.head(10).iterrows():
        print(f"{i+1:2d}. {row['search_type']} | {row['keyword']} @ {row['location']}")
        print(f"    {row['url'][:80]}...")
    
    # 生成JSON格式（结构化数据）
    json_filename = f"linkedin_searches_structured_{timestamp}.json"
    structured_data = generate_linkedin_job_links(keywords, locations, companies)
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 结构化数据已保存到: {json_filename}")
    
    print(f"\n💡 使用建议:")
    print(f"1. 在Excel或Google Sheets中打开CSV文件")
    print(f"2. 点击URL列的链接直接访问LinkedIn搜索")
    print(f"3. 根据需要筛选不同的搜索类型")
    print(f"4. 结合Google搜索获得更全面的结果")
    
    # 测试几个链接的可访问性
    print(f"\n🔍 测试链接可访问性...")
    import requests
    
    test_urls = df.head(3)['url'].tolist()
    
    for i, url in enumerate(test_urls):
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            status = "✅" if response.status_code in [200, 302] else f"❌ {response.status_code}"
            print(f"{i+1}. {status} - {url[:60]}...")
        except Exception as e:
            print(f"{i+1}. ❌ 网络错误 - {url[:60]}...")

if __name__ == "__main__":
    main()