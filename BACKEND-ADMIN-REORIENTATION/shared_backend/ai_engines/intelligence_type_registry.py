"""
Dynamic Intelligence Type Registry
Automatically discovers and registers intelligence types from data files

Created: October 21, 2025
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Callable
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class IntelligenceType:
    """Definition of a discovered intelligence type"""
    name: str
    category: str
    source_keys: List[str] = field(default_factory=list)
    schema: Dict[str, Any] = field(default_factory=dict)
    input_structure: str = "Dict[str, Any]"
    output_structure: str = "Dict[str, Any]"
    handler: Optional[Callable] = None
    priority: str = "MEDIUM"  # HIGH, MEDIUM, LOW
    evidence_files: List[str] = field(default_factory=list)
    usage_count: int = 0
    is_implemented: bool = False
    description: str = ""
    examples: List[Dict] = field(default_factory=list)
    related_types: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'category': self.category,
            'source_keys': self.source_keys,
            'schema': self.schema,
            'input_structure': self.input_structure,
            'output_structure': self.output_structure,
            'has_handler': self.handler is not None,
            'priority': self.priority,
            'evidence_files': self.evidence_files,
            'usage_count': self.usage_count,
            'is_implemented': self.is_implemented,
            'description': self.description,
            'related_types': self.related_types
        }


class IntelligenceTypeRegistry:
    """
    Dynamic registry for intelligence types.
    Discovers types from data files and registers handlers.
    """
    
    def __init__(self, data_directory: Optional[Path] = None):
        """
        Initialize the registry.
        
        Args:
            data_directory: Path to directory containing evidence files
        """
        self.data_directory = data_directory
        self.types: Dict[str, IntelligenceType] = {}
        self.categories: Dict[str, List[str]] = defaultdict(list)
        self.discovery_log: List[Dict] = []
        
        logger.info("Initialized Intelligence Type Registry")
    
    def discover_from_directory(self, directory: Path) -> Dict[str, int]:
        """
        Scan directory for JSON files and discover intelligence types.
        
        Args:
            directory: Path to directory to scan
            
        Returns:
            Discovery statistics
        """
        logger.info(f"Discovering intelligence types from: {directory}")
        
        stats = {
            'files_scanned': 0,
            'types_discovered': 0,
            'schemas_extracted': 0,
            'errors': 0
        }
        
        if not directory.exists():
            logger.warning(f"Directory not found: {directory}")
            return stats
        
        # Scan JSON files
        for json_file in directory.glob('**/*.json'):
            try:
                stats['files_scanned'] += 1
                discovered = self._analyze_file(json_file)
                stats['types_discovered'] += len(discovered)
                logger.info(f"Discovered {len(discovered)} types from {json_file.name}")
            except Exception as e:
                logger.error(f"Error analyzing {json_file}: {e}")
                stats['errors'] += 1
        
        logger.info(f"Discovery complete: {stats}")
        return stats
    
    def _analyze_file(self, file_path: Path) -> List[str]:
        """
        Analyze a JSON file and extract intelligence types.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of discovered type names
        """
        discovered = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON in {file_path}: {e}")
                return discovered
        
        # Analyze top-level keys
        if isinstance(data, dict):
            for key, value in data.items():
                type_name = self._infer_type_name(key)
                category = self._infer_category(key, value)
                schema = self._extract_schema(value)
                
                if type_name:
                    self._register_or_update_type(
                        name=type_name,
                        category=category,
                        source_key=key,
                        schema=schema,
                        evidence_file=str(file_path.name)
                    )
                    discovered.append(type_name)
                
                # Analyze nested structures
                if isinstance(value, dict):
                    nested_types = self._analyze_nested(key, value, file_path.name)
                    discovered.extend(nested_types)
        
        return discovered
    
    def _infer_type_name(self, key: str) -> Optional[str]:
        """
        Infer intelligence type name from key.
        
        Args:
            key: JSON key name
            
        Returns:
            Inferred type name or None
        """
        # Rule 1: Keys ending in "_intelligence"
        if key.endswith('_intelligence'):
            base = key.replace('_intelligence', '')
            # Special mappings
            if base == 'web_company':
                return 'company_intelligence'
            elif base == 'business':
                return 'market_intelligence'
            else:
                return f"{base}_intelligence"
        
        # Rule 2: Keys ending in "_analysis"
        if key.endswith('_analysis'):
            return key  # Keep as-is
        
        # Rule 3: Keys ending in "_profile"
        if key.endswith('_profile'):
            return f"{key.replace('_profile', '')}_profile_analysis"
        
        # Rule 4: Known patterns
        known_mappings = {
            'metadata': 'metadata_tracking',
            'user_touchpoints': 'touchpoint_analysis',
            'candidate_journey': 'candidate_journey_tracking',
            'engagement_metrics': 'engagement_metrics',
            'recruiter_notes': 'recruiter_intelligence'
        }
        
        if key in known_mappings:
            return known_mappings[key]
        
        # Default: key becomes type name
        return key.lower().replace(' ', '_')
    
    def _infer_category(self, key: str, value: Any) -> str:
        """
        Infer category from key and value structure.
        
        Args:
            key: JSON key name
            value: JSON value
            
        Returns:
            Category name
        """
        # Pattern-based categorization
        if 'intelligence' in key:
            if 'company' in key or 'web' in key:
                return 'Company & Market Intelligence'
            elif 'business' in key or 'market' in key:
                return 'Business Intelligence'
            else:
                return 'Intelligence & Analytics'
        
        if 'profile' in key or 'candidate' in key:
            return 'Profile & Identity'
        
        if 'skill' in key:
            return 'Skills & Capabilities'
        
        if 'location' in key or 'geography' in key:
            return 'Location & Geography'
        
        if 'salary' in key or 'compensation' in key:
            return 'Salary & Compensation'
        
        if 'job' in key or 'match' in key or 'compatibility' in key:
            return 'Job Matching & Compatibility'
        
        if 'network' in key or 'connection' in key:
            return 'Network & Relationships'
        
        if 'career' in key:
            return 'Career & Growth'
        
        if 'touchpoint' in key or 'engagement' in key or 'journey' in key:
            return 'Engagement & Touchpoints'
        
        if 'ai' in key or 'confidence' in key or 'score' in key:
            return 'AI & Quality Metrics'
        
        if 'education' in key or 'qualification' in key:
            return 'Education & Qualifications'
        
        return 'Uncategorized'
    
    def _extract_schema(self, value: Any, max_depth: int = 3, current_depth: int = 0) -> Dict[str, str]:
        """
        Extract schema from value structure.
        
        Args:
            value: JSON value to analyze
            max_depth: Maximum nesting depth
            current_depth: Current depth
            
        Returns:
            Schema dictionary
        """
        if current_depth >= max_depth:
            return {}
        
        schema = {}
        
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, str):
                    # Infer type from value patterns
                    if '@' in v:
                        schema[k] = 'email'
                    elif v.startswith('http'):
                        schema[k] = 'url'
                    elif '%' in v:
                        schema[k] = 'percentage'
                    elif '£' in v or '$' in v or '€' in v:
                        schema[k] = 'currency'
                    else:
                        schema[k] = 'string'
                elif isinstance(v, bool):
                    schema[k] = 'boolean'
                elif isinstance(v, int):
                    schema[k] = 'integer'
                elif isinstance(v, float):
                    schema[k] = 'float'
                elif isinstance(v, list):
                    if v and isinstance(v[0], dict):
                        schema[k] = f"List[{self._extract_schema(v[0], max_depth, current_depth + 1)}]"
                    else:
                        schema[k] = 'array'
                elif isinstance(v, dict):
                    schema[k] = self._extract_schema(v, max_depth, current_depth + 1)
        
        return schema
    
    def _analyze_nested(self, parent_key: str, data: Dict, file_name: str) -> List[str]:
        """
        Analyze nested structures for additional types.
        
        Args:
            parent_key: Parent key name
            data: Nested data
            file_name: Source file name
            
        Returns:
            List of discovered type names
        """
        discovered = []
        
        for key, value in data.items():
            # Look for specific patterns that indicate sub-types
            if isinstance(value, dict) and len(value) > 0:
                type_name = self._infer_type_name(key)
                if type_name and type_name not in self.types:
                    category = self._infer_category(key, value)
                    schema = self._extract_schema(value)
                    
                    self._register_or_update_type(
                        name=type_name,
                        category=category,
                        source_key=f"{parent_key}.{key}",
                        schema=schema,
                        evidence_file=file_name
                    )
                    discovered.append(type_name)
        
        return discovered
    
    def _register_or_update_type(
        self,
        name: str,
        category: str,
        source_key: str,
        schema: Dict,
        evidence_file: str
    ):
        """
        Register a new type or update existing one.
        
        Args:
            name: Type name
            category: Category name
            source_key: Source key in JSON
            schema: Extracted schema
            evidence_file: Source file name
        """
        if name in self.types:
            # Update existing
            intel_type = self.types[name]
            if source_key not in intel_type.source_keys:
                intel_type.source_keys.append(source_key)
            if evidence_file not in intel_type.evidence_files:
                intel_type.evidence_files.append(evidence_file)
            # Merge schemas
            intel_type.schema.update(schema)
        else:
            # Create new
            intel_type = IntelligenceType(
                name=name,
                category=category,
                source_keys=[source_key],
                schema=schema,
                evidence_files=[evidence_file]
            )
            self.types[name] = intel_type
            self.categories[category].append(name)
            
            # Log discovery
            self.discovery_log.append({
                'timestamp': datetime.now().isoformat(),
                'type': name,
                'category': category,
                'source_key': source_key,
                'file': evidence_file
            })
    
    def register_handler(
        self,
        type_name: str,
        handler: Callable,
        priority: str = "MEDIUM",
        description: str = ""
    ):
        """
        Register a handler for an intelligence type.
        
        Args:
            type_name: Intelligence type name
            handler: Callable handler function
            priority: Priority level (HIGH, MEDIUM, LOW)
            description: Handler description
        """
        if type_name not in self.types:
            logger.warning(f"Type '{type_name}' not in registry, creating entry")
            self.types[type_name] = IntelligenceType(
                name=type_name,
                category='Uncategorized'
            )
        
        intel_type = self.types[type_name]
        intel_type.handler = handler
        intel_type.priority = priority
        intel_type.is_implemented = True
        if description:
            intel_type.description = description
        
        logger.info(f"Registered handler for '{type_name}' (priority: {priority})")
    
    def get_handler(self, type_name: str) -> Optional[Callable]:
        """
        Get handler for an intelligence type.
        
        Args:
            type_name: Intelligence type name
            
        Returns:
            Handler function or None
        """
        if type_name in self.types:
            self.types[type_name].usage_count += 1
            return self.types[type_name].handler
        return None
    
    def get_type_info(self, type_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an intelligence type.
        
        Args:
            type_name: Intelligence type name
            
        Returns:
            Type information dictionary or None
        """
        if type_name in self.types:
            return self.types[type_name].to_dict()
        return None
    
    def list_types(
        self,
        category: Optional[str] = None,
        implemented_only: bool = False,
        priority: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List registered intelligence types.
        
        Args:
            category: Filter by category
            implemented_only: Only return implemented types
            priority: Filter by priority
            
        Returns:
            List of type information dictionaries
        """
        results = []
        
        for intel_type in self.types.values():
            # Apply filters
            if category and intel_type.category != category:
                continue
            if implemented_only and not intel_type.is_implemented:
                continue
            if priority and intel_type.priority != priority:
                continue
            
            results.append(intel_type.to_dict())
        
        return results
    
    def get_categories(self) -> Dict[str, int]:
        """
        Get all categories and type counts.
        
        Returns:
            Dictionary of category names to type counts
        """
        return {cat: len(types) for cat, types in self.categories.items()}
    
    def get_implementation_status(self) -> Dict[str, Any]:
        """
        Get implementation status summary.
        
        Returns:
            Status summary dictionary
        """
        total = len(self.types)
        implemented = sum(1 for t in self.types.values() if t.is_implemented)
        
        by_priority = defaultdict(int)
        for intel_type in self.types.values():
            if not intel_type.is_implemented:
                by_priority[intel_type.priority] += 1
        
        return {
            'total_types': total,
            'implemented': implemented,
            'unimplemented': total - implemented,
            'percentage_complete': (implemented / total * 100) if total > 0 else 0,
            'unimplemented_by_priority': dict(by_priority),
            'categories': self.get_categories()
        }
    
    def get_usage_stats(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Get usage statistics for intelligence types.
        
        Args:
            top_n: Number of top types to return
            
        Returns:
            List of usage statistics
        """
        sorted_types = sorted(
            self.types.values(),
            key=lambda t: t.usage_count,
            reverse=True
        )
        
        return [
            {
                'name': t.name,
                'category': t.category,
                'usage_count': t.usage_count,
                'is_implemented': t.is_implemented
            }
            for t in sorted_types[:top_n]
        ]
    
    def export_registry(self, output_path: Path):
        """
        Export registry to JSON file.
        
        Args:
            output_path: Path to output JSON file
        """
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'total_types': len(self.types),
            'categories': self.get_categories(),
            'types': {name: intel_type.to_dict() for name, intel_type in self.types.items()},
            'discovery_log': self.discovery_log
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Exported registry to {output_path}")
    
    def generate_stub_handlers(self) -> str:
        """
        Generate Python code for stub handlers.
        
        Returns:
            Python code string
        """
        code_lines = [
            "# Auto-generated stub handlers",
            "# Generated: " + datetime.now().isoformat(),
            "",
            "from typing import Dict, Any",
            "",
        ]
        
        for name, intel_type in self.types.items():
            if not intel_type.is_implemented:
                func_name = f"_handle_{name.replace('-', '_')}"
                code_lines.extend([
                    f"def {func_name}(self, data: Dict[str, Any]) -> Dict[str, Any]:",
                    f'    """',
                    f'    Handle {name} intelligence type.',
                    f'    Category: {intel_type.category}',
                    f'    Source keys: {", ".join(intel_type.source_keys)}',
                    f'    """',
                    f'    return {{',
                    f'        "status": "stub",',
                    f'        "type": "{name}",',
                    f'        "category": "{intel_type.category}",',
                    f'        "message": "{name} - to be implemented",',
                    f'        "schema": {intel_type.schema},',
                    f'        "data_received": list(data.keys())',
                    f'    }}',
                    ""
                ])
        
        return "\n".join(code_lines)


# Global registry instance
_global_registry = None

def get_global_registry() -> IntelligenceTypeRegistry:
    """Get or create global registry instance"""
    global _global_registry
    if _global_registry is None:
        _global_registry = IntelligenceTypeRegistry()
    return _global_registry
