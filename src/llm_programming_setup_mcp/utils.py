"""Shared utilities for LLM Programming Setup MCP Server."""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def find_rules_directory() -> Optional[Path]:
    """
    Find the rules directory containing configuration files.
    
    Tries multiple locations in order:
    1. Current working directory / rules
    2. Package directory / rules  
    3. Alternative package structure / rules
    
    Returns:
        Path to rules directory if found, None otherwise
    """
    current_dir = Path.cwd()
    rules_candidates = [
        current_dir / "rules",  # When running from project root
        Path(__file__).parent.parent / "rules",  # When installed as package
        Path(__file__).parent.parent.parent / "rules"  # Alternative structure
    ]
    
    for candidate in rules_candidates:
        if candidate.exists() and (candidate / "goto.yaml").exists():
            logger.debug(f"Found rules directory at: {candidate}")
            return candidate
    
    # Fallback to package location
    fallback = Path(__file__).parent.parent / "rules"
    logger.warning(f"Rules directory not found, using fallback: {fallback}")
    return fallback


def safe_file_read(file_path: Path, encoding: str = 'utf-8') -> Optional[str]:
    """
    Safely read a file with proper error handling.
    
    Args:
        file_path: Path to file to read
        encoding: File encoding (default: utf-8)
        
    Returns:
        File content as string, or None if error occurred
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        return None


def ensure_directory(directory_path: Path) -> bool:
    """
    Ensure directory exists, create if necessary.
    
    Args:
        directory_path: Path to directory
        
    Returns:
        True if directory exists or was created successfully
    """
    try:
        directory_path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory_path}: {e}")
        return False