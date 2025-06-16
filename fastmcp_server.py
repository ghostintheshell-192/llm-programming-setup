#!/usr/bin/env python3
"""
LLM Programming Setup MCP Server using FastMCP
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP

# Set up the current directory and paths
import os
import sys

# Set environment like Claude Desktop would
os.environ["PYTHONPATH"] = "/data/repos/meta-projects/llm-programming-setup/src"
os.chdir("/data/repos/meta-projects/llm-programming-setup")
sys.path.insert(0, "/data/repos/meta-projects/llm-programming-setup/src")

# Now import our tools
from llm_programming_setup_mcp.tools.project_scanner import ProjectScanner
from llm_programming_setup_mcp.tools.context_generator import ContextGenerator
from llm_programming_setup_mcp.tools.template_processor import TemplateProcessor
from llm_programming_setup_mcp.tools.token_optimizer import TokenOptimizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP app
app = FastMCP(
    title="LLM Programming Setup",
    description="A server for LLM-agnostic programming setup and context optimization",
    version="1.0.0"
)

# Initialize tools
project_scanner = ProjectScanner()
context_generator = ContextGenerator()
template_processor = TemplateProcessor()
token_optimizer = TokenOptimizer()

@app.tool()
def scan_project(path: str = ".") -> Dict[str, Any]:
    """
    Scan project directory to detect language and applicable standards.
    
    Args:
        path: Path to project directory (default: current directory)
        
    Returns:
        Dictionary with scan results including detected language, confidence, and applicable standards
    """
    try:
        # Now using synchronous method - no more asyncio conflict
        result = project_scanner.scan(path)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.tool()
def generate_context(path: str = ".", project_name: Optional[str] = None) -> str:
    """
    Generate universal LLM context file based on project scan.
    
    Args:
        path: Path to project directory (default: current directory)
        project_name: Override project name (default: directory name)
        
    Returns:
        Generated context content as string
    """
    try:
        # First scan the project
        scan_result = project_scanner.scan(path)
        
        # Generate context
        context = context_generator.generate(
            scan_result, 
            project_name=project_name
        )
        
        return context
    except Exception as e:
        return f"Error: {str(e)}"

@app.tool()
def show_copy_instructions() -> str:
    """
    Show instructions for using generated context with different LLMs.
    
    Returns:
        Instructions as string
    """
    try:
        instructions = template_processor.get_copy_instructions()
        return instructions
    except Exception as e:
        return f"Error: {str(e)}"

@app.tool()
def estimate_tokens(context_file: str) -> Dict[str, Any]:
    """
    Estimate token count for generated context.
    
    Args:
        context_file: Path to context file to analyze
        
    Returns:
        Dictionary with token estimation results
    """
    try:
        estimation = token_optimizer.estimate_tokens(context_file)
        return estimation
    except Exception as e:
        return {"error": str(e)}

@app.tool()
def optimize_context(context_file: str) -> Dict[str, Any]:
    """
    Analyze context and suggest optimizations to reduce token usage.
    
    Args:
        context_file: Path to context file to optimize
        
    Returns:
        Dictionary with optimization suggestions
    """
    try:
        optimizations = token_optimizer.suggest_optimizations(context_file)
        return optimizations
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("Starting LLM Programming Setup FastMCP Server...")
    app.run()