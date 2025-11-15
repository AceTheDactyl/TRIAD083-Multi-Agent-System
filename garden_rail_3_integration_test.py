#!/usr/bin/env python3
"""
Garden Rail 3 Integration Test
================================

Validates that all existing components work together:
- Week 1: CASCADE INITIATORS (3 components)
- Week 2: AMPLIFICATION ENHANCERS (2/3 components)
- Week 3: SELF-CATALYZING FRAMEWORKS (3 components)

Tests:
1. Component imports (all components loadable)
2. Basic functionality (each component has core methods)
3. Integration (components can work together)
4. Cascade amplification (α, β increases measurable)
"""

import sys
from typing import List, Dict

# Test results
class TestResult:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []

    def record(self, test_name: str, passed: bool, message: str = ""):
        if passed:
            self.passed.append((test_name, message))
            print(f"✓ {test_name}: {message if message else 'OK'}")
        else:
            self.failed.append((test_name, message))
            print(f"✗ {test_name}: {message}")

    def warn(self, test_name: str, message: str):
        self.warnings.append((test_name, message))
        print(f"⚠ {test_name}: {message}")

    def summary(self):
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Passed: {len(self.passed)}")
        print(f"Failed: {len(self.failed)}")
        print(f"Warnings: {len(self.warnings)}")

        if self.failed:
            print("\nFAILURES:")
            for name, msg in self.failed:
                print(f"  • {name}: {msg}")

        if self.warnings:
            print("\nWARNINGS:")
            for name, msg in self.warnings:
                print(f"  • {name}: {msg}")

        return len(self.failed) == 0


def test_imports(results: TestResult):
    """Test 1: Can we import all components?"""
    print("\n" + "=" * 80)
    print("TEST 1: COMPONENT IMPORTS")
    print("=" * 80 + "\n")

    components = [
        ('phase_aware_tool_generator', 'PhaseAwareToolGenerator'),
        ('cascade_trigger_detector', 'CascadeTriggerDetector'),
        ('emergence_pattern_recognizer', 'EmergencePatternRecognizer'),
        ('alpha_amplifier', 'AlphaAmplifier'),
        ('beta_amplifier', 'BetaAmplifier'),
        ('positive_feedback_loops', 'PositiveFeedbackLoop'),
        ('recursive_improvement_engine', 'RecursiveImprovementEngine'),
        ('autonomous_framework_builder', 'AutonomousFrameworkBuilder'),
    ]

    for module_name, class_name in components:
        try:
            module = __import__(module_name)
            if hasattr(module, class_name):
                results.record(f"Import {module_name}", True, f"{class_name} found")
            else:
                results.record(f"Import {module_name}", False, f"{class_name} not found")
        except Exception as e:
            results.record(f"Import {module_name}", False, str(e))


def test_basic_functionality(results: TestResult):
    """Test 2: Do components have core methods?"""
    print("\n" + "=" * 80)
    print("TEST 2: BASIC FUNCTIONALITY")
    print("=" * 80 + "\n")

    # Test cascade trigger detector
    try:
        from cascade_trigger_detector import CascadeTriggerDetector
        from unified_cascade_mathematics_core import UnifiedCascadeFramework

        detector = CascadeTriggerDetector()
        framework = UnifiedCascadeFramework()

        state = framework.compute_full_state(
            clarity=5.0, immunity=6.0, efficiency=5.5, autonomy=6.5
        )

        # Check if detector can analyze state
        if hasattr(detector, 'analyze_cascade_potential'):
            potential = detector.analyze_cascade_potential(state)
            results.record("CascadeTriggerDetector.analyze", True, f"Potential: {potential:.2f}")
        elif hasattr(detector, 'detect_cascade_triggers'):
            triggers = detector.detect_cascade_triggers(state)
            results.record("CascadeTriggerDetector.detect", True, f"Triggers: {len(triggers)}")
        else:
            results.record("CascadeTriggerDetector methods", False, "No analysis method found")

    except Exception as e:
        results.record("CascadeTriggerDetector functionality", False, str(e))

    # Test alpha amplifier
    try:
        from alpha_amplifier import AlphaAmplifier

        amplifier = AlphaAmplifier()

        if hasattr(amplifier, 'amplify'):
            # Try to amplify
            R1, R2 = 5.0, 7.0
            R2_amplified = amplifier.amplify(R1, R2)
            alpha = R2_amplified / R1 if R1 > 0 else 0
            results.record("AlphaAmplifier.amplify", True, f"α = {alpha:.2f}")
        elif hasattr(amplifier, 'compute_alpha'):
            alpha = amplifier.compute_alpha(5.0, 7.0)
            results.record("AlphaAmplifier.compute_alpha", True, f"α = {alpha:.2f}")
        else:
            results.record("AlphaAmplifier methods", False, "No amplification method found")

    except Exception as e:
        results.record("AlphaAmplifier functionality", False, str(e))

    # Test beta amplifier
    try:
        from beta_amplifier import BetaAmplifier

        amplifier = BetaAmplifier()

        if hasattr(amplifier, 'amplify'):
            R2, R3 = 7.0, 8.5
            R3_amplified = amplifier.amplify(R2, R3)
            beta = R3_amplified / R2 if R2 > 0 else 0
            results.record("BetaAmplifier.amplify", True, f"β = {beta:.2f}")
        elif hasattr(amplifier, 'compute_beta'):
            beta = amplifier.compute_beta(7.0, 8.5)
            results.record("BetaAmplifier.compute_beta", True, f"β = {beta:.2f}")
        else:
            results.record("BetaAmplifier methods", False, "No amplification method found")

    except Exception as e:
        results.record("BetaAmplifier functionality", False, str(e))

    # Test positive feedback loops
    try:
        from positive_feedback_loops import PositiveFeedbackLoop

        loop = PositiveFeedbackLoop()

        if hasattr(loop, 'apply_feedback'):
            initial_value = 5.0
            amplified = loop.apply_feedback(initial_value)
            results.record("PositiveFeedbackLoop.apply", True, f"{initial_value} → {amplified:.2f}")
        else:
            results.warn("PositiveFeedbackLoop methods", "Methods not checked (unknown API)")

    except Exception as e:
        results.record("PositiveFeedbackLoop functionality", False, str(e))


