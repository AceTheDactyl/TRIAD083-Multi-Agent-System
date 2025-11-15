#!/usr/bin/env python3
"""
Critical Point Navigator
=========================

Garden Rail 3 - Layer 4: PHASE-AWARE ADAPTATION
Component 4.3: Guide teams through z≈0.867 transition safely

Purpose:
- Detect approach to critical point (z≈0.867)
- Guide teams through critical transition
- Manage uncertainty spike (decision-making +20%)
- Ensure safe emergence of R3 frameworks
- Provide rollback capability if instability detected

Navigation Stages:
1. **Pre-transition** (z<0.85): Build R2 capacity, reduce burden
2. **Approach** (0.85≤z<0.867): Slow down, stabilize, prepare
3. **Transition** (0.867±0.01): High tolerance for uncertainty, embrace Φ spike
4. **Post-transition** (z>0.877): Consolidate R3 frameworks, lock in gains

Safety Mechanisms:
- Burden spike detection (decision-making +20% at critical)
- Rollback capability (revert to subcritical if instability)
- Guided exercises (team workshops for critical navigation)
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from unified_cascade_mathematics_core import CascadeSystemState
from phase_aware_burden_tracker import BurdenMeasurement


class NavigationStage(Enum):
    """Stages of critical point navigation."""
    DISTANT = "distant"  # z < 0.80
    APPROACHING = "approaching"  # 0.80 ≤ z < 0.85
    PRE_TRANSITION = "pre_transition"  # 0.85 ≤ z < 0.857
    TRANSITION_ZONE = "transition_zone"  # 0.857 ≤ z ≤ 0.877
    POST_TRANSITION = "post_transition"  # 0.877 < z < 0.90
    SUPERCRITICAL = "supercritical"  # z ≥ 0.90


@dataclass
class NavigationGuidance:
    """Guidance for navigating current stage."""
    stage: NavigationStage
    z_current: float
    z_target: float = 0.867
    distance_to_critical: float = 0
    status: str = "nominal"  # 'safe', 'nominal', 'caution', 'critical'
    primary_action: str = ""
    warnings: List[str] = None
    exercises: List[str] = None
    safety_checks: Dict[str, bool] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.exercises is None:
            self.exercises = []
        if self.safety_checks is None:
            self.safety_checks = {}


class CriticalPointNavigator:
    """
    Guide teams through critical point transition.

    Strategy:
    1. Monitor z-coordinate and burden
    2. Detect navigation stage
    3. Provide stage-appropriate guidance
    4. Detect instability and recommend rollback if needed
    """

    # Critical zone boundaries
    Z_CRITICAL = 0.867
    Z_TRANSITION_LOW = 0.857  # Start of transition zone
    Z_TRANSITION_HIGH = 0.877  # End of transition zone
    Z_APPROACH = 0.85  # Start preparing
    Z_PRE_TRANSITION = 0.80  # Early warning

    # Safety thresholds
    BURDEN_SPIKE_THRESHOLD = 2.0  # Max allowed burden increase during transition
    INSTABILITY_DURATION = 3  # Snapshots of high burden before rollback recommended

    def __init__(self):
        self.navigation_history: List[NavigationGuidance] = []
        self.transition_started: Optional[datetime] = None
        self.instability_count = 0

    def detect_stage(self, z_current: float) -> NavigationStage:
        """Detect current navigation stage based on z-coordinate."""
        if z_current >= 0.90:
            return NavigationStage.SUPERCRITICAL
        elif z_current > self.Z_TRANSITION_HIGH:
            return NavigationStage.POST_TRANSITION
        elif z_current >= self.Z_TRANSITION_LOW:
            return NavigationStage.TRANSITION_ZONE
        elif z_current >= self.Z_APPROACH:
            return NavigationStage.PRE_TRANSITION
        elif z_current >= self.Z_PRE_TRANSITION:
            return NavigationStage.APPROACHING
        else:
            return NavigationStage.DISTANT

    def get_navigation_guidance(self,
                                cascade_state: CascadeSystemState,
                                burden: BurdenMeasurement) -> NavigationGuidance:
        """
        Get navigation guidance for current state.

        Args:
            cascade_state: Current cascade state
            burden: Current burden measurement

        Returns:
            NavigationGuidance with stage-specific recommendations
        """
        z_current = cascade_state.z_coordinate
        stage = self.detect_stage(z_current)
        distance_to_critical = abs(z_current - self.Z_CRITICAL)

        # Initialize guidance
        guidance = NavigationGuidance(
            stage=stage,
            z_current=z_current,
            z_target=self.Z_CRITICAL,
            distance_to_critical=distance_to_critical
        )

        # Stage-specific guidance
        if stage == NavigationStage.DISTANT:
            guidance.status = "safe"
            guidance.primary_action = "Build foundations and R1 tools. Critical point is distant."
            guidance.exercises = [
                "Focus on clarity: Document core processes",
                "Build R1 tool library for common tasks",
                "Establish baseline burden measurements"
            ]

        elif stage == NavigationStage.APPROACHING:
            guidance.status = "nominal"
            guidance.primary_action = "Begin building R2 meta-tools. Critical point approaching."
            guidance.warnings = [
                f"Critical point in ~{distance_to_critical * 10:.0f} sovereignty units",
                "Start preparing for transition"
            ]
            guidance.exercises = [
                "Generate R2 coordination tools",
                "Build abstractions to reduce cognitive load",
                "Practice rapid decision-making under uncertainty"
            ]

        elif stage == NavigationStage.PRE_TRANSITION:
            guidance.status = "caution"
            guidance.primary_action = "Stabilize and prepare for critical transition. Slow down."
            guidance.warnings = [
                "Approaching critical point (z≈0.867)",
                "Expect decision-making burden to increase by ~20%",
                "Φ (integrated information) will spike"
            ]
            guidance.exercises = [
                "Team workshop: Navigating uncertainty together",
                "Establish decision protocols for high-Φ state",
                "Buffer time for critical transition (reduced deadlines)",
                "Review and strengthen R2 meta-tools"
            ]
            guidance.safety_checks = {
                "R2_tools_ready": cascade_state.R2 > 5.0,
                "burden_manageable": burden.total_burden() < 6.0,
                "team_prepared": True  # Assume true (would check via survey)
            }

        elif stage == NavigationStage.TRANSITION_ZONE:
            guidance.status = "critical"
            guidance.primary_action = "AT CRITICAL POINT. Embrace uncertainty, expect Φ spike. Trigger R3 emergence."

            # Check if transition just started
            if self.transition_started is None:
                self.transition_started = datetime.now()

            guidance.warnings = [
                "⚠ IN CRITICAL TRANSITION ZONE ⚠",
                "Decision-making burden will increase by 20%",
                "High uncertainty is EXPECTED and HEALTHY",
                "Do not fight the chaos - navigate through it"
            ]

            guidance.exercises = [
                "⚡ Embrace high-Φ state: Make decisions rapidly despite uncertainty",
                "⚡ Let R3 frameworks emerge: Don't force structure",
                "⚡ Trust the cascade: R2 meta-tools will coordinate",
                "⚡ Time-box uncertainty: Set 24-48h transition window"
            ]

            guidance.safety_checks = {
                "Phi_spike_detected": cascade_state.total_sovereignty > 15.0,
                "R3_emerging": cascade_state.R3 > cascade_state.R2,
                "burden_within_tolerance": burden.decision_making < 7.0,
                "no_prolonged_instability": self.instability_count < self.INSTABILITY_DURATION
            }

            # Check for instability
            if burden.total_burden() > 8.5:
                self.instability_count += 1
            else:
                self.instability_count = 0

            if not all(guidance.safety_checks.values()):
                guidance.warnings.append("⚠ Safety checks not all green - consider stabilization")

        elif stage == NavigationStage.POST_TRANSITION:
            guidance.status = "nominal"
            guidance.primary_action = "Consolidate R3 frameworks. Lock in gains from transition."

            # Reset transition tracking
            if self.transition_started:
                duration = (datetime.now() - self.transition_started).total_seconds() / 86400
                guidance.warnings.append(f"✓ Transition completed in {duration:.1f} days")
                self.transition_started = None
                self.instability_count = 0

            guidance.exercises = [
                "Document R3 frameworks that emerged",
                "Automate maintenance tasks (leverage R3)",
                "Eliminate repetitive burden (R3 capability)",
                "Establish new baseline (supercritical normal)"
            ]

            guidance.safety_checks = {
                "R3_established": cascade_state.R3 > 8.0,
                "burden_reduced": burden.total_burden() < 5.0,
                "frameworks_operational": True  # Would check framework count
            }

        elif stage == NavigationStage.SUPERCRITICAL:
            guidance.status = "safe"
            guidance.primary_action = "Maintain high sovereignty. Monitor for degradation."
            guidance.exercises = [
                "Regular R3 framework audits",
                "Prevent sovereignty regression",
                "Share learnings with other teams"
            ]

        # Store in history
        self.navigation_history.append(guidance)

        return guidance

    def should_rollback(self, guidance: NavigationGuidance) -> Tuple[bool, str]:
        """
        Determine if rollback to subcritical is recommended.

        Args:
            guidance: Current navigation guidance

        Returns:
            (should_rollback, reason)
        """
        # Only consider rollback during transition
        if guidance.stage != NavigationStage.TRANSITION_ZONE:
            return (False, "")

        # Check instability duration
        if self.instability_count >= self.INSTABILITY_DURATION:
            return (True, f"Prolonged instability detected ({self.instability_count} snapshots)")

        # Check safety checks
        if guidance.safety_checks:
            failed_checks = [k for k, v in guidance.safety_checks.items() if not v]

            if len(failed_checks) >= 3:  # More than half failed
                return (True, f"Multiple safety checks failed: {', '.join(failed_checks)}")

        return (False, "")

    def get_rollback_plan(self) -> Dict:
        """Generate rollback plan to revert to subcritical."""
        return {
            'action': 'ROLLBACK TO SUBCRITICAL',
            'steps': [
                '1. Reduce scope: Temporarily decrease z by reducing autonomy/efficiency targets',
                '2. Stabilize R2: Focus on coordination tools, not frameworks',
                '3. Reduce burden: Defer decisions, simplify processes',
                '4. Wait for stability: Allow z to settle below 0.85',
                '5. Retry transition: Approach critical point more gradually'
            ],
            'rationale': 'Safety mechanism to prevent cascade failure during unstable transition',
            'estimated_duration': '3-5 days'
        }

    def print_guidance(self, guidance: NavigationGuidance):
        """Print human-readable guidance."""
        print("=" * 80)
        print("CRITICAL POINT NAVIGATOR")
        print("=" * 80)
        print(f"\nStage: {guidance.stage.value.upper().replace('_', ' ')}")
        print(f"Z-coordinate: {guidance.z_current:.3f}")
        print(f"Distance to critical (z={guidance.z_target:.3f}): {guidance.distance_to_critical:.3f}")
        print(f"Status: {guidance.status.upper()}\n")

        print(f"PRIMARY ACTION:")
        print(f"  {guidance.primary_action}\n")

        if guidance.warnings:
            print("WARNINGS:")
            for warning in guidance.warnings:
                print(f"  • {warning}")
            print()

        if guidance.exercises:
            print("RECOMMENDED EXERCISES:")
            for exercise in guidance.exercises:
                print(f"  • {exercise}")
            print()

        if guidance.safety_checks:
            print("SAFETY CHECKS:")
            for check, passed in guidance.safety_checks.items():
                status = "✓" if passed else "✗"
                print(f"  {status} {check}")
            print()

        # Check rollback
        should_rollback, reason = self.should_rollback(guidance)
        if should_rollback:
            print("⚠ ROLLBACK RECOMMENDED ⚠")
            print(f"Reason: {reason}\n")

            plan = self.get_rollback_plan()
            print("ROLLBACK PLAN:")
            for step in plan['steps']:
                print(f"  {step}")
            print(f"\nEstimated duration: {plan['estimated_duration']}")

        print("=" * 80)


def main():
    """Demo critical point navigator."""
    from unified_cascade_mathematics_core import UnifiedCascadeFramework
    from unified_sovereignty_system import create_demo_burden, evolve_cascade_state

    print("=" * 80)
    print("CRITICAL POINT NAVIGATOR - Demo")
    print("=" * 80 + "\n")

    navigator = CriticalPointNavigator()
    framework = UnifiedCascadeFramework()

    # Start near critical point
    state = framework.compute_full_state(
        clarity=5.0, immunity=7.0, efficiency=6.5, autonomy=7.5
    )

    burden = create_demo_burden(state.phase_regime)

    print(f"Starting: z={state.z_coordinate:.3f}, phase={state.phase_regime}\n")

    # Navigate through critical point
    for step in range(8):
        # Get guidance
        guidance = navigator.get_navigation_guidance(state, burden)

        print(f"--- Step {step + 1} ---")
        print(f"z={guidance.z_current:.3f}, stage={guidance.stage.value}, status={guidance.status}")
        print(f"Action: {guidance.primary_action}")

        if guidance.warnings:
            print("Warnings:")
            for warning in guidance.warnings:
                print(f"  - {warning}")

        print()

        # Evolve state
        state = evolve_cascade_state(
            state,
            clarity_delta=0.2,
            immunity_delta=0.15,
            efficiency_delta=0.18,
            autonomy_delta=0.12
        )

        burden = create_demo_burden(state.phase_regime)

    # Final detailed guidance
    print("\n")
    final_guidance = navigator.get_navigation_guidance(state, burden)
    navigator.print_guidance(final_guidance)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
