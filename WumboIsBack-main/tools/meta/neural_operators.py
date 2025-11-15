#!/usr/bin/env python3
"""
TRIAD Neural Operators Framework
==================================

Implements Layer 3 physics framework: Neural operators for tool adaptation.

Features:
- Fourier Neural Operator (FNO) for learning solution operators
- Spectral Graph Theory for TRIAD K3 topology
- Physics-informed wrappers with conservation and symmetry enforcement
- Resolution-invariant function-to-function learning

Based on: Physics Framework Integration Document, Section 3
Author: Claude (Sonnet 4.5) + TRIAD Physics Framework
Version: 1.0.0
"""

import numpy as np
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
import logging

# Optional deep learning imports (graceful degradation if not available)
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.fft import fftn, ifftn, rfftn, irfftn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logging.warning("PyTorch not available. Neural operator features will be limited.")


# ══════════════════════════════════════════════════════════════════════════════
# SPECTRAL GRAPH THEORY - TRIAD K3 TOPOLOGY
# ══════════════════════════════════════════════════════════════════════════════

class TRIADGraphTopology:
    """
    Spectral graph theory for TRIAD's complete K3 graph (3 fully-connected nodes).

    Topology: Alpha ↔ Beta ↔ Gamma ↔ Alpha (complete triangle)

    Provides:
    - Graph Laplacian L = D - A
    - Eigendecomposition (spectrum analysis)
    - Diffusion operators e^{-tL}
    - Consensus dynamics
    """

    def __init__(self):
        """Initialize K3 graph topology for TRIAD."""
        # Adjacency matrix (undirected, unweighted)
        self.A = np.array([
            [0, 1, 1],  # Alpha connected to Beta, Gamma
            [1, 0, 1],  # Beta connected to Alpha, Gamma
            [1, 1, 0]   # Gamma connected to Alpha, Beta
        ], dtype=float)

        # Degree matrix
        self.D = np.diag(np.sum(self.A, axis=1))  # [2, 2, 2]

        # Graph Laplacian: L = D - A
        self.L = self.D - self.A
        # L = [[ 2, -1, -1],
        #      [-1,  2, -1],
        #      [-1, -1,  2]]

        # Normalized Laplacian: L_norm = D^{-1/2} L D^{-1/2}
        D_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(self.D)))
        self.L_norm = D_inv_sqrt @ self.L @ D_inv_sqrt

        # Eigendecomposition
        self.eigenvalues, self.eigenvectors = np.linalg.eigh(self.L)

        # For K3: eigenvalues = [0, 3, 3]
        # λ₀ = 0 (uniform mode, consensus)
        # λ₁ = λ₂ = 3 (Fiedler value, high-frequency modes)

        self.logger = logging.getLogger('GraphTopology')
        self._log_spectrum()

    def _log_spectrum(self):
        """Log spectral properties."""
        self.logger.info("=== TRIAD K3 Graph Spectrum ===")
        self.logger.info(f"Eigenvalues: {self.eigenvalues}")
        self.logger.info(f"Fiedler value (λ₁): {self.eigenvalues[1]}")
        self.logger.info(f"Algebraic connectivity: {self.eigenvalues[1]}")

    def diffusion_operator(self, t: float) -> np.ndarray:
        """
        Compute diffusion operator e^{-tL}.

        Solves heat equation: ∂X/∂t = -L X
        Solution: X(t) = e^{-tL} X(0)

        Parameters
        ----------
        t : float
            Diffusion time

        Returns
        -------
        np.ndarray: 3×3 diffusion matrix
        """
        # e^{-tL} = U diag(e^{-t λᵢ}) U^T
        eigenval_exp = np.exp(-t * self.eigenvalues)
        U = self.eigenvectors
        return U @ np.diag(eigenval_exp) @ U.T

    def consensus_time(self, tolerance: float = 0.01) -> float:
        """
        Estimate time to reach consensus (within tolerance).

        Consensus happens when high-frequency modes decay.
        Rate governed by Fiedler value λ₁.

        Parameters
        ----------
        tolerance : float
            Convergence threshold (default: 1%)

        Returns
        -------
        float: Time steps to consensus
        """
        # High-frequency modes decay as e^{-λ₁ t}
        # Want e^{-λ₁ t} < tolerance
        # t > -ln(tolerance) / λ₁
        lambda_1 = self.eigenvalues[1]  # Fiedler value
        return -np.log(tolerance) / lambda_1

    def apply_diffusion(self, initial_state: np.ndarray, t: float) -> np.ndarray:
        """
        Apply diffusion to initial node states.

        Parameters
        ----------
        initial_state : np.ndarray
            Initial values at 3 nodes [α, β, γ]
        t : float
            Diffusion time

        Returns
        -------
        np.ndarray: Final state after diffusion
        """
        D_t = self.diffusion_operator(t)
        return D_t @ initial_state

    def measure_consensus(self, state: np.ndarray) -> float:
        """
        Measure degree of consensus in current state.

        Perfect consensus: all nodes equal (variance = 0)
        No consensus: high variance

        Parameters
        ----------
        state : np.ndarray
            Current node values

        Returns
        -------
        float: Consensus measure in [0, 1] (1 = perfect consensus)
        """
        variance = np.var(state)
        # Normalize: use max possible variance for 3 nodes
        max_variance = 1.0  # Assumes normalized state
        consensus = 1.0 - min(variance / max_variance, 1.0)
        return consensus


# ══════════════════════════════════════════════════════════════════════════════
# FOURIER NEURAL OPERATOR (FNO)
# ══════════════════════════════════════════════════════════════════════════════

if TORCH_AVAILABLE:
    class SpectralConv1d(nn.Module):
        """
        1D Fourier layer for FNO.

        Performs convolution in Fourier space:
        1. FFT: u → û
        2. Multiply: û * R (learned filter)
        3. IFFT: û * R → v
        """

        def __init__(self, in_channels: int, out_channels: int, modes: int):
            """
            Initialize spectral convolution layer.

            Parameters
            ----------
            in_channels : int
                Input feature channels
            out_channels : int
                Output feature channels
            modes : int
                Number of Fourier modes to keep
            """
            super().__init__()
            self.in_channels = in_channels
            self.out_channels = out_channels
            self.modes = modes

            # Fourier weights (complex, learned)
            scale = 1.0 / (in_channels * out_channels)
            self.weights = nn.Parameter(
                scale * torch.rand(in_channels, out_channels, modes, 2)
            )

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            """
            Apply spectral convolution.

            Parameters
            ----------
            x : torch.Tensor
                Input (batch, channels, n_points)

            Returns
            -------
            torch.Tensor: Output (batch, channels, n_points)
            """
            batch_size = x.shape[0]

            # FFT
            x_ft = torch.fft.rfft(x, dim=-1)

            # Truncate to modes
            x_ft = x_ft[:, :, :self.modes]

            # Multiply by learned weights (treating complex as 2D real)
            out_ft = torch.zeros(
                batch_size, self.out_channels, self.modes,
                dtype=torch.cfloat, device=x.device
            )

            for i in range(self.in_channels):
                for j in range(self.out_channels):
                    # Convert real weights to complex
                    weight_complex = torch.complex(
                        self.weights[i, j, :, 0],
                        self.weights[i, j, :, 1]
                    )
                    out_ft[:, j, :] += x_ft[:, i, :] * weight_complex

            # Pad back to original size
            out_ft_padded = torch.nn.functional.pad(
                out_ft, (0, x.shape[-1]//2 + 1 - self.modes)
            )

            # IFFT
            out = torch.fft.irfft(out_ft_padded, n=x.shape[-1], dim=-1)

            return out


    class FNO1d(nn.Module):
        """
        Fourier Neural Operator for 1D problems.

        Learns mappings between function spaces:
        G: U → V where U, V are spaces of functions.

        Applications in TRIAD:
        - State evolution operators
        - Consensus accelerators
        - Tool adaptation functions
        """

        def __init__(
            self,
            modes: int = 12,
            width: int = 32,
            depth: int = 4,
            in_dim: int = 3,
            out_dim: int = 3
        ):
            """
            Initialize FNO.

            Parameters
            ----------
            modes : int
                Number of Fourier modes
            width : int
                Hidden feature dimension
            depth : int
                Number of spectral layers
            in_dim : int
                Input dimension (default: 3 for TRIAD nodes)
            out_dim : int
                Output dimension (default: 3 for TRIAD nodes)
            """
            super().__init__()
            self.modes = modes
            self.width = width
            self.depth = depth

            # Lifting layer: input → width channels
            self.fc0 = nn.Linear(in_dim, width)

            # Spectral convolution layers
            self.conv_layers = nn.ModuleList([
                SpectralConv1d(width, width, modes) for _ in range(depth)
            ])

            # Residual connection layers
            self.w_layers = nn.ModuleList([
                nn.Linear(width, width) for _ in range(depth)
            ])

            # Projection layers: width → output
            self.fc1 = nn.Linear(width, 128)
            self.fc2 = nn.Linear(128, out_dim)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            """
            Apply FNO operator.

            Parameters
            ----------
            x : torch.Tensor
                Input function (batch, n_points, in_dim)

            Returns
            -------
            torch.Tensor: Output function (batch, n_points, out_dim)
            """
            # Lift to higher dimension
            x = self.fc0(x)  # (batch, n_points, width)
            x = x.permute(0, 2, 1)  # (batch, width, n_points) for conv

            # Fourier layers with residual connections
            for conv, w in zip(self.conv_layers, self.w_layers):
                x1 = conv(x)
                x2 = w(x.permute(0, 2, 1)).permute(0, 2, 1)
                x = F.gelu(x1 + x2)

            # Project back to output dimension
            x = x.permute(0, 2, 1)  # (batch, n_points, width)
            x = F.gelu(self.fc1(x))
            x = self.fc2(x)

            return x


# ══════════════════════════════════════════════════════════════════════════════
# PHYSICS-INFORMED WRAPPERS
# ══════════════════════════════════════════════════════════════════════════════

if TORCH_AVAILABLE:
    class ConservationLayer(nn.Module):
        """
        Enforces conservation laws on network outputs.

        Example: Ensure total state sums to constant (mass conservation).
        """

        def __init__(self, target_sum: float = 1.0, dim: int = -1):
            """
            Initialize conservation layer.

            Parameters
            ----------
            target_sum : float
                Target sum for conservation (default: 1.0 for normalization)
            dim : int
                Dimension along which to conserve (default: -1, last dim)
            """
            super().__init__()
            self.target_sum = target_sum
            self.dim = dim

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            """
            Enforce conservation by normalization.

            Parameters
            ----------
            x : torch.Tensor
                Input tensor

            Returns
            -------
            torch.Tensor: Normalized tensor with sum = target_sum
            """
            current_sum = x.sum(dim=self.dim, keepdim=True)
            # Avoid division by zero
            current_sum = torch.clamp(current_sum, min=1e-10)
            return x * (self.target_sum / current_sum)


    class SymmetryEnforcementLayer(nn.Module):
        """
        Enforces permutation symmetry for TRIAD nodes.

        Makes output invariant to node relabeling:
        f(α, β, γ) = f(β, γ, α) = f(γ, α, β)
        """

        def __init__(self, mode: str = 'average'):
            """
            Initialize symmetry enforcement.

            Parameters
            ----------
            mode : str
                'average': Average over all permutations
                'max': Take max over permutations
            """
            super().__init__()
            self.mode = mode

            # K3 cyclic permutations
            self.permutations = [
                [0, 1, 2],  # Identity
                [1, 2, 0],  # Cyclic 1
                [2, 0, 1],  # Cyclic 2
            ]

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            """
            Apply symmetry enforcement.

            Parameters
            ----------
            x : torch.Tensor
                Input (batch, n_nodes=3, features) or (batch, n_nodes=3)
                Or (batch, time_points, n_nodes) for FNO output

            Returns
            -------
            torch.Tensor: Symmetrized output
            """
            # Apply all permutations
            permuted = []
            for perm in self.permutations:
                if x.dim() == 2:
                    # Shape: (batch, nodes)
                    permuted.append(x[:, perm])
                elif x.dim() == 3:
                    # Shape: (batch, time_points, nodes) - permute last dim
                    # Use advanced indexing to permute node dimension
                    permuted.append(x[..., perm])
                else:
                    raise ValueError(f"Unexpected tensor dim: {x.dim()}")

            # Stack and aggregate
            stacked = torch.stack(permuted, dim=0)

            if self.mode == 'average':
                return stacked.mean(dim=0)
            elif self.mode == 'max':
                return stacked.max(dim=0)[0]
            else:
                raise ValueError(f"Unknown mode: {self.mode}")


    class PhysicsInformedTRIAD(nn.Module):
        """
        Physics-informed wrapper for TRIAD state evolution.

        Combines:
        - Neural operator (FNO) for state evolution
        - Conservation layer (mass/energy conservation)
        - Symmetry enforcement (permutation invariance)
        """

        def __init__(
            self,
            operator: nn.Module,
            enforce_conservation: bool = True,
            enforce_symmetry: bool = True
        ):
            """
            Initialize physics-informed wrapper.

            Parameters
            ----------
            operator : nn.Module
                Base neural operator (e.g., FNO)
            enforce_conservation : bool
                Apply conservation layer
            enforce_symmetry : bool
                Apply symmetry enforcement
            """
            super().__init__()
            self.operator = operator

            # Physics constraint layers
            self.conservation = ConservationLayer() if enforce_conservation else None
            self.symmetry = SymmetryEnforcementLayer() if enforce_symmetry else None

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            """
            Apply physics-informed evolution.

            Parameters
            ----------
            x : torch.Tensor
                Initial state

            Returns
            -------
            torch.Tensor: Evolved state (satisfying physics constraints)
            """
            # Apply base operator
            out = self.operator(x)

            # Enforce physics constraints
            if self.conservation is not None:
                out = self.conservation(out)

            if self.symmetry is not None:
                out = self.symmetry(out)

            return out


# ══════════════════════════════════════════════════════════════════════════════
# NEURAL OPERATOR TRAINER
# ══════════════════════════════════════════════════════════════════════════════

class NeuralOperatorTrainer:
    """
    Trains neural operators for TRIAD state evolution.

    Learns mappings:
    - Initial state → Final state (after consensus/diffusion)
    - Tool configuration → Adapted configuration
    - Parameter space → Solution space
    """

    def __init__(
        self,
        graph_topology: TRIADGraphTopology,
        operator_config: Optional[Dict] = None
    ):
        """
        Initialize trainer.

        Parameters
        ----------
        graph_topology : TRIADGraphTopology
            TRIAD graph structure
        operator_config : dict, optional
            FNO configuration
        """
        self.graph = graph_topology
        self.config = operator_config or {
            'modes': 12,
            'width': 32,
            'depth': 4
        }

        self.logger = logging.getLogger('NeuralOperatorTrainer')

        # Initialize operator if torch available
        if TORCH_AVAILABLE:
            self.operator = FNO1d(**self.config)
            self.physics_wrapper = PhysicsInformedTRIAD(self.operator)
        else:
            self.operator = None
            self.physics_wrapper = None

    def generate_training_data(
        self,
        n_samples: int = 1000,
        t_max: float = 2.0
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate training data from graph diffusion dynamics.

        Creates pairs (initial_state, final_state) using exact diffusion.

        Parameters
        ----------
        n_samples : int
            Number of training examples
        t_max : float
            Maximum diffusion time

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]: (inputs, outputs)
        """
        inputs = []
        outputs = []

        for _ in range(n_samples):
            # Random initial state
            initial = np.random.randn(3)

            # Random diffusion time
            t = np.random.uniform(0.1, t_max)

            # Exact solution via diffusion operator
            final = self.graph.apply_diffusion(initial, t)

            inputs.append(initial)
            outputs.append(final)

        return np.array(inputs), np.array(outputs)

    def train(
        self,
        n_epochs: int = 100,
        batch_size: int = 32,
        learning_rate: float = 1e-3
    ) -> Dict:
        """
        Train neural operator on diffusion dynamics.

        Parameters
        ----------
        n_epochs : int
            Training epochs
        batch_size : int
            Batch size
        learning_rate : float
            Learning rate

        Returns
        -------
        dict: Training history
        """
        if not TORCH_AVAILABLE or self.physics_wrapper is None:
            self.logger.warning("PyTorch not available. Skipping training.")
            return {'status': 'skipped'}

        # Generate data
        X_train, Y_train = self.generate_training_data(n_samples=1000)

        # Convert to tensors
        X = torch.FloatTensor(X_train).unsqueeze(1)  # (N, 1, 3)
        Y = torch.FloatTensor(Y_train).unsqueeze(1)  # (N, 1, 3)

        # Optimizer
        optimizer = torch.optim.Adam(
            self.physics_wrapper.parameters(),
            lr=learning_rate
        )

        # Training loop
        history = {'loss': []}

        for epoch in range(n_epochs):
            # Shuffle data
            perm = torch.randperm(X.shape[0])
            X_shuffled = X[perm]
            Y_shuffled = Y[perm]

            epoch_loss = 0.0
            n_batches = 0

            # Mini-batch training
            for i in range(0, X.shape[0], batch_size):
                X_batch = X_shuffled[i:i+batch_size]
                Y_batch = Y_shuffled[i:i+batch_size]

                # Forward pass
                Y_pred = self.physics_wrapper(X_batch)

                # Loss (MSE)
                loss = F.mse_loss(Y_pred, Y_batch)

                # Backward pass
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()
                n_batches += 1

            avg_loss = epoch_loss / n_batches
            history['loss'].append(avg_loss)

            if (epoch + 1) % 10 == 0:
                self.logger.info(f"Epoch {epoch+1}/{n_epochs}, Loss: {avg_loss:.6f}")

        return history


# ══════════════════════════════════════════════════════════════════════════════
# MAIN - DEMONSTRATION
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Demonstrate neural operators for TRIAD."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("=" * 70)
    print("TRIAD Neural Operators - Layer 3 Physics Framework")
    print("=" * 70)

    # 1. Graph topology
    print("\n[1] Initializing K3 graph topology...")
    graph = TRIADGraphTopology()

    # Test diffusion
    print("\n[2] Testing graph diffusion...")
    initial_state = np.array([1.0, 0.0, 0.0])  # Alpha = 1, others = 0
    print(f"Initial state: {initial_state}")

    t_consensus = graph.consensus_time(tolerance=0.01)
    print(f"Predicted consensus time (1% tolerance): {t_consensus:.3f}")

    final_state = graph.apply_diffusion(initial_state, t=t_consensus)
    print(f"State after t={t_consensus:.3f}: {final_state}")
    print(f"Consensus measure: {graph.measure_consensus(final_state):.4f}")

    # 2. Neural operator training
    if TORCH_AVAILABLE:
        print("\n[3] Training neural operator...")
        trainer = NeuralOperatorTrainer(graph)
        history = trainer.train(n_epochs=50, batch_size=32)
        print(f"Final training loss: {history['loss'][-1]:.6f}")

        # Test trained operator
        print("\n[4] Testing trained operator...")
        test_input = torch.FloatTensor([[1.0, 0.0, 0.0]]).unsqueeze(1)
        with torch.no_grad():
            test_output = trainer.physics_wrapper(test_input)
        print(f"Operator prediction: {test_output.squeeze().numpy()}")

        # Compare with exact solution
        exact = graph.apply_diffusion(initial_state, t=1.0)
        print(f"Exact solution (t=1.0): {exact}")
    else:
        print("\n[3] PyTorch not available - skipping neural operator training")

    print("\n" + "=" * 70)
    print("Neural operators framework initialized successfully!")
    print("=" * 70)


if __name__ == '__main__':
    main()
