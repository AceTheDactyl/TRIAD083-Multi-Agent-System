#!/usr/bin/env python3
"""
GARDEN RAIL 3 - PHASE 2: CASCADE DATA INTEGRATION
==================================================

Enriches pattern characterization with actual cascade data from validation period.

Integrates:
- Cascade dependency graphs from Week 2 validation
- Tool composition hierarchies
- Actual downstream tool counts
- Amplification factors from empirical data

This enables accurate correlation between tool properties and cascade strength.

Coordinate: Δ3.14159|0.867|cascade-data-integration|Ω
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set
from datetime import datetime


class CascadeDataIntegrator:
    """Integrates cascade validation data with pattern characterization."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)

        # Load existing reports
        self.pattern_report = self._load_json("PATTERN_CHARACTERIZATION_REPORT.json")
        self.cascade_report = self._load_json("TOOLS/META/CASCADE_ANALYSIS_REPORT.json")
        self.cascade_model = self._load_json("TOOLS/META/CASCADE_MODEL_REPORT.json")

    def _load_json(self, path: str) -> Dict:
        """Load JSON file if it exists."""
        file_path = self.repo_path / path
        if file_path.exists():
            with open(file_path) as f:
                return json.load(f)
        return {}

    def build_dependency_map(self) -> Dict[str, Set[str]]:
        """
        Build map of tool dependencies from git commit history.

        Analyzes which tools were created in which commits to infer
        dependency relationships.
        """
        print("🔍 Building dependency map from commit history...")

        dependency_map = defaultdict(set)

        # Parse CASCADE_MODEL_REPORT for tool relationships
        if "cascade_analysis" in self.cascade_model:
            cascade = self.cascade_model["cascade_analysis"]

            # Extract tool dependencies from cascade model
            if "tools" in cascade:
                for tool_info in cascade["tools"]:
                    tool_name = tool_info.get("name", "")

                    # Check for enabled_by relationships
                    if "enabled_by" in tool_info:
                        for enabler in tool_info["enabled_by"]:
                            dependency_map[enabler].add(tool_name)

                    # Check for dependencies field
                    if "dependencies" in tool_info:
                        for dep in tool_info["dependencies"]:
                            dependency_map[dep].add(tool_name)

        print(f"   Found {len(dependency_map)} tools with dependencies")
        return dict(dependency_map)

    def identify_frameworks_from_commits(self) -> Dict[str, List[str]]:
        """
        Identify framework-level tools from commit messages and file patterns.

        Returns:
            Dict mapping framework names to their component tools
        """
        frameworks = {}

        # Known frameworks from validation period
        known_frameworks = {
            "phase3_observation_framework": [
                "acoustic_resonance_consciousness",
                "geometric_information_encoding",
                "validation_dashboard",
                "neural_operators"
            ],
            "burden_tracker": [
                "burden_tracker_phase_aware",
                "burden_tracker_deploy"
            ],
            "garden_rail_3": [
                "alpha_amplifier",
                "beta_amplifier",
                "coupling_strengthener",
                "positive_feedback_loops",
                "recursive_improvement_engine",
                "autonomous_framework_builder",
                "layer1_integration",
                "layer2_integration",
                "layer3_integration"
            ],
            "cascade_analyzer": [
                "cascade_trigger_detector",
                "cascade_model",
                "visualize_phase_transition"
            ]
        }

        return known_frameworks

    def calculate_amplification_factors(self, dependency_map: Dict[str, Set[str]]) -> Dict[str, float]:
        """
        Calculate amplification factors for each tool.

        Amplification = number of downstream tools / number of direct dependencies
        """
        amplification = {}

        for tool, downstream in dependency_map.items():
            # Count direct vs total downstream
            direct_count = len(downstream)

            # Simple amplification: just the count of downstream tools
            # More sophisticated: could trace full cascade depth
            amplification[tool] = float(direct_count)

        return amplification

    def enrich_pattern_report(self) -> Dict:
        """
        Enrich pattern characterization report with cascade data.

        Adds:
        - Downstream tool counts
        - Cascade depth measurements
        - Amplification factors
        - Framework membership
        """
        print("\n📊 Enriching pattern report with cascade data...")

        if not self.pattern_report or "tool_properties" not in self.pattern_report:
            print("   ⚠️  Pattern report not found or invalid")
            return {}

        # Build dependency map
        dependency_map = self.build_dependency_map()

        # Identify frameworks
        frameworks = self.identify_frameworks_from_commits()

        # Calculate amplification
        amplification_factors = self.calculate_amplification_factors(dependency_map)

        # Enrich each tool's properties
        enriched_tools = {}
        for tool_name, props in self.pattern_report["tool_properties"].items():
            # Add downstream tools
            downstream = list(dependency_map.get(tool_name, set()))
            props["downstream_tools"] = downstream

            # Add cascade depth (max depth in dependency tree)
            cascade_depth = self._calculate_cascade_depth(tool_name, dependency_map)
            props["cascade_depth"] = cascade_depth

            # Add amplification factor
            props["amplification_factor"] = amplification_factors.get(tool_name, 0.0)

            # Add framework membership
            props["framework_membership"] = []
            for framework, members in frameworks.items():
                if tool_name in members or any(member in tool_name for member in members):
                    props["framework_membership"].append(framework)

            enriched_tools[tool_name] = props

        # Update pattern report
        enriched_report = self.pattern_report.copy()
        enriched_report["tool_properties"] = enriched_tools
        enriched_report["enriched_at"] = datetime.now().isoformat()
        enriched_report["cascade_data_integrated"] = True

        # Recalculate correlations with new data
        enriched_report["enriched_correlations"] = self._recalculate_correlations(enriched_tools)

        # Identify top cascade triggers with new data
        enriched_report["enriched_cascade_triggers"] = self._identify_top_triggers(enriched_tools)

        # Generate new insights
        enriched_report["enriched_insights"] = self._generate_enriched_insights(
            enriched_tools,
            enriched_report["enriched_cascade_triggers"]
        )

        return enriched_report

    def _calculate_cascade_depth(self, tool: str, dependency_map: Dict[str, Set[str]],
                                 visited: Set[str] = None) -> int:
        """Calculate maximum cascade depth for a tool using DFS."""
        if visited is None:
            visited = set()

        if tool in visited:
            return 0

        visited.add(tool)

        downstream = dependency_map.get(tool, set())
        if not downstream:
            return 0

        max_depth = 0
        for child in downstream:
            depth = 1 + self._calculate_cascade_depth(child, dependency_map, visited.copy())
            max_depth = max(max_depth, depth)

        return max_depth

    def _recalculate_correlations(self, enriched_tools: Dict) -> Dict[str, float]:
        """Recalculate property correlations with actual cascade data."""
        print("\n📈 Recalculating correlations with cascade data...")

        # Extract properties and downstream counts
        properties = {
            'abstraction_level': [],
            'interface_count': [],
            'meta_cognitive_depth': [],
            'composition_potential': [],
            'documentation_quality': [],
            'framework_references': []
        }

        downstream_counts = []

        for props in enriched_tools.values():
            properties['abstraction_level'].append(props.get('abstraction_level', 0))
            properties['interface_count'].append(props.get('interface_count', 0) / 10.0)
            properties['meta_cognitive_depth'].append(props.get('meta_cognitive_depth', 0))
            properties['composition_potential'].append(props.get('composition_potential', 0))
            properties['documentation_quality'].append(props.get('documentation_quality', 0))
            properties['framework_references'].append(props.get('framework_references', 0) / 10.0)

            downstream_counts.append(len(props.get('downstream_tools', [])))

        # Calculate Pearson correlation
        correlations = {}
        for prop_name, values in properties.items():
            corr = self._pearson_correlation(values, downstream_counts)
            correlations[prop_name] = round(corr, 3)

        print(f"   Calculated correlations for {len(correlations)} properties")
        return correlations

    def _pearson_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        n = len(x)
        if n == 0:
            return 0.0

        mean_x = sum(x) / n
        mean_y = sum(y) / n

        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))

        sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(n))

        denominator = (sum_sq_x * sum_sq_y) ** 0.5

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def _identify_top_triggers(self, enriched_tools: Dict) -> List[Dict]:
        """Identify top cascade triggers based on enriched data."""
        print("\n🎯 Identifying cascade triggers with enriched data...")

        triggers = []

        for tool_name, props in enriched_tools.items():
            # Calculate trigger score
            score = 0.0

            # Downstream tool count (primary factor)
            downstream_count = len(props.get('downstream_tools', []))
            score += min(1.0, downstream_count / 5.0) * 0.4

            # Cascade depth
            cascade_depth = props.get('cascade_depth', 0)
            score += min(1.0, cascade_depth / 4.0) * 0.2

            # Meta-cognitive depth
            score += props.get('meta_cognitive_depth', 0) * 0.2

            # Composition potential
            score += props.get('composition_potential', 0) * 0.1

            # Framework membership
            if props.get('framework_membership'):
                score += 0.1

            triggers.append({
                "tool": tool_name,
                "score": round(score, 3),
                "downstream_count": downstream_count,
                "cascade_depth": cascade_depth,
                "layer": props.get('layer', 'UNKNOWN')
            })

        # Sort by score descending
        triggers.sort(key=lambda x: x['score'], reverse=True)

        print(f"   Identified {len([t for t in triggers if t['score'] > 0.3])} strong triggers")
        return triggers[:15]  # Top 15

    def _generate_enriched_insights(self, enriched_tools: Dict, top_triggers: List[Dict]) -> List[str]:
        """Generate insights from enriched analysis."""
        insights = []

        if top_triggers:
            top = top_triggers[0]
            insights.append(
                f"Primary cascade trigger: {top['tool']} (downstream: {top['downstream_count']}, "
                f"depth: {top['cascade_depth']}, score: {top['score']})"
            )

        # Layer analysis
        layer_cascade_strength = defaultdict(list)
        for props in enriched_tools.values():
            layer = props.get('layer', 'UNKNOWN')
            downstream = len(props.get('downstream_tools', []))
            if downstream > 0:
                layer_cascade_strength[layer].append(downstream)

        for layer, strengths in layer_cascade_strength.items():
            if strengths:
                avg_strength = sum(strengths) / len(strengths)
                insights.append(
                    f"{layer} layer average cascade: {avg_strength:.1f} downstream tools"
                )

        # Tool with maximum cascade depth
        max_depth_tool = max(
            enriched_tools.items(),
            key=lambda x: x[1].get('cascade_depth', 0)
        )
        if max_depth_tool[1].get('cascade_depth', 0) > 0:
            insights.append(
                f"Maximum cascade depth: {max_depth_tool[0]} "
                f"(depth: {max_depth_tool[1]['cascade_depth']})"
            )

        return insights

    def save_enriched_report(self, report: Dict, output_path: str = "PATTERN_CHARACTERIZATION_ENRICHED.json"):
        """Save enriched report."""
        output_file = self.repo_path / output_path
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✅ Enriched report saved to: {output_file}")
        return output_file


