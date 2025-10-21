# Troubleshooting Guide: Dynamic Intelligence System

**Version:** 1.0  
**Last Updated:** October 21, 2025

This guide helps you resolve common issues when using the Dynamic Intelligence System.

---

## 📚 Table of Contents

1. [Installation Issues](#installation-issues)
2. [Discovery Issues](#discovery-issues)
3. [Handler Issues](#handler-issues)
4. [Portal Bridge Issues](#portal-bridge-issues)
5. [Performance Issues](#performance-issues)
6. [Data Format Issues](#data-format-issues)
7. [Error Messages Explained](#error-messages-explained)
8. [Debugging Techniques](#debugging-techniques)
9. [FAQ](#faq)

---

## 1. Installation Issues

### Problem: "Module not found: intelligence_type_registry"

**Cause:** Missing or incorrect Python path

**Solution:**
```python
# Ensure correct path in imports
from shared_backend.ai_engines.intelligence_type_registry import IntelligenceTypeRegistry

# Or add to Python path
import sys
sys.path.append('/path/to/project/root')
```

---

### Problem: "No module named 'shared_backend'"

**Cause:** Working directory not set correctly

**Solution:**
```bash
# Set working directory to project root
cd /path/to/IntelliCV/SANDBOX/BACKEND-ADMIN-REORIENTATION

# Run from project root
python -m shared_backend.services.portal_bridge
```

---

### Problem: Import errors on startup

**Cause:** Circular imports or missing dependencies

**Solution:**
1. Check all `__init__.py` files exist
2. Verify import order
3. Check for circular dependencies

```python
# Good: Import from specific modules
from shared_backend.ai_engines.inference_engine import InferenceEngine

# Bad: Import entire module
import shared_backend.ai_engines  # May cause issues
```

---

## 2. Discovery Issues

### Problem: "No intelligence types discovered"

**Cause:** Data directory not found or empty

**Solution:**
```python
# 1. Check data directory exists
import os
data_path = 'path/to/ai_data_final'
print(f"Directory exists: {os.path.exists(data_path)}")
print(f"Files found: {len(os.listdir(data_path))}")

# 2. Check file format
import json
with open('ai_data_final/sample.json') as f:
    data = json.load(f)
    print(f"Valid JSON: {data}")

# 3. Verify discovery runs
from shared_backend.ai_engines.intelligence_type_registry import IntelligenceTypeRegistry
registry = IntelligenceTypeRegistry()
registry.discover_from_directory('ai_data_final')
print(f"Types discovered: {len(registry.list_types())}")
```

**Expected:** 70+ types discovered in < 10 seconds

---

### Problem: "New JSON file not discovered"

**Cause:** Application not restarted after adding file

**Solution:**
1. Stop application
2. Add JSON file to `ai_data_final/`
3. Restart application
4. Discovery runs automatically

**Verify:**
```python
bridge = PortalBridge()
types = bridge.get_intelligence_types()
print(f"Available types: {types['types']}")
```

---

### Problem: "Intelligence type patterns not recognized"

**Cause:** JSON doesn't match expected patterns

**Solution:**
Ensure JSON uses one of these patterns:

```json
{
    "career_intelligence": { ... },      // ✅ Pattern 1: _intelligence
    "skill_analysis": { ... },           // ✅ Pattern 2: _analysis
    "job_recommendations": { ... },      // ✅ Pattern 3: _recommendations
    "nested": {                          // ✅ Pattern 4: Nested
        "career_path": { ... }
    }
}
```

---

### Problem: "Duplicate intelligence types"

**Cause:** Same type in multiple files

**Solution:**
This is OK! Registry keeps first occurrence. To control priority:
1. Implement handler with higher priority
2. Or rename one type

**Check duplicates:**
```python
registry = IntelligenceTypeRegistry()
all_types = registry.list_types()
type_names = [t['name'] for t in all_types]
duplicates = [name for name in type_names if type_names.count(name) > 1]
print(f"Duplicates: {duplicates}")
```

---

## 3. Handler Issues

### Problem: "Handler not called for implemented type"

**Cause:** Handler not registered properly

**Solution:**
```python
# Check handler registration
from shared_backend.ai_engines.hybrid_integrator import HybridAIIntegrator

integrator = HybridAIIntegrator()
handler = integrator.intelligence_registry.get_handler('career_path')

if handler:
    print("✅ Handler registered")
else:
    print("❌ Handler not registered - check _register_intelligence_handlers()")
```

**Fix:** Add to `HybridAIIntegrator._register_intelligence_handlers()`:
```python
def _register_intelligence_handlers(self):
    self.intelligence_registry.register_handler(
        'career_path',
        lambda data: self.inference_engine.infer_career_path(data),
        priority='HIGH',
        description='Career path inference'
    )
```

---

### Problem: "Handler returns None"

**Cause:** Handler not returning dict

**Solution:**
All handlers must return dict with 'status':
```python
def my_handler(data):
    # ❌ Bad: Returns None
    results = process_data(data)
    
    # ✅ Good: Returns dict
    return {
        'status': 'success',
        'data': results
    }
```

---

### Problem: "Handler crashes with KeyError"

**Cause:** Missing required field in data

**Solution:**
Validate inputs in handler:
```python
def safe_handler(data):
    # Validate required fields
    required = ['profile', 'target_role']
    missing = [f for f in required if f not in data]
    
    if missing:
        return {
            'status': 'error',
            'error': f'Missing required fields: {missing}'
        }
    
    # Process data
    result = process_data(data)
    return {'status': 'success', 'data': result}
```

---

## 4. Portal Bridge Issues

### Problem: "get_intelligence() returns 'unknown' status"

**Cause:** Intelligence type not discovered

**Solution:**
```python
# 1. Check available types
bridge = PortalBridge()
available = bridge.get_intelligence_types()
print(f"Available: {available['types']}")

# 2. Check your type name
requested_type = 'career_path_analysis'
if requested_type in available['types']:
    print("✅ Type exists")
else:
    print(f"❌ Type not found. Did you mean: {available['types'][:5]}")
```

**Fix:** Use correct type name or add JSON file for new type

---

### Problem: "Metadata not appearing in results"

**Cause:** Old code not using Portal Bridge

**Solution:**
```python
# ❌ Old code (no metadata)
from shared_backend.ai_engines.inference_engine import InferenceEngine
engine = InferenceEngine()
result = engine.infer_career_path(data)  # No metadata

# ✅ New code (includes metadata)
from shared_backend.services.portal_bridge import PortalBridge
bridge = PortalBridge()
result = bridge.get_career_intelligence(data)  # Includes metadata

# Check metadata
if 'portal_bridge_metadata' in result:
    print("✅ Using Portal Bridge")
else:
    print("❌ Using old direct engine call")
```

---

### Problem: "Portal type not recognized"

**Cause:** Invalid portal_type value

**Solution:**
```python
# Valid portal types
VALID_PORTAL_TYPES = ['user', 'admin', 'recruiter']

# Use valid type
result = bridge.get_intelligence(
    intelligence_type='career_path',
    data=profile_data,
    portal_type='user'  # ✅ Valid
)

# Invalid will default to 'user'
result = bridge.get_intelligence(
    intelligence_type='career_path',
    data=profile_data,
    portal_type='invalid'  # ⚠️ Defaults to 'user'
)
```

---

## 5. Performance Issues

### Problem: "Slow startup (> 30 seconds)"

**Cause:** Too many files or slow disk

**Solution:**
```python
# 1. Check file count
import os
data_dir = 'ai_data_final'
files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
print(f"JSON files: {len(files)}")  # Should be < 5,000

# 2. Profile discovery
import time
start = time.time()
registry = IntelligenceTypeRegistry()
registry.discover_from_directory(data_dir)
elapsed = time.time() - start
print(f"Discovery time: {elapsed:.2f}s")  # Should be < 10s

# 3. If too slow, reduce files or use faster disk (SSD)
```

**Optimization:**
- Use SSD instead of HDD
- Reduce number of JSON files
- Cache discovery results (future feature)

---

### Problem: "Slow intelligence requests (> 5 seconds)"

**Cause:** Handler not optimized or loading data each time

**Solution:**
```python
# ❌ Bad: Loads data every request
def slow_handler(data):
    with open('large_file.json') as f:
        reference_data = json.load(f)  # Slow!
    return process(data, reference_data)

# ✅ Good: Load data once at init
class OptimizedEngine:
    def __init__(self):
        with open('large_file.json') as f:
            self.reference_data = json.load(f)  # Load once
    
    def handler(self, data):
        return process(data, self.reference_data)  # Fast!
```

**Profile handler:**
```python
import time
start = time.time()
result = bridge.get_career_intelligence(profile_data)
elapsed = time.time() - start
print(f"Request time: {elapsed:.2f}s")  # Should be < 1s
```

---

### Problem: "High memory usage (> 1GB)"

**Cause:** Too much data cached

**Solution:**
1. Check data size
2. Implement cache eviction
3. Use lazy loading

```python
# Check memory usage
import psutil
import os
process = psutil.Process(os.getpid())
memory_mb = process.memory_info().rss / 1024 / 1024
print(f"Memory usage: {memory_mb:.2f} MB")  # Should be < 500 MB
```

---

## 6. Data Format Issues

### Problem: "JSON parsing errors"

**Cause:** Invalid JSON format

**Solution:**
```python
# Validate JSON file
import json

try:
    with open('ai_data_final/file.json') as f:
        data = json.load(f)
    print("✅ Valid JSON")
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON: {e}")
    print(f"Error at line {e.lineno}, column {e.colno}")
```

**Common issues:**
- Trailing commas: `{"key": "value",}`
- Single quotes: `{'key': 'value'}` (use double quotes)
- Missing quotes: `{key: "value"}`

---

### Problem: "Schema extraction fails"

**Cause:** Unexpected data structure

**Solution:**
Ensure data follows patterns:
```json
{
    "career_intelligence": {
        "suggested_roles": ["Role 1", "Role 2"],
        "next_steps": ["Step 1", "Step 2"]
    }
}
```

**Check extracted schema:**
```python
registry = IntelligenceTypeRegistry()
registry.discover_from_directory('ai_data_final')
type_info = registry.get_type_info('career_intelligence')
print(f"Schema: {type_info.schema}")
```

---

## 7. Error Messages Explained

### "Intelligence type 'X' is not implemented yet"

**Meaning:** Type discovered but no handler registered

**Solution:** 
- Use stub response (helpful with schema)
- Or implement handler

**What to do:**
```python
result = bridge.get_intelligence('new_type', data)
# status: 'not_implemented'
# Use result['schema'] to see expected format
# Use result['example_usage'] to see how to use
```

---

### "Unknown intelligence type: X"

**Meaning:** Type not discovered or typo

**Solution:**
1. Check spelling
2. Check if type exists
3. Add JSON file if new type

```python
# Get available types
types = bridge.get_intelligence_types()
print(f"Available: {types['types']}")

# Check your type
if 'my_type' in types['types']:
    print("Type exists")
else:
    print("Type not found - check spelling or add JSON file")
```

---

### "Handler execution failed"

**Meaning:** Handler crashed

**Solution:**
Check logs for stack trace:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
result = bridge.get_intelligence('career_path', data)
# Check console for detailed error
```

**Fix handler:**
```python
def safe_handler(data):
    try:
        result = risky_operation(data)
        return {'status': 'success', 'data': result}
    except Exception as e:
        logging.error(f"Handler error: {e}", exc_info=True)
        return {'status': 'error', 'error': str(e)}
```

---

## 8. Debugging Techniques

### Enable Debug Logging

```python
import logging

# Enable debug logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Run operation
bridge = PortalBridge()
result = bridge.get_career_intelligence(profile_data)

# Check logs for detailed information
```

---

### Test Discovery Manually

```python
from shared_backend.ai_engines.intelligence_type_registry import IntelligenceTypeRegistry

# Create registry
registry = IntelligenceTypeRegistry()

# Discover types
types = registry.discover_from_directory('ai_data_final')
print(f"Discovered {len(types)} types")

# List all types
for type_name, type_info in types.items():
    print(f"- {type_name}: {type_info['description']}")

# Check specific type
type_info = registry.get_type_info('career_path')
print(f"Career path info: {type_info}")
```

---

### Test Handler Registration

```python
from shared_backend.ai_engines.hybrid_integrator import HybridAIIntegrator

# Create integrator
integrator = HybridAIIntegrator()

# Check handlers
registered = integrator.intelligence_registry._handlers
print(f"Registered handlers: {list(registered.keys())}")

# Test specific handler
handler = integrator.intelligence_registry.get_handler('career_path')
if handler:
    print("✅ Handler exists")
    test_data = {'profile': {}}
    result = handler(test_data)
    print(f"Test result: {result}")
else:
    print("❌ Handler not registered")
```

---

### Test Portal Bridge

```python
from shared_backend.services.portal_bridge import PortalBridge

# Create bridge
bridge = PortalBridge()

# Test universal method
result = bridge.get_intelligence(
    intelligence_type='career_path',
    data={'profile': {'skills': ['Python']}},
    portal_type='user'
)

print(f"Status: {result['status']}")
print(f"Has metadata: {'portal_bridge_metadata' in result}")

# Test convenience method
result = bridge.get_career_intelligence({'profile': {'skills': ['Python']}})
print(f"Convenience method works: {result['status'] == 'success'}")
```

---

### Profile Performance

```python
import time

# Test discovery time
start = time.time()
registry = IntelligenceTypeRegistry()
registry.discover_from_directory('ai_data_final')
discovery_time = time.time() - start
print(f"Discovery: {discovery_time:.2f}s")  # Should be < 10s

# Test request time
bridge = PortalBridge()
start = time.time()
result = bridge.get_career_intelligence(profile_data)
request_time = time.time() - start
print(f"Request: {request_time:.2f}s")  # Should be < 1s

# Test handler lookup time
start = time.time()
handler = registry.get_handler('career_path')
lookup_time = time.time() - start
print(f"Lookup: {lookup_time*1000:.2f}ms")  # Should be < 1ms
```

---

## 9. FAQ

### Q: Why is my new intelligence type not showing up?

**A:** Did you restart the application? Discovery runs once at startup. Add JSON file, restart, type available.

---

### Q: Can I add intelligence types without restarting?

**A:** Not currently. Discovery runs at startup. Future feature: hot-reload.

---

### Q: What's the difference between 'not_implemented' and 'unknown'?

**A:** 
- `not_implemented`: Type discovered, no handler (returns helpful stub)
- `unknown`: Type not discovered at all (typo or missing JSON)

---

### Q: How do I know if I'm using Portal Bridge or old code?

**A:** Check imports:
```python
# ✅ Portal Bridge
from shared_backend.services.portal_bridge import PortalBridge

# ❌ Old code
from shared_backend.ai_engines.inference_engine import InferenceEngine
```

Also check for metadata:
```python
if 'portal_bridge_metadata' in result:
    print("Using Portal Bridge")
```

---

### Q: Can I use both Portal Bridge and direct engine calls?

**A:** Yes, backward compatible. But Portal Bridge is recommended for consistency and features.

---

### Q: How do I add my own handler?

**A:** See [DEVELOPER_GUIDE.md - Section 5: Implementing Handlers](DEVELOPER_GUIDE.md#5-implementing-handlers)

---

### Q: What happens if two JSON files have the same intelligence type?

**A:** Registry keeps first occurrence. Implement handler with priority to control which is used.

---

### Q: How do I test if my migration is complete?

**A:** Run migration tests:
```bash
pytest tests/test_phase_3_portal_migration.py -v
```

Check all imports changed from InferenceEngine to PortalBridge.

---

### Q: Can I use Portal Bridge in background jobs?

**A:** Yes! Portal Bridge is stateless and thread-safe. Safe for:
- Background tasks
- Scheduled jobs
- Multiple threads
- Async operations

---

### Q: How do I see all available intelligence types?

**A:**
```python
bridge = PortalBridge()
types_result = bridge.get_intelligence_types()
all_types = types_result['types']
print(f"Available types: {len(all_types)}")
for type_name in all_types:
    print(f"- {type_name}")
```

---

## Need More Help?

1. **Check docs:**
   - [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - How to use system
   - [API_REFERENCE.md](API_REFERENCE.md) - Complete API docs
   - [PORTAL_MIGRATION_GUIDE.md](PORTAL_MIGRATION_GUIDE.md) - Migration help
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design

2. **Enable debug logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Check logs:**
   ```bash
   tail -f logs/system.log
   ```

4. **Run tests:**
   ```bash
   pytest tests/ -v --log-cli-level=DEBUG
   ```

---

**Document Version:** 1.0  
**Last Updated:** October 21, 2025  
**Status:** ✅ Production Ready
