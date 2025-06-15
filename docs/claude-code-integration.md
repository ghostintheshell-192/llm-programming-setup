# Claude Code Integration Guide

## Quick Setup

### 1. Install the MCP Server

```bash
cd /data/repos/meta-projects/llm-programming-setup
pip install -e .
```

### 2. Add to Claude Code Configuration

Add this to your Claude Code MCP configuration file:

```json
{
  "mcpServers": {
    "llm-programming-setup": {
      "command": "python3",
      "args": ["-m", "llm_programming_setup_mcp.server"],
      "cwd": "/data/repos/meta-projects/llm-programming-setup"
    }
  }
}
```

### 3. Test the Tools

In Claude Code, you can now use:

```
Use scan_project to analyze this directory
```

```
Use generate_context to create my LLM context file
```

```
Use show_copy_instructions
```

## Available MCP Tools

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `scan_project` | Detect project type and language | `Use scan_project with path="/path/to/project"` |
| `generate_context` | Create universal LLM_CONTEXT.md | `Use generate_context with project_name="my-app"` |
| `show_copy_instructions` | Get setup instructions for all LLMs | `Use show_copy_instructions` |
| `estimate_tokens` | Calculate token count and costs | `Use estimate_tokens with context_file="LLM_CONTEXT.md"` |
| `optimize_context` | Get optimization suggestions | `Use optimize_context with context_file="LLM_CONTEXT.md"` |

## Workflow Example

1. **Navigate to your project**:

   ```bash
   cd /path/to/your/project
   ```

2. **Scan the project**:

   ```
   Use scan_project
   ```

3. **Generate context**:

   ```
   Use generate_context
   ```

4. **Get copy instructions**:

   ```
   Use show_copy_instructions
   ```

5. **Optimize if needed**:

   ```
   Use optimize_context with context_file="LLM_CONTEXT.md"
   ```

## Troubleshooting

### Common Issues

1. **Python module not found**:
   - Make sure you ran `pip install -e .` in the project directory
   - Check that the path in `cwd` is correct

2. **Permission errors**:
   - Ensure the directory is readable
   - Check that Python 3 is available

3. **YAML parsing errors**:
   - The server will gracefully handle missing `rules/goto.yaml`
   - Check file permissions in the `rules/` directory

### Testing Installation

```bash
# Test the server directly
python3 -m llm_programming_setup_mcp.server --help

# Test Python imports
python3 -c "from llm_programming_setup_mcp.server import main; print('✅ Installation successful')"
```

## Advanced Configuration

### Custom Rules Path

You can modify the rules path by editing `src/llm_programming_setup_mcp/tools/project_scanner.py`:

```python
# Change this line to point to your custom rules
self.rules_path = Path("/custom/path/to/rules")
```

### Adding New Languages

1. Edit `rules/goto.yaml` to add detection patterns
2. Create new standards file in `rules/coding-standards/`
3. Restart Claude Code to reload the server