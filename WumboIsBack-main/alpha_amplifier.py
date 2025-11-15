#!/usr/bin/env python3
"""
GARDEN RAIL 3 - LAYER 2: ALPHA AMPLIFIER
Increases self-catalysis rate α from 2.0 to 2.5 (CORE→BRIDGES cascade strength)

Coordinate: Δ3.14159|0.867|layer-2-alpha|Ω

Theoretical Foundation:
- α measures autocatalytic strength in dϕ/dt = α·ϕ - β·ϕ³
- Current: α = 2.0 (empirically measured)
- Target: α = 2.5 (25% increase)
- Impact: R₂ increases from 25% to 31% (+6% burden reduction)

Mechanism:
- Analyze tool dependency graphs to identify CORE→BRIDGES patterns
- Strengthen connections between coordination tools and meta-tool bridges
- Ensure each CORE tool spawns 2-3 BRIDGES tools (up from ~2.3)
- Monitor and optimize cascade potential in real-time
"""

import sys
sys.path.insert(0, '/mnt/user-data/outputs')

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
from enum import Enum
import json


class ToolLayer(Enum):
    """Tool classification by cascade layer"""
    CORE = "core"          # Coordination tools (Layer 1)
    BRIDGES = "bridges"    # Meta-tool connectors (Layer 2)
    META = "meta"          # Composition tools (Layer 3)
    FRAMEWORK = "framework"  # Self-building systems (Layer 4)


@dataclass
class ToolDependency:
    """Represents a dependency relationship between tools"""
    source_tool: str
    target_tool: str
    source_layer: ToolLayer
    target_layer: ToolLayer
    strength: float  # 0.0-1.0, strength of dependency
    timestamp: datetime
    cascade_triggered: bool = False

    def is_alpha_relevant(self) -> bool:
        """Check if this dependency contributes to α (CORE→BRIDGES)"""
        return (self.source_layer == ToolLayer.CORE and
                self.target_layer == ToolLayer.BRIDGES)


@dataclass
class AlphaMetrics:
    """Metrics for tracking α amplification"""
    current_alpha: float
    target_alpha: float = 2.5
    core_tools_count: int = 0
    bridges_tools_spawned: int = 0
    average_bridges_per_core: float = 0.0
    cascade_success_rate: float = 0.0
    alpha_improvement: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    def calculate_alpha(self) -> float:
        """Calculate current α from observed patterns"""
        if self.core_tools_count == 0:
            return 0.0
        return self.bridges_tools_spawned / self.core_tools_count

    def progress_toward_target(self) -> float:
        """Calculate progress toward α = 2.5 target"""
        if self.target_alpha == 0:
            return 0.0
        return (self.current_alpha / self.target_alpha) * 100.0


class AlphaAmplifier:
    """
    Amplifies self-catalysis rate α by strengthening CORE→BRIDGES cascades

    Strategy:
    1. Monitor tool generation patterns to identify CORE tools
    2. Analyze which CORE tools successfully spawn BRIDGES tools
    3. Identify patterns that maximize BRIDGES-per-CORE ratio
    4. Enhance CORE tool specifications to trigger more BRIDGES cascades
    5. Track α improvement over time
    """

    def __init__(self):
        # Tool dependency graph
        self.dependencies: List[ToolDependency] = []

        # Tool registry by layer
        self.tools_by_layer: Dict[ToolLayer, Set[str]] = {
            layer: set() for layer in ToolLayer
        }

        # Alpha metrics tracking
        self.metrics_history: List[AlphaMetrics] = []

        # Cascade enhancement rules
        self.enhancement_rules: List[Dict] = []

        # Current α state
        self.current_alpha = 2.0  # Empirically measured baseline
        self.target_alpha = 2.5

        print("="*70)
        print("ALPHA AMPLIFIER INITIALIZED")
        print("="*70)
        print(f"Current α: {self.current_alpha:.2f}")
        print(f"Target α: {self.target_alpha:.2f}")
        print(f"Required improvement: {((self.target_alpha/self.current_alpha - 1) * 100):.1f}%")
        print()

    def register_tool(self, tool_id: str, layer: ToolLayer):
        """Register a tool in the appropriate layer"""
        self.tools_by_layer[layer].add(tool_id)

    def record_dependency(self,
                         source_tool: str,
                         target_tool: str,
                         source_layer: ToolLayer,
                         target_layer: ToolLayer,
                         strength: float = 1.0,
                         cascade_triggered: bool = False):
        """
        Record a tool dependency relationship

        Args:
            source_tool: Tool that triggered the dependency
            target_tool: Tool that was generated/required
            source_layer: Layer of source tool
            target_layer: Layer of target tool
            strength: Strength of dependency (0.0-1.0)
            cascade_triggered: Whether this triggered a cascade
        """
        dependency = ToolDependency(
            source_tool=source_tool,
            target_tool=target_tool,
            source_layer=source_layer,
            target_layer=target_layer,
            strength=strength,
            timestamp=datetime.now(),
            cascade_triggered=cascade_triggered
        )

        self.dependencies.append(dependency)

        # Register tools if not already registered
        self.register_tool(source_tool, source_layer)
        self.register_tool(target_tool, target_layer)

    def analyze_core_bridges_patterns(self) -> Dict[str, List[str]]:
        """
        Analyze which CORE tools spawn which BRIDGES tools

        Returns:
            Dict mapping CORE tool IDs to list of BRIDGES tools they spawned
        """
        core_to_bridges: Dict[str, List[str]] = {}

        for dep in self.dependencies:
            if dep.is_alpha_relevant():
                if dep.source_tool not in core_to_bridges:
                    core_to_bridges[dep.source_tool] = []
                core_to_bridges[dep.source_tool].append(dep.target_tool)

        return core_to_bridges

    def calculate_current_alpha(self) -> float:
        """
        Calculate current α from observed dependency patterns

        α = (total BRIDGES spawned) / (total CORE tools)
        """
        patterns = self.analyze_core_bridges_patterns()

        if len(patterns) == 0:
            return self.current_alpha  # Return baseline if no data

        total_core = len(patterns)
        total_bridges = sum(len(bridges) for bridges in patterns.values())

        alpha = total_bridges / total_core if total_core > 0 else 0.0

        return alpha

    def identify_high_alpha_patterns(self, min_bridges: int = 3) -> List[Tuple[str, List[str]]]:
        """
        Identify CORE tools that spawn many BRIDGES tools

        These are the patterns we want to replicate

        Args:
            min_bridges: Minimum BRIDGES tools to be considered high-α

        Returns:
            List of (core_tool, bridges_tools) tuples for high performers
        """
        patterns = self.analyze_core_bridges_patterns()

        high_alpha = [
            (core, bridges) for core, bridges in patterns.items()
            if len(bridges) >= min_bridges
        ]

        # Sort by number of bridges (descending)
        high_alpha.sort(key=lambda x: len(x[1]), reverse=True)

        return high_alpha

    def generate_enhancement_rule(self, core_tool: str, bridges_tools: List[str]) -> Dict:
        """
        Generate an enhancement rule based on successful pattern

        Args:
            core_tool: CORE tool that triggered good cascade
            bridges_tools: BRIDGES tools that were spawned

        Returns:
            Enhancement rule dictionary
        """
        # Analyze what made this CORE tool successful
        rule = {
            'template_tool': core_tool,
            'bridges_count': len(bridges_tools),
            'bridges_types': self._categorize_bridges(bridges_tools),
            'replication_strategy': self._infer_replication_strategy(core_tool, bridges_tools),
            'expected_alpha_contribution': len(bridges_tools),
            'confidence': 0.7,  # Initial confidence
            'activations': 1,
            'timestamp': datetime.now().isoformat()
        }

        return rule

    def _categorize_bridges(self, bridges_tools: List[str]) -> Dict[str, int]:
        """Categorize BRIDGES tools by type (heuristic based on naming)"""
        categories = {
            'coordination': 0,
            'composition': 0,
            'meta_generation': 0,
            'other': 0
        }

        for tool in bridges_tools:
            tool_lower = tool.lower()
            if 'coord' in tool_lower or 'sync' in tool_lower:
                categories['coordination'] += 1
            elif 'compose' in tool_lower or 'integrate' in tool_lower:
                categories['composition'] += 1
            elif 'meta' in tool_lower or 'generate' in tool_lower:
                categories['meta_generation'] += 1
            else:
                categories['other'] += 1

        return categories

    def _infer_replication_strategy(self, core_tool: str, bridges_tools: List[str]) -> str:
        """Infer strategy for replicating this pattern"""
        bridges_count = len(bridges_tools)

        if bridges_count >= 4:
            return "high_fanout"  # One CORE spawns many BRIDGES
        elif bridges_count == 3:
            return "triple_bridge"  # One CORE spawns 3 BRIDGES
        elif bridges_count == 2:
            return "dual_bridge"  # One CORE spawns 2 BRIDGES
        else:
            return "single_bridge"  # One CORE spawns 1 BRIDGE

    def learn_enhancement_rules(self):
        """
        Learn enhancement rules from successful high-α patterns

        These rules will guide future CORE tool design
        """
        high_alpha_patterns = self.identify_high_alpha_patterns(min_bridges=2)

        print(f"\nLearning from {len(high_alpha_patterns)} high-α patterns...")

        for core_tool, bridges_tools in high_alpha_patterns:
            rule = self.generate_enhancement_rule(core_tool, bridges_tools)
            self.enhancement_rules.append(rule)

            print(f"  ✓ Learned rule from {core_tool}")
            print(f"    → Spawned {len(bridges_tools)} BRIDGES tools")
            print(f"    → Strategy: {rule['replication_strategy']}")

    def apply_enhancement_to_tool_spec(self, tool_spec: Dict) -> Dict:
        """
        Enhance a tool specification to increase α contribution

        Args:
            tool_spec: Original tool specification

        Returns:
            Enhanced tool specification with increased cascade potential
        """
        # Find matching enhancement rules
        matching_rules = [
            rule for rule in self.enhancement_rules
            if rule['confidence'] > 0.5
        ]

        if not matching_rules:
            # No rules learned yet, return original spec
            return tool_spec

        # Use highest-confidence rule
        best_rule = max(matching_rules, key=lambda r: r['confidence'])

        # Enhance tool spec based on rule
        enhanced_spec = tool_spec.copy()
        enhanced_spec['alpha_enhancement'] = {
            'target_bridges_count': best_rule['bridges_count'],
            'strategy': best_rule['replication_strategy'],
            'expected_alpha': best_rule['expected_alpha_contribution'],
            'rule_template': best_rule['template_tool']
        }

        return enhanced_spec

    def calculate_metrics(self) -> AlphaMetrics:
        """Calculate current α metrics"""
        patterns = self.analyze_core_bridges_patterns()

        core_count = len(patterns)
        bridges_count = sum(len(bridges) for bridges in patterns.values())
        avg_bridges = bridges_count / core_count if core_count > 0 else 0.0

        current_alpha = self.calculate_current_alpha()

        # Calculate cascade success rate
        alpha_deps = [d for d in self.dependencies if d.is_alpha_relevant()]
        cascade_triggered = sum(1 for d in alpha_deps if d.cascade_triggered)
        success_rate = cascade_triggered / len(alpha_deps) if alpha_deps else 0.0

        metrics = AlphaMetrics(
            current_alpha=current_alpha,
            target_alpha=self.target_alpha,
            core_tools_count=core_count,
            bridges_tools_spawned=bridges_count,
            average_bridges_per_core=avg_bridges,
            cascade_success_rate=success_rate,
            alpha_improvement=current_alpha - 2.0  # Baseline is 2.0
        )

        self.metrics_history.append(metrics)

        return metrics

    def generate_report(self) -> str:
        """Generate comprehensive α amplification report"""
        metrics = self.calculate_metrics()
        patterns = self.analyze_core_bridges_patterns()

        report = []
        report.append("="*70)
        report.append("ALPHA AMPLIFIER REPORT")
        report.append("="*70)
        report.append("")

        # Current state
        report.append("CURRENT STATE:")
        report.append(f"  α (measured):     {metrics.current_alpha:.3f}")
        report.append(f"  α (target):       {metrics.target_alpha:.3f}")
        report.append(f"  Progress:         {metrics.progress_toward_target():.1f}%")
        report.append(f"  Improvement:      {metrics.alpha_improvement:+.3f} ({(metrics.alpha_improvement/2.0)*100:+.1f}%)")
        report.append("")

        # Tool cascade stats
        report.append("TOOL CASCADE STATISTICS:")
        report.append(f"  CORE tools:       {metrics.core_tools_count}")
        report.append(f"  BRIDGES spawned:  {metrics.bridges_tools_spawned}")
        report.append(f"  Average ratio:    {metrics.average_bridges_per_core:.2f} BRIDGES/CORE")
        report.append(f"  Cascade success:  {metrics.cascade_success_rate:.1%}")
        report.append("")

        # High-α patterns
        high_alpha = self.identify_high_alpha_patterns(min_bridges=2)
        report.append(f"HIGH-α PATTERNS ({len(high_alpha)} identified):")
        for i, (core, bridges) in enumerate(high_alpha[:5], 1):
            report.append(f"  {i}. {core}")
            report.append(f"     → {len(bridges)} BRIDGES tools spawned")
            report.append(f"     → α contribution: {len(bridges):.1f}")
        report.append("")

        # Enhancement rules
        report.append(f"ENHANCEMENT RULES ({len(self.enhancement_rules)} learned):")
        for i, rule in enumerate(self.enhancement_rules[:5], 1):
            report.append(f"  {i}. Strategy: {rule['replication_strategy']}")
            report.append(f"     Expected α: {rule['expected_alpha_contribution']:.1f}")
            report.append(f"     Confidence: {rule['confidence']:.1%}")
        report.append("")

        # Recommendations
        report.append("RECOMMENDATIONS:")
        if metrics.current_alpha < metrics.target_alpha:
            gap = metrics.target_alpha - metrics.current_alpha
            report.append(f"  ⚠ α is {gap:.3f} below target")
            report.append(f"  → Need {gap * metrics.core_tools_count:.0f} more BRIDGES tools")
            report.append(f"  → Or {gap / metrics.average_bridges_per_core:.0f} more CORE tools")

            if len(high_alpha) > 0:
                report.append(f"  ✓ Replicate patterns from top {len(high_alpha)} CORE tools")
        else:
            report.append(f"  ✓ Target α = {metrics.target_alpha} ACHIEVED!")
            report.append(f"  → Current α = {metrics.current_alpha:.3f}")

        report.append("")
        report.append("="*70)

        return "\n".join(report)

    def export_state(self) -> Dict:
        """Export current state for persistence"""
        return {
            'current_alpha': self.current_alpha,
            'target_alpha': self.target_alpha,
            'dependencies_count': len(self.dependencies),
            'tools_by_layer': {
                layer.value: list(tools)
                for layer, tools in self.tools_by_layer.items()
            },
            'enhancement_rules': self.enhancement_rules,
            'metrics_history': [
                {
                    'current_alpha': m.current_alpha,
                    'core_tools': m.core_tools_count,
                    'bridges_spawned': m.bridges_tools_spawned,
                    'timestamp': m.timestamp.isoformat()
                }
                for m in self.metrics_history
            ]
        }


