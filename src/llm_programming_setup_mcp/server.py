#!/usr/bin/env python3
"""
LLM Programming Setup MCP Server

A Model Context Protocol server for LLM-agnostic programming setup and context optimization.
Provides tools for project scanning, context generation, and token optimization.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    ListToolsResult,
    TextContent,
    Tool,
)
from pydantic import BaseModel

from .tools.project_scanner import ProjectScanner
from .tools.context_generator import ContextGenerator
from .tools.template_processor import TemplateProcessor
from .tools.token_optimizer import TokenOptimizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize server
server = Server("llm-programming-setup-mcp")

# Initialize tools
project_scanner = ProjectScanner()
context_generator = ContextGenerator()
template_processor = TemplateProcessor()
token_optimizer = TokenOptimizer()


class ProjectInfo(BaseModel):
    """Project information model."""
    path: str
    detected_language: Optional[str] = None
    confidence: float = 0.0
    files_found: List[str] = []
    standards_files: List[str] = []


@server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools."""
    return ListToolsResult(
        tools=[
            Tool(
                name="scan_project",
                description="Scan project directory to detect language and applicable standards",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to project directory (default: current directory)"
                        }
                    },
                    "additionalProperties": False
                }
            ),
            Tool(
                name="generate_context",
                description="Generate universal LLM context file based on project scan",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to project directory (default: current directory)"
                        },
                        "project_name": {
                            "type": "string",
                            "description": "Override project name (default: directory name)"
                        }
                    },
                    "additionalProperties": False
                }
            ),
            Tool(
                name="show_copy_instructions",
                description="Show instructions for using generated context with different LLMs",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            ),
            Tool(
                name="estimate_tokens",
                description="Estimate token count for generated context",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "context_file": {
                            "type": "string",
                            "description": "Path to context file to analyze"
                        }
                    },
                    "required": ["context_file"],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="optimize_context",
                description="Analyze context and suggest optimizations to reduce token usage",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "context_file": {
                            "type": "string",
                            "description": "Path to context file to optimize"
                        }
                    },
                    "required": ["context_file"],
                    "additionalProperties": False
                }
            )
        ]
    )


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "scan_project":
            path = arguments.get("path", ".")
            result = project_scanner.scan(path)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )
                ]
            )
            
        elif name == "generate_context":
            path = arguments.get("path", ".")
            project_name = arguments.get("project_name")
            
            # First scan the project
            scan_result = project_scanner.scan(path)
            
            # Generate context
            context = context_generator.generate(
                scan_result, 
                project_name=project_name
            )
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=context
                    )
                ]
            )
            
        elif name == "show_copy_instructions":
            instructions = template_processor.get_copy_instructions()
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=instructions
                    )
                ]
            )
            
        elif name == "estimate_tokens":
            context_file = arguments.get("context_file", "LLM_CONTEXT.md")
            estimation = token_optimizer.estimate_tokens(context_file)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(estimation, indent=2)
                    )
                ]
            )
            
        elif name == "optimize_context":
            context_file = arguments.get("context_file", "LLM_CONTEXT.md")
            optimizations = token_optimizer.suggest_optimizations(context_file)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(optimizations, indent=2)
                    )
                ]
            )
            
        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )
                ],
                isError=True
            )
            
    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ],
            isError=True
        )


async def main() -> None:
    """Main entry point for the MCP server."""
    logger.info("Starting LLM Programming Setup MCP Server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


# if __name__ == "__main__":
#     asyncio.run(main())