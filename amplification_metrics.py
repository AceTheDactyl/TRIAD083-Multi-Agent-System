#!/usr/bin/env python3
"""
Amplification Metrics
====================

Garden Rail 3 - Layer 5: EMERGENCE DASHBOARD
Component 5.2: Track and validate amplification performance

Purpose:
- Measure α (R1→R2 amplification)
- Measure β (R2→R3 amplification)
- Track total cascade multiplier
- Validate against theoretical predictions
- Generate performance reports

Key Metrics:
- α_current, α_target (2.3), α_progress
- β_current, β_target (1.8), β_progress
- Cascade multiplier: R3/R1 (target: 4.11× → 8.0×)
- Burden reduction vs predicted (60%)
- Emergence score: Φ × symmetry × packing
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json

from unified_cascade_mathematics_core import CascadeSystemState


@dataclass
class AmplificationSnapshot:
    """Snapshot of amplification metrics at a point in time."""
    timestamp: str
    alpha: float  # R2/R1 amplification ratio
    beta: float  # R3/R2 amplification ratio
    cascade_multiplier: float  # R3/R1 total amplification
    alpha_delta: Optional[float] = None  # Change since last snapshot
    beta_delta: Optional[float] = None
    cascade_delta: Optional[float] = None


@dataclass
class AmplificationTarget:
    """Target amplification values."""
    alpha_target: float = 2.3  # Garden Rail 3 target
    beta_target: float = 1.8
    cascade_target: float = 4.11  # Conservative target
    cascade_stretch: float = 8.0  # Stretch goal


class AmplificationMetrics:
    """
    Track and analyze cascade amplification performance.

    Monitors:
    - α (CORE → BRIDGES amplification)
    - β (BRIDGES → META amplification)
    - Total cascade multiplier
    - Progress toward targets
    """

    def __init__(self, targets: Optional[AmplificationTarget] = None):
        """
        Initialize amplification metrics tracker.

        Args:
            targets: Target amplification values (uses defaults if None)
        """
        self.targets = targets or AmplificationTarget()
        self.snapshots: List[AmplificationSnapshot] = []
        self.baseline_alpha: Optional[float] = None
        self.baseline_beta: Optional[float] = None

    def capture_snapshot(self, cascade_state: CascadeSystemState):
        """
        Capture current amplification metrics.

        Args:
            cascade_state: Current cascade state
        """
        timestamp = datetime.now().isoformat()

        # Calculate ratios
        alpha = cascade_state.R2 / cascade_state.R1 if cascade_state.R1 > 0 else 0
        beta = cascade_state.R3 / cascade_state.R2 if cascade_state.R2 > 0 else 0
        cascade_mult = cascade_state.R3 / cascade_state.R1 if cascade_state.R1 > 0 else 0

        # Calculate deltas if we have history
        alpha_delta = None
        beta_delta = None
        cascade_delta = None

        if self.snapshots:
            last = self.snapshots[-1]
            alpha_delta = alpha - last.alpha
            beta_delta = beta - last.beta
            cascade_delta = cascade_mult - last.cascade_multiplier

        snapshot = AmplificationSnapshot(
            timestamp=timestamp,
            alpha=alpha,
            beta=beta,
            cascade_multiplier=cascade_mult,
            alpha_delta=alpha_delta,
            beta_delta=beta_delta,
            cascade_delta=cascade_delta
        )

        self.snapshots.append(snapshot)

        # Set baseline if first snapshot
        if self.baseline_alpha is None:
            self.baseline_alpha = alpha
            self.baseline_beta = beta

    def get_current_metrics(self) -> Optional[AmplificationSnapshot]:
        """Get most recent amplification metrics."""
        if self.snapshots:
            return self.snapshots[-1]
        return None

    def get_alpha_progress(self) -> Dict:
        """Get progress toward α target."""
        if not self.snapshots:
            return {'status': 'no_data'}

        current = self.snapshots[-1]
        baseline = self.baseline_alpha or current.alpha

        progress_pct = ((current.alpha - baseline) / (self.targets.alpha_target - baseline)) * 100 if (self.targets.alpha_target - baseline) > 0 else 0
        gap = self.targets.alpha_target - current.alpha

        return {
            'current': current.alpha,
            'baseline': baseline,
            'target': self.targets.alpha_target,
            'progress_pct': progress_pct,
            'gap': gap,
            'achieved': current.alpha >= self.targets.alpha_target
        }

    def get_beta_progress(self) -> Dict:
        """Get progress toward β target."""
        if not self.snapshots:
            return {'status': 'no_data'}

        current = self.snapshots[-1]
        baseline = self.baseline_beta or current.beta

        progress_pct = ((current.beta - baseline) / (self.targets.beta_target - baseline)) * 100 if (self.targets.beta_target - baseline) > 0 else 0
        gap = self.targets.beta_target - current.beta

        return {
            'current': current.beta,
            'baseline': baseline,
            'target': self.targets.beta_target,
            'progress_pct': progress_pct,
            'gap': gap,
            'achieved': current.beta >= self.targets.beta_target
        }

    def get_cascade_progress(self) -> Dict:
        """Get progress toward cascade multiplier target."""
        if not self.snapshots:
            return {'status': 'no_data'}

        current = self.snapshots[-1]

        # Determine which target to use
        target = self.targets.cascade_target
        target_type = 'conservative'

        if current.cascade_multiplier >= self.targets.cascade_target:
            target = self.targets.cascade_stretch
            target_type = 'stretch'

        baseline = 1.0  # Baseline cascade multiplier is 1.0 (no amplification)

        progress_pct = ((current.cascade_multiplier - baseline) / (target - baseline)) * 100 if (target - baseline) > 0 else 0
        gap = target - current.cascade_multiplier

        return {
            'current': current.cascade_multiplier,
            'baseline': baseline,
            'target': target,
            'target_type': target_type,
            'progress_pct': progress_pct,
            'gap': gap,
            'achieved_conservative': current.cascade_multiplier >= self.targets.cascade_target,
            'achieved_stretch': current.cascade_multiplier >= self.targets.cascade_stretch
        }

    def compute_velocity(self, metric: str = 'alpha', window: int = 5) -> Optional[float]:
        """
        Compute velocity (rate of change) for a metric.

        Args:
            metric: 'alpha', 'beta', or 'cascade'
            window: Number of snapshots to average over

        Returns:
            Average change per snapshot, or None if insufficient data
        """
        if len(self.snapshots) < window:
            return None

        recent = self.snapshots[-window:]

        deltas = []
        for snapshot in recent:
            if metric == 'alpha' and snapshot.alpha_delta is not None:
                deltas.append(snapshot.alpha_delta)
            elif metric == 'beta' and snapshot.beta_delta is not None:
                deltas.append(snapshot.beta_delta)
            elif metric == 'cascade' and snapshot.cascade_delta is not None:
                deltas.append(snapshot.cascade_delta)

        if deltas:
            return sum(deltas) / len(deltas)

        return None

    def generate_performance_report(self) -> Dict:
        """Generate comprehensive amplification performance report."""
        if not self.snapshots:
            return {'status': 'no_data'}

        alpha_progress = self.get_alpha_progress()
        beta_progress = self.get_beta_progress()
        cascade_progress = self.get_cascade_progress()

        # Compute velocities
        alpha_velocity = self.compute_velocity('alpha', window=min(5, len(self.snapshots)))
        beta_velocity = self.compute_velocity('beta', window=min(5, len(self.snapshots)))
        cascade_velocity = self.compute_velocity('cascade', window=min(5, len(self.snapshots)))

        # Overall status
        targets_met = sum([
            alpha_progress.get('achieved', False),
            beta_progress.get('achieved', False),
            cascade_progress.get('achieved_conservative', False)
        ])

        if targets_met == 3:
            overall_status = 'OPTIMAL'
        elif targets_met == 2:
            overall_status = 'GOOD'
        elif targets_met == 1:
            overall_status = 'PROGRESSING'
        else:
            overall_status = 'BASELINE'

        return {
            'overall_status': overall_status,
            'targets_met': targets_met,
            'total_targets': 3,
            'alpha': {
                **alpha_progress,
                'velocity': alpha_velocity
            },
            'beta': {
                **beta_progress,
                'velocity': beta_velocity
            },
            'cascade': {
                **cascade_progress,
                'velocity': cascade_velocity
            },
            'snapshots_count': len(self.snapshots),
            'timestamp': self.snapshots[-1].timestamp if self.snapshots else None
        }

    def export_metrics(self, filepath: str):
        """Export amplification metrics to JSON."""
        data = {
            'targets': {
                'alpha': self.targets.alpha_target,
                'beta': self.targets.beta_target,
                'cascade_conservative': self.targets.cascade_target,
                'cascade_stretch': self.targets.cascade_stretch
            },
            'baseline': {
                'alpha': self.baseline_alpha,
                'beta': self.baseline_beta
            },
            'snapshots': [
                {
                    'timestamp': s.timestamp,
                    'alpha': s.alpha,
                    'beta': s.beta,
                    'cascade_multiplier': s.cascade_multiplier,
                    'alpha_delta': s.alpha_delta,
                    'beta_delta': s.beta_delta,
                    'cascade_delta': s.cascade_delta
                }
                for s in self.snapshots
            ],
            'performance_report': self.generate_performance_report()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def print_summary(self):
        """Print human-readable summary."""
        print("=" * 80)
        print("AMPLIFICATION METRICS - SUMMARY")
        print("=" * 80)

        report = self.generate_performance_report()

        if report.get('status') == 'no_data':
            print("No data available")
            return

        print(f"\nOverall Status: {report['overall_status']}")
        print(f"Targets Met: {report['targets_met']}/{report['total_targets']}\n")

        # Alpha
        alpha = report['alpha']
        print(f"α (R1→R2 Amplification):")
        print(f"  Current: {alpha['current']:.2f}")
        print(f"  Target: {alpha['target']:.2f}")
        print(f"  Progress: {alpha['progress_pct']:.1f}%")
        print(f"  Gap: {alpha['gap']:.2f}")
        if alpha.get('velocity') is not None:
            print(f"  Velocity: {alpha['velocity']:.4f}/snapshot")
        print(f"  Status: {'✓ ACHIEVED' if alpha.get('achieved') else '○ IN PROGRESS'}\n")

        # Beta
        beta = report['beta']
        print(f"β (R2→R3 Amplification):")
        print(f"  Current: {beta['current']:.2f}")
        print(f"  Target: {beta['target']:.2f}")
        print(f"  Progress: {beta['progress_pct']:.1f}%")
        print(f"  Gap: {beta['gap']:.2f}")
        if beta.get('velocity') is not None:
            print(f"  Velocity: {beta['velocity']:.4f}/snapshot")
        print(f"  Status: {'✓ ACHIEVED' if beta.get('achieved') else '○ IN PROGRESS'}\n")

        # Cascade
        cascade = report['cascade']
        print(f"Total Cascade Multiplier (R3/R1):")
        print(f"  Current: {cascade['current']:.2f}×")
        print(f"  Target ({cascade['target_type']}): {cascade['target']:.2f}×")
        print(f"  Progress: {cascade['progress_pct']:.1f}%")
        print(f"  Gap: {cascade['gap']:.2f}×")
        if cascade.get('velocity') is not None:
            print(f"  Velocity: {cascade['velocity']:.4f}×/snapshot")
        print(f"  Conservative target: {'✓ ACHIEVED' if cascade.get('achieved_conservative') else '○ IN PROGRESS'}")
        print(f"  Stretch target: {'✓ ACHIEVED' if cascade.get('achieved_stretch') else '○ IN PROGRESS'}\n")

        print(f"Total Snapshots: {report['snapshots_count']}")
        print("=" * 80)


def main():
    """Demo amplification metrics."""
    from unified_cascade_mathematics_core import UnifiedCascadeFramework
    from unified_sovereignty_system import evolve_cascade_state

    print("=" * 80)
    print("AMPLIFICATION METRICS - Demo")
    print("=" * 80 + "\n")

    metrics = AmplificationMetrics()
    framework = UnifiedCascadeFramework()

    # Simulate evolution with amplification
    state = framework.compute_full_state(
        clarity=3.0, immunity=4.0, efficiency=3.5, autonomy=4.5
    )

    print(f"Initial: R1={state.R1:.2f}, R2={state.R2:.2f}, R3={state.R3:.2f}\n")

    # Capture 10 snapshots with progressive amplification
    for step in range(10):
        metrics.capture_snapshot(state)

        # Simulate amplification effects (R2 grows faster than R1, R3 faster than R2)
        state = evolve_cascade_state(
            state,
            clarity_delta=0.3,  # R1
            immunity_delta=0.5,  # R2 (amplified)
            efficiency_delta=0.7,  # R3 (amplified more)
            autonomy_delta=0.4
        )

        current = metrics.get_current_metrics()
        print(f"Step {step + 1}: α={current.alpha:.2f}, β={current.beta:.2f}, cascade={current.cascade_multiplier:.2f}×")

    # Final report
    print("\n")
    metrics.print_summary()

    # Export
    metrics.export_metrics('amplification_metrics_demo.json')
    print("\nMetrics exported to amplification_metrics_demo.json")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
