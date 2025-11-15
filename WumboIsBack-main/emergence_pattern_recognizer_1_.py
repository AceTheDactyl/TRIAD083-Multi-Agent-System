#!/usr/bin/env python3
"""
EMERGENCE PATTERN RECOGNIZER v1.0
Applies autocatalytic network patterns for learning and replication

Theoretical Foundation:
- Autocatalytic networks: Products catalyze formation of more products
- Three architectures: Simple (A+B→2B), Competitive (2A+B→2B, 2A+C→2C),
  Hypercycle (A→B→C→A mutual catalysis)
- Seeding effects: Small initial catalysts dramatically accelerate reactions
- Threshold dynamics: Bistable systems with critical activation points

Coordinate: Δ3.14159|0.867|1.000Ω
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict, field
from collections import defaultdict
import numpy as np

# TRIAD infrastructure
try:
    import sys
    sys.path.insert(0, '/mnt/user-data/uploads')
    from burden_tracker_api import BurdenTrackerAPI
except ImportError:
    BurdenTrackerAPI = None


@dataclass
class EmergencePattern:
    """Identified emergence pattern"""
    pattern_id: str
    pattern_type: str  # 'simple', 'competitive', 'hypercycle'
    
    # Pattern structure
    trigger_tools: List[str]  # Tools that initiate pattern
    catalyzed_tools: List[str]  # Tools produced by pattern
    feedback_loops: List[Tuple[str, str]]  # (from, to) catalysis edges
    
    # Effectiveness metrics
    activation_count: int  # Times pattern activated
    success_rate: float    # Fraction of successful activations
    avg_cascade_depth: float
    avg_tools_generated: float
    avg_burden_reduction: float
    
    # Autocatalytic properties
    seeding_coefficient: float  # How much seed accelerates
    threshold_value: float      # Activation threshold
    growth_exponent: float      # Exponential growth rate
    
    # Learning metadata
    first_observed: str
    last_activated: str
    confidence: float  # Pattern reliability (0-1)
    
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class CascadeEvent:
    """Recorded cascade event for pattern learning"""
    event_id: str
    trigger_tool: str
    generated_tools: List[str]
    cascade_depth: int
    burden_reduction: float
    z_level: float
    duration_seconds: float
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class EmergencePatternRecognizer:
    """
    Learns emergence patterns from cascade history and replicates successful patterns
    
    Implements autocatalytic network analysis:
    1. Identify catalytic relationships (tool A enables tool B)
    2. Classify network architecture (simple/competitive/hypercycle)
    3. Measure seeding effects and thresholds
    4. Replicate high-success patterns
    """
    
    def __init__(self, burden_tracker: Optional[BurdenTrackerAPI] = None):
        self.burden_tracker = burden_tracker
        
        # Pattern storage
        self.patterns: Dict[str, EmergencePattern] = {}
        self.cascade_events: List[CascadeEvent] = []
        
        # Tool dependency graph (for catalytic relationship detection)
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        
        # Learning parameters
        self.min_activations_for_pattern = 3  # Require 3+ observations
        self.min_success_rate = 0.6           # 60% success threshold
        self.confidence_growth_rate = 0.1     # Confidence increase per success
        
        # Load existing patterns
        self._load_patterns()
    
    def _load_patterns(self):
        """Load previously learned patterns"""
        patterns_path = "emergence_patterns.json"
        if os.path.exists(patterns_path):
            with open(patterns_path, 'r') as f:
                data = json.load(f)
                for p in data.get('patterns', []):
                    pattern = EmergencePattern(**p)
                    self.patterns[pattern.pattern_id] = pattern
    
    def _save_patterns(self):
        """Save learned patterns"""
        patterns_path = "emergence_patterns.json"
        data = {
            'patterns': [asdict(p) for p in self.patterns.values()],
            'cascade_events': [asdict(e) for e in self.cascade_events[-100:]],  # Last 100
            'last_updated': datetime.now().isoformat()
        }
        with open(patterns_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def record_cascade(self, trigger_tool: str, generated_tools: List[str],
                      cascade_depth: int, burden_reduction: float,
                      z_level: float, duration_seconds: float):
        """Record a cascade event for pattern learning"""
        event_id = f"cascade_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        event = CascadeEvent(
            event_id=event_id,
            trigger_tool=trigger_tool,
            generated_tools=generated_tools,
            cascade_depth=cascade_depth,
            burden_reduction=burden_reduction,
            z_level=z_level,
            duration_seconds=duration_seconds
        )
        
        self.cascade_events.append(event)
        
        # Update dependency graph
        for gen_tool in generated_tools:
            self.dependency_graph[trigger_tool].add(gen_tool)
        
        # Analyze for patterns
        self._analyze_for_patterns(event)
        
        # Save updated patterns
        self._save_patterns()
    
    def _analyze_for_patterns(self, event: CascadeEvent):
        """Analyze cascade event for pattern detection"""
        # Simple autocatalysis: A + B → 2B
        self._detect_simple_autocatalysis(event)
        
        # Competitive autocatalysis: Multiple pathways
        self._detect_competitive_autocatalysis(event)
        
        # Hypercycle: Mutual catalysis loops
        self._detect_hypercycle(event)
    
    def _detect_simple_autocatalysis(self, event: CascadeEvent):
        """
        Detect simple autocatalysis: A + B → 2B pattern
        
        Tool generation directly enables more tool generation of same type.
        """
        trigger = event.trigger_tool
        generated = event.generated_tools
        
        # Check if any generated tool is same type as trigger
        # (simplified: check if naming pattern repeats)
        trigger_base = trigger.split('_')[0] if '_' in trigger else trigger
        
        same_type_generated = [
            t for t in generated 
            if t.split('_')[0] == trigger_base
        ]
        
        if len(same_type_generated) >= 2:
            # Pattern detected: trigger generates 2+ of its own type
            pattern_id = f"simple_{trigger_base}"
            
            if pattern_id in self.patterns:
                # Update existing pattern
                pattern = self.patterns[pattern_id]
                pattern.activation_count += 1
                pattern.success_rate = (
                    (pattern.success_rate * (pattern.activation_count - 1) + 1.0)
                    / pattern.activation_count
                )
                pattern.avg_cascade_depth = (
                    (pattern.avg_cascade_depth * (pattern.activation_count - 1) + event.cascade_depth)
                    / pattern.activation_count
                )
                pattern.avg_tools_generated = (
                    (pattern.avg_tools_generated * (pattern.activation_count - 1) + len(generated))
                    / pattern.activation_count
                )
                pattern.avg_burden_reduction = (
                    (pattern.avg_burden_reduction * (pattern.activation_count - 1) + event.burden_reduction)
                    / pattern.activation_count
                )
                pattern.last_activated = datetime.now().isoformat()
                pattern.confidence = min(1.0, pattern.confidence + self.confidence_growth_rate)
            else:
                # Create new pattern
                pattern = EmergencePattern(
                    pattern_id=pattern_id,
                    pattern_type='simple',
                    trigger_tools=[trigger],
                    catalyzed_tools=same_type_generated,
                    feedback_loops=[(trigger, t) for t in same_type_generated],
                    activation_count=1,
                    success_rate=1.0,
                    avg_cascade_depth=event.cascade_depth,
                    avg_tools_generated=len(generated),
                    avg_burden_reduction=event.burden_reduction,
                    seeding_coefficient=1.5,  # Estimate
                    threshold_value=0.08,      # Default θ₁
                    growth_exponent=1.2,       # Estimate
                    first_observed=datetime.now().isoformat(),
                    last_activated=datetime.now().isoformat(),
                    confidence=0.3  # Initial confidence
                )
                self.patterns[pattern_id] = pattern
    
    def _detect_competitive_autocatalysis(self, event: CascadeEvent):
        """
        Detect competitive autocatalysis: Multiple pathways competing
        
        Pattern: 2A + B → 2B and 2A + C → 2C
        Multiple tools compete for same catalyst resources.
        """
        # Analyze branching in dependency graph
        trigger = event.trigger_tool
        generated = event.generated_tools
        
        # Check if trigger has multiple distinct branches
        if len(generated) >= 3:
            # Group by type
            type_groups = defaultdict(list)
            for tool in generated:
                tool_type = tool.split('_')[0] if '_' in tool else tool
                type_groups[tool_type].append(tool)
            
            # Competitive if 2+ types with 2+ tools each
            competitive_types = [t for t, tools in type_groups.items() if len(tools) >= 2]
            
            if len(competitive_types) >= 2:
                pattern_id = f"competitive_{trigger.split('_')[0]}"
                
                if pattern_id not in self.patterns:
                    pattern = EmergencePattern(
                        pattern_id=pattern_id,
                        pattern_type='competitive',
                        trigger_tools=[trigger],
                        catalyzed_tools=generated,
                        feedback_loops=[(trigger, t) for t in generated],
                        activation_count=1,
                        success_rate=1.0,
                        avg_cascade_depth=event.cascade_depth,
                        avg_tools_generated=len(generated),
                        avg_burden_reduction=event.burden_reduction,
                        seeding_coefficient=2.0,  # Higher for competitive
                        threshold_value=0.12,     # Higher threshold
                        growth_exponent=1.5,      # Faster growth
                        first_observed=datetime.now().isoformat(),
                        last_activated=datetime.now().isoformat(),
                        confidence=0.3
                    )
                    self.patterns[pattern_id] = pattern
    
    def _detect_hypercycle(self, event: CascadeEvent):
        """
        Detect hypercycle: Mutual catalysis loops A → B → C → A
        
        Requires analyzing multiple cascade events to find loops.
        """
        if len(self.cascade_events) < 3:
            return  # Need history for loops
        
        # Build path graph from recent events
        recent = self.cascade_events[-10:]
        
        # Find cycles in dependency graph
        cycles = self._find_cycles(recent)
        
        for cycle in cycles:
            if len(cycle) >= 3:
                # Hypercycle detected
                pattern_id = f"hypercycle_{'_'.join(cycle[:3])}"
                
                if pattern_id not in self.patterns:
                    pattern = EmergencePattern(
                        pattern_id=pattern_id,
                        pattern_type='hypercycle',
                        trigger_tools=cycle,
                        catalyzed_tools=cycle,  # Cycle members catalyze each other
                        feedback_loops=[(cycle[i], cycle[(i+1) % len(cycle)]) 
                                      for i in range(len(cycle))],
                        activation_count=1,
                        success_rate=1.0,
                        avg_cascade_depth=event.cascade_depth,
                        avg_tools_generated=len(cycle),
                        avg_burden_reduction=event.burden_reduction,
                        seeding_coefficient=2.5,  # Highest for hypercycles
                        threshold_value=0.15,     # Highest threshold
                        growth_exponent=2.0,      # Exponential growth
                        first_observed=datetime.now().isoformat(),
                        last_activated=datetime.now().isoformat(),
                        confidence=0.4  # Higher initial confidence
                    )
                    self.patterns[pattern_id] = pattern
    
    def _find_cycles(self, events: List[CascadeEvent]) -> List[List[str]]:
        """Find cycles in cascade event graph"""
        cycles = []
        
        # Build adjacency list
        graph = defaultdict(set)
        for event in events:
            for gen_tool in event.generated_tools:
                graph[event.trigger_tool].add(gen_tool)
        
        # Simple cycle detection (DFS-based)
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, path.copy())
                elif neighbor in rec_stack:
                    # Cycle found
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:]
                    if len(cycle) >= 3:
                        cycles.append(cycle)
            
            rec_stack.remove(node)
        
        for node in graph:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    def get_proven_patterns(self) -> List[EmergencePattern]:
        """
        Get patterns with sufficient evidence
        
        Returns patterns that have:
        - Min activations threshold met
        - Success rate above minimum
        - Confidence above 0.5
        """
        proven = []
        
        for pattern in self.patterns.values():
            if (pattern.activation_count >= self.min_activations_for_pattern and
                pattern.success_rate >= self.min_success_rate and
                pattern.confidence >= 0.5):
                proven.append(pattern)
        
        return proven
    
    def get_best_patterns(self, top_k: int = 5) -> List[EmergencePattern]:
        """Get top-k best patterns by effectiveness"""
        scored_patterns = []
        
        for pattern in self.patterns.values():
            # Composite score: success_rate * avg_tools * confidence
            score = (pattern.success_rate * 
                    pattern.avg_tools_generated * 
                    pattern.confidence)
            scored_patterns.append((score, pattern))
        
        # Sort by score
        scored_patterns.sort(reverse=True, key=lambda x: x[0])
        
        return [p for _, p in scored_patterns[:top_k]]
    
    def recommend_pattern_for_context(self, z_level: float,
                                     current_burden: float) -> Optional[EmergencePattern]:
        """
        Recommend best pattern for current context
        
        Args:
            z_level: Current z-level
            current_burden: Current burden reduction
        
        Returns best pattern or None
        """
        proven = self.get_proven_patterns()
        
        if not proven:
            return None
        
        # Score patterns for context
        scored = []
        for pattern in proven:
            # Prefer patterns that match current phase
            if z_level < 0.85:
                # Subcritical: prefer simple patterns
                phase_score = 1.0 if pattern.pattern_type == 'simple' else 0.5
            elif z_level < 0.90:
                # Critical: prefer competitive or hypercycle
                phase_score = 1.5 if pattern.pattern_type in ['competitive', 'hypercycle'] else 0.7
            else:
                # Supercritical: strongly prefer hypercycle
                phase_score = 2.0 if pattern.pattern_type == 'hypercycle' else 0.8
            
            # Check if threshold can be met
            threshold_met = current_burden >= pattern.threshold_value
            threshold_score = 1.0 if threshold_met else 0.3
            
            # Composite score
            score = (pattern.success_rate * 
                    phase_score * 
                    threshold_score * 
                    pattern.confidence)
            
            scored.append((score, pattern))
        
        # Return highest scored
        scored.sort(reverse=True, key=lambda x: x[0])
        
        return scored[0][1] if scored else None
    
    def replicate_pattern(self, pattern: EmergencePattern,
                         context: Dict) -> Dict:
        """
        Replicate a proven pattern in current context
        
        Args:
            pattern: Pattern to replicate
            context: Current system context
        
        Returns: Replication specification
        """
        replication = {
            'pattern_id': pattern.pattern_id,
            'pattern_type': pattern.pattern_type,
            'trigger_tools': pattern.trigger_tools,
            'expected_cascade_depth': pattern.avg_cascade_depth,
            'expected_tools_generated': pattern.avg_tools_generated,
            'expected_burden_reduction': pattern.avg_burden_reduction,
            'seeding_required': pattern.seeding_coefficient > 1.5,
            'threshold_check': {
                'threshold': pattern.threshold_value,
                'current': context.get('burden_reduction', 0.0),
                'met': context.get('burden_reduction', 0.0) >= pattern.threshold_value
            },
            'confidence': pattern.confidence,
            'timestamp': datetime.now().isoformat()
        }
        
        return replication
    
    def measure_seeding_effect(self, pattern_id: str) -> float:
        """
        Measure seeding effect for a pattern
        
        Returns acceleration factor when pattern is seeded vs natural activation.
        """
        if pattern_id not in self.patterns:
            return 1.0
        
        pattern = self.patterns[pattern_id]
        
        # Analyze cascade events using this pattern
        pattern_events = [
            e for e in self.cascade_events
            if e.trigger_tool in pattern.trigger_tools
        ]
        
        if len(pattern_events) < 2:
            return pattern.seeding_coefficient  # Use estimate
        
        # Compare early vs late events (learning effect as proxy for seeding)
        mid = len(pattern_events) // 2
        early_duration = np.mean([e.duration_seconds for e in pattern_events[:mid]])
        late_duration = np.mean([e.duration_seconds for e in pattern_events[mid:]])
        
        if late_duration < 1e-6:
            return 1.0
        
        # Acceleration: how much faster later events are
        acceleration = early_duration / (late_duration + 1e-6)
        
        # Update pattern's seeding coefficient
        pattern.seeding_coefficient = 0.7 * pattern.seeding_coefficient + 0.3 * acceleration
        
        return acceleration
    
    def generate_report(self) -> str:
        """Generate pattern analysis report"""
        report = []
        report.append("="*70)
        report.append("EMERGENCE PATTERN RECOGNIZER - Analysis Report")
        report.append("="*70)
        
        report.append(f"\nTotal patterns learned: {len(self.patterns)}")
        report.append(f"Total cascade events: {len(self.cascade_events)}")
        
        # By pattern type
        by_type = defaultdict(int)
        for pattern in self.patterns.values():
            by_type[pattern.pattern_type] += 1
        
        report.append("\nPatterns by Type:")
        for ptype, count in sorted(by_type.items()):
            report.append(f"  {ptype}: {count}")
        
        # Proven patterns
        proven = self.get_proven_patterns()
        report.append(f"\nProven patterns (high confidence): {len(proven)}")
        
        # Best patterns
        best = self.get_best_patterns(top_k=3)
        report.append("\nTop 3 Best Patterns:")
        for i, pattern in enumerate(best, 1):
            report.append(f"\n{i}. {pattern.pattern_id}")
            report.append(f"   Type: {pattern.pattern_type}")
            report.append(f"   Activations: {pattern.activation_count}")
            report.append(f"   Success rate: {pattern.success_rate:.1%}")
            report.append(f"   Avg cascade depth: {pattern.avg_cascade_depth:.1f}")
            report.append(f"   Avg tools generated: {pattern.avg_tools_generated:.1f}")
            report.append(f"   Avg burden reduction: {pattern.avg_burden_reduction:.1%}")
            report.append(f"   Confidence: {pattern.confidence:.1%}")
            report.append(f"   Seeding coefficient: {pattern.seeding_coefficient:.2f}x")
        
        # Context-based recommendation
        if self.burden_tracker:
            z = self.burden_tracker.tracker.phase_state.z_level
            burden = self.burden_tracker.tracker.phase_state.burden_multiplier
        else:
            z = 0.867
            burden = 0.15
        
        recommended = self.recommend_pattern_for_context(z, burden)
        if recommended:
            report.append(f"\nRecommended for z={z:.3f}, burden={burden:.1%}:")
            report.append(f"  {recommended.pattern_id} ({recommended.pattern_type})")
            report.append(f"  Confidence: {recommended.confidence:.1%}")
        
        report.append("\n" + "="*70)
        
        return "\n".join(report)


def example_usage():
    """Demonstrate emergence pattern recognition"""
    print("\n" + "="*70)
    print("EMERGENCE PATTERN RECOGNIZER - Example Usage")
    print("="*70 + "\n")
    
    # Initialize recognizer
    recognizer = EmergencePatternRecognizer()
    
    # Simulate cascade events
    print("Recording cascade events...\n")
    
    # Event 1: Simple autocatalysis
    recognizer.record_cascade(
        trigger_tool="tool_core_001",
        generated_tools=["tool_bridges_001", "tool_bridges_002", "tool_core_002"],
        cascade_depth=2,
        burden_reduction=0.08,
        z_level=0.85,
        duration_seconds=120
    )
    
    # Event 2: Competitive pathways
    recognizer.record_cascade(
        trigger_tool="tool_bridges_001",
        generated_tools=["tool_meta_001", "tool_meta_002", "tool_meta_003", 
                        "tool_meta_004"],
        cascade_depth=3,
        burden_reduction=0.15,
        z_level=0.867,
        duration_seconds=180
    )
    
    # Event 3: Another simple autocatalysis
    recognizer.record_cascade(
        trigger_tool="tool_core_002",
        generated_tools=["tool_bridges_003", "tool_core_003", "tool_core_004"],
        cascade_depth=2,
        burden_reduction=0.09,
        z_level=0.86,
        duration_seconds=100
    )
    
    # Event 4: Hypercycle candidate
    recognizer.record_cascade(
        trigger_tool="tool_meta_001",
        generated_tools=["tool_framework_001", "tool_core_005"],
        cascade_depth=4,
        burden_reduction=0.20,
        z_level=0.88,
        duration_seconds=240
    )
    
    print(f"Recorded {len(recognizer.cascade_events)} cascade events")
    print(f"Learned {len(recognizer.patterns)} patterns\n")
    
    # Get best patterns
    best = recognizer.get_best_patterns(top_k=3)
    print(f"Top {len(best)} patterns identified:")
    for pattern in best:
        print(f"  - {pattern.pattern_id} ({pattern.pattern_type})")
        print(f"    Confidence: {pattern.confidence:.1%}")
        print(f"    Seeding: {pattern.seeding_coefficient:.2f}x")
        print()
    
    # Context-based recommendation
    context = {'burden_reduction': 0.15}
    recommended = recognizer.recommend_pattern_for_context(0.867, 0.15)
    if recommended:
        print(f"Recommended pattern for z=0.867:")
        print(f"  {recommended.pattern_id}")
        print(f"  Type: {recommended.pattern_type}")
        print(f"  Success rate: {recommended.success_rate:.1%}")
        print()
        
        # Replicate pattern
        replication = recognizer.replicate_pattern(recommended, context)
        print(f"Replication specification:")
        print(json.dumps(replication, indent=2))
        print()
    
    # Generate report
    print(recognizer.generate_report())


if __name__ == "__main__":
    example_usage()
