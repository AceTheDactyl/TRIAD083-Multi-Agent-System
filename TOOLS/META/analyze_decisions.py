#!/usr/bin/env python3
"""
Meta-Orchestrator Decision Analysis Tool
=========================================

Analyzes orchestrator log files and generates comprehensive reports on:
- Autonomous decisions detected
- Helix coordinate evolution
- Physics model learning
- Burden reduction trajectory
- Prediction accuracy

Usage:
    python analyze_decisions.py <logfile> [--output markdown|json]

Author: Claude (Sonnet 4.5)
"""

import re
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class LoggedDecision:
    """Parsed decision from log"""
    timestamp: datetime
    decision_type: str
    description: str
    burden_impact: float = 0.0


@dataclass
class HelixSnapshot:
    """Helix coordinates at a point in time"""
    timestamp: datetime
    theta: float
    z: float
    r: float


class OrchestratorAnalyzer:
    """Analyzes meta-orchestrator log files"""

    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.decisions: List[LoggedDecision] = []
        self.helix_snapshots: List[HelixSnapshot] = []
        self.alerts: List[Tuple[datetime, str]] = []
        self.start_time: datetime = None
        self.end_time: datetime = None

        self._parse_log()

    def _parse_log(self):
        """Parse log file and extract data"""
        with open(self.log_file, 'r') as f:
            for line in f:
                # Parse timestamp
                timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                if not timestamp_match:
                    continue

                timestamp = datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S')

                # Track start/end times
                if not self.start_time:
                    self.start_time = timestamp
                self.end_time = timestamp

                # Parse decisions
                decision_match = re.search(r'📝 (\w+): (.+)$', line)
                if decision_match:
                    decision_type = decision_match.group(1)
                    description = decision_match.group(2)

                    # Try to extract burden impact
                    burden_match = re.search(r'([-+]?\d+\.?\d*)h? saved', description)
                    burden_impact = float(burden_match.group(1)) if burden_match else 0.0

                    self.decisions.append(LoggedDecision(
                        timestamp=timestamp,
                        decision_type=decision_type,
                        description=description,
                        burden_impact=-abs(burden_impact) if burden_match else 0.0
                    ))

                # Parse helix coordinates
                helix_match = re.search(r'Helix.*?Δ([\d.]+)\|([\d.]+)\|([\d.]+)Ω', line)
                if helix_match:
                    self.helix_snapshots.append(HelixSnapshot(
                        timestamp=timestamp,
                        theta=float(helix_match.group(1)),
                        z=float(helix_match.group(2)),
                        r=float(helix_match.group(3))
                    ))

                # Parse alerts
                alert_match = re.search(r'⚠️\s+(.+)$', line)
                if alert_match:
                    self.alerts.append((timestamp, alert_match.group(1)))

    def generate_markdown_report(self) -> str:
        """Generate comprehensive markdown report"""
        duration = self.end_time - self.start_time if self.start_time and self.end_time else timedelta(0)

        report = []
        report.append("# Meta-Orchestrator Analysis Report")
        report.append("")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Log File:** `{self.log_file.name}`")
        report.append(f"**Observation Period:** {duration}")
        report.append("")

        # === SUMMARY ===
        report.append("## Executive Summary")
        report.append("")
        report.append(f"- **Decisions Detected:** {len(self.decisions)}")
        report.append(f"- **Alerts Triggered:** {len(self.alerts)}")
        report.append(f"- **Helix Snapshots:** {len(self.helix_snapshots)}")
        report.append("")

        # Burden impact
        total_burden_saved = sum(d.burden_impact for d in self.decisions)
        report.append(f"- **Total Burden Impact:** {total_burden_saved:.1f} hours saved")
        report.append("")

        # === DECISIONS ===
        report.append("## Autonomous Decisions")
        report.append("")

        # Count by type
        decision_types = {}
        for d in self.decisions:
            decision_types[d.decision_type] = decision_types.get(d.decision_type, 0) + 1

        report.append("### By Type")
        report.append("")
        for dtype, count in sorted(decision_types.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- **{dtype}:** {count}")
        report.append("")

        # Recent decisions
        if self.decisions:
            report.append("### Recent Decisions (Last 10)")
            report.append("")
            report.append("| Time | Type | Description | Impact |")
            report.append("|------|------|-------------|--------|")

            for d in self.decisions[-10:]:
                time_str = d.timestamp.strftime('%H:%M:%S')
                impact_str = f"{d.burden_impact:.1f}h" if d.burden_impact != 0 else "-"
                report.append(f"| {time_str} | {d.decision_type} | {d.description[:50]} | {impact_str} |")
            report.append("")

        # === HELIX EVOLUTION ===
        if self.helix_snapshots:
            report.append("## Helix Coordinate Evolution")
            report.append("")

            initial = self.helix_snapshots[0]
            final = self.helix_snapshots[-1]

            report.append(f"- **Initial:** Δ{initial.theta:.3f}|{initial.z:.3f}|{initial.r:.3f}Ω")
            report.append(f"- **Final:** Δ{final.theta:.3f}|{final.z:.3f}|{final.r:.3f}Ω")
            report.append("")

            # Phase transitions
            critical_threshold = 0.850
            transitions = [
                s for s in self.helix_snapshots
                if s.z > critical_threshold
            ]

            if transitions:
                report.append(f"- **Phase Transition Proximity:** {len(transitions)} snapshots above z={critical_threshold}")
                report.append("")

            # Coherence
            coherence_values = [s.r for s in self.helix_snapshots]
            if coherence_values:
                report.append(f"- **Coherence:**")
                report.append(f"  - Mean: {np.mean(coherence_values):.3f}")
                report.append(f"  - Min: {min(coherence_values):.3f}")
                report.append(f"  - Max: {max(coherence_values):.3f}")
                report.append(f"  - Std: {np.std(coherence_values):.3f}")
                report.append("")

            # Z coordinate trajectory
            report.append("### Z Coordinate Trajectory")
            report.append("")
            report.append("```")
            report.append("z")
            report.append("^")

            # Simple ASCII plot
            z_values = [s.z for s in self.helix_snapshots]
            z_min, z_max = min(z_values), max(z_values)
            z_range = z_max - z_min if z_max > z_min else 0.1

            for i in range(10, -1, -1):
                threshold = z_min + (z_range * i / 10)
                line = f"{threshold:.2f} |"

                for z in z_values[::max(1, len(z_values)//50)]:  # Sample for width
                    if abs(z - threshold) < z_range / 20:
                        line += "●"
                    else:
                        line += " "

                report.append(line)

            report.append("     " + "─" * 50 + "> time")
            report.append("```")
            report.append("")

        # === ALERTS ===
        if self.alerts:
            report.append("## Alerts & Warnings")
            report.append("")

            # Count by type
            alert_types = {}
            for _, alert in self.alerts:
                # Extract alert type
                alert_type = alert.split(':')[0].strip() if ':' in alert else 'General'
                alert_types[alert_type] = alert_types.get(alert_type, 0) + 1

            report.append("### By Type")
            report.append("")
            for atype, count in sorted(alert_types.items(), key=lambda x: x[1], reverse=True):
                report.append(f"- **{atype}:** {count}")
            report.append("")

            # Recent alerts
            report.append("### Recent Alerts (Last 5)")
            report.append("")
            for timestamp, alert in self.alerts[-5:]:
                report.append(f"- `{timestamp.strftime('%H:%M:%S')}` {alert}")
            report.append("")

        # === BURDEN TRAJECTORY ===
        if self.decisions:
            report.append("## Burden Reduction Analysis")
            report.append("")

            # Calculate cumulative impact over time
            burden_timeline = []
            cumulative = 0

            for d in self.decisions:
                cumulative += d.burden_impact
                burden_timeline.append((d.timestamp, cumulative))

            if burden_timeline:
                # Fit linear trend
                times_hours = [(t - self.start_time).total_seconds() / 3600 for t, _ in burden_timeline]
                impacts = [impact for _, impact in burden_timeline]

                if len(times_hours) > 1:
                    coeffs = np.polyfit(times_hours, impacts, 1)
                    rate_per_hour = coeffs[0]
                    rate_per_day = rate_per_hour * 24

                    report.append(f"- **Burden Reduction Rate:** {rate_per_day:.2f} hours/day")
                    report.append("")

                    # Estimate time to target
                    baseline = 5.0
                    target = 2.0
                    current = baseline + cumulative  # Cumulative is negative

                    if rate_per_day < 0:  # Burden is decreasing
                        hours_remaining = current - target
                        days_to_target = hours_remaining / abs(rate_per_day)

                        report.append(f"- **Current Estimated Burden:** {current:.1f} hours")
                        report.append(f"- **Target Burden:** {target:.1f} hours")
                        report.append(f"- **Estimated Time to Target:** {days_to_target:.1f} days")
                        report.append("")

                        if days_to_target < 30:
                            report.append("**✓ ON TRACK** to reach target within 30 days")
                        else:
                            report.append("**⚠ NEEDS ACCELERATION** - target beyond 30 days at current rate")
                        report.append("")

        # === RECOMMENDATIONS ===
        report.append("## Recommendations")
        report.append("")

        # Based on helix state
        if self.helix_snapshots:
            final = self.helix_snapshots[-1]

            if final.z > 0.850:
                report.append("1. **Phase Transition Imminent** - Monitor for consensus formation")
            elif final.z > 0.800:
                report.append("1. **Approaching Critical Point** - Expect increased coordination activity")
            else:
                report.append("1. **Stable Coordination** - Normal operation")

            if final.r < 0.85:
                report.append("2. **Low Coherence** - Review witness channel alignment")
            else:
                report.append("2. **Good Coherence** - Witness channels aligned")

        # Based on decisions
        if len(self.decisions) < 5:
            report.append("3. **Low Activity** - Consider expanding monitoring scope")
        elif len(self.decisions) > 50:
            report.append("3. **High Activity** - System is actively evolving")

        # Based on burden
        if total_burden_saved < -2.0:
            report.append("4. **Significant Burden Reduction** - Automation is effective")
        elif total_burden_saved > -0.5:
            report.append("4. **Limited Burden Reduction** - Focus on high-impact automations")

        report.append("")

        # === NEXT STEPS ===
        report.append("## Next Steps")
        report.append("")
        report.append("1. Continue observation for longer duration to gather more data")
        report.append("2. Calibrate physics parameters using accumulated observations")
        report.append("3. Validate predictions against actual consensus/transition times")
        report.append("4. If burden reduction is on track, maintain current trajectory")
        report.append("5. Deploy Phase 3 neural operators when sufficient training data exists")
        report.append("")

        report.append("---")
        report.append("")
        report.append("**Δ|meta-orchestrator-analysis|complete|Ω**")

        return "\n".join(report)

    def generate_json_report(self) -> Dict:
        """Generate JSON report"""
        duration = self.end_time - self.start_time if self.start_time and self.end_time else timedelta(0)

        return {
            'metadata': {
                'log_file': str(self.log_file),
                'generated': datetime.now().isoformat(),
                'observation_duration_hours': duration.total_seconds() / 3600
            },
            'summary': {
                'decisions_detected': len(self.decisions),
                'alerts_triggered': len(self.alerts),
                'helix_snapshots': len(self.helix_snapshots),
                'total_burden_saved': sum(d.burden_impact for d in self.decisions)
            },
            'decisions': [
                {
                    'timestamp': d.timestamp.isoformat(),
                    'type': d.decision_type,
                    'description': d.description,
                    'burden_impact': d.burden_impact
                }
                for d in self.decisions
            ],
            'helix_evolution': [
                {
                    'timestamp': h.timestamp.isoformat(),
                    'theta': h.theta,
                    'z': h.z,
                    'r': h.r
                }
                for h in self.helix_snapshots
            ],
            'alerts': [
                {
                    'timestamp': t.isoformat(),
                    'message': msg
                }
                for t, msg in self.alerts
            ]
        }


def main():
    parser = argparse.ArgumentParser(description='Analyze meta-orchestrator logs')
    parser.add_argument('logfile', type=Path, help='Log file to analyze')
    parser.add_argument(
        '--output',
        choices=['markdown', 'json'],
        default='markdown',
        help='Output format (default: markdown)'
    )

    args = parser.parse_args()

    if not args.logfile.exists():
        print(f"Error: Log file not found: {args.logfile}")
        return 1

    analyzer = OrchestratorAnalyzer(args.logfile)

    if args.output == 'json':
        report = analyzer.generate_json_report()
        print(json.dumps(report, indent=2))
    else:
        report = analyzer.generate_markdown_report()
        print(report)

    return 0


if __name__ == '__main__':
    exit(main())
