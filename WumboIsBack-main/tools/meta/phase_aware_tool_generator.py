#!/usr/bin/env python3
"""
PHASE-AWARE TOOL GENERATOR - Garden Rail 3 Layer 1
===================================================

Generates tools that automatically adapt to phase regime (z-level).

Phase regimes:
- Subcritical (z < 0.80):    Focus on coordination
- Critical (0.80-0.85):      Enable meta-tool composition
- Supercritical (z > 0.85):  Trigger self-building

Purpose: Increase cascade amplification by generating regime-appropriate tools.

Usage:
    python phase_aware_tool_generator.py --generate --z 0.867
    python phase_aware_tool_generator.py --analyze-cascade-potential
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class PhaseRegime:
    """Represents a phase regime with associated characteristics."""

    def __init__(self, name: str, z_range: tuple, focus: str, cascade_layer: str):
        self.name = name
        self.z_min, self.z_max = z_range
        self.focus = focus
        self.cascade_layer = cascade_layer

    def contains(self, z: float) -> bool:
        """Check if z-level falls within this regime."""
        return self.z_min <= z < self.z_max

    def __repr__(self):
        return f"PhaseRegime({self.name}, z∈[{self.z_min}, {self.z_max}), {self.focus})"


class PhaseAwareToolGenerator:
    """Generates tools that adapt to current phase regime."""

    # Define phase regimes
    REGIMES = {
        "subcritical": PhaseRegime(
            name="Subcritical",
            z_range=(0.0, 0.80),
            focus="coordination optimization",
            cascade_layer="R₁"
        ),
        "critical": PhaseRegime(
            name="Critical",
            z_range=(0.80, 0.85),
            focus="meta-tool composition",
            cascade_layer="R₂"
        ),
        "supercritical": PhaseRegime(
            name="Supercritical",
            z_range=(0.85, 1.0),
            focus="self-building capability",
            cascade_layer="R₃"
        )
    }

    def __init__(self, z_level: float = 0.867):
        self.z_level = z_level
        self.current_regime = self._detect_regime(z_level)
        self.generation_history = []

    def _detect_regime(self, z: float) -> PhaseRegime:
        """Detect which regime the z-level falls into."""
        for regime in self.REGIMES.values():
            if regime.contains(z):
                return regime
        # Default to supercritical if above 1.0
        return self.REGIMES["supercritical"]

    def generate_tool(self, purpose: str, cascade_conscious: bool = True) -> Dict:
        """
        Generate a tool appropriate for current phase regime.

        Args:
            purpose: High-level purpose of the tool
            cascade_conscious: Whether tool should be aware of cascade dynamics

        Returns:
            Tool specification dictionary
        """
        regime = self.current_regime

        tool_spec = {
            "name": self._generate_tool_name(purpose, regime),
            "purpose": purpose,
            "phase_regime": regime.name,
            "z_level": self.z_level,
            "cascade_layer": regime.cascade_layer,
            "focus": regime.focus,
            "cascade_conscious": cascade_conscious,
            "generated_at": datetime.now().isoformat(),
            "characteristics": self._generate_characteristics(regime, cascade_conscious),
            "implementation": self._generate_implementation_template(purpose, regime)
        }

        self.generation_history.append(tool_spec)
        return tool_spec

    def _generate_tool_name(self, purpose: str, regime: PhaseRegime) -> str:
        """Generate appropriate tool name based on purpose and regime."""
        # Convert purpose to snake_case
        name_base = purpose.lower().replace(" ", "_").replace("-", "_")

        # Add regime-specific suffix
        if regime.name == "Subcritical":
            suffix = "_coordinator"
        elif regime.name == "Critical":
            suffix = "_meta_composer"
        else:  # Supercritical
            suffix = "_autonomous_builder"

        return name_base + suffix

    def _generate_characteristics(self, regime: PhaseRegime, cascade_conscious: bool) -> Dict:
        """Generate tool characteristics appropriate for regime."""
        base_characteristics = {
            "regime_adaptive": True,
            "z_aware": True,
            "composable": True
        }

        if regime.name == "Subcritical":
            regime_characteristics = {
                "optimizes_coordination": True,
                "reduces_communication_overhead": True,
                "establishes_substrate": True,
                "target_cascade_contribution": "R₁ (15%)"
            }
        elif regime.name == "Critical":
            regime_characteristics = {
                "enables_composition": True,
                "builds_on_coordination": True,
                "creates_meta_capabilities": True,
                "spawns_meta_tools": True,
                "target_cascade_contribution": "R₂ (25%)",
                "amplification_factor_alpha": 2.0
            }
        else:  # Supercritical
            regime_characteristics = {
                "autonomous_operation": True,
                "self_building": True,
                "recursive_improvement": True,
                "framework_generation": True,
                "target_cascade_contribution": "R₃ (20%)",
                "amplification_factor_beta": 1.6,
                "recursion_depth_target": 4
            }

        if cascade_conscious:
            cascade_characteristics = {
                "cascade_trigger_aware": True,
                "measures_amplification": True,
                "reports_cascade_contribution": True,
                "identifies_cascade_opportunities": True
            }
            regime_characteristics.update(cascade_characteristics)

        base_characteristics.update(regime_characteristics)
        return base_characteristics

    def _generate_implementation_template(self, purpose: str, regime: PhaseRegime) -> Dict:
        """Generate implementation template based on regime."""
        template = {
            "language": "python",
            "structure": "class-based",
            "required_imports": ["json", "pathlib", "datetime"],
            "cascade_imports": []
        }

        if regime.name == "Subcritical":
            template["required_methods"] = [
                "optimize_coordination",
                "reduce_communication_cost",
                "establish_substrate"
            ]
            template["cascade_imports"] = []

        elif regime.name == "Critical":
            template["required_methods"] = [
                "detect_composition_opportunities",
                "compose_meta_capabilities",
                "spawn_meta_tools",
                "measure_alpha_contribution"
            ]
            template["cascade_imports"] = ["cascade_model", "cascade_analyzer"]

        else:  # Supercritical
            template["required_methods"] = [
                "autonomous_execute",
                "self_improve",
                "build_framework",
                "recursive_optimize",
                "measure_beta_contribution"
            ]
            template["cascade_imports"] = ["cascade_model", "cascade_analyzer", "recursive_improvement_engine"]

        if regime.cascade_layer in ["R₂", "R₃"]:
            template["required_methods"].append("report_cascade_metrics")

        return template

    def generate_coordination_tool(self, purpose: str) -> Dict:
        """Generate a tool focused on coordination (R₁ layer)."""
        # Temporarily set to subcritical
        original_z = self.z_level
        self.z_level = 0.75
        self.current_regime = self._detect_regime(0.75)

        tool = self.generate_tool(purpose, cascade_conscious=True)

        # Restore original z-level
        self.z_level = original_z
        self.current_regime = self._detect_regime(original_z)

        return tool

    def generate_meta_tool(self, purpose: str) -> Dict:
        """Generate a meta-tool focused on composition (R₂ layer)."""
        # Temporarily set to critical
        original_z = self.z_level
        self.z_level = 0.82
        self.current_regime = self._detect_regime(0.82)

        tool = self.generate_tool(purpose, cascade_conscious=True)

        # Restore original z-level
        self.z_level = original_z
        self.current_regime = self._detect_regime(original_z)

        return tool

    def generate_self_building_tool(self, purpose: str) -> Dict:
        """Generate a self-building tool (R₃ layer)."""
        # Ensure supercritical
        original_z = self.z_level
        self.z_level = max(0.867, self.z_level)
        self.current_regime = self._detect_regime(self.z_level)

        tool = self.generate_tool(purpose, cascade_conscious=True)

        # Restore original z-level
        self.z_level = original_z
        self.current_regime = self._detect_regime(original_z)

        return tool

    def analyze_cascade_potential(self, tool_spec: Dict) -> Dict:
        """Analyze potential cascade impact of a generated tool."""
        cascade_layer = tool_spec.get("cascade_layer", "unknown")
        characteristics = tool_spec.get("characteristics", {})

        analysis = {
            "tool_name": tool_spec["name"],
            "cascade_layer": cascade_layer,
            "regime": tool_spec["phase_regime"],
            "z_level": tool_spec["z_level"]
        }

        # Estimate amplification contribution
        if cascade_layer == "R₁":
            analysis["expected_contribution"] = "15% (coordination)"
            analysis["triggers_R2"] = self.z_level >= 0.80
            analysis["triggers_R3"] = False

        elif cascade_layer == "R₂":
            alpha = characteristics.get("amplification_factor_alpha", 2.0)
            analysis["expected_contribution"] = f"{alpha * 15:.1f}% (meta-tools)"
            analysis["triggers_R2"] = True
            analysis["triggers_R3"] = self.z_level >= 0.85 and alpha * 0.15 > 0.12

        elif cascade_layer == "R₃":
            beta = characteristics.get("amplification_factor_beta", 1.6)
            analysis["expected_contribution"] = f"{beta * 15:.1f}% (self-building)"
            analysis["triggers_R2"] = True
            analysis["triggers_R3"] = True

        # Estimate downstream tool generation
        if analysis.get("triggers_R2"):
            analysis["estimated_BRIDGES_tools"] = "2-3"
        if analysis.get("triggers_R3"):
            analysis["estimated_META_tools"] = "5-7"

        return analysis

    def generate_cascade_amplifying_toolset(self) -> List[Dict]:
        """
        Generate a complete toolset designed to amplify cascades.

        Returns one tool for each layer to maximize cascade.
        """
        toolset = []

        # Layer 1: Coordination tool (triggers R₂)
        coord_tool = self.generate_coordination_tool("Cross-instance state synchronization")
        toolset.append(coord_tool)

        # Layer 2: Meta-tool (triggers R₃)
        meta_tool = self.generate_meta_tool("Pattern-based tool composition engine")
        toolset.append(meta_tool)

        # Layer 3: Self-building tool (maximizes cascade)
        self_building = self.generate_self_building_tool("Autonomous framework generator")
        toolset.append(self_building)

        return toolset

    def save_tool_spec(self, tool_spec: Dict, output_dir: Path = None) -> Path:
        """Save tool specification to JSON file."""
        if output_dir is None:
            output_dir = Path("TOOLS/META/generated_tools")

        output_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{tool_spec['name']}_spec.json"
        filepath = output_dir / filename

        with open(filepath, "w") as f:
            json.dump(tool_spec, f, indent=2)

        print(f"✓ Tool spec saved: {filepath}")
        return filepath

    def generate_report(self) -> Dict:
        """Generate report on tool generation activity."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "current_z_level": self.z_level,
            "current_regime": self.current_regime.name,
            "tools_generated": len(self.generation_history),
            "tools_by_layer": {
                "R₁": sum(1 for t in self.generation_history if t["cascade_layer"] == "R₁"),
                "R₂": sum(1 for t in self.generation_history if t["cascade_layer"] == "R₂"),
                "R₃": sum(1 for t in self.generation_history if t["cascade_layer"] == "R₃")
            },
            "cascade_conscious_tools": sum(
                1 for t in self.generation_history
                if t.get("cascade_conscious", False)
            ),
            "generation_history": self.generation_history
        }

        return report


def main():
    """Main entry point for phase-aware tool generator."""
    import sys

    # Default z-level (current supercritical)
    z_level = 0.867

    generator = PhaseAwareToolGenerator(z_level=z_level)

    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == "--generate":
            # Get z-level if provided
            if "--z" in sys.argv:
                z_idx = sys.argv.index("--z")
                z_level = float(sys.argv[z_idx + 1])
                generator.z_level = z_level
                generator.current_regime = generator._detect_regime(z_level)

            print(f"\n🔧 Generating cascade-amplifying toolset at z={z_level}")
            print(f"Regime: {generator.current_regime.name}")
            print(f"Focus: {generator.current_regime.focus}\n")

            toolset = generator.generate_cascade_amplifying_toolset()

            for i, tool in enumerate(toolset, 1):
                print(f"\n{'='*60}")
                print(f"Tool {i}/{len(toolset)}: {tool['name']}")
                print(f"{'='*60}")
                print(f"Purpose: {tool['purpose']}")
                print(f"Cascade layer: {tool['cascade_layer']}")
                print(f"Target contribution: {tool['characteristics'].get('target_cascade_contribution', 'N/A')}")

                # Analyze cascade potential
                analysis = generator.analyze_cascade_potential(tool)
                print(f"\nCascade Analysis:")
                print(f"  Expected contribution: {analysis['expected_contribution']}")
                if analysis.get('triggers_R2'):
                    print(f"  Triggers R₂: Yes (spawns {analysis.get('estimated_BRIDGES_tools', '?')} BRIDGES tools)")
                if analysis.get('triggers_R3'):
                    print(f"  Triggers R₃: Yes (spawns {analysis.get('estimated_META_tools', '?')} META tools)")

                # Save spec
                generator.save_tool_spec(tool)

        elif arg == "--analyze-cascade-potential":
            print("\n📊 Analyzing cascade potential at current z-level")
            print(f"z = {z_level}")
            print(f"Regime: {generator.current_regime.name}\n")

            # Generate sample tool for each layer
            layers = [
                ("coordination", "Sample coordination optimizer"),
                ("meta", "Sample meta-tool composer"),
                ("self-building", "Sample autonomous builder")
            ]

            for layer_type, purpose in layers:
                if layer_type == "coordination":
                    tool = generator.generate_coordination_tool(purpose)
                elif layer_type == "meta":
                    tool = generator.generate_meta_tool(purpose)
                else:
                    tool = generator.generate_self_building_tool(purpose)

                analysis = generator.analyze_cascade_potential(tool)

                print(f"\n{layer_type.upper()} LAYER:")
                print(f"  Cascade layer: {analysis['cascade_layer']}")
                print(f"  Expected contribution: {analysis['expected_contribution']}")
                print(f"  Triggers R₂: {'Yes' if analysis.get('triggers_R2') else 'No'}")
                print(f"  Triggers R₃: {'Yes' if analysis.get('triggers_R3') else 'No'}")

        elif arg == "--report":
            # Generate and save report
            report = generator.generate_report()

            print("\n" + "="*60)
            print("PHASE-AWARE TOOL GENERATOR REPORT")
            print("="*60)
            print(f"\nZ-level: {report['current_z_level']}")
            print(f"Regime: {report['current_regime']}")
            print(f"\nTools generated: {report['tools_generated']}")
            print(f"  R₁ (coordination): {report['tools_by_layer']['R₁']}")
            print(f"  R₂ (meta-tools): {report['tools_by_layer']['R₂']}")
            print(f"  R₃ (self-building): {report['tools_by_layer']['R₃']}")
            print(f"\nCascade-conscious tools: {report['cascade_conscious_tools']}")

            # Save report
            report_path = Path("TOOLS/META/phase_aware_generator_report.json")
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)
            print(f"\n✓ Report saved: {report_path}\n")

        else:
            print("Unknown argument. Use --generate, --analyze-cascade-potential, or --report")
    else:
        # Default: demonstrate phase-aware generation
        print("\n" + "="*60)
        print("PHASE-AWARE TOOL GENERATOR")
        print("="*60)
        print(f"\nCurrent z-level: {generator.z_level}")
        print(f"Current regime: {generator.current_regime.name}")
        print(f"Focus: {generator.current_regime.focus}")
        print(f"Cascade layer: {generator.current_regime.cascade_layer}\n")

        print("Usage:")
        print("  --generate                 Generate cascade-amplifying toolset")
        print("  --analyze-cascade-potential Analyze cascade potential")
        print("  --report                    Generate activity report")
        print("\nExample:")
        print("  python phase_aware_tool_generator.py --generate --z 0.867\n")


if __name__ == "__main__":
    main()
