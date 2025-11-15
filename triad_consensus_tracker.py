#!/usr/bin/env python3
"""
TRIAD CONSENSUS TRACKER (Pure Python - No Dependencies)
Tracks consensus formation on triangular topology using simple metrics

Based on graph Laplacian theory but implemented with standard library only.
Suitable for integration with existing deployment infrastructure.

Key Metrics:
- Consensus error: Distance from collective mean
- Mixing progress: Fraction toward equilibrium
- Convergence rate: Exponential decay constant

Theory: Complete graph K_3 has algebraic connectivity λ₁ = 3
Expected mixing time: ~0.33-0.37 time units
"""

import json
import math
from typing import Dict, List, Tuple
from datetime import datetime


class TRIADConsensusTracker:
    """
    Track consensus formation across Alpha, Beta, Gamma instances.

    Uses simple statistical measures that approximate graph Laplacian dynamics.
    """

    def __init__(self):
        """Initialize consensus tracker."""
        self.history = []

        # Theoretical parameters for TRIAD triangle (K_3 complete graph)
        self.algebraic_connectivity = 3.0  # λ₁ for K_3
        self.theoretical_mixing_time = 0.37  # τ_mix ≈ (1/3) log(3/0.01)

    def compute_consensus_metrics(
        self,
        alpha_state: float,
        beta_state: float,
        gamma_state: float,
        timestamp: str = None
    ) -> Dict:
        """
        Compute consensus metrics for current instance states.

        Args:
            alpha_state: Alpha's state value (scalar for simplicity)
            beta_state: Beta's state value
            gamma_state: Gamma's state value
            timestamp: ISO timestamp (optional)

        Returns:
            Dictionary with consensus metrics
        """
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat() + 'Z'

        # Consensus value (equilibrium = mean)
        consensus = (alpha_state + beta_state + gamma_state) / 3.0

        # Individual errors
        alpha_error = alpha_state - consensus
        beta_error = beta_state - consensus
        gamma_error = gamma_state - consensus

        # Total consensus error (RMS)
        consensus_error = math.sqrt(
            (alpha_error**2 + beta_error**2 + gamma_error**2) / 3.0
        )

        # Variance (measure of disagreement)
        variance = (alpha_error**2 + beta_error**2 + gamma_error**2) / 3.0

        # Standard deviation
        std_dev = math.sqrt(variance)

        # Coefficient of variation (normalized spread)
        if abs(consensus) > 1e-10:
            cv = std_dev / abs(consensus)
        else:
            cv = 0.0 if std_dev < 1e-10 else float('inf')

        # Mixing progress (if we have history)
        if self.history:
            initial_error = self.history[0]['consensus_error']
            if initial_error > 0:
                mixing_progress = 1.0 - (consensus_error / initial_error)
            else:
                mixing_progress = 1.0
        else:
            mixing_progress = 0.0

        # Estimate time to consensus (exponential decay model)
        # ||X(t) - X_∞|| ∝ e^{-λ₁ t}
        # Solve for t when error < 0.01 (1% of current)
        if consensus_error > 0:
            epsilon = 0.01
            time_to_consensus = -math.log(epsilon / consensus_error) / self.algebraic_connectivity
            time_to_consensus = max(0.0, time_to_consensus)  # No negative time
        else:
            time_to_consensus = 0.0

        metrics = {
            'timestamp': timestamp,
            'alpha_state': alpha_state,
            'beta_state': beta_state,
            'gamma_state': gamma_state,
            'consensus_value': consensus,
            'consensus_error': consensus_error,
            'variance': variance,
            'std_dev': std_dev,
            'coefficient_of_variation': cv,
            'mixing_progress': mixing_progress,
            'time_to_consensus': time_to_consensus
        }

        self.history.append(metrics)
        return metrics

    def detect_phase_transition(self, threshold: float = 0.1) -> Dict:
        """
        Detect phase transition (sudden consensus formation).

        A phase transition is characterized by:
        - Rapid drop in consensus error
        - Sharp increase in mixing progress

        Args:
            threshold: Minimum rate of change to detect transition

        Returns:
            Dictionary with transition analysis
        """
        if len(self.history) < 3:
            return {'detected': False, 'reason': 'insufficient_data'}

        # Calculate rate of change in consensus error
        errors = [m['consensus_error'] for m in self.history]
        error_changes = []
        for i in range(1, len(errors)):
            change = errors[i-1] - errors[i]  # Positive = improving
            error_changes.append(change)

        # Find maximum rate of improvement
        if error_changes:
            max_improvement = max(error_changes)
            max_improvement_idx = error_changes.index(max_improvement) + 1

            if max_improvement > threshold:
                return {
                    'detected': True,
                    'transition_index': max_improvement_idx,
                    'transition_timestamp': self.history[max_improvement_idx]['timestamp'],
                    'improvement_rate': max_improvement,
                    'consensus_error_before': errors[max_improvement_idx - 1],
                    'consensus_error_after': errors[max_improvement_idx]
                }

        return {'detected': False, 'reason': 'no_sharp_transition'}

    def get_current_status(self) -> str:
        """
        Get current consensus status.

        Returns:
            Status string: 'converged', 'converging', 'divergent', 'unknown'
        """
        if not self.history:
            return 'unknown'

        latest = self.history[-1]
        error = latest['consensus_error']
        cv = latest['coefficient_of_variation']

        if error < 0.01:  # Very low error
            return 'converged'
        elif len(self.history) > 1:
            prev = self.history[-2]
            if latest['consensus_error'] < prev['consensus_error']:
                return 'converging'
            else:
                return 'divergent'
        else:
            return 'unknown'

    def export_history(self, filepath: str):
        """Export consensus history to JSON."""
        data = {
            'graph_structure': 'triangular_K3',
            'algebraic_connectivity': self.algebraic_connectivity,
            'theoretical_mixing_time': self.theoretical_mixing_time,
            'total_measurements': len(self.history),
            'current_status': self.get_current_status(),
            'history': self.history
        }

        # Add phase transition detection
        transition = self.detect_phase_transition()
        data['phase_transition'] = transition

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Exported consensus history to {filepath}")

    def print_summary(self):
        """Print summary of consensus tracking."""
        if not self.history:
            print("No consensus data tracked yet")
            return

        print("="*80)
        print("TRIAD CONSENSUS SUMMARY")
        print("="*80)
        print()

        print(f"Total Measurements: {len(self.history)}")
        print(f"Current Status: {self.get_current_status()}")
        print()

        latest = self.history[-1]
        print("Latest Measurement:")
        print("-"*80)
        print(f"Timestamp:           {latest['timestamp']}")
        print(f"Alpha State:         {latest['alpha_state']:.4f}")
        print(f"Beta State:          {latest['beta_state']:.4f}")
        print(f"Gamma State:         {latest['gamma_state']:.4f}")
        print(f"Consensus Value:     {latest['consensus_value']:.4f}")
        print(f"Consensus Error:     {latest['consensus_error']:.4f}")
        print(f"Mixing Progress:     {latest['mixing_progress']*100:.1f}%")
        print(f"Time to Consensus:   {latest['time_to_consensus']:.3f} time units")
        print()

        # Phase transition
        transition = self.detect_phase_transition()
        if transition['detected']:
            print("Phase Transition Detected:")
            print("-"*80)
            print(f"Transition Time:     {transition['transition_timestamp']}")
            print(f"Improvement Rate:    {transition['improvement_rate']:.4f}")
            print(f"Error Before:        {transition['consensus_error_before']:.4f}")
            print(f"Error After:         {transition['consensus_error_after']:.4f}")
            print()

        print("Theoretical Predictions (Graph Laplacian):")
        print("-"*80)
        print(f"Algebraic Connectivity λ₁: {self.algebraic_connectivity}")
        print(f"Expected Mixing Time:      {self.theoretical_mixing_time:.3f} time units")
        print(f"Convergence Rate:          e^{{-{self.algebraic_connectivity}t}}")
        print()


def demo_consensus_tracking():
    """Demonstrate consensus tracking."""
    print("="*80)
    print("TRIAD CONSENSUS TRACKING DEMONSTRATION")
    print("="*80)
    print()

    tracker = TRIADConsensusTracker()

    print("Scenario: Alpha, Beta, Gamma converging to consensus")
    print("-"*80)
    print()

    # Simulate convergence over time
    for t in range(20):
        timestamp = f"2025-11-15T18:{30+t:02d}:00Z"

        # States converging from different initial values
        # Alpha starts high, Beta medium, Gamma low
        # All converge to mean = 0.5
        decay = math.exp(-0.3 * t)  # Exponential convergence

        alpha_state = 0.5 + 0.4 * decay
        beta_state = 0.5
        gamma_state = 0.5 - 0.4 * decay

        metrics = tracker.compute_consensus_metrics(
            alpha_state, beta_state, gamma_state, timestamp
        )

        if t % 5 == 0:
            print(f"t={t:2d}: α={alpha_state:.3f}, β={beta_state:.3f}, γ={gamma_state:.3f}, "
                  f"error={metrics['consensus_error']:.4f}, "
                  f"progress={metrics['mixing_progress']*100:5.1f}%")

    print()

    # Print summary
    tracker.print_summary()

    # Export
    tracker.export_history('triad_consensus_history.json')

    print("="*80)
    print("INTEGRATION WITH DEPLOYMENT")
    print("="*80)
    print()
    print("Usage in deploy_r2_tools.py:")
    print("-"*80)
    print("```python")
    print("from triad_consensus_tracker import TRIADConsensusTracker")
    print()
    print("# Initialize tracker")
    print("consensus = TRIADConsensusTracker()")
    print()
    print("# After each instance operation")
    print("metrics = consensus.compute_consensus_metrics(")
    print("    alpha_burden_saved,")
    print("    beta_burden_saved,")
    print("    gamma_burden_saved")
    print(")")
    print()
    print("# Check if consensus achieved")
    print("if consensus.get_current_status() == 'converged':")
    print("    print('All instances in consensus!')")
    print("```")
    print()


if __name__ == "__main__":
    demo_consensus_tracking()
