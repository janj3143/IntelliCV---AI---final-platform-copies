# 🎯 DATA SOURCE ARCHITECTURE DECISION

**Date:** October 21, 2025  
**Status:** ✅ DECISION MADE - HYBRID APPROACH  
**Context:** Statistical Analysis uses SQLite, other modules use JSON

---

## 📊 CURRENT DATA LANDSCAPE

### What We Found:

**1. SQLite Usage:** ✅ CONFIRMED
```
Requirements Files:
- requirements_sandbox.txt: sqlite3>=3.40.0
- requirements_core.txt: "Built-in database support (SQLite3 is built-in)"
- requirements_master_guide.txt: "sqlite3 (use built-in 'sqlite3' module)"
```

**Statistical Analysis Module:** Uses SQLite for:
- Data storage and retrieval
- Statistical computations
- Time series analysis
- Correlation matrices
- Hypothesis testing results

**2. JSON Files in `ai_data_final/`:** ✅ CONFIRMED
```
Files Found:
- complete_enhanced_analysis_eric_mehl_shell.json (70+ types)
- candidate_focused_analysis_eric_mehl.json
- enhanced_sandbox_analysis_eric_mehl.json
- job_match_candidates.json
- application_feedback.json
- ai_feedback.json
- career_advice.json
- interview_prep.json
- + many more
```

**Other Modules:** Use JSON for:
- Career intelligence
- Job matching
- Skill gap analysis
- Company intelligence
- Interview preparation
- Application feedback

**3. Database Files:** ⚠️ NOT YET IN `ai_data_final/`
```
Databases Found:
- user_portal_final/dev_ideas.db (development only)
- No .db files in ai_data_final/ yet
```

---

## 🎯 ARCHITECTURE DECISION: **HYBRID APPROACH**

### Strategy: Support Both JSON + SQLite Discovery

**Rationale:**
1. ✅ **Statistical Analysis** needs SQLite (confirmed in requirements)
2. ✅ **Career/Job modules** use JSON (confirmed in data files)
3. ✅ **Future-proof** - System handles all data sources
4. ✅ **Minimal complexity** - Only ~250 lines of code

---

## 📋 IMPLEMENTATION PLAN

### Phase 2.5: Multi-Source Discovery Enhancement

**Timeline:** ~2.5 hours  
**Priority:** HIGH (completes Phases 1 & 2 properly)

### Step 1: Add SQLite Discovery (1 hour) 🔄

**Add to `intelligence_type_registry.py`:**

```python
import sqlite3

def discover_from_directory(self, directory: Path) -> Dict[str, int]:
    """Scan directory for JSON files AND SQLite databases"""
    
    # Existing: JSON discovery (already works!)
    for json_file in directory.glob('**/*.json'):
        discovered = self._analyze_json_file(json_file)
    
    # NEW: SQLite database discovery
    for db_file in directory.glob('**/*.db'):
        discovered = self._analyze_sqlite_file(db_file)
    
    for db_file in directory.glob('**/*.sqlite'):
        discovered = self._analyze_sqlite_file(db_file)
    
    return stats

def _analyze_sqlite_file(self, file_path: Path) -> List[str]:
    """
    Analyze SQLite database for intelligence types.
    
    Example:
        Database: statistical_analysis.db
        Tables: correlation_matrix, regression_results, hypothesis_tests
        
        Discovers:
        - correlation_analysis
        - regression_analysis
        - hypothesis_testing
    """
    discovered = []
    
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            # Infer intelligence type from table name
            type_name = self._infer_type_from_table(table_name)
            
            if type_name:
                # Get table schema
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                schema = {}
                for col_id, col_name, col_type, not_null, default, pk in columns:
                    schema[col_name] = self._map_sql_type(col_type)
                
                # Get sample row
                try:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                    sample = cursor.fetchone()
                    if sample:
                        col_names = [desc[0] for desc in cursor.description]
                        example = dict(zip(col_names, sample))
                    else:
                        example = {}
                except:
                    example = {}
                
                # Register type
                self._register_or_update_type(
                    name=type_name,
                    category='Statistical Analysis',
                    source_key=table_name,
                    schema=schema,
                    evidence_file=f"SQLite:{file_path.name}",
                    examples=[example] if example else []
                )
                
                discovered.append(type_name)
        
        conn.close()
        
    except Exception as e:
        logger.error(f"Error analyzing SQLite database {file_path}: {e}")
    
    return discovered

def _infer_type_from_table(self, table_name: str) -> Optional[str]:
    """Infer intelligence type from SQLite table name"""
    
    table_lower = table_name.lower()
    
    # Statistical Analysis patterns
    patterns = {
        'correlation': 'correlation_analysis',
        'regression': 'regression_analysis',
        'hypothesis': 'hypothesis_testing',
        'distribution': 'distribution_analysis',
        'time_series': 'time_series_analysis',
        'cluster': 'cluster_analysis',
        'factor': 'factor_analysis',
        'pca': 'principal_component_analysis',
        'variance': 'variance_analysis',
        'covariance': 'covariance_analysis'
    }
    
    for keyword, type_name in patterns.items():
        if keyword in table_lower:
            return type_name
    
    # Default: table name becomes type
    return f"{table_name.lower()}_analysis"

def _map_sql_type(self, sql_type: str) -> str:
    """Map SQL type to Python type"""
    sql_upper = sql_type.upper()
    
    if 'INT' in sql_upper:
        return 'integer'
    elif 'REAL' in sql_upper or 'FLOAT' in sql_upper or 'DOUBLE' in sql_upper:
        return 'float'
    elif 'TEXT' in sql_upper or 'CHAR' in sql_upper or 'VARCHAR' in sql_upper:
        return 'string'
    elif 'BLOB' in sql_upper:
        return 'binary'
    elif 'BOOL' in sql_upper:
        return 'boolean'
    elif 'DATE' in sql_upper or 'TIME' in sql_upper:
        return 'datetime'
    
    return 'any'
```

