"""
Test JSON loading logic to verify it can extract job_postings correctly
"""
import json
import os
import glob

def test_load_job_postings():
    """Test the exact loading logic used in the app"""
    postings = None
    
    # Try multiple sources (same as in the app)
    search_files = [
        "src/outputs/linkedin/latest_search_results.json",
        "src/outputs/linkedin/job_postings.json",
    ]
    
    # Also check for timestamped search_results files
    linkedin_dir = "src/outputs/linkedin"
    if os.path.exists(linkedin_dir):
        timestamped_files = sorted(
            glob.glob(f"{linkedin_dir}/search_results_*.json"),
            reverse=True  # Most recent first
        )
        search_files.extend(timestamped_files[:3])  # Add top 3 recent
    
    print("=" * 70)
    print("Testing Job Postings JSON Loading Logic")
    print("=" * 70)
    
    for i, job_file in enumerate(search_files, 1):
        print(f"\n{i}. Checking: {job_file}")
        
        if not os.path.exists(job_file):
            print("   ❌ File not found")
            continue
        
        file_size = os.path.getsize(job_file)
        print(f"   📁 Size: {file_size:,} bytes")
            
        try:
            with open(job_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
                # Skip empty files
                if not content:
                    print("   ⚠️  Empty file")
                    continue
                
                # Try to parse JSON
                data = json.loads(content)
                print(f"   ✅ Valid JSON")
                
                # Check different possible structures
                if isinstance(data, dict):
                    # Method 1: Direct job_postings array
                    if "job_postings" in data:
                        found_postings = data["job_postings"]
                        if found_postings:
                            postings = found_postings
                            print(f"   ✅ Found {len(postings)} jobs in 'job_postings' field")
                            print(f"   🎯 SELECTED THIS FILE!")
                            break
                        else:
                            print(f"   ⚠️  'job_postings' field is empty")
                    
                    # Method 2: Nested in crew_output (CrewAI format)
                    if "crew_output" in data:
                        print("   🔍 Found 'crew_output' field, trying to parse...")
                        try:
                            crew_data = json.loads(data["crew_output"]) if isinstance(data["crew_output"], str) else data["crew_output"]
                            if isinstance(crew_data, dict) and "job_postings" in crew_data:
                                found_postings = crew_data["job_postings"]
                                if found_postings:
                                    postings = found_postings
                                    print(f"   ✅ Extracted {len(postings)} jobs from crew_output")
                                    print(f"   🎯 SELECTED THIS FILE!")
                                    break
                        except Exception as e:
                            print(f"   ❌ Failed to parse crew_output: {e}")
                else:
                    print(f"   ⚠️  Data is not a dictionary: {type(data)}")
        
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON decode error: {e}")
            # Show first 100 chars
            with open(job_file, 'r', encoding='utf-8') as f:
                preview = f.read(100)
                print(f"   Preview: {preview}...")
        except Exception as e:
            print(f"   ❌ Other error: {e}")
    
    print("\n" + "=" * 70)
    if postings:
        print(f"✅ SUCCESS: Loaded {len(postings)} job postings")
        print("\nFirst 3 jobs:")
        for i, job in enumerate(postings[:3], 1):
            print(f"\n{i}. {job.get('job_title', 'No title')}")
            print(f"   Company: {job.get('company_name', 'Unknown')}")
            print(f"   Location: {job.get('location', 'Unknown')}")
            print(f"   URL: {job.get('application_url', 'No URL')[:70]}...")
    else:
        print("❌ FAILED: No job postings found")
        print("\n💡 Suggestions:")
        print("   1. Run a new search in the Streamlit app")
        print("   2. Run: python quick_test_linkedin_tool.py")
        print("   3. Check that LinkinJobSearchTool is saving correctly")
    
    print("=" * 70)
    return postings is not None and len(postings) > 0

if __name__ == "__main__":
    success = test_load_job_postings()
    exit(0 if success else 1)
