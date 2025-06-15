# LLM Context - llm-programming-setup

*Generated on 2025-06-15 17:41:15 by llm-programming-setup-mcp*

## Project Detection Results

**Detected Language:** python (confidence: 60.0%)
**Project Type:** Python application or library project

**Total Files Scanned:** 9

### Required Files Status

- ✅ .gitignore
- ✅ LICENSE
- ✅ README.md
- ✅ CLAUDE.md

---

## Applicable Coding Standards

### coding-standards/general-principles.md

# General Coding Principles

## 1. Universal Rules

### Fail Fast vs. Silent Failure
- **Before implementing fallback/recovery**: Ask if the failure indicates a problem that should be solved at the root
- **Avoid masking errors**: A fallback that "makes everything work" often hides real bugs  
- **Prefer controlled crashes**: It's better to fail clearly than continue in an inconsistent state
- **Distinguish fallback from default case**:
  - ❌ **Fallback** = "If this doesn't work, do this instead" (hides problems)
  - ✅ **Default case** = "In this expected situation, behave this way" (handles legitimate scenario)
- **Practical rule**: If you're asking "what do I do if this fails?", you're probably creating a problematic fallback. If you're asking "what's the normal behavior in this case?", it's probably a legitimate default case.

### Code Quality Fundamentals
- **Self-documenting code**: Write clear, expressive code instead of relying on comments
- **English only**: All code, comments, and documentation must be in English
- **Consistency**: Follow established patterns within the codebase
- **Simplicity**: Prefer the simplest solution that works
- **Single responsibility**: Each function/class should have one clear purpose
- **Meaningful names**: Use descriptive names that explain intent

### Comments Policy
- Add comments only when complex logic needs explanation
- **All comments must be in English**
- Prefer descriptive names over explanatory comments
- Document WHY, not WHAT
- Remove commented-out code before committing

## 2. Error Handling Examples

### ❌ Bad: Silent Failure (Fallback)
```javascript
function processUserData(userData) {
  try {
    return validateAndTransform(userData);
  } catch (error) {
    return {}; // Hides the real problem!
  }
}
```

### ✅ Good: Fail Fast
```javascript
function processUserData(userData) {
  if (!userData || typeof userData !== 'object') {
    throw new Error('User data must be a valid object');
  }
  
  if (!userData.email) {
    throw new Error('User email is required');
  }
  
  return validateAndTransform(userData);
}
```

### ✅ Good: Legitimate Default Case
```javascript
function getUserDisplayName(user) {
  if (user.displayName) return user.displayName;
  if (user.firstName && user.lastName) return `${user.firstName} ${user.lastName}`;
  return user.email; // Legitimate default - all users have email
}
```

## 3. Common Anti-Patterns to Avoid

### Code Structure
- **Magic numbers**: Use named constants instead of hardcoded values
- **Deep nesting**: Extract methods to reduce complexity (max 3-4 levels)
- **Long parameter lists**: Use objects/structs for grouped parameters (max 3-4 parameters)
- **God classes**: Split responsibilities into focused classes
- **Copy-paste code**: Extract common functionality into reusable methods
- **Premature optimization**: Profile before optimizing

### Naming Issues
- **Abbreviations**: Use full, descriptive names (`userManager` not `usrMgr`)
- **Misleading names**: Names should accurately reflect what the code does
- **Inconsistent conventions**: Follow the established patterns in the codebase
- **Generic names**: Avoid `data`, `info`, `manager` without context

## 4. Function Design Principles

### Size and Complexity
- **Maximum 25 lines** per function (guideline, not hard rule)
- **Single responsibility**: One function should do one thing well
- **Clear inputs/outputs**: Parameters and return values should be obvious
- **No side effects**: Unless clearly documented and necessary

### Parameters
- **Maximum 3-4 parameters** - more suggests the function is doing too much
- **Use descriptive parameter names**: `calculateTax(income, rate, deductions)` not `calc(a, b, c)`
- **Validate inputs**: Check parameters at the beginning of the function
- **Use default values** when appropriate

## 5. Code Review Checklist

