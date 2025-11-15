#!/usr/bin/env python3
"""
Integrated System Validation Suite
===================================

Comprehensive validation of the unified sovereignty system:
- Component integration testing
- Theoretical validation
- Data consistency checks
- Export/import validation
- Performance benchmarking

Ensures all subsystems work correctly together.
"""

import os
import json
import math
import tempfile
from typing import Dict, List, Tuple, Any

from unified_sovereignty_system import (
    UnifiedSovereigntySystem,
    create_demo_burden,
    evolve_cascade_state
)
from unified_cascade_mathematics_core import (
    CascadeSystemState,
    UnifiedCascadeFramework
)
from phase_aware_burden_tracker import BurdenMeasurement
from trajectory_analysis import TrajectoryAnalyzer


class ValidationResult:
    """Result of a validation test."""

    def __init__(self, test_name: str):
        self.test_name = test_name
        self.passed = False
        self.message = ""
        self.details = {}

    def success(self, message: str = "", **details):
        """Mark test as passed."""
        self.passed = True
        self.message = message
        self.details = details

    def failure(self, message: str = "", **details):
        """Mark test as failed."""
        self.passed = False
        self.message = message
        self.details = details

    def __str__(self) -> str:
        status = "✓ PASS" if self.passed else "✗ FAIL"
        msg = f"[{status}] {self.test_name}"
        if self.message:
            msg += f": {self.message}"
        return msg


