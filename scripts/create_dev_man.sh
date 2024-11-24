#!/bin/bash

# Create DEV-MAN directory structure
mkdir -p DEV-MAN/{docs,diagrams,progress}

# Create symlink for README.md
ln -s ../README.md DEV-MAN/docs/README.md

# Create progress tracking files
cat > DEV-MAN/progress/whats-working.md << 'EOF'
# What's Working

## Core Functionality ✅
- Basic project structure set up
- FastAPI application initialized
- SQLAlchemy models defined
- Basic test structure in place

## In Progress 🚧
- CSV import functionality
- Markdown file parsing
- Database integration
- Test coverage improvement

## Not Started Yet ❌
- AG Grid integration
- Frontend styling
- Error handling improvements
- Documentation completion

## Latest Test Results
```
Last run: [DATE]
Passing: 4
Failing: 3
Errors: 3
Coverage: 74%
```

## Recent Updates
- Added initial test suite
- Set up database models
- Created basic API endpoints
EOF

cat > DEV-MAN/progress/TODO.md << 'EOF'
# TODO List

## High Priority
- [ ] Fix failing tests
  - [ ] Database fixture issues
  - [ ] Markdown parser number handling
  - [ ] Model validation for dates
- [ ] Improve test coverage (currently 74%)
- [ ] Complete CSV import functionality

## Medium Priority
- [ ] Enhance frontend UI
- [ ] Add error handling for API endpoints
- [ ] Implement proper logging
- [ ] Add data validation

## Low Priority
- [ ] Add dark mode support
- [ ] Implement export functionality
- [ ] Add user preferences
- [ ] Create detailed documentation

## Completed ✅
- [x] Set up basic project structure
- [x] Initialize FastAPI application
- [x] Create database models
- [x] Set up testing framework
EOF

# Create visualization folder
mkdir -p DEV-MAN/diagrams
cat > DEV-MAN/diagrams/architecture.md << 'EOF'
# Project Architecture

```mermaid
graph TD
    A[Markdown Files] --> B[FastAPI Backend]
    C[CSV Files] --> B
    B --> D[SQLite Database]
    B --> E[AG Grid Frontend]
    E --> F[User Interface]
```

## Component Details
1. **Data Sources**
   - Markdown files for card details
   - CSV import capability
   - Notion export compatibility

2. **Backend**
   - FastAPI for REST API
   - SQLAlchemy for ORM
   - Data validation and processing

3. **Frontend**
   - AG Grid for data display
   - Chart.js for visualizations
   - Responsive design

4. **Database**
   - SQLite for local storage
   - Migration support
   - Data persistence
EOF

# Create symlinks for documentation
ln -s ../../.cursorules DEV-MAN/docs/cursorules.md
ln -s ../../pytest.ini DEV-MAN/docs/pytest-config.md

# Create error tracking file
cat > DEV-MAN/progress/errors.md << 'EOF'
# Error Tracking Log

## Command Line Errors

### Setup and Installation
```bash
# Error during package installation
error: Failed to prepare distributions
  Caused by: Failed to build `credit-cards @ file:///Users/markcarpenter/Desktop/projects/FINANCES/credit-cards`
  Caused by: Build backend failed to build editable through `build_editable` (exit status: 1)
```

### Test Execution
```bash
# Pytest errors
ERROR: usage: pytest [options] [file_or_dir] [file_or_dir] [...]
pytest: error: unrecognized arguments: --cov=credit_cards --cov-report=term-missing
```

### Runtime Errors
```python
ModuleNotFoundError: No module named 'fastapi'
TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union
```

## Browser Console Errors

### Frontend JavaScript
```javascript
Uncaught TypeError: Cannot read properties of undefined (reading 'api')
```

### Network Requests
```
POST /upload-csv/ 400 (Bad Request)
GET /credit-cards/ 500 (Internal Server Error)
```

## Resolution Status

### Fixed Issues ✅
- [x] Package installation errors resolved by updating pyproject.toml
- [x] Test coverage configuration fixed in pytest.ini

### Pending Issues 🚧
- [ ] Browser console errors during CSV upload
- [ ] Test failures in markdown parser
- [ ] Database connection issues in tests

### Known Workarounds 🔧
1. **Package Installation**: Use `pip install -e .` instead of `uv pip install -e .`
2. **Test Coverage**: Install pytest-cov explicitly before running tests
3. **Database Tests**: Use in-memory SQLite for testing

## Error Categories

### Critical ❌
- Database connection failures
- API endpoint crashes
- Package installation failures

### Warning ⚠️
- Test coverage incomplete
- Frontend console warnings
- Deprecated function usage

### Info ℹ️
- Development server reloads
- Debug messages
- Performance metrics

## Latest Test Results
```
Tests: 10 total
✅ Passed: 4
❌ Failed: 3
⚠️ Errors: 3
📊 Coverage: 74%
```

## System Information
- OS: macOS
- Python: 3.12.7
- Browser: Chrome/Firefox
- Node.js: N/A

## Update History
1. 2024-03-XX: Initial error tracking setup
2. 2024-03-XX: Added test failure documentation
3. 2024-03-XX: Updated with browser console errors

---
*Last Updated: [Current Date]*
EOF

# Add error logging function
cat > DEV-MAN/scripts/log_error.sh << 'EOF'
#!/bin/bash

# Usage: ./log_error.sh "Error Category" "Error Message"
ERROR_FILE="../progress/errors.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "## $TIMESTAMP - $1" >> "$ERROR_FILE"
echo '```' >> "$ERROR_FILE"
echo "$2" >> "$ERROR_FILE"
echo '```' >> "$ERROR_FILE"
echo "" >> "$ERROR_FILE"
EOF

chmod +x DEV-MAN/scripts/log_error.sh

echo "DEV-MAN structure created successfully with error tracking!" 