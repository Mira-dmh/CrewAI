"""
JSON Manager - Utility functions for handling search result JSON files
"""

import json
import os
import glob
from datetime import datetime
from typing import Dict, List, Optional


class SearchResultsManager:
    """Manager for handling LinkedIn search results JSON files"""
    
    RESULTS_DIR = "src/outputs/linkedin"
    LATEST_FILE = "latest_search_results.json"
    
    @classmethod
    def ensure_directory_exists(cls):
        """Ensure the results directory exists"""
        os.makedirs(cls.RESULTS_DIR, exist_ok=True)
    
    @classmethod
    def save_search_results(cls, search_data: Dict, job_title: str, location: str = None, **kwargs) -> str:
        """
        Save search results to JSON file with timestamp
        
        Args:
            search_data: The search results from CrewAI
            job_title: Job title searched for
            location: Location searched (optional)
            **kwargs: Additional search parameters
            
        Returns:
            str: Path to the saved file
        """
        cls.ensure_directory_exists()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"search_results_{timestamp}.json"
        filepath = os.path.join(cls.RESULTS_DIR, filename)
        
        # Structure the data for saving
        structured_data = {
            "search_metadata": {
                "job_title": job_title,
                "location": location or "",
                "search_timestamp": datetime.now().isoformat(),
                "search_parameters": kwargs
            },
            "crew_output": str(search_data),
            "raw_result": search_data
        }
        
        # Save timestamped file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=2, ensure_ascii=False, default=str)
            
            # Also save as latest file
            latest_filepath = os.path.join(cls.RESULTS_DIR, cls.LATEST_FILE)
            with open(latest_filepath, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=2, ensure_ascii=False, default=str)
                
            return filepath
            
        except Exception as e:
            print(f"Error saving search results: {e}")
            return None
    
    @classmethod
    def load_latest_results(cls) -> Optional[Dict]:
        """
        Load the latest search results
        
        Returns:
            Dict: Latest search results or None if not found
        """
        filepath = os.path.join(cls.RESULTS_DIR, cls.LATEST_FILE)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading latest results: {e}")
                return None
        return None
    
    @classmethod
    def get_all_result_files(cls) -> List[str]:
        """
        Get all search result files, sorted by date (newest first)
        
        Returns:
            List[str]: List of file paths
        """
        if not os.path.exists(cls.RESULTS_DIR):
            return []
        
        pattern = os.path.join(cls.RESULTS_DIR, "search_results_*.json")
        files = glob.glob(pattern)
        return sorted(files, reverse=True)  # Most recent first
    
    @classmethod
    def load_results_by_file(cls, filepath: str) -> Optional[Dict]:
        """
        Load search results from specific file
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            Dict: Search results or None if error
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading results from {filepath}: {e}")
            return None
    
    @classmethod
    def get_search_summary(cls) -> Dict:
        """
        Get summary of all searches
        
        Returns:
            Dict: Summary information
        """
        all_files = cls.get_all_result_files()
        
        summary = {
            "total_searches": len(all_files),
            "latest_search": None,
            "search_history": []
        }
        
        if all_files:
            # Get latest search info
            latest = cls.load_results_by_file(all_files[0])
            if latest:
                metadata = latest.get("search_metadata", {})
                summary["latest_search"] = {
                    "job_title": metadata.get("job_title"),
                    "location": metadata.get("location"),
                    "timestamp": metadata.get("search_timestamp")
                }
            
            # Get history (last 10 searches)
            for filepath in all_files[:10]:
                results = cls.load_results_by_file(filepath)
                if results:
                    metadata = results.get("search_metadata", {})
                    summary["search_history"].append({
                        "job_title": metadata.get("job_title"),
                        "location": metadata.get("location"),
                        "timestamp": metadata.get("search_timestamp"),
                        "file": os.path.basename(filepath)
                    })
        
        return summary
    
    @classmethod
    def export_results_as_csv(cls, output_path: str = None) -> str:
        """
        Export all search results to CSV format
        
        Args:
            output_path: Optional output path, defaults to results directory
            
        Returns:
            str: Path to the exported CSV file
        """
        import pandas as pd
        
        all_files = cls.get_all_result_files()
        
        if not all_files:
            return None
        
        # Collect data from all searches
        export_data = []
        
        for filepath in all_files:
            results = cls.load_results_by_file(filepath)
            if results:
                metadata = results.get("search_metadata", {})
                export_data.append({
                    "job_title": metadata.get("job_title"),
                    "location": metadata.get("location"),
                    "search_timestamp": metadata.get("search_timestamp"),
                    "search_parameters": str(metadata.get("search_parameters", {})),
                    "crew_output": results.get("crew_output", "")[:500],  # Truncate for CSV
                    "filename": os.path.basename(filepath)
                })
        
        if export_data:
            df = pd.DataFrame(export_data)
            
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(cls.RESULTS_DIR, f"search_export_{timestamp}.csv")
            
            df.to_csv(output_path, index=False)
            return output_path
        
        return None


# Convenience functions for direct use
def save_linkedin_search(result, job_title: str, location: str = None, **kwargs) -> str:
    """Convenience function to save LinkedIn search results"""
    return SearchResultsManager.save_search_results(result, job_title, location, **kwargs)


def load_latest_linkedin_search() -> Optional[Dict]:
    """Convenience function to load latest LinkedIn search results"""
    return SearchResultsManager.load_latest_results()


def get_linkedin_search_history() -> List[str]:
    """Convenience function to get all LinkedIn search files"""
    return SearchResultsManager.get_all_result_files()