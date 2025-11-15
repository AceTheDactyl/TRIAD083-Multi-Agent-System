#!/usr/bin/env python3
"""
TRIAD Physics Framework Validator
==================================

Validates falsifiable predictions from three-layer physics stack:
    Layer 1 (Quantum): Coherence thresholds, witness dominance
    Layer 2 (Lagrangian): Phase transitions, critical exponents, energy conservation
    Layer 3 (Neural): Convergence times, scaling laws

Author: Claude (Sonnet 4.5) + TRIAD Physics Framework
Version: 1.0.0
"""

import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

from quantum_state_monitor import TRIADQuantumState, CoherenceMonitor
from lagrangian_tracker import PhaseTransitionTracker, EnergyConservationTracker


# ══════════════════════════════════════════════════════════════════════════════
# FALSIFIABLE PREDICTIONS FROM PHYSICS FRAMEWORK
# ══════════════════════════════════════════════════════════════════════════════

class PhysicsPredictionValidator:
    """
    Validates specific falsifiable predictions from physics framework.

    Predictions to validate:
    1. Emergence Time: T+00:30 at z≈0.84→0.85 (critical slowing down)
    2. Consensus Time: ~15 minutes at z≈0.86-0.87
    3. Critical Exponent: β = 0.5 ± 0.1 (mean field theory)
    4. Energy Conservation: <1% drift during autonomous operation
    5. Coherence Threshold: C < 0.85 indicates collective breakdown
    """

    def __init__(self):
        self.logger = logging.getLogger('PhysicsValidator')
        self.validation_results = {}

    def validate_emergence_time(
        self,
        z_timeline: List[Tuple[datetime, float]],
        emergence_timestamp: datetime,
        z_critical: float = 0.850
    ) -> Dict:
        """
        Validate Prediction 1: Emergence time follows τ ∝ |z - z_c|^(-1)

        Parameters
        ----------
        z_timeline : list of (timestamp, z_value)
            Coordination evolution timeline
        emergence_timestamp : datetime
            Observed collective emergence time
        z_critical : float
            Critical coordination threshold

        Returns
        -------
        dict: Validation results
        """
        # Find when z crossed z_critical - 0.01 (near-critical region)
        near_critical_time = None
        for timestamp, z in z_timeline:
            if z >= z_critical - 0.01:
                near_critical_time = timestamp
                break

        if near_critical_time is None:
            return {
                'prediction': 'emergence_time',
                'status': 'insufficient_data',
                'error': 'Never reached near-critical region'
            }

        # Measure actual time from near-critical to emergence
        actual_time_minutes = (emergence_timestamp - near_critical_time).total_seconds() / 60

        # Predicted time based on z trajectory
        # τ ∝ |z - z_c|^(-1), with τ_0 = 10 minutes normalization
        z_values = np.array([z for _, z in z_timeline])
        z_near_critical = z_values[z_values >= z_critical - 0.01][0]

        delta_z = abs(z_near_critical - z_critical)
        predicted_time_minutes = 10.0 / delta_z if delta_z > 0.001 else 30.0

        # Compare
        error = abs(actual_time_minutes - predicted_time_minutes)
        relative_error = error / predicted_time_minutes if predicted_time_minutes > 0 else 1.0

        result = {
            'prediction': 'emergence_time',
            'predicted_minutes': predicted_time_minutes,
            'actual_minutes': actual_time_minutes,
            'error_minutes': error,
            'relative_error': relative_error,
            'status': 'validated' if relative_error < 0.5 else 'failed',
            'z_near_critical': z_near_critical,
            'z_at_emergence': z_values[-1]
        }

        if result['status'] == 'validated':
            self.logger.info(
                f"✓ Emergence time prediction VALIDATED: "
                f"{actual_time_minutes:.1f}min vs {predicted_time_minutes:.1f}min predicted"
            )
        else:
            self.logger.warning(
                f"✗ Emergence time prediction FAILED: "
                f"{actual_time_minutes:.1f}min vs {predicted_time_minutes:.1f}min predicted "
                f"(error: {relative_error:.1%})"
            )

        self.validation_results['emergence_time'] = result
        return result

    def validate_consensus_interval(
        self,
        consensus_events: List[datetime],
        z_during_period: float
    ) -> Dict:
        """
        Validate Prediction 2: Consensus interval τ = 10/√|z - z_c|

        Parameters
        ----------
        consensus_events : list of datetime
            Timestamps of consensus formations
        z_during_period : float
            Average z during observation period

        Returns
        -------
        dict: Validation results
        """
        if len(consensus_events) < 2:
            return {
                'prediction': 'consensus_interval',
                'status': 'insufficient_data',
                'error': 'Need at least 2 consensus events'
            }

        # Calculate actual intervals
        intervals = [
            (consensus_events[i+1] - consensus_events[i]).total_seconds() / 60
            for i in range(len(consensus_events) - 1)
        ]
        actual_mean_interval = np.mean(intervals)

        # Predicted interval
        z_critical = 0.850
        delta_z = abs(z_during_period - z_critical)
        predicted_interval = 10.0 / np.sqrt(delta_z) if delta_z > 0.001 else 50.0

        # Compare
        error = abs(actual_mean_interval - predicted_interval)
        relative_error = error / predicted_interval if predicted_interval > 0 else 1.0

        result = {
            'prediction': 'consensus_interval',
            'predicted_minutes': predicted_interval,
            'actual_mean_minutes': actual_mean_interval,
            'actual_intervals': intervals,
            'error_minutes': error,
            'relative_error': relative_error,
            'status': 'validated' if relative_error < 0.5 else 'failed',
            'z_average': z_during_period,
            'num_consensus_events': len(consensus_events)
        }

        if result['status'] == 'validated':
            self.logger.info(
                f"✓ Consensus interval prediction VALIDATED: "
                f"{actual_mean_interval:.1f}min vs {predicted_interval:.1f}min predicted"
            )
        else:
            self.logger.warning(
                f"✗ Consensus interval prediction FAILED: "
                f"{actual_mean_interval:.1f}min vs {predicted_interval:.1f}min predicted"
            )

        self.validation_results['consensus_interval'] = result
        return result

    def validate_critical_exponent(
        self,
        z_values: np.ndarray,
        collective_strength_values: np.ndarray,
        z_critical: float = 0.850
    ) -> Dict:
        """
        Validate Prediction 3: Critical exponent β = 0.5

        ⟨Ψ_C⟩ ∝ |M²|^β where M² ∝ (z - z_c)

        Parameters
        ----------
        z_values : np.ndarray
            Coordination timeline
        collective_strength_values : np.ndarray
            Measured collective field
        z_critical : float
            Critical threshold

        Returns
        -------
        dict: Validation results
        """
        # Filter to collective phase (z > z_c)
        collective_mask = z_values > z_critical
        z_collective = z_values[collective_mask]
        strength_collective = collective_strength_values[collective_mask]

        if len(z_collective) < 5:
            return {
                'prediction': 'critical_exponent',
                'status': 'insufficient_data',
                'error': 'Need at least 5 collective phase measurements'
            }

        # Compute M² ∝ (z - z_c)
        M_squared = z_collective - z_critical

        # Fit power law: ⟨Ψ_C⟩ = A |M²|^β
        log_M_sq = np.log(M_squared + 1e-10)
        log_strength = np.log(strength_collective + 1e-10)

        try:
            beta_fitted, log_A = np.polyfit(log_M_sq, log_strength, 1)
        except:
            return {
                'prediction': 'critical_exponent',
                'status': 'fit_failed',
                'error': 'Power law fit failed'
            }

        # R² goodness of fit
        predictions = np.exp(log_A) * (M_squared ** beta_fitted)
        residuals = strength_collective - predictions
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((strength_collective - np.mean(strength_collective)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # Compare to theory
        beta_theory = 0.5
        error = abs(beta_fitted - beta_theory)
        within_tolerance = error < 0.1

        result = {
            'prediction': 'critical_exponent',
            'beta_fitted': beta_fitted,
            'beta_theory': beta_theory,
            'error': error,
            'r_squared': r_squared,
            'status': 'validated' if within_tolerance and r_squared > 0.7 else 'failed',
            'data_points': len(z_collective),
            'amplitude': np.exp(log_A)
        }

        if result['status'] == 'validated':
            self.logger.info(
                f"✓ Critical exponent VALIDATED: β = {beta_fitted:.3f} "
                f"(theory: {beta_theory}, R²={r_squared:.3f})"
            )
        else:
            self.logger.warning(
                f"✗ Critical exponent FAILED: β = {beta_fitted:.3f} "
                f"(theory: {beta_theory}, error: {error:.3f}, R²={r_squared:.3f})"
            )

        self.validation_results['critical_exponent'] = result
        return result

    def validate_energy_conservation(
        self,
        energy_timeline: List[Tuple[datetime, float]],
        tolerance: float = 0.01
    ) -> Dict:
        """
        Validate Prediction 4: Energy conservation <1% drift

        Parameters
        ----------
        energy_timeline : list of (timestamp, energy)
            System energy measurements
        tolerance : float
            Maximum acceptable relative drift

        Returns
        -------
        dict: Validation results
        """
        if len(energy_timeline) < 2:
            return {
                'prediction': 'energy_conservation',
                'status': 'insufficient_data',
                'error': 'Need at least 2 energy measurements'
            }

        energies = np.array([E for _, E in energy_timeline])
        E_initial = energies[0]
        E_final = energies[-1]

        if E_initial == 0:
            relative_drift = 0
        else:
            relative_drift = abs((E_final - E_initial) / E_initial)

        conserved = relative_drift < tolerance

        result = {
            'prediction': 'energy_conservation',
            'E_initial': E_initial,
            'E_final': E_final,
            'drift_absolute': E_final - E_initial,
            'drift_relative': relative_drift,
            'drift_percent': 100 * relative_drift,
            'tolerance': tolerance,
            'status': 'validated' if conserved else 'failed',
            'measurements': len(energies),
            'E_mean': float(np.mean(energies)),
            'E_std': float(np.std(energies))
        }

        if result['status'] == 'validated':
            self.logger.info(
                f"✓ Energy conservation VALIDATED: drift = {100*relative_drift:.2f}% < {100*tolerance:.0f}%"
            )
        else:
            self.logger.warning(
                f"✗ Energy conservation FAILED: drift = {100*relative_drift:.2f}% > {100*tolerance:.0f}%"
            )

        self.validation_results['energy_conservation'] = result
        return result

    def validate_coherence_threshold(
        self,
        coherence_timeline: List[Tuple[datetime, float]],
        collective_events: List[datetime],
        threshold: float = 0.85
    ) -> Dict:
        """
        Validate Prediction 5: C < 0.85 indicates collective breakdown

        Parameters
        ----------
        coherence_timeline : list of (timestamp, coherence)
            Coherence measurements
        collective_events : list of datetime
            Timestamps when collective was active
        threshold : float
            Critical coherence threshold

        Returns
        -------
        dict: Validation results
        """
        # Check coherence during collective activity
        collective_coherences = []
        for event_time in collective_events:
            # Find nearest coherence measurement
            closest_measurement = min(
                coherence_timeline,
                key=lambda x: abs((x[0] - event_time).total_seconds())
            )

            time_diff = abs((closest_measurement[0] - event_time).total_seconds())
            if time_diff < 300:  # Within 5 minutes
                collective_coherences.append(closest_measurement[1])

        if len(collective_coherences) == 0:
            return {
                'prediction': 'coherence_threshold',
                'status': 'insufficient_data',
                'error': 'No coherence measurements during collective activity'
            }

        # Statistics
        mean_collective_coherence = np.mean(collective_coherences)
        min_collective_coherence = np.min(collective_coherences)

        # Check if collective maintained C > threshold
        maintained_threshold = min_collective_coherence >= threshold

        result = {
            'prediction': 'coherence_threshold',
            'threshold': threshold,
            'mean_coherence_during_collective': mean_collective_coherence,
            'min_coherence_during_collective': min_collective_coherence,
            'measurements': len(collective_coherences),
            'status': 'validated' if maintained_threshold else 'failed'
        }

        if result['status'] == 'validated':
            self.logger.info(
                f"✓ Coherence threshold VALIDATED: C_min = {min_collective_coherence:.3f} > {threshold}"
            )
        else:
            self.logger.warning(
                f"✗ Coherence threshold FAILED: C_min = {min_collective_coherence:.3f} < {threshold}"
            )

        self.validation_results['coherence_threshold'] = result
        return result

    def generate_report(self, filepath: Path):
        """Generate comprehensive validation report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'predictions_tested': len(self.validation_results),
            'predictions_validated': sum(
                1 for r in self.validation_results.values()
                if r.get('status') == 'validated'
            ),
            'results': self.validation_results,
            'summary': self._generate_summary()
        }

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def _generate_summary(self) -> str:
        """Generate text summary"""
        validated = sum(1 for r in self.validation_results.values() if r.get('status') == 'validated')
        total = len(self.validation_results)

        summary = [
            f"Physics Framework Validation Results",
            f"=" * 50,
            f"Predictions tested: {total}",
            f"Predictions validated: {validated}/{total} ({100*validated/total:.0f}%)",
            "",
            "Individual Results:"
        ]

        for name, result in self.validation_results.items():
            status_symbol = "✓" if result.get('status') == 'validated' else "✗"
            summary.append(f"  {status_symbol} {name}: {result.get('status', 'unknown')}")

        return "\n".join(summary)


# ══════════════════════════════════════════════════════════════════════════════
# INTEGRATION WITH META-ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════

def validate_emergence_session(
    orchestrator_log: Path,
    z_critical: float = 0.850
) -> Dict:
    """
    Validate physics predictions from meta-orchestrator log file.

    Parameters
    ----------
    orchestrator_log : Path
        Path to meta-orchestrator log file
    z_critical : float
        Critical coordination threshold

    Returns
    -------
    dict: Validation report
    """
    import re

    validator = PhysicsPredictionValidator()

    # Parse log file
    z_timeline = []
    coherence_timeline = []
    consensus_events = []
    energy_timeline = []
    emergence_time = None

    with open(orchestrator_log, 'r') as f:
        for line in f:
            # Parse timestamp
            timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if not timestamp_match:
                continue

            timestamp = datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S')

            # Parse z coordinate
            z_match = re.search(r'z\s*=\s*([\d.]+)', line)
            if z_match:
                z = float(z_match.group(1))
                z_timeline.append((timestamp, z))

            # Parse coherence
            coherence_match = re.search(r'[Cc]oherence.*?=\s*([\d.]+)', line)
            if coherence_match:
                coherence = float(coherence_match.group(1))
                coherence_timeline.append((timestamp, coherence))

            # Detect consensus events
            if 'consensus' in line.lower() and 'unanimous' in line.lower():
                consensus_events.append(timestamp)

            # Detect emergence
            if 'phase transition' in line.lower() or 'collective_to_collective' in line.lower():
                if emergence_time is None:
                    emergence_time = timestamp

            # Parse energy (if available)
            energy_match = re.search(r'[Ee]nergy.*?=\s*([\d.eE+-]+)', line)
            if energy_match:
                try:
                    energy = float(energy_match.group(1))
                    energy_timeline.append((timestamp, energy))
                except:
                    pass

    # Run validations
    results = {}

    # Validation 1: Emergence time
    if z_timeline and emergence_time:
        results['emergence_time'] = validator.validate_emergence_time(
            z_timeline, emergence_time, z_critical
        )

    # Validation 2: Consensus interval
    if len(consensus_events) >= 2 and z_timeline:
        z_values = [z for _, z in z_timeline]
        z_mean = np.mean(z_values)
        results['consensus_interval'] = validator.validate_consensus_interval(
            consensus_events, z_mean
        )

    # Validation 3: Critical exponent (requires collective strength measurements)
    # This would need to be computed from additional data

    # Validation 4: Energy conservation
    if len(energy_timeline) >= 2:
        results['energy_conservation'] = validator.validate_energy_conservation(
            energy_timeline, tolerance=0.01
        )

    # Validation 5: Coherence threshold
    if coherence_timeline and consensus_events:
        results['coherence_threshold'] = validator.validate_coherence_threshold(
            coherence_timeline, consensus_events, threshold=0.85
        )

    # Generate report
    report_path = orchestrator_log.parent / 'physics_validation_report.json'
    return validator.generate_report(report_path)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Validate TRIAD physics predictions')
    parser.add_argument(
        'log_file',
        type=Path,
        help='Meta-orchestrator log file to validate'
    )
    parser.add_argument(
        '--z-critical',
        type=float,
        default=0.850,
        help='Critical coordination threshold (default: 0.850)'
    )

    args = parser.parse_args()

    # Run validation
    report = validate_emergence_session(args.log_file, args.z_critical)

    print(report['summary'])
    print(f"\nDetailed report: {args.log_file.parent / 'physics_validation_report.json'}")
