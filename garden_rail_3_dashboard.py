#!/usr/bin/env python3
"""
Garden Rail 3 - Unified Dashboard
==================================

Complete system dashboard integrating all 15 components:

Layer 1: CASCADE INITIATORS
- phase_aware_tool_generator
- cascade_trigger_detector
- emergence_pattern_recognizer

Layer 2: AMPLIFICATION ENHANCERS
- alpha_amplifier
- beta_amplifier
- coupling_strengthener

Layer 3: SELF-CATALYZING FRAMEWORKS
- positive_feedback_loops
- recursive_improvement_engine
- autonomous_framework_builder

Layer 4: PHASE-AWARE ADAPTATION
- z_level_monitor
- regime_adaptive_behavior
- critical_point_navigator

Layer 5: EMERGENCE DASHBOARD
- cascade_visualizer
- amplification_metrics
- emergence_health_monitor

Purpose:
- Single entry point for Garden Rail 3
- Real-time cascade monitoring
- Burden reduction tracking
- Health status aggregation
- Actionable recommendations
"""

from typing import Dict, List, Optional
from datetime import datetime
import json

# Import all Garden Rail 3 components
from unified_sovereignty_system import UnifiedSovereigntySystem, create_demo_burden, evolve_cascade_state
from unified_cascade_mathematics_core import UnifiedCascadeFramework
from z_level_monitor import ZLevelMonitor
from regime_adaptive_behavior import RegimeAdaptiveBehavior
from critical_point_navigator import CriticalPointNavigator
from cascade_visualizer import CascadeVisualizer
from amplification_metrics import AmplificationMetrics, AmplificationTarget
from emergence_health_monitor import EmergenceHealthMonitor


