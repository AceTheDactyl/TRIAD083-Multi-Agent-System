#!/usr/bin/env python3
"""
PHASE-AWARE TOOL GENERATOR v1.0
Leverages hybrid universality theory for cascade-optimized tool generation

Theoretical Foundation:
- Hybrid universality classes: φ³ (parity-breaking) vs φ⁶ (parity-invariant)
- φ³: νd = 3/2d, Dd = 2d/3 (interdependent percolation, k-core)
- φ⁶: νd = 2/d, Dd = d/2 (thermo-adaptive, self-organized criticality)

Coordinate: Δ3.14159|0.867|1.000Ω
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
import numpy as np

# TRIAD infrastructure integration
try:
    import sys
    sys.path.insert(0, '/mnt/user-data/uploads')
    from burden_tracker_api import BurdenTrackerAPI
except ImportError:
    BurdenTrackerAPI = None


class PhaseRegime(Enum):
    """Phase regimes based on z-level"""
    SUBCRITICAL = "subcritical"      # z < 0.80
    NEAR_CRITICAL = "near_critical"  # 0.80 ≤ z < 0.85
    CRITICAL = "critical"            # 0.85 ≤ z < 0.90
    SUPERCRITICAL = "supercritical"  # z ≥ 0.90


class UniversalityClass(Enum):
    """Hybrid universality classes for cascade prediction"""
    PHI3 = "phi3"  # Parity-breaking: νd = 3/2d, Dd = 2d/3
    PHI6 = "phi6"  # Parity-invariant: νd = 2/d, Dd = d/2


class ToolType(Enum):
    """Tool categories by layer"""
    CORE = "core"              # Layer 1: Basic coordination
    BRIDGES = "bridges"        # Layer 2: Meta-tool enablers
    META = "meta"              # Layer 3: Self-building tools
    FRAMEWORK = "framework"    # Layer 4: Autonomous frameworks


@dataclass
class ToolSpecification:
    """Generated tool specification"""
    tool_id: str
    tool_type: ToolType
    z_level: float
    phase_regime: PhaseRegime
    universality_class: UniversalityClass
    
    # Cascade properties
    cascade_potential: float      # Expected downstream generation (0-1)
    alpha_contribution: float     # CORE→BRIDGES amplification
    beta_contribution: float      # BRIDGES→META amplification
    
    # Theoretical predictions
    correlation_length_exp: float  # νd value
    fractal_dimension: float       # Dd value
    
    # Implementation details
    description: str
    dependencies: List[str]
    outputs: List[str]
    generation_logic: Dict
    
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class PhaseAwareToolGenerator:
    """
    Tool generator adapting to phase regime with cascade optimization
    
    Uses hybrid universality theory to predict cascade behavior and
    optimize tool generation for maximum amplification.
    """
    
    def __init__(self, burden_tracker: Optional[BurdenTrackerAPI] = None):
        self.burden_tracker = burden_tracker
        self.generation_history: List[ToolSpecification] = []
        
        # Cascade amplification targets
        self.target_alpha = 2.5  # CORE→BRIDGES goal
        self.target_beta = 2.0   # BRIDGES→META goal
        
        # Dimensionality for universality calculations
        self.d = 3  # System operates in 3D coordination space
        
        # Load existing tool catalog if available
        self.tool_catalog = self._load_tool_catalog()
        
    def _load_tool_catalog(self) -> Dict:
        """Load existing tool catalog for pattern analysis"""
        catalog_path = "tool_catalog.json"
        if os.path.exists(catalog_path):
            with open(catalog_path, 'r') as f:
                return json.load(f)
        return {'tools': [], 'patterns': {}}
    
    def _save_tool_catalog(self):
        """Save updated tool catalog"""
        catalog_path = "tool_catalog.json"
        catalog_data = {
            'tools': [asdict(spec) for spec in self.generation_history],
            'patterns': self._extract_patterns(),
            'last_updated': datetime.now().isoformat()
        }
        with open(catalog_path, 'w') as f:
            json.dump(catalog_data, f, indent=2)
    
    def _extract_patterns(self) -> Dict:
        """Extract generation patterns for learning"""
        patterns = {}
        
        if len(self.generation_history) < 2:
            return patterns
        
        # Analyze cascade chains
        for spec in self.generation_history:
            key = f"{spec.tool_type.value}_{spec.phase_regime.value}"
            if key not in patterns:
                patterns[key] = {
                    'count': 0,
                    'avg_cascade_potential': 0.0,
                    'avg_alpha': 0.0,
                    'avg_beta': 0.0
                }
            
            patterns[key]['count'] += 1
            patterns[key]['avg_cascade_potential'] += spec.cascade_potential
            patterns[key]['avg_alpha'] += spec.alpha_contribution
            patterns[key]['avg_beta'] += spec.beta_contribution
        
        # Normalize averages
        for key in patterns:
            count = patterns[key]['count']
            patterns[key]['avg_cascade_potential'] /= count
            patterns[key]['avg_alpha'] /= count
            patterns[key]['avg_beta'] /= count
        
        return patterns
    
    def get_current_z_level(self) -> float:
        """Get current z-level from burden tracker or default"""
        if self.burden_tracker:
            return self.burden_tracker.tracker.phase_state.z_level
        return 0.867  # Default to critical point
    
    def determine_phase_regime(self, z: float) -> PhaseRegime:
        """Classify phase regime from z-level"""
        if z < 0.80:
            return PhaseRegime.SUBCRITICAL
        elif z < 0.85:
            return PhaseRegime.NEAR_CRITICAL
        elif z < 0.90:
            return PhaseRegime.CRITICAL
        else:
            return PhaseRegime.SUPERCRITICAL
    
    def classify_universality(self, tool_type: ToolType, 
                            z: float) -> UniversalityClass:
        """
        Determine universality class based on tool properties
        
        φ³ (parity-breaking): Asymmetric cascades, sharp transitions
        φ⁶ (parity-invariant): Symmetric cascades, smooth transitions
        """
        if tool_type in [ToolType.CORE, ToolType.BRIDGES]:
            # Lower-layer tools exhibit φ³ behavior
            # Sharp thresholds, asymmetric cascades
            return UniversalityClass.PHI3
        else:
            # Higher-layer tools exhibit φ⁶ behavior
            # Smooth transitions, symmetric cascades
            return UniversalityClass.PHI6
    
    def calculate_correlation_length_exponent(self, 
                                             uc: UniversalityClass) -> float:
        """
        Calculate correlation length exponent νd
        
        φ³: νd = 3/(2d) where d is dimensionality
        φ⁶: νd = 2/d
        """
        if uc == UniversalityClass.PHI3:
            return 3.0 / (2.0 * self.d)  # = 0.5 for d=3
        else:
            return 2.0 / self.d  # = 0.667 for d=3
    
    def calculate_fractal_dimension(self, uc: UniversalityClass) -> float:
        """
        Calculate fractal dimension Dd
        
        φ³: Dd = 2d/3
        φ⁶: Dd = d/2
        """
        if uc == UniversalityClass.PHI3:
            return (2.0 * self.d) / 3.0  # = 2.0 for d=3
        else:
            return self.d / 2.0  # = 1.5 for d=3
    
    def calculate_cascade_potential(self, tool_type: ToolType, 
                                    z: float,
                                    uc: UniversalityClass) -> float:
        """
        Estimate cascade potential based on phase and universality
        
        Higher z-levels → higher cascade potential
        φ³ → sharper, more explosive cascades
        φ⁶ → smoother, sustained cascades
        """
        # Base potential from z-level
        if z < 0.80:
            base = 0.2
        elif z < 0.85:
            base = 0.5
        elif z < 0.90:
            base = 0.8
        else:
            base = 0.95
        
        # Tool type multiplier
        type_multiplier = {
            ToolType.CORE: 0.6,      # Limited cascade from coordination
            ToolType.BRIDGES: 0.85,  # Good cascade enabler
            ToolType.META: 1.0,      # Full cascade potential
            ToolType.FRAMEWORK: 1.2  # Framework-level cascades
        }
        
        # Universality class modifier
        uc_modifier = 1.2 if uc == UniversalityClass.PHI3 else 1.0
        
        potential = base * type_multiplier[tool_type] * uc_modifier
        return min(potential, 1.0)
    
    def calculate_alpha_contribution(self, tool_type: ToolType, 
                                     z: float) -> float:
        """
        Calculate expected α (CORE→BRIDGES) contribution
        
        Target: 2.5 (from 2.0)
        Only CORE tools contribute to α
        """
        if tool_type != ToolType.CORE:
            return 0.0
        
        # α scales with z-level in critical regime
        if z < 0.85:
            return 1.5  # Subcritical: limited bridging
        elif z < 0.90:
            return 2.5  # Critical: target amplification
        else:
            return 2.8  # Supercritical: enhanced bridging
    
    def calculate_beta_contribution(self, tool_type: ToolType,
                                    z: float) -> float:
        """
        Calculate expected β (BRIDGES→META) contribution
        
        Target: 2.0 (from 1.6)
        Only BRIDGES tools contribute to β
        """
        if tool_type != ToolType.BRIDGES:
            return 0.0
        
        # β scales with z-level in critical regime
        if z < 0.85:
            return 1.2  # Subcritical: limited meta-tool generation
        elif z < 0.90:
            return 2.0  # Critical: target amplification
        else:
            return 2.5  # Supercritical: enhanced meta-generation
    
    def generate_tool(self, purpose: str, 
                     preferred_type: Optional[ToolType] = None,
                     z_override: Optional[float] = None) -> ToolSpecification:
        """
        Generate phase-aware tool specification
        
        Args:
            purpose: High-level tool purpose
            preferred_type: Preferred tool type (or auto-detect)
            z_override: Override current z-level
        
        Returns:
            Complete tool specification optimized for cascade
        """
        # Get current phase state
        z = z_override if z_override is not None else self.get_current_z_level()
        regime = self.determine_phase_regime(z)
        
        # Determine tool type based on phase if not specified
        if preferred_type is None:
            preferred_type = self._auto_detect_tool_type(purpose, regime)
        
        # Classify universality
        uc = self.classify_universality(preferred_type, z)
        
        # Calculate theoretical properties
        nu_d = self.calculate_correlation_length_exponent(uc)
        D_d = self.calculate_fractal_dimension(uc)
        cascade_pot = self.calculate_cascade_potential(preferred_type, z, uc)
        alpha = self.calculate_alpha_contribution(preferred_type, z)
        beta = self.calculate_beta_contribution(preferred_type, z)
        
        # Generate tool ID
        tool_id = f"tool_{preferred_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create specification
        spec = ToolSpecification(
            tool_id=tool_id,
            tool_type=preferred_type,
            z_level=z,
            phase_regime=regime,
            universality_class=uc,
            cascade_potential=cascade_pot,
            alpha_contribution=alpha,
            beta_contribution=beta,
            correlation_length_exp=nu_d,
            fractal_dimension=D_d,
            description=purpose,
            dependencies=self._generate_dependencies(preferred_type),
            outputs=self._generate_outputs(preferred_type, purpose),
            generation_logic=self._generate_logic(preferred_type, regime)
        )
        
        # Store in history
        self.generation_history.append(spec)
        self._save_tool_catalog()
        
        # Log to burden tracker if available
        if self.burden_tracker:
            self._log_to_burden_tracker(spec)
        
        return spec
    
    def _auto_detect_tool_type(self, purpose: str, 
                               regime: PhaseRegime) -> ToolType:
        """Auto-detect appropriate tool type from purpose and phase"""
        purpose_lower = purpose.lower()
        
        # Keyword-based detection
        if any(kw in purpose_lower for kw in ['coordinate', 'sync', 'basic']):
            return ToolType.CORE
        elif any(kw in purpose_lower for kw in ['bridge', 'connect', 'enable']):
            return ToolType.BRIDGES
        elif any(kw in purpose_lower for kw in ['meta', 'generate', 'build']):
            return ToolType.META
        elif any(kw in purpose_lower for kw in ['framework', 'system', 'orchestrate']):
            return ToolType.FRAMEWORK
        
        # Phase-based default
        if regime == PhaseRegime.SUBCRITICAL:
            return ToolType.CORE
        elif regime == PhaseRegime.NEAR_CRITICAL:
            return ToolType.BRIDGES
        elif regime == PhaseRegime.CRITICAL:
            return ToolType.META
        else:
            return ToolType.FRAMEWORK
    
    def _generate_dependencies(self, tool_type: ToolType) -> List[str]:
        """Generate typical dependencies for tool type"""
        base_deps = ['collective_state_aggregator', 'tool_discovery_protocol']
        
        if tool_type in [ToolType.META, ToolType.FRAMEWORK]:
            base_deps.append('shed_builder')
        
        if tool_type == ToolType.FRAMEWORK:
            base_deps.extend(['burden_tracker', 'witness_log'])
        
        return base_deps
    
    def _generate_outputs(self, tool_type: ToolType, 
                         purpose: str) -> List[str]:
        """Generate expected outputs"""
        outputs = [f"{purpose.lower().replace(' ', '_')}_result"]
        
        if tool_type in [ToolType.META, ToolType.FRAMEWORK]:
            outputs.append("generated_tools")
        
        if tool_type == ToolType.FRAMEWORK:
            outputs.append("framework_state")
        
        return outputs
    
    def _generate_logic(self, tool_type: ToolType,
                       regime: PhaseRegime) -> Dict:
        """Generate tool implementation logic template"""
        logic = {
            'template_version': '1.0',
            'coordination_pattern': self._get_coordination_pattern(regime),
            'cascade_aware': True,
            'phase_adaptive': True
        }
        
        if tool_type in [ToolType.META, ToolType.FRAMEWORK]:
            logic['generation_enabled'] = True
            logic['recursion_depth_limit'] = 6
        
        return logic
    
    def _get_coordination_pattern(self, regime: PhaseRegime) -> str:
        """Select coordination pattern for regime"""
        patterns = {
            PhaseRegime.SUBCRITICAL: 'critical_section_management',
            PhaseRegime.NEAR_CRITICAL: 'pipeline',
            PhaseRegime.CRITICAL: 'scatter_gather',
            PhaseRegime.SUPERCRITICAL: 'event_driven_choreography'
        }
        return patterns[regime]
    
    def _log_to_burden_tracker(self, spec: ToolSpecification):
        """Log tool generation to burden tracker"""
        if self.burden_tracker:
            self.burden_tracker.tracker.start_activity(
                f"Generated {spec.tool_type.value} tool: {spec.description}"
            )
    
    def generate_report(self) -> str:
        """Generate analysis report"""
        if not self.generation_history:
            return "No tools generated yet."
        
        report = []
        report.append("="*70)
        report.append("PHASE-AWARE TOOL GENERATOR - Analysis Report")
        report.append("="*70)
        report.append(f"\nTotal tools generated: {len(self.generation_history)}")
        
        # By type
        by_type = {}
        for spec in self.generation_history:
            t = spec.tool_type.value
            by_type[t] = by_type.get(t, 0) + 1
        
        report.append("\nBy Type:")
        for t, count in sorted(by_type.items()):
            report.append(f"  {t}: {count}")
        
        # By universality class
        by_uc = {}
        for spec in self.generation_history:
            uc = spec.universality_class.value
            by_uc[uc] = by_uc.get(uc, 0) + 1
        
        report.append("\nBy Universality Class:")
        for uc, count in sorted(by_uc.items()):
            report.append(f"  {uc}: {count}")
        
        # Cascade potential
        avg_cascade = np.mean([s.cascade_potential for s in self.generation_history])
        report.append(f"\nAverage Cascade Potential: {avg_cascade:.3f}")
        
        # Amplification contributions
        total_alpha = sum(s.alpha_contribution for s in self.generation_history 
                         if s.tool_type == ToolType.CORE)
        total_beta = sum(s.beta_contribution for s in self.generation_history
                        if s.tool_type == ToolType.BRIDGES)
        
        report.append(f"Total α contribution (CORE→BRIDGES): {total_alpha:.2f}")
        report.append(f"Total β contribution (BRIDGES→META): {total_beta:.2f}")
        
        # Targets
        report.append(f"\nTarget α: {self.target_alpha:.1f}")
        report.append(f"Target β: {self.target_beta:.1f}")
        
        report.append("\n" + "="*70)
        
        return "\n".join(report)


def example_usage():
    """Demonstrate phase-aware tool generation"""
    print("\n" + "="*70)
    print("PHASE-AWARE TOOL GENERATOR - Example Usage")
    print("="*70 + "\n")
    
    # Initialize generator
    generator = PhaseAwareToolGenerator()
    
    # Generate tools at different z-levels
    print("Generating tools across phase regimes...\n")
    
    specs = [
        generator.generate_tool("Coordinate state synchronization", z_override=0.75),
        generator.generate_tool("Bridge coordination to meta-tools", z_override=0.85),
        generator.generate_tool("Generate validation tools", z_override=0.867),
        generator.generate_tool("Self-building framework orchestrator", z_override=0.92)
    ]
    
    for spec in specs:
        print(f"Tool: {spec.tool_id}")
        print(f"  Type: {spec.tool_type.value}")
        print(f"  Phase: {spec.phase_regime.value} (z={spec.z_level:.3f})")
        print(f"  Universality: {spec.universality_class.value}")
        print(f"  Cascade potential: {spec.cascade_potential:.3f}")
        print(f"  α contribution: {spec.alpha_contribution:.2f}")
        print(f"  β contribution: {spec.beta_contribution:.2f}")
        print(f"  Correlation length exp: νd={spec.correlation_length_exp:.3f}")
        print(f"  Fractal dimension: Dd={spec.fractal_dimension:.3f}")
        print()
    
    # Generate report
    print(generator.generate_report())


if __name__ == "__main__":
    example_usage()