### Before Submitting
- [ ] Code follows language-specific naming conventions
- [ ] No magic numbers or hardcoded values
- [ ] Error handling is explicit and meaningful
- [ ] Functions have single responsibility
- [ ] Code is self-documenting with clear names
- [ ] No commented-out code
- [ ] Tests cover new functionality
- [ ] Documentation updated if needed
- [ ] No silent failures or inappropriate fallbacks

### Security Considerations
- [ ] No hardcoded secrets or credentials
- [ ] Input validation for user-provided data
- [ ] Proper error messages (don't expose internal details)
- [ ] Resource cleanup (files, connections, memory)

### Performance Considerations
- [ ] No obvious performance bottlenecks
- [ ] Efficient algorithms for the use case
- [ ] Proper resource usage
- [ ] Consider caching for expensive operations

## 6. Testing Guidelines

### Test Structure
- **Arrange, Act, Assert**: Clear test organization
- **Descriptive test names**: Should explain what is being tested
- **Test one thing**: Each test should verify one specific behavior
- **Independent tests**: Tests should not depend on each other

### Test Coverage
- **Happy path**: Normal, expected behavior
- **Edge cases**: Boundary conditions and special cases
- **Error cases**: How the code handles invalid input
- **Integration points**: How components work together

## 7. Documentation Standards

### Code Documentation
- **README files**: Clear setup and usage instructions
- **API documentation**: For public interfaces
- **Architecture docs**: For complex systems
- **Inline docs**: For complex algorithms or business logic

### Documentation Quality
- **Keep it current**: Update docs when code changes
- **Be concise**: Clear and to the point
- **Include examples**: Show how to use the code
- **Explain decisions**: Document architectural choices and trade-offs

## 8. Refactoring Checklist

After completing a first implementation, systematically evaluate:

### 1. Code Duplication
- ✅ Are there nearly identical code blocks? Can they be extracted into methods?
- ✅ Do you have loops with similar structure but different values? Can they be parameterized?
- ✅ Are there repeated conditional expressions? Can they be extracted into predicate functions?

### 2. Responsibility Evaluation
- ✅ Does each method do too many different things? (>25 lines is suspicious)
- ✅ Are there comments that separate "logical sections" within methods?
- ✅ Do methods have more than 3-4 parameters? (Suggests too many responsibilities)

### 3. Domain Modeling
- ✅ Does the code correctly reflect real relationships between entities?
- ✅ Do class/method names reflect the domain language?
- ✅ Are there properties or methods "out of place" relative to the main responsibility?

### 4. Pattern Opportunities
- ✅ Object creation: Are Factory, Builder patterns needed?
- ✅ Conditional behaviors: Are Strategy, Command patterns appropriate?
- ✅ State management: Is State pattern or event-based approaches needed?

### 5. Abstraction and Interfaces
- ✅ Are there dependencies on concrete implementations instead of interfaces?
- ✅ Do classes contain methods operating at different abstraction levels?
- ✅ Can the code be improved with composition instead of inheritance?

### 6. Progressive Generalization
- ✅ Can generics/templates make the code more reusable?
- ✅ Are there specialized data structures that could be parameterized?
- ✅ Do similar functionalities exist in different types? Candidates for base class extraction.

### 7. Final Checks
- ✅ Does the new generalized code maintain or improve readability?
- ✅ Do the introduced abstractions have clear value or are they premature?
- ✅ Is the complexity/flexibility balance appropriate for current requirements?
- ✅ Does the modification introduce circular dependencies or unwanted coupling?

---

**Remember**: These principles apply across all programming languages. See language-specific files for detailed conventions and examples.

---

### coding-standards/python.md

# Python Coding Standards

## 1. Naming Conventions

### Files and Modules
- **Files/Modules**: `snake_case.py` (`data_processor.py`, `user_manager.py`)
- **Packages**: `snake_case` (`data_processing/`, `user_management/`)
- **Test files**: `test_*.py` or `*_test.py` (`test_user_manager.py`)

### Code Elements
- **Classes**: `PascalCase` (`DataProcessor`, `UserManager`, `DatabaseConnection`)
- **Functions/Variables**: `snake_case` (`process_data()`, `user_count`, `is_valid`)
- **Constants**: `UPPER_SNAKE_CASE` (`MAX_RETRIES`, `DEFAULT_TIMEOUT`, `API_BASE_URL`)
- **Private members**: `_leading_underscore` (`_internal_method`, `_private_var`)
- **Very private**: `__double_underscore` (name mangling, rarely used)

## 2. Import Organization

### Import Order (PEP 8)
1. Standard library imports (os, sys, json, pathlib, logging)
2. Related third-party imports (requests, pandas, numpy, flask)
3. Local application/library imports (relative to project)

### Import Guidelines
- Group imports with blank lines between groups
- Order alphabetically within each group
- Use absolute imports for packages, relative for local modules
- Avoid `import *` except in `__init__.py` when appropriate

### Correct Example:
```python
# Standard library
import logging
import os
import sys

# Third-party
import requests
from flask import Flask, jsonify
from pydantic import BaseModel

# Local imports
from .config import settings
from .utils import helper_function
```

### Incorrect Example:
```python
from flask import Flask, jsonify
from pydantic import BaseModel
import requests
import logging  # ❌ Mixed standard library with third-party
```

## 3. Function and Class Design

### Function Design Principles
- Use type hints consistently for parameters and return values
- Implement proper parameter validation at function entry
- Apply default parameter values appropriately
- Use descriptive docstrings following Google or NumPy style
- Keep functions focused on single responsibility

### Class Structure Organization
- Define `__init__` method with proper parameter validation
- Use `@property` decorators for computed attributes
- Implement `__str__` and `__repr__` methods for debugging
- Apply proper method organization (public before private)
- Use dataclasses for simple data containers

### Type Hinting Best Practices
- Use Union for multiple possible types
- Apply Optional for nullable values
- Use generics for reusable type definitions
- Import type hints from typing module consistently
- Use TypeVar for generic function definitions

## 4. Error Handling and Exceptions

### Exception Hierarchy Design
- Create custom exception classes inheriting from appropriate base classes
- Use specific exception types rather than generic Exception
- Implement proper exception chaining with `raise from`
- Apply descriptive error messages with context
- Use exceptions for exceptional conditions, not control flow

### Error Handling Patterns
- Use try-catch blocks with specific exception types
- Implement proper resource cleanup with context managers
- Apply proper logging at appropriate levels
- Handle exceptions at the right abstraction level
- Use finally blocks for guaranteed cleanup operations

## 5. Data Structures and Collections

### Collection Usage Guidelines
- Use list comprehensions for simple transformations
- Apply generator expressions for memory-efficient processing
- Use dict comprehensions for dictionary creation
- Prefer collections.defaultdict for default value scenarios
- Use sets for membership testing and deduplication

### Data Class and Named Tuple Usage
- Use dataclasses for mutable data containers
- Apply NamedTuple for immutable data structures
- Implement proper validation in `__post_init__` methods
- Use frozen dataclasses for immutable objects
- Apply proper field defaults and factory functions

## 6. Async Programming and Concurrency

### Async/Await Patterns
- Use async/await consistently for I/O-bound operations
- Apply proper exception handling in async functions
- Use asyncio.gather() for concurrent operations
- Implement proper cancellation handling
- Apply proper timeout handling for network operations

### Threading and Multiprocessing
- Use threading for I/O-bound tasks
- Apply multiprocessing for CPU-bound tasks
- Use proper synchronization primitives (locks, queues)
- Implement proper resource sharing strategies
- Apply proper cleanup for background threads

## 7. Testing Strategies

### Unit Testing Structure
- Use unittest or pytest frameworks consistently
- Apply proper test isolation and independence
- Use descriptive test method names
- Implement proper setup and teardown methods
- Mock external dependencies appropriately

### Test Organization Patterns
- Group related tests in test classes
- Use parametrized tests for data-driven testing
- Apply proper test fixtures for complex setup
- Use property-based testing for complex algorithms
- Implement proper integration test strategies

## 8. Performance and Optimization

### Performance Best Practices
- Profile code before optimizing
- Use appropriate data structures for the use case
- Apply caching strategies for expensive operations
- Use generators for memory-efficient processing
- Implement proper database query optimization

### Memory Management
- Use weak references for large cached objects
- Apply proper cleanup for file handles and network connections
- Use context managers for resource management
- Monitor memory usage in production environments
- Implement proper garbage collection strategies

## 9. Package and Dependency Management

### Virtual Environment Management
- **Always use virtual environments** for project isolation
- Create with: `python -m venv venv` (name the directory `venv`)
- Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
- Deactivate: `deactivate`
- **Never commit `venv/` directory** - add to `.gitignore`
- Include activation instructions in README.md for new developers
- Use `pip freeze > requirements.txt` to capture exact versions

### Package Structure
- Use proper `__init__.py` files for package organization
- Implement consistent package versioning
- Apply proper dependency specification
- Use virtual environments for project isolation
- Implement proper build and distribution strategies

### Dependency Management
- Use requirements.txt or pyproject.toml for dependencies
- Pin dependency versions for reproducible builds (`pandas>=1.5.0,<2.0.0`)
- Apply proper dependency updates and security scanning
- Use lock files for exact dependency specification
- Implement proper dependency injection patterns
- Separate dev dependencies: `requirements-dev.txt` or use pyproject.toml sections

## 10. Documentation and Code Quality

### Documentation Standards
- Use docstrings for all public modules, classes, and functions
- Apply consistent docstring format (Google, NumPy, or Sphinx)
- Include type information in docstrings when helpful
- Provide usage examples for complex functions
- Document return values and raised exceptions

### Code Quality Tools
- Use black for automatic code formatting
- Apply flake8 or pylint for linting
- Use mypy for static type checking
- Implement pre-commit hooks for code quality
- Apply proper configuration for all tools

## 11. Security Best Practices

### Input Validation and Sanitization
- Validate all user input at application boundaries
- Use parameterized queries for database operations
- Apply proper sanitization for user-generated content
- Implement rate limiting for API endpoints
- Use proper authentication and authorization mechanisms

### Secure Coding Practices
- Never hardcode secrets or credentials
- Use environment variables for configuration
- Apply proper encryption for sensitive data
- Implement proper session management
- Use secure communication protocols (HTTPS, TLS)

## 12. Common Anti-Patterns to Avoid

### Import Anti-Patterns
- Using wildcard imports (`from module import *`)
- Circular import dependencies
- Importing modules inside functions unnecessarily
- Using relative imports incorrectly
- Not following PEP 8 import order

### Exception Handling Anti-Patterns
- Using bare `except:` clauses that catch all exceptions
- Catching exceptions without handling them appropriately
- Using exceptions for normal control flow
- Not providing sufficient error context
- Swallowing exceptions silently

### Performance Anti-Patterns
- Using string concatenation in loops instead of join()
- Not using list comprehensions when appropriate
- Creating unnecessary intermediate lists
- Not using appropriate data structures for the use case
- Premature optimization without profiling

### Code Organization Anti-Patterns
- Creating monolithic modules with too many responsibilities
- Not using proper separation of concerns
- Mixing business logic with presentation logic
- Not following consistent naming conventions
- Creating deep inheritance hierarchies unnecessarily

---

**Note**: Follow PEP 8 style guide and the general principles defined in `general-principles.md` along with these Python-specific guidelines. Use automated tools like black, flake8, and mypy for code quality enforcement.

---

## How to Use This Context

This file contains universal coding standards and project context that work with any LLM.
Copy the content as follows:

### Claude (Anthropic)
1. Rename this file to `CLAUDE.md`
2. Place in your project root directory
3. Claude will automatically read it

### ChatGPT (OpenAI)
1. Create a new Project in ChatGPT
2. Copy this content to Project's Custom Instructions
3. Or upload as a file to the Project's Knowledge base

### Gemini (Google)
1. For Firebase Studio: Copy to `.idx/airules.md`
2. For GitHub: Copy to `.gemini/styleguide.md`
3. For general use: Reference as needed

### Other LLMs
- Use as system prompt or context document
- Reference key sections as needed
- Adapt file name to your LLM's conventions

---

*Context optimized for token efficiency • LLM-agnostic design • Generated by llm-programming-setup-mcp*