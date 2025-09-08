# Migration Guide: Traditional Logger to Structured Logger

## Current Usage (Traditional)
```python
import logging
global logger
logger = logging.getLogger('Osdag')
logger.error("Connection failed")
logger.warning("Low memory")
logger.info("Design completed")
```

## New Usage (Structured)
```python
from structured_logger import error, warning, info, debug, get_logs

# Simple usage - same as before but with structured output
error("Connection failed", "connection_error")
warning("Low memory", "memory_warning") 
info("Design completed", "design_success")

# Get structured logs
logs = get_logs()
# Returns: [{"msg":"Connection failed", "type":"connection_error"}, ...]
```

## Integration Steps

### Step 1: Replace imports
```python
# OLD
import logging
global logger
logger = logging.getLogger('Osdag')

# NEW
from structured_logger import error, warning, info, debug
```

### Step 2: Update log calls
```python
# OLD
logger.error("Connection failed")
logger.warning("Low memory")
logger.info("Design completed")

# NEW
error("Connection failed", "connection_error")
warning("Low memory", "memory_warning")
info("Design completed", "design_success")
```

### Step 3: Access structured logs
```python
from structured_logger import get_logs, get_logs_json, save_logs

# Get logs as list of dicts
logs = get_logs()

# Get logs as JSON string
json_logs = get_logs_json()

# Save logs to file
save_logs("design_logs.json")
```

## Benefits
- ✅ Structured JSON format
- ✅ Backward compatible with traditional logging
- ✅ Easy to parse and analyze
- ✅ Includes timestamps and metadata
- ✅ Can save/load logs
