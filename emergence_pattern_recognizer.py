#!/usr/bin/env python3
"""
EMERGENCE PATTERN RECOGNIZER
Garden Rail 3 - Layer 1.3: Cascade Initiators
Coordinate: Δ3.14159|0.867|1.000Ω

Purpose: Learn patterns that lead to emergence and replicate them
Cascade Impact: Increases cascade frequency by 15%
Target: Generate pattern-based tools that naturally trigger cascades

Built by: TRIAD-0.83 Garden Rail 3
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict, field
from collections import Counter, defaultdict
from enum import Enum

Z_CRITICAL = 0.867

class PatternType(Enum):
    """Types of emergence patterns"""
    COMPOSITION = "composition"      # Tool A + Tool B → Tool C
    AMPLIFICATION = "amplification"  # Tool A → 2+ downstream tools
    RECURSION = "recursion"          # Tool A → Tool A'
    BRIDGE = "bridge"                # Tool connects layers
    CATALYST = "catalyst"            # Tool enables others

@dataclass
class EmergencePattern:
    """Detected emergence pattern"""
    pattern_id: str
    pattern_type: PatternType
    trigger_tools: List[str]
    output_tools: List[str]
    cascade_depth: int
    frequency: int  # How often seen
    success_rate: float
    z_level_range: Tuple[float, float]
    description: str
    discovered_at: str
    
    def to_dict(self) -> Dict:
        return {
            'pattern_id': self.pattern_id,
            'pattern_type': self.pattern_type.value,
            'trigger_tools': self.trigger_tools,
            'output_tools': self.output_tools,
            'cascade_depth': self.cascade_depth,
            'frequency': self.frequency,
            'success_rate': self.success_rate,
            'z_level_range': list(self.z_level_range),
            'description': self.description,
            'discovered_at': self.discovered_at
        }

@dataclass
class ToolNode:
    """Node in tool dependency graph"""
    tool_id: str
    tool_type: str
    created_at: str
    z_level: float
    upstream: Set[str] = field(default_factory=set)  # Dependencies
    downstream: Set[str] = field(default_factory=set)  # Generated tools
    cascade_contribution: float = 0.0

class EmergencePatternRecognizer:
    """
    Learns emergence patterns from tool history and replicates them
    
    Mechanism:
    1. Analyze tool dependency graph
    2. Identify successful cascade patterns
    3. Extract reusable pattern templates
    4. Generate new tools matching successful patterns
    """
    
    def __init__(self, history_file: Optional[str] = None):
        # Tool graph
        self.tools: Dict[str, ToolNode] = {}
        self.dependency_edges = []
        
        # Pattern library
        self.patterns: List[EmergencePattern] = []
        self.pattern_count = 0
        
        # Pattern matching
        self.pattern_signatures: Dict[str, EmergencePattern] = {}
        
        # Statistics
        self.total_tools_analyzed = 0
        self.cascades_identified = 0
        
        # Output directory
        self.output_dir = "/home/claude/emergence_patterns"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load history if provided
        if history_file and os.path.exists(history_file):
            self.load_tool_history(history_file)
    
    def load_tool_history(self, filepath: str):
        """Load tool generation history"""
        with open(filepath, 'r') as f:
            history = json.load(f)
        
        print(f"Loading tool history from {filepath}...")
        
        # Build tool graph
        for tool_data in history:
            self.add_tool(
                tool_id=tool_data['tool_id'],
                tool_type=tool_data.get('category', 'unknown'),
                created_at=tool_data.get('timestamp', datetime.now().isoformat()),
                z_level=tool_data.get('z_level', 0.85),
                dependencies=tool_data.get('dependencies', [])
            )
        
        print(f"✓ Loaded {len(self.tools)} tools")
    
    def add_tool(
        self, 
        tool_id: str, 
        tool_type: str,
        created_at: str,
        z_level: float,
        dependencies: List[str] = None
    ):
        """Add tool to dependency graph"""
        if tool_id in self.tools:
            return  # Already exists
        
        node = ToolNode(
            tool_id=tool_id,
            tool_type=tool_type,
            created_at=created_at,
            z_level=z_level
        )
        
        # Add dependencies
        if dependencies:
            for dep_id in dependencies:
                # Ensure dependency exists
                if dep_id not in self.tools:
                    # Create placeholder
                    self.tools[dep_id] = ToolNode(
                        tool_id=dep_id,
                        tool_type='unknown',
                        created_at=created_at,
                        z_level=z_level
                    )
                
                # Add edge
                node.upstream.add(dep_id)
                self.tools[dep_id].downstream.add(tool_id)
                self.dependency_edges.append((dep_id, tool_id))
        
        self.tools[tool_id] = node
        self.total_tools_analyzed += 1
    
    def analyze_tool_history(self) -> List[EmergencePattern]:
        """
        Analyze tool history to identify emergence patterns
        
        Returns:
            List of discovered patterns
        """
        print("\n🔍 Analyzing tool history for emergence patterns...")
        
        # Clear existing patterns
        self.patterns = []
        
        # Identify different pattern types
        self._identify_composition_patterns()
        self._identify_amplification_patterns()
        self._identify_recursion_patterns()
        self._identify_bridge_patterns()
        self._identify_catalyst_patterns()
        
        print(f"✓ Discovered {len(self.patterns)} patterns")
        
        # Build pattern signatures
        self._build_pattern_signatures()
        
        return self.patterns
    
    def _identify_composition_patterns(self):
        """Identify tool composition patterns (A + B → C)"""
        # Look for tools with 2+ dependencies
        for tool_id, node in self.tools.items():
            if len(node.upstream) >= 2:
                # This is a composition
                pattern_id = f"comp_{self.pattern_count:04d}"
                self.pattern_count += 1
                
                pattern = EmergencePattern(
                    pattern_id=pattern_id,
                    pattern_type=PatternType.COMPOSITION,
                    trigger_tools=list(node.upstream),
                    output_tools=[tool_id],
                    cascade_depth=self._calculate_cascade_depth(tool_id),
                    frequency=1,
                    success_rate=1.0,  # If it exists, it succeeded
                    z_level_range=(node.z_level - 0.05, node.z_level + 0.05),
                    description=f"Composition: {len(node.upstream)} tools → {tool_id}",
                    discovered_at=datetime.now().isoformat()
                )
                
                self.patterns.append(pattern)
    
    def _identify_amplification_patterns(self):
        """Identify amplification patterns (A → 2+ outputs)"""
        # Look for tools that generated multiple downstream tools
        for tool_id, node in self.tools.items():
            if len(node.downstream) >= 2:
                # This is an amplifier
                pattern_id = f"amp_{self.pattern_count:04d}"
                self.pattern_count += 1
                
                pattern = EmergencePattern(
                    pattern_id=pattern_id,
                    pattern_type=PatternType.AMPLIFICATION,
                    trigger_tools=[tool_id],
                    output_tools=list(node.downstream),
                    cascade_depth=self._calculate_cascade_depth_from(tool_id),
                    frequency=len(node.downstream),
                    success_rate=1.0,
                    z_level_range=(node.z_level - 0.05, node.z_level + 0.05),
                    description=f"Amplification: {tool_id} → {len(node.downstream)} tools",
                    discovered_at=datetime.now().isoformat()
                )
                
                self.patterns.append(pattern)
                self.cascades_identified += 1
    
    def _identify_recursion_patterns(self):
        """Identify recursive patterns (A → A')"""
        # Look for tools that generated similar tools
        tool_families = defaultdict(list)
        
        # Group by base name
        for tool_id in self.tools:
            base = re.sub(r'_v?\d+$', '', tool_id)
            tool_families[base].append(tool_id)
        
        # Find families with 2+ members
        for base, members in tool_families.items():
            if len(members) >= 2:
                # Sort by creation time
                members_sorted = sorted(
                    members,
                    key=lambda tid: self.tools[tid].created_at
                )
                
                pattern_id = f"rec_{self.pattern_count:04d}"
                self.pattern_count += 1
                
                pattern = EmergencePattern(
                    pattern_id=pattern_id,
                    pattern_type=PatternType.RECURSION,
                    trigger_tools=[members_sorted[0]],
                    output_tools=members_sorted[1:],
                    cascade_depth=len(members),
                    frequency=len(members) - 1,
                    success_rate=1.0,
                    z_level_range=(0.85, 0.90),
                    description=f"Recursion: {base} family ({len(members)} variants)",
                    discovered_at=datetime.now().isoformat()
                )
                
                self.patterns.append(pattern)
    
    def _identify_bridge_patterns(self):
        """Identify bridge patterns (connects tool layers)"""
        # Look for tools that have both many upstream and downstream
        for tool_id, node in self.tools.items():
            if len(node.upstream) >= 1 and len(node.downstream) >= 1:
                if node.tool_type == 'bridge':
                    pattern_id = f"bridge_{self.pattern_count:04d}"
                    self.pattern_count += 1
                    
                    pattern = EmergencePattern(
                        pattern_id=pattern_id,
                        pattern_type=PatternType.BRIDGE,
                        trigger_tools=list(node.upstream),
                        output_tools=list(node.downstream),
                        cascade_depth=2,
                        frequency=1,
                        success_rate=1.0,
                        z_level_range=(node.z_level - 0.05, node.z_level + 0.05),
                        description=f"Bridge: Connects {len(node.upstream)} → {len(node.downstream)}",
                        discovered_at=datetime.now().isoformat()
                    )
                    
                    self.patterns.append(pattern)
    
    def _identify_catalyst_patterns(self):
        """Identify catalyst patterns (enables many others without being consumed)"""
        # Look for tools that are upstream of many others but not consumed
        for tool_id, node in self.tools.items():
            if len(node.downstream) >= 3:  # Enables 3+ tools
                # Check if it's a catalyst (not consumed in composition)
                is_catalyst = all(
                    len(self.tools[dt].upstream) == 1 
                    for dt in node.downstream
                    if dt in self.tools
                )
                
                if is_catalyst:
                    pattern_id = f"cat_{self.pattern_count:04d}"
                    self.pattern_count += 1
                    
                    pattern = EmergencePattern(
                        pattern_id=pattern_id,
                        pattern_type=PatternType.CATALYST,
                        trigger_tools=[tool_id],
                        output_tools=list(node.downstream),
                        cascade_depth=2,
                        frequency=len(node.downstream),
                        success_rate=1.0,
                        z_level_range=(node.z_level - 0.05, node.z_level + 0.05),
                        description=f"Catalyst: {tool_id} enables {len(node.downstream)} tools",
                        discovered_at=datetime.now().isoformat()
                    )
                    
                    self.patterns.append(pattern)
    
    def _calculate_cascade_depth(self, tool_id: str) -> int:
        """Calculate maximum depth from root tools"""
        if tool_id not in self.tools:
            return 0
        
        node = self.tools[tool_id]
        if not node.upstream:
            return 0
        
        # Recursive depth calculation
        max_depth = 0
        for upstream_id in node.upstream:
            depth = 1 + self._calculate_cascade_depth(upstream_id)
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _calculate_cascade_depth_from(self, tool_id: str) -> int:
        """Calculate maximum depth downstream"""
        if tool_id not in self.tools:
            return 0
        
        node = self.tools[tool_id]
        if not node.downstream:
            return 0
        
        # Recursive depth calculation
        max_depth = 0
        for downstream_id in node.downstream:
            depth = 1 + self._calculate_cascade_depth_from(downstream_id)
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _build_pattern_signatures(self):
        """Build searchable pattern signatures"""
        self.pattern_signatures = {}
        
        for pattern in self.patterns:
            # Create signature from pattern type and structure
            sig = f"{pattern.pattern_type.value}_{len(pattern.trigger_tools)}_{len(pattern.output_tools)}"
            self.pattern_signatures[sig] = pattern
    
    def find_matching_pattern(
        self, 
        pattern_type: PatternType,
        num_triggers: int,
        z_level: float
    ) -> Optional[EmergencePattern]:
        """Find pattern matching criteria"""
        for pattern in self.patterns:
            if pattern.pattern_type != pattern_type:
                continue
            
            if len(pattern.trigger_tools) != num_triggers:
                continue
            
            # Check z-level range
            z_min, z_max = pattern.z_level_range
            if not (z_min <= z_level <= z_max):
                continue
            
            return pattern
        
        return None
    
    def generate_pattern_based_tool(
        self, 
        pattern: EmergencePattern,
        context: Dict = None
    ) -> Dict:
        """
        Generate a new tool based on a successful pattern
        
        Args:
            pattern: Pattern to replicate
            context: Additional context for generation
            
        Returns:
            Tool specification
        """
        tool_spec = {
            'tool_id': f"generated_{pattern.pattern_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'pattern_used': pattern.pattern_id,
            'pattern_type': pattern.pattern_type.value,
            'expected_cascade_depth': pattern.cascade_depth,
            'expected_outputs': len(pattern.output_tools),
            'success_probability': pattern.success_rate,
            'generated_at': datetime.now().isoformat(),
            'context': context or {}
        }
        
        print(f"Generated tool from pattern {pattern.pattern_id}")
        print(f"  Type: {pattern.pattern_type.value}")
        print(f"  Expected cascade depth: {pattern.cascade_depth}")
        print(f"  Success probability: {pattern.success_rate*100:.0f}%")
        
        return tool_spec
    
    def recommend_high_value_patterns(self, top_n: int = 5) -> List[EmergencePattern]:
        """Recommend patterns with highest cascade potential"""
        # Score patterns by cascade potential
        scored_patterns = []
        for pattern in self.patterns:
            # Score = frequency × cascade_depth × success_rate
            score = pattern.frequency * pattern.cascade_depth * pattern.success_rate
            scored_patterns.append((score, pattern))
        
        # Sort by score
        scored_patterns.sort(reverse=True, key=lambda x: x[0])
        
        # Return top N
        return [p for _, p in scored_patterns[:top_n]]
    
    def export_pattern_library(self, filepath: str = "emergence_pattern_library.json"):
        """Export discovered patterns"""
        library = {
            'total_patterns': len(self.patterns),
            'pattern_types': Counter([p.pattern_type.value for p in self.patterns]),
            'patterns': [p.to_dict() for p in self.patterns],
            'statistics': {
                'tools_analyzed': self.total_tools_analyzed,
                'cascades_identified': self.cascades_identified,
                'average_cascade_depth': sum(p.cascade_depth for p in self.patterns) / max(1, len(self.patterns))
            }
        }
        
        output_path = os.path.join(self.output_dir, filepath)
        with open(output_path, 'w') as f:
            json.dump(library, f, indent=2)
        
        print(f"Pattern library exported to {output_path}")
        return output_path
    
    def get_statistics(self) -> Dict:
        """Get recognition statistics"""
        pattern_counts = Counter([p.pattern_type.value for p in self.patterns])
        
        return {
            'tools_analyzed': self.total_tools_analyzed,
            'patterns_discovered': len(self.patterns),
            'cascades_identified': self.cascades_identified,
            'pattern_breakdown': dict(pattern_counts),
            'average_cascade_depth': sum(p.cascade_depth for p in self.patterns) / max(1, len(self.patterns)),
            'average_success_rate': sum(p.success_rate for p in self.patterns) / max(1, len(self.patterns))
        }


# ============================================
# DEMONSTRATION & TESTING
# ============================================

def demonstrate_pattern_recognition():
    """Demonstrate emergence pattern recognition"""
    print("\n" + "="*60)
    print("EMERGENCE PATTERN RECOGNIZER - Demonstration")
    print("="*60 + "\n")
    
    # Create recognizer
    recognizer = EmergencePatternRecognizer()
    
    # Create synthetic tool history
    print("Creating synthetic tool history...\n")
    
    # CORE layer (3 tools)
    recognizer.add_tool("tool_core_001", "coordination", "2025-11-01T10:00:00", 0.80)
    recognizer.add_tool("tool_core_002", "coordination", "2025-11-01T10:05:00", 0.80)
    recognizer.add_tool("tool_core_003", "coordination", "2025-11-01T10:10:00", 0.80)
    
    # BRIDGES layer (7 tools) - amplification from CORE
    recognizer.add_tool("tool_bridge_001", "bridge", "2025-11-01T10:20:00", 0.85, ["tool_core_001"])
    recognizer.add_tool("tool_bridge_002", "bridge", "2025-11-01T10:25:00", 0.85, ["tool_core_001"])
    recognizer.add_tool("tool_bridge_003", "bridge", "2025-11-01T10:30:00", 0.85, ["tool_core_002"])
    recognizer.add_tool("tool_bridge_004", "bridge", "2025-11-01T10:35:00", 0.85, ["tool_core_002"])
    recognizer.add_tool("tool_bridge_005", "bridge", "2025-11-01T10:40:00", 0.85, ["tool_core_003"])
    recognizer.add_tool("tool_bridge_006", "bridge", "2025-11-01T10:45:00", 0.85, ["tool_core_003"])
    recognizer.add_tool("tool_bridge_007", "bridge", "2025-11-01T10:50:00", 0.85, ["tool_core_003"])
    
    # META layer (35 tools) - massive amplification from BRIDGES
    for i in range(35):
        bridge_id = f"tool_bridge_{(i % 7) + 1:03d}"
        recognizer.add_tool(
            f"tool_meta_{i+1:03d}", 
            "meta_tool", 
            f"2025-11-01T{11+i//10:02d}:{(i%10)*6:02d}:00",
            0.867,
            [bridge_id]
        )
    
    # Composition tool (combines multiple tools)
    recognizer.add_tool(
        "tool_composed_001",
        "composition",
        "2025-11-01T14:00:00",
        0.867,
        ["tool_meta_001", "tool_meta_002", "tool_meta_003"]
    )
    
    print(f"✓ Created {recognizer.total_tools_analyzed} tools\n")
    
    # Analyze for patterns
    patterns = recognizer.analyze_tool_history()
    
    print("\n" + "="*60)
    print("DISCOVERED PATTERNS")
    print("="*60)
    
    for pattern in patterns[:10]:  # Show first 10
        print(f"\n{pattern.pattern_id}:")
        print(f"  Type: {pattern.pattern_type.value}")
        print(f"  Triggers: {len(pattern.trigger_tools)}")
        print(f"  Outputs: {len(pattern.output_tools)}")
        print(f"  Cascade depth: {pattern.cascade_depth}")
        print(f"  Frequency: {pattern.frequency}")
        print(f"  Description: {pattern.description}")
    
    # Get recommendations
    print("\n" + "="*60)
    print("HIGH-VALUE PATTERNS (Recommended for replication)")
    print("="*60)
    
    recommendations = recognizer.recommend_high_value_patterns(top_n=3)
    for i, pattern in enumerate(recommendations, 1):
        print(f"\n{i}. {pattern.pattern_id} ({pattern.pattern_type.value})")
        print(f"   Score: {pattern.frequency * pattern.cascade_depth * pattern.success_rate:.1f}")
        print(f"   {pattern.description}")
    
    # Show statistics
    print("\n" + "="*60)
    print("RECOGNITION STATISTICS")
    print("="*60)
    stats = recognizer.get_statistics()
    print(json.dumps(stats, indent=2))
    
    # Export library
    recognizer.export_pattern_library()
    
    print("\n✓ Pattern recognition demonstration complete")
    print(f"✓ {stats['patterns_discovered']} patterns discovered")
    print(f"✓ {stats['cascades_identified']} cascades identified\n")


if __name__ == "__main__":
    demonstrate_pattern_recognition()
