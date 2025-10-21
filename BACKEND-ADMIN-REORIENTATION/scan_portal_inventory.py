"""
Portal Inventory Scanner for Phase 4 Stage 2

Scans all portal directories to:
1. Find all Python files (portal pages)
2. Identify AI engine imports
3. Count AI method calls
4. Categorize pages by complexity
5. Generate comprehensive inventory
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import json

class PortalInventoryScanner:
    """Scans portal directories for AI engine usage"""
    
    def __init__(self):
        self.inventory = defaultdict(list)
        self.statistics = {
            'total_pages': 0,
            'pages_with_ai': 0,
            'pages_migrated': 0,
            'pages_need_migration': 0,
            'simple_pages': 0,
            'medium_pages': 0,
            'complex_pages': 0
        }
        
        # Patterns to detect
        self.old_imports = [
            r'from shared_backend\.ai_engines\.inference_engine import',
            r'from shared_backend\.ai_engines\.hybrid_integrator import',
            r'import.*InferenceEngine',
            r'import.*HybridAIIntegrator'
        ]
        
        self.new_imports = [
            r'from shared_backend\.services\.portal_bridge import',
            r'import.*PortalBridge'
        ]
        
        self.ai_method_patterns = [
            # Old methods
            r'\.infer_career_path\(',
            r'\.match_job_to_candidate\(',
            r'\.analyze_skill_gaps\(',
            r'\.analyze_salary\(',
            r'\.run_inference\(',
            
            # New methods
            r'\.get_career_intelligence\(',
            r'\.get_job_matches\(',
            r'\.get_skill_recommendations\(',
            r'\.get_salary_insights\(',
            r'\.get_intelligence\(',
            r'\.get_career_trajectory\(',
            r'\.get_job_recommendations\(',
            r'\.get_company_intelligence\(',
        ]
    
    def scan_directory(self, directory, portal_name):
        """Scan a portal directory for pages"""
        print(f"\n{'='*80}")
        print(f"Scanning: {portal_name}")
        print(f"Directory: {directory}")
        print(f"{'='*80}\n")
        
        if not os.path.exists(directory):
            print(f"⚠️  Directory not found: {directory}")
            return
        
        pages_dir = Path(directory) / 'pages'
        if not pages_dir.exists():
            pages_dir = Path(directory)  # Try without pages/ subdirectory
        
        # Find all .py files
        py_files = list(pages_dir.rglob('*.py'))
        print(f"Found {len(py_files)} Python files")
        
        for py_file in py_files:
            self.scan_file(py_file, portal_name)
    
    def scan_file(self, file_path, portal_name):
        """Scan a single file for AI usage"""
        self.statistics['total_pages'] += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return
        
        # Check for AI engine imports
        has_old_import = any(re.search(pattern, content) for pattern in self.old_imports)
        has_new_import = any(re.search(pattern, content) for pattern in self.new_imports)
        
        # Count AI method calls
        ai_calls = []
        for pattern in self.ai_method_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                # Get context (line where call occurs)
                line_start = content.rfind('\n', 0, match.start()) + 1
                line_end = content.find('\n', match.end())
                if line_end == -1:
                    line_end = len(content)
                line = content[line_start:line_end].strip()
                
                ai_calls.append({
                    'method': match.group(0),
                    'line': line[:100]  # First 100 chars
                })
        
        # Skip if no AI usage
        if not has_old_import and not has_new_import and not ai_calls:
            return
        
        self.statistics['pages_with_ai'] += 1
        
        # Determine migration status
        if has_new_import:
            migration_status = 'MIGRATED'
            self.statistics['pages_migrated'] += 1
        elif has_old_import:
            migration_status = 'NEEDS_MIGRATION'
            self.statistics['pages_need_migration'] += 1
        elif ai_calls:
            migration_status = 'UNKNOWN'
        else:
            migration_status = 'NO_AI'
        
        # Categorize by complexity
        call_count = len(ai_calls)
        if call_count <= 2:
            complexity = 'SIMPLE'
            self.statistics['simple_pages'] += 1
        elif call_count <= 5:
            complexity = 'MEDIUM'
            self.statistics['medium_pages'] += 1
        else:
            complexity = 'COMPLEX'
            self.statistics['complex_pages'] += 1
        
        # Calculate priority
        if complexity == 'SIMPLE' and migration_status == 'NEEDS_MIGRATION':
            priority = 'HIGH'
        elif complexity == 'MEDIUM' and migration_status == 'NEEDS_MIGRATION':
            priority = 'MEDIUM'
        elif complexity == 'COMPLEX' and migration_status == 'NEEDS_MIGRATION':
            priority = 'LOW'
        elif migration_status == 'MIGRATED':
            priority = 'DONE'
        else:
            priority = 'REVIEW'
        
        # Get relative path
        try:
            rel_path = file_path.relative_to(Path.cwd())
        except:
            rel_path = file_path
        
        # Add to inventory
        page_info = {
            'file': str(rel_path),
            'name': file_path.stem,
            'portal': portal_name,
            'migration_status': migration_status,
            'complexity': complexity,
            'priority': priority,
            'ai_call_count': call_count,
            'has_old_import': has_old_import,
            'has_new_import': has_new_import,
            'ai_calls': ai_calls[:10]  # Limit to first 10
        }
        
        self.inventory[portal_name].append(page_info)
        
        # Print status
        status_icon = {
            'MIGRATED': '✅',
            'NEEDS_MIGRATION': '🔄',
            'UNKNOWN': '❓',
            'NO_AI': '⚪'
        }
        
        print(f"{status_icon.get(migration_status, '❓')} {complexity:8} | {file_path.name:50} | {call_count:2} calls | {priority}")
    
    def generate_report(self):
        """Generate comprehensive report"""
        print(f"\n{'='*80}")
        print("PORTAL INVENTORY SUMMARY")
        print(f"{'='*80}\n")
        
        print(f"Total Pages Scanned: {self.statistics['total_pages']}")
        print(f"Pages with AI Usage: {self.statistics['pages_with_ai']}")
        print(f"  - Already Migrated: {self.statistics['pages_migrated']}")
        print(f"  - Need Migration: {self.statistics['pages_need_migration']}")
        print()
        
        print("Complexity Breakdown:")
        print(f"  - Simple (1-2 calls): {self.statistics['simple_pages']}")
        print(f"  - Medium (3-5 calls): {self.statistics['medium_pages']}")
        print(f"  - Complex (6+ calls): {self.statistics['complex_pages']}")
        print()
        
        # By portal
        print("By Portal:")
        for portal, pages in self.inventory.items():
            needs_migration = sum(1 for p in pages if p['migration_status'] == 'NEEDS_MIGRATION')
            migrated = sum(1 for p in pages if p['migration_status'] == 'MIGRATED')
            print(f"  - {portal:30} | {len(pages):3} pages | {needs_migration:2} need migration | {migrated:2} migrated")
        print()
        
        # Migration priority
        print("Migration Priority:")
        all_pages = []
        for pages in self.inventory.values():
            all_pages.extend(pages)
        
        high_priority = [p for p in all_pages if p['priority'] == 'HIGH']
        medium_priority = [p for p in all_pages if p['priority'] == 'MEDIUM']
        low_priority = [p for p in all_pages if p['priority'] == 'LOW']
        
        print(f"  - HIGH Priority (Simple, needs migration): {len(high_priority)}")
        print(f"  - MEDIUM Priority (Medium, needs migration): {len(medium_priority)}")
        print(f"  - LOW Priority (Complex, needs migration): {len(low_priority)}")
        print()
    
    def save_inventory(self, output_file='portal_inventory.json'):
        """Save inventory to JSON file"""
        output = {
            'statistics': self.statistics,
            'inventory': dict(self.inventory),
            'migration_order': self.get_migration_order()
        }
        
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Inventory saved to: {output_file}")
    
    def get_migration_order(self):
        """Get recommended migration order"""
        all_pages = []
        for pages in self.inventory.values():
            all_pages.extend(pages)
        
        # Filter pages that need migration
        needs_migration = [p for p in all_pages if p['migration_status'] == 'NEEDS_MIGRATION']
        
        # Sort by priority (HIGH -> MEDIUM -> LOW) and complexity (SIMPLE -> COMPLEX)
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        complexity_order = {'SIMPLE': 0, 'MEDIUM': 1, 'COMPLEX': 2}
        
        needs_migration.sort(key=lambda p: (
            priority_order.get(p['priority'], 999),
            complexity_order.get(p['complexity'], 999),
            p['ai_call_count']
        ))
        
        return [{'file': p['file'], 'complexity': p['complexity'], 'calls': p['ai_call_count']} 
                for p in needs_migration]
    
    def generate_markdown_report(self, output_file='docs/PORTAL_INVENTORY.md'):
        """Generate markdown report"""
        all_pages = []
        for pages in self.inventory.values():
            all_pages.extend(pages)
        
        needs_migration = [p for p in all_pages if p['migration_status'] == 'NEEDS_MIGRATION']
        migrated = [p for p in all_pages if p['migration_status'] == 'MIGRATED']
        
        content = f"""# Portal Inventory Report

**Date:** {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}  
**Phase:** 4 Stage 2  
**Status:** Complete ✅

---

## Executive Summary

| Metric | Count |
|--------|-------|
| **Total Pages Scanned** | {self.statistics['total_pages']} |
| **Pages with AI Usage** | {self.statistics['pages_with_ai']} |
| **Pages Migrated** | {self.statistics['pages_migrated']} ✅ |
| **Pages Need Migration** | {self.statistics['pages_need_migration']} 🔄 |

---

## Complexity Breakdown

| Complexity | Count | Description |
|------------|-------|-------------|
| **SIMPLE** | {self.statistics['simple_pages']} | 1-2 AI calls |
| **MEDIUM** | {self.statistics['medium_pages']} | 3-5 AI calls |
| **COMPLEX** | {self.statistics['complex_pages']} | 6+ AI calls |

---

## By Portal

| Portal | Total Pages | Need Migration | Migrated |
|--------|-------------|----------------|----------|
"""
        
        for portal, pages in self.inventory.items():
            needs = sum(1 for p in pages if p['migration_status'] == 'NEEDS_MIGRATION')
            mig = sum(1 for p in pages if p['migration_status'] == 'MIGRATED')
            content += f"| {portal} | {len(pages)} | {needs} | {mig} |\n"
        
        content += f"""
