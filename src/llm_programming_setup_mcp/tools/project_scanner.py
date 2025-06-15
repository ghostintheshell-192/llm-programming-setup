"""Project scanner for detecting programming languages and project types."""

import os
import glob
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
import logging

logger = logging.getLogger(__name__)


class ProjectScanner:
    """Scans project directories to detect programming languages and applicable standards."""
    
    def __init__(self):
        """Initialize the project scanner with goto.yaml configuration."""
        # Look for rules directory - try relative to project root first
        current_dir = Path.cwd()
        rules_candidates = [
            current_dir / "rules",  # When running from project root
            Path(__file__).parent.parent.parent / "rules",  # When installed as package
            Path(__file__).parent.parent.parent.parent / "rules"  # Alternative structure
        ]
        
        self.rules_path = None
        for candidate in rules_candidates:
            if candidate.exists() and (candidate / "goto.yaml").exists():
                self.rules_path = candidate
                break
        
        if self.rules_path is None:
            # Fallback to package location
            self.rules_path = Path(__file__).parent.parent.parent / "rules"
            
        self.goto_config = self._load_goto_config()
    
    def _load_goto_config(self) -> Dict[str, Any]:
        """Load goto.yaml configuration."""
        goto_file = self.rules_path / "goto.yaml"
        try:
            with open(goto_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load goto.yaml: {e}")
            return {}
    
    async def scan(self, path: str = ".") -> Dict[str, Any]:
        """
        Scan project directory to detect programming language and standards.
        
        Args:
            path: Path to project directory
            
        Returns:
            Dictionary with scan results
        """
        project_path = Path(path).resolve()
        
        if not project_path.exists():
            return {
                "error": f"Path does not exist: {path}",
                "path": str(project_path)
            }
        
        if not project_path.is_dir():
            return {
                "error": f"Path is not a directory: {path}",
                "path": str(project_path)
            }
        
        # Get all files in the directory (non-recursive for performance)
        files = []
        try:
            for item in project_path.iterdir():
                if item.is_file():
                    files.append(item.name)
        except PermissionError:
            return {
                "error": f"Permission denied accessing: {path}",
                "path": str(project_path)
            }
        
        # Detect language based on file patterns
        detection_results = self._detect_languages(files)
        
        # Determine primary language using priority order
        primary_language = self._determine_primary_language(detection_results)
        
        # Get applicable standards
        standards = self._get_standards(primary_language) if primary_language else []
        
        # Check for mandatory files
        mandatory_files = self._check_mandatory_files(files, primary_language)
        
        return {
            "path": str(project_path),
            "project_name": project_path.name,
            "files_found": sorted(files),
            "detected_languages": detection_results,
            "primary_language": primary_language,
            "confidence": detection_results.get(primary_language, {}).get("confidence", 0.0) if primary_language else 0.0,
            "applicable_standards": standards,
            "mandatory_files": mandatory_files,
            "total_files": len(files)
        }
    
    def _detect_languages(self, files: List[str]) -> Dict[str, Dict[str, Any]]:
        """Detect programming languages based on file patterns."""
        detection_results = {}
        
        language_detection = self.goto_config.get("language_detection", {})
        
        for language, config in language_detection.items():
            file_patterns = config.get("files", [])
            matches = []
            
            for pattern in file_patterns:
                # Handle glob patterns
                if "*" in pattern:
                    matching_files = [f for f in files if self._match_pattern(f, pattern)]
                    matches.extend(matching_files)
                else:
                    # Exact match
                    if pattern in files:
                        matches.append(pattern)
            
            if matches:
                # Calculate confidence based on number of matches and file importance
                confidence = min(1.0, len(matches) * 0.3)
                
                # Boost confidence for key files
                key_files = ["package.json", "requirements.txt", "pubspec.yaml", "*.sln", "CMakeLists.txt"]
                for key_file in key_files:
                    if any(self._match_pattern(match, key_file) for match in matches):
                        confidence = min(1.0, confidence + 0.4)
                
                detection_results[language] = {
                    "confidence": confidence,
                    "matched_files": matches,
                    "description": config.get("description", f"{language} project")
                }
        
        return detection_results
    
    def _match_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches pattern (supports basic glob patterns)."""
        if "*" not in pattern:
            return filename == pattern
        
        # Simple glob matching
        if pattern.startswith("*."):
            extension = pattern[2:]
            return filename.endswith(f".{extension}")
        
        # More complex patterns would need fnmatch
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def _determine_primary_language(self, detection_results: Dict[str, Dict[str, Any]]) -> Optional[str]:
        """Determine primary language using confidence scores and priority order."""
        if not detection_results:
            return None
        
        # Get priority order from config
        priority_order = self.goto_config.get("multi_language", {}).get("priority_order", [])
        
        # First, try priority order
        for lang in priority_order:
            if lang in detection_results:
                return lang
        
        # If no priority match, use highest confidence
        return max(detection_results.keys(), key=lambda x: detection_results[x]["confidence"])
    
    def _get_standards(self, language: Optional[str]) -> List[str]:
        """Get applicable standards files for the detected language."""
        if not language:
            return ["coding-standards/general-principles.md"]
        
        language_detection = self.goto_config.get("language_detection", {})
        lang_config = language_detection.get(language, {})
        
        return lang_config.get("standards", ["coding-standards/general-principles.md"])
    
    def _check_mandatory_files(self, files: List[str], language: Optional[str]) -> Dict[str, Any]:
        """Check for mandatory files based on detected language."""
        if not language:
            return {"required": [], "missing": [], "present": []}
        
        language_detection = self.goto_config.get("language_detection", {})
        lang_config = language_detection.get(language, {})
        mandatory_files = lang_config.get("mandatory_files", [])
        
        present = [f for f in mandatory_files if f in files]
        missing = [f for f in mandatory_files if f not in files]
        
        return {
            "required": mandatory_files,
            "present": present,
            "missing": missing,
            "all_present": len(missing) == 0
        }