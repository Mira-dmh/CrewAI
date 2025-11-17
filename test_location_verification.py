"""
Test Location Extraction and Verification
"""

from Tools.LinkedInJobSearchTool import LinkedInJobSearchTool
from Tools.LocationVerificationTool import LocationVerificationTool
import json

def test_location_extraction():
    """Test the location extraction from LinkedIn snippets"""
    
    tool = LinkedInJobSearchTool()
    
    test_cases = [
        {
            "title": "Google Cloud Data & AI Engineer - Slalom",
            "snippet": "Google Cloud Data & AI Engineer. Slalom Calgary, Alberta, Canada. Just now 168 applicants.",
            "expected": "Calgary, Alberta"
        },
        {
            "title": "AI Engineer with Google ADK - Avance Consulting",
            "snippet": "Role: AI Engineer with Google ADK. Location: Cupertino, CA or Sunnyvale, CA. Position Type: Full Time.",
            "expected": "Cupertino, CA"
        },
        {
            "title": "AI Developer Engineer, Cloud AI in Mountain View, CA",
            "snippet": "Mountain View, CA $152,000 - $228,000 2 weeks ago. Python AI Engineer.",
            "expected": "Mountain View, CA"
        },
        {
            "title": "Software Engineer - Toronto Office",
            "snippet": "We are hiring in Toronto, Ontario for a senior software engineer position.",
            "expected": "Toronto, Ontario"
        }
    ]
    
    print("🧪 Testing Location Extraction\n")
    print("=" * 80)
    
    for i, case in enumerate(test_cases, 1):
        result = tool._extract_location_from_text(case["title"], case["snippet"])
        passed = case["expected"] in result or result in case["expected"]
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"\nTest {i}: {status}")
        print(f"Title: {case['title'][:60]}...")
        print(f"Snippet: {case['snippet'][:60]}...")
        print(f"Expected: {case['expected']}")
        print(f"Got: {result}")
    
    print("\n" + "=" * 80)


def test_location_verification():
    """Test the location verification tool"""
    
    tool = LocationVerificationTool()
    
    test_cases = [
        {
            "search": "CA",
            "actual": "Calgary, Alberta",
            "should_match": False,
            "reason": "CA = California, not Canada"
        },
        {
            "search": "CA",
            "actual": "San Francisco, CA",
            "should_match": True,
            "reason": "Both are California"
        },
        {
            "search": "CA",
            "actual": "Toronto, Ontario",
            "should_match": False,
            "reason": "Toronto is in Canada, not California"
        },
        {
            "search": "San Francisco",
            "actual": "San Francisco, CA",
            "should_match": True,
            "reason": "City name matches"
        },
        {
            "search": "NY",
            "actual": "New York, NY",
            "should_match": True,
            "reason": "New York state matches"
        },
        {
            "search": "NY",
            "actual": "Los Angeles, CA",
            "should_match": False,
            "reason": "Different states"
        }
    ]
    
    print("\n\n🧪 Testing Location Verification\n")
    print("=" * 80)
    
    for i, case in enumerate(test_cases, 1):
        result_json = tool._run(case["search"], case["actual"])
        result = json.loads(result_json)
        
        match_status = result["match_status"]
        is_match = match_status == "MATCH"
        passed = is_match == case["should_match"]
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"\nTest {i}: {status}")
        print(f"Search: '{case['search']}' | Actual: '{case['actual']}'")
        print(f"Expected: {'MATCH' if case['should_match'] else 'MISMATCH'}")
        print(f"Got: {match_status} (confidence: {result['match_confidence']})")
        print(f"Reason: {result.get('reason', 'N/A')}")
        if not passed:
            print(f"⚠️  Test reason: {case['reason']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_location_extraction()
    test_location_verification()
    print("\n\n✨ All tests completed!\n")
