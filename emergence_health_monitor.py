#!/usr/bin/env python3
"""
Emergence Health Monitor
========================

Garden Rail 3 - Layer 5: EMERGENCE DASHBOARD
Component 5.3: Overall health dashboard for Garden Rail 3 system

Purpose:
- Aggregate health from all Garden Rail 3 components
- Monitor system operational status
- Detect degradation and suggest interventions
- Generate health reports

Health Indicators:
1. System Health: % of components operational
2. Cascade Health: Amplifications happening? (α, β targets)
3. Burden Health: Reduction on track? (≥40%)
4. Emergence Health: Patterns appearing? (Φ, symmetry)
5. Self-Catalysis Health: Recursion working? (autonomous %)

Status Levels:
- 🟢 OPTIMAL: All targets met, emergence detected
- 🟡 NOMINAL: Core functions working, some targets missed
- 🟠 DEGRADED: Amplification below target, intervention needed
- 🔴 CRITICAL: System instability, cascade failure
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class ComponentHealth:
    """Health status of a single component."""
    component_name: str
    status: str  # 'optimal', 'nominal', 'degraded', 'critical', 'offline'
    health_score: float  # 0.0-1.0
    issues: List[str] = field(default_factory=list)
    last_check: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SystemHealthReport:
    """Complete system health report."""
    timestamp: str
    overall_status: str  # 'OPTIMAL', 'NOMINAL', 'DEGRADED', 'CRITICAL'
    overall_health_score: float  # 0.0-1.0
    component_health: Dict[str, ComponentHealth]
    key_findings: List[str]
    interventions_suggested: List[str]
    metrics: Dict[str, float]


class EmergenceHealthMonitor:
    """
    Monitor overall health of Garden Rail 3 system.

    Aggregates health from:
    - Layer 1: Cascade initiators
    - Layer 2: Amplification enhancers
    - Layer 3: Self-catalyzing frameworks
    - Layer 4: Phase-aware adaptation
    - Layer 5: Emergence dashboard
    """

    # Health thresholds
    OPTIMAL_THRESHOLD = 0.85  # 85%+ health
    NOMINAL_THRESHOLD = 0.70  # 70-85% health
    DEGRADED_THRESHOLD = 0.50  # 50-70% health
    # Below 50% = CRITICAL

    def __init__(self):
        self.component_health: Dict[str, ComponentHealth] = {}
        self.health_history: List[SystemHealthReport] = []

    def check_component_health(self, component_name: str, **metrics) -> ComponentHealth:
        """
        Check health of a specific component.

        Args:
            component_name: Name of component to check
            **metrics: Component-specific metrics for health assessment

        Returns:
            ComponentHealth object
        """
        issues = []
        health_score = 1.0  # Start perfect, deduct for issues

        # Component-specific health checks
        if component_name == 'alpha_amplifier':
            # Check if α is meeting target
            alpha_current = metrics.get('alpha_current', 0)
            alpha_target = metrics.get('alpha_target', 2.3)

            if alpha_current >= alpha_target:
                status = 'optimal'
            elif alpha_current >= alpha_target * 0.8:
                status = 'nominal'
                health_score = 0.75
                issues.append(f"α below target ({alpha_current:.2f} < {alpha_target:.2f})")
            elif alpha_current >= alpha_target * 0.5:
                status = 'degraded'
                health_score = 0.55
                issues.append(f"α significantly below target ({alpha_current:.2f})")
            else:
                status = 'critical'
                health_score = 0.30
                issues.append(f"α critically low ({alpha_current:.2f})")

        elif component_name == 'beta_amplifier':
            # Check if β is meeting target
            beta_current = metrics.get('beta_current', 0)
            beta_target = metrics.get('beta_target', 1.8)

            if beta_current >= beta_target:
                status = 'optimal'
            elif beta_current >= beta_target * 0.8:
                status = 'nominal'
                health_score = 0.75
                issues.append(f"β below target ({beta_current:.2f} < {beta_target:.2f})")
            elif beta_current >= beta_target * 0.5:
                status = 'degraded'
                health_score = 0.55
                issues.append(f"β significantly below target ({beta_current:.2f})")
            else:
                status = 'critical'
                health_score = 0.30
                issues.append(f"β critically low ({beta_current:.2f})")

        elif component_name == 'cascade_multiplier':
            # Check total cascade amplification
            cascade_current = metrics.get('cascade_current', 0)
            cascade_target = metrics.get('cascade_target', 4.11)

            if cascade_current >= cascade_target:
                status = 'optimal'
            elif cascade_current >= cascade_target * 0.7:
                status = 'nominal'
                health_score = 0.75
                issues.append(f"Cascade below target ({cascade_current:.2f}× < {cascade_target:.2f}×)")
            elif cascade_current >= 2.0:
                status = 'degraded'
                health_score = 0.55
                issues.append(f"Cascade significantly below target ({cascade_current:.2f}×)")
            else:
                status = 'critical'
                health_score = 0.30
                issues.append(f"Cascade critically low ({cascade_current:.2f}×)")

        elif component_name == 'burden_reduction':
            # Check if burden reduction is on track
            reduction_current = metrics.get('reduction_current', 0)
            reduction_target = metrics.get('reduction_target', 60)

            if reduction_current >= reduction_target:
                status = 'optimal'
            elif reduction_current >= 40:  # Minimum acceptable
                status = 'nominal'
                health_score = 0.75
                issues.append(f"Burden reduction below target ({reduction_current:.1f}% < {reduction_target:.1f}%)")
            elif reduction_current >= 20:
                status = 'degraded'
                health_score = 0.55
                issues.append(f"Burden reduction significantly below target ({reduction_current:.1f}%)")
            else:
                status = 'critical'
                health_score = 0.30
                issues.append(f"Burden reduction critically low ({reduction_current:.1f}%)")

        elif component_name == 'emergence_patterns':
            # Check emergence indicators (Φ, symmetry, packing)
            phi = metrics.get('phi', 0)
            symmetry = metrics.get('symmetry', 0)
            packing = metrics.get('packing', 0)

            emergence_score = (phi / 100.0) * symmetry * (packing / 100.0)  # Composite score

            if emergence_score >= 0.85:
                status = 'optimal'
            elif emergence_score >= 0.65:
                status = 'nominal'
                health_score = 0.75
                issues.append(f"Emergence score below optimal ({emergence_score:.2f})")
            elif emergence_score >= 0.40:
                status = 'degraded'
                health_score = 0.55
                issues.append(f"Emergence score low ({emergence_score:.2f})")
            else:
                status = 'critical'
                health_score = 0.30
                issues.append(f"Emergence score critically low ({emergence_score:.2f})")

        elif component_name == 'self_catalysis':
            # Check autonomous framework generation rate
            autonomy_rate = metrics.get('autonomy_rate', 0)  # % of improvements self-generated

            if autonomy_rate >= 70:
                status = 'optimal'
            elif autonomy_rate >= 50:
                status = 'nominal'
                health_score = 0.75
                issues.append(f"Self-catalysis below target ({autonomy_rate:.0f}% < 70%)")
            elif autonomy_rate >= 30:
                status = 'degraded'
                health_score = 0.55
                issues.append(f"Self-catalysis significantly below target ({autonomy_rate:.0f}%)")
            else:
                status = 'critical'
                health_score = 0.30
                issues.append(f"Self-catalysis critically low ({autonomy_rate:.0f}%)")

        elif component_name == 'z_level_monitor':
            # Check if z-monitoring is working
            snapshots_count = metrics.get('snapshots_count', 0)
            is_stalling = metrics.get('is_stalling', False)

            if snapshots_count >= 5 and not is_stalling:
                status = 'optimal'
            elif snapshots_count >= 3:
                status = 'nominal'
                health_score = 0.75
                if is_stalling:
                    issues.append("Z-coordinate stalling detected")
            elif snapshots_count >= 1:
                status = 'degraded'
                health_score = 0.55
                issues.append(f"Insufficient z-tracking data ({snapshots_count} snapshots)")
            else:
                status = 'critical'
                health_score = 0.30
                issues.append("Z-level monitor offline")

        else:
            # Generic component (assume operational)
            status = 'nominal'
            health_score = 0.75
            issues.append("Generic health check (no specific metrics)")

        component = ComponentHealth(
            component_name=component_name,
            status=status,
            health_score=health_score,
            issues=issues
        )

        # Store in component health map
        self.component_health[component_name] = component

        return component

    def generate_system_report(self) -> SystemHealthReport:
        """Generate comprehensive system health report."""
        timestamp = datetime.now().isoformat()

        # Compute overall health score (average of all components)
        if self.component_health:
            overall_score = sum(c.health_score for c in self.component_health.values()) / len(self.component_health)
        else:
            overall_score = 0.0

        # Determine overall status
        if overall_score >= self.OPTIMAL_THRESHOLD:
            overall_status = 'OPTIMAL'
        elif overall_score >= self.NOMINAL_THRESHOLD:
            overall_status = 'NOMINAL'
        elif overall_score >= self.DEGRADED_THRESHOLD:
            overall_status = 'DEGRADED'
        else:
            overall_status = 'CRITICAL'

        # Aggregate key findings
        key_findings = []
        interventions = []

        for comp in self.component_health.values():
            if comp.status == 'optimal':
                key_findings.append(f"✓ {comp.component_name}: OPTIMAL")
            elif comp.status in ['degraded', 'critical']:
                for issue in comp.issues:
                    key_findings.append(f"⚠ {comp.component_name}: {issue}")

                # Suggest interventions
                if comp.component_name == 'alpha_amplifier':
                    interventions.append("Increase R2 tool generation to boost α")
                elif comp.component_name == 'beta_amplifier':
                    interventions.append("Generate R3 frameworks to boost β")
                elif comp.component_name == 'cascade_multiplier':
                    interventions.append("Strengthen coupling between cascade layers")
                elif comp.component_name == 'burden_reduction':
                    interventions.append("Review burden calculation - may need phase-specific adjustment")
                elif comp.component_name == 'emergence_patterns':
                    interventions.append("Check Φ calculation and symmetry metrics")
                elif comp.component_name == 'self_catalysis':
                    interventions.append("Enable autonomous framework builder")
                elif comp.component_name == 'z_level_monitor':
                    interventions.append("Increase z-coordinate snapshot frequency")

        # Collect key metrics
        metrics = {
            'overall_health_score': overall_score,
            'components_optimal': sum(1 for c in self.component_health.values() if c.status == 'optimal'),
            'components_nominal': sum(1 for c in self.component_health.values() if c.status == 'nominal'),
            'components_degraded': sum(1 for c in self.component_health.values() if c.status == 'degraded'),
            'components_critical': sum(1 for c in self.component_health.values() if c.status == 'critical'),
            'total_components': len(self.component_health)
        }

        report = SystemHealthReport(
            timestamp=timestamp,
            overall_status=overall_status,
            overall_health_score=overall_score,
            component_health=self.component_health.copy(),
            key_findings=key_findings,
            interventions_suggested=interventions,
            metrics=metrics
        )

        # Store in history
        self.health_history.append(report)

        return report

    def print_health_report(self, report: Optional[SystemHealthReport] = None):
        """Print human-readable health report."""
        if report is None:
            report = self.generate_system_report()

        # Status emoji
        status_emoji = {
            'OPTIMAL': '🟢',
            'NOMINAL': '🟡',
            'DEGRADED': '🟠',
            'CRITICAL': '🔴'
        }

        print("=" * 80)
        print("GARDEN RAIL 3 - EMERGENCE HEALTH MONITOR")
        print("=" * 80)
        print(f"\nOverall Status: {status_emoji.get(report.overall_status, '⚪')} {report.overall_status}")
        print(f"Health Score: {report.overall_health_score:.0%}\n")

        print("COMPONENT HEALTH")
        print("-" * 80)

        for comp_name, comp in report.component_health.items():
            status_icon = {
                'optimal': '✓',
                'nominal': '○',
                'degraded': '⚠',
                'critical': '✗',
                'offline': '•'
            }.get(comp.status, '?')

            print(f"{status_icon} {comp_name}: {comp.status.upper()} ({comp.health_score:.0%})")

            if comp.issues:
                for issue in comp.issues:
                    print(f"    - {issue}")

        print()

        print("KEY FINDINGS")
        print("-" * 80)
        for finding in report.key_findings:
            print(f"  {finding}")

        if report.interventions_suggested:
            print()
            print("RECOMMENDED INTERVENTIONS")
            print("-" * 80)
            for i, intervention in enumerate(report.interventions_suggested, 1):
                print(f"  {i}. {intervention}")

        print()
        print("METRICS")
        print("-" * 80)
        print(f"  Optimal: {report.metrics['components_optimal']}")
        print(f"  Nominal: {report.metrics['components_nominal']}")
        print(f"  Degraded: {report.metrics['components_degraded']}")
        print(f"  Critical: {report.metrics['components_critical']}")
        print(f"  Total: {report.metrics['total_components']}")

        print("=" * 80)

    def export_health_report(self, report: SystemHealthReport, filepath: str):
        """Export health report to JSON."""
        data = {
            'timestamp': report.timestamp,
            'overall_status': report.overall_status,
            'overall_health_score': report.overall_health_score,
            'component_health': {
                name: {
                    'status': comp.status,
                    'health_score': comp.health_score,
                    'issues': comp.issues,
                    'last_check': comp.last_check
                }
                for name, comp in report.component_health.items()
            },
            'key_findings': report.key_findings,
            'interventions_suggested': report.interventions_suggested,
            'metrics': report.metrics
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    """Demo emergence health monitor."""
    print("=" * 80)
    print("EMERGENCE HEALTH MONITOR - Demo")
    print("=" * 80 + "\n")

    monitor = EmergenceHealthMonitor()

    # Check various components with simulated metrics
    print("Checking component health...\n")

    # Good components
    monitor.check_component_health('alpha_amplifier',
                                   alpha_current=2.5, alpha_target=2.3)

    monitor.check_component_health('cascade_multiplier',
                                   cascade_current=5.2, cascade_target=4.11)

    monitor.check_component_health('z_level_monitor',
                                   snapshots_count=15, is_stalling=False)

    # Degraded components
    monitor.check_component_health('beta_amplifier',
                                   beta_current=1.3, beta_target=1.8)

    monitor.check_component_health('burden_reduction',
                                   reduction_current=35, reduction_target=60)

    # Critical component
    monitor.check_component_health('self_catalysis',
                                   autonomy_rate=15)

    # Generate and print report
    report = monitor.generate_system_report()
    monitor.print_health_report(report)

    # Export
    monitor.export_health_report(report, 'health_report_demo.json')
    print("\nHealth report exported to health_report_demo.json")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
