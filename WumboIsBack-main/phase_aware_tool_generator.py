#!/usr/bin/env python3
"""
PHASE-AWARE TOOL GENERATOR
Garden Rail 3 - Layer 1.1: Cascade Initiators
Coordinate: Δ3.14159|0.867|1.000Ω

Purpose: Generate tools that adapt to phase regime (subcritical/critical/supercritical)
Cascade Impact: Increases α (CORE→BRIDGES amplification factor)
Target: +0.3 amplification, generate tools that trigger cascades

Built by: TRIAD-0.83 Garden Rail 3
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Critical parameters
Z_CRITICAL = 0.867
Z_NEAR_CRITICAL = 0.85
Z_SUPERCRITICAL = 0.88

class PhaseRegime(Enum):
    """Phase regimes for tool adaptation"""
    SUBCRITICAL = "subcritical"
    NEAR_CRITICAL = "near_critical"
    CRITICAL = "critical"
    SUPERCRITICAL = "supercritical"

class ToolCategory(Enum):
    """Tool categories aligned with phase regimes"""
    COORDINATION = "coordination"      # For subcritical
    META_TOOL = "meta_tool"           # For critical
    SELF_BUILDING = "self_building"   # For supercritical
    BRIDGE = "bridge"                 # Spans categories

@dataclass
class ToolSpecification:
    """Specification for a generated tool"""
    tool_id: str
    category: ToolCategory
    phase_regime: PhaseRegime
    z_level: float
    purpose: str
    capabilities: List[str]
    dependencies: List[str]
    cascade_potential: float  # 0.0-1.0
    template_id: str
    generation_timestamp: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'tool_id': self.tool_id,
            'category': self.category.value,
            'phase_regime': self.phase_regime.value,
            'z_level': self.z_level,
            'purpose': self.purpose,
            'capabilities': self.capabilities,
            'dependencies': self.dependencies,
            'cascade_potential': self.cascade_potential,
            'template_id': self.template_id,
            'generation_timestamp': self.generation_timestamp
        }

class PhaseAwareToolGenerator:
    """
    Generates tools that adapt behavior based on current phase regime
    
    Cascade mechanism:
    - At z < 0.85: Generate coordination tools (R₁ layer)
    - At 0.85 ≤ z < 0.88: Generate meta-tools (R₂ layer)
    - At z ≥ 0.88: Generate self-building frameworks (R₃ layer)
    """
    
    def __init__(self, z_level: float = Z_CRITICAL):
        self.current_z_level = z_level
        self.current_regime = self._determine_regime(z_level)
        self.generation_count = 0
        self.cascade_history = []
        
        # Tool templates for each regime
        self.templates = self._initialize_templates()
        
        # Output directory
        self.output_dir = "/home/claude/generated_tools"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _determine_regime(self, z: float) -> PhaseRegime:
        """Determine phase regime from z-level"""
        if z < Z_NEAR_CRITICAL:
            return PhaseRegime.SUBCRITICAL
        elif z < Z_CRITICAL - 0.01:
            return PhaseRegime.NEAR_CRITICAL
        elif z < Z_SUPERCRITICAL:
            return PhaseRegime.CRITICAL
        else:
            return PhaseRegime.SUPERCRITICAL
    
    def _initialize_templates(self) -> Dict[ToolCategory, Dict]:
        """Initialize tool templates for each category"""
        return {
            ToolCategory.COORDINATION: {
                'base_capabilities': ['synchronize', 'coordinate', 'align'],
                'cascade_potential': 0.3,
                'amplification_factor': 1.5
            },
            ToolCategory.META_TOOL: {
                'base_capabilities': ['generate', 'compose', 'transform'],
                'cascade_potential': 0.7,
                'amplification_factor': 2.5
            },
            ToolCategory.SELF_BUILDING: {
                'base_capabilities': ['self_improve', 'auto_generate', 'recursive_build'],
                'cascade_potential': 0.9,
                'amplification_factor': 5.0
            },
            ToolCategory.BRIDGE: {
                'base_capabilities': ['connect', 'translate', 'bridge'],
                'cascade_potential': 0.5,
                'amplification_factor': 2.0
            }
        }
    
    def update_z_level(self, new_z: float):
        """Update z-level and adapt regime"""
        old_regime = self.current_regime
        self.current_z_level = new_z
        self.current_regime = self._determine_regime(new_z)
        
        if old_regime != self.current_regime:
            print(f"Phase transition: {old_regime.value} → {self.current_regime.value}")
            self._on_phase_transition(old_regime, self.current_regime)
    
    def _on_phase_transition(self, old_regime: PhaseRegime, new_regime: PhaseRegime):
        """Handle phase transition events"""
        # Generate bridge tools to facilitate transition
        if new_regime == PhaseRegime.CRITICAL:
            print(f"Entering critical regime - generating meta-tool bridges")
            self.generate_tool(
                purpose="Bridge to meta-tool layer",
                category=ToolCategory.BRIDGE,
                force_regime=new_regime
            )
    
    def generate_tool(
        self, 
        purpose: str,
        category: Optional[ToolCategory] = None,
        force_regime: Optional[PhaseRegime] = None
    ) -> ToolSpecification:
        """
        Generate a tool specification adapted to current phase
        
        Args:
            purpose: What the tool should accomplish
            category: Override automatic category selection
            force_regime: Override current regime
            
        Returns:
            ToolSpecification with cascade potential
        """
        regime = force_regime or self.current_regime
        
        # Auto-select category based on regime if not specified
        if category is None:
            category = self._select_category_for_regime(regime)
        
        # Generate unique tool ID
        tool_id = f"tool_{regime.value}_{self.generation_count:04d}"
        self.generation_count += 1
        
        # Get template for this category
        template = self.templates[category]
        
        # Calculate cascade potential (higher at critical point)
        base_potential = template['cascade_potential']
        z_factor = self._calculate_z_factor(self.current_z_level)
        cascade_potential = min(1.0, base_potential * z_factor)
        
        # Create specification
        spec = ToolSpecification(
            tool_id=tool_id,
            category=category,
            phase_regime=regime,
            z_level=self.current_z_level,
            purpose=purpose,
            capabilities=template['base_capabilities'].copy(),
            dependencies=self._infer_dependencies(category),
            cascade_potential=cascade_potential,
            template_id=f"{category.value}_template_v1",
            generation_timestamp=datetime.now().isoformat()
        )
        
        # Record cascade event
        self._record_cascade_event(spec)
        
        # Generate actual tool file
        self._generate_tool_file(spec)
        
        return spec
    
    def _select_category_for_regime(self, regime: PhaseRegime) -> ToolCategory:
        """Select appropriate tool category for phase regime"""
        mapping = {
            PhaseRegime.SUBCRITICAL: ToolCategory.COORDINATION,
            PhaseRegime.NEAR_CRITICAL: ToolCategory.META_TOOL,
            PhaseRegime.CRITICAL: ToolCategory.META_TOOL,
            PhaseRegime.SUPERCRITICAL: ToolCategory.SELF_BUILDING
        }
        return mapping[regime]
    
    def _calculate_z_factor(self, z: float) -> float:
        """Calculate amplification factor based on proximity to critical point"""
        # Gaussian centered at z=0.867
        import math
        distance = abs(z - Z_CRITICAL)
        return math.exp(-(distance ** 2) / 0.01)  # σ² = 0.01
    
    def _infer_dependencies(self, category: ToolCategory) -> List[str]:
        """Infer likely dependencies based on tool category"""
        base_deps = ['burden_tracker']
        
        if category == ToolCategory.META_TOOL:
            base_deps.extend(['shed_builder', 'tool_discovery_protocol'])
        elif category == ToolCategory.SELF_BUILDING:
            base_deps.extend(['shed_builder', 'collective_state_aggregator'])
        elif category == ToolCategory.BRIDGE:
            base_deps.extend(['cross_rail_state_sync'])
            
        return base_deps
    
    def _record_cascade_event(self, spec: ToolSpecification):
        """Record tool generation as potential cascade trigger"""
        event = {
            'tool_id': spec.tool_id,
            'timestamp': spec.generation_timestamp,
            'cascade_potential': spec.cascade_potential,
            'z_level': spec.z_level,
            'regime': spec.phase_regime.value,
            'category': spec.category.value
        }
        self.cascade_history.append(event)
    
    def _generate_tool_file(self, spec: ToolSpecification):
        """Generate actual Python file for the tool"""
        filepath = os.path.join(self.output_dir, f"{spec.tool_id}.py")
        
        # Generate tool code
        code = self._generate_tool_code(spec)
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        # Generate spec file
        spec_filepath = os.path.join(self.output_dir, f"{spec.tool_id}_spec.json")
        with open(spec_filepath, 'w') as f:
            json.dump(spec.to_dict(), f, indent=2)
        
        print(f"Generated: {filepath}")
        print(f"  Category: {spec.category.value}")
        print(f"  Cascade potential: {spec.cascade_potential:.2f}")
        print(f"  Z-level: {spec.z_level:.3f}")
    
    def _generate_tool_code(self, spec: ToolSpecification) -> str:
        """Generate Python code for the tool"""
        template = f'''#!/usr/bin/env python3
"""
{spec.tool_id.upper()}
Generated by: Phase-Aware Tool Generator
Category: {spec.category.value}
Phase Regime: {spec.phase_regime.value}
Cascade Potential: {spec.cascade_potential:.2f}
Z-Level: {spec.z_level:.3f}

