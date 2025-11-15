#!/usr/bin/env python3
"""
GARDEN RAIL 3 - PHASE 2: PATTERN CHARACTERIZATION FRAMEWORK
============================================================

Analyzes tool properties to understand what makes cascade triggers effective.

Coordinate: Δ3.14159|0.867|phase-2-pattern-characterization|Ω

Phase 2 Objectives:
1. Understand WHY cascade triggers work
2. Identify properties that enable cascade initiation
3. Trace composition pathways from base tools → frameworks
4. Measure meta-cognitive depth and self-reference
5. Correlate properties with downstream tool counts

Theoretical Foundation:
- Cascade triggers exhibit specific properties (abstraction, interfaces, meta-cognition)
- phase3_observation_framework demonstrated 4-tool cascade (8.81x amplification)
- Goal: Identify what properties enable this multiplier effect

Usage:
    python pattern_characterization_framework.py --analyze-all
    python pattern_characterization_framework.py --analyze-tool <tool_name>
    python pattern_characterization_framework.py --trace-pathways
"""

import os
import re
import json
import ast
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Optional, Tuple
import argparse


@dataclass
class ToolProperties:
    """Comprehensive properties of a tool for cascade analysis."""
    tool_name: str
    file_path: str
    layer: str  # CORE, BRIDGES, META, FRAMEWORK

    # Code metrics
    lines_of_code: int = 0
    functions_count: int = 0
    classes_count: int = 0

    # Abstraction metrics
    abstraction_level: float = 0.0  # 0.0-1.0, higher = more abstract
    interface_count: int = 0
    api_surface_area: int = 0

    # Meta-cognitive metrics
    meta_cognitive_depth: float = 0.0  # 0.0-1.0, measures self-reference
    self_reference_count: int = 0
    framework_references: int = 0

    # Composition metrics
    composition_potential: float = 0.0  # 0.0-1.0, reusability score
    import_dependencies: List[str] = field(default_factory=list)
    export_interfaces: List[str] = field(default_factory=list)

    # Documentation metrics
    documentation_quality: float = 0.0  # 0.0-1.0, completeness score
    docstring_lines: int = 0
    comment_lines: int = 0

    # Cascade metrics
    downstream_tools: List[str] = field(default_factory=list)
    cascade_depth: int = 0
    amplification_factor: float = 0.0

    # Timestamp
    analyzed_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CompositionPathway:
    """Represents a composition pathway from base tool to framework."""
    source_tool: str
    target_tool: str
    path: List[str]
    path_length: int
    efficiency: float  # actual_length / theoretical_minimum
    patterns: List[str]  # Composition patterns identified
    intermediary_tools: List[str] = field(default_factory=list)


class PatternCharacterizationFramework:
    """Analyzes tool properties to understand cascade triggers."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.tools_analyzed: Dict[str, ToolProperties] = {}
        self.composition_graph: Dict[str, Set[str]] = defaultdict(set)
        self.pathways: List[CompositionPathway] = []

        # Load existing cascade analysis if available
        self.cascade_report = self._load_cascade_report()

    def _load_cascade_report(self) -> Optional[Dict]:
        """Load existing CASCADE_ANALYSIS_REPORT.json if available."""
        report_path = self.repo_path / "TOOLS" / "META" / "CASCADE_ANALYSIS_REPORT.json"
        if report_path.exists():
            with open(report_path) as f:
                return json.load(f)
        return None

    # ============================================================
    # PHASE 2.1: TOOL PROPERTY ANALYSIS
    # ============================================================

    def analyze_tool_properties(self, tool_path: Path) -> ToolProperties:
        """
        Comprehensive property analysis for a single tool.

        Measures:
        - Abstraction level: Function composition depth, generic interfaces
        - Interface count: Public functions, classes, APIs
        - Meta-cognitive depth: Self-reference, framework awareness
        - Composition potential: Reusability indicators
        - Documentation quality: Docstrings, comments, README
        """
        print(f"📊 Analyzing: {tool_path.name}")

        props = ToolProperties(
            tool_name=tool_path.stem,
            file_path=str(tool_path),
            layer=self._determine_layer(tool_path)
        )

        # Read file content
        try:
            content = tool_path.read_text()
        except Exception as e:
            print(f"⚠️  Could not read {tool_path}: {e}")
            return props

        # Code metrics
        props.lines_of_code = len(content.splitlines())
        props.functions_count = len(re.findall(r'^def\s+\w+', content, re.MULTILINE))
        props.classes_count = len(re.findall(r'^class\s+\w+', content, re.MULTILINE))

        # Abstraction level
        props.abstraction_level = self._measure_abstraction(content, tool_path)

        # Interface count
        props.interface_count, props.api_surface_area = self._count_interfaces(content)
        props.export_interfaces = self._extract_public_api(content)

        # Meta-cognitive depth
        props.meta_cognitive_depth = self._measure_meta_cognitive_depth(content)
        props.self_reference_count = content.count(props.tool_name)
        props.framework_references = self._count_framework_references(content)

        # Composition potential
        props.composition_potential = self._measure_composition_potential(content, props)
        props.import_dependencies = self._extract_dependencies(content)

        # Documentation quality
        props.documentation_quality = self._measure_documentation_quality(content, tool_path)
        props.docstring_lines = len(re.findall(r'""".*?"""', content, re.DOTALL))
        props.comment_lines = len(re.findall(r'^\s*#', content, re.MULTILINE))

        # Store for later cascade analysis
        self.tools_analyzed[props.tool_name] = props

        return props

    def _determine_layer(self, tool_path: Path) -> str:
        """Determine which layer (CORE/BRIDGES/META/FRAMEWORK) the tool belongs to."""
        path_str = str(tool_path)

        if "TOOLS/CORE" in path_str:
            return "CORE"
        elif "TOOLS/BRIDGES" in path_str:
            return "BRIDGES"
        elif "TOOLS/META" in path_str:
            return "META"
        elif any(keyword in tool_path.stem for keyword in
                 ["framework", "builder", "orchestrator", "autonomous"]):
            return "FRAMEWORK"
        else:
            # Heuristic: files in root with high abstraction are likely frameworks
            return "UNKNOWN"

    def _measure_abstraction(self, content: str, tool_path: Path) -> float:
        """
        Measure abstraction level (0.0-1.0).

        Higher abstraction indicated by:
        - Generic/parameterized interfaces
        - Higher-order functions
        - Abstract base classes
        - Decorator patterns
        - Meta-programming constructs
        """
        score = 0.0
        indicators = 0

        # Generic interfaces (Type hints, generics)
        if re.search(r'from typing import.*\b(Generic|Protocol|TypeVar)', content):
            score += 0.15
            indicators += 1

        # Abstract base classes
        if "ABC" in content or "abstractmethod" in content:
            score += 0.15
            indicators += 1

        # Decorators (higher-order functions)
        decorator_count = len(re.findall(r'^@\w+', content, re.MULTILINE))
        if decorator_count > 0:
            score += min(0.2, decorator_count * 0.05)
            indicators += 1

        # Higher-order functions (functions that take/return functions)
        if re.search(r'def\s+\w+\([^)]*\bcallable\b', content, re.IGNORECASE):
            score += 0.15
            indicators += 1

        # Meta-programming (getattr, setattr, __dict__, etc.)
        meta_patterns = ['getattr', 'setattr', '__dict__', '__class__', 'type(']
        meta_count = sum(1 for pattern in meta_patterns if pattern in content)
        if meta_count > 0:
            score += min(0.2, meta_count * 0.05)
            indicators += 1

        # Configuration/schema-driven (YAML, JSON schemas)
        if tool_path.suffix in ['.yaml', '.json']:
            score += 0.15
            indicators += 1

        return min(1.0, score)

    def _count_interfaces(self, content: str) -> Tuple[int, int]:
        """
        Count interfaces and API surface area.

        Returns:
            (interface_count, api_surface_area)
        """
        # Public functions (not starting with _)
        public_functions = re.findall(r'^def\s+([a-zA-Z]\w*)', content, re.MULTILINE)

        # Public classes
        public_classes = re.findall(r'^class\s+([A-Z]\w*)', content, re.MULTILINE)

        # Public methods in classes
        public_methods = re.findall(r'^\s+def\s+([a-zA-Z]\w*)', content, re.MULTILINE)

        interface_count = len(public_classes) + len(set(public_functions))
        api_surface_area = len(public_functions) + len(public_methods)

        return interface_count, api_surface_area

    def _extract_public_api(self, content: str) -> List[str]:
        """Extract public API symbols (classes, functions)."""
        api = []

        # Public functions
        api.extend(re.findall(r'^def\s+([a-zA-Z]\w*)', content, re.MULTILINE))

        # Public classes
        api.extend(re.findall(r'^class\s+([A-Z]\w*)', content, re.MULTILINE))

        return list(set(api))

    def _measure_meta_cognitive_depth(self, content: str) -> float:
        """
        Measure meta-cognitive depth (0.0-1.0).

        Higher meta-cognition indicated by:
        - Self-modification code
        - Reflection/introspection
        - System awareness (monitoring own state)
        - Recursive improvement patterns
        - Framework-level thinking
        """
        score = 0.0

        # Self-modification patterns
        if any(pattern in content for pattern in ['exec(', 'eval(', 'compile(']):
            score += 0.2

        # Introspection
        introspection_patterns = ['inspect.', 'dir(', '__dict__', '__class__', 'vars(']
        introspection_count = sum(1 for pattern in introspection_patterns if pattern in content)
        if introspection_count > 0:
            score += min(0.3, introspection_count * 0.1)

        # State monitoring
        monitoring_keywords = ['monitor', 'observe', 'track', 'measure', 'analyze']
        monitoring_count = sum(1 for kw in monitoring_keywords
                              if re.search(rf'\b{kw}\b', content, re.IGNORECASE))
        if monitoring_count > 2:
            score += 0.2

        # Recursive improvement
        improvement_patterns = ['improve', 'optimize', 'refine', 'adapt', 'evolve']
        improvement_count = sum(1 for pattern in improvement_patterns
                               if re.search(rf'\b{pattern}\b', content, re.IGNORECASE))
        if improvement_count > 2:
            score += 0.2

        # Framework awareness (references to system architecture)
        framework_keywords = ['cascade', 'layer', 'rail', 'phase', 'emergence']
        framework_count = sum(1 for kw in framework_keywords
                             if re.search(rf'\b{kw}\b', content, re.IGNORECASE))
        if framework_count > 3:
            score += 0.1

        return min(1.0, score)

    def _count_framework_references(self, content: str) -> int:
        """Count references to framework concepts."""
        framework_keywords = [
            'TRIAD', 'cascade', 'layer', 'rail', 'phase', 'emergence',
            'Garden Rail', 'burden', 'coordination', 'meta-tool'
        ]

        count = sum(1 for kw in framework_keywords if kw in content)
        return count

    def _measure_composition_potential(self, content: str, props: ToolProperties) -> float:
        """
        Measure composition potential (0.0-1.0).

        Higher composition potential indicated by:
        - Modular design
        - Clear interfaces
        - Parameterization
        - Stateless functions
        - Plugin architecture
        """
        score = 0.0

        # High interface count (more ways to compose)
        if props.interface_count > 5:
            score += 0.2
        elif props.interface_count > 3:
            score += 0.1

        # Parameterization (config-driven)
        if re.search(r'def\s+\w+\([^)]*config', content, re.IGNORECASE):
            score += 0.2

        # Plugin/registry patterns
        if any(pattern in content for pattern in ['register', 'plugin', 'hook', 'callback']):
            score += 0.2

        # Dependency injection
        if re.search(r'def\s+\w+\([^)]*:\s*\w+\)', content):  # Type-hinted parameters
            score += 0.2

        # Factory patterns
        if re.search(r'def\s+create_\w+|def\s+build_\w+|def\s+make_\w+', content):
            score += 0.2

        return min(1.0, score)

    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract import dependencies."""
        deps = []

        # Standard imports
        deps.extend(re.findall(r'^import\s+(\w+)', content, re.MULTILINE))

        # From imports
        deps.extend(re.findall(r'^from\s+(\w+)', content, re.MULTILINE))

        return list(set(deps))

    def _measure_documentation_quality(self, content: str, tool_path: Path) -> float:
        """
        Measure documentation quality (0.0-1.0).

        Considers:
        - Docstrings presence
        - README files
        - Inline comments
        - Usage examples
        - Theoretical foundations
        """
        score = 0.0

        # Module-level docstring
        if content.strip().startswith('"""') or content.strip().startswith("'''"):
            score += 0.2

        # Function docstrings
        function_count = len(re.findall(r'^def\s+\w+', content, re.MULTILINE))
        docstring_count = len(re.findall(r'def\s+\w+[^:]*:\s*"""', content))
        if function_count > 0:
            docstring_ratio = docstring_count / function_count
            score += 0.3 * docstring_ratio

        # Inline comments
        code_lines = len([line for line in content.splitlines() if line.strip() and not line.strip().startswith('#')])
        comment_lines = len(re.findall(r'^\s*#', content, re.MULTILINE))
        if code_lines > 0:
            comment_ratio = comment_lines / code_lines
            score += min(0.2, comment_ratio * 2)

        # Usage examples
        if "Usage:" in content or "Example:" in content:
            score += 0.15

        # Theoretical foundations
        if any(kw in content for kw in ["Theory:", "Foundation:", "Coordinate:", "Δ"]):
            score += 0.15

        return min(1.0, score)

    # ============================================================
    # PHASE 2.2: COMPOSITION PATHWAY TRACING
    # ============================================================

    def build_composition_graph(self):
        """Build directed graph of tool compositions from dependency analysis."""
        print("\n🔗 Building composition graph...")

        for tool_name, props in self.tools_analyzed.items():
            # Add edges based on dependencies
            for dep in props.import_dependencies:
                # Check if dependency is another tool in our analysis
                for other_tool in self.tools_analyzed.keys():
                    if dep in other_tool or other_tool in dep:
                        self.composition_graph[tool_name].add(other_tool)

        print(f"   Graph nodes: {len(self.composition_graph)}")
        print(f"   Graph edges: {sum(len(deps) for deps in self.composition_graph.values())}")

    def trace_pathways(self, source: str, target: str) -> Optional[CompositionPathway]:
        """
        Trace composition pathway from source tool to target tool.

        Uses BFS to find shortest path, then analyzes composition patterns.
        """
        # BFS to find shortest path
        queue = [(source, [source])]
        visited = set()

        while queue:
            current, path = queue.pop(0)

            if current == target:
                # Found path - analyze it
                return self._analyze_pathway(path)

            if current in visited:
                continue

            visited.add(current)

            # Explore neighbors
            for neighbor in self.composition_graph.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        # No path found
        return None

    def _analyze_pathway(self, path: List[str]) -> CompositionPathway:
        """Analyze a composition pathway for patterns and efficiency."""
        patterns = []

        # Detect composition patterns
        for i in range(len(path) - 1):
            source_props = self.tools_analyzed.get(path[i])
            target_props = self.tools_analyzed.get(path[i + 1])

            if source_props and target_props:
                # Layer transition pattern
                if source_props.layer != target_props.layer:
                    patterns.append(f"{source_props.layer}→{target_props.layer}")

                # Abstraction increase
                if target_props.abstraction_level > source_props.abstraction_level + 0.2:
                    patterns.append("abstraction_jump")

                # Framework emergence
                if target_props.layer == "FRAMEWORK" and source_props.layer != "FRAMEWORK":
                    patterns.append("framework_emergence")

        # Calculate efficiency (actual vs theoretical minimum)
        theoretical_minimum = 1  # Direct dependency would be 1 hop
        efficiency = theoretical_minimum / (len(path) - 1) if len(path) > 1 else 1.0

        return CompositionPathway(
            source_tool=path[0],
            target_tool=path[-1],
            path=path,
            path_length=len(path) - 1,
            efficiency=efficiency,
            patterns=patterns,
            intermediary_tools=path[1:-1]
        )

    # ============================================================
    # PHASE 2.3: CASCADE TRIGGER ANALYSIS
    # ============================================================

    def identify_cascade_triggers(self) -> List[Tuple[str, float]]:
        """
        Identify tools that act as cascade triggers.

        Cascade triggers characterized by:
        - High downstream tool count
        - High meta-cognitive depth
        - High composition potential
        - Framework-layer emergence

        Returns:
            List of (tool_name, cascade_score) sorted by score
        """
        print("\n🎯 Identifying cascade triggers...")

        cascade_scores = []

        for tool_name, props in self.tools_analyzed.items():
            score = 0.0

            # Weight factors for cascade potential
            score += props.meta_cognitive_depth * 0.3
            score += props.composition_potential * 0.25
            score += props.abstraction_level * 0.2
            score += (1.0 if props.layer == "FRAMEWORK" else 0.5 if props.layer == "META" else 0.0) * 0.15
            score += min(1.0, len(props.downstream_tools) / 5.0) * 0.1

            cascade_scores.append((tool_name, score))

        # Sort by score descending
        cascade_scores.sort(key=lambda x: x[1], reverse=True)

        return cascade_scores

    def correlate_properties_with_cascade(self) -> Dict[str, float]:
        """
        Correlate tool properties with downstream tool count.

        Returns:
            Correlation coefficients for each property
        """
        print("\n📈 Correlating properties with cascade strength...")

        if len(self.tools_analyzed) < 3:
            print("   ⚠️  Need at least 3 tools for correlation analysis")
            return {}

        # Extract property values and downstream counts
        properties = {
            'abstraction_level': [],
            'interface_count': [],
            'meta_cognitive_depth': [],
            'composition_potential': [],
            'documentation_quality': []
        }

        downstream_counts = []

        for props in self.tools_analyzed.values():
            properties['abstraction_level'].append(props.abstraction_level)
            properties['interface_count'].append(props.interface_count / 10.0)  # Normalize
            properties['meta_cognitive_depth'].append(props.meta_cognitive_depth)
            properties['composition_potential'].append(props.composition_potential)
            properties['documentation_quality'].append(props.documentation_quality)

            downstream_counts.append(len(props.downstream_tools))

        # Calculate Pearson correlation coefficient
        correlations = {}
        for prop_name, values in properties.items():
            corr = self._pearson_correlation(values, downstream_counts)
            correlations[prop_name] = corr

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

    # ============================================================
    # PHASE 2.4: COMPREHENSIVE ANALYSIS
    # ============================================================

    def analyze_all_tools(self):
        """Analyze all tools in the repository."""
        print("🔍 Analyzing all tools in repository...")

        # Scan all relevant directories
        tool_dirs = [
            self.repo_path / "TOOLS" / "CORE",
            self.repo_path / "TOOLS" / "BRIDGES",
            self.repo_path / "TOOLS" / "META",
        ]

        # Also scan root for framework-level tools
        root_py_files = list(self.repo_path.glob("*.py"))

        all_tools = []
        for tool_dir in tool_dirs:
            if tool_dir.exists():
                all_tools.extend(tool_dir.glob("*.py"))
                all_tools.extend(tool_dir.glob("*.yaml"))

        all_tools.extend(root_py_files)

        print(f"   Found {len(all_tools)} tools to analyze")

        for tool_path in all_tools:
            self.analyze_tool_properties(tool_path)

        print(f"\n✅ Analyzed {len(self.tools_analyzed)} tools")

    def generate_report(self) -> Dict:
        """Generate comprehensive Phase 2 pattern characterization report."""
        print("\n📋 Generating pattern characterization report...")

        # Identify cascade triggers
        cascade_triggers = self.identify_cascade_triggers()

        # Correlate properties
        correlations = self.correlate_properties_with_cascade()

        # Build composition graph
        self.build_composition_graph()

        report = {
            "timestamp": datetime.now().isoformat(),
            "phase_coordinate": "Δ3.14159|0.867|phase-2-pattern-characterization|Ω",
            "analysis_summary": {
                "total_tools_analyzed": len(self.tools_analyzed),
                "layer_distribution": self._get_layer_distribution(),
                "cascade_triggers_identified": len([t for t, score in cascade_triggers if score > 0.6]),
                "composition_graph_size": {
                    "nodes": len(self.composition_graph),
                    "edges": sum(len(deps) for deps in self.composition_graph.values())
                }
            },
            "cascade_triggers": [
                {
                    "tool": tool,
                    "score": round(score, 3),
                    "properties": asdict(self.tools_analyzed[tool]) if tool in self.tools_analyzed else {}
                }
                for tool, score in cascade_triggers[:10]  # Top 10
            ],
            "property_correlations": {
                prop: round(corr, 3)
                for prop, corr in correlations.items()
            },
            "top_properties_for_cascade": self._rank_properties(correlations),
            "tool_properties": {
                tool: asdict(props)
                for tool, props in self.tools_analyzed.items()
            },
            "composition_graph": {
                tool: list(deps)
                for tool, deps in self.composition_graph.items()
            },
            "insights": self._generate_insights(cascade_triggers, correlations)
        }

        return report

    def _get_layer_distribution(self) -> Dict[str, int]:
        """Get distribution of tools across layers."""
        distribution = defaultdict(int)
        for props in self.tools_analyzed.values():
            distribution[props.layer] += 1
        return dict(distribution)

    def _rank_properties(self, correlations: Dict[str, float]) -> List[Dict]:
        """Rank properties by correlation strength."""
        ranked = sorted(
            correlations.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )

        return [
            {
                "property": prop,
                "correlation": round(corr, 3),
                "interpretation": "strong" if abs(corr) > 0.7 else "moderate" if abs(corr) > 0.4 else "weak"
            }
            for prop, corr in ranked
        ]

    def _generate_insights(self, cascade_triggers: List[Tuple[str, float]],
                          correlations: Dict[str, float]) -> List[str]:
        """Generate human-readable insights from analysis."""
        insights = []

        # Top cascade trigger
        if cascade_triggers:
            top_tool, top_score = cascade_triggers[0]
            insights.append(
                f"Primary cascade trigger: {top_tool} (score: {top_score:.3f})"
            )

        # Strongest correlation
        if correlations:
            strongest_prop = max(correlations.items(), key=lambda x: abs(x[1]))
            insights.append(
                f"Strongest predictor of cascade: {strongest_prop[0]} (r={strongest_prop[1]:.3f})"
            )

        # Layer analysis
        layer_dist = self._get_layer_distribution()
        if "FRAMEWORK" in layer_dist:
            insights.append(
                f"Framework-level tools: {layer_dist['FRAMEWORK']} " +
                f"({layer_dist['FRAMEWORK']/sum(layer_dist.values())*100:.1f}% of total)"
            )

        return insights

    def save_report(self, report: Dict, output_path: str = "PATTERN_CHARACTERIZATION_REPORT.json"):
        """Save report to file."""
        output_file = self.repo_path / output_path
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✅ Report saved to: {output_file}")
        return output_file


