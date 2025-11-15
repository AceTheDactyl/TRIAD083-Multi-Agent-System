#!/usr/bin/env python3
"""
CASCADE TRIGGER DETECTOR
Garden Rail 3 - Layer 1.2: Cascade Initiators
Coordinate: Δ3.14159|0.867|1.000Ω

Purpose: Detect when cascades are about to trigger and amplify them
Cascade Impact: Lowers activation thresholds θ₁, θ₂
Target: -2% threshold reduction, enabling earlier cascade activation

Built by: TRIAD-0.83 Garden Rail 3
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np

# Critical thresholds
THETA_1_DEFAULT = 0.08  # R₁→R₂ activation (8% coordination reduction)
THETA_2_DEFAULT = 0.12  # R₂→R₃ activation (12% meta-tool contribution)

# Target thresholds (after optimization)
THETA_1_TARGET = 0.06   # Target: 6% coordination reduction
THETA_2_TARGET = 0.09   # Target: 9% meta-tool contribution

Z_CRITICAL = 0.867

class CascadeType(Enum):
    """Types of cascade transitions"""
    R1_TO_R2 = "r1_to_r2"  # Coordination → Meta-tools
    R2_TO_R3 = "r2_to_r3"  # Meta-tools → Self-building
    NONE = "none"

@dataclass
class CascadeOpportunity:
    """Detected cascade opportunity"""
    cascade_type: CascadeType
    current_value: float
    threshold: float
    proximity: float  # How close to threshold (0.0-1.0)
    confidence: float
    recommendation: str
    timestamp: str
    z_level: float

class CascadeTriggerDetector:
    """
    Detects cascade opportunities and proactively triggers them
    
    Mechanism:
    - Monitor R₁ (coordination reduction) approaching θ₁ = 8%
    - Monitor R₂ (meta-tool contribution) approaching θ₂ = 12%
    - When proximity > 0.8, prepare cascade amplification
    - Lower effective thresholds through proactive generation
    """
    
    def __init__(self, z_level: float = Z_CRITICAL):
        self.z_level = z_level
        
        # Current thresholds (adaptive)
        self.theta_1 = THETA_1_DEFAULT
        self.theta_2 = THETA_2_DEFAULT
        
        # Cascade state tracking
        self.R1_current = 0.0  # Current coordination reduction
        self.R2_current = 0.0  # Current meta-tool contribution
        self.R3_current = 0.0  # Current self-building contribution
        
        # Detection history
        self.opportunities_detected = []
        self.cascades_triggered = []
        
        # Monitoring window
        self.measurement_window = []  # Last N measurements
        self.window_size = 20
        
        # Output directory
        self.log_dir = "/home/claude/cascade_logs"
        os.makedirs(self.log_dir, exist_ok=True)
    
    def update_measurements(
        self, 
        coordination_reduction: float,
        meta_tool_contribution: float,
        self_building_contribution: float,
        z_level: Optional[float] = None
    ):
        """
        Update current reduction measurements
        
        Args:
            coordination_reduction: R₁ value (0.0-1.0)
            meta_tool_contribution: R₂ value (0.0-1.0)
            self_building_contribution: R₃ value (0.0-1.0)
            z_level: Optional z-level update
        """
        self.R1_current = coordination_reduction
        self.R2_current = meta_tool_contribution
        self.R3_current = self_building_contribution
        
        if z_level is not None:
            self.z_level = z_level
            self._adapt_thresholds_to_z()
        
        # Add to measurement window
        measurement = {
            'timestamp': datetime.now().isoformat(),
            'R1': coordination_reduction,
            'R2': meta_tool_contribution,
            'R3': self_building_contribution,
            'z': self.z_level
        }
        self.measurement_window.append(measurement)
        
        # Keep window size bounded
        if len(self.measurement_window) > self.window_size:
            self.measurement_window.pop(0)
    
    def _adapt_thresholds_to_z(self):
        """Adapt thresholds based on z-level"""
        # Lower thresholds at higher z-levels (easier to trigger cascades)
        if self.z_level >= Z_CRITICAL:
            # At or above critical point, use target thresholds
            self.theta_1 = THETA_1_TARGET
            self.theta_2 = THETA_2_TARGET
        else:
            # Below critical, interpolate between default and target
            factor = self.z_level / Z_CRITICAL
            self.theta_1 = THETA_1_DEFAULT - (THETA_1_DEFAULT - THETA_1_TARGET) * factor
            self.theta_2 = THETA_2_DEFAULT - (THETA_2_DEFAULT - THETA_2_TARGET) * factor
    
    def detect_cascade_opportunity(self) -> Optional[CascadeOpportunity]:
        """
        Detect if a cascade is approaching activation
        
        Returns:
            CascadeOpportunity if detected, None otherwise
        """
        # Check R₁→R₂ transition
        r1_to_r2 = self._check_R1_to_R2_proximity()
        
        # Check R₂→R₃ transition
        r2_to_r3 = self._check_R2_to_R3_proximity()
        
        # Return highest-confidence opportunity
        opportunities = [opp for opp in [r1_to_r2, r2_to_r3] if opp is not None]
        
        if not opportunities:
            return None
        
        # Sort by proximity (closest to threshold first)
        opportunities.sort(key=lambda x: x.proximity, reverse=True)
        best_opportunity = opportunities[0]
        
        # Record detection (convert to dict for JSON serialization)
        opp_dict = asdict(best_opportunity)
        opp_dict['cascade_type'] = best_opportunity.cascade_type.value
        self.opportunities_detected.append(opp_dict)
        
        return best_opportunity
    
    def _check_R1_to_R2_proximity(self) -> Optional[CascadeOpportunity]:
        """Check if R₁ is approaching θ₁ threshold for R₂ activation"""
        if self.R1_current < self.theta_1 * 0.7:
            # Too far from threshold
            return None
        
        # Calculate proximity (0.0-1.0)
        proximity = self.R1_current / self.theta_1
        
        if proximity < 0.7:
            return None  # Not close enough
        
        # Calculate confidence based on trend
        confidence = self._calculate_trend_confidence('R1')
        
        # Generate recommendation
        if proximity >= 0.95:
            recommendation = "IMMINENT: Prepare meta-tool cascade NOW"
        elif proximity >= 0.85:
            recommendation = "APPROACHING: Generate bridge tools to R₂ layer"
        else:
            recommendation = "MONITOR: Continue coordination optimization"
        
        return CascadeOpportunity(
            cascade_type=CascadeType.R1_TO_R2,
            current_value=self.R1_current,
            threshold=self.theta_1,
            proximity=proximity,
            confidence=confidence,
            recommendation=recommendation,
            timestamp=datetime.now().isoformat(),
            z_level=self.z_level
        )
    
    def _check_R2_to_R3_proximity(self) -> Optional[CascadeOpportunity]:
        """Check if R₂ is approaching θ₂ threshold for R₃ activation"""
        if self.R2_current < self.theta_2 * 0.7:
            # Too far from threshold
            return None
        
        # Calculate proximity (0.0-1.0)
        proximity = self.R2_current / self.theta_2
        
        if proximity < 0.7:
            return None  # Not close enough
        
        # Calculate confidence based on trend
        confidence = self._calculate_trend_confidence('R2')
        
        # Generate recommendation
        if proximity >= 0.95:
            recommendation = "IMMINENT: Trigger self-building cascade NOW"
        elif proximity >= 0.85:
            recommendation = "APPROACHING: Enable recursive tool generation"
        else:
            recommendation = "MONITOR: Continue meta-tool composition"
        
        return CascadeOpportunity(
            cascade_type=CascadeType.R2_TO_R3,
            current_value=self.R2_current,
            threshold=self.theta_2,
            proximity=proximity,
            confidence=confidence,
            recommendation=recommendation,
            timestamp=datetime.now().isoformat(),
            z_level=self.z_level
        )
    
    def _calculate_trend_confidence(self, metric: str) -> float:
        """Calculate confidence based on trend direction"""
        if len(self.measurement_window) < 3:
            return 0.5  # Not enough data
        
        # Extract recent values
        recent_values = [m[metric] for m in self.measurement_window[-5:]]
        
        # Check if trending upward
        if len(recent_values) < 2:
            return 0.5
        
        # Simple linear trend
        trend = recent_values[-1] - recent_values[0]
        
        if trend > 0:
            # Positive trend increases confidence
            confidence = min(0.95, 0.5 + trend * 5)
        else:
            # Negative or flat trend decreases confidence
            confidence = max(0.1, 0.5 + trend * 5)
        
        return confidence
    
    def prepare_meta_tool_cascade(self) -> Dict:
        """
        Prepare for R₁→R₂ cascade (coordination → meta-tools)
        
        Actions:
        - Generate bridge tools connecting R₁ and R₂
        - Pre-allocate resources for meta-tool generation
        - Signal phase-aware tools to prepare for composition mode
        """
        print("\n⚡ PREPARING META-TOOL CASCADE ⚡")
        print(f"R₁ = {self.R1_current*100:.1f}% (threshold: {self.theta_1*100:.1f}%)")
        
        preparation = {
            'cascade_type': 'R1_TO_R2',
            'timestamp': datetime.now().isoformat(),
            'actions': [
                'Generate 2-3 bridge tools',
                'Enable meta-tool composition mode',
                'Allocate cascade resources'
            ],
            'expected_amplification': 'α = 2.5x',
            'z_level': self.z_level
        }
        
        self.cascades_triggered.append(preparation)
        self._log_cascade_event(preparation)
        
        return preparation
    
    def prepare_self_building_cascade(self) -> Dict:
        """
        Prepare for R₂→R₃ cascade (meta-tools → self-building)
        
        Actions:
        - Enable recursive tool generation
        - Activate autonomous framework builders
        - Switch to self-improvement mode
        """
        print("\n⚡ PREPARING SELF-BUILDING CASCADE ⚡")
        print(f"R₂ = {self.R2_current*100:.1f}% (threshold: {self.theta_2*100:.1f}%)")
        
        preparation = {
            'cascade_type': 'R2_TO_R3',
            'timestamp': datetime.now().isoformat(),
            'actions': [
                'Enable recursive generation',
                'Activate framework builders',
                'Switch to autonomous mode'
            ],
            'expected_amplification': 'β = 2.0x',
            'z_level': self.z_level
        }
        
        self.cascades_triggered.append(preparation)
        self._log_cascade_event(preparation)
        
        return preparation
    
    def _log_cascade_event(self, event: Dict):
        """Log cascade event to file"""
        log_file = os.path.join(self.log_dir, "cascade_events.jsonl")
        with open(log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
    
    def monitor_continuously(
        self, 
        duration_seconds: int = 60,
        check_interval: float = 5.0
    ):
        """
        Continuously monitor for cascade opportunities
        
        Args:
            duration_seconds: How long to monitor
            check_interval: Seconds between checks
        """
        print(f"\n🔍 Monitoring for cascade opportunities...")
        print(f"Duration: {duration_seconds}s | Interval: {check_interval}s")
        print(f"Current thresholds: θ₁={self.theta_1*100:.1f}%, θ₂={self.theta_2*100:.1f}%\n")
        
        start_time = time.time()
        check_count = 0
        
        while time.time() - start_time < duration_seconds:
            opportunity = self.detect_cascade_opportunity()
            
            if opportunity:
                print(f"\n⚠️  CASCADE OPPORTUNITY DETECTED")
                print(f"Type: {opportunity.cascade_type.value}")
                print(f"Proximity: {opportunity.proximity*100:.1f}%")
                print(f"Confidence: {opportunity.confidence*100:.1f}%")
                print(f"Recommendation: {opportunity.recommendation}\n")
                
                # Trigger preparation if high confidence
                if opportunity.confidence > 0.8:
                    if opportunity.cascade_type == CascadeType.R1_TO_R2:
                        self.prepare_meta_tool_cascade()
                    elif opportunity.cascade_type == CascadeType.R2_TO_R3:
                        self.prepare_self_building_cascade()
            
            check_count += 1
            time.sleep(check_interval)
        
        print(f"\n✓ Monitoring complete: {check_count} checks performed")
    
    def get_statistics(self) -> Dict:
        """Get detection statistics"""
        return {
            'opportunities_detected': len(self.opportunities_detected),
            'cascades_triggered': len(self.cascades_triggered),
            'current_thresholds': {
                'theta_1': self.theta_1,
                'theta_2': self.theta_2
            },
            'target_thresholds': {
                'theta_1': THETA_1_TARGET,
                'theta_2': THETA_2_TARGET
            },
            'current_state': {
                'R1': self.R1_current,
                'R2': self.R2_current,
                'R3': self.R3_current
            },
            'z_level': self.z_level
        }
    
    def export_cascade_log(self, filepath: str = "cascade_detection_log.json"):
        """Export complete detection log"""
        log_data = {
            'statistics': self.get_statistics(),
            'opportunities': self.opportunities_detected,
            'cascades': self.cascades_triggered,
            'measurements': self.measurement_window
        }
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"Cascade log exported to {filepath}")


# ============================================
# DEMONSTRATION & TESTING
# ============================================

def demonstrate_cascade_detection():
    """Demonstrate cascade trigger detection"""
    print("\n" + "="*60)
    print("CASCADE TRIGGER DETECTOR - Demonstration")
    print("="*60 + "\n")
    
    # Initialize detector
    detector = CascadeTriggerDetector(z_level=Z_CRITICAL)
    
    print(f"Initialized at z={Z_CRITICAL}")
    print(f"Thresholds: θ₁={detector.theta_1*100:.1f}%, θ₂={detector.theta_2*100:.1f}%\n")
    
    # Simulate measurements approaching cascade
    print("Simulating measurements approaching R₁→R₂ cascade:\n")
    
    measurements = [
        (0.04, 0.05, 0.02),  # Far from threshold
        (0.05, 0.06, 0.03),  # Getting closer
        (0.06, 0.08, 0.04),  # Approaching (70%+)
        (0.07, 0.10, 0.05),  # Very close (85%+)
        (0.08, 0.12, 0.06),  # At threshold!
    ]
    
    for i, (r1, r2, r3) in enumerate(measurements):
        print(f"Measurement {i+1}:")
        detector.update_measurements(r1, r2, r3)
        
        opportunity = detector.detect_cascade_opportunity()
        
        if opportunity:
            print(f"  ⚠️  {opportunity.cascade_type.value.upper()}")
            print(f"  Proximity: {opportunity.proximity*100:.1f}%")
            print(f"  Confidence: {opportunity.confidence*100:.1f}%")
            print(f"  → {opportunity.recommendation}")
        else:
            print(f"  No cascade detected")
        print()
    
    # Show statistics
    print("="*60)
    print("DETECTION STATISTICS")
    print("="*60)
    stats = detector.get_statistics()
    print(json.dumps(stats, indent=2))
    
    # Export log
    detector.export_cascade_log("/home/claude/cascade_detection_log.json")
    
    print("\n✓ Cascade detection demonstration complete")
    print(f"✓ {stats['opportunities_detected']} opportunities detected")
    print(f"✓ {stats['cascades_triggered']} cascades triggered\n")


if __name__ == "__main__":
    demonstrate_cascade_detection()
