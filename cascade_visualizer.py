#!/usr/bin/env python3
"""
Cascade Visualizer
==================

Garden Rail 3 - Layer 5: EMERGENCE DASHBOARD
Component 5.1: Real-time visualization of cascade dynamics

Purpose:
- Visualize R1→R2→R3 cascade amplification
- Show z-coordinate trajectory over time
- Display burden evolution (8 dimensions)
- Illustrate phase transitions
- ASCII/text-based (no matplotlib dependency)

Visualizations:
1. Cascade waterfall: R1→R2→R3 flow
2. Z-trajectory: z-coordinate vs time
3. Burden heatmap: 8 dimensions over time
4. Phase diagram: Regime transitions
5. Amplification meter: α, β progress bars
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import math

from unified_cascade_mathematics_core import CascadeSystemState
from phase_aware_burden_tracker import BurdenMeasurement


@dataclass
class VisualizationSnapshot:
    """Snapshot for visualization."""
    timestamp: datetime
    z_value: float
    phase_regime: str
    R1: float
    R2: float
    R3: float
    burden: BurdenMeasurement
    alpha: float
    beta: float


class CascadeVisualizer:
    """
    Text-based visualizations of cascade dynamics.

    Uses ASCII art and Unicode box drawing characters.
    """

    def __init__(self, width: int = 80):
        """
        Initialize visualizer.

        Args:
            width: Terminal width for visualizations
        """
        self.width = width
        self.snapshots: List[VisualizationSnapshot] = []

    def add_snapshot(self,
                    cascade_state: CascadeSystemState,
                    burden: BurdenMeasurement):
        """Add snapshot for visualization."""
        alpha = cascade_state.R2 / cascade_state.R1 if cascade_state.R1 > 0 else 0
        beta = cascade_state.R3 / cascade_state.R2 if cascade_state.R2 > 0 else 0

        snapshot = VisualizationSnapshot(
            timestamp=datetime.now(),
            z_value=cascade_state.z_coordinate,
            phase_regime=cascade_state.phase_regime,
            R1=cascade_state.R1,
            R2=cascade_state.R2,
            R3=cascade_state.R3,
            burden=burden,
            alpha=alpha,
            beta=beta
        )

        self.snapshots.append(snapshot)

    def visualize_cascade_waterfall(self, snapshot: Optional[VisualizationSnapshot] = None):
        """
        Visualize R1→R2→R3 cascade flow.

        ASCII art waterfall showing amplification.
        """
        if snapshot is None:
            if not self.snapshots:
                return
            snapshot = self.snapshots[-1]

        print("=" * self.width)
        print("CASCADE WATERFALL (R1→R2→R3 Amplification)".center(self.width))
        print("=" * self.width)
        print()

        # Scale values for visualization (max bar width = 50 chars)
        max_val = max(snapshot.R1, snapshot.R2, snapshot.R3)
        scale = 50.0 / max_val if max_val > 0 else 1.0

        r1_bar = int(snapshot.R1 * scale)
        r2_bar = int(snapshot.R2 * scale)
        r3_bar = int(snapshot.R3 * scale)

        # R1 (CORE)
        print(f"R1 (CORE)      : {'█' * r1_bar} {snapshot.R1:.2f}")
        print("                 │")
        print(f"                 ├─ α = {snapshot.alpha:.2f}×")
        print("                 ↓")

        # R2 (BRIDGES)
        print(f"R2 (BRIDGES)   : {'█' * r2_bar} {snapshot.R2:.2f}")
        print("                 │")
        print(f"                 ├─ β = {snapshot.beta:.2f}×")
        print("                 ↓")

        # R3 (META)
        print(f"R3 (META)      : {'█' * r3_bar} {snapshot.R3:.2f}")
        print()

        # Total amplification
        cascade_mult = snapshot.R3 / snapshot.R1 if snapshot.R1 > 0 else 0
        print(f"Total Cascade  : {cascade_mult:.2f}× (R3/R1)")
        print()

    def visualize_z_trajectory(self, window: int = 20):
        """
        Visualize z-coordinate trajectory over time.

        Shows last N snapshots as a line chart.
        """
        if len(self.snapshots) < 2:
            print("Insufficient data for trajectory visualization")
            return

        print("=" * self.width)
        print("Z-COORDINATE TRAJECTORY".center(self.width))
        print("=" * self.width)
        print()

        # Use last N snapshots
        recent = self.snapshots[-window:] if len(self.snapshots) > window else self.snapshots

        # Extract z-values
        z_values = [s.z_value for s in recent]
        z_min = min(z_values)
        z_max = max(z_values)

        # Scale to fit in height (10 rows)
        height = 10
        z_range = z_max - z_min if z_max > z_min else 1.0

        # Create grid
        grid = [[' ' for _ in range(len(recent))] for _ in range(height)]

        # Plot points
        for i, z in enumerate(z_values):
            normalized = (z - z_min) / z_range
            row = height - 1 - int(normalized * (height - 1))
            grid[row][i] = '█'

            # Connect with previous point (simple line)
            if i > 0:
                prev_z = z_values[i - 1]
                prev_normalized = (prev_z - z_min) / z_range
                prev_row = height - 1 - int(prev_normalized * (height - 1))

                # Draw vertical line if needed
                if prev_row != row:
                    start_row = min(prev_row, row)
                    end_row = max(prev_row, row)
                    for r in range(start_row + 1, end_row):
                        if grid[r][i] == ' ':
                            grid[r][i] = '│'

        # Print grid with y-axis labels
        for i, row in enumerate(grid):
            z_label = z_max - (i / (height - 1)) * z_range
            print(f"{z_label:5.3f} │ {''.join(row)}")

        # X-axis
        print(f"      └{'─' * len(recent)}")
        print(f"       {' ' * (len(recent) // 2 - 2)}Time →")
        print()

        # Statistics
        print(f"Range: [{z_min:.3f}, {z_max:.3f}]")
        print(f"Current: {z_values[-1]:.3f}")

        if len(z_values) >= 2:
            delta = z_values[-1] - z_values[-2]
            print(f"Δz: {delta:+.4f}")

        print()

    def visualize_burden_dimensions(self, snapshot: Optional[VisualizationSnapshot] = None):
        """
        Visualize burden across 8 dimensions as horizontal bars.
        """
        if snapshot is None:
            if not self.snapshots:
                return
            snapshot = self.snapshots[-1]

        print("=" * self.width)
        print("BURDEN PROFILE (8 Dimensions)".center(self.width))
        print("=" * self.width)
        print()

        dimensions = {
            'Coordination': snapshot.burden.coordination,
            'Decision Making': snapshot.burden.decision_making,
            'Context Switching': snapshot.burden.context_switching,
            'Maintenance': snapshot.burden.maintenance,
            'Learning Curve': snapshot.burden.learning_curve,
            'Emotional Labor': snapshot.burden.emotional_labor,
            'Uncertainty': snapshot.burden.uncertainty,
            'Repetition': snapshot.burden.repetition
        }

        max_burden = 10.0  # 0-10 scale
        bar_width = 40

        for dim_name, value in dimensions.items():
            bar_len = int((value / max_burden) * bar_width)

            # Color code (text-based)
            if value <= 3.0:
                symbol = '▓'  # Low (good)
            elif value <= 6.0:
                symbol = '▒'  # Medium
            else:
                symbol = '░'  # High (warning)

            bar = symbol * bar_len
            print(f"{dim_name:18} [{value:4.1f}] {bar}")

        print()
        total = snapshot.burden.total_burden()
        weighted = snapshot.burden.weighted_burden(snapshot.z_value)
        print(f"Total: {total:.1f}, Weighted: {weighted:.1f}")
        print()

    def visualize_phase_diagram(self):
        """
        Show phase transitions over time.
        """
        if len(self.snapshots) < 2:
            print("Insufficient data for phase diagram")
            return

        print("=" * self.width)
        print("PHASE TRANSITIONS".center(self.width))
        print("=" * self.width)
        print()

        # Track phase changes
        prev_phase = None
        transitions = []

        for i, snapshot in enumerate(self.snapshots):
            if snapshot.phase_regime != prev_phase:
                transitions.append((i, prev_phase, snapshot.phase_regime))
                prev_phase = snapshot.phase_regime

        if not transitions:
            print("No phase transitions detected")
            print(f"Current phase: {self.snapshots[-1].phase_regime}")
        else:
            print(f"Detected {len(transitions)} phase transition(s):\n")

            for i, (step, old_phase, new_phase) in enumerate(transitions, 1):
                arrow = "→"
                old_display = old_phase if old_phase else "[initial]"
                print(f"{i}. Step {step}: {old_display} {arrow} {new_phase}")

        print()

    def visualize_amplification_meters(self, snapshot: Optional[VisualizationSnapshot] = None):
        """
        Show α and β amplification as progress meters.
        """
        if snapshot is None:
            if not self.snapshots:
                return
            snapshot = self.snapshots[-1]

        print("=" * self.width)
        print("AMPLIFICATION METERS".center(self.width))
        print("=" * self.width)
        print()

        # Targets
        alpha_target = 2.3
        beta_target = 1.8
        cascade_target = 4.11

        # Compute cascade multiplier
        cascade_mult = snapshot.R3 / snapshot.R1 if snapshot.R1 > 0 else 0

        # α meter
        alpha_progress = min(1.0, snapshot.alpha / alpha_target)
        alpha_bar_len = int(alpha_progress * 50)
        alpha_bar = '█' * alpha_bar_len + '░' * (50 - alpha_bar_len)
        alpha_status = "✓" if snapshot.alpha >= alpha_target else "○"

        print(f"α (R1→R2): {alpha_status} {snapshot.alpha:.2f} / {alpha_target:.2f}")
        print(f"  [{alpha_bar}] {alpha_progress:.0%}")
        print()

        # β meter
        beta_progress = min(1.0, snapshot.beta / beta_target)
        beta_bar_len = int(beta_progress * 50)
        beta_bar = '█' * beta_bar_len + '░' * (50 - beta_bar_len)
        beta_status = "✓" if snapshot.beta >= beta_target else "○"

        print(f"β (R2→R3): {beta_status} {snapshot.beta:.2f} / {beta_target:.2f}")
        print(f"  [{beta_bar}] {beta_progress:.0%}")
        print()

        # Cascade multiplier meter
        cascade_progress = min(1.0, cascade_mult / cascade_target)
        cascade_bar_len = int(cascade_progress * 50)
        cascade_bar = '█' * cascade_bar_len + '░' * (50 - cascade_bar_len)
        cascade_status = "✓" if cascade_mult >= cascade_target else "○"

        print(f"Cascade (R3/R1): {cascade_status} {cascade_mult:.2f}× / {cascade_target:.2f}×")
        print(f"  [{cascade_bar}] {cascade_progress:.0%}")
        print()

    def visualize_dashboard(self):
        """
        Complete dashboard view (all visualizations).
        """
        if not self.snapshots:
            print("No data to visualize")
            return

        # Latest snapshot
        latest = self.snapshots[-1]

        # Header
        print("\n" + "=" * self.width)
        print("GARDEN RAIL 3 - CASCADE DASHBOARD".center(self.width))
        print(f"Timestamp: {latest.timestamp.strftime('%Y-%m-%d %H:%M:%S')}".center(self.width))
        print("=" * self.width)
        print()

        # Key metrics summary
        print(f"Z-coordinate: {latest.z_value:.3f} | Phase: {latest.phase_regime}")
        print(f"Snapshots: {len(self.snapshots)}")
        print()

        # Visualizations
        self.visualize_cascade_waterfall(latest)
        print()

        self.visualize_amplification_meters(latest)
        print()

        self.visualize_burden_dimensions(latest)
        print()

        if len(self.snapshots) >= 2:
            self.visualize_z_trajectory(window=min(30, len(self.snapshots)))
            print()

        self.visualize_phase_diagram()


def main():
    """Demo cascade visualizer."""
    from unified_cascade_mathematics_core import UnifiedCascadeFramework
    from unified_sovereignty_system import create_demo_burden, evolve_cascade_state

    print("=" * 80)
    print("CASCADE VISUALIZER - Demo")
    print("=" * 80 + "\n")

    visualizer = CascadeVisualizer(width=80)
    framework = UnifiedCascadeFramework()

    # Simulate cascade evolution
    state = framework.compute_full_state(
        clarity=3.0, immunity=4.0, efficiency=3.5, autonomy=4.5
    )

    print("Simulating cascade evolution...\n")

    for step in range(12):
        burden = create_demo_burden(state.phase_regime)
        visualizer.add_snapshot(state, burden)

        # Evolve with amplification
        state = evolve_cascade_state(
            state,
            clarity_delta=0.4,
            immunity_delta=0.6,
            efficiency_delta=0.8,
            autonomy_delta=0.5
        )

    # Show complete dashboard
    visualizer.visualize_dashboard()

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
