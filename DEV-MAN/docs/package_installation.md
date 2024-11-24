# Package Installation Guide

## Understanding `pip install -e .`

### What `-e` (Editable) Mode Does
- Installs the package in "editable" or "development" mode
- Creates a special link to your source code
- Changes to code are immediately reflected without reinstalling
- The `.` means "current directory"

### Directory Matters
```bash
# This works - installs from pyproject.toml
/WORKSTATION$ uv pip install -e .

# This doesn't work - wrong directory
/WORKSTATION/timeline$ uv pip install -e .
```

### Why Directory Matters
1. **pyproject.toml Location**
   - Must run from directory containing pyproject.toml
   - This file defines what to install
   - Contains all package configurations

2. **Package Discovery**
   ```toml
   [tool.setuptools]
   packages = ["crews", "timeline"]  # Looks for these from root
   ```

## Starting the Application

### 1. Install Package
```bash
# Go to project root
cd /path/to/WORKSTATION

# Install in editable mode
uv pip install -e .
```

### 2. Initialize Database
```bash
# Creates SQLite database
python -m timeline.init_db
```

### 3. Start File Watcher
```bash
# Watches for file changes
timeline watch
```

### 4. Start Dev Docs Server
```bash
# Starts documentation server
dev-docs
```

### 5. View Timeline
```bash
# Open in browser
http://localhost:8010/dev/timeline
```

## What Each Command Does

### `uv pip install -e .`
- Installs all dependencies from pyproject.toml
- Makes packages available system-wide
- Enables command-line tools (timeline, dev-docs)

### `python -m timeline.init_db`
- Creates SQLite database
- Sets up tables for events
- Prepares for tracking changes

### `timeline watch`
- Starts file change monitoring
- Records changes to database
- Tracks cursor interactions

### `dev-docs`
- Starts documentation server
- Shows diagrams and docs
- Displays timeline feed

## Common Issues

### Wrong Directory
```bash
Error: No pyproject.toml found
Solution: cd to WORKSTATION root
```

### Missing Dependencies
```bash
Error: No module named 'crewai'
Solution: uv pip install -e .
```

### Database Issues
```bash
Error: No such table: timeline_events
Solution: python -m timeline.init_db
```

## Best Practices

1. **Always Install from Root**
   - Contains pyproject.toml
   - Has complete package structure
   - Proper dependency resolution

2. **Use Virtual Environments**
   ```bash
   # Create new environment
   uv venv .venv
   source .venv/bin/activate
   ```

3. **Check Installation**
   ```bash
   # Should show timeline package
   pip list | grep timeline
   ```

## Package Structure
```
WORKSTATION/
├── pyproject.toml     # Package definition
├── crews/            # Crews package
├── timeline/         # Timeline package
└── DEV-MAN/         # Documentation
``` 