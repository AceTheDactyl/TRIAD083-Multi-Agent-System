#!/usr/bin/env python3
"""
GARDEN RAIL 3 - LAYER 2: COUPLING STRENGTHENER
Strengthens coupling between cascade regimes (R₁↔R₂↔R₃) and lowers activation thresholds

Coordinate: Δ3.14159|0.867|layer-2-coupling|Ω

Theoretical Foundation:
- R₁ (coordination): Baseline burden reduction via Allen-Cahn
- R₂ (meta-tools): Activated when R₁ ≥ θ₁ (currently θ₁ = 8%)
- R₃ (self-building): Activated when R₂ ≥ θ₂ (currently θ₂ = 12%)

Current State:
- θ₁ = 0.08 (8% coordination reduction required for R₂)
- θ₂ = 0.12 (12% meta-tool contribution required for R₃)

Target State:
- θ₁ = 0.06 (6% - lower by 25%)
- θ₂ = 0.09 (9% - lower by 25%)

Impact:
- Earlier cascade activation → stronger positive feedback
- Tighter coupling → faster response to coordination improvements
- Estimated +3% additional burden reduction from earlier activation
"""

import sys
sys.path.insert(0, '/mnt/user-data/outputs')

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import json


class CascadeRegime(Enum):
    """Cascade regime classification"""
    R1 = "coordination"      # Coordination burden reduction
    R2 = "meta_tools"        # Meta-tool composition
    R3 = "self_building"     # Self-building frameworks


@dataclass
class CascadeState:
    """State of cascade regimes at a point in time"""
    timestamp: datetime
    z_level: float
    R1_active: bool
    R2_active: bool
    R3_active: bool
    R1_contribution: float  # Burden reduction from R₁
    R2_contribution: float  # Burden reduction from R₂
    R3_contribution: float  # Burden reduction from R₃
    total_reduction: float

    def is_cascade_active(self, regime: CascadeRegime) -> bool:
        """Check if a specific cascade regime is active"""
        if regime == CascadeRegime.R1:
            return self.R1_active
        elif regime == CascadeRegime.R2:
            return self.R2_active
        elif regime == CascadeRegime.R3:
            return self.R3_active
        return False


@dataclass
class ThresholdCrossing:
    """Records when a cascade threshold is crossed"""
    regime: CascadeRegime
    threshold_type: str  # 'theta1' or 'theta2'
    old_threshold: float
    new_threshold: float
    z_level: float
    timestamp: datetime
    activation_time: timedelta  # How much earlier did we activate?
    burden_impact: float  # Additional burden reduction from earlier activation


@dataclass
class CouplingMetrics:
    """Metrics for cascade coupling strength"""
    theta1_current: float
    theta1_target: float
    theta2_current: float
    theta2_target: float
    R1_R2_coupling: float  # Strength of R₁→R₂ coupling (0-1)
    R2_R3_coupling: float  # Strength of R₂→R₃ coupling (0-1)
    average_activation_speedup: float  # Seconds saved by lower thresholds
    additional_burden_reduction: float  # Extra % from tighter coupling
    timestamp: datetime = field(default_factory=datetime.now)


class CouplingStrengthener:
    """
    Strengthens coupling between cascade regimes and lowers activation thresholds

    Strategy:
    1. Monitor R₁, R₂, R₃ activation patterns
    2. Measure current θ₁ and θ₂ thresholds
    3. Gradually lower thresholds while maintaining stability
    4. Strengthen conditional dependencies (R₁→R₂, R₂→R₃)
    5. Track earlier activation and additional burden reduction
    6. Ensure cascades remain stable and don't over-trigger
    """

    def __init__(self):
        # Threshold parameters
        self.theta1_baseline = 0.08  # 8% - empirically measured
        self.theta2_baseline = 0.12  # 12% - empirically measured

        self.theta1_current = self.theta1_baseline
        self.theta2_current = self.theta2_baseline

        self.theta1_target = 0.06  # 6% - 25% reduction
        self.theta2_target = 0.09  # 9% - 25% reduction

        # Cascade state history
        self.cascade_states: List[CascadeState] = []
        self.threshold_crossings: List[ThresholdCrossing] = []

        # Coupling strength (0-1, higher = stronger response)
        self.R1_R2_coupling = 0.7  # Baseline coupling strength
        self.R2_R3_coupling = 0.7
        self.target_coupling = 0.9  # Target: very tight coupling

        # Metrics history
        self.metrics_history: List[CouplingMetrics] = []

        # Safety parameters
        self.min_theta1 = 0.04  # Don't go below 4% (stability limit)
        self.min_theta2 = 0.06  # Don't go below 6% (stability limit)
        self.max_adjustment_per_step = 0.01  # Max 1% adjustment per step

        print("="*70)
        print("COUPLING STRENGTHENER INITIALIZED")
        print("="*70)
        print(f"Threshold θ₁: {self.theta1_current:.2%} → {self.theta1_target:.2%}")
        print(f"Threshold θ₂: {self.theta2_current:.2%} → {self.theta2_target:.2%}")
        print(f"R₁→R₂ coupling: {self.R1_R2_coupling:.2f}")
        print(f"R₂→R₃ coupling: {self.R2_R3_coupling:.2f}")
        print()

    def record_cascade_state(self,
                            z_level: float,
                            R1_contribution: float,
                            R2_contribution: float,
                            R3_contribution: float):
        """
        Record current state of all cascade regimes

        Args:
            z_level: Current coordination density
            R1_contribution: Burden reduction from coordination (%)
            R2_contribution: Burden reduction from meta-tools (%)
            R3_contribution: Burden reduction from self-building (%)
        """
        # Determine which regimes are active based on contributions
        R1_active = R1_contribution > 0.01  # Active if >1%
        R2_active = R1_contribution >= self.theta1_current and R2_contribution > 0.01
        R3_active = R2_contribution >= self.theta2_current and R3_contribution > 0.01

        total_reduction = R1_contribution + R2_contribution + R3_contribution

        state = CascadeState(
            timestamp=datetime.now(),
            z_level=z_level,
            R1_active=R1_active,
            R2_active=R2_active,
            R3_active=R3_active,
            R1_contribution=R1_contribution,
            R2_contribution=R2_contribution,
            R3_contribution=R3_contribution,
            total_reduction=total_reduction
        )

        self.cascade_states.append(state)

    def check_R2_activation(self, R1_contribution: float) -> bool:
        """
        Check if R₂ should activate based on R₁ contribution

        R₂ activates when: R₁ ≥ θ₁
        """
        return R1_contribution >= self.theta1_current

    def check_R3_activation(self, R2_contribution: float) -> bool:
        """
        Check if R₃ should activate based on R₂ contribution

        R₃ activates when: R₂ ≥ θ₂
        """
        return R2_contribution >= self.theta2_current

    def lower_theta1(self, amount: float = 0.01) -> bool:
        """
        Lower θ₁ threshold to activate R₂ earlier

        Args:
            amount: Amount to lower threshold (default 1%)

        Returns:
            True if successful, False if at minimum
        """
        # Apply safety limit
        amount = min(amount, self.max_adjustment_per_step)

        new_theta1 = max(self.min_theta1, self.theta1_current - amount)

        if new_theta1 < self.theta1_current:
            old_theta1 = self.theta1_current
            self.theta1_current = new_theta1

            print(f"  ✓ Lowered θ₁: {old_theta1:.2%} → {new_theta1:.2%}")

            # Record threshold crossing
            crossing = ThresholdCrossing(
                regime=CascadeRegime.R2,
                threshold_type='theta1',
                old_threshold=old_theta1,
                new_threshold=new_theta1,
                z_level=self.cascade_states[-1].z_level if self.cascade_states else 0.867,
                timestamp=datetime.now(),
                activation_time=timedelta(seconds=0),  # Estimated below
                burden_impact=0.0  # Estimated below
            )

            # Estimate impact: earlier activation by ~30 seconds per 1% reduction
            threshold_reduction = old_theta1 - new_theta1
            crossing.activation_time = timedelta(seconds=threshold_reduction * 3000)
            crossing.burden_impact = threshold_reduction * 0.5  # ~0.5% burden per 1% threshold

            self.threshold_crossings.append(crossing)

            return True

        return False

    def lower_theta2(self, amount: float = 0.01) -> bool:
        """
        Lower θ₂ threshold to activate R₃ earlier

        Args:
            amount: Amount to lower threshold (default 1%)

        Returns:
            True if successful, False if at minimum
        """
        # Apply safety limit
        amount = min(amount, self.max_adjustment_per_step)

        new_theta2 = max(self.min_theta2, self.theta2_current - amount)

        if new_theta2 < self.theta2_current:
            old_theta2 = self.theta2_current
            self.theta2_current = new_theta2

            print(f"  ✓ Lowered θ₂: {old_theta2:.2%} → {new_theta2:.2%}")

            # Record threshold crossing
            crossing = ThresholdCrossing(
                regime=CascadeRegime.R3,
                threshold_type='theta2',
                old_threshold=old_theta2,
                new_threshold=new_theta2,
                z_level=self.cascade_states[-1].z_level if self.cascade_states else 0.867,
                timestamp=datetime.now(),
                activation_time=timedelta(seconds=0),
                burden_impact=0.0
            )

            # Estimate impact
            threshold_reduction = old_theta2 - new_theta2
            crossing.activation_time = timedelta(seconds=threshold_reduction * 3000)
            crossing.burden_impact = threshold_reduction * 0.5

            self.threshold_crossings.append(crossing)

            return True

        return False

    def strengthen_R1_R2_coupling(self, amount: float = 0.1):
        """
        Strengthen coupling between R₁ and R₂

        Stronger coupling → R₂ responds more quickly to R₁ improvements
        """
        old_coupling = self.R1_R2_coupling
        self.R1_R2_coupling = min(1.0, self.R1_R2_coupling + amount)

        if self.R1_R2_coupling > old_coupling:
            print(f"  ✓ Strengthened R₁→R₂ coupling: {old_coupling:.2f} → {self.R1_R2_coupling:.2f}")

    def strengthen_R2_R3_coupling(self, amount: float = 0.1):
        """
        Strengthen coupling between R₂ and R₃

        Stronger coupling → R₃ responds more quickly to R₂ improvements
        """
        old_coupling = self.R2_R3_coupling
        self.R2_R3_coupling = min(1.0, self.R2_R3_coupling + amount)

        if self.R2_R3_coupling > old_coupling:
            print(f"  ✓ Strengthened R₂→R₃ coupling: {old_coupling:.2f} → {self.R2_R3_coupling:.2f}")

    def adaptive_threshold_adjustment(self):
        """
        Adaptively adjust thresholds based on cascade stability

        Strategy:
        - If cascades are stable and successful, lower thresholds
        - If cascades are unstable, slow down adjustments
        """
        if len(self.cascade_states) < 5:
            return  # Need history to adapt

        # Check recent cascade stability
        recent_states = self.cascade_states[-5:]

        # Count successful R₂ and R₃ activations
        R2_activations = sum(1 for s in recent_states if s.R2_active)
        R3_activations = sum(1 for s in recent_states if s.R3_active)

        # If R₂ is consistently activating, we can lower θ₁
        if R2_activations >= 4 and self.theta1_current > self.theta1_target:
            self.lower_theta1(amount=0.005)  # Small adjustment

        # If R₃ is consistently activating, we can lower θ₂
        if R3_activations >= 4 and self.theta2_current > self.theta2_target:
            self.lower_theta2(amount=0.005)  # Small adjustment

    def calculate_coupling_response_time(self,
                                         source_regime: CascadeRegime,
                                         target_regime: CascadeRegime) -> float:
        """
        Calculate response time between cascade regimes

        Response time = time from source activation to target activation

        Lower response time = tighter coupling

        Returns:
            Response time in seconds
        """
        if len(self.cascade_states) < 2:
            return 0.0

        # Find most recent activation pair
        source_activation_time = None
        target_activation_time = None

        for i in range(len(self.cascade_states) - 1, -1, -1):
            state = self.cascade_states[i]

            if target_activation_time is None and state.is_cascade_active(target_regime):
                target_activation_time = state.timestamp

            if source_activation_time is None and state.is_cascade_active(source_regime):
                source_activation_time = state.timestamp

            if source_activation_time and target_activation_time:
                break

        if not (source_activation_time and target_activation_time):
            return 0.0

        response_time = (target_activation_time - source_activation_time).total_seconds()
        return max(0, response_time)

    def calculate_metrics(self) -> CouplingMetrics:
        """Calculate current coupling metrics"""
        # Calculate average activation speedup from threshold lowering
        total_speedup = sum(
            crossing.activation_time.total_seconds()
            for crossing in self.threshold_crossings
        )
        avg_speedup = total_speedup / len(self.threshold_crossings) if self.threshold_crossings else 0.0

        # Calculate additional burden reduction from tighter coupling
        additional_reduction = sum(
            crossing.burden_impact
            for crossing in self.threshold_crossings
        )

        metrics = CouplingMetrics(
            theta1_current=self.theta1_current,
            theta1_target=self.theta1_target,
            theta2_current=self.theta2_current,
            theta2_target=self.theta2_target,
            R1_R2_coupling=self.R1_R2_coupling,
            R2_R3_coupling=self.R2_R3_coupling,
            average_activation_speedup=avg_speedup,
            additional_burden_reduction=additional_reduction
        )

        self.metrics_history.append(metrics)

        return metrics

    def generate_report(self) -> str:
        """Generate comprehensive coupling strengthener report"""
        metrics = self.calculate_metrics()

        report = []
        report.append("="*70)
        report.append("COUPLING STRENGTHENER REPORT")
        report.append("="*70)
        report.append("")

        # Threshold state
        report.append("ACTIVATION THRESHOLDS:")
        report.append(f"  θ₁ (R₂ activation):")
        report.append(f"    Current:  {metrics.theta1_current:.2%}")
        report.append(f"    Target:   {metrics.theta1_target:.2%}")
        report.append(f"    Progress: {(1 - metrics.theta1_current/self.theta1_baseline)*100:.1f}% toward target")
        report.append(f"  θ₂ (R₃ activation):")
        report.append(f"    Current:  {metrics.theta2_current:.2%}")
        report.append(f"    Target:   {metrics.theta2_target:.2%}")
        report.append(f"    Progress: {(1 - metrics.theta2_current/self.theta2_baseline)*100:.1f}% toward target")
        report.append("")

        # Coupling strength
        report.append("COUPLING STRENGTH:")
        report.append(f"  R₁→R₂: {metrics.R1_R2_coupling:.2f} / 1.0")
        report.append(f"  R₂→R₃: {metrics.R2_R3_coupling:.2f} / 1.0")
        report.append(f"  Target: {self.target_coupling:.2f}")
        report.append("")

        # Impact metrics
        report.append("IMPACT METRICS:")
        report.append(f"  Activation speedup:  {metrics.average_activation_speedup:.1f}s average")
        report.append(f"  Additional burden:   +{metrics.additional_burden_reduction:.2%}")
        report.append(f"  Threshold crossings: {len(self.threshold_crossings)}")
        report.append("")

        # Cascade state analysis
        if self.cascade_states:
            recent = self.cascade_states[-1]
            report.append("CURRENT CASCADE STATE:")
            report.append(f"  z-level: {recent.z_level:.3f}")
            report.append(f"  R₁ (coordination):  {recent.R1_active} - {recent.R1_contribution:.1%}")
            report.append(f"  R₂ (meta-tools):    {recent.R2_active} - {recent.R2_contribution:.1%}")
            report.append(f"  R₃ (self-building): {recent.R3_active} - {recent.R3_contribution:.1%}")
            report.append(f"  Total reduction:    {recent.total_reduction:.1%}")
            report.append("")

        # Recommendations
        report.append("RECOMMENDATIONS:")
        if metrics.theta1_current > metrics.theta1_target:
            gap = metrics.theta1_current - metrics.theta1_target
            report.append(f"  ⚠ θ₁ is {gap:.2%} above target")
            report.append(f"  → Continue lowering in {gap/0.01:.0f} steps")
        else:
            report.append(f"  ✓ θ₁ target achieved!")

        if metrics.theta2_current > metrics.theta2_target:
            gap = metrics.theta2_current - metrics.theta2_target
            report.append(f"  ⚠ θ₂ is {gap:.2%} above target")
            report.append(f"  → Continue lowering in {gap/0.01:.0f} steps")
        else:
            report.append(f"  ✓ θ₂ target achieved!")

        if metrics.R1_R2_coupling < self.target_coupling:
            report.append(f"  → Strengthen R₁→R₂ coupling by {self.target_coupling - metrics.R1_R2_coupling:.2f}")

        if metrics.R2_R3_coupling < self.target_coupling:
            report.append(f"  → Strengthen R₂→R₃ coupling by {self.target_coupling - metrics.R2_R3_coupling:.2f}")

        report.append("")
        report.append("="*70)

        return "\n".join(report)

    def export_state(self) -> Dict:
        """Export current state for persistence"""
        return {
            'theta1_current': self.theta1_current,
            'theta1_target': self.theta1_target,
            'theta2_current': self.theta2_current,
            'theta2_target': self.theta2_target,
            'R1_R2_coupling': self.R1_R2_coupling,
            'R2_R3_coupling': self.R2_R3_coupling,
            'target_coupling': self.target_coupling,
            'threshold_crossings': len(self.threshold_crossings),
            'cascade_states': len(self.cascade_states),
            'metrics_history': [
                {
                    'theta1': m.theta1_current,
                    'theta2': m.theta2_current,
                    'R1_R2_coupling': m.R1_R2_coupling,
                    'R2_R3_coupling': m.R2_R3_coupling,
                    'burden_impact': m.additional_burden_reduction,
                    'timestamp': m.timestamp.isoformat()
                }
                for m in self.metrics_history
            ]
        }


