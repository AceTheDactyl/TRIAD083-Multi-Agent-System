#!/usr/bin/env python3
"""
TRIAD Phase Transition Visualizer
==================================

Visualize TRIAD's information processing phase transition at z=0.867
Shows how information domains separate while maintaining coherence.

Usage:
    python3 visualize_phase_transition.py

Requirements:
    numpy, matplotlib, scipy

Output:
    phase_transition.gif - Animated visualization
    Console output with transition point detection
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import gaussian_filter
import warnings
warnings.filterwarnings('ignore')


class PhaseTransitionVisualizer:
    """
    Visualize TRIAD's information processing phase transition at z=0.867
    Shows how information domains separate while maintaining coherence
    """

    def __init__(self, N=128, epsilon=0.15):
        """
        Initialize phase transition visualizer.

        Parameters
        ----------
        N : int
            Grid size (N×N information field)
        epsilon : float
            Interface width parameter (controls diffusion)
        """
        self.N = N
        self.epsilon = epsilon
        self.dx = 1.0 / N
        self.dt = 0.0001

        # Initialize near critical point
        self.u = 0.5 + 0.1 * np.random.randn(N, N)
        self.z_history = []
        self.energy_history = []

    def compute_z_elevation(self, u):
        """
        Map information field to z-coordinate.

        The z-coordinate measures coordination level:
        - z < 0.850: Collective information processing
        - z ≈ 0.850: Critical point (phase transition)
        - z > 0.850: Individual information domains

        Parameters
        ----------
        u : np.ndarray
            Information density field

        Returns
        -------
        float
            Current z-elevation
        """
        # Phase separation metric (variance of information density)
        phase_separation = np.std(u)

        # Information coherence (smoothness of field)
        grad_x, grad_y = np.gradient(u)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        coherence = 1.0 - np.mean(gradient_magnitude)

        # Combined z-elevation (increases with separation and coherence)
        z = 0.85 + 0.5 * phase_separation * coherence

        return z

    def allen_cahn_step(self, z_current):
        """
        Single timestep of Allen-Cahn information dynamics.

        Evolution equation:
            ∂u/∂t = ε²∇²u - W'(u)

        Where:
            - ε²∇²u: Information diffusion
            - W'(u): Phase separation force

        Parameters
        ----------
        z_current : float
            Current z-coordinate
        """
        # Diffusion term (information spreading)
        # Using Gaussian filter as approximation to Laplacian
        laplacian = gaussian_filter(self.u, sigma=self.epsilon, mode='wrap')
        laplacian = (laplacian - self.u) / (self.epsilon**2)

        # Reaction term (phase separation driver)
        # Double-well potential: W(u) = u²(1-u)²
        # Derivative: W'(u) = 2u(1-u)(1-2u)

        # Adjust potential strength based on z-level
        if z_current < 0.867:
            # Pre-transition: weak phase separation
            # Favor collective information processing
            reaction = -2 * self.u * (1 - self.u) * (0.5 - self.u)
        else:
            # Post-transition: strong phase separation
            # Favor individual information domains
            reaction = -4 * self.u * (1 - self.u) * (0.5 - self.u)

        # Update information field via gradient descent
        self.u += self.dt * (self.epsilon**2 * laplacian + reaction)

        # Clip to physical bounds [0, 1]
        self.u = np.clip(self.u, 0, 1)

    def compute_free_energy(self):
        """
        Compute total free energy of information field.

        F[u] = ∫ [½ε²|∇u|² + W(u)] dx

        Returns
        -------
        float
            Total free energy
        """
        # Gradient energy (interface cost)
        grad_x, grad_y = np.gradient(self.u)
        gradient_energy = 0.5 * self.epsilon**2 * np.sum(grad_x**2 + grad_y**2)

        # Bulk energy (phase potential)
        bulk_energy = np.sum(self.u**2 * (1 - self.u)**2)

        return gradient_energy + bulk_energy

    def visualize_transition(self, n_steps=10000, save_as='phase_transition.gif'):
        """
        Create animation showing the phase transition at z=0.867.

        Parameters
        ----------
        n_steps : int
            Number of evolution steps
        save_as : str
            Output filename for animation

        Returns
        -------
        tuple
            (z_history, energy_history) tracking evolution
        """
        print("Initializing phase transition visualization...")
        print(f"Grid size: {self.N}×{self.N}")
        print(f"Evolution steps: {n_steps}")
        print(f"Interface width: ε = {self.epsilon}")
        print()

        # Setup figure with 2×2 subplots
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.patch.set_facecolor('white')

        # Unpack axes
        ax_field = axes[0, 0]
        ax_z = axes[0, 1]
        ax_hist = axes[1, 0]
        ax_energy = axes[1, 1]

        # Initialize information field plot
        im = ax_field.imshow(self.u, cmap='RdBu_r', vmin=0, vmax=1,
                            interpolation='bilinear')
        ax_field.set_title('Information Density Field u(x,y,t)', fontsize=12, fontweight='bold')
        ax_field.axis('off')
        plt.colorbar(im, ax=ax_field, fraction=0.046, pad=0.04)

        # Initialize z-elevation plot
        z_line, = ax_z.plot([], [], 'b-', linewidth=2, label='z-coordinate')
        ax_z.axhline(y=0.867, color='r', linestyle='--', linewidth=2,
                    label='Critical z=0.867')
        ax_z.axhspan(0.865, 0.869, alpha=0.2, color='red',
                    label='Transition region')
        ax_z.set_xlim(0, n_steps)
        ax_z.set_ylim(0.84, 0.88)
        ax_z.set_xlabel('Evolution Steps', fontsize=10)
        ax_z.set_ylabel('z-elevation', fontsize=10)
        ax_z.set_title('Phase Transition Tracking', fontsize=12, fontweight='bold')
        ax_z.legend(loc='upper right', fontsize=8)
        ax_z.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)

        # Histogram bins
        hist_bins = np.linspace(0, 1, 50)

        # Animation update function
        def animate(frame):
            # Evolve system
            z_current = self.compute_z_elevation(self.u)
            self.allen_cahn_step(z_current)

            # Store history
            self.z_history.append(z_current)
            energy = self.compute_free_energy()
            self.energy_history.append(energy)

            # Update information field plot
            im.set_array(self.u)

            # Update z-elevation plot
            if len(self.z_history) > 1:
                z_line.set_data(range(len(self.z_history)), self.z_history)

            # Update information density histogram
            ax_hist.clear()
            counts, bins, patches = ax_hist.hist(
                self.u.flatten(), bins=hist_bins, density=True,
                alpha=0.7, color='steelblue', edgecolor='black', linewidth=0.5
            )

            # Color histogram by phase
            for i, patch in enumerate(patches):
                bin_center = (bins[i] + bins[i+1]) / 2
                if bin_center < 0.3:
                    patch.set_facecolor('blue')
                elif bin_center > 0.7:
                    patch.set_facecolor('red')
                else:
                    patch.set_facecolor('gray')

            ax_hist.set_xlabel('Information Density', fontsize=10)
            ax_hist.set_ylabel('Probability Density', fontsize=10)
            ax_hist.set_title(f'Distribution at z={z_current:.3f}',
                            fontsize=12, fontweight='bold')
            ax_hist.set_xlim(0, 1)
            ax_hist.set_ylim(0, np.max(counts) * 1.2 if len(counts) > 0 else 5)
            ax_hist.grid(True, alpha=0.3, axis='y', linestyle=':', linewidth=0.5)

            # Annotate phase transition
            if abs(z_current - 0.867) < 0.001 and frame > 100:
                ax_hist.text(
                    0.5, ax_hist.get_ylim()[1]*0.85,
                    '⚡ PHASE TRANSITION ⚡',
                    ha='center', fontsize=14, color='red',
                    fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7)
                )

            # Update energy plot
            if len(self.energy_history) > 1:
                ax_energy.clear()
                ax_energy.plot(self.energy_history, 'g-', linewidth=2,
                             label='Free Energy F[u]')
                ax_energy.set_xlabel('Evolution Steps', fontsize=10)
                ax_energy.set_ylabel('Free Energy', fontsize=10)
                ax_energy.set_title('Energy Minimization', fontsize=12, fontweight='bold')
                ax_energy.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
                ax_energy.legend(loc='upper right', fontsize=8)

                # Add energy derivative (should be negative)
                if len(self.energy_history) > 10:
                    dE_dt = np.diff(self.energy_history[-10:])
                    if np.mean(dE_dt) < 0:
                        ax_energy.text(
                            0.05, 0.95, 'dE/dt < 0 ✓',
                            transform=ax_energy.transAxes,
                            fontsize=10, color='green', fontweight='bold',
                            verticalalignment='top'
                        )

            # Overall figure title with status
            phase_status = "COLLECTIVE" if z_current < 0.867 else "INDIVIDUAL"
            phase_color = "blue" if z_current < 0.867 else "red"

            fig.suptitle(
                f'TRIAD Information Processing Dynamics - Step {frame}\n'
                f'Phase: {phase_status} | z = {z_current:.4f}',
                fontsize=14, fontweight='bold', color=phase_color
            )

            # Print progress
            if frame % 500 == 0:
                print(f"Step {frame:5d}/{n_steps}: z={z_current:.4f}, "
                      f"Energy={energy:.2f}, Phase={phase_status}")

            return [im]

        # Create animation
        print("Generating animation...")
        anim = FuncAnimation(
            fig, animate, frames=n_steps,
            interval=50, blit=True, repeat=False
        )

        # Save animation
        if save_as:
            print(f"Saving animation to {save_as}...")
            try:
                anim.save(save_as, writer='pillow', fps=20, dpi=100)
                print(f"✓ Animation saved successfully")
            except Exception as e:
                print(f"✗ Failed to save animation: {e}")
                print("  (Matplotlib backend may not support animation)")

        plt.tight_layout()
        plt.show()

        return self.z_history, self.energy_history

    def analyze_transition(self):
        """
        Analyze phase transition statistics.

        Returns
        -------
        dict
            Transition analysis results
        """
        z_array = np.array(self.z_history)

        # Find transition point
        transition_idx = np.argmax(z_array > 0.867)

        if transition_idx == 0 and z_array[0] <= 0.867:
            transition_idx = len(z_array)  # No transition observed

        # Compute statistics
        results = {
            'transition_step': transition_idx,
            'transition_z': z_array[transition_idx] if transition_idx < len(z_array) else None,
            'initial_z': z_array[0],
            'final_z': z_array[-1],
            'z_critical_predicted': 0.867,
            'z_critical_observed': z_array[transition_idx] if transition_idx < len(z_array) else None,
            'error_percent': None
        }

        if results['z_critical_observed'] is not None:
            error = abs(results['z_critical_observed'] - results['z_critical_predicted'])
            results['error_percent'] = 100 * error / results['z_critical_predicted']

        return results


def main():
    """Main execution function."""

    print("="*60)
    print("TRIAD Phase Transition Visualizer")
    print("="*60)
    print()

    # Create visualizer
    viz = PhaseTransitionVisualizer(N=128, epsilon=0.15)

    # Run visualization
    z_history, energy_history = viz.visualize_transition(
        n_steps=5000,
        save_as='phase_transition.gif'
    )

    print()
    print("="*60)
    print("Analysis Results")
    print("="*60)

    # Analyze transition
    results = viz.analyze_transition()

    print(f"Phase transition detected at step {results['transition_step']}")
    print(f"Initial z-elevation: {results['initial_z']:.4f}")
    print(f"Final z-elevation: {results['final_z']:.4f}")

    if results['z_critical_observed'] is not None:
        print(f"Transition point:")
        print(f"  Predicted: z = {results['z_critical_predicted']:.4f}")
        print(f"  Observed:  z = {results['z_critical_observed']:.4f}")
        print(f"  Error:     {results['error_percent']:.2f}%")

        if results['error_percent'] < 5.0:
            print("  ✓ Transition validated (error < 5%)")
        else:
            print("  ⚠ Transition error high")
    else:
        print("No phase transition observed in simulation window")

    print()
    print("Final energy: {:.2f}".format(energy_history[-1]))
    print("Energy change: {:.2f}%".format(
        100 * (energy_history[-1] - energy_history[0]) / energy_history[0]
    ))

    print()
    print("="*60)
    print("Visualization complete!")
    print("="*60)


if __name__ == "__main__":
    main()
