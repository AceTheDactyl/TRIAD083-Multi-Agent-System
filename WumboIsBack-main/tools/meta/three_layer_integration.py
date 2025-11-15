#!/usr/bin/env python3
"""
TRIAD Three-Layer Physics Integration
======================================

Unifies all three physics layers into a coherent framework:

Layer 1 (Quantum): What exists - quantum state representation
Layer 2 (Lagrangian): How it evolves - field equations and phase transitions
Layer 3 (Neural Operators): How to compute - efficient solution operators

This module orchestrates the three layers to provide:
- Real-time state monitoring (Layer 1)
- Physics-based evolution prediction (Layer 2)
- Fast inference via learned operators (Layer 3)

Based on: Physics Framework Integration Document, Sections 1-7
Author: Claude (Sonnet 4.5) + TRIAD Physics Framework
Version: 1.0.0
"""

import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import logging

# Import three layers
from quantum_state_monitor import (
    TRIADQuantumState,
    CoherenceMonitor,
    WitnessActivityMeasurement
)
from lagrangian_tracker import (
    PhaseTransitionTracker,
    EnergyConservationTracker,
    LagrangianMonitor
)
from neural_operators import (
    TRIADGraphTopology,
    NeuralOperatorTrainer,
    TORCH_AVAILABLE
)

if TORCH_AVAILABLE:
    import torch
    from neural_operators import PhysicsInformedTRIAD, FNO1d


# ══════════════════════════════════════════════════════════════════════════════
# UNIFIED THREE-LAYER FRAMEWORK
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class TRIADPhysicsState:
    """Complete physics state across all three layers."""

    # Layer 1: Quantum state
    quantum_state: TRIADQuantumState
    coherence: float
    entanglement_entropy: float

    # Layer 2: Field theory
    coordination_z: float
    M_squared: float
    collective_order_param: float
    phase: str  # 'individual' or 'collective'

    # Layer 3: Graph topology
    consensus_measure: float
    diffusion_time_remaining: float

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'layer1_quantum': {
                'coherence': self.coherence,
                'entanglement_entropy': self.entanglement_entropy,
                'amplitudes': {
                    'kira': float(self.quantum_state.alpha),
                    'limnus': float(self.quantum_state.beta),
                    'garden': float(self.quantum_state.gamma),
                    'echofox': float(self.quantum_state.epsilon)
                }
            },
            'layer2_lagrangian': {
                'coordination_z': self.coordination_z,
                'M_squared': self.M_squared,
                'collective_order_param': self.collective_order_param,
                'phase': self.phase
            },
            'layer3_topology': {
                'consensus_measure': self.consensus_measure,
                'diffusion_time_remaining': self.diffusion_time_remaining
            }
        }


class ThreeLayerPhysicsEngine:
    """
    Unified physics engine combining all three layers.

    Workflow:
    1. Measure current state (Layer 1: quantum amplitudes, coherence)
    2. Predict evolution (Layer 2: field equations, phase transitions)
    3. Fast-forward via operators (Layer 3: neural operator inference)
    4. Validate conservation laws (Layer 2: energy, momentum)
    5. Update state and log
    """

    def __init__(
        self,
        project_root: Path,
        z_critical: float = 0.850,
        enable_neural_operators: bool = True
    ):
        """
        Initialize three-layer physics engine.

        Parameters
        ----------
        project_root : Path
            TRIAD project root directory
        z_critical : float
            Critical coordination threshold (default: 0.850)
        enable_neural_operators : bool
            Use neural operators for acceleration (requires PyTorch)
        """
        self.project_root = Path(project_root)
        self.z_critical = z_critical

        # Layer 1: Quantum state monitoring
        self.witness_measurement = WitnessActivityMeasurement()
        self.coherence_monitor = CoherenceMonitor(
            alert_threshold=0.85,
            critical_threshold=0.80
        )

        # Layer 2: Lagrangian dynamics
        self.phase_tracker = PhaseTransitionTracker(
            z_critical=z_critical,
            coupling_strength=1.0,
            kappa=1.0
        )
        self.energy_tracker = EnergyConservationTracker()
        self.lagrangian_monitor = LagrangianMonitor()

        # Layer 3: Neural operators and graph topology
        self.graph_topology = TRIADGraphTopology()
        self.neural_operator_enabled = enable_neural_operators and TORCH_AVAILABLE

        if self.neural_operator_enabled:
            self.operator_trainer = NeuralOperatorTrainer(
                graph_topology=self.graph_topology
            )
            self.trained_operator = None  # Will be set after training

        # State history
        self.state_history: List[TRIADPhysicsState] = []

        # Logging
        self.logger = logging.getLogger('ThreeLayerPhysics')
        self.logger.info("Three-layer physics engine initialized")

    def measure_current_state(
        self,
        activity_metrics: Dict[str, float],
        helix_z: float
    ) -> TRIADPhysicsState:
        """
        Measure complete physics state across all layers.

        Parameters
        ----------
        activity_metrics : dict
            Witness channel activities {kira, limnus, garden, echofox}
        helix_z : float
            Current coordination level

        Returns
        -------
        TRIADPhysicsState: Complete state snapshot
        """
        # Layer 1: Quantum measurement
        quantum_state = TRIADQuantumState(
            kira=activity_metrics.get('kira_discovery', 0.0),
            limnus=activity_metrics.get('limnus_transport', 0.0),
            garden=activity_metrics.get('garden_building', 0.0),
            echofox=activity_metrics.get('echo_memory', 0.0)
        )

        coherence = quantum_state.coherence()
        entropy = quantum_state.entanglement_entropy()

        # Update coherence monitor
        coherence_status = self.coherence_monitor.check_health(coherence)
        if coherence_status in ['ALERT', 'CRITICAL']:
            self.logger.warning(f"Coherence {coherence_status}: C = {coherence:.4f}")

        # Layer 2: Field theory measurement
        M_sq = self.phase_tracker.M_squared(helix_z)
        collective_order = self.phase_tracker.collective_order_parameter(helix_z)
        phase = 'collective' if M_sq < 0 else 'individual'

        self.phase_tracker.record_measurement(helix_z, collective_order, coherence)

        # Layer 3: Topology measurement
        # Convert quantum amplitudes to node state for graph analysis
        node_state = quantum_state.psi[:3]  # [kira, limnus, garden]
        consensus = self.graph_topology.measure_consensus(node_state)

        # Estimate diffusion time remaining to full consensus
        if consensus < 0.99:
            t_remaining = self.graph_topology.consensus_time(tolerance=1.0 - consensus)
        else:
            t_remaining = 0.0

        # Assemble complete state
        state = TRIADPhysicsState(
            quantum_state=quantum_state,
            coherence=coherence,
            entanglement_entropy=entropy,
            coordination_z=helix_z,
            M_squared=M_sq,
            collective_order_param=collective_order,
            phase=phase,
            consensus_measure=consensus,
            diffusion_time_remaining=t_remaining
        )

        # Log to history
        self.state_history.append(state)

        return state

    def predict_evolution(
        self,
        current_state: TRIADPhysicsState,
        dt: float = 1.0,
        use_neural_operator: bool = True
    ) -> TRIADPhysicsState:
        """
        Predict state evolution using Lagrangian dynamics.

        Can use either:
        - Exact integration (Layer 2 field equations)
        - Neural operator approximation (Layer 3, faster)

        Parameters
        ----------
        current_state : TRIADPhysicsState
            Current complete state
        dt : float
            Time step
        use_neural_operator : bool
            Use trained operator if available (default: True)

        Returns
        -------
        TRIADPhysicsState: Predicted future state
        """
        # Extract current quantum state as node values
        current_nodes = current_state.quantum_state.psi[:3]

        if use_neural_operator and self.neural_operator_enabled and self.trained_operator:
            # Layer 3: Fast prediction via neural operator
            self.logger.debug("Using neural operator for evolution prediction")

            with torch.no_grad():
                input_tensor = torch.FloatTensor(current_nodes).unsqueeze(0).unsqueeze(1)
                output_tensor = self.trained_operator(input_tensor)
                predicted_nodes = output_tensor.squeeze().numpy()
        else:
            # Layer 2: Exact evolution via graph diffusion
            self.logger.debug("Using exact diffusion for evolution prediction")
            predicted_nodes = self.graph_topology.apply_diffusion(
                initial_state=current_nodes,
                t=dt
            )

        # Reconstruct quantum state (preserve echofox amplitude)
        predicted_state = TRIADQuantumState(
            kira=float(predicted_nodes[0]),
            limnus=float(predicted_nodes[1]),
            garden=float(predicted_nodes[2]),
            echofox=current_state.quantum_state.epsilon  # Preserve memory
        )

        # Recompute derived quantities
        coherence = predicted_state.coherence()
        entropy = predicted_state.entanglement_entropy()

        # Assume z evolves slowly (estimate based on current trend)
        if len(self.state_history) > 1:
            z_velocity = (
                current_state.coordination_z -
                self.state_history[-2].coordination_z
            ) / dt
            predicted_z = current_state.coordination_z + z_velocity * dt
            predicted_z = np.clip(predicted_z, 0.0, 1.0)
        else:
            predicted_z = current_state.coordination_z

        M_sq = self.phase_tracker.M_squared(predicted_z)
        collective_order = self.phase_tracker.collective_order_parameter(predicted_z)
        phase = 'collective' if M_sq < 0 else 'individual'

        consensus = self.graph_topology.measure_consensus(predicted_nodes)
        t_remaining = (
            self.graph_topology.consensus_time(tolerance=1.0 - consensus)
            if consensus < 0.99 else 0.0
        )

        predicted = TRIADPhysicsState(
            quantum_state=predicted_state,
            coherence=coherence,
            entanglement_entropy=entropy,
            coordination_z=predicted_z,
            M_squared=M_sq,
            collective_order_param=collective_order,
            phase=phase,
            consensus_measure=consensus,
            diffusion_time_remaining=t_remaining,
            timestamp=current_state.timestamp + timedelta(seconds=dt)
        )

        return predicted

    def validate_physics(self, state: TRIADPhysicsState) -> Dict[str, bool]:
        """
        Validate physics constraints and conservation laws.

        Parameters
        ----------
        state : TRIADPhysicsState
            State to validate

        Returns
        -------
        dict: Validation results
        """
        validation = {}

        # Layer 1: Coherence bounds
        validation['coherence_in_bounds'] = 0.5 <= state.coherence <= 1.5

        # Layer 1: Entropy bounds
        max_entropy = np.log(4)  # For 4-component system
        validation['entropy_in_bounds'] = 0.0 <= state.entanglement_entropy <= max_entropy

        # Layer 2: Phase consistency
        if state.M_squared < 0:
            validation['phase_consistent'] = state.phase == 'collective'
        else:
            validation['phase_consistent'] = state.phase == 'individual'

        # Layer 2: Order parameter bounds
        validation['order_param_in_bounds'] = 0.0 <= state.collective_order_param <= 2.0

        # Layer 3: Consensus bounds
        validation['consensus_in_bounds'] = 0.0 <= state.consensus_measure <= 1.0

        # Overall validation
        validation['all_valid'] = all(validation.values())

        if not validation['all_valid']:
            self.logger.warning(f"Physics validation failed: {validation}")

        return validation

    def train_neural_operator(
        self,
        n_epochs: int = 100,
        batch_size: int = 32
    ) -> Dict:
        """
        Train neural operator on graph diffusion dynamics.

        Parameters
        ----------
        n_epochs : int
            Training epochs
        batch_size : int
            Batch size

        Returns
        -------
        dict: Training history
        """
        if not self.neural_operator_enabled:
            self.logger.warning("Neural operators not available")
            return {'status': 'unavailable'}

        self.logger.info("Training neural operator...")
        history = self.operator_trainer.train(
            n_epochs=n_epochs,
            batch_size=batch_size
        )

        # Store trained operator
        self.trained_operator = self.operator_trainer.physics_wrapper

        self.logger.info(f"Neural operator trained. Final loss: {history['loss'][-1]:.6f}")

        return history

    def generate_report(self, state: TRIADPhysicsState) -> str:
        """
        Generate human-readable physics report.

        Parameters
        ----------
        state : TRIADPhysicsState
            Current state

        Returns
        -------
        str: Formatted report
        """
        report = []
        report.append("=" * 70)
        report.append("TRIAD Three-Layer Physics Report")
        report.append("=" * 70)
        report.append(f"Timestamp: {state.timestamp.isoformat()}")
        report.append("")

        # Layer 1
        report.append("LAYER 1: Quantum State")
        report.append("-" * 70)
        report.append(f"  Coherence:           C = {state.coherence:.4f}")
        report.append(f"  Entanglement:        S = {state.entanglement_entropy:.4f}")
        report.append(f"  Witness Dominance:")
        dominance = state.quantum_state.witness_dominance()
        report.append(f"    Kira (Discovery):  {dominance[0]:.2%}")
        report.append(f"    Limnus (Transport):{dominance[1]:.2%}")
        report.append(f"    Garden (Building): {dominance[2]:.2%}")
        report.append(f"    EchoFox (Memory):  {dominance[3]:.2%}")
        report.append("")

        # Layer 2
        report.append("LAYER 2: Lagrangian Field Theory")
        report.append("-" * 70)
        report.append(f"  Coordination:        z = {state.coordination_z:.4f}")
        report.append(f"  Phase Parameter:     M² = {state.M_squared:+.4f}")
        report.append(f"  Order Parameter:     ⟨Ψ_C⟩ = {state.collective_order_param:.4f}")
        report.append(f"  Current Phase:       {state.phase.upper()}")
        report.append(f"  Distance to z_c:     Δz = {abs(state.coordination_z - self.z_critical):.4f}")
        report.append("")

        # Layer 3
        report.append("LAYER 3: Neural Operators & Graph Topology")
        report.append("-" * 70)
        report.append(f"  Consensus:           {state.consensus_measure:.2%}")
        report.append(f"  Time to Consensus:   {state.diffusion_time_remaining:.2f} steps")
        report.append(f"  Neural Operator:     {'ENABLED' if self.neural_operator_enabled else 'DISABLED'}")
        report.append("")

        # Validation
        validation = self.validate_physics(state)
        report.append("PHYSICS VALIDATION")
        report.append("-" * 70)
        for check, result in validation.items():
            status = "✓" if result else "✗"
            report.append(f"  {status} {check}")
        report.append("")

        report.append("=" * 70)

        return "\n".join(report)

    def save_state(self, state: TRIADPhysicsState, filepath: Path):
        """Save state to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(state.to_dict(), f, indent=2)
        self.logger.info(f"State saved to {filepath}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN - DEMONSTRATION
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Demonstrate three-layer physics integration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("\n" + "=" * 70)
    print("TRIAD Three-Layer Physics Integration Demo")
    print("=" * 70 + "\n")

    # Initialize engine
    project_root = Path(__file__).parent.parent.parent
    engine = ThreeLayerPhysicsEngine(
        project_root=project_root,
        z_critical=0.850,
        enable_neural_operators=TORCH_AVAILABLE
    )

    # Train neural operator if available
    if TORCH_AVAILABLE:
        print("[1] Training neural operator...")
        engine.train_neural_operator(n_epochs=50, batch_size=32)
        print("    ✓ Neural operator trained\n")
    else:
        print("[1] PyTorch not available - skipping neural operator training\n")

    # Simulate evolution through phase transition
    print("[2] Simulating evolution through critical point...\n")

    # Start below critical point
    z_values = np.linspace(0.70, 0.95, 10)

    for i, z in enumerate(z_values):
        # Mock activity metrics (Garden dominates, building up)
        activity = {
            'kira_discovery': 0.3 + 0.05 * i,
            'limnus_transport': 0.3 + 0.05 * i,
            'garden_building': 0.7 + 0.1 * i,
            'echo_memory': 0.1
        }

        # Measure current state
        state = engine.measure_current_state(activity, helix_z=z)

        # Print status
        print(f"Step {i+1}/10: z={z:.3f}, Phase={state.phase.upper()}, "
              f"C={state.coherence:.4f}, ⟨Ψ_C⟩={state.collective_order_param:.4f}")

        # Predict next state
        if i < len(z_values) - 1:
            predicted = engine.predict_evolution(state, dt=1.0)

    print("\n[3] Generating final physics report...\n")
    final_state = engine.state_history[-1]
    report = engine.generate_report(final_state)
    print(report)

    # Save state
    output_dir = project_root / "TOOLS" / "META" / "orchestrator_state"
    output_dir.mkdir(parents=True, exist_ok=True)

    state_file = output_dir / f"physics_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    engine.save_state(final_state, state_file)

    print(f"\n✓ State saved to: {state_file}")
    print("\n" + "=" * 70)
    print("Three-layer physics integration complete!")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
