# Timeline Package - Usage Guide

## Overview
Timeline is a file and activity monitoring system that tracks changes in your project and stores them in a local database with rich visualization options.

## Installation

1. Install the package in development mode:
```bash
# Using UV (recommended)
uv pip install -e .

# Or using regular pip
pip install -e .
```

## Basic Usage

### 1. Start Watching Files
```bash
# Watch current directory
timeline watch

# Watch specific directory
timeline watch --path /path/to/watch
```

### 2. View Recent Changes
```bash
# Show last 100 changes
timeline logs

# Show specific number of changes
timeline logs --limit 50

# Filter by event type
timeline logs --type file_change

# Filter by source
timeline logs --source "crews/"
```

## Log Files
- All logs are stored in `timeline/logs/` as markdown files
- Each log file includes:
  - Timestamp
  - Event type
  - Source
  - Action
  - Details (if available)
  - Content preview

## Database
- Default SQLite database at `timeline.db`
- Can use PostgreSQL by providing different DB URL:
```bash
timeline watch --db postgresql://user:pass@localhost/dbname
```

## Features

### 1. File Monitoring
- Tracks file changes in real-time
- Ignores common patterns (.git, __pycache__, etc.)
- Records file content changes

### 2. Terminal Command Tracking
- Captures terminal commands
- Records command output
- Links commands to file changes

### 3. Rich Visualization
- Terminal-based tables
- Markdown file output
- Filterable results

## Example Workflow

1. Start the watcher:
```bash
timeline watch
```

2. Make some changes to your files

3. View recent changes:
```bash
timeline logs --limit 10
```

4. Filter specific changes:
```bash
# View only Python file changes
timeline logs --type file_change --source ".py"

# View last 50 terminal commands
timeline logs --type terminal --limit 50
```

## Configuration

### Ignored Patterns
Default ignored patterns:
- *.pyc
- __pycache__
- .git
- node_modules

### Database Schema
```sql
CREATE TABLE timeline_events (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(50),
    source VARCHAR(100),
    action VARCHAR(50),
    details JSON,
    content TEXT
);
```

## Troubleshooting

### Common Issues

1. **Database Connection**
   ```bash
   # Check database connection
   timeline logs --db sqlite:///timeline.db
   ```

2. **File Permissions**
   - Ensure write permissions for logs directory
   - Ensure database file is writable

3. **Missing Events**
   - Check ignored patterns
   - Verify watch path is correct

### Getting Help
```bash
# Show all commands
timeline --help

# Show specific command help
timeline watch --help
timeline logs --help
```

## Integration with Other Tools

### 1. With CrewAI
- Timeline can track CrewAI operations
- Filter CrewAI events: `timeline logs --type crew`

### 2. With Cursor
- Tracks file changes from Cursor
- Records Cursor commands

## Best Practices

1. **Regular Cleanup**
   - Archive old log files
   - Maintain database size

2. **Filtering**
   - Use specific filters for better performance
   - Combine type and source filters

3. **Database Management**
   - Regular backups
   - Periodic maintenance

## Contributing
- Fork the repository
- Create feature branch
- Submit pull request

## License
MIT License 