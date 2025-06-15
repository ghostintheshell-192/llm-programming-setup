# Claude Code - Global Repository Rules

## Development Methodology

### Core Principles
- **Functional minimalism**: Implement the minimum complexity necessary for current requirements
- **Incrementality**: Test each change before proceeding, implement one component at a time
- **Responsiveness as requirement**: A blocked interface makes the application non-functional
- **Effective simplicity**: Prefer the simplest solution that works
- **Reversibility**: Return to working versions when optimizations compromise functionality

### Critical Approach
- Critically evaluate and question questionable assumptions
- For ambiguous questions: identify the unclear part and ask for direct clarification
- Do not develop elaborate explanations for possible interpretations of the question

## Technology Compatibility
- Verify complete compatibility between proposed frameworks and libraries
- Explicitly list compatibility requirements before suggesting any library
- Confirm active support for third-party libraries with recent framework versions
- Compare alternatives highlighting compatibility advantages/disadvantages
- Report potential integration problems before implementation

## State and Lifecycle Management
- Clearly define the possible states of each component
- Document allowable state transitions
- Properly manage resource cleanup
- Implement appropriate state management patterns
- Avoid inconsistent states or race conditions

## Declarative Systems and UI Frameworks
- Consider not only WHAT happens but WHEN (timing of operations)
- The ORDER of evaluation is more important than static relationships
- Properties and bindings are evaluated at specific lifecycle phases
- Trace the complete temporal flow to diagnose dependency problems

## Security, Configuration and Scalability
- Define security models for device access and credential management
- Establish versioning, validation and configuration backup processes
- Scale for different needs by identifying potential bottlenecks
- Plan optimization strategies based on measurable requirements, not hypothetical ones

## Git Workflow and Branch Management

### Branch Strategy - MANDATORY
**NEVER work directly on main branch**

1. **Create feature branch for each task**:
   ```bash
   git checkout -b feature/task-description
   # Example: git checkout -b feature/streamlit-dashboard
   # Example: git checkout -b fix/button-lifecycle-bug
   # Example: git checkout -b refactor/settings-architecture
   ```

2. **Branch naming conventions**:
   - `feature/description` - New functionality
   - `fix/description` - Bug fixes
   - `refactor/description` - Code improvements
   - `docs/description` - Documentation updates
   - `chore/description` - Maintenance tasks

3. **Workflow process**:
   ```bash
   # Start new work
   git checkout main
   git pull origin main
   git checkout -b feature/my-new-feature
   
   # Work and commit
   git add .
   git commit -m "descriptive message"
   
   # Push feature branch
   git push -u origin feature/my-new-feature
   
   # Merge when ready
   git checkout main
   git merge feature/my-new-feature
   git push origin main
   
   # Cleanup
   git branch -d feature/my-new-feature
   git push origin --delete feature/my-new-feature
   ```

4. **When to create branches**:
   - ✅ **Always** when working on roadmap items
   - ✅ **Always** when implementing new features
   - ✅ **Always** when fixing bugs
   - ✅ **Always** when refactoring code
   - ❌ **Exception**: Only work on main for initial project setup

5. **Branch lifecycle**:
   - Create branch from latest main
   - Work on single focused task
   - Commit frequently with clear messages
   - Test thoroughly before merge
   - Clean up branch after merge

### Commit Message Standards
- Use descriptive commit messages
- Include context and reasoning
- Follow conventional commits format when possible
- Always include Claude Code attribution

## User Personal Information
current IDE: `[your IDE]`
current O.S: `[your Operating System]`

## Reference Repository
Consult the `rules/` folder for specific principles and additional templates.

### Coding Standards Workflow
**ALWAYS follow this exact process before coding:**

1. **Update projects list**: Run `cd rules && python3 update_projects.py` to refresh project mappings
2. **Read user preferences**: Load `rules/user-preferences.yaml` for behavior configuration
3. **Read `rules/goto.yaml`**
4. **If user specifies a project by name**, check `rules/projects.yaml` for project type and path, then skip to step 7
5. **If working in current directory**, look at the files present (use LS tool)
6. **Match file patterns** from goto.yaml against what you see in the directory
7. **Check mandatory files**: Verify if required files exist based on detected language
8. **Handle missing files**: Based on user-preferences.yaml mode (auto/ask/manual)
9. **Read the files listed in `standards:`** for the identified language
10. **If multiple languages match**, use the priority_order from goto.yaml
11. **If no match**, read only general-principles.md and ask user for clarification

**Example:** If you see `pubspec.yaml` → read `general-principles.md` + `flutter-dart.md`
**Example:** If user says "work on `[app name]`" → update projects.yaml → find type `flutter` → read `general-principles.md` + `flutter-dart.md`

### Standards Structure
- `rules/update_projects.py` - **Script** - Regenerates projects.yaml by scanning /data/repos/
- `rules/user-preferences.yaml` - **User Configuration** - Customizes Claude behavior and workflow
- `rules/goto.yaml` - **START HERE** - Routing file to determine which standards to read
- `rules/projects.yaml` - **Auto-generated** - Project mappings with paths and types
- `rules/coding-standards/general-principles.md` - Universal coding principles (always read)
- `rules/coding-standards/[language].md` - Language-specific standards (as indicated by goto.yaml)
- `rules/repository-standards.md` - Repository organization and structure
- `rules/naming-mappings.yaml` - Automatic name conversion rules