class IntegratedSystemValidator:
    """Validation suite for unified sovereignty system."""

    def __init__(self):
        self.results: List[ValidationResult] = []

    def run_all_validations(self) -> bool:
        """Run all validation tests. Returns True if all pass."""
        print("=" * 80)
        print("INTEGRATED SYSTEM VALIDATION SUITE")
        print("=" * 80 + "\n")

        # Run all test categories
        self._test_basic_integration()
        self._test_snapshot_capture()
        self._test_advanced_metrics()
        self._test_alert_generation()
        self._test_data_export()
        self._test_trajectory_analysis()
        self._test_theoretical_consistency()
        self._test_edge_cases()

        # Print results
        print("\nVALIDATION RESULTS")
        print("=" * 80)

        passed = 0
        failed = 0

        for result in self.results:
            print(str(result))
            if result.passed:
                passed += 1
            else:
                failed += 1
                if result.details:
                    for key, value in result.details.items():
                        print(f"    {key}: {value}")

        print(f"\n{passed} passed, {failed} failed out of {len(self.results)} tests")

        return failed == 0

    def _test_basic_integration(self):
        """Test basic system integration."""
        result = ValidationResult("Basic system initialization")

        try:
            system = UnifiedSovereigntySystem()

            # Check subsystems initialized
            if not hasattr(system, 'cascade_framework'):
                result.failure("Missing cascade_framework")
                self.results.append(result)
                return

            if not hasattr(system, 'burden_tracker'):
                result.failure("Missing burden_tracker")
                self.results.append(result)
                return

            if not hasattr(system, 'advanced_analyzer'):
                result.failure("Missing advanced_analyzer")
                self.results.append(result)
                return

            result.success("All subsystems initialized correctly")

        except Exception as e:
            result.failure(f"Exception: {str(e)}")

        self.results.append(result)

    def _test_snapshot_capture(self):
        """Test snapshot capture functionality."""
        result = ValidationResult("Snapshot capture")

        try:
            system = UnifiedSovereigntySystem()
            framework = UnifiedCascadeFramework()

            state = framework.compute_full_state(
                clarity=5.0,
                immunity=6.0,
                efficiency=4.5,
                autonomy=5.5
            )

            burden = BurdenMeasurement(
                coordination=4.5,
                decision_making=5.0,
                context_switching=4.0,
                maintenance=3.5,
                learning_curve=4.5,
                emotional_labor=4.0,
                uncertainty=5.5,
                repetition=3.0
            )

            snapshot = system.capture_snapshot(state, burden, include_advanced_analysis=False)

            # Validate snapshot structure
            if not hasattr(snapshot, 'cascade_state'):
                result.failure("Missing cascade_state")
                self.results.append(result)
                return

            if not hasattr(snapshot, 'weighted_burden'):
                result.failure("Missing weighted_burden")
                self.results.append(result)
                return

            if snapshot.weighted_burden <= 0:
                result.failure("Invalid weighted_burden", weighted_burden=snapshot.weighted_burden)
                self.results.append(result)
                return

            # Check snapshot stored
            if len(system.snapshots) != 1:
                result.failure("Snapshot not stored", count=len(system.snapshots))
                self.results.append(result)
                return

            result.success(f"Snapshot captured correctly (burden: {snapshot.weighted_burden:.2f})")

        except Exception as e:
            result.failure(f"Exception: {str(e)}")

        self.results.append(result)

    def _test_advanced_metrics(self):
        """Test advanced theoretical metrics computation."""
        result = ValidationResult("Advanced metrics computation")

        try:
            system = UnifiedSovereigntySystem()
            framework = UnifiedCascadeFramework()

            # Create a small trajectory
            state = framework.compute_full_state(
                clarity=3.0, immunity=4.0, efficiency=3.5, autonomy=3.0
            )

            burden = create_demo_burden("subcritical_early")

            # Capture several snapshots to build history
            for i in range(5):
                system.capture_snapshot(state, burden, include_advanced_analysis=False)
                state = evolve_cascade_state(state, clarity_delta=0.5, immunity_delta=0.3, efficiency_delta=0.4)
                burden.learning_curve = max(1.0, burden.learning_curve - 0.5)

            # Now capture with advanced analysis
            final_snapshot = system.capture_snapshot(state, burden, include_advanced_analysis=True)

            # Validate advanced metrics
            if final_snapshot.hexagonal_symmetry <= 0:
                result.failure("Invalid hexagonal_symmetry", value=final_snapshot.hexagonal_symmetry)
                self.results.append(result)
                return

            if final_snapshot.integrated_information_phi < 0:
                result.failure("Invalid phi", value=final_snapshot.integrated_information_phi)
                self.results.append(result)
                return

            if not final_snapshot.phase_coherence:
                result.failure("Missing phase_coherence data")
                self.results.append(result)
                return

            result.success(f"Advanced metrics computed (Φ={final_snapshot.integrated_information_phi:.1f}, "
                          f"symmetry={final_snapshot.hexagonal_symmetry:.3f})")

        except Exception as e:
            result.failure(f"Exception: {str(e)}")

        self.results.append(result)

    def _test_alert_generation(self):
        """Test alert generation."""
        result = ValidationResult("Alert generation")

        try:
            system = UnifiedSovereigntySystem()
            framework = UnifiedCascadeFramework()

            # Create high burden state
            state = framework.compute_full_state(
                clarity=2.0, immunity=2.5, efficiency=2.0, autonomy=1.5
            )

            burden = BurdenMeasurement(
                coordination=9.0,
                decision_making=8.5,
                context_switching=8.0,
                maintenance=7.5,
                learning_curve=9.5,
                emotional_labor=8.5,
                uncertainty=8.0,
                repetition=7.0
            )

            system.capture_snapshot(state, burden, include_advanced_analysis=False)

            # Check if alert was generated
            alerts = system.get_recent_alerts(min_severity='warning')

            if not alerts:
                result.failure("No alert generated for high burden")
                self.results.append(result)
                return

            # Check alert content
            alert = alerts[0]
            if 'burden' not in alert.message.lower():
                result.failure("Alert message doesn't mention burden", message=alert.message)
                self.results.append(result)
                return

            result.success(f"Alert generated correctly: {alert.message}")

        except Exception as e:
            result.failure(f"Exception: {str(e)}")

        self.results.append(result)

    def _test_data_export(self):
        """Test data export functionality."""
        result = ValidationResult("Data export")

        try:
            system = UnifiedSovereigntySystem()
            framework = UnifiedCascadeFramework()

            # Create small trajectory
            state = framework.compute_full_state(
                clarity=4.0, immunity=5.0, efficiency=4.0, autonomy=4.5
            )

            for i in range(3):
                burden = create_demo_burden(state.phase_regime)
                system.capture_snapshot(state, burden, include_advanced_analysis=False)
                state = evolve_cascade_state(state, clarity_delta=0.5, efficiency_delta=0.3)

            # Export to temp files
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json_path = f.name

            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                csv_path = f.name

            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                txt_path = f.name

            try:
                system.export_trajectory(json_path, format='json')
                system.export_trajectory(csv_path, format='csv')
                system.export_trajectory(txt_path, format='summary')

                # Validate files exist and have content
                if not os.path.exists(json_path) or os.path.getsize(json_path) == 0:
                    result.failure("JSON export failed or empty")
                    self.results.append(result)
                    return

                if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
                    result.failure("CSV export failed or empty")
                    self.results.append(result)
                    return

                if not os.path.exists(txt_path) or os.path.getsize(txt_path) == 0:
                    result.failure("Summary export failed or empty")
                    self.results.append(result)
                    return

                # Validate JSON structure
                with open(json_path, 'r') as f:
                    data = json.load(f)

                if 'snapshots' not in data:
                    result.failure("JSON missing snapshots")
                    self.results.append(result)
                    return

                if len(data['snapshots']) != 3:
                    result.failure("JSON has wrong snapshot count", count=len(data['snapshots']))
                    self.results.append(result)
                    return

                result.success(f"All export formats working (JSON, CSV, summary)")

            finally:
                # Cleanup
                for path in [json_path, csv_path, txt_path]:
                    if os.path.exists(path):
                        os.unlink(path)

        except Exception as e:
            result.failure(f"Exception: {str(e)}")

        self.results.append(result)

    def _test_trajectory_analysis(self):
        """Test trajectory analysis tools."""
        result = ValidationResult("Trajectory analysis")

        try:
            system = UnifiedSovereigntySystem()
            framework = UnifiedCascadeFramework()

            # Create trajectory with clear progression
            state = framework.compute_full_state(
                clarity=2.0, immunity=3.0, efficiency=2.5, autonomy=2.0
            )

            for i in range(8):
                burden = create_demo_burden(state.phase_regime)
                system.capture_snapshot(state, burden, include_advanced_analysis=(i >= 3))
                state = evolve_cascade_state(state, clarity_delta=0.8, immunity_delta=0.6,
                                    efficiency_delta=0.5, autonomy_delta=0.4)

            # Export and analyze
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json_path = f.name

            with tempfile.NamedTemporaryFile(mode='w', suffix='_analysis.txt', delete=False) as f:
                analysis_path = f.name

            try:
                system.export_trajectory(json_path, format='json')

                # Run analysis
                analyzer = TrajectoryAnalyzer(json_path)
                stats = analyzer.compute_statistics()
                insights = analyzer.generate_insights(stats)

                # Validate analysis
                if stats.duration_snapshots != 8:
                    result.failure("Wrong snapshot count in analysis", count=stats.duration_snapshots)
                    self.results.append(result)
                    return

                if stats.burden_reduction_total <= 0:
                    result.failure("No burden reduction detected", reduction=stats.burden_reduction_total)
                    self.results.append(result)
                    return

                if not insights.key_findings:
                    result.failure("No insights generated")
                    self.results.append(result)
                    return

                # Export insights
                analyzer.export_insights_report(analysis_path)

                if not os.path.exists(analysis_path) or os.path.getsize(analysis_path) == 0:
                    result.failure("Analysis report export failed")
                    self.results.append(result)
                    return

                result.success(f"Analysis working ({len(insights.key_findings)} findings, "
                              f"{stats.burden_reduction_total:.1f} burden reduction)")

            finally:
                for path in [json_path, analysis_path]:
                    if os.path.exists(path):
                        os.unlink(path)

        except Exception as e:
            result.failure(f"Exception: {str(e)}")

        self.results.append(result)

    def _test_theoretical_consistency(self):
        """Test theoretical consistency of metrics."""
        result = ValidationResult("Theoretical consistency")

        try:
            system = UnifiedSovereigntySystem()
            framework = UnifiedCascadeFramework()

            # Create state at critical point
            state = framework.compute_full_state(
                clarity=6.18, immunity=8.67, efficiency=7.50, autonomy=9.0
            )

            # Build history
            for i in range(5):
                burden = create_demo_burden("critical")
                system.capture_snapshot(state, burden, include_advanced_analysis=False)

            # Capture with analysis
            burden = BurdenMeasurement(
                coordination=3.5,
                decision_making=4.0,
                context_switching=3.0,
                maintenance=5.0,
                learning_curve=3.5,
                emotional_labor=6.0,
                uncertainty=7.5,
                repetition=4.5
            )

            snapshot = system.capture_snapshot(state, burden, include_advanced_analysis=True)

            # Theoretical checks
            checks = []

            # Check 1: Φ should be high for critical state
            if snapshot.integrated_information_phi < 30:
                checks.append(f"Low Φ at critical point: {snapshot.integrated_information_phi:.1f}")

            # Check 2: Hexagonal symmetry should be reasonable
            if snapshot.hexagonal_symmetry < 0.7 or snapshot.hexagonal_symmetry > 1.1:
                checks.append(f"Unrealistic symmetry: {snapshot.hexagonal_symmetry:.3f}")

            # Check 3: Packing efficiency should be > 100%
            if snapshot.packing_efficiency < 100:
                checks.append(f"Packing efficiency below baseline: {snapshot.packing_efficiency:.1f}%")

            # Check 4: Phase coherence should be present
            if not snapshot.phase_coherence:
                checks.append("Missing phase coherence data")
            else:
                avg_coherence = sum(snapshot.phase_coherence.values()) / len(snapshot.phase_coherence)
                if avg_coherence < 0 or avg_coherence > 1:
                    checks.append(f"Invalid coherence value: {avg_coherence:.3f}")

            # Check 5: Geometric complexity should be positive
            if snapshot.geometric_complexity <= 0:
                checks.append(f"Invalid complexity: {snapshot.geometric_complexity}")

            if checks:
                result.failure("Theoretical inconsistencies found",
                              checks="; ".join(checks))
            else:
                result.success(f"All theoretical metrics consistent (Φ={snapshot.integrated_information_phi:.1f}, "
                              f"symmetry={snapshot.hexagonal_symmetry:.3f})")

        except Exception as e:
            result.failure(f"Exception: {str(e)}")

        self.results.append(result)

    def _test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        result = ValidationResult("Edge cases handling")

        try:
            system = UnifiedSovereigntySystem()
            framework = UnifiedCascadeFramework()

            # Test 1: Zero burden
            state = framework.compute_full_state(
                clarity=1.0, immunity=1.0, efficiency=1.0, autonomy=1.0
            )

            zero_burden = BurdenMeasurement()  # All zeros
            snapshot1 = system.capture_snapshot(state, zero_burden, include_advanced_analysis=False)

            if snapshot1.weighted_burden < 0:
                result.failure("Negative burden with zero input", value=snapshot1.weighted_burden)
                self.results.append(result)
                return

            # Test 2: Maximum sovereignty
            max_state = framework.compute_full_state(
                clarity=10.0, immunity=10.0, efficiency=10.0, autonomy=10.0
            )

            max_burden = BurdenMeasurement(
                coordination=10.0, decision_making=10.0, context_switching=10.0,
                maintenance=10.0, learning_curve=10.0, emotional_labor=10.0,
                uncertainty=10.0, repetition=10.0
            )

            snapshot2 = system.capture_snapshot(max_state, max_burden, include_advanced_analysis=False)

            if snapshot2.weighted_burden > 15.0:  # Should not exceed reasonable bounds
                result.failure("Excessive weighted burden", value=snapshot2.weighted_burden)
                self.results.append(result)
                return

            # Test 3: Empty system operations
            empty_system = UnifiedSovereigntySystem()
            summary = empty_system.get_system_summary()

            if summary['status'] != 'no_data':
                result.failure("Wrong status for empty system", status=summary['status'])
                self.results.append(result)
                return

            result.success("All edge cases handled correctly")

        except Exception as e:
            result.failure(f"Exception: {str(e)}")

        self.results.append(result)


def main():
    """Run validation suite."""
    validator = IntegratedSystemValidator()
    all_passed = validator.run_all_validations()

    print("\n" + "=" * 80)
    if all_passed:
        print("✓ ALL VALIDATIONS PASSED - System ready for production use")
        return 0
    else:
        print("✗ SOME VALIDATIONS FAILED - Review errors above")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