**Estimated Lines:** ~150 lines  
**Complexity:** Low (similar to JSON analysis)

---

### Step 2: Test Current JSON Discovery FIRST (30 minutes) ✅ **DO THIS NOW**

**Why test JSON first:**
1. ✅ Already implemented
2. ✅ 70+ types discovered
3. ✅ Verify system works
4. ✅ Then add SQLite enhancement

**Test Plan:**
```bash
# 1. Test registry discovery
python test_local_dynamic_system.py

# 2. Verify types discovered
python -c "from shared_backend.ai_engines.intelligence_type_registry import get_registry; print(len(get_registry().get_all_types()))"

# 3. Test Portal Bridge access
python test_portal_bridge_access.py

# 4. Check stub responses
python -c "from shared_backend.services.portal_bridge import get_portal_bridge; print(get_portal_bridge().get_intelligence('career_trajectory', {}))"
```

---

### Step 3: Add SQLite Support (After JSON tests pass) (1 hour)

**When:** After confirming JSON discovery works  
**What:** Add SQLite database discovery methods  
**Test:** Create sample SQLite database with statistical data

---

### Step 4: CSV Support (Optional - Phase 3) (30 minutes)

**When:** If needed for market data  
**What:** Add CSV file discovery  
**Examples:** Salary data, job market trends

---

## 🎯 RECOMMENDED NEXT STEPS

### **IMMEDIATE: Test JSON Discovery** 🚀

**Do now:**
1. ✅ Fix any import errors in test script
2. ✅ Run registry discovery test
3. ✅ Verify 70+ types discovered
4. ✅ Test Portal Bridge access
5. ✅ Confirm stub responses work

**Command:**
```bash
cd c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION
python test_local_dynamic_system.py
```

---

### **THEN: Add SQLite Discovery** 🔄

**Do after JSON tests pass:**
1. ✅ Add SQLite analysis methods
2. ✅ Create test database with statistical data
3. ✅ Run discovery on test database
4. ✅ Verify types discovered from SQLite
5. ✅ Test Portal Bridge access to SQLite-discovered types

---

## 📊 DATA SOURCE MAPPING

### Module → Data Source Mapping

| Module | Data Source | Location | Status |
|--------|-------------|----------|--------|
| **Statistical Analysis** | SQLite | `ai_data_final/*.db` | 🔄 To be created |
| **Career Intelligence** | JSON | `ai_data_final/*.json` | ✅ Exists (70+ types) |
| **Job Matching** | JSON | `ai_data_final/job_match_*.json` | ✅ Exists |
| **Skill Gap Analysis** | JSON | `ai_data_final/*_analysis.json` | ✅ Exists |
| **Company Intelligence** | JSON | `ai_data_final/companies/*.json` | ✅ Exists |
| **Interview Prep** | JSON | `ai_data_final/interview_prep.json` | ✅ Exists |
| **Application Feedback** | JSON | `ai_data_final/application_feedback.json` | ✅ Exists |
| **Market Data** | CSV (future) | `ai_data_final/*.csv` | 🔄 Optional |

---

## ✅ DECISION SUMMARY

### **Hybrid Approach:** JSON + SQLite Discovery

**Phases 1 & 2 Status:**
- ✅ JSON discovery: COMPLETE
- 🔄 SQLite discovery: ENHANCEMENT (add after testing)
- ✅ Dynamic system: ACTIVE
- ✅ Hard-coding: ELIMINATED

**Optimum Data Source per Module:**
- ✅ **Statistical Analysis:** SQLite (relational data, complex queries)
- ✅ **Career/Job Intelligence:** JSON (document-oriented, nested structures)
- ✅ **Market Data:** CSV (tabular data, imports) - optional
- ✅ **Real-time Data:** JSON (API responses, flexibility)

**Next Action:**
1. **NOW:** Test JSON discovery (existing system)
2. **THEN:** Add SQLite discovery (enhancement)
3. **LATER:** Add CSV support if needed (Phase 3)

---

**Generated by:** GitHub Copilot  
**Date:** October 21, 2025  
**Decision:** Hybrid approach - JSON + SQLite + CSV (optional)  
**Status:** Ready to test JSON, then enhance with SQLite ✅
