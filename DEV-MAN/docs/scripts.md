# Scripts Documentation

## Overview
This document explains the scripts available in the project and how to use them.

## Script Directory Structure
```
scripts/
├── create_dev_man.bat     # Windows version of DEV-MAN creator
├── create_dev_man.sh      # Linux/Mac version of DEV-MAN creator
└── log_error.bat          # Error logging utility
```

## Development Management Scripts

### create_dev_man (Windows/Linux)
Creates the development management structure for tracking project progress.

**Usage:**
```bash
# Windows
.\scripts\create_dev_man.bat

# Linux/Mac
./scripts/create_dev_man.sh
```

**Creates:**
- `DEV-MAN/docs/` - Documentation files
- `DEV-MAN/diagrams/` - Architecture diagrams
- `DEV-MAN/progress/` - Progress tracking
- `DEV-MAN/scripts/` - Utility scripts

### Error Logging

**Windows Usage:**
```batch
.\scripts\log_error.bat "Error Category" "Error Message"
```

**Linux Usage:**
```bash
./scripts/log_error.sh "Error Category" "Error Message"
```

Example:
```bash
./scripts/log_error.sh "API Error" "GoHighLevel connection timeout"
```

## Generated Structure
```
DEV-MAN/
├── docs/
│   ├── README.md (symlink)
│   ├── monitoring.md
│   └── scripts.md
├── diagrams/
│   └── architecture.md
├── progress/
│   ├── whats-working.md
│   ├── TODO.md
│   └── errors.md
└── scripts/
    └── log_error.bat/sh
```

## Common Tasks

### 1. Initial Setup
```bash
# Windows
.\scripts\create_dev_man.bat

# Linux/Mac
./scripts/create_dev_man.sh
```

### 2. Logging Errors
```bash
# Windows
.\scripts\log_error.bat "Infrastructure" "NGINX configuration failed"

# Linux/Mac
./scripts/log_error.sh "Infrastructure" "NGINX configuration failed"
```

### 3. Monitoring Health Checks
The monitoring configuration is automatically created in `DEV-MAN/docs/monitoring.md` with:
- API health endpoints
- Response time thresholds
- Error rate limits
- Downtime alerts

## Best Practices

1. **Error Logging**
   - Always include error category
   - Provide detailed error messages
   - Add timestamp for tracking
   - Use consistent categories

2. **Documentation Updates**
   - Update progress files regularly
   - Keep TODO list current
   - Document resolved issues

3. **Architecture Changes**
   - Update diagrams when adding components
   - Document new integrations
   - Keep monitoring thresholds current

## Script Permissions
For Linux/Mac systems, ensure scripts are executable:
```bash
chmod +x scripts/create_dev_man.sh
chmod +x scripts/log_error.sh
```

## Common Issues and Solutions

### Windows
1. **Symlink Creation**
   - Requires admin privileges
   - Run command prompt as administrator
   - Alternative: Create manual copies

### Linux/Mac
1. **Permission Denied**
   ```bash
   chmod +x scripts/*.sh
   ```

2. **Line Ending Issues**
   ```bash
   dos2unix scripts/*.sh
   ```

## Integration with Other Tools

### Docker Integration
Scripts can be run inside Docker containers:
```bash
docker exec -it container_name /app/scripts/create_dev_man.sh
```

### CI/CD Usage
Scripts can be integrated into CI/CD pipelines:
```yaml
steps:
  - name: Setup DEV-MAN
    run: ./scripts/create_dev_man.sh
  
  - name: Log Deployment Error
    if: failure()
    run: ./scripts/log_error.sh "Deployment" "Pipeline failed"
```

## Future Improvements
- [ ] Add automated testing scripts
- [ ] Create backup/restore utilities
- [ ] Add configuration validation
- [ ] Implement automated health checks 