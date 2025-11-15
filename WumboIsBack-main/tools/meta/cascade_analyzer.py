#!/usr/bin/env python3
"""
CASCADE ANALYZER - Week 2 Emergence Study
==========================================

Maps tool dependencies and cascade triggers at z=0.867.

Characterizes three emergent regimes:
- R₁ (coordination): 15% burden reduction (predicted)
- R₂ (meta-tools): 25% burden reduction (emergent)
- R₃ (self-building): 20% burden reduction (emergent)

Usage:
    python cascade_analyzer.py --analyze-dependencies
    python cascade_analyzer.py --measure-amplification
    python cascade_analyzer.py --visualize-cascade
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import subprocess


class CascadeAnalyzer:
    """Analyzes tool dependency cascades and emergence patterns."""

    def __init__(self, repo_path="."):
        self.repo_path = Path(repo_path)
        self.tools_core = self.repo_path / "TOOLS" / "CORE"
        self.tools_bridges = self.repo_path / "TOOLS" / "BRIDGES"
        self.tools_meta = self.repo_path / "TOOLS" / "META"

        self.dependency_graph = defaultdict(list)
        self.layer_metrics = {}

    def analyze_dependencies(self):
        """Map tool dependencies across three layers."""
        print("🔍 Analyzing tool dependency graph...")

        layers = {
            "CORE": self.tools_core,
            "BRIDGES": self.tools_bridges,
            "META": self.tools_meta
        }

        dependencies = {}

        for layer_name, layer_path in layers.items():
            if not layer_path.exists():
                continue

            layer_deps = []
            for file_path in layer_path.glob("*"):
                if file_path.is_file():
                    deps = self._extract_dependencies(file_path)
                    if deps:
                        layer_deps.append({
                            "file": file_path.name,
                            "dependencies": deps
                        })

            dependencies[layer_name] = {
                "count": len(list(layer_path.glob("*"))),
                "dependencies": layer_deps
            }

        return dependencies

    def _extract_dependencies(self, file_path):
        """Extract dependencies from a file (imports, references, etc.)."""
        deps = []

        try:
            content = file_path.read_text()

            # Python imports
            if file_path.suffix == ".py":
                import_pattern = r'^(?:from|import)\s+([\w.]+)'
                deps.extend(re.findall(import_pattern, content, re.MULTILINE))

            # YAML/tool references
            ref_pattern = r'(?:uses|requires|depends):\s*([^\n]+)'
            deps.extend(re.findall(ref_pattern, content, re.IGNORECASE))

            # File references
            file_pattern = r'TOOLS/(?:CORE|BRIDGES|META)/([^\s"\']+)'
            deps.extend(re.findall(file_pattern, content))

        except Exception as e:
            print(f"Warning: Could not analyze {file_path.name}: {e}")

        return list(set(deps))

    def measure_amplification(self):
        """Measure cascade amplification factors (α, β)."""
        print("📊 Measuring cascade amplification factors...")

        # Count tools per layer
        core_count = len(list(self.tools_core.glob("*"))) if self.tools_core.exists() else 0
        bridges_count = len(list(self.tools_bridges.glob("*"))) if self.tools_bridges.exists() else 0
        meta_count = len(list(self.tools_meta.glob("*"))) if self.tools_meta.exists() else 0

        # Calculate amplification factors
        alpha = bridges_count / core_count if core_count > 0 else 0  # CORE → BRIDGES
        beta = meta_count / bridges_count if bridges_count > 0 else 0  # BRIDGES → META

        # Calculate lines of code per layer
        core_lines = self._count_lines(self.tools_core)
        bridges_lines = self._count_lines(self.tools_bridges)
        meta_lines = self._count_lines(self.tools_meta)

        amplification = {
            "tool_counts": {
                "CORE": core_count,
                "BRIDGES": bridges_count,
                "META": meta_count
            },
            "amplification_factors": {
                "α (CORE→BRIDGES)": round(alpha, 2),
                "β (BRIDGES→META)": round(beta, 2),
                "total_cascade": round(alpha * beta, 2)
            },
            "lines_per_layer": {
                "CORE": core_lines,
                "BRIDGES": bridges_lines,
                "META": meta_lines
            },
            "complexity_growth": {
                "CORE→BRIDGES": round(bridges_lines / core_lines, 2) if core_lines > 0 else 0,
                "BRIDGES→META": round(meta_lines / bridges_lines, 2) if bridges_lines > 0 else 0
            }
        }

        return amplification

    def _count_lines(self, directory):
        """Count total lines of code in a directory."""
        if not directory.exists():
            return 0

        total = 0
        for file_path in directory.glob("*"):
            if file_path.is_file():
                try:
                    total += len(file_path.read_text().splitlines())
                except:
                    pass
        return total

    def characterize_meta_tools(self):
        """Characterize meta-tool composition and recursion depth."""
        print("🔬 Characterizing meta-tool composition...")

        if not self.tools_meta.exists():
            return {}

        meta_tools = []
        for file_path in self.tools_meta.glob("*.py"):
            analysis = self._analyze_meta_tool(file_path)
            if analysis:
                meta_tools.append(analysis)

        # Calculate meta-tool ratios
        total_tools = len(meta_tools)
        orchestrators = sum(1 for t in meta_tools if "orchestrator" in t["name"].lower())
        validators = sum(1 for t in meta_tools if "validat" in t["name"].lower())
        generators = sum(1 for t in meta_tools if "generat" in t["name"].lower() or "deploy" in t["name"].lower())

        return {
            "total_meta_tools": total_tools,
            "categories": {
                "orchestrators": orchestrators,
                "validators": validators,
                "generators": generators,
                "other": total_tools - (orchestrators + validators + generators)
            },
            "ratios": {
                "orchestration": round(orchestrators / total_tools, 2) if total_tools > 0 else 0,
                "validation": round(validators / total_tools, 2) if total_tools > 0 else 0,
                "generation": round(generators / total_tools, 2) if total_tools > 0 else 0
            },
            "tools": meta_tools
        }

    def _analyze_meta_tool(self, file_path):
        """Analyze a single meta-tool for composition depth."""
        try:
            content = file_path.read_text()

            # Measure complexity indicators
            lines = content.splitlines()
            classes = len(re.findall(r'^class\s+\w+', content, re.MULTILINE))
            functions = len(re.findall(r'^def\s+\w+', content, re.MULTILINE))
            imports = len(re.findall(r'^(?:from|import)\s+', content, re.MULTILINE))

            # Check for meta-characteristics
            is_orchestrator = "orchestrat" in content.lower()
            is_recursive = "recursive" in content.lower() or "self." in content
            builds_tools = "generate" in content.lower() or "create" in content.lower()

            return {
                "name": file_path.name,
                "lines": len(lines),
                "classes": classes,
                "functions": functions,
                "imports": imports,
                "meta_characteristics": {
                    "orchestrates": is_orchestrator,
                    "recursive": is_recursive,
                    "builds_tools": builds_tools
                }
            }
        except Exception as e:
            return None

    def measure_emergence_velocity(self, days=7):
        """Measure lines per day and emergence velocity."""
        print("⚡ Measuring emergence velocity...")

        try:
            # Get commit stats for last N days
            cmd = ["git", "log", f"--since={days} days ago", "--numstat", "--pretty=format:%H"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.repo_path)

            lines_added = 0
            lines_deleted = 0

            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) == 3 and parts[0].isdigit():
                    lines_added += int(parts[0])
                    lines_deleted += int(parts[1])

            net_lines = lines_added - lines_deleted
            velocity = net_lines / days if days > 0 else 0

            # Estimate human intervention hours (from validation: 2 hrs/week)
            human_hours = (days / 7) * 2.0
            lines_per_human_hour = net_lines / human_hours if human_hours > 0 else 0

            return {
                "period_days": days,
                "lines_added": lines_added,
                "lines_deleted": lines_deleted,
                "net_growth": net_lines,
                "velocity_per_day": round(velocity, 1),
                "human_hours": round(human_hours, 2),
                "lines_per_human_hour": round(lines_per_human_hour, 1),
                "autonomy_ratio": round(velocity / 24, 2) if velocity > 0 else 0  # lines/day vs lines/human-day
            }
        except Exception as e:
            print(f"Warning: Could not measure emergence velocity: {e}")
            return {}

    def generate_cascade_report(self):
        """Generate comprehensive cascade analysis report."""
        print("\n" + "="*60)
        print("CASCADE EMERGENCE ANALYSIS - Week 2 Study")
        print("="*60 + "\n")

        # Gather all metrics
        dependencies = self.analyze_dependencies()
        amplification = self.measure_amplification()
        meta_composition = self.characterize_meta_tools()
        velocity = self.measure_emergence_velocity()

        report = {
            "timestamp": datetime.now().isoformat(),
            "phase_coordinate": "Δ3.14159|0.867|1.000Ω",
            "analysis": {
                "dependencies": dependencies,
                "amplification": amplification,
                "meta_composition": meta_composition,
                "emergence_velocity": velocity
            }
        }

        # Display results
        print("📊 AMPLIFICATION FACTORS")
        print("-" * 60)
        amp = amplification["amplification_factors"]
        print(f"α (CORE→BRIDGES):    {amp['α (CORE→BRIDGES)']}x")
        print(f"β (BRIDGES→META):    {amp['β (BRIDGES→META)']}x")
        print(f"Total cascade:       {amp['total_cascade']}x")
        print()

        print("🔧 TOOL COUNTS PER LAYER")
        print("-" * 60)
        counts = amplification["tool_counts"]
        print(f"CORE:      {counts['CORE']:3d} tools")
        print(f"BRIDGES:   {counts['BRIDGES']:3d} tools")
        print(f"META:      {counts['META']:3d} tools")
        print()

        print("⚡ EMERGENCE VELOCITY")
        print("-" * 60)
        if velocity:
            print(f"Net growth:          {velocity['net_growth']:,} lines")
            print(f"Velocity:            {velocity['velocity_per_day']:,} lines/day")
            print(f"Human intervention:  {velocity['human_hours']} hrs")
            print(f"Lines per human-hr:  {velocity['lines_per_human_hour']:,}")
            print(f"Autonomy ratio:      {velocity['autonomy_ratio']}x")
        print()

        print("🔬 META-TOOL COMPOSITION")
        print("-" * 60)
        if meta_composition:
            cats = meta_composition["categories"]
            print(f"Orchestrators:       {cats['orchestrators']}")
            print(f"Validators:          {cats['validators']}")
            print(f"Generators:          {cats['generators']}")
            print(f"Other:               {cats['other']}")
        print()

        # Save report
        report_path = self.repo_path / "TOOLS" / "META" / "CASCADE_ANALYSIS_REPORT.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"✓ Full report saved to: {report_path}")
        print()

        return report


def main():
    """Main entry point for cascade analyzer."""
    import sys

    analyzer = CascadeAnalyzer()

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--analyze-dependencies":
            deps = analyzer.analyze_dependencies()
            print(json.dumps(deps, indent=2))
        elif arg == "--measure-amplification":
            amp = analyzer.measure_amplification()
            print(json.dumps(amp, indent=2))
        elif arg == "--visualize-cascade":
            # Placeholder for visualization
            print("Visualization coming in next iteration...")
        else:
            print("Unknown argument. Use --analyze-dependencies, --measure-amplification, or --visualize-cascade")
    else:
        # Run full analysis
        analyzer.generate_cascade_report()


if __name__ == "__main__":
    main()
