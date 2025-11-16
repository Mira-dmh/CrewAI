# Single-Agent vs Multi-Agent Comparison Study

This directory contains tools for running comprehensive comparison studies between single-agent and multi-agent CrewAI job search systems.

## 📁 Directory Structure

```
single-agent/
├── single.py                    # Single-agent crew implementation
├── cli_runner.py               # CLI for running single-agent searches
├── multi_agent_runner.py       # CLI for running multi-agent searches
├── compare_results.py          # Analysis and comparison tool
├── test_queries.json           # Sample batch queries
├── outputs/                    # Single-agent results
│   └── multi_agent/           # Multi-agent results
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Single Query Test

Run a single job search with the single-agent system:

```bash
cd /Users/dingdingjiang/CrewAI
python single-agent/cli_runner.py "Data Analyst" "New York, NY"
```

Run the same query with multi-agent system:

```bash
python single-agent/multi_agent_runner.py "Data Analyst" "New York, NY" --query-id comp_001
```

### 2. Batch Comparison Study

**Step 1: Run all queries through single-agent system**
```bash
python single-agent/cli_runner.py --batch single-agent/test_queries.json
```

**Step 2: Run all queries through multi-agent system**
```bash
python single-agent/multi_agent_runner.py --batch single-agent/test_queries.json
```

**Step 3: Analyze and compare results**
```bash
python single-agent/compare_results.py
```

This will output:
- Console summary with aggregate statistics
- `comparison_table_TIMESTAMP.csv` - Detailed comparison table
- `comparison_report_TIMESTAMP.json` - Full comparison report

## 📊 What Gets Measured

### Quantitative Metrics
- **Execution Time**: How long each system takes to complete the search
- **Jobs Mentioned**: Number of job postings referenced in output
- **Skills Identified**: Number of relevant skills extracted (out of 10 common skills)
- **Companies Mentioned**: Number of companies referenced
- **Salary Data Present**: Whether salary information is included (Yes/No)
- **Verification Present**: Whether verification/confidence data is included (Yes/No)
- **Success Rate**: Percentage of queries that completed successfully

### Expected Output Format

```
================================================================================
SINGLE-AGENT VS MULTI-AGENT COMPARISON SUMMARY
================================================================================

📊 Total Comparisons: 10

⏱️  EXECUTION TIME:
   Single-Agent Avg: 12.4 seconds
   Multi-Agent Avg:  4.6 seconds
   Improvement:      63.0% faster ✅

💼 JOBS MENTIONED:
   Single-Agent Avg: 15.2
   Multi-Agent Avg:  38.7
   Improvement:      +154.6%

🎯 SKILLS IDENTIFIED:
   Single-Agent Avg: 2.1 / 10
   Multi-Agent Avg:  2.9 / 10
   Improvement:      +38.1%

✅ SUCCESS RATES:
   Single-Agent: 90.0%
   Multi-Agent:  100.0%

💰 SALARY DATA PRESENCE:
   Single-Agent: 40.0%
   Multi-Agent:  80.0%

🔍 VERIFICATION PRESENCE:
   Single-Agent: 30.0%
   Multi-Agent:  90.0%
```

## 🎯 Test Queries

The default `test_queries.json` includes 10 diverse queries:

1. Data Analyst (Technology, Medium complexity)
2. Marketing Coordinator (Marketing, Low complexity)
3. Nurse Practitioner (Healthcare, Medium complexity)
4. Software Engineer (Technology, High complexity)
5. Financial Analyst (Finance, Medium complexity)
6. UX Designer (Design, Medium complexity)
7. Operations Manager (Business, High complexity)
8. Content Writer (Marketing, Low complexity)
9. Machine Learning Engineer (AI/ML, High complexity)
10. Human Resources Specialist (HR, Low complexity)

## ⚙️ CLI Options

### Single-Agent Runner

```bash
# Basic usage
python single-agent/cli_runner.py "Job Title" "Location"

# With custom query ID
python single-agent/cli_runner.py "Software Engineer" "SF, CA" --query-id comp_004

# Batch mode
python single-agent/cli_runner.py --batch queries.json

# Custom output directory
python single-agent/cli_runner.py "Designer" "Seattle, WA" --output-dir ./custom_results
```

### Multi-Agent Runner

```bash
# Basic usage
python single-agent/multi_agent_runner.py "Job Title" "Location"