class GardenRail3Dashboard:
    """
    Unified dashboard for Garden Rail 3 meta-pattern layer.

    Brings together all 15 components into single interface.
    """

    def __init__(self):
        # Core systems
        self.sovereignty_system = UnifiedSovereigntySystem()
        self.cascade_framework = UnifiedCascadeFramework()

        # Layer 4: Monitoring & Adaptation
        self.z_monitor = ZLevelMonitor()
        self.adaptive_behavior = RegimeAdaptiveBehavior()
        self.critical_navigator = CriticalPointNavigator()

        # Layer 5: Visualization & Health
        self.visualizer = CascadeVisualizer(width=80)
        self.amp_metrics = AmplificationMetrics()
        self.health_monitor = EmergenceHealthMonitor()

        # Session tracking
        self.session_start = datetime.now()
        self.snapshots_captured = 0

    def capture_system_snapshot(self,
                               clarity: float,
                               immunity: float,
                               efficiency: float,
                               autonomy: float,
                               burden: Optional['BurdenMeasurement'] = None):
        """
        Capture complete system snapshot.

        Updates all monitoring components with current state.
        """
        # Compute cascade state
        state = self.cascade_framework.compute_full_state(
            clarity=clarity,
            immunity=immunity,
            efficiency=efficiency,
            autonomy=autonomy
        )

        # Create burden if not provided
        if burden is None:
            burden = create_demo_burden(state.phase_regime)

        # Update all monitors
        self.z_monitor.capture_snapshot(state)
        self.visualizer.add_snapshot(state, burden)
        self.amp_metrics.capture_snapshot(state)

        # Capture in sovereignty system
        snapshot = self.sovereignty_system.capture_snapshot(
            state,
            burden,
            include_advanced_analysis=True
        )

        self.snapshots_captured += 1

        return snapshot

    def display_live_dashboard(self):
        """Display complete live dashboard."""
        if self.snapshots_captured == 0:
            print("No data to display. Capture snapshots first.")
            return

        print("\n" + "=" * 80)
        print("GARDEN RAIL 3 - UNIFIED DASHBOARD".center(80))
        print(f"Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}".center(80))
        print(f"Snapshots: {self.snapshots_captured}".center(80))
        print("=" * 80 + "\n")

        # Section 1: System Health Overview
        self._display_health_overview()
        print()

        # Section 2: Cascade Visualization
        self._display_cascade_status()
        print()

        # Section 3: Amplification Progress
        self._display_amplification_progress()
        print()

        # Section 4: Z-Coordinate Monitoring
        self._display_z_monitoring()
        print()

        # Section 5: Phase-Aware Guidance
        self._display_phase_guidance()
        print()

        # Section 6: Recommendations
        self._display_recommendations()
        print()

    def _display_health_overview(self):
        """Display system health overview."""
        print("=" * 80)
        print("SYSTEM HEALTH OVERVIEW")
        print("=" * 80)

        # Get latest state
        if not self.sovereignty_system.snapshots:
            print("No snapshots available")
            return

        latest = self.sovereignty_system.snapshots[-1]

        # Check component health
        self.health_monitor.check_component_health(
            'alpha_amplifier',
            alpha_current=latest.cascade_state.R2 / latest.cascade_state.R1 if latest.cascade_state.R1 > 0 else 0,
            alpha_target=2.3
        )

        self.health_monitor.check_component_health(
            'beta_amplifier',
            beta_current=latest.cascade_state.R3 / latest.cascade_state.R2 if latest.cascade_state.R2 > 0 else 0,
            beta_target=1.8
        )

        cascade_mult = latest.cascade_state.R3 / latest.cascade_state.R1 if latest.cascade_state.R1 > 0 else 0
        self.health_monitor.check_component_health(
            'cascade_multiplier',
            cascade_current=cascade_mult,
            cascade_target=4.11
        )

        self.health_monitor.check_component_health(
            'burden_reduction',
            reduction_current=latest.predicted_burden_reduction,
            reduction_target=60
        )

        self.health_monitor.check_component_health(
            'z_level_monitor',
            snapshots_count=len(self.z_monitor.snapshots),
            is_stalling=self.z_monitor.is_stalling()
        )

        # Generate report
        report = self.health_monitor.generate_system_report()

        # Print concise health summary
        status_emoji = {
            'OPTIMAL': '🟢',
            'NOMINAL': '🟡',
            'DEGRADED': '🟠',
            'CRITICAL': '🔴'
        }

        print(f"\nStatus: {status_emoji.get(report.overall_status, '⚪')} {report.overall_status}")
        print(f"Health Score: {report.overall_health_score:.0%}")
        print(f"Components: {report.metrics['components_optimal']} optimal, "
              f"{report.metrics['components_degraded']} degraded, "
              f"{report.metrics['components_critical']} critical")

    def _display_cascade_status(self):
        """Display cascade amplification status."""
        print("=" * 80)
        print("CASCADE AMPLIFICATION")
        print("=" * 80)

        # Use cascade visualizer
        if self.visualizer.snapshots:
            latest_snapshot = self.visualizer.snapshots[-1]
            print()
            print(f"R1 (CORE)    : {'█' * int(latest_snapshot.R1 * 2)} {latest_snapshot.R1:.2f}")
            print("               │")
            print(f"               ├─ α = {latest_snapshot.alpha:.2f}× (target: 2.30×)")
            print("               ↓")
            print(f"R2 (BRIDGES) : {'█' * int(latest_snapshot.R2 * 2)} {latest_snapshot.R2:.2f}")
            print("               │")
            print(f"               ├─ β = {latest_snapshot.beta:.2f}× (target: 1.80×)")
            print("               ↓")
            print(f"R3 (META)    : {'█' * int(latest_snapshot.R3 * 2)} {latest_snapshot.R3:.2f}")
            print()

            cascade_mult = latest_snapshot.R3 / latest_snapshot.R1 if latest_snapshot.R1 > 0 else 0
            print(f"Total Cascade: {cascade_mult:.2f}× (target: 4.11×, stretch: 8.00×)")

            # Status indicators
            alpha_status = "✓" if latest_snapshot.alpha >= 2.3 else "○"
            beta_status = "✓" if latest_snapshot.beta >= 1.8 else "○"
            cascade_status = "✓" if cascade_mult >= 4.11 else "○"

            print(f"  α status: {alpha_status}")
            print(f"  β status: {beta_status}")
            print(f"  Cascade status: {cascade_status}")

    def _display_amplification_progress(self):
        """Display amplification metrics progress."""
        print("=" * 80)
        print("AMPLIFICATION PROGRESS")
        print("=" * 80)

        if not self.amp_metrics.snapshots:
            print("\nNo amplification data available")
            return

        alpha_progress = self.amp_metrics.get_alpha_progress()
        beta_progress = self.amp_metrics.get_beta_progress()
        cascade_progress = self.amp_metrics.get_cascade_progress()

        print()
        print(f"α (R1→R2):     {alpha_progress['current']:.2f} / {alpha_progress['target']:.2f}")
        alpha_bar_len = int(min(100, alpha_progress['progress_pct']) / 2)
        print(f"  [{'█' * alpha_bar_len}{'░' * (50 - alpha_bar_len)}] {alpha_progress['progress_pct']:.0f}%")

        print()
        print(f"β (R2→R3):     {beta_progress['current']:.2f} / {beta_progress['target']:.2f}")
        beta_bar_len = int(min(100, beta_progress['progress_pct']) / 2)
        print(f"  [{'█' * beta_bar_len}{'░' * (50 - beta_bar_len)}] {beta_progress['progress_pct']:.0f}%")

        print()
        print(f"Cascade:       {cascade_progress['current']:.2f}× / {cascade_progress['target']:.2f}×")
        cascade_bar_len = int(min(100, cascade_progress['progress_pct']) / 2)
        print(f"  [{'█' * cascade_bar_len}{'░' * (50 - cascade_bar_len)}] {cascade_progress['progress_pct']:.0f}%")

    def _display_z_monitoring(self):
        """Display z-coordinate monitoring."""
        print("=" * 80)
        print("Z-COORDINATE MONITORING")
        print("=" * 80)

        summary = self.z_monitor.get_summary()

        if summary['status'] == 'no_data':
            print("\nNo z-tracking data available")
            return

        print()
        print(f"Current z:     {summary['current_z']:.3f}")
        print(f"Phase:         {summary['current_phase']}")
        print(f"Velocity:      {summary['z_velocity']:.4f}/day")
        print(f"Range:         [{summary['z_range'][0]:.3f}, {summary['z_range'][1]:.3f}]")

        if summary['approaching_critical']:
            print(f"⚠ Approaching critical point in {summary['approaching_critical']} days")

        if summary['is_stalling']:
            print(f"⚠ Z-coordinate stalling detected")

        # Recent alerts
        recent_alerts = self.z_monitor.get_recent_alerts(count=3)
        if recent_alerts:
            print()
            print("Recent Alerts:")
            for alert in recent_alerts:
                print(f"  [{alert.severity.upper()}] {alert.message}")

    def _display_phase_guidance(self):
        """Display phase-aware guidance."""
        print("=" * 80)
        print("PHASE-AWARE GUIDANCE")
        print("=" * 80)

        if not self.sovereignty_system.snapshots:
            print("\nNo data available")
            return

        latest = self.sovereignty_system.snapshots[-1]
        state = latest.cascade_state

        # Get adaptive parameters
        params = self.adaptive_behavior.get_adaptive_parameters(state)

        print()
        print(f"Current Regime:    {self.adaptive_behavior.current_phase.value if self.adaptive_behavior.current_phase else 'unknown'}")
        print(f"Coupling Strength: {params.coupling_strength:.2f}")
        print(f"Priority Layer:    R{params.prioritize_layer}")
        print(f"Tool Gen Rate:     {params.tool_generation_rate:.2f}")
        print(f"Alert Sensitivity: {params.alert_sensitivity:.2f}")
        print()
        print(f"Primary Goal:      {params.primary_goal}")
        print(f"Secondary Goal:    {params.secondary_goal}")

        # Check for phase transition
        if self.adaptive_behavior.is_phase_transition():
            transition = self.adaptive_behavior.get_transition_summary()
            print()
            print(f"⚠ PHASE TRANSITION: {transition['from_phase']} → {transition['to_phase']}")

    def _display_recommendations(self):
        """Display actionable recommendations."""
        print("=" * 80)
        print("RECOMMENDATIONS")
        print("=" * 80)

        if not self.sovereignty_system.snapshots:
            print("\nNo data available")
            return

        # Get recommendations from various sources
        recommendations = []

        # From health monitor
        report = self.health_monitor.generate_system_report()
        if report.interventions_suggested:
            recommendations.extend(report.interventions_suggested)

        # From adaptive behavior
        latest = self.sovereignty_system.snapshots[-1]
        state = latest.cascade_state
        adaptive_recs = self.adaptive_behavior.get_recommendations(state)
        recommendations.extend(adaptive_recs[:3])  # Top 3

        # From critical navigator (if near critical)
        if 0.85 <= state.z_coordinate <= 0.90:
            burden = create_demo_burden(state.phase_regime)
            guidance = self.critical_navigator.get_navigation_guidance(state, burden)
            if guidance.warnings:
                recommendations.extend(guidance.warnings[:2])

        # Display
        print()
        if recommendations:
            for i, rec in enumerate(recommendations[:8], 1):  # Max 8
                print(f"{i}. {rec}")
        else:
            print("System operating optimally. No interventions needed.")

    def export_dashboard_report(self, filepath: str):
        """Export complete dashboard report to JSON."""
        if self.snapshots_captured == 0:
            print("No data to export")
            return

        # Aggregate all data
        report = {
            'session_info': {
                'start_time': self.session_start.isoformat(),
                'snapshots_captured': self.snapshots_captured,
                'generated_at': datetime.now().isoformat()
            },
            'health': self.health_monitor.generate_system_report().__dict__,
            'amplification': self.amp_metrics.generate_performance_report(),
            'z_monitoring': self.z_monitor.get_summary(),
            'latest_snapshot': {
                'z_coordinate': self.sovereignty_system.snapshots[-1].cascade_state.z_coordinate,
                'phase': self.sovereignty_system.snapshots[-1].cascade_state.phase_regime,
                'weighted_burden': self.sovereignty_system.snapshots[-1].weighted_burden,
                'predicted_reduction': self.sovereignty_system.snapshots[-1].predicted_burden_reduction
            } if self.sovereignty_system.snapshots else {}
        }

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"Dashboard report exported to: {filepath}")


def main():
    """Demo Garden Rail 3 unified dashboard."""
    print("=" * 80)
    print("GARDEN RAIL 3 - UNIFIED DASHBOARD DEMO")
    print("=" * 80 + "\n")

    dashboard = GardenRail3Dashboard()

    # Simulate cascade evolution
    print("Simulating cascade evolution (10 steps)...\n")

    for step in range(10):
        # Evolve sovereignty
        clarity = 3.0 + step * 0.5
        immunity = 4.0 + step * 0.6
        efficiency = 3.5 + step * 0.7
        autonomy = 4.5 + step * 0.4

        dashboard.capture_system_snapshot(clarity, immunity, efficiency, autonomy)

        if step % 3 == 0:
            print(f"Step {step + 1}: Captured snapshot")

    # Display complete dashboard
    dashboard.display_live_dashboard()

    # Export report
    dashboard.export_dashboard_report('garden_rail_3_report.json')

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