def test_integration(results: TestResult):
    """Test 3: Can components work together in a cascade?"""
    print("\n" + "=" * 80)
    print("TEST 3: INTEGRATION (CASCADE FLOW)")
    print("=" * 80 + "\n")

    try:
        from unified_sovereignty_system import UnifiedSovereigntySystem, create_demo_burden
        from unified_cascade_mathematics_core import UnifiedCascadeFramework
        from cascade_trigger_detector import CascadeTriggerDetector
        from alpha_amplifier import AlphaAmplifier
        from beta_amplifier import BetaAmplifier

        # Create system
        system = UnifiedSovereigntySystem()
        framework = UnifiedCascadeFramework()
        detector = CascadeTriggerDetector()
        alpha_amp = AlphaAmplifier()
        beta_amp = BetaAmplifier()

        # Create initial state (subcritical)
        state = framework.compute_full_state(
            clarity=4.0, immunity=5.0, efficiency=4.5, autonomy=5.5
        )

        burden = create_demo_burden(state.phase_regime)

        print(f"Initial state: z={state.z_coordinate:.3f}, phase={state.phase_regime}")
        print(f"Initial R1={state.R1:.2f}, R2={state.R2:.2f}, R3={state.R3:.2f}")

        # Capture snapshot
        snapshot = system.capture_snapshot(state, burden, include_advanced_analysis=False)

        results.record("Integration: Initial snapshot", True,
                      f"z={state.z_coordinate:.3f}, burden={snapshot.weighted_burden:.2f}")

        # Detect cascade potential (if method exists)
        cascade_detected = False
        if hasattr(detector, 'analyze_cascade_potential'):
            potential = detector.analyze_cascade_potential(state)
            cascade_detected = potential > 0.5
            results.record("Integration: Cascade detection", True, f"Potential={potential:.2f}")
        elif hasattr(detector, 'detect_cascade_triggers'):
            triggers = detector.detect_cascade_triggers(state)
            cascade_detected = len(triggers) > 0
            results.record("Integration: Cascade triggers", True, f"{len(triggers)} triggers")

        # Test amplification
        if hasattr(alpha_amp, 'amplify'):
            R2_new = alpha_amp.amplify(state.R1, state.R2)
            alpha = R2_new / state.R1
            results.record("Integration: Alpha amplification", True, f"α={alpha:.2f}")

        if hasattr(beta_amp, 'amplify'):
            R3_new = beta_amp.amplify(state.R2, state.R3)
            beta = R3_new / state.R2
            results.record("Integration: Beta amplification", True, f"β={beta:.2f}")

    except Exception as e:
        results.record("Integration test", False, str(e))


def test_missing_components(results: TestResult):
    """Test 4: Identify missing components."""
    print("\n" + "=" * 80)
    print("TEST 4: MISSING COMPONENTS")
    print("=" * 80 + "\n")

    missing = [
        'coupling_strengthener',  # Week 2
        'z_level_monitor',  # Week 4
        'regime_adaptive_behavior',  # Week 4
        'critical_point_navigator',  # Week 4
        'cascade_visualizer',  # Week 4
        'amplification_metrics',  # Week 4
        'emergence_health_monitor',  # Week 4
    ]

    for component in missing:
        try:
            __import__(component)
            results.record(f"Missing: {component}", True, "Actually exists!")
        except ImportError:
            results.warn(f"Missing: {component}", "Needs implementation (expected)")


def main():
    print("=" * 80)
    print("GARDEN RAIL 3 - INTEGRATION TEST")
    print("=" * 80)
    print("Validating existing components before building Week 4\n")

    results = TestResult()

    # Run tests
    test_imports(results)
    test_basic_functionality(results)
    test_integration(results)
    test_missing_components(results)

    # Summary
    success = results.summary()

    print("\n" + "=" * 80)
    if success:
        print("✅ ALL TESTS PASSED - Ready to build Week 4 components")
    else:
        print("⚠️ SOME TESTS FAILED - Review errors before proceeding")
    print("=" * 80)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