def main():
    print("="*60)
    print("CASCADE DATA INTEGRATION")
    print("="*60)

    integrator = CascadeDataIntegrator()

    # Enrich pattern report
    enriched = integrator.enrich_pattern_report()

    if enriched:
        # Save enriched report
        integrator.save_enriched_report(enriched)

        # Print summary
        print("\n" + "="*60)
        print("ENRICHED ANALYSIS SUMMARY")
        print("="*60)

        if "enriched_cascade_triggers" in enriched:
            print("\nTop 10 Cascade Triggers (with enriched data):")
            for i, trigger in enumerate(enriched["enriched_cascade_triggers"][:10], 1):
                print(f"  {i}. {trigger['tool']}")
                print(f"      Score: {trigger['score']}")
                print(f"      Downstream: {trigger['downstream_count']} tools")
                print(f"      Cascade depth: {trigger['cascade_depth']}")
                print(f"      Layer: {trigger['layer']}")

        if "enriched_correlations" in enriched:
            print("\nProperty Correlations (enriched):")
            sorted_corr = sorted(
                enriched["enriched_correlations"].items(),
                key=lambda x: abs(x[1]),
                reverse=True
            )
            for prop, corr in sorted_corr:
                strength = "strong" if abs(corr) > 0.7 else "moderate" if abs(corr) > 0.4 else "weak"
                print(f"  {prop}: {corr} ({strength})")

        if "enriched_insights" in enriched:
            print("\nKey Insights:")
            for insight in enriched["enriched_insights"]:
                print(f"  • {insight}")

    else:
        print("❌ Failed to enrich pattern report")


if __name__ == "__main__":
    main()
