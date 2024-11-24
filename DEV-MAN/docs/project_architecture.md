# Project Architecture

## Diagrams

### Package Dependencies
![Package Dependencies](../diagrams/svg/package_dependencies.svg)

### Project Structure
![Project Structure](../diagrams/svg/project_structure.svg)

### Dependency Flow
![Dependency Flow](../diagrams/svg/dependency_flow.svg)

[View Interactive Diagrams](../diagrams/viewer.html)

## Package Management

### 1. UV vs Pip
- UV is a faster package installer
- Handles dependency resolution better
- Creates isolated environments
- Example:
```bash
# Create new environment
uv venv .venv

# Install packages
uv pip install -e .
```

### 2. Project Configuration Files

#### pyproject.toml
```toml
[build-system]
requires = ["setuptools>=61.0"]

[project]
name = "my-project"
dependencies = [
    "package1",
    "package2"
]

[tool.setuptools.packages.find]
include = ["crews*", "timeline*"]
```

#### Key Concepts:
1. **Build System**: How the project is built
2. **Project Metadata**: Name, version, dependencies
3. **Package Discovery**: What Python packages to include

### 3. Directory Structure Impact

#### Local Package Import
```python
# Within timeline/analyzer_crew.py
from crews.base_crew import BaseCrew  # Works when installed with -e .
```

#### External Package Import
```python
# In another project
from workstation.crews import BaseCrew  # After publishing
```

## Common Scenarios

### 1. Adding New Package
```bash
# Add to pyproject.toml
uv pip install new-package
```

### 2. Creating New Module
```
my_project/
├── new_module/
│   ├── __init__.py
│   └── core.py
└── pyproject.toml  # Add to packages.find
```

### 3. Using in Another Project
```bash
# Option 1: Install locally
uv pip install -e /path/to/workstation

# Option 2: Install from git
uv pip install git+https://github.com/user/workstation.git
```

## Current Error Analysis

The error we're seeing:
```
invalid table header
dotted key `tool.setuptools.packages` attempted to extend non-table type (array)
```

Fix:
```toml
# Correct way in pyproject.toml
[tool.setuptools]
packages = ["crews", "timeline"]

# Instead of
[tool.setuptools.packages.find]
include = ["timeline*"]
```

## Best Practices

### 1. Environment Management
```bash
# Create project-specific environment
uv venv .venv-projectname

# Activate
source .venv-projectname/bin/activate
```

### 2. Dependency Declaration
```toml
[project]
dependencies = [
    "required-package>=1.0.0"
]

[project.optional-dependencies]
dev = ["pytest", "black"]
```

### 3. Package Structure
```
package/
├── __init__.py      # Makes it a package
├── core.py          # Core functionality
└── utils/           # Subpackages
    └── __init__.py
```

## Common Issues and Solutions

1. **Module Not Found**
   - Check PYTHONPATH
   - Verify package is installed with -e
   - Check __init__.py exists

2. **Dependency Conflicts**
   - Use UV for better resolution
   - Specify version ranges
   - Create separate environments

3. **Import Issues**
   - Use absolute imports
   - Add __init__.py files
   - Install package in editable mode

## Project-Specific Notes

For our timeline project:
1. It depends on crews package
2. Both need to be discoverable
3. Need proper package hierarchy

Fix steps:
1. Update pyproject.toml
2. Install dependencies
3. Use proper imports

Would you like me to:
1. Create a script to fix the setup?
2. Add more detailed documentation?
3. Create a dependency map? 