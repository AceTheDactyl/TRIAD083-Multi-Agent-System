#!/usr/bin/env python3
"""
GARDEN RAIL 3 - LAYER 1 INTEGRATION
Demonstrates cascade detection, pattern recognition, and tool generation

Coordinate: Δ3.14159|0.867|1.000Ω
"""

import sys
sys.path.insert(0, '/mnt/user-data/outputs')

from phase_aware_tool_generator import PhaseAwareToolGenerator, ToolType
from cascade_trigger_detector import CascadeTriggerDetector, SystemState
from emergence_pattern_recognizer import EmergencePatternRecognizer
from datetime import datetime
import time

# Try to import burden_tracker
try:
    sys.path.insert(0, '/mnt/user-data/uploads')
    from burden_tracker_api import BurdenTrackerAPI
    BURDEN_TRACKER_AVAILABLE = True
except ImportError:
    BURDEN_TRACKER_AVAILABLE = False
    print("[INFO] burden_tracker not available, using simulation mode")


class Layer1Integration:
    """
    Integrates all three Layer 1 components for cascade amplification
    
    Flow:
    1. CascadeTriggerDetector monitors system state
    2. When cascade detected, EmergencePatternRecognizer identifies pattern
    3. PhaseAwareToolGenerator creates optimized tools for amplification
    4. Results fed back to pattern recognizer for learning
    """
    
    def __init__(self):
        # Initialize burden tracker if available
        if BURDEN_TRACKER_AVAILABLE:
            self.burden_tracker = BurdenTrackerAPI(z_level=0.867)
        else:
            self.burden_tracker = None
        
        # Initialize Layer 1 components
        self.tool_generator = PhaseAwareToolGenerator(self.burden_tracker)
        self.cascade_detector = CascadeTriggerDetector(self.burden_tracker)
        self.pattern_recognizer = EmergencePatternRecognizer(self.burden_tracker)
        
        print("="*70)
        print("GARDEN RAIL 3 - LAYER 1 CASCADE INITIATORS")
        print("="*70)
        print("\nComponents initialized:")
        print("  ✓ PhaseAwareToolGenerator (hybrid universality theory)")
        print("  ✓ CascadeTriggerDetector (non-normal amplification)")
        print("  ✓ EmergencePatternRecognizer (autocatalytic networks)")
        if self.burden_tracker:
            print(f"  ✓ BurdenTracker (z={self.burden_tracker.tracker.phase_state.z_level:.3f})")
        print()
    
    def simulate_system_evolution(self, steps: int = 20):
        """
        Simulate system evolution through phase regimes
        
        Demonstrates cascade detection, pattern learning, and tool generation
        """
        print("="*70)
        print("SIMULATING SYSTEM EVOLUTION THROUGH PHASE REGIMES")
        print("="*70)
        print()
        
        # Evolve z-level from subcritical to supercritical
        z_levels = [0.80 + (i * 0.005) for i in range(steps)]
        
        for step, z in enumerate(z_levels):
            print(f"\n--- Step {step+1}/{steps}: z = {z:.3f} ---")
            
            # Record system state
            state = SystemState(
                timestamp=datetime.now(),
                z_level=z,
                tool_count=10 + step * 2,
                generation_rate=0.5 + step * 0.2,
                burden_reduction=0.05 + step * 0.02,
                R1_active=True,
                R2_active=(z >= 0.85),
                R3_active=(z >= 0.87)
            )
            self.cascade_detector.record_state(state)
            
            # Check for cascade
            if step > 10:  # Need history to detect
                cascade_signal = self.cascade_detector.detect_cascade()
                
                if cascade_signal:
                    print(f"  🔥 CASCADE DETECTED!")
                    print(f"     Type: {cascade_signal.signal_type}")
                    print(f"     Confidence: {cascade_signal.confidence:.1%}")
                    print(f"     Predicted tools: {cascade_signal.predicted_tools}")
                    print(f"     κ = {cascade_signal.condition_number:.3f} (κc = {cascade_signal.critical_threshold:.3f})")
                    
                    # Generate optimized tool for this cascade
                    if cascade_signal.R2_probability > 0.7:
                        tool_spec = self.tool_generator.generate_tool(
                            purpose="Enable meta-tool cascade amplification",
                            preferred_type=ToolType.BRIDGES,
                            z_override=z
                        )
                        print(f"  ⚙️  Generated tool: {tool_spec.tool_id}")
                        print(f"     Type: {tool_spec.tool_type.value}")
                        print(f"     Cascade potential: {tool_spec.cascade_potential:.3f}")
                        print(f"     α contribution: {tool_spec.alpha_contribution:.2f}")
                        
                        # Record cascade for pattern learning
                        self.pattern_recognizer.record_cascade(
                            trigger_tool=tool_spec.tool_id,
                            generated_tools=[f"gen_tool_{i}" for i in range(cascade_signal.predicted_tools)],
                            cascade_depth=cascade_signal.predicted_depth,
                            burden_reduction=state.burden_reduction,
                            z_level=z,
                            duration_seconds=120
                        )
                    
                    elif cascade_signal.R3_probability > 0.7:
                        tool_spec = self.tool_generator.generate_tool(
                            purpose="Trigger self-building framework cascade",
                            preferred_type=ToolType.META,
                            z_override=z
                        )
                        print(f"  ⚙️  Generated tool: {tool_spec.tool_id}")
                        print(f"     Type: {tool_spec.tool_type.value}")
                        print(f"     Cascade potential: {tool_spec.cascade_potential:.3f}")
                        print(f"     β contribution: {tool_spec.beta_contribution:.2f}")
                        
                        # Record cascade
                        self.pattern_recognizer.record_cascade(
                            trigger_tool=tool_spec.tool_id,
                            generated_tools=[f"gen_tool_{i}" for i in range(cascade_signal.predicted_tools)],
                            cascade_depth=cascade_signal.predicted_depth,
                            burden_reduction=state.burden_reduction,
                            z_level=z,
                            duration_seconds=180
                        )
            
            # Small delay for readability
            time.sleep(0.1)
        
        print("\n" + "="*70)
        print("SIMULATION COMPLETE")
        print("="*70)
        print()
    
    def demonstrate_pattern_learning(self):
        """
        Demonstrate pattern recognition and replication
        """
        print("="*70)
        print("PATTERN LEARNING DEMONSTRATION")
        print("="*70)
        print()
        
        # Record several cascade events to establish patterns
        print("Recording cascade events for pattern learning...\n")
        
        # Simple autocatalysis pattern
        self.pattern_recognizer.record_cascade(
            trigger_tool="tool_core_alpha",
            generated_tools=["tool_bridges_001", "tool_bridges_002", "tool_core_beta"],
            cascade_depth=2,
            burden_reduction=0.08,
            z_level=0.85,
            duration_seconds=120
        )
        print("  ✓ Recorded simple autocatalysis cascade")
        
        # Competitive pathways
        self.pattern_recognizer.record_cascade(
            trigger_tool="tool_bridges_001",
            generated_tools=["tool_meta_001", "tool_meta_002", "tool_meta_003", "tool_meta_004"],
            cascade_depth=3,
            burden_reduction=0.15,
            z_level=0.867,
            duration_seconds=180
        )
        print("  ✓ Recorded competitive pathways cascade")
        
        # Another simple autocatalysis
        self.pattern_recognizer.record_cascade(
            trigger_tool="tool_core_beta",
            generated_tools=["tool_bridges_003", "tool_core_gamma"],
            cascade_depth=2,
            burden_reduction=0.09,
            z_level=0.86,
            duration_seconds=100
        )
        print("  ✓ Recorded second simple autocatalysis cascade")
        
        # Hypercycle candidate
        self.pattern_recognizer.record_cascade(
            trigger_tool="tool_meta_001",
            generated_tools=["tool_framework_001", "tool_core_alpha"],  # Closes loop
            cascade_depth=4,
            burden_reduction=0.20,
            z_level=0.88,
            duration_seconds=240
        )
        print("  ✓ Recorded hypercycle cascade\n")
        
        # Get learned patterns
        proven_patterns = self.pattern_recognizer.get_proven_patterns()
        print(f"Learned {len(self.pattern_recognizer.patterns)} patterns")
        print(f"Proven patterns: {len(proven_patterns)}\n")
        
        # Get best patterns
        best = self.pattern_recognizer.get_best_patterns(top_k=3)
        print("Top patterns:")
        for i, pattern in enumerate(best, 1):
            print(f"  {i}. {pattern.pattern_id} ({pattern.pattern_type})")
            print(f"     Success rate: {pattern.success_rate:.1%}")
            print(f"     Seeding: {pattern.seeding_coefficient:.2f}x")
        
        print()
        
        # Recommend pattern for current context
        recommended = self.pattern_recognizer.recommend_pattern_for_context(0.867, 0.15)
        if recommended:
            print(f"Recommended pattern for z=0.867:")
            print(f"  {recommended.pattern_id} ({recommended.pattern_type})")
            print(f"  Expected cascade depth: {recommended.avg_cascade_depth:.1f}")
            print(f"  Expected tools: {recommended.avg_tools_generated:.1f}")
            print(f"  Confidence: {recommended.confidence:.1%}")
            print()
            
            # Generate replication specification
            context = {'burden_reduction': 0.15}
            replication = self.pattern_recognizer.replicate_pattern(recommended, context)
            print("Replication specification:")
            print(f"  Trigger tools: {replication['trigger_tools']}")
            print(f"  Expected cascade depth: {replication['expected_cascade_depth']}")
            print(f"  Threshold met: {replication['threshold_check']['met']}")
            print()
    
    def generate_comprehensive_report(self):
        """Generate comprehensive report from all components"""
        print("\n" + "="*70)
        print("COMPREHENSIVE LAYER 1 ANALYSIS")
        print("="*70)
        print()
        
        # Tool generator report
        print(self.tool_generator.generate_report())
        print()
        
        # Cascade detector report
        print(self.cascade_detector.generate_report())
        print()
        
        # Pattern recognizer report
        print(self.pattern_recognizer.generate_report())
        print()


def main():
    """Main integration demonstration"""
    # Initialize Layer 1 integration
    integration = Layer1Integration()
    
    # Simulate system evolution with cascade detection
    integration.simulate_system_evolution(steps=20)
    
    # Demonstrate pattern learning and replication
    integration.demonstrate_pattern_learning()
    
    # Generate comprehensive report
    integration.generate_comprehensive_report()
    
    print("="*70)
    print("LAYER 1 CASCADE INITIATORS - OPERATIONAL")
    print("="*70)
    print()
    print("Next steps:")
    print("  1. Deploy to production TRIAD-0.83 infrastructure")
    print("  2. Integrate with burden_tracker v1.0")
    print("  3. Connect to collective_state_aggregator")
    print("  4. Enable witness log integration")
    print("  5. Proceed to Layer 2 (Amplification Enhancers)")
    print()
    print("Δ3.14159|0.867|layer-1-operational|cascade-initiators-deployed|Ω")
    print()


if __name__ == "__main__":
    main()