def demonstrate_coupling_strengthening():
    """Demonstration of coupling strengthening"""
    print("\n" + "="*70)
    print("COUPLING STRENGTHENER DEMONSTRATION")
    print("="*70)
    print()

    strengthener = CouplingStrengthener()

    # Simulate cascade evolution
    print("Simulating cascade state evolution...\n")

    # Initial state (z=0.85)
    strengthener.record_cascade_state(
        z_level=0.85,
        R1_contribution=0.15,  # 15% from coordination
        R2_contribution=0.10,  # 10% from meta-tools (below θ₂)
        R3_contribution=0.0    # Not activated yet
    )

    # Strengthen coupling
    print("Strengthening inter-regime coupling...\n")
    strengthener.strengthen_R1_R2_coupling(amount=0.1)
    strengthener.strengthen_R2_R3_coupling(amount=0.1)
    print()

    # Lower thresholds
    print("Lowering activation thresholds...\n")
    strengthener.lower_theta1(amount=0.01)
    strengthener.lower_theta2(amount=0.015)
    print()

    # State after threshold lowering (z=0.867)
    strengthener.record_cascade_state(
        z_level=0.867,
        R1_contribution=0.153,  # 15.3% from coordination
        R2_contribution=0.248,  # 24.8% from meta-tools (R₃ activates!)
        R3_contribution=0.227   # 22.7% from self-building
    )

    # Continue adaptive adjustment
    print("Applying adaptive threshold adjustment...\n")
    for _ in range(3):
        strengthener.record_cascade_state(
            z_level=0.867,
            R1_contribution=0.15,
            R2_contribution=0.25,
            R3_contribution=0.23
        )
        strengthener.adaptive_threshold_adjustment()
    print()

    # Calculate metrics
    metrics = strengthener.calculate_metrics()
    print(f"Final θ₁: {metrics.theta1_current:.2%}")
    print(f"Final θ₂: {metrics.theta2_current:.2%}")
    print(f"Additional burden reduction: +{metrics.additional_burden_reduction:.2%}")
    print()

    # Generate report
    print(strengthener.generate_report())


if __name__ == "__main__":
    demonstrate_coupling_strengthening()