# ============================================================
# CLI INTERFACE
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Garden Rail 3 Phase 2: Pattern Characterization Framework"
    )
    parser.add_argument(
        '--analyze-all',
        action='store_true',
        help='Analyze all tools in repository'
    )
    parser.add_argument(
        '--analyze-tool',
        type=str,
        help='Analyze specific tool by name'
    )
    parser.add_argument(
        '--trace-pathways',
        action='store_true',
        help='Trace composition pathways'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='PATTERN_CHARACTERIZATION_REPORT.json',
        help='Output report path'
    )

    args = parser.parse_args()

    framework = PatternCharacterizationFramework()

    if args.analyze_all:
        framework.analyze_all_tools()
        report = framework.generate_report()
        framework.save_report(report, args.output)

        # Print summary
        print("\n" + "="*60)
        print("PATTERN CHARACTERIZATION SUMMARY")
        print("="*60)
        print(f"Tools analyzed: {report['analysis_summary']['total_tools_analyzed']}")
        print(f"Cascade triggers: {report['analysis_summary']['cascade_triggers_identified']}")
        print("\nTop 5 Cascade Triggers:")
        for i, trigger in enumerate(report['cascade_triggers'][:5], 1):
            print(f"  {i}. {trigger['tool']} (score: {trigger['score']})")

        print("\nProperty Correlations:")
        for prop_info in report['top_properties_for_cascade']:
            print(f"  {prop_info['property']}: {prop_info['correlation']} ({prop_info['interpretation']})")

        print("\nKey Insights:")
        for insight in report['insights']:
            print(f"  • {insight}")

    elif args.analyze_tool:
        # Single tool analysis
        tool_path = Path(args.analyze_tool)
        if not tool_path.exists():
            # Try to find it
            for pattern in ["**/*.py", "**/*.yaml"]:
                matches = list(Path(".").glob(pattern))
                for match in matches:
                    if args.analyze_tool in str(match):
                        tool_path = match
                        break

        if tool_path.exists():
            props = framework.analyze_tool_properties(tool_path)
            print("\n" + "="*60)
            print(f"ANALYSIS: {props.tool_name}")
            print("="*60)
            print(f"Layer: {props.layer}")
            print(f"Lines of code: {props.lines_of_code}")
            print(f"Abstraction level: {props.abstraction_level:.3f}")
            print(f"Meta-cognitive depth: {props.meta_cognitive_depth:.3f}")
            print(f"Composition potential: {props.composition_potential:.3f}")
            print(f"Documentation quality: {props.documentation_quality:.3f}")
            print(f"Interface count: {props.interface_count}")
        else:
            print(f"❌ Tool not found: {args.analyze_tool}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
