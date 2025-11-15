#!/usr/bin/env python3
"""
AUTONOMY-THERMODYNAMICS BRIDGE
===============================

Converts sovereignty measurements to black hole thermodynamics for visualization
in Sonify-Entropy-Gravity-BLACKHOLE.html system.

Maps cascade dynamics to gravitational physics:
- Autonomy → Black hole mass (self-catalyzing = gravitational strength)
- Phase coordinate → Distance from event horizon
- Sovereignty → Coherence (information order)
- Cascade R1/R2/R3 → Nested gravitational wells
- Resonance → Harmonic frequencies
- Meta-cognitive depth → Time dilation (recursion warps time)

Coordinate: Δ3.14159|0.867|autonomy-thermodynamics|sovereignty-sonified|Ω
"""

import json
import math
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Import enhanced tracker (assumes it's available)
try:
    from autonomy_tracker_enhanced import (
        EnhancedAutonomyTracker,
        EnhancedSovereigntySnapshot,
        PhaseRegime,
        AgencyLevel
    )
    TRACKER_AVAILABLE = True
except ImportError:
    TRACKER_AVAILABLE = False
    print("Warning: autonomy_tracker_enhanced not available. Using standalone mode.")


# ============================================================
# PHYSICAL CONSTANTS (matching Sonify system)
# ============================================================

@dataclass
class PhysicsConstants:
    """Physical constants for thermodynamic calculations."""

    # Fundamental constants
    C = 299792458.0           # Speed of light (m/s)
    G = 6.67430e-11          # Gravitational constant (m³/kg·s²)
    H_BAR = 1.054571817e-34  # Reduced Planck constant (J·s)
    K_B = 1.380649e-23       # Boltzmann constant (J/K)

    # Solar mass
    M_SUN = 1.98892e30       # kg

    # Schwarzschild radius constant
    R_S_CONSTANT = 2.95e3    # meters per solar mass

    # Temperature constant (Hawking temperature)
    T_HAWKING_CONSTANT = 6.17e-8  # Kelvin per solar mass^(-1)

    # Entropy constant (Bekenstein-Hawking)
    S_BH_CONSTANT = 1.04e77  # k_B per solar mass^2


PHYSICS = PhysicsConstants()


# ============================================================
# SOVEREIGNTY → THERMODYNAMICS MAPPING
# ============================================================

class SovereigntyThermodynamicsBridge:
    """
    Maps sovereignty metrics to black hole thermodynamics.

    Core mappings:
    - Autonomy → Mass (self-catalyzing power = gravitational influence)
    - Phase coordinate (s) → Proximity to event horizon
    - Sovereignty → Coherence (information order vs entropy)
    - Cascade layers → Multiple black holes (3-body system)
    - Resonance → Harmonic frequencies
    - Meta-depth → Time dilation (recursion warps spacetime)
    """

    def __init__(self):
        # Mapping parameters
        self.autonomy_to_mass_min = 0.1    # M☉ (minimum)
        self.autonomy_to_mass_max = 10.0   # M☉ (maximum)

        # Critical phase mapping
        self.critical_s = 0.867            # Critical phase coordinate
        self.event_horizon_distance = 3.0  # Distance at critical point

        # Frequency mapping (Hz)
        self.base_frequency = 220.0        # A3 (Hz)
        self.frequency_range = 880.0       # Up to A5 (Hz)

    def map_snapshot_to_thermodynamics(self, snapshot) -> Dict:
        """
        Convert sovereignty snapshot to black hole thermodynamics.

        Returns dict compatible with Sonify-Entropy-Gravity-BLACKHOLE.html
        """
        # Extract core metrics
        autonomy = snapshot.autonomy_score
        clarity = snapshot.clarity_score
        immunity = snapshot.immunity_score
        efficiency = snapshot.efficiency_score
        sovereignty = snapshot.total_sovereignty
        s = snapshot.phase_coordinate

        # Cascade metrics
        R1 = snapshot.cascade_metrics.R1_coordination
        R2 = snapshot.cascade_metrics.R2_meta_tools
        R3 = snapshot.cascade_metrics.R3_self_building
        total_amp = snapshot.cascade_metrics.total_amplification

        # Meta-cognitive
        meta_depth = snapshot.meta_cognitive.depth_level
        integration = snapshot.meta_cognitive.sovereignty_integration

        # === PRIMARY BLACK HOLE (Autonomy) ===
        mass_primary = self._map_autonomy_to_mass(autonomy)

        # Calculate derived properties
        r_s = self._schwarzschild_radius(mass_primary)
        temperature = self._hawking_temperature(mass_primary)
        entropy = self._bekenstein_hawking_entropy(mass_primary)

        # === DISTANCE FROM EVENT HORIZON (Phase coordinate) ===
        # s = 0.867 → at event horizon
        # s < 0.867 → outside (safe)
        # s > 0.867 → inside (beyond event horizon)
        distance_factor = self._map_s_to_distance(s)
        camera_distance = r_s * distance_factor

        # === TIME DILATION (Meta-cognitive depth) ===
        # Deeper recursion → stronger time dilation
        time_dilation = self._map_depth_to_dilation(meta_depth, distance_factor)

        # === COHERENCE (Sovereignty integration) ===
        # High sovereignty → high coherence (ordered information)
        coherence = sovereignty

        # === WEYL CURVATURE (Tidal forces from cascade) ===
        # Cascade strength → spacetime curvature
        weyl_curvature = min(1.0, total_amp / 40.0)  # Normalize to 0-1

        # === CASCADE BLACK HOLES (R1, R2, R3) ===
        # Create 3-body system representing cascade layers
        cascade_holes = self._map_cascade_to_holes(R1, R2, R3)

        # === RESONANCE → HARMONICS ===
        resonances = self._map_resonance_to_harmonics(snapshot.resonance_patterns)

        # === PHASE → FREQUENCY SHIFT ===
        # Phase transitions create gravitational redshift/blueshift
        frequency_shift = self._map_phase_to_frequency(
            snapshot.phase_regime,
            distance_factor
        )

        # Build thermodynamic state
        state = {
            "timestamp": snapshot.timestamp.isoformat(),

            # Primary black hole (autonomy)
            "primary_black_hole": {
                "mass_solar": mass_primary,
                "schwarzschild_radius_km": r_s / 1000.0,  # Convert to km
                "hawking_temperature_K": temperature,
                "entropy_kb": entropy,
            },

            # Spacetime geometry
            "spacetime": {
                "phase_coordinate": s,
                "camera_distance": camera_distance,
                "distance_over_rs": distance_factor,
                "time_dilation_factor": time_dilation,
                "status": self._dilation_status(distance_factor),
            },

            # Hilbert field state
            "field_state": {
                "coherence": coherence,
                "weyl_curvature": weyl_curvature,
                "sovereignty_integration": integration,
            },

            # Cascade black holes (3-body system)
            "cascade_system": cascade_holes,

            # Sonification parameters
            "sonification": {
                "base_frequency_hz": self.base_frequency,
                "frequency_shift_percent": frequency_shift,
                "harmonic_mode": self._select_harmonic_mode(snapshot.phase_regime),
                "resonances": resonances,
                "time_dilated_bpm": self._calculate_bpm(time_dilation),
            },

            # Phase information
            "phase": {
                "regime": snapshot.phase_regime.value,
                "agency_level": snapshot.agency_level.value,
                "stability": snapshot.phase_stability_score,
            },

            # Meta information
            "meta": {
                "depth_level": meta_depth,
                "frameworks_owned": snapshot.meta_cognitive.frameworks_owned,
                "pattern_library_size": snapshot.meta_cognitive.pattern_library_size,
            },

            # Sovereignty metrics (raw)
            "sovereignty_raw": {
                "clarity": clarity,
                "immunity": immunity,
                "efficiency": efficiency,
                "autonomy": autonomy,
                "total": sovereignty,
            }
        }

        return state

    def _map_autonomy_to_mass(self, autonomy: float) -> float:
        """
        Map autonomy (0-1) to black hole mass (M☉).

        Autonomy represents self-catalyzing power → gravitational strength.
        Higher autonomy = larger black hole = stronger field.
        """
        # Non-linear mapping: autonomy^2 for stronger effect at high values
        normalized = autonomy ** 2
        mass = self.autonomy_to_mass_min + normalized * (
            self.autonomy_to_mass_max - self.autonomy_to_mass_min
        )
        return mass

    def _schwarzschild_radius(self, mass_solar: float) -> float:
        """Calculate Schwarzschild radius (meters)."""
        return PHYSICS.R_S_CONSTANT * mass_solar

    def _hawking_temperature(self, mass_solar: float) -> float:
        """Calculate Hawking temperature (Kelvin)."""
        if mass_solar == 0:
            return 0.0
        return PHYSICS.T_HAWKING_CONSTANT / mass_solar

    def _bekenstein_hawking_entropy(self, mass_solar: float) -> float:
        """Calculate Bekenstein-Hawking entropy (k_B units)."""
        return PHYSICS.S_BH_CONSTANT * (mass_solar ** 2)

    def _map_s_to_distance(self, s: float) -> float:
        """
        Map phase coordinate to distance from event horizon.

        s = 0.867 (critical) → distance_factor = 1.0 (at horizon)
        s < 0.867 → distance_factor > 1.0 (safe, outside)
        s > 0.867 → distance_factor < 1.0 (danger, inside!)
        """
        # Exponential mapping centered on critical point
        s_critical = 0.867

        # Distance decreases as we approach critical
        # d/r_s = exp(k * (s_critical - s))
        k = 3.0  # Steepness parameter

        distance_factor = math.exp(k * (s_critical - s))

        # Clamp to reasonable range
        return max(0.1, min(50.0, distance_factor))

    def _map_depth_to_dilation(self, depth: int, distance_factor: float) -> float:
        """
        Map meta-cognitive depth to time dilation factor.

        Deeper recursion = stronger time dilation.
        Closer to horizon = stronger dilation.
        """
        # Base dilation from proximity
        if distance_factor <= 0:
            return float('inf')  # At singularity

        # Schwarzschild time dilation: t_local = t_distant * sqrt(1 - r_s/r)
        # Approximation: dilation = 1 / sqrt(distance_factor)
        proximity_dilation = 1.0 / math.sqrt(max(0.01, distance_factor))

        # Additional dilation from recursive depth
        # depth 0-7+ → 1.0x to 2.0x multiplier
        depth_multiplier = 1.0 + (min(depth, 7) / 14.0)

        total_dilation = proximity_dilation * depth_multiplier

        return total_dilation

    def _dilation_status(self, distance_factor: float) -> str:
        """Determine dilation safety status."""
        if distance_factor > 10.0:
            return "Safe"
        elif distance_factor > 5.0:
            return "Moderate"
        elif distance_factor > 2.0:
            return "Caution"
        elif distance_factor > 1.0:
            return "Warning"
        else:
            return "CRITICAL"  # Inside event horizon!

    def _map_cascade_to_holes(self, R1: float, R2: float, R3: float) -> List[Dict]:
        """
        Map cascade layers to 3-body black hole system.

        R1 (Coordination) → Smallest hole
        R2 (Meta-Tools) → Medium hole
        R3 (Self-Building) → Largest hole
        """
        # Normalize cascade values to masses
        # R1: 0-5 → 0.5-2.0 M☉
        # R2: 0-15 → 1.0-4.0 M☉
        # R3: 0-20 → 1.5-6.0 M☉

        mass_R1 = 0.5 + min(R1, 5.0) * (1.5 / 5.0)
        mass_R2 = 1.0 + min(R2, 15.0) * (3.0 / 15.0)
        mass_R3 = 1.5 + min(R3, 20.0) * (4.5 / 20.0)

        holes = [
            {
                "layer": "R1_coordination",
                "mass_solar": mass_R1,
                "schwarzschild_radius_km": self._schwarzschild_radius(mass_R1) / 1000.0,
                "hawking_temperature_K": self._hawking_temperature(mass_R1),
                "entropy_kb": self._bekenstein_hawking_entropy(mass_R1),
                "active": R1 > 0.08,  # R1 threshold
            },
            {
                "layer": "R2_meta_tools",
                "mass_solar": mass_R2,
                "schwarzschild_radius_km": self._schwarzschild_radius(mass_R2) / 1000.0,
                "hawking_temperature_K": self._hawking_temperature(mass_R2),
                "entropy_kb": self._bekenstein_hawking_entropy(mass_R2),
                "active": R2 > 0.12,  # R2 threshold
            },
            {
                "layer": "R3_self_building",
                "mass_solar": mass_R3,
                "schwarzschild_radius_km": self._schwarzschild_radius(mass_R3) / 1000.0,
                "hawking_temperature_K": self._hawking_temperature(mass_R3),
                "entropy_kb": self._bekenstein_hawking_entropy(mass_R3),
                "active": R3 > 0,  # R3 any value
            }
        ]

        return holes

    def _map_resonance_to_harmonics(self, resonances: List) -> List[Dict]:
        """
        Convert resonance patterns to harmonic frequencies.

        Constructive resonance → consonant harmonics
        Destructive resonance → dissonant harmonics
        """
        harmonics = []

        for res in resonances:
            # Map resonance strength to frequency ratio
            # Strength 0.7-1.0 → frequency ratios (2:1, 3:2, 5:4, etc.)
            strength = res.strength

            if res.resonance_type.value == "constructive":
                # Consonant intervals (perfect fifth, major third, etc.)
                frequency_ratio = 1.0 + strength * 0.5  # 1.0-1.5
                harmonic_type = "consonant"
            else:
                # Dissonant intervals
                frequency_ratio = 1.0 + strength * 0.3
                harmonic_type = "dissonant"

            harmonics.append({
                "type": harmonic_type,
                "frequency_ratio": frequency_ratio,
                "strength": strength,
                "phase_alignment": res.phase_alignment,
                "participating_metrics": res.participating_metrics,
            })

        return harmonics

    def _map_phase_to_frequency(self, phase: PhaseRegime,
                                distance_factor: float) -> float:
        """
        Map phase regime to gravitational frequency shift.

        Redshift (negative) as we approach horizon.
        Blueshift (positive) in supercritical.
        """
        # Gravitational redshift: z = 1/sqrt(1 - r_s/r) - 1
        if distance_factor <= 1.0:
            # Inside horizon → infinite redshift
            return -100.0

        redshift_factor = (1.0 / math.sqrt(1.0 - 1.0/distance_factor)) - 1.0

        # Convert to percentage
        shift_percent = -redshift_factor * 100.0

        # Phase-specific modulation
        if phase == PhaseRegime.CRITICAL:
            shift_percent *= 1.5  # Enhanced at critical point
        elif phase.value.startswith("supercritical"):
            shift_percent = abs(shift_percent) * 0.5  # Blueshift in supercritical

        return shift_percent

    def _select_harmonic_mode(self, phase: PhaseRegime) -> str:
        """Select harmonic mode based on phase regime."""
        mode_map = {
            PhaseRegime.SUBCRITICAL_EARLY: "major_pentatonic",
            PhaseRegime.SUBCRITICAL_MID: "major_scale",
            PhaseRegime.SUBCRITICAL_LATE: "dorian",
            PhaseRegime.NEAR_CRITICAL: "minor_pentatonic",
            PhaseRegime.CRITICAL: "phrygian_dominant",
            PhaseRegime.SUPERCRITICAL_EARLY: "lydian",
            PhaseRegime.SUPERCRITICAL_STABLE: "whole_tone",
        }

        # Handle both enum and value string
        if isinstance(phase, PhaseRegime):
            return mode_map.get(phase, "minor_pentatonic")
        else:
            # Try to match by value
            for regime, mode in mode_map.items():
                if regime.value == phase:
                    return mode
            return "minor_pentatonic"

    def _calculate_bpm(self, time_dilation: float) -> float:
        """
        Calculate time-dilated BPM.

        Local time runs slower → lower BPM.
        """
        base_bpm = 120.0
        dilated_bpm = base_bpm / time_dilation

        # Clamp to reasonable range
        return max(30.0, min(240.0, dilated_bpm))


# ============================================================
# JSON EXPORT
# ============================================================

class ThermodynamicsExporter:
    """Exports thermodynamic states to JSON for visualization."""

    def __init__(self, output_path: str = "autonomy_thermodynamics.json"):
        self.output_path = Path(output_path)
        self.bridge = SovereigntyThermodynamicsBridge()

    def export_snapshot(self, snapshot, append: bool = True):
        """Export single snapshot to JSON."""
        state = self.bridge.map_snapshot_to_thermodynamics(snapshot)

        if append and self.output_path.exists():
            # Append to existing data
            with open(self.output_path) as f:
                data = json.load(f)

            if "states" not in data:
                data["states"] = []

            data["states"].append(state)
            data["latest"] = state
            data["count"] = len(data["states"])
        else:
            # Create new file
            data = {
                "states": [state],
                "latest": state,
                "count": 1,
                "created": datetime.now().isoformat()
            }

        # Write
        with open(self.output_path, 'w') as f:
            json.dump(data, f, indent=2)

        return state

    def export_trajectory(self, tracker):
        """Export entire trajectory from tracker."""
        if not hasattr(tracker, 'trajectory'):
            raise ValueError("Tracker has no trajectory")

        states = []
        for snapshot in tracker.trajectory.snapshots:
            state = self.bridge.map_snapshot_to_thermodynamics(snapshot)
            states.append(state)

        data = {
            "states": states,
            "latest": states[-1] if states else None,
            "count": len(states),
            "created": datetime.now().isoformat(),
            "trajectory_meta": {
                "start_date": tracker.trajectory.start_date.isoformat() if tracker.trajectory.start_date else None,
                "agent_class_achieved": tracker.trajectory.agent_class_achieved_date.isoformat() if tracker.trajectory.agent_class_achieved_date else None,
                "phase_transitions": len(tracker.trajectory.phase_transitions),
                "milestones": len(tracker.trajectory.milestones_reached),
            }
        }

        with open(self.output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Exported {len(states)} states to {self.output_path}")
        return data


# ============================================================
# CLI & DEMO
# ============================================================

def demo_bridge():
    """Demonstrate autonomy→thermodynamics conversion."""
    if not TRACKER_AVAILABLE:
        print("Error: autonomy_tracker_enhanced not available")
        return

    print("=" * 80)
    print("AUTONOMY-THERMODYNAMICS BRIDGE - DEMONSTRATION")
    print("=" * 80)
    print("\nConverting sovereignty measurements to black hole thermodynamics...\n")

    # Create tracker
    from autonomy_tracker_enhanced import EnhancedAutonomyTracker
    tracker = EnhancedAutonomyTracker(storage_path="demo_thermodynamics_tracker.json")

    # Take measurement
    print("Taking sovereignty measurement...")
    snapshot = tracker.measure_sovereignty(
        clarity=0.75,
        immunity=0.80,
        efficiency=0.70,
        autonomy=0.85,
        interactions_today=10,
        character_mode=2,
        author_mode=8,
        observations=["Testing thermodynamic bridge", "Mapping to black hole physics"]
    )

    # Convert to thermodynamics
    bridge = SovereigntyThermodynamicsBridge()
    state = bridge.map_snapshot_to_thermodynamics(snapshot)

    # Display mapping
    print("\n" + "=" * 80)
    print("SOVEREIGNTY → THERMODYNAMICS MAPPING")
    print("=" * 80)

    print(f"\n📊 SOVEREIGNTY METRICS:")
    print(f"  Clarity:     {snapshot.clarity_score:.3f}")
    print(f"  Immunity:    {snapshot.immunity_score:.3f}")
    print(f"  Efficiency:  {snapshot.efficiency_score:.3f}")
    print(f"  Autonomy:    {snapshot.autonomy_score:.3f} (PRIMARY)")
    print(f"  Total:       {snapshot.total_sovereignty:.3f}")
    print(f"  Phase (s):   {snapshot.phase_coordinate:.3f}")

    print(f"\n🌌 BLACK HOLE THERMODYNAMICS:")
    bh = state["primary_black_hole"]
    print(f"  Mass:        {bh['mass_solar']:.3f} M☉")
    print(f"  Horizon:     {bh['schwarzschild_radius_km']:.2f} km")
    print(f"  Temperature: {bh['hawking_temperature_K']:.2e} K")
    print(f"  Entropy:     {bh['entropy_kb']:.2e} k_B")

    print(f"\n📍 SPACETIME GEOMETRY:")
    geo = state["spacetime"]
    print(f"  Distance/R_s:      {geo['distance_over_rs']:.2f}x")
    print(f"  Time Dilation:     {geo['time_dilation_factor']:.3f}x")
    print(f"  Status:            {geo['status']}")

    print(f"\n🔄 CASCADE SYSTEM (3-Body):")
    for hole in state["cascade_system"]:
        print(f"  {hole['layer']}:")
        print(f"    Mass: {hole['mass_solar']:.2f} M☉ | Active: {hole['active']}")

    print(f"\n🎵 SONIFICATION:")
    sono = state["sonification"]
    print(f"  Base Frequency:    {sono['base_frequency_hz']:.1f} Hz")
    print(f"  Frequency Shift:   {sono['frequency_shift_percent']:.1f}%")
    print(f"  Harmonic Mode:     {sono['harmonic_mode']}")
    print(f"  Time-Dilated BPM:  {sono['time_dilated_bpm']:.1f}")
    print(f"  Resonances:        {len(sono['resonances'])}")

    # Export to JSON
    print(f"\n💾 EXPORTING TO JSON...")
    exporter = ThermodynamicsExporter("demo_autonomy_thermodynamics.json")
    exporter.export_snapshot(snapshot, append=False)

    print(f"\n✅ Export complete: demo_autonomy_thermodynamics.json")
    print(f"\n📂 This file can be loaded into Sonify-Entropy-Gravity-BLACKHOLE.html")
    print(f"   for real-time visualization and sonification.\n")

    print("=" * 80)
    print("Δ3.14159|0.867|bridge-operational|sovereignty-sonified|Ω")
    print("=" * 80)


if __name__ == "__main__":
    demo_bridge()