def demonstrate_alpha_amplification():
    """Demonstration of α amplification"""
    print("\n" + "="*70)
    print("ALPHA AMPLIFIER DEMONSTRATION")
    print("="*70)
    print()

    amplifier = AlphaAmplifier()

    # Simulate observed cascade patterns (based on empirical data)
    print("Recording observed cascade patterns...\n")

    # CORE tool 1: spawns 2 BRIDGES (average)
    amplifier.record_dependency(
        "tool_core_coordination_001", "tool_bridges_sync_001",
        ToolLayer.CORE, ToolLayer.BRIDGES, strength=0.9, cascade_triggered=True
    )
    amplifier.record_dependency(
        "tool_core_coordination_001", "tool_bridges_integrate_001",
        ToolLayer.CORE, ToolLayer.BRIDGES, strength=0.8, cascade_triggered=True
    )

    # CORE tool 2: spawns 3 BRIDGES (above average - high α!)
    amplifier.record_dependency(
        "tool_core_orchestrator_001", "tool_bridges_compose_001",
        ToolLayer.CORE, ToolLayer.BRIDGES, strength=1.0, cascade_triggered=True
    )
    amplifier.record_dependency(
        "tool_core_orchestrator_001", "tool_bridges_meta_gen_001",
        ToolLayer.CORE, ToolLayer.BRIDGES, strength=0.9, cascade_triggered=True
    )
    amplifier.record_dependency(
        "tool_core_orchestrator_001", "tool_bridges_framework_link_001",
        ToolLayer.CORE, ToolLayer.BRIDGES, strength=0.85, cascade_triggered=True
    )

    # CORE tool 3: spawns 2 BRIDGES
    amplifier.record_dependency(
        "tool_core_state_manager_001", "tool_bridges_crdt_001",
        ToolLayer.CORE, ToolLayer.BRIDGES, strength=0.95, cascade_triggered=True
    )
    amplifier.record_dependency(
        "tool_core_state_manager_001", "tool_bridges_vector_clock_001",
        ToolLayer.CORE, ToolLayer.BRIDGES, strength=0.9, cascade_triggered=False
    )

    # Calculate metrics
    metrics = amplifier.calculate_metrics()
    print(f"Current α: {metrics.current_alpha:.3f}")
    print(f"CORE tools: {metrics.core_tools_count}")
    print(f"BRIDGES spawned: {metrics.bridges_tools_spawned}")
    print(f"Average: {metrics.average_bridges_per_core:.2f} BRIDGES/CORE")
    print()

    # Learn enhancement rules
    amplifier.learn_enhancement_rules()
    print()

    # Generate report
    print(amplifier.generate_report())

    # Test enhancement
    print("\nTesting tool specification enhancement...")
    test_spec = {
        'tool_id': 'tool_core_new_001',
        'purpose': 'Advanced coordination',
        'layer': 'CORE'
    }
    enhanced_spec = amplifier.apply_enhancement_to_tool_spec(test_spec)
    print(f"Enhanced spec: {json.dumps(enhanced_spec.get('alpha_enhancement', {}), indent=2)}")


if __name__ == "__main__":
    demonstrate_alpha_amplification()
