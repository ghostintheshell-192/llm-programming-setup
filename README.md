# LLM Programming Setup

A comprehensive configuration system for Large Language Models (LLMs) to provide consistent, language-specific programming assistance across different project types.

## Overview

This setup provides LLMs with structured guidelines, coding standards, and project detection capabilities to deliver consistent programming assistance. It automatically detects project types and applies appropriate coding standards based on file patterns.

## Features

- **Automatic Project Detection**: Identifies project type based on file patterns (Flutter, Python, C#, JavaScript/TypeScript, C/C++)
- **Language-Specific Standards**: Comprehensive coding guidelines for each supported language
- **Flexible Configuration**: User preferences for project initialization and workflow behavior
- **IDE Integration**: VSCode-specific configurations and recommendations
- **Repository Standards**: Consistent project structure and naming conventions

## Quick Start

1. **Copy the setup to your project root**:
   ```bash
   cp -r llm-programming-setup/* /your/project/root/
   ```

2. **Customize paths in CLAUDE.md**:
   - Replace `[your IDE]` with your preferred IDE
   - Replace `[your Operating System]` with your OS
   - Replace `[/your/directory]` with your actual project path

3. **Configure user preferences**:
   ```bash
   edit rules/user-preferences.yaml
   ```

4. **Initialize project mappings**:
   ```bash
   cd rules
   python3 update_projects.py
   ```

## Project Structure

```
llm-programming-setup/
├── CLAUDE.md                          # Main LLM configuration file
├── LICENSE                            # MIT License
├── README.md                          # This file
├── rules/                             # Configuration rules directory
│   ├── coding-standards/              # Language-specific coding standards
│   │   ├── general-principles.md      # Universal coding principles
│   │   ├── python.md                  # Python-specific guidelines
│   │   ├── flutter-dart.md            # Flutter/Dart guidelines
│   │   ├── javascript-typescript.md   # JS/TS guidelines
│   │   ├── csharp-dotnet.md          # C#/.NET guidelines
│   │   └── c-cpp.md                   # C/C++ guidelines
│   ├── ide-standards/                 # IDE-specific configurations
│   │   └── vs-code.md                 # VSCode settings
│   ├── goto.yaml                      # Project type detection rules
│   ├── user-preferences.yaml          # User behavior configuration
│   ├── repository-standards.md        # Repository organization
│   ├── naming-mappings.yaml          # Naming conventions
│   └── update_projects.py            # Project mapping script
└── example-project/                   # Example implementation (intentionally incomplete)
```

## Configuration Files

### Core Configuration

- **`CLAUDE.md`**: Main configuration file with development methodology and workflow instructions
- **`rules/goto.yaml`**: Defines file patterns for automatic project type detection
- **`rules/user-preferences.yaml`**: Customizes LLM behavior and workflow preferences

### Language Standards

Each language has dedicated standards in `rules/coding-standards/`:
- **General Principles**: Universal coding practices
- **Language-Specific**: Frameworks, patterns, and best practices per language

### Project Detection

The system automatically detects project types based on file patterns:
- **Flutter**: `pubspec.yaml`, `*.dart`
- **Python**: `requirements.txt`, `pyproject.toml`, `*.py`
- **C#/.NET**: `*.csproj`, `*.sln`, `*.cs`
- **JavaScript/TypeScript**: `package.json`, `*.js`, `*.ts`
- **C/C++**: `CMakeLists.txt`, `Makefile`, `*.cpp`

## Usage

### Basic Usage

1. Place the configuration files in your project
2. The LLM will automatically detect project type and apply appropriate standards
3. All coding assistance will follow the configured guidelines

### Advanced Configuration

1. **Customize project detection**:
   ```yaml
   # Edit rules/goto.yaml
   language_detection:
     python:
       files: ["requirements.txt", "*.py"]
       standards: ["coding-standards/general-principles.md", "coding-standards/python.md"]
   ```

2. **Modify user preferences**:
   ```yaml
   # Edit rules/user-preferences.yaml
   project_initialization:
     mode: "ask"  # Options: auto, ask, manual
   ```

3. **Update project mappings**:
   ```bash
   cd rules
   python3 update_projects.py
   ```

## Customization

### Adding New Languages

1. Create new standard file: `rules/coding-standards/new-language.md`
2. Add detection pattern to `rules/goto.yaml`
3. Update `update_projects.py` detection logic

### Modifying Behavior

- **Project initialization**: Edit `user-preferences.yaml`
- **File detection**: Modify patterns in `goto.yaml`
- **Coding standards**: Update language-specific `.md` files

## Git Workflow

The setup enforces a feature-branch workflow:
- Always create feature branches for new work
- Use descriptive branch names (`feature/`, `fix/`, `refactor/`)
- Clean up branches after merging

## Testing the Setup - Example Project

The `example-project/` directory contains an **intentionally incomplete** Python Flask application that demonstrates the workflow:

### What's Included
- ✅ `main.py` - Basic Flask app with proper import order
- ✅ `requirements.txt` - Dependencies for project detection
- ✅ `config.py` - Configuration module
- ✅ `tests/test_main.py` - Unit tests
- ✅ `.gitignore` - Git ignore rules

### What's Missing (On Purpose)
- ❌ `LICENSE` - Missing mandatory file
- ❌ `README.md` - Missing mandatory file  
- ❌ `CLAUDE.md` - Missing mandatory file

### How to Test the Workflow

1. **Navigate to example-project**:
   ```bash
   cd example-project
   ```

2. **Follow the LLM workflow** starting from the main `CLAUDE.md`
3. **The LLM should detect** missing mandatory files and offer to create them
4. **This demonstrates** the automatic project analysis and correction capabilities

This approach lets you verify that the setup correctly identifies project issues and guides proper resolution.

## Requirements

- Python 3.6+ (for project mapping script)
- PyYAML library (`pip install pyyaml`)

## License

MIT License - Feel free to adapt and modify for your needs.

## Contributing

This is a template system designed for customization. Adapt the standards and configuration to match your specific development workflow and requirements.