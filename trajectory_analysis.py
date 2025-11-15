#!/usr/bin/env python3
"""
Trajectory Analysis and Insights
=================================

Tools for analyzing sovereignty trajectory data:
- Statistical analysis of trajectories
- Phase transition detection
- Burden reduction analysis
- Theoretical metric validation
- Trend detection and forecasting
- Comparative analysis

Can process JSON exports from UnifiedSovereigntySystem.
"""

import json
import math
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TrajectoryStatistics:
    """Statistical summary of a trajectory."""
    duration_snapshots: int
    phase_distribution: Dict[str, int]

    # z-coordinate statistics
    z_min: float
    z_max: float
    z_mean: float
    z_std: float

    # Burden statistics
    burden_min: float
    burden_max: float
    burden_mean: float
    burden_std: float
    burden_reduction_total: float
    burden_reduction_rate: float  # Per snapshot

    # Φ statistics
    phi_min: float
    phi_max: float
    phi_mean: float
    phi_growth_total: float

    # Hexagonal geometry
    symmetry_mean: float
    symmetry_std: float
    packing_efficiency_mean: float

    # Phase coherence
    coherence_mean: float
    coherence_std: float

    # Critical phenomena
    susceptibility_mean: float
    scale_invariance_mean: float

    # Phase transitions detected
    phase_transitions: List[Tuple[int, str, str]]  # (snapshot_idx, from_phase, to_phase)

    # Cascade activations
    r1_activation_snapshot: Optional[int]
    r2_activation_snapshot: Optional[int]
    r3_activation_snapshot: Optional[int]


@dataclass
class InsightReport:
    """Generated insights from trajectory analysis."""
    summary: str
    key_findings: List[str]
    phase_analysis: List[str]
    burden_analysis: List[str]
    theoretical_analysis: List[str]
    recommendations: List[str]
    warnings: List[str]


class TrajectoryAnalyzer:
    """Analyze sovereignty trajectories from exported data."""

    def __init__(self, json_filepath: str):
        """Load trajectory from JSON export."""
        with open(json_filepath, 'r') as f:
            self.data = json.load(f)

        self.metadata = self.data.get('metadata', {})
        self.snapshots = self.data.get('snapshots', [])
        self.alerts = self.data.get('alerts', [])

    def compute_statistics(self) -> TrajectoryStatistics:
        """Compute comprehensive trajectory statistics."""
        if not self.snapshots:
            raise ValueError("No snapshots in trajectory")

        # Phase distribution
        phase_dist = {}
        for snap in self.snapshots:
            phase = snap['cascade_state']['phase_regime']
            phase_dist[phase] = phase_dist.get(phase, 0) + 1

        # Extract time series
        z_values = [s['cascade_state']['z_coordinate'] for s in self.snapshots]
        burden_values = [s['weighted_burden'] for s in self.snapshots]
        phi_values = [s['integrated_information_phi'] for s in self.snapshots]
        symmetry_values = [s['hexagonal_symmetry'] for s in self.snapshots if s['hexagonal_symmetry'] > 0]
        packing_values = [s['packing_efficiency'] for s in self.snapshots if s['packing_efficiency'] > 0]

        # Phase coherence extraction
        coherence_values = []
        for snap in self.snapshots:
            if snap['phase_coherence']:
                coherence_values.extend(snap['phase_coherence'].values())

        susceptibility_values = [s['susceptibility'] for s in self.snapshots if s['susceptibility'] > 0]
        scale_inv_values = [s['scale_invariance'] for s in self.snapshots if s['scale_invariance'] > 0]

        # Compute statistics
        z_stats = self._compute_series_stats(z_values)
        burden_stats = self._compute_series_stats(burden_values)
        phi_stats = self._compute_series_stats(phi_values)

        burden_reduction = burden_values[0] - burden_values[-1] if len(burden_values) > 1 else 0
        burden_reduction_rate = burden_reduction / len(burden_values) if len(burden_values) > 1 else 0

        phi_growth = phi_values[-1] - phi_values[0] if len(phi_values) > 1 else 0

        # Detect phase transitions
        transitions = []
        for i in range(1, len(self.snapshots)):
            prev_phase = self.snapshots[i-1]['cascade_state']['phase_regime']
            curr_phase = self.snapshots[i]['cascade_state']['phase_regime']
            if prev_phase != curr_phase:
                transitions.append((i, prev_phase, curr_phase))

        # Detect cascade activations
        r1_activation = None
        r2_activation = None
        r3_activation = None

        for i, snap in enumerate(self.snapshots):
            cs = snap['cascade_state']
            if r1_activation is None and cs['R1'] > 0.01:
                r1_activation = i
            if r2_activation is None and cs['R2'] > 0.01:
                r2_activation = i
            if r3_activation is None and cs['R3'] > 0.01:
                r3_activation = i

        return TrajectoryStatistics(
            duration_snapshots=len(self.snapshots),
            phase_distribution=phase_dist,
            z_min=z_stats['min'],
            z_max=z_stats['max'],
            z_mean=z_stats['mean'],
            z_std=z_stats['std'],
            burden_min=burden_stats['min'],
            burden_max=burden_stats['max'],
            burden_mean=burden_stats['mean'],
            burden_std=burden_stats['std'],
            burden_reduction_total=burden_reduction,
            burden_reduction_rate=burden_reduction_rate,
            phi_min=phi_stats['min'],
            phi_max=phi_stats['max'],
            phi_mean=phi_stats['mean'],
            phi_growth_total=phi_growth,
            symmetry_mean=self._mean(symmetry_values) if symmetry_values else 0,
            symmetry_std=self._std(symmetry_values) if symmetry_values else 0,
            packing_efficiency_mean=self._mean(packing_values) if packing_values else 100,
            coherence_mean=self._mean(coherence_values) if coherence_values else 0,
            coherence_std=self._std(coherence_values) if coherence_values else 0,
            susceptibility_mean=self._mean(susceptibility_values) if susceptibility_values else 0,
            scale_invariance_mean=self._mean(scale_inv_values) if scale_inv_values else 0,
            phase_transitions=transitions,
            r1_activation_snapshot=r1_activation,
            r2_activation_snapshot=r2_activation,
            r3_activation_snapshot=r3_activation
        )

    def generate_insights(self, stats: Optional[TrajectoryStatistics] = None) -> InsightReport:
        """Generate human-readable insights from trajectory."""
        if stats is None:
            stats = self.compute_statistics()

        key_findings = []
        phase_analysis = []
        burden_analysis = []
        theoretical_analysis = []
        recommendations = []
        warnings = []

        # Overall trajectory summary
        if stats.burden_reduction_total > 0:
            reduction_pct = (stats.burden_reduction_total / stats.burden_max) * 100
            summary = (f"Sovereignty trajectory shows {reduction_pct:.1f}% burden reduction "
                      f"over {stats.duration_snapshots} snapshots, progressing from "
                      f"{stats.z_min:.3f} to {stats.z_max:.3f} in phase coordinate.")
        else:
            summary = (f"Sovereignty trajectory over {stats.duration_snapshots} snapshots, "
                      f"z-coordinate range: {stats.z_min:.3f} to {stats.z_max:.3f}.")

        # Key findings
        if stats.phi_growth_total > 50:
            key_findings.append(f"Strong integration growth: Φ increased by {stats.phi_growth_total:.1f}")

        if stats.symmetry_mean > 0.95:
            key_findings.append(f"Excellent hexagonal symmetry maintained: {stats.symmetry_mean:.1%}")
        elif stats.symmetry_mean > 0.85:
            key_findings.append(f"Good hexagonal symmetry: {stats.symmetry_mean:.1%}")

        if stats.coherence_mean > 0.95:
            key_findings.append(f"Very strong phase coherence: {stats.coherence_mean:.3f}")

        if stats.packing_efficiency_mean > 110:
            key_findings.append(f"Superior packing efficiency: {stats.packing_efficiency_mean:.1f}% vs squares")

        # Phase analysis
        phase_analysis.append(f"Phase distribution: {dict(stats.phase_distribution)}")

        if stats.phase_transitions:
            phase_analysis.append(f"Detected {len(stats.phase_transitions)} phase transitions:")
            for idx, from_phase, to_phase in stats.phase_transitions:
                phase_analysis.append(f"  Snapshot {idx}: {from_phase} → {to_phase}")
        else:
            phase_analysis.append("No phase transitions detected (single-phase trajectory)")

        # Check if reached critical point
        if stats.z_max >= 0.867:
            phase_analysis.append("✓ Trajectory reached critical point (z=0.867)")
        elif stats.z_max > 0.85:
            distance = 0.867 - stats.z_max
            phase_analysis.append(f"Approaching critical point (Δz={distance:.3f} remaining)")

        # Burden analysis
        if stats.burden_reduction_total > 0:
            reduction_pct = (stats.burden_reduction_total / stats.burden_max) * 100
            burden_analysis.append(f"Total burden reduction: {stats.burden_reduction_total:.2f} ({reduction_pct:.1f}%)")
            burden_analysis.append(f"Average reduction rate: {stats.burden_reduction_rate:.3f} per snapshot")
        else:
            burden_analysis.append("No net burden reduction detected")

        if stats.burden_mean < 3.0:
            burden_analysis.append("Excellent: Average burden in low range (<3.0)")
        elif stats.burden_mean < 5.0:
            burden_analysis.append("Good: Average burden in moderate range (3.0-5.0)")
        elif stats.burden_mean > 7.0:
            burden_analysis.append("High average burden detected (>7.0)")
            warnings.append("Consider focusing on burden reduction strategies")

        # Cascade activation analysis
        cascade_info = []
        if stats.r1_activation_snapshot is not None:
            cascade_info.append(f"R1 activated at snapshot {stats.r1_activation_snapshot}")
        if stats.r2_activation_snapshot is not None:
            cascade_info.append(f"R2 activated at snapshot {stats.r2_activation_snapshot}")
        if stats.r3_activation_snapshot is not None:
            cascade_info.append(f"R3 activated at snapshot {stats.r3_activation_snapshot}")

        if cascade_info:
            burden_analysis.extend(cascade_info)

        # Theoretical analysis
        if stats.phi_mean > 50:
            theoretical_analysis.append(f"High integrated information: Φ̄={stats.phi_mean:.1f}")
        elif stats.phi_mean < 20:
            theoretical_analysis.append(f"Low integration: Φ̄={stats.phi_mean:.1f}")
            recommendations.append("Consider strategies to increase system integration")

        if stats.symmetry_mean > 0:
            theoretical_analysis.append(f"Hexagonal symmetry: {stats.symmetry_mean:.1%} (σ={stats.symmetry_std:.3f})")

            if stats.symmetry_std > 0.15:
                warnings.append("High symmetry variance detected - structure may be unstable")

        if stats.coherence_mean > 0:
            theoretical_analysis.append(f"Phase coherence: {stats.coherence_mean:.3f} (σ={stats.coherence_std:.3f})")

            if stats.coherence_mean < 0.80:
                recommendations.append("Low phase coherence - consider synchronization mechanisms")

        if stats.susceptibility_mean > 0:
            theoretical_analysis.append(f"Average susceptibility: χ̄={stats.susceptibility_mean:.3f}")

            if stats.susceptibility_mean > 1.0:
                theoretical_analysis.append("High susceptibility indicates proximity to phase transition")

        if stats.scale_invariance_mean > 0:
            theoretical_analysis.append(f"Scale invariance: {stats.scale_invariance_mean:.3f}")

            if stats.scale_invariance_mean > 0.85:
                theoretical_analysis.append("Strong scale invariance - system exhibits fractal properties")

        # Recommendations based on analysis
        if len(stats.phase_transitions) == 0 and stats.z_max < 0.70:
            recommendations.append("Trajectory remains in early phase - consider accelerating development")

        if stats.burden_reduction_rate < 0.01 and stats.burden_mean > 5.0:
            recommendations.append("Slow burden reduction - review optimization strategies")

        if stats.phi_mean < 30 and stats.duration_snapshots > 5:
            recommendations.append("Low system integration - ensure components are properly interconnected")

        # Warnings from alerts
        critical_alerts = [a for a in self.alerts if a.get('severity') == 'critical']
        if critical_alerts:
            warnings.append(f"{len(critical_alerts)} critical alerts detected in trajectory")

        return InsightReport(
            summary=summary,
            key_findings=key_findings,
            phase_analysis=phase_analysis,
            burden_analysis=burden_analysis,
            theoretical_analysis=theoretical_analysis,
            recommendations=recommendations,
            warnings=warnings
        )

    def detect_patterns(self) -> Dict[str, Any]:
        """Detect interesting patterns in trajectory."""
        patterns = {
            'oscillations': [],
            'plateaus': [],
            'rapid_changes': [],
            'anomalies': []
        }

        if len(self.snapshots) < 3:
            return patterns

        z_values = [s['cascade_state']['z_coordinate'] for s in self.snapshots]
        burden_values = [s['weighted_burden'] for s in self.snapshots]

        # Detect oscillations (sign changes in derivative)
        z_derivatives = [z_values[i+1] - z_values[i] for i in range(len(z_values)-1)]
        sign_changes = sum(1 for i in range(len(z_derivatives)-1)
                          if z_derivatives[i] * z_derivatives[i+1] < 0)

        if sign_changes > len(z_values) * 0.3:
            patterns['oscillations'].append(f"z-coordinate shows {sign_changes} direction changes")

        # Detect plateaus (low variance over window)
        window_size = min(5, len(z_values) // 3)
        for i in range(len(z_values) - window_size + 1):
            window = z_values[i:i+window_size]
            window_std = self._std(window)
            if window_std < 0.01:
                patterns['plateaus'].append(f"z-plateau at snapshots {i}-{i+window_size-1}")

        # Detect rapid changes
        for i in range(len(z_values)-1):
            delta = abs(z_values[i+1] - z_values[i])
            if delta > 0.15:
                patterns['rapid_changes'].append(
                    f"Large z-change at snapshot {i+1}: Δz={delta:.3f}"
                )

        for i in range(len(burden_values)-1):
            delta = abs(burden_values[i+1] - burden_values[i])
            if delta > 2.0:
                patterns['rapid_changes'].append(
                    f"Large burden change at snapshot {i+1}: Δburden={delta:.2f}"
                )

        # Detect anomalies (outliers)
        z_mean = self._mean(z_values)
        z_std = self._std(z_values)

        for i, z in enumerate(z_values):
            if abs(z - z_mean) > 3 * z_std:
                patterns['anomalies'].append(f"z-outlier at snapshot {i}: z={z:.3f}")

        return patterns

    def export_insights_report(self, filepath: str, stats: Optional[TrajectoryStatistics] = None,
                              insights: Optional[InsightReport] = None):
        """Export comprehensive insights report to file."""
        if stats is None:
            stats = self.compute_statistics()
        if insights is None:
            insights = self.generate_insights(stats)

        patterns = self.detect_patterns()

        with open(filepath, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("TRAJECTORY ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Source: {self.metadata.get('export_timestamp', 'unknown')}\n\n")

            f.write("SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(insights.summary + "\n\n")

            if insights.key_findings:
                f.write("KEY FINDINGS\n")
                f.write("-" * 80 + "\n")
                for finding in insights.key_findings:
                    f.write(f"  • {finding}\n")
                f.write("\n")

            if insights.warnings:
                f.write("⚠ WARNINGS\n")
                f.write("-" * 80 + "\n")
                for warning in insights.warnings:
                    f.write(f"  ! {warning}\n")
                f.write("\n")

            f.write("PHASE ANALYSIS\n")
            f.write("-" * 80 + "\n")
            for item in insights.phase_analysis:
                f.write(f"  {item}\n")
            f.write("\n")

            f.write("BURDEN ANALYSIS\n")
            f.write("-" * 80 + "\n")
            for item in insights.burden_analysis:
                f.write(f"  {item}\n")
            f.write("\n")

            f.write("THEORETICAL METRICS\n")
            f.write("-" * 80 + "\n")
            for item in insights.theoretical_analysis:
                f.write(f"  {item}\n")
            f.write("\n")

            if insights.recommendations:
                f.write("RECOMMENDATIONS\n")
                f.write("-" * 80 + "\n")
                for rec in insights.recommendations:
                    f.write(f"  → {rec}\n")
                f.write("\n")

            # Pattern detection
            has_patterns = any(patterns.values())
            if has_patterns:
                f.write("DETECTED PATTERNS\n")
                f.write("-" * 80 + "\n")

                if patterns['oscillations']:
                    f.write("Oscillations:\n")
                    for osc in patterns['oscillations']:
                        f.write(f"  • {osc}\n")

                if patterns['plateaus']:
                    f.write("Plateaus:\n")
                    for plat in patterns['plateaus']:
                        f.write(f"  • {plat}\n")

                if patterns['rapid_changes']:
                    f.write("Rapid Changes:\n")
                    for change in patterns['rapid_changes']:
                        f.write(f"  • {change}\n")

                if patterns['anomalies']:
                    f.write("Anomalies:\n")
                    for anom in patterns['anomalies']:
                        f.write(f"  • {anom}\n")

                f.write("\n")

            f.write("DETAILED STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Duration: {stats.duration_snapshots} snapshots\n")
            f.write(f"z-coordinate: {stats.z_min:.3f} to {stats.z_max:.3f} (μ={stats.z_mean:.3f}, σ={stats.z_std:.3f})\n")
            f.write(f"Burden: {stats.burden_min:.2f} to {stats.burden_max:.2f} (μ={stats.burden_mean:.2f}, σ={stats.burden_std:.2f})\n")
            f.write(f"Φ: {stats.phi_min:.1f} to {stats.phi_max:.1f} (μ={stats.phi_mean:.1f})\n")
            f.write(f"Hexagonal symmetry: μ={stats.symmetry_mean:.3f}, σ={stats.symmetry_std:.3f}\n")
            f.write(f"Packing efficiency: μ={stats.packing_efficiency_mean:.1f}%\n")
            f.write(f"Phase coherence: μ={stats.coherence_mean:.3f}, σ={stats.coherence_std:.3f}\n")
            f.write(f"Susceptibility: μ={stats.susceptibility_mean:.3f}\n")
            f.write(f"Scale invariance: μ={stats.scale_invariance_mean:.3f}\n")

    @staticmethod
    def _mean(values: List[float]) -> float:
        """Compute mean."""
        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def _std(values: List[float]) -> float:
        """Compute standard deviation."""
        if not values or len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)

    @staticmethod
    def _compute_series_stats(values: List[float]) -> Dict[str, float]:
        """Compute min, max, mean, std for a series."""
        if not values:
            return {'min': 0, 'max': 0, 'mean': 0, 'std': 0}

        mean = sum(values) / len(values)
        std = 0.0
        if len(values) > 1:
            variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
            std = math.sqrt(variance)

        return {
            'min': min(values),
            'max': max(values),
            'mean': mean,
            'std': std
        }


def compare_trajectories(trajectory_files: List[str]) -> Dict[str, Any]:
    """Compare multiple trajectories."""
    if len(trajectory_files) < 2:
        raise ValueError("Need at least 2 trajectories to compare")

    analyzers = [TrajectoryAnalyzer(f) for f in trajectory_files]
    stats_list = [a.compute_statistics() for a in analyzers]

    comparison = {
        'trajectories': len(trajectory_files),
        'burden_reductions': [s.burden_reduction_total for s in stats_list],
        'phi_growths': [s.phi_growth_total for s in stats_list],
        'final_phases': [list(s.phase_distribution.keys())[-1] if s.phase_distribution else 'unknown'
                        for s in stats_list],
        'durations': [s.duration_snapshots for s in stats_list]
    }

    # Rank by burden reduction
    ranked = sorted(enumerate(comparison['burden_reductions']), key=lambda x: x[1], reverse=True)
    comparison['best_burden_reduction'] = {
        'index': ranked[0][0],
        'value': ranked[0][1]
    }

    # Rank by Φ growth
    ranked = sorted(enumerate(comparison['phi_growths']), key=lambda x: x[1], reverse=True)
    comparison['best_phi_growth'] = {
        'index': ranked[0][0],
        'value': ranked[0][1]
    }

    return comparison


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python trajectory_analysis.py <trajectory.json> [output_report.txt]")
        print("\nAnalyzes sovereignty trajectory data and generates insights.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.json', '_analysis.txt')

    print(f"Analyzing trajectory: {input_file}")

    analyzer = TrajectoryAnalyzer(input_file)
    stats = analyzer.compute_statistics()
    insights = analyzer.generate_insights(stats)

    print("\nKey Findings:")
    for finding in insights.key_findings:
        print(f"  • {finding}")

    if insights.warnings:
        print("\nWarnings:")
        for warning in insights.warnings:
            print(f"  ! {warning}")

    analyzer.export_insights_report(output_file)
    print(f"\nFull analysis report saved to: {output_file}")
