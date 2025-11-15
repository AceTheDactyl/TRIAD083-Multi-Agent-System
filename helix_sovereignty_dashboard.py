#!/usr/bin/env python3
"""
HELIX SOVEREIGNTY DASHBOARD
Drift OS Integration - Week 1-2
Coordinate: Δ3.14159|1.000|1.000Ω

Purpose: Real-time visibility into Jason's sovereignty journey via Helix operations
Integration: Combines helix_burden_tracker + Garden Rail 3 components
Target: Visualize 20 hrs/week → 8 hrs/week burden reduction

Built by: TRIAD-0.83 Drift OS Integration
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

# Import Helix burden tracking
from helix_burden_tracker import HelixBurdenTracker, HelixLayer

# Import Garden Rail 3 components
from cascade_visualizer import CascadeVisualizer
from amplification_metrics import AmplificationMetrics
from emergence_health_monitor import EmergenceHealthMonitor
from z_level_monitor import ZLevelMonitor


@dataclass
class HelixMetrics:
    """Current metrics for Helix operations."""
    total_burden_hrs_per_week: float
    target_burden_hrs_per_week: float = 8.0
    baseline_burden_hrs_per_week: float = 20.0
    reduction_pct: float = 0.0
    z_coordinate: float = 0.0
    phase_regime: str = "unknown"
    alpha: float = 0.0
    beta: float = 0.0
    cascade_multiplier: float = 0.0


class HelixSovereigntyDashboard:
    """
    Unified dashboard for visualizing Helix sovereignty metrics.

    Combines:
    - Helix burden tracking (operational data)
    - Garden Rail 3 visualizations (cascade, health, z-monitoring)
    - Custom Helix-specific views (VaultNode health, tool autonomy)

    Usage:
        dashboard = HelixSovereigntyDashboard()
        dashboard.display_live_dashboard()
    """

    def __init__(self,
                 burden_tracker: Optional[HelixBurdenTracker] = None):
        """
        Initialize dashboard with burden tracker and Garden Rail 3 components.

        Args:
            burden_tracker: Existing burden tracker (or creates new one)
        """
        # Core tracking
        self.burden_tracker = burden_tracker or HelixBurdenTracker()

        # Garden Rail 3 components
        self.visualizer = CascadeVisualizer(width=80)
        self.amp_metrics = AmplificationMetrics()
        self.health_monitor = EmergenceHealthMonitor()
        self.z_monitor = ZLevelMonitor()

        # Session tracking
        self.session_start = datetime.utcnow()
        self.snapshot_count = 0

    def capture_current_state(self):
        """
        Capture current Helix state and update all monitors.

        This should be called after any Helix operation completes.
        """
        # Get weekly summary from burden tracker
        summary = self.burden_tracker.get_weekly_summary()

        # Extract sovereignty snapshot if available
        snapshots = self.burden_tracker.sovereignty_system.snapshots
        if snapshots:
            latest = snapshots[-1]

            # Update z-monitor
            self.z_monitor.capture_snapshot(latest.cascade_state)

            # Update amplification metrics
            self.amp_metrics.capture_snapshot(latest.cascade_state)

            # Calculate alpha and beta from R values
            alpha = latest.cascade_state.R2 / latest.cascade_state.R1 if latest.cascade_state.R1 > 0 else 0.0
            beta = latest.cascade_state.R3 / latest.cascade_state.R2 if latest.cascade_state.R2 > 0 else 0.0

            # Update health monitor
            self.health_monitor.check_component_health(
                'alpha_amplifier',
                alpha_current=alpha,
                alpha_baseline=1.0,
                alpha_target=2.3
            )
            self.health_monitor.check_component_health(
                'beta_amplifier',
                beta_current=beta,
                beta_baseline=1.0,
                beta_target=1.8
            )
            self.health_monitor.check_component_health(
                'cascade_multiplier',
                cascade_current=latest.cascade_state.cascade_multiplier,
                cascade_target=4.11
            )

            self.snapshot_count += 1

    def get_current_metrics(self) -> HelixMetrics:
        """Get current Helix metrics snapshot."""
        summary = self.burden_tracker.get_weekly_summary()

        # Calculate reduction percentage
        current_burden = summary.get('time_investment_hrs_per_week', 20.0)
        baseline = 20.0
        reduction_pct = ((baseline - current_burden) / baseline) * 100.0 if baseline > 0 else 0.0

        # Get sovereignty metrics
        snapshots = self.burden_tracker.sovereignty_system.snapshots
        z = summary.get('current_z', 0.0)
        phase = summary.get('phase_regime', 'unknown')
        alpha = 0.0
        beta = 0.0
        cascade = 0.0

        if snapshots:
            latest = snapshots[-1]
            alpha = latest.cascade_state.R2 / latest.cascade_state.R1 if latest.cascade_state.R1 > 0 else 0.0
            beta = latest.cascade_state.R3 / latest.cascade_state.R2 if latest.cascade_state.R2 > 0 else 0.0
            cascade = latest.cascade_state.cascade_multiplier

        return HelixMetrics(
            total_burden_hrs_per_week=current_burden,
            reduction_pct=reduction_pct,
            z_coordinate=z,
            phase_regime=phase,
            alpha=alpha,
            beta=beta,
            cascade_multiplier=cascade
        )

    def visualize_helix_cascade(self):
        """Show CORE→BRIDGES→META amplification waterfall."""
        print("="*80)
        print("HELIX CASCADE AMPLIFICATION (CORE → BRIDGES → META)")
        print("="*80)
        print()

        snapshots = self.burden_tracker.sovereignty_system.snapshots
        if not snapshots:
            print("⚠ No cascade data available yet")
            print("(Operations need to be tracked to generate cascade metrics)")
            print()
            return

        latest = snapshots[-1]

        # Create visualization snapshot from UnifiedSystemSnapshot
        from cascade_visualizer import VisualizationSnapshot
        from datetime import datetime

        viz_snapshot = VisualizationSnapshot(
            timestamp=datetime.now(),
            z_value=latest.cascade_state.z_coordinate,
            phase_regime=latest.cascade_state.phase_regime,
            R1=latest.cascade_state.R1,
            R2=latest.cascade_state.R2,
            R3=latest.cascade_state.R3,
            burden=latest.burden,
            alpha=latest.cascade_state.R2 / latest.cascade_state.R1 if latest.cascade_state.R1 > 0 else 0.0,
            beta=latest.cascade_state.R3 / latest.cascade_state.R2 if latest.cascade_state.R2 > 0 else 0.0
        )

        self.visualizer.visualize_cascade_waterfall(viz_snapshot)
        print()

    def visualize_jason_burden(self):
        """Show 20 hrs/week → 8 hrs/week burden reduction progress."""
        print("="*80)
        print("JASON'S BURDEN REDUCTION (20 hrs/week → 8 hrs/week target)")
        print("="*80)
        print()

        metrics = self.get_current_metrics()

        # Burden progress bar
        baseline = 20.0
        target = 8.0
        current = metrics.total_burden_hrs_per_week

        # Calculate bar widths (0-70 chars)
        max_bar = 70
        current_bar = int((current / baseline) * max_bar)
        target_bar = int((target / baseline) * max_bar)

        print(f"Current Burden:  {current:.2f} hrs/week")
        print(f"  [{'█' * current_bar}{'░' * (max_bar - current_bar)}]")
        print()
        print(f"Target Burden:   {target:.2f} hrs/week")
        print(f"  [{'█' * target_bar}{'░' * (max_bar - target_bar)}]")
        print()

        # Reduction metrics
        reduction_needed = baseline - target  # 12 hrs
        reduction_achieved = baseline - current
        progress_pct = (reduction_achieved / reduction_needed) * 100.0 if reduction_needed > 0 else 0.0

        print(f"Reduction Achieved: {reduction_achieved:.2f} hrs ({metrics.reduction_pct:.1f}% of baseline)")
        print(f"Reduction Target:   {reduction_needed:.2f} hrs (60% of baseline)")
        print(f"Progress to Target: {progress_pct:.1f}%")
        print()

        # Status indicator
        if progress_pct >= 100.0:
            status = "🟢 TARGET ACHIEVED"
        elif progress_pct >= 75.0:
            status = "🟡 NEAR TARGET"
        elif progress_pct >= 50.0:
            status = "🟠 MODERATE PROGRESS"
        elif progress_pct >= 25.0:
            status = "🔵 EARLY PROGRESS"
        else:
            status = "⚪ BASELINE"

        print(f"Status: {status}")
        print()

    def visualize_vaultnode_health(self):
        """Show VaultNode elevations (z-values) and phase regimes."""
        print("="*80)
        print("VAULTNODE SOVEREIGNTY HEALTH")
        print("="*80)
        print()

        metrics = self.get_current_metrics()

        # Display current z-coordinate and phase
        print(f"System Z-Coordinate: {metrics.z_coordinate:.3f}")
        print(f"Phase Regime:        {metrics.phase_regime}")
        print()

        # Show z-trajectory if available
        if self.z_monitor.snapshots:
            print("Recent Z-Trajectory:")
            recent = self.z_monitor.snapshots[-min(5, len(self.z_monitor.snapshots)):]
            for snapshot in recent:
                z = snapshot.z_value
                phase = snapshot.phase_regime
                timestamp = snapshot.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                print(f"  {timestamp}: z={z:.3f} ({phase})")
            print()

        # Z-coordinate interpretation
        if metrics.z_coordinate < 0.50:
            interpretation = "Subcritical - Low sovereignty, high manual burden"
        elif metrics.z_coordinate < 0.80:
            interpretation = "Approaching critical - Building momentum"
        elif 0.85 <= metrics.z_coordinate <= 0.89:
            interpretation = "⚠ CRITICAL POINT - Maximum emergence potential"
        elif metrics.z_coordinate < 1.0:
            interpretation = "Supercritical - High sovereignty, cascade active"
        else:
            interpretation = "Maximum sovereignty - Fully autonomous"

        print(f"Interpretation: {interpretation}")
        print()

    def visualize_tool_autonomy(self):
        """Show which tools are autonomous vs manual."""
        print("="*80)
        print("TOOL AUTONOMY LEVELS")
        print("="*80)
        print()

        summary = self.burden_tracker.get_weekly_summary()

        # Get operations by layer
        time_by_layer = summary.get('time_by_layer', {})
        total_time = summary.get('time_investment_hrs_per_week', 0.0)

        if total_time == 0:
            print("⚠ No tool usage data available yet")
            print()
            return

        print("Time Investment by Layer:")
        for layer_str, hours in time_by_layer.items():
            pct = (hours / total_time) * 100.0 if total_time > 0 else 0.0
            bar_width = int((pct / 100.0) * 50)
            bar = '█' * bar_width + '░' * (50 - bar_width)
            print(f"  {layer_str:10} {hours:6.3f} hrs ({pct:5.1f}%) [{bar}]")

        print()

        # Manual effort estimate
        avg_manual = summary.get('average_manual_effort_pct', 100.0)
        autonomy_pct = 100.0 - avg_manual

        print(f"Average Manual Effort: {avg_manual:.1f}%")
        print(f"Average Autonomy:      {autonomy_pct:.1f}%")
        print()

        if autonomy_pct < 20:
            status = "⚪ Mostly Manual - High burden"
        elif autonomy_pct < 40:
            status = "🔵 Some Automation - Moderate burden"
        elif autonomy_pct < 60:
            status = "🟡 Balanced - Autonomy emerging"
        elif autonomy_pct < 80:
            status = "🟠 Highly Autonomous - Low burden"
        else:
            status = "🟢 Fully Autonomous - Minimal burden"

        print(f"Status: {status}")
        print()

    def display_live_dashboard(self):
        """Display complete live dashboard with all visualizations."""
        print()
        print("="*80)
        print(" " * 20 + "HELIX SOVEREIGNTY DASHBOARD")
        print(" " * 18 + f"Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(" " * 26 + f"Snapshots: {self.snapshot_count}")
        print("="*80)
        print()

        # Section 1: Jason's Burden Reduction
        self.visualize_jason_burden()

        # Section 2: Helix Cascade Amplification
        self.visualize_helix_cascade()

        # Section 3: VaultNode Sovereignty Health
        self.visualize_vaultnode_health()

        # Section 4: Tool Autonomy
        self.visualize_tool_autonomy()

        # Section 5: System Health (from Garden Rail 3)
        print("="*80)
        print("OVERALL SYSTEM HEALTH")
        print("="*80)
        print()

        health_report = self.health_monitor.generate_system_report()
        status_emoji = {
            'optimal': '🟢',
            'nominal': '🟡',
            'degraded': '🟠',
            'critical': '🔴'
        }
        emoji = status_emoji.get(health_report.overall_status, '⚪')

        print(f"Status: {emoji} {health_report.overall_status.upper()}")
        print(f"Health Score: {health_report.overall_health_score*100:.0f}%")
        print()

        if health_report.interventions_suggested:
            print("Interventions Suggested:")
            for rec in health_report.interventions_suggested[:3]:
                print(f"  • {rec}")
            print()

        print("="*80)
        print()

    def export_dashboard_snapshot(self, filepath: str):
        """Export current dashboard state to JSON."""
        metrics = self.get_current_metrics()
        summary = self.burden_tracker.get_weekly_summary()

        snapshot = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'session_start': self.session_start.isoformat() + 'Z',
            'snapshot_count': self.snapshot_count,
            'helix_metrics': {
                'burden_hrs_per_week': metrics.total_burden_hrs_per_week,
                'target_hrs_per_week': metrics.target_burden_hrs_per_week,
                'baseline_hrs_per_week': metrics.baseline_burden_hrs_per_week,
                'reduction_pct': metrics.reduction_pct,
                'z_coordinate': metrics.z_coordinate,
                'phase_regime': metrics.phase_regime,
                'alpha': metrics.alpha,
                'beta': metrics.beta,
                'cascade_multiplier': metrics.cascade_multiplier
            },
            'weekly_summary': summary,
            'health': {
                'status': self.health_monitor.generate_system_report().overall_status,
                'health_score': self.health_monitor.generate_system_report().overall_health_score,
                'interventions': self.health_monitor.generate_system_report().interventions_suggested
            }
        }

        with open(filepath, 'w') as f:
            json.dump(snapshot, f, indent=2)

        print(f"✓ Dashboard snapshot exported to {filepath}")


def test_helix_dashboard():
    """Test the Helix sovereignty dashboard."""
    print("="*80)
    print("HELIX SOVEREIGNTY DASHBOARD - TEST")
    print("="*80)
    print()

    # Create dashboard
    dashboard = HelixSovereigntyDashboard()

    # Simulate some operations using the tool wrapper
    from helix_tool_wrapper import HelixToolWrapper

    wrapper = HelixToolWrapper(burden_tracker=dashboard.burden_tracker)

    print("Simulating Helix operations...")
    print()

    # Simulate a day of Jason's work
    operations = [
        ("TOOLS/CORE/helix_loader.yaml", "load_pattern", {"pattern": "emergence"}),
        ("TOOLS/CORE/coordinate_detector.yaml", "detect_coordinate", {"vaultnode": "z0p85"}),
        ("TOOLS/BRIDGES/consent_protocol.yaml", "request_consent", {"action": "state_transfer"}),
        ("TOOLS/BRIDGES/cross_instance_messenger.yaml", "send_message", {"target": "instance_2"}),
        ("TOOLS/META/shed_builder.yaml", "build_framework", {"framework": "autonomous_consolidation"}),
    ]

    for tool_path, operation, context in operations:
        wrapper.execute_tool(tool_path, operation, context, simulate=True)

    # Capture state after operations
    dashboard.capture_current_state()

    print()
    # Display dashboard
    dashboard.display_live_dashboard()

    # Export snapshot
    dashboard.export_dashboard_snapshot('helix_dashboard_snapshot.json')


if __name__ == "__main__":
    test_helix_dashboard()
