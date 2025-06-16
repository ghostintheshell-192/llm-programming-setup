# Demo Workspace Tutorial

This guide explains how to use the `demo/` directory as a realistic test environment for the LLM Programming Setup MCP server.

## Purpose

**`demo/` = User's Development Environment**

- Contains real projects that need initialization
- MCP server analyzes and enhances these projects
- Demonstrates the complete workflow from detection to completion

## Contents

### `sample-project/`

**An intentionally incomplete Python Flask application** ready for MCP initialization:

- **Present**: `main.py`, `requirements.txt`, `config.py`, tests
- **Missing**: `LICENSE`, `README.md`, `CLAUDE.md` (by design)
- **Purpose**: Perfect test case for the MCP server's capabilities

### `sample-output.md` 

**Example of generated LLM context** from running MCP tools on sample-project:
- Shows what `generate_context` produces
- Universal format compatible with all LLMs
- Contains project detection results and coding standards
- Demonstrates token-optimized output (~3,773 tokens)

## Complete Workflow Demo

### Step 1: Analyze the Incomplete Project

```bash
cd demo/sample-project/
```

```
Use scan_project to detect project type
```
**Expected Result**: Python project detected, missing files identified

### Step 2: Generate Universal Context

```
Use generate_context to create LLM_CONTEXT.md
```
**Expected Result**: Universal context file created with standards

### Step 3: Get Integration Instructions

```
Use show_copy_instructions
```
**Expected Result**: Instructions for using with Claude, ChatGPT, Gemini, etc.

### Step 4: Optimize and Estimate Costs

```
Use estimate_tokens with context_file="LLM_CONTEXT.md"
Use optimize_context with context_file="LLM_CONTEXT.md"
```
**Expected Result**: Token count, cost estimates, optimization suggestions

## Real-World Simulation

This demo environment simulates what happens when a developer:

1. **Has an existing project** (sample-project) with missing standards
2. **Runs the MCP server** to analyze and enhance it
3. **Gets universal context** that works with any LLM
4. **Follows optimization suggestions** to reduce token costs
5. **Integrates with their preferred LLM** platform

## Sample Metrics

From the included `sample-output.md`:

- **Project Type**: Python Flask application
- **Detection Confidence**: 60% (based on file patterns)
- **Token Count**: 3,773 tokens
- **Cost Range**: $0.001 (Claude Haiku) to $0.038 (GPT-4)
- **Optimization Potential**: 22% token reduction possible

## Learning Outcomes

After running this demo, you'll understand:

- How the MCP server detects project types
- What universal LLM context looks like
- How to optimize for token efficiency
- How to integrate with different LLM platforms
- The cost implications of different context sizes

## MCP Server Actions in Demo

When you run the MCP server on `demo/sample-project/`, it should:

1. **Detect Python project** from `requirements.txt` and `.py` files
2. **Identify missing files**: LICENSE, README.md, CLAUDE.md
3. **Apply Python standards** from `rules/coding-standards/`
4. **Generate universal context** with project-specific standards
5. **Provide optimization suggestions** for token efficiency

---

**This demo proves that the MCP server transforms incomplete projects into well-documented, LLM-optimized development environments.**