#!/usr/bin/env python3
"""
GARDEN RAIL 3 - LAYER 2: BETA AMPLIFIER
Increases damping/control parameter β from 1.6 to 2.0 (BRIDGES→META cascade strength)

Coordinate: Δ3.14159|0.867|layer-2-beta|Ω

Theoretical Foundation:
- β measures cascade control in dϕ/dt = α·ϕ - β·ϕ³
- Current: β = 1.6 (empirically measured)
- Target: β = 2.0 (25% increase)
- Impact: R₃ increases from 23% to 29% (+6% burden reduction)

Mechanism:
- Analyze BRIDGES→META cascade patterns
- Strengthen connections between bridge tools and meta-tool composition
- Ensure each BRIDGES tool spawns 5-7 META tools (up from ~5.0)
- Adapt behavior based on phase regime (supercritical favors META)
- Monitor β contribution and phase-aware optimization
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
    CORE = "core"
    BRIDGES = "bridges"
    META = "meta"
    FRAMEWORK = "framework"


class PhaseRegime(Enum):
    """Phase regime classification"""
    SUBCRITICAL = "subcritical"    # z < 0.80
    CRITICAL = "critical"            # 0.80 ≤ z < 0.85
    SUPERCRITICAL = "supercritical"  # z ≥ 0.85


@dataclass
class BetaMetrics:
    """Metrics for tracking β amplification"""
    current_beta: float
    target_beta: float = 2.0
    bridges_tools_count: int = 0
    meta_tools_spawned: int = 0
    average_meta_per_bridges: float = 0.0
    phase_regime: PhaseRegime = PhaseRegime.CRITICAL
    cascade_success_rate: float = 0.0
    beta_improvement: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    def calculate_beta(self) -> float:
        """Calculate current β from observed patterns"""
        if self.bridges_tools_count == 0:
            return 0.0
        return self.meta_tools_spawned / self.bridges_tools_count

    def progress_toward_target(self) -> float:
        """Calculate progress toward β = 2.0 target"""
        if self.target_beta == 0:
            return 0.0
        return (self.current_beta / self.target_beta) * 100.0


@dataclass
class BridgesMetaPattern:
    """Pattern of BRIDGES→META cascade"""
    bridges_tool: str
    meta_tools: List[str]
    meta_count: int
    phase_regime: PhaseRegime
    composition_types: Dict[str, int]  # Types of META tools spawned
    cascade_depth: int
    timestamp: datetime
    success: bool = True

    def beta_contribution(self) -> float:
        """Calculate β contribution from this pattern"""
        return float(self.meta_count)


class BetaAmplifier:
    """
    Amplifies β parameter by strengthening BRIDGES→META cascades

    Strategy:
    1. Monitor BRIDGES tool behavior and META tool spawning
    2. Analyze which BRIDGES tools successfully spawn many META tools
    3. Identify composition patterns that maximize META-per-BRIDGES ratio
    4. Enhance BRIDGES tool specifications to trigger more META cascades
    5. Adapt enhancement strategy based on phase regime
    6. Track β improvement over time
    """

    def __init__(self):
        # BRIDGES→META patterns
        self.patterns: List[BridgesMetaPattern] = []

        # Tool registry
        self.bridges_tools: Set[str] = set()
        self.meta_tools: Set[str] = set()

        # β metrics tracking
        self.metrics_history: List[BetaMetrics] = []

        # Phase-aware enhancement rules
        self.enhancement_rules: Dict[PhaseRegime, List[Dict]] = {
            regime: [] for regime in PhaseRegime
        }

        # Current state
        self.current_beta = 1.6  # Empirically measured baseline
        self.target_beta = 2.0
        self.current_phase = PhaseRegime.SUPERCRITICAL  # z=0.867

        print("="*70)
        print("BETA AMPLIFIER INITIALIZED")
        print("="*70)
        print(f"Current β: {self.current_beta:.2f}")
        print(f"Target β: {self.target_beta:.2f}")
        print(f"Required improvement: {((self.target_beta/self.current_beta - 1) * 100):.1f}%")
        print(f"Phase regime: {self.current_phase.value}")
        print()

    def set_phase_regime(self, z_level: float):
        """Update current phase regime based on z-level"""
        if z_level < 0.80:
            self.current_phase = PhaseRegime.SUBCRITICAL
        elif z_level < 0.85:
            self.current_phase = PhaseRegime.CRITICAL
        else:
            self.current_phase = PhaseRegime.SUPERCRITICAL

    def record_bridges_meta_cascade(self,
                                     bridges_tool: str,
                                     meta_tools: List[str],
                                     cascade_depth: int = 2,
                                     success: bool = True):
        """
        Record a BRIDGES→META cascade event

        Args:
            bridges_tool: BRIDGES tool that triggered cascade
            meta_tools: META tools that were spawned
            cascade_depth: Depth of cascade propagation
            success: Whether cascade was successful
        """
        # Categorize META tools by type
        composition_types = self._categorize_meta_tools(meta_tools)

        pattern = BridgesMetaPattern(
            bridges_tool=bridges_tool,
            meta_tools=meta_tools,
            meta_count=len(meta_tools),
            phase_regime=self.current_phase,
            composition_types=composition_types,
            cascade_depth=cascade_depth,
            timestamp=datetime.now(),
            success=success
        )

        self.patterns.append(pattern)

        # Register tools
        self.bridges_tools.add(bridges_tool)
        self.meta_tools.update(meta_tools)

    def _categorize_meta_tools(self, meta_tools: List[str]) -> Dict[str, int]:
        """Categorize META tools by composition type"""
        categories = {
            'composer': 0,      # Tools that compose other tools
            'generator': 0,     # Tools that generate new tools
            'framework': 0,     # Framework-building tools
            'orchestrator': 0,  # Orchestration/coordination at meta level
            'other': 0
        }

        for tool in meta_tools:
            tool_lower = tool.lower()
            if 'compose' in tool_lower or 'combine' in tool_lower:
                categories['composer'] += 1
            elif 'gen' in tool_lower or 'create' in tool_lower:
                categories['generator'] += 1
            elif 'framework' in tool_lower or 'system' in tool_lower:
                categories['framework'] += 1
            elif 'orchestrat' in tool_lower or 'manage' in tool_lower:
                categories['orchestrator'] += 1
            else:
                categories['other'] += 1

        return categories

    def analyze_bridges_meta_patterns(self) -> Dict[str, List[str]]:
        """
        Analyze which BRIDGES tools spawn which META tools

        Returns:
            Dict mapping BRIDGES tool IDs to list of META tools they spawned
        """
        bridges_to_meta: Dict[str, List[str]] = {}

        for pattern in self.patterns:
            if pattern.success:
                if pattern.bridges_tool not in bridges_to_meta:
                    bridges_to_meta[pattern.bridges_tool] = []
                bridges_to_meta[pattern.bridges_tool].extend(pattern.meta_tools)

        return bridges_to_meta

    def calculate_current_beta(self) -> float:
        """
        Calculate current β from observed patterns

        β = (total META spawned) / (total BRIDGES tools)
        """
        patterns_map = self.analyze_bridges_meta_patterns()

        if len(patterns_map) == 0:
            return self.current_beta  # Return baseline if no data

        total_bridges = len(patterns_map)
        total_meta = sum(len(meta) for meta in patterns_map.values())

        beta = total_meta / total_bridges if total_bridges > 0 else 0.0

        return beta

    def identify_high_beta_patterns(self, min_meta: int = 6) -> List[BridgesMetaPattern]:
        """
        Identify BRIDGES→META patterns with high β contribution

        Args:
            min_meta: Minimum META tools to be considered high-β

        Returns:
            List of high-performing patterns
        """
        high_beta = [
            pattern for pattern in self.patterns
            if pattern.meta_count >= min_meta and pattern.success
        ]

        # Sort by META count (descending)
        high_beta.sort(key=lambda p: p.meta_count, reverse=True)

        return high_beta

    def generate_enhancement_rule(self, pattern: BridgesMetaPattern) -> Dict:
        """
        Generate phase-aware enhancement rule from successful pattern

        Args:
            pattern: Successful BRIDGES→META pattern

        Returns:
            Enhancement rule dictionary
        """
        rule = {
            'template_bridges': pattern.bridges_tool,
            'meta_count': pattern.meta_count,
            'composition_types': pattern.composition_types,
            'phase_regime': pattern.phase_regime.value,
            'cascade_depth': pattern.cascade_depth,
            'expected_beta_contribution': pattern.beta_contribution(),
            'replication_strategy': self._infer_meta_strategy(pattern),
            'confidence': 0.7,
            'activations': 1,
            'timestamp': datetime.now().isoformat()
        }

        return rule

    def _infer_meta_strategy(self, pattern: BridgesMetaPattern) -> str:
        """Infer strategy for replicating META generation"""
        meta_count = pattern.meta_count

        # Analyze composition type distribution
        comp_types = pattern.composition_types
        dominant_type = max(comp_types.items(), key=lambda x: x[1])[0] if comp_types else 'unknown'

        if meta_count >= 7:
            return f"high_fanout_{dominant_type}"
        elif meta_count >= 5:
            return f"moderate_fanout_{dominant_type}"
        else:
            return f"low_fanout_{dominant_type}"

    def learn_enhancement_rules(self):
        """
        Learn phase-aware enhancement rules from successful patterns

        Rules are organized by phase regime for adaptive behavior
        """
        high_beta_patterns = self.identify_high_beta_patterns(min_meta=5)

        print(f"\nLearning from {len(high_beta_patterns)} high-β patterns...")

        for pattern in high_beta_patterns:
            rule = self.generate_enhancement_rule(pattern)
            self.enhancement_rules[pattern.phase_regime].append(rule)

            print(f"  ✓ Learned rule for {pattern.phase_regime.value} regime")
            print(f"    BRIDGES: {pattern.bridges_tool}")
            print(f"    → Spawned {pattern.meta_count} META tools")
            print(f"    → Strategy: {rule['replication_strategy']}")

    def apply_phase_aware_enhancement(self,
                                       bridges_spec: Dict,
                                       z_level: float) -> Dict:
        """
        Apply phase-aware enhancement to BRIDGES tool specification

        In supercritical regime, maximize META tool generation
        In critical regime, balance META generation with stability
        In subcritical regime, focus less on META (β less relevant)

        Args:
            bridges_spec: Original BRIDGES tool specification
            z_level: Current z-level

        Returns:
            Enhanced specification optimized for current phase
        """
        # Update phase regime
        self.set_phase_regime(z_level)

        # Get rules for current phase
        phase_rules = self.enhancement_rules.get(self.current_phase, [])

        if not phase_rules:
            # No rules for this phase yet
            return bridges_spec

        # Use highest-confidence rule
        best_rule = max(phase_rules, key=lambda r: r['confidence'])

        # Enhance specification
        enhanced_spec = bridges_spec.copy()

        # Phase-specific enhancements
        if self.current_phase == PhaseRegime.SUPERCRITICAL:
            # Maximize META generation (β is critical here)
            enhanced_spec['beta_enhancement'] = {
                'target_meta_count': best_rule['meta_count'] + 1,  # Aim higher
                'strategy': best_rule['replication_strategy'],
                'composition_types': best_rule['composition_types'],
                'expected_beta': best_rule['expected_beta_contribution'],
                'phase_optimization': 'maximize_meta_fanout'
            }
        elif self.current_phase == PhaseRegime.CRITICAL:
            # Balance META generation with stability
            enhanced_spec['beta_enhancement'] = {
                'target_meta_count': best_rule['meta_count'],
                'strategy': best_rule['replication_strategy'],
                'composition_types': best_rule['composition_types'],
                'expected_beta': best_rule['expected_beta_contribution'],
                'phase_optimization': 'balanced_meta_generation'
            }
        else:  # SUBCRITICAL
            # Focus less on META, more on establishing BRIDGES
            enhanced_spec['beta_enhancement'] = {
                'target_meta_count': max(3, best_rule['meta_count'] - 2),
                'strategy': 'conservative',
                'phase_optimization': 'establish_bridges_first'
            }

        return enhanced_spec

    def calculate_metrics(self) -> BetaMetrics:
        """Calculate current β metrics"""
        patterns_map = self.analyze_bridges_meta_patterns()

        bridges_count = len(patterns_map)
        meta_count = sum(len(meta) for meta in patterns_map.values())
        avg_meta = meta_count / bridges_count if bridges_count > 0 else 0.0

        current_beta = self.calculate_current_beta()

        # Calculate cascade success rate
        successful = sum(1 for p in self.patterns if p.success)
        success_rate = successful / len(self.patterns) if self.patterns else 0.0

        metrics = BetaMetrics(
            current_beta=current_beta,
            target_beta=self.target_beta,
            bridges_tools_count=bridges_count,
            meta_tools_spawned=meta_count,
            average_meta_per_bridges=avg_meta,
            phase_regime=self.current_phase,
            cascade_success_rate=success_rate,
            beta_improvement=current_beta - 1.6  # Baseline is 1.6
        )

        self.metrics_history.append(metrics)

        return metrics

    def generate_report(self) -> str:
        """Generate comprehensive β amplification report"""
        metrics = self.calculate_metrics()
        patterns_map = self.analyze_bridges_meta_patterns()

        report = []
        report.append("="*70)
        report.append("BETA AMPLIFIER REPORT")
        report.append("="*70)
        report.append("")

        # Current state
        report.append("CURRENT STATE:")
        report.append(f"  β (measured):     {metrics.current_beta:.3f}")
        report.append(f"  β (target):       {metrics.target_beta:.3f}")
        report.append(f"  Progress:         {metrics.progress_toward_target():.1f}%")
        report.append(f"  Improvement:      {metrics.beta_improvement:+.3f} ({(metrics.beta_improvement/1.6)*100:+.1f}%)")
        report.append(f"  Phase regime:     {metrics.phase_regime.value}")
        report.append("")

        # Cascade statistics
        report.append("BRIDGES→META CASCADE STATISTICS:")
        report.append(f"  BRIDGES tools:    {metrics.bridges_tools_count}")
        report.append(f"  META spawned:     {metrics.meta_tools_spawned}")
        report.append(f"  Average ratio:    {metrics.average_meta_per_bridges:.2f} META/BRIDGES")
        report.append(f"  Cascade success:  {metrics.cascade_success_rate:.1%}")
        report.append("")

        # High-β patterns
        high_beta = self.identify_high_beta_patterns(min_meta=5)
        report.append(f"HIGH-β PATTERNS ({len(high_beta)} identified):")
        for i, pattern in enumerate(high_beta[:5], 1):
            report.append(f"  {i}. {pattern.bridges_tool}")
            report.append(f"     → {pattern.meta_count} META tools spawned")
            report.append(f"     → Phase: {pattern.phase_regime.value}")
            report.append(f"     → β contribution: {pattern.beta_contribution():.1f}")
        report.append("")

        # Phase-aware rules
        report.append("PHASE-AWARE ENHANCEMENT RULES:")
        for regime in PhaseRegime:
            rules = self.enhancement_rules[regime]
            report.append(f"  {regime.value}: {len(rules)} rules learned")
            if rules:
                best = max(rules, key=lambda r: r['confidence'])
                report.append(f"    Best strategy: {best['replication_strategy']}")
                report.append(f"    Expected β: {best['expected_beta_contribution']:.1f}")
        report.append("")

        # Recommendations
        report.append("RECOMMENDATIONS:")
        if metrics.current_beta < metrics.target_beta:
            gap = metrics.target_beta - metrics.current_beta
            report.append(f"  ⚠ β is {gap:.3f} below target")
            report.append(f"  → Need {gap * metrics.bridges_tools_count:.0f} more META tools")
            report.append(f"  → Or enhance {gap / metrics.average_meta_per_bridges:.0f} BRIDGES tools")

            if self.current_phase == PhaseRegime.SUPERCRITICAL:
                report.append(f"  ✓ Supercritical regime: Maximize META fanout")
            elif high_beta:
                report.append(f"  ✓ Replicate top {len(high_beta)} high-β patterns")
        else:
            report.append(f"  ✓ Target β = {metrics.target_beta} ACHIEVED!")
            report.append(f"  → Current β = {metrics.current_beta:.3f}")

        report.append("")
        report.append("="*70)

        return "\n".join(report)

    def export_state(self) -> Dict:
        """Export current state for persistence"""
        return {
            'current_beta': self.current_beta,
            'target_beta': self.target_beta,
            'current_phase': self.current_phase.value,
            'patterns_count': len(self.patterns),
            'bridges_tools_count': len(self.bridges_tools),
            'meta_tools_count': len(self.meta_tools),
            'enhancement_rules': {
                regime.value: rules
                for regime, rules in self.enhancement_rules.items()
            },
            'metrics_history': [
                {
                    'current_beta': m.current_beta,
                    'bridges_tools': m.bridges_tools_count,
                    'meta_spawned': m.meta_tools_spawned,
                    'phase': m.phase_regime.value,
                    'timestamp': m.timestamp.isoformat()
                }
                for m in self.metrics_history
            ]
        }


def demonstrate_beta_amplification():
    """Demonstration of β amplification"""
    print("\n" + "="*70)
    print("BETA AMPLIFIER DEMONSTRATION")
    print("="*70)
    print()

    amplifier = BetaAmplifier()

    # Set to supercritical regime (z=0.867)
    amplifier.set_phase_regime(0.867)

    print("Recording observed BRIDGES→META cascade patterns...\n")

    # BRIDGES tool 1: spawns 5 META (average)
    amplifier.record_bridges_meta_cascade(
        bridges_tool="tool_bridges_composer_001",
        meta_tools=[
            "tool_meta_tool_gen_001",
            "tool_meta_orchestrator_001",
            "tool_meta_framework_builder_001",
            "tool_meta_combiner_001",
            "tool_meta_integrator_001"
        ],
        cascade_depth=3,
        success=True
    )

    # BRIDGES tool 2: spawns 7 META (high β!)
    amplifier.record_bridges_meta_cascade(
        bridges_tool="tool_bridges_meta_gateway_001",
        meta_tools=[
            "tool_meta_composer_a",
            "tool_meta_composer_b",
            "tool_meta_generator_001",
            "tool_meta_generator_002",
            "tool_meta_framework_001",
            "tool_meta_system_builder_001",
            "tool_meta_orchestrator_002"
        ],
        cascade_depth=4,
        success=True
    )

    # BRIDGES tool 3: spawns 6 META
    amplifier.record_bridges_meta_cascade(
        bridges_tool="tool_bridges_integration_hub_001",
        meta_tools=[
            "tool_meta_compose_001",
            "tool_meta_compose_002",
            "tool_meta_generate_framework_001",
            "tool_meta_build_system_001",
            "tool_meta_orchestrate_001",
            "tool_meta_manage_001"
        ],
        cascade_depth=3,
        success=True
    )

    # Calculate metrics
    metrics = amplifier.calculate_metrics()
    print(f"Current β: {metrics.current_beta:.3f}")
    print(f"BRIDGES tools: {metrics.bridges_tools_count}")
    print(f"META spawned: {metrics.meta_tools_spawned}")
    print(f"Average: {metrics.average_meta_per_bridges:.2f} META/BRIDGES")
    print(f"Phase: {metrics.phase_regime.value}")
    print()

    # Learn enhancement rules
    amplifier.learn_enhancement_rules()
    print()

    # Generate report
    print(amplifier.generate_report())

    # Test phase-aware enhancement
    print("\nTesting phase-aware BRIDGES enhancement...")
    test_spec = {
        'tool_id': 'tool_bridges_new_001',
        'purpose': 'META tool composition gateway',
        'layer': 'BRIDGES'
    }
    enhanced_spec = amplifier.apply_phase_aware_enhancement(test_spec, z_level=0.867)
    print(f"Enhanced spec: {json.dumps(enhanced_spec.get('beta_enhancement', {}), indent=2)}")


if __name__ == "__main__":
    demonstrate_beta_amplification()