# With query ID (for comparison tracking)
python single-agent/multi_agent_runner.py "Data Analyst" "NYC" --query-id comp_001

# Batch mode
python single-agent/multi_agent_runner.py --batch test_queries.json
```

### Comparison Analyzer

```bash
# Default directories
python single-agent/compare_results.py

# Custom directories
python single-agent/compare_results.py \
  --single-dir ./my_single_results \
  --multi-dir ./my_multi_results
```

## 📝 Creating Custom Test Queries

Create a JSON file with your queries:

```json
[
  {
    "query_id": "custom_001",
    "job_title": "DevOps Engineer",
    "location": "Remote",
    "complexity": "high",
    "industry": "Technology"
  },
  {
    "query_id": "custom_002",
    "job_title": "Sales Manager",
    "location": "Dallas, TX",
    "complexity": "medium",
    "industry": "Sales"
  }
]
```

Then run:
```bash
python single-agent/cli_runner.py --batch custom_queries.json
python single-agent/multi_agent_runner.py --batch custom_queries.json
python single-agent/compare_results.py
```

## 🔬 Research Use Cases

### 1. Performance Benchmarking
Compare execution speed and resource usage between architectures.

### 2. Quality Assessment
Evaluate completeness and accuracy of job market analysis.

### 3. Scalability Testing
Test how each system handles varying query complexities.

### 4. Industry-Specific Analysis
Compare performance across different industries (Tech, Healthcare, Finance, etc.).

## 📈 Output Files

After running comparisons, you'll find:

```
single-agent/outputs/
├── search_result_comp_001_TIMESTAMP.json    # Individual single-agent results
├── search_result_comp_002_TIMESTAMP.json
├── ...
├── comparison_table_TIMESTAMP.csv           # Detailed comparison table
├── comparison_report_TIMESTAMP.json         # Full JSON report
└── multi_agent/
    ├── search_result_comp_001_TIMESTAMP.json  # Individual multi-agent results
    ├── search_result_comp_002_TIMESTAMP.json
    └── ...
```

## 🎓 Example Workflow

```bash
# 1. Navigate to project directory
cd /Users/dingdingjiang/CrewAI

# 2. Activate virtual environment (if needed)
source .venv/bin/activate

# 3. Run single-agent batch
echo "Running single-agent searches..."
python single-agent/cli_runner.py --batch single-agent/test_queries.json

# 4. Run multi-agent batch
echo "Running multi-agent searches..."
python single-agent/multi_agent_runner.py --batch single-agent/test_queries.json

# 5. Generate comparison report
echo "Analyzing results..."
python single-agent/compare_results.py

# 6. View detailed results
open single-agent/outputs/comparison_table_*.csv
```

## 🚨 Important Notes

1. **Query IDs Must Match**: For proper comparison, use the same `query_id` in both systems
2. **Batch Mode**: Recommended for consistent comparisons across multiple queries
3. **Rate Limiting**: 2-second delay between queries to avoid API rate limits
4. **Environment Variables**: Ensure `.env` file has `OPENAI_API_KEY` and `SERPER_API_KEY`
5. **Terminal Only**: Single-agent system runs in terminal only (not integrated with Streamlit UI)

## 🐛 Troubleshooting

**Issue**: No matched results found
```bash
# Solution: Ensure query_ids match in both runs
python single-agent/cli_runner.py "Job Title" "Location" --query-id test_001
python single-agent/multi_agent_runner.py "Job Title" "Location" --query-id test_001
```

**Issue**: Import errors
```bash
# Solution: Run from project root directory
cd /Users/dingdingjiang/CrewAI
python single-agent/cli_runner.py --batch single-agent/test_queries.json
```

**Issue**: Missing API keys
```bash
# Solution: Check .env file
cat .env | grep -E "OPENAI|SERPER"
```

## 📚 Next Steps

After collecting comparison data:
1. Use results for academic papers or presentations
2. Conduct blind human evaluation (see main project docs)
3. Run statistical significance tests (t-tests, ANOVA)
4. Create visualizations with matplotlib/seaborn
5. Document findings in research report

---

**For questions or issues, see main project README.md**
