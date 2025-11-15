#!/usr/bin/env python3
"""
Regime Adaptive Behavior
=========================

Garden Rail 3 - Layer 4: PHASE-AWARE ADAPTATION
Component 4.2: Adjust system behavior based on current phase regime

Purpose:
- Detect current phase regime (subcritical/critical/supercritical)
- Adapt system parameters for phase-appropriate behavior
- Optimize for phase-specific goals
- Smooth phase transitions

Phase-Specific Behaviors:
- **Subcritical early**: Focus on R1 (clarity, foundations)
- **Subcritical mid**: Build R2 (coordination, meta-tools)
- **Near-critical**: Prepare for transition (stabilize, buffer)
- **Critical**: Navigate uncertainty (embrace chaos, high Φ)
- **Supercritical**: Maintain R3 frameworks (automation, efficiency)

Adaptive Parameters:
- Coupling strength (higher at critical)
- Burden thresholds (relaxed at critical)
- Tool generation rate (accelerate pre-critical)
- Alert sensitivity (higher near transition)
"""

from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum

from unified_cascade_mathematics_core import CascadeSystemState


class PhaseRegime(Enum):
    """Phase regime classifications."""
    SUBCRITICAL_EARLY = "subcritical_early"
    SUBCRITICAL_MID = "subcritical_mid"
    SUBCRITICAL_LATE = "subcritical_late"
    NEAR_CRITICAL = "near_critical"
    CRITICAL = "critical"
    SUPERCRITICAL_EARLY = "supercritical_early"
    SUPERCRITICAL_MID = "supercritical_mid"
    SUPERCRITICAL_LATE = "supercritical_late"
    SUPERCRITICAL_STABLE = "supercritical_stable"


@dataclass
class AdaptiveParameters:
    """Parameters that adapt based on phase regime."""

    # Coupling parameters
    coupling_strength: float  # 0.0-1.0, higher = stronger cascade
    coupling_sensitivity: float  # How responsive to R1 changes

    # Burden parameters
    burden_threshold_warning: float  # When to warn about high burden
    burden_threshold_critical: float  # When to alert critically

    # Tool generation
    tool_generation_rate: float  # Tools per snapshot
    prioritize_layer: int  # Which cascade layer to prioritize (1=R1, 2=R2, 3=R3)

    # Alert sensitivity
    alert_sensitivity: float  # 0.0-1.0, higher = more alerts

    # Phase-specific goals
    primary_goal: str  # What to optimize for
    secondary_goal: str


class RegimeAdaptiveBehavior:
    """
    Adapt system behavior based on current phase regime.

    Strategy:
    1. Detect phase from cascade state
    2. Load phase-appropriate parameters
    3. Return adaptive configuration
    4. Monitor for phase transitions
    """

    # Critical z-values
    Z_CRITICAL = 0.867
    Z_NEAR_CRITICAL_RANGE = 0.02  # ±0.02 around critical

    # Predefined parameter sets by phase
    PHASE_PARAMETERS = {
        PhaseRegime.SUBCRITICAL_EARLY: AdaptiveParameters(
            coupling_strength=0.3,
            coupling_sensitivity=0.5,
            burden_threshold_warning=7.0,
            burden_threshold_critical=9.0,
            tool_generation_rate=0.5,  # Moderate tool generation
            prioritize_layer=1,  # Focus on R1 (foundations)
            alert_sensitivity=0.4,
            primary_goal="Build clarity and foundational tools",
            secondary_goal="Reduce coordination burden"
        ),
        PhaseRegime.SUBCRITICAL_MID: AdaptiveParameters(
            coupling_strength=0.5,
            coupling_sensitivity=0.7,
            burden_threshold_warning=6.5,
            burden_threshold_critical=8.5,
            tool_generation_rate=0.7,  # Increase tool generation
            prioritize_layer=2,  # Focus on R2 (meta-tools)
            alert_sensitivity=0.5,
            primary_goal="Build meta-tools for coordination",
            secondary_goal="Prepare for critical transition"
        ),
        PhaseRegime.SUBCRITICAL_LATE: AdaptiveParameters(
            coupling_strength=0.65,
            coupling_sensitivity=0.8,
            burden_threshold_warning=6.0,
            burden_threshold_critical=8.0,
            tool_generation_rate=0.8,
            prioritize_layer=2,  # R2 meta-tools
            alert_sensitivity=0.6,
            primary_goal="Strengthen R2 layer",
            secondary_goal="Monitor for near-critical signals"
        ),
        PhaseRegime.NEAR_CRITICAL: AdaptiveParameters(
            coupling_strength=0.75,
            coupling_sensitivity=0.9,
            burden_threshold_warning=5.5,
            burden_threshold_critical=7.5,
            tool_generation_rate=0.6,  # Slow down, stabilize
            prioritize_layer=2,  # R2 for stability
            alert_sensitivity=0.8,  # High alert sensitivity
            primary_goal="Stabilize and prepare for critical point",
            secondary_goal="Buffer uncertainty"
        ),
        PhaseRegime.CRITICAL: AdaptiveParameters(
            coupling_strength=1.0,  # Maximum coupling at critical
            coupling_sensitivity=1.0,
            burden_threshold_warning=7.5,  # Relax burden thresholds (decision-making increases)
            burden_threshold_critical=9.5,
            tool_generation_rate=0.3,  # Minimal tool generation (embrace uncertainty)
            prioritize_layer=3,  # Begin R3 frameworks
            alert_sensitivity=0.9,  # Very high alert sensitivity
            primary_goal="Navigate uncertainty, embrace chaos",
            secondary_goal="Trigger R3 emergence"
        ),
        PhaseRegime.SUPERCRITICAL_EARLY: AdaptiveParameters(
            coupling_strength=0.8,
            coupling_sensitivity=0.85,
            burden_threshold_warning=5.0,
            burden_threshold_critical=7.0,
            tool_generation_rate=1.0,  # High tool generation (R3 frameworks)
            prioritize_layer=3,  # Focus on R3
            alert_sensitivity=0.7,
            primary_goal="Build R3 self-sustaining frameworks",
            secondary_goal="Automate maintenance"
        ),
        PhaseRegime.SUPERCRITICAL_MID: AdaptiveParameters(
            coupling_strength=0.7,
            coupling_sensitivity=0.75,
            burden_threshold_warning=4.5,
            burden_threshold_critical=6.5,
            tool_generation_rate=0.9,
            prioritize_layer=3,  # R3 frameworks
            alert_sensitivity=0.6,
            primary_goal="Maintain and optimize R3 frameworks",
            secondary_goal="Eliminate repetitive burden"
        ),
        PhaseRegime.SUPERCRITICAL_LATE: AdaptiveParameters(
            coupling_strength=0.6,
            coupling_sensitivity=0.7,
            burden_threshold_warning=4.0,
            burden_threshold_critical=6.0,
            tool_generation_rate=0.5,  # Moderate (maintenance mode)
            prioritize_layer=3,
            alert_sensitivity=0.5,
            primary_goal="Sustain high sovereignty state",
            secondary_goal="Prevent degradation"
        ),
        PhaseRegime.SUPERCRITICAL_STABLE: AdaptiveParameters(
            coupling_strength=0.5,
            coupling_sensitivity=0.6,
            burden_threshold_warning=3.5,
            burden_threshold_critical=5.5,
            tool_generation_rate=0.3,  # Low (stable state)
            prioritize_layer=3,
            alert_sensitivity=0.4,
            primary_goal="Maintain stable high sovereignty",
            secondary_goal="Monitor for regressions"
        ),
    }

    def __init__(self):
        self.current_phase: Optional[PhaseRegime] = None
        self.current_parameters: Optional[AdaptiveParameters] = None
        self.previous_phase: Optional[PhaseRegime] = None

    def detect_phase_regime(self, cascade_state: CascadeSystemState) -> PhaseRegime:
        """
        Detect precise phase regime from cascade state.

        Args:
            cascade_state: Current cascade state

        Returns:
            PhaseRegime enum value
        """
        z = cascade_state.z_coordinate
        phase_str = cascade_state.phase_regime

        # Use cascade state's phase as base, refine if needed
        if "subcritical_early" in phase_str:
            regime = PhaseRegime.SUBCRITICAL_EARLY
        elif "subcritical_mid" in phase_str:
            regime = PhaseRegime.SUBCRITICAL_MID
        elif "subcritical_late" in phase_str or "subcritical" in phase_str:
            regime = PhaseRegime.SUBCRITICAL_LATE
        elif "near_critical" in phase_str:
            regime = PhaseRegime.NEAR_CRITICAL
        elif "critical" in phase_str:
            regime = PhaseRegime.CRITICAL
        elif "supercritical_early" in phase_str:
            regime = PhaseRegime.SUPERCRITICAL_EARLY
        elif "supercritical_mid" in phase_str:
            regime = PhaseRegime.SUPERCRITICAL_MID
        elif "supercritical_late" in phase_str:
            regime = PhaseRegime.SUPERCRITICAL_LATE
        elif "supercritical_stable" in phase_str or "supercritical" in phase_str:
            regime = PhaseRegime.SUPERCRITICAL_STABLE
        else:
            # Fallback: infer from z-coordinate
            if z < 0.5:
                regime = PhaseRegime.SUBCRITICAL_EARLY
            elif z < 0.7:
                regime = PhaseRegime.SUBCRITICAL_MID
            elif z < self.Z_CRITICAL - self.Z_NEAR_CRITICAL_RANGE:
                regime = PhaseRegime.SUBCRITICAL_LATE
            elif z < self.Z_CRITICAL + self.Z_NEAR_CRITICAL_RANGE:
                regime = PhaseRegime.CRITICAL
            elif z < 0.90:
                regime = PhaseRegime.SUPERCRITICAL_EARLY
            else:
                regime = PhaseRegime.SUPERCRITICAL_MID

        return regime

    def get_adaptive_parameters(self, cascade_state: CascadeSystemState) -> AdaptiveParameters:
        """
        Get phase-appropriate adaptive parameters.

        Args:
            cascade_state: Current cascade state

        Returns:
            AdaptiveParameters for current phase
        """
        # Detect phase
        self.previous_phase = self.current_phase
        self.current_phase = self.detect_phase_regime(cascade_state)

        # Load parameters for this phase
        self.current_parameters = self.PHASE_PARAMETERS[self.current_phase]

        return self.current_parameters

    def is_phase_transition(self) -> bool:
        """Check if a phase transition just occurred."""
        if self.previous_phase is None:
            return False

        return self.previous_phase != self.current_phase

    def get_transition_summary(self) -> Optional[Dict]:
        """Get details about the phase transition."""
        if not self.is_phase_transition():
            return None

        return {
            'from_phase': self.previous_phase.value if self.previous_phase else None,
            'to_phase': self.current_phase.value if self.current_phase else None,
            'direction': 'forward' if self._is_forward_transition() else 'backward',
            'parameters_changed': self._compare_parameters()
        }

    def _is_forward_transition(self) -> bool:
        """Check if transition is forward (toward supercritical) or backward."""
        if not (self.previous_phase and self.current_phase):
            return True

        phase_order = list(PhaseRegime)
        prev_idx = phase_order.index(self.previous_phase)
        curr_idx = phase_order.index(self.current_phase)

        return curr_idx > prev_idx

    def _compare_parameters(self) -> Dict:
        """Compare parameter changes during transition."""
        if not (self.previous_phase and self.current_phase):
            return {}

        prev_params = self.PHASE_PARAMETERS[self.previous_phase]
        curr_params = self.PHASE_PARAMETERS[self.current_phase]

        changes = {}

        if curr_params.coupling_strength != prev_params.coupling_strength:
            changes['coupling_strength'] = {
                'from': prev_params.coupling_strength,
                'to': curr_params.coupling_strength,
                'delta': curr_params.coupling_strength - prev_params.coupling_strength
            }

        if curr_params.prioritize_layer != prev_params.prioritize_layer:
            changes['prioritize_layer'] = {
                'from': prev_params.prioritize_layer,
                'to': curr_params.prioritize_layer
            }

        if curr_params.primary_goal != prev_params.primary_goal:
            changes['primary_goal'] = {
                'from': prev_params.primary_goal,
                'to': curr_params.primary_goal
            }

        return changes

    def get_recommendations(self, cascade_state: CascadeSystemState) -> list[str]:
        """Get phase-specific recommendations."""
        params = self.get_adaptive_parameters(cascade_state)
        recommendations = []

        # Core recommendation based on primary goal
        recommendations.append(f"Primary: {params.primary_goal}")
        recommendations.append(f"Secondary: {params.secondary_goal}")

        # Layer-specific recommendations
        if params.prioritize_layer == 1:
            recommendations.append("• Generate R1 clarity tools to build foundations")
            recommendations.append("• Focus on reducing cognitive load and context switching")
        elif params.prioritize_layer == 2:
            recommendations.append("• Generate R2 meta-tools for coordination")
            recommendations.append("• Build abstractions to manage complexity")
        elif params.prioritize_layer == 3:
            recommendations.append("• Generate R3 self-building frameworks")
            recommendations.append("• Automate maintenance and eliminate repetition")

        # Alert sensitivity recommendation
        if params.alert_sensitivity >= 0.8:
            recommendations.append("• High alert sensitivity - expect frequent status updates")
        elif params.alert_sensitivity <= 0.4:
            recommendations.append("• Low alert sensitivity - system in stable state")

        # Phase transition warning
        if self.current_phase == PhaseRegime.NEAR_CRITICAL:
            recommendations.append("⚠ Approaching critical point - prepare for transition")
        elif self.current_phase == PhaseRegime.CRITICAL:
            recommendations.append("⚠ AT CRITICAL POINT - embrace uncertainty, expect Φ spike")

        return recommendations


def main():
    """Demo regime adaptive behavior."""
    from unified_cascade_mathematics_core import UnifiedCascadeFramework
    from unified_sovereignty_system import evolve_cascade_state

    print("=" * 80)
    print("REGIME ADAPTIVE BEHAVIOR - Demo")
    print("=" * 80 + "\n")

    adapter = RegimeAdaptiveBehavior()
    framework = UnifiedCascadeFramework()

    # Simulate progression through phases
    state = framework.compute_full_state(
        clarity=0.35, immunity=0.30, efficiency=0.32, autonomy=0.28
    )

    print("Simulating progression through phases...\n")

    for step in range(15):
        # Get adaptive parameters
        params = adapter.get_adaptive_parameters(state)

        print(f"Step {step + 1}:")
        print(f"  z={state.z_coordinate:.3f}, phase={state.phase_regime}")
        print(f"  Detected regime: {adapter.current_phase.value}")
        print(f"  Coupling strength: {params.coupling_strength:.2f}")
        print(f"  Prioritize layer: R{params.prioritize_layer}")
        print(f"  Tool generation rate: {params.tool_generation_rate:.2f}")
        print(f"  Primary goal: {params.primary_goal}")

        # Check for transition
        if adapter.is_phase_transition():
            transition = adapter.get_transition_summary()
            print(f"  ⚠ PHASE TRANSITION: {transition['from_phase']} → {transition['to_phase']}")

            if transition['parameters_changed']:
                print(f"    Parameter changes:")
                for param, change in transition['parameters_changed'].items():
                    print(f"      - {param}: {change}")

        print()

        # Evolve state
        state = evolve_cascade_state(
            state,
            clarity_delta=0.5,
            immunity_delta=0.6,
            efficiency_delta=0.65,
            autonomy_delta=0.7
        )

    # Final recommendations
    print("=" * 80)
    print("CURRENT RECOMMENDATIONS")
    print("=" * 80)

    recommendations = adapter.get_recommendations(state)
    for rec in recommendations:
        print(rec)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