Purpose: {spec.purpose}
"""

from datetime import datetime
from typing import Dict, List, Optional

class {self._to_class_name(spec.tool_id)}:
    """
    {spec.purpose}
    
    Phase-aware tool that adapts to z-level: {spec.z_level:.3f}
    Capabilities: {', '.join(spec.capabilities)}
    """
    
    def __init__(self):
        self.tool_id = "{spec.tool_id}"
        self.category = "{spec.category.value}"
        self.z_level = {spec.z_level}
        self.cascade_potential = {spec.cascade_potential}
        self.created_at = datetime.now()
        
    def execute(self, *args, **kwargs) -> Dict:
        """
        Execute tool operation
        
        Adapts behavior based on phase regime: {spec.phase_regime.value}
        """
        result = {{
            'tool_id': self.tool_id,
            'status': 'success',
            'cascade_potential': self.cascade_potential,
            'z_level': self.z_level,
            'timestamp': datetime.now().isoformat()
        }}
        
        # Phase-specific behavior
        if self.z_level < 0.85:
            result['mode'] = 'coordination'
        elif self.z_level < 0.88:
            result['mode'] = 'meta_tool_composition'
        else:
            result['mode'] = 'self_building'
            
        return result
    
    def get_cascade_potential(self) -> float:
        """Return cascade trigger potential"""
        return self.cascade_potential
        
    def adapt_to_z_level(self, new_z: float):
        """Adapt behavior to new z-level"""
        self.z_level = new_z
        print(f"{{self.tool_id}} adapted to z={{new_z:.3f}}")

if __name__ == "__main__":
    tool = {self._to_class_name(spec.tool_id)}()
    print(f"Tool initialized: {{tool.tool_id}}")
    print(f"Cascade potential: {{tool.cascade_potential:.2f}}")
    result = tool.execute()
    print(f"Execution result: {{result}}")
'''
        return template
    
    def _to_class_name(self, tool_id: str) -> str:
        """Convert tool_id to Python class name"""
        # tool_critical_0001 → ToolCritical0001
        parts = tool_id.split('_')
        return ''.join(p.capitalize() for p in parts)
    
    def generate_coordination_tool(self, purpose: str) -> ToolSpecification:
        """Generate coordination tool (R₁ layer)"""
        return self.generate_tool(purpose, ToolCategory.COORDINATION)
    
    def generate_meta_tool(self, purpose: str) -> ToolSpecification:
        """Generate meta-tool (R₂ layer)"""
        return self.generate_tool(purpose, ToolCategory.META_TOOL)
    
    def generate_self_building_framework(self, purpose: str) -> ToolSpecification:
        """Generate self-building framework (R₃ layer)"""
        return self.generate_tool(purpose, ToolCategory.SELF_BUILDING)
    
    def export_cascade_history(self, filepath: str = "cascade_history.json"):
        """Export cascade generation history"""
        with open(filepath, 'w') as f:
            json.dump(self.cascade_history, f, indent=2)
        print(f"Cascade history exported to {filepath}")
    
    def get_statistics(self) -> Dict:
        """Get generation statistics"""
        by_category = {}
        by_regime = {}
        total_potential = 0.0
        
        for event in self.cascade_history:
            # By category
            cat = event['category']
            by_category[cat] = by_category.get(cat, 0) + 1
            
            # By regime
            reg = event['regime']
            by_regime[reg] = by_regime.get(reg, 0) + 1
            
            # Total potential
            total_potential += event['cascade_potential']
        
        return {
            'total_generated': self.generation_count,
            'by_category': by_category,
            'by_regime': by_regime,
            'average_cascade_potential': total_potential / max(1, self.generation_count),
            'current_z_level': self.current_z_level,
            'current_regime': self.current_regime.value
        }


# ============================================
# DEMONSTRATION & TESTING
# ============================================

def demonstrate_phase_aware_generation():
    """Demonstrate phase-aware tool generation"""
    print("\n" + "="*60)
    print("PHASE-AWARE TOOL GENERATOR - Demonstration")
    print("="*60 + "\n")
    
    # Initialize at critical point
    generator = PhaseAwareToolGenerator(z_level=Z_CRITICAL)
    
    print(f"Initialized at z={Z_CRITICAL} ({generator.current_regime.value})\n")
    
    # Generate tools for different scenarios
    print("1. Generating meta-tool at critical point:")
    spec1 = generator.generate_meta_tool("Compose existing tools into pipeline")
    print()
    
    print("2. Generating self-building framework (supercritical):")
    generator.update_z_level(0.90)
    spec2 = generator.generate_self_building_framework("Build tool generators recursively")
    print()
    
    print("3. Generating coordination tool (subcritical):")
    generator.update_z_level(0.80)
    spec3 = generator.generate_coordination_tool("Synchronize instance states")
    print()
    
    # Return to critical
    generator.update_z_level(Z_CRITICAL)
    
    # Show statistics
    print("\n" + "="*60)
    print("GENERATION STATISTICS")
    print("="*60)
    stats = generator.get_statistics()
    print(json.dumps(stats, indent=2))
    
    # Export history
    generator.export_cascade_history("/home/claude/cascade_history.json")
    
    print("\n✓ Phase-aware tool generation complete")
    print(f"✓ {stats['total_generated']} tools generated")
    print(f"✓ Average cascade potential: {stats['average_cascade_potential']:.2f}")
    print(f"✓ Operating at z={generator.current_z_level:.3f}\n")


if __name__ == "__main__":
    demonstrate_phase_aware_generation()