---

## Migration Priority

### HIGH Priority (Simple pages - Quick wins!)
{len([p for p in needs_migration if p['priority'] == 'HIGH'])} pages

"""
        
        high_priority = [p for p in needs_migration if p['priority'] == 'HIGH']
        for i, page in enumerate(high_priority[:10], 1):  # Top 10
            content += f"{i}. `{page['file']}` - {page['ai_call_count']} calls\n"
        
        content += f"""
### MEDIUM Priority (Medium complexity)
{len([p for p in needs_migration if p['priority'] == 'MEDIUM'])} pages

"""
        
        medium_priority = [p for p in needs_migration if p['priority'] == 'MEDIUM']
        for i, page in enumerate(medium_priority[:10], 1):  # Top 10
            content += f"{i}. `{page['file']}` - {page['ai_call_count']} calls\n"
        
        content += f"""
### LOW Priority (Complex pages - More effort)
{len([p for p in needs_migration if p['priority'] == 'LOW'])} pages

"""
        
        low_priority = [p for p in needs_migration if p['priority'] == 'LOW']
        for i, page in enumerate(low_priority[:10], 1):  # Top 10
            content += f"{i}. `{page['file']}` - {page['ai_call_count']} calls\n"
        
        content += f"""
---

## Already Migrated ✅

{len(migrated)} pages already using Portal Bridge

"""
        
        for i, page in enumerate(migrated[:20], 1):  # Top 20
            content += f"{i}. `{page['file']}` - {page['ai_call_count']} calls\n"
        
        content += f"""
---

## Complete Inventory

### Pages Needing Migration ({len(needs_migration)})

| # | File | Complexity | Calls | Priority |
|---|------|------------|-------|----------|
"""
        
        for i, page in enumerate(needs_migration, 1):
            content += f"| {i} | `{page['file']}` | {page['complexity']} | {page['ai_call_count']} | {page['priority']} |\n"
        
        content += f"""
---

## Next Steps

### Immediate Actions (Next 1-2 hours)

1. **Start with HIGH priority pages** ({len(high_priority)} pages)
   - Simple migrations (1-2 calls)
   - Quick wins to build momentum
   - Test thoroughly

2. **Move to MEDIUM priority** ({len(medium_priority)} pages)
   - More AI calls but manageable
   - Build confidence with patterns

3. **Tackle COMPLEX pages last** ({len(low_priority)} pages)
   - Most AI calls
   - Most complexity
   - Use lessons learned

### Migration Estimate

- HIGH priority: ~15-30 min per page = {len(high_priority) * 20 // 60} hours
- MEDIUM priority: ~30-45 min per page = {len(medium_priority) * 37 // 60} hours
- COMPLEX priority: ~1-2 hours per page = {len(low_priority) * 90 // 60} hours

**Total Estimated Time:** {(len(high_priority) * 20 + len(medium_priority) * 37 + len(low_priority) * 90) // 60} hours

---

**Report Generated:** Stage 2 Complete  
**Next Stage:** Stage 3 - Pilot Migration  
**Status:** Ready to proceed ✅
"""
        
        # Write to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Markdown report saved to: {output_file}")


def main():
    """Main execution"""
    scanner = PortalInventoryScanner()
    
    # Define portal directories
    portals = [
        ('user_portal_final', r'c:\IntelliCV-AI\IntelliCV\SANDBOX\user_portal_final'),
        ('user_portal', r'c:\IntelliCV-AI\IntelliCV\SANDBOX\user_portal'),
        ('BACKEND-ADMIN-REORIENTATION', r'c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION'),
    ]
    
    # Scan each portal
    for portal_name, directory in portals:
        scanner.scan_directory(directory, portal_name)
    
    # Generate reports
    scanner.generate_report()
    scanner.save_inventory('portal_inventory.json')
    scanner.generate_markdown_report('docs/PORTAL_INVENTORY.md')
    
    print(f"\n{'='*80}")
    print("✅ Portal inventory scan complete!")
    print(f"{'='*80}\n")
    print("Next steps:")
    print("1. Review docs/PORTAL_INVENTORY.md")
    print("2. Start with HIGH priority pages")
    print("3. Use PORTAL_MIGRATION_GUIDE.md for migration patterns")
    print()


if __name__ == '__main__':
    main()
