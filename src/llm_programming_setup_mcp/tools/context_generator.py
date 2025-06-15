"""Context generator for creating universal LLM context files."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from ..utils import find_rules_directory, safe_file_read

logger = logging.getLogger(__name__)


class ContextGenerator:
    """Generates universal LLM context files based on project scan results."""
    
    def __init__(self) -> None:
        """Initialize the context generator."""
        self.rules_path = find_rules_directory()
        self.templates_path = Path(__file__).parent.parent / "templates"
    
    async def generate(self, scan_result: Dict[str, Any], project_name: Optional[str] = None) -> str:
        """
        Generate universal LLM context based on scan results.
        
        Args:
            scan_result: Results from project scanner
            project_name: Override project name
            
        Returns:
            Generated context as string
        """
        if "error" in scan_result:
            return f"Error: Cannot generate context - {scan_result['error']}"
        
        # Extract information from scan result
        detected_project_name = project_name or scan_result.get("project_name", "unknown-project")
        primary_language = scan_result.get("primary_language")
        confidence = scan_result.get("confidence", 0.0)
        standards = scan_result.get("applicable_standards", [])
        mandatory_files = scan_result.get("mandatory_files", {})
        
        # Load standards content
        standards_content = await self._load_standards_content(standards)
        
        # Generate context
        context = self._build_context(
            project_name=detected_project_name,
            primary_language=primary_language,
            confidence=confidence,
            standards_content=standards_content,
            mandatory_files=mandatory_files,
            scan_result=scan_result
        )
        
        return context
    
    async def _load_standards_content(self, standards: list) -> Dict[str, str]:
        """Load content from standards files with caching."""
        content = {}
        
        for standard_file in standards:
            file_path = self.rules_path / standard_file
            
            # Use cached file reading
            file_content = safe_file_read(file_path, use_cache=True)
            if file_content is not None:
                content[standard_file] = file_content
            else:
                logger.warning(f"Could not load {standard_file}")
                content[standard_file] = f"# {standard_file}\n\n*Content not available*"
        
        return content
    
    def _build_context(
        self, 
        project_name: str,
        primary_language: Optional[str],
        confidence: float,
        standards_content: Dict[str, str],
        mandatory_files: Dict[str, Any],
        scan_result: Dict[str, Any]
    ) -> str:
        """Build the universal context file content."""
        
        # Header
        context_lines = [
            f"# LLM Context - {project_name}",
            "",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by llm-programming-setup-mcp*",
            "",
            "## Project Detection Results",
            ""
        ]
        
        # Project info
        if primary_language:
            context_lines.extend([
                f"**Detected Language:** {primary_language} (confidence: {confidence:.1%})",
                f"**Project Type:** {scan_result.get('detected_languages', {}).get(primary_language, {}).get('description', 'Unknown')}",
                ""
            ])
        else:
            context_lines.extend([
                "**Detected Language:** Unknown/Mixed",
                "**Project Type:** Generic project",
                ""
            ])
        
        # File summary
        context_lines.extend([
            f"**Total Files Scanned:** {scan_result.get('total_files', 0)}",
            ""
        ])
        
        # Mandatory files status
        if mandatory_files.get("required"):
            context_lines.extend([
                "### Required Files Status",
                ""
            ])
            
            for file in mandatory_files["required"]:
                status = "✅" if file in mandatory_files["present"] else "❌"
                context_lines.append(f"- {status} {file}")
            
            context_lines.append("")
            
            if mandatory_files["missing"]:
                context_lines.extend([
                    "**Missing Files:** Consider creating the following files:",
                    ""
                ])
                for file in mandatory_files["missing"]:
                    context_lines.append(f"- {file}")
                context_lines.append("")
        
        # Standards content
        context_lines.extend([
            "---",
            "",
            "## Applicable Coding Standards",
            ""
        ])
        
        for standard_file, content in standards_content.items():
            context_lines.extend([
                f"### {standard_file}",
                "",
                content,
                "",
                "---",
                ""
            ])
        
        # Copy instructions
        context_lines.extend([
            "## How to Use This Context",
            "",
            "This file contains universal coding standards and project context that work with any LLM.",
            "Copy the content as follows:",
            "",
            "### Claude (Anthropic)",
            "1. Rename this file to `CLAUDE.md`",
            "2. Place in your project root directory",
            "3. Claude will automatically read it",
            "",
            "### ChatGPT (OpenAI)", 
            "1. Create a new Project in ChatGPT",
            "2. Copy this content to Project's Custom Instructions",
            "3. Or upload as a file to the Project's Knowledge base",
            "",
            "### Gemini (Google)",
            "1. For Firebase Studio: Copy to `.idx/airules.md`",
            "2. For GitHub: Copy to `.gemini/styleguide.md`", 
            "3. For general use: Reference as needed",
            "",
            "### Other LLMs",
            "- Use as system prompt or context document",
            "- Reference key sections as needed",
            "- Adapt file name to your LLM's conventions",
            "",
            "---",
            "",
            f"*Context optimized for token efficiency • LLM-agnostic design • Generated by llm-programming-setup-mcp*"
        ])
        
        return "\n".join(context_lines)
    
    def get_summary(self, scan_result: Dict[str, Any]) -> str:
        """Get a brief summary of the generated context."""
        if "error" in scan_result:
            return f"Error: {scan_result['error']}"
        
        primary_language = scan_result.get("primary_language", "Unknown")
        confidence = scan_result.get("confidence", 0.0)
        standards_count = len(scan_result.get("applicable_standards", []))
        
        return (
            f"Generated context for {primary_language} project "
            f"(confidence: {confidence:.1%}, {standards_count} standards applied)"
        )