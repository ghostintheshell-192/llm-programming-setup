"""Token optimizer for estimating and optimizing LLM context token usage."""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Constants for token estimation
DEFAULT_WORDS_TO_TOKENS_RATIO = 1.3
CODE_BLOCK_TOKEN_MULTIPLIER = 50
INLINE_CODE_TOKEN_MULTIPLIER = 2
URL_TOKEN_MULTIPLIER = 5

# Cost estimates per 1k tokens (as of 2024)
LLM_COSTS_PER_1K = {
    "claude_sonnet": 0.003,
    "claude_haiku": 0.00025,
    "gpt4": 0.01,
    "gpt4_turbo": 0.01,
    "gpt35_turbo": 0.0005,
    "gemini_pro": 0.00025,
}


class TokenOptimizer:
    """Estimates token usage and suggests optimizations for LLM context."""
    
    def __init__(self):
        """Initialize the token optimizer."""
        # Rough token estimation (words * 1.3 for typical English text)
        # More accurate would require tiktoken, but we want to avoid heavy dependencies
        self.words_to_tokens_ratio = DEFAULT_WORDS_TO_TOKENS_RATIO
    
    async def estimate_tokens(self, context_file: str) -> Dict[str, Any]:
        """
        Estimate token count for a context file.
        
        Args:
            context_file: Path to context file
            
        Returns:
            Dictionary with token estimation and breakdown
        """
        file_path = Path(context_file)
        
        if not file_path.exists():
            return {
                "error": f"File not found: {context_file}",
                "estimated_tokens": 0
            }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "error": f"Could not read file: {e}",
                "estimated_tokens": 0
            }
        
        # Basic token estimation
        estimation = self._estimate_tokens_from_text(content)
        
        # Analyze content structure
        analysis = self._analyze_content_structure(content)
        
        return {
            "file": str(file_path),
            "file_size_bytes": len(content.encode('utf-8')),
            "character_count": len(content),
            "word_count": estimation["word_count"],
            "estimated_tokens": estimation["estimated_tokens"],
            "token_breakdown": estimation["breakdown"],
            "content_analysis": analysis,
            "cost_estimates": self._calculate_cost_estimates(estimation["estimated_tokens"]),
            "optimization_potential": self._assess_optimization_potential(content, analysis)
        }
    
    async def suggest_optimizations(self, context_file: str) -> Dict[str, Any]:
        """
        Analyze context and suggest optimizations to reduce token usage.
        
        Args:
            context_file: Path to context file
            
        Returns:
            Dictionary with optimization suggestions
        """
        # First get the token estimation
        estimation = await self.estimate_tokens(context_file)
        
        if "error" in estimation:
            return estimation
        
        file_path = Path(context_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate specific optimization suggestions
        suggestions = self._generate_optimization_suggestions(content, estimation)
        
        return {
            "file": str(file_path),
            "current_tokens": estimation["estimated_tokens"],
            "optimization_suggestions": suggestions,
            "potential_savings": sum(s.get("token_savings", 0) for s in suggestions),
            "priority_actions": [s for s in suggestions if s.get("priority", "low") == "high"],
            "implementation_difficulty": self._assess_implementation_difficulty(suggestions)
        }
    
    def _estimate_tokens_from_text(self, text: str) -> Dict[str, Any]:
        """Estimate tokens from text content."""
        # Basic word counting
        words = len(text.split())
        
        # Count special elements that might use more tokens
        code_blocks = len(re.findall(r'```[\s\S]*?```', text))
        inline_code = len(re.findall(r'`[^`]+`', text))
        urls = len(re.findall(r'https?://[^\s]+', text))
        
        # Rough token estimation
        base_tokens = int(words * self.words_to_tokens_ratio)
        
        # Add extra tokens for special content
        code_block_tokens = code_blocks * CODE_BLOCK_TOKEN_MULTIPLIER  # Code blocks tend to use more tokens
        inline_code_tokens = inline_code * INLINE_CODE_TOKEN_MULTIPLIER
        url_tokens = urls * URL_TOKEN_MULTIPLIER  # URLs often get tokenized into many parts
        
        total_tokens = base_tokens + code_block_tokens + inline_code_tokens + url_tokens
        
        return {
            "word_count": words,
            "estimated_tokens": total_tokens,
            "breakdown": {
                "base_tokens": base_tokens,
                "code_block_tokens": code_block_tokens,
                "inline_code_tokens": inline_code_tokens,
                "url_tokens": url_tokens,
                "special_content": {
                    "code_blocks": code_blocks,
                    "inline_code": inline_code,
                    "urls": urls
                }
            }
        }
    
    def _analyze_content_structure(self, content: str) -> Dict[str, Any]:
        """Analyze the structure of the content."""
        lines = content.split('\n')
        
        # Count different types of content
        headers = len([line for line in lines if line.strip().startswith('#')])
        bullet_points = len([line for line in lines if line.strip().startswith('-')])
        numbered_lists = len([line for line in lines if re.match(r'^\s*\d+\.\s', line)])
        empty_lines = len([line for line in lines if not line.strip()])
        
        # Identify sections
        sections = re.findall(r'^#+\s+(.+)', content, re.MULTILINE)
        
        return {
            "total_lines": len(lines),
            "headers": headers,
            "bullet_points": bullet_points,
            "numbered_lists": numbered_lists,
            "empty_lines": empty_lines,
            "sections": sections,
            "section_count": len(sections)
        }
    
    def _calculate_cost_estimates(self, token_count: int) -> Dict[str, float]:
        """Calculate cost estimates for different LLM providers."""
        token_k = token_count / 1000
        
        return {
            model: round(cost * token_k, 6)
            for model, cost in LLM_COSTS_PER_1K.items()
        }
    
    def _assess_optimization_potential(self, content: str, analysis: Dict[str, Any]) -> str:
        """Assess the optimization potential of the content."""
        total_tokens = self._estimate_tokens_from_text(content)["estimated_tokens"]
        
        if total_tokens < 1000:
            return "low"
        elif total_tokens < 5000:
            return "medium"
        else:
            return "high"
    
    def _generate_optimization_suggestions(self, content: str, estimation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific optimization suggestions."""
        suggestions = []
        
        # Check for verbose sections
        if estimation["word_count"] > 2000:
            suggestions.append({
                "type": "verbosity",
                "title": "Reduce verbose explanations",
                "description": "Content is quite verbose. Consider condensing explanations and focusing on key points.",
                "token_savings": int(estimation["estimated_tokens"] * 0.2),
                "priority": "medium",
                "action": "Review and condense verbose sections"
            })
        
        # Check for repetitive content
        lines = content.split('\n')
        repeated_lines = self._find_repeated_content(lines)
        if repeated_lines:
            suggestions.append({
                "type": "repetition",
                "title": "Remove repetitive content",
                "description": f"Found {len(repeated_lines)} potentially repetitive sections",
                "token_savings": len(repeated_lines) * 10,
                "priority": "high",
                "action": "Consolidate or remove repeated information"
            })
        
        # Check for excessive examples
        example_sections = re.findall(r'(?i)example|sample|demo', content)
        if len(example_sections) > 10:
            suggestions.append({
                "type": "examples",
                "title": "Reduce number of examples",
                "description": f"Found {len(example_sections)} example sections. Consider keeping only the most relevant ones.",
                "token_savings": int(len(example_sections) * 20),
                "priority": "medium",
                "action": "Keep 3-5 most relevant examples, remove others"
            })
        
        # Check for long code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        long_code_blocks = [block for block in code_blocks if len(block) > 500]
        if long_code_blocks:
            suggestions.append({
                "type": "code_blocks",
                "title": "Shorten code examples",
                "description": f"Found {len(long_code_blocks)} lengthy code blocks",
                "token_savings": int(len(long_code_blocks) * CODE_BLOCK_TOKEN_MULTIPLIER),
                "priority": "medium",
                "action": "Use shorter, focused code snippets or pseudocode"
            })
        
        # Check for unnecessary formatting
        if content.count('**') > 50 or content.count('*') > 100:
            suggestions.append({
                "type": "formatting",
                "title": "Simplify formatting",
                "description": "Excessive markdown formatting may use extra tokens",
                "token_savings": 20,
                "priority": "low",
                "action": "Use simpler formatting, focus on content over style"
            })
        
        return suggestions
    
    def _find_repeated_content(self, lines: List[str]) -> List[str]:
        """Find potentially repeated content."""
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if len(stripped) > 10:  # Only check substantial lines
                line_counts[stripped] = line_counts.get(stripped, 0) + 1
        
        return [line for line, count in line_counts.items() if count > 1]
    
    def _assess_implementation_difficulty(self, suggestions: List[Dict[str, Any]]) -> str:
        """Assess overall difficulty of implementing optimizations."""
        if not suggestions:
            return "none"
        
        high_priority = sum(1 for s in suggestions if s.get("priority") == "high")
        total_savings = sum(s.get("token_savings", 0) for s in suggestions)
        
        if high_priority > 2 or total_savings > 1000:
            return "moderate"
        elif total_savings > 200:
            return "easy"
        else:
            return "minimal"