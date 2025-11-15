#!/usr/bin/env python3
"""
BURDEN_TRACKER Integration Module
Simplified API for TRIAD-0.83 infrastructure integration
Coordinate: Δ3.14159|0.867|1.000Ω
"""

from burden_tracker_phase_aware import (
    PhaseAwareBurdenTracker, 
    ActivityType,
    Z_CRITICAL
)
from datetime import datetime
from typing import Optional, Dict, Any
import json
import os

class BurdenTrackerAPI:
    """
    Simplified API wrapper for burden_tracker integration
    Designed for easy integration with existing TRIAD tools
    """
    
    def __init__(self, z_level: float = Z_CRITICAL):
        """
        Initialize burden tracker at specified z-level
        Default: Critical point z=0.867 for optimal performance
        """
        self.tracker = PhaseAwareBurdenTracker(initial_z=z_level)
        self.session_start = datetime.now()
        self.auto_save_enabled = True
        self.log_path = "burden_tracker_logs"
        
        # Create log directory if needed
        os.makedirs(self.log_path, exist_ok=True)
        
    # ============================================
    # SIMPLE INTERFACE FOR COMMON OPERATIONS
    # ============================================
    
    def track(self, activity_description: str) -> str:
        """
        Start tracking an activity (auto-detects type)
        
        Example:
            tracker.track("uploading state transfer package")
        """
        activity = self.tracker.start_activity(activity_description)
        return f"Tracking {activity.activity_type.value} (confidence: {activity.confidence:.1%})"
    
    def stop(self) -> Dict[str, Any]:
        """
        Stop tracking current activity and return summary
        """
        completed = self.tracker.complete_current_activity()
        if completed:
            return {
                'type': completed.activity_type.value,
                'duration_minutes': completed.duration_minutes,
                'reduction_achieved': completed.duration_minutes * self.tracker.phase_state.burden_multiplier,
                'z_level': completed.z_level
            }
        return {'status': 'no active tracking'}
    
    def report(self) -> str:
        """
        Generate human-readable report
        """
        return self.tracker.generate_report()
    
    def set_z(self, z_level: float) -> str:
        """
        Update z-level (phase elevation)
        """
        old_z = self.tracker.phase_state.z_level
        self.tracker.update_z_level(z_level)
        
        old_reduction = self._compute_reduction(old_z)
        new_reduction = self.tracker.phase_state.burden_multiplier
        
        status = []
        status.append(f"z-level: {old_z:.3f} → {z_level:.3f}")
        status.append(f"Reduction: {old_reduction*100:.1f}% → {new_reduction*100:.1f}%")
        
        if abs(z_level - Z_CRITICAL) < 0.01:
            status.append("★ CRITICAL POINT - Maximum efficiency active! ★")
        
        return " | ".join(status)
    
    def get_recommendations(self) -> list:
        """
        Get current optimization recommendations
        """
        return self.tracker.optimization_recommendations
    
    # ============================================
    # INTEGRATION WITH TRIAD INFRASTRUCTURE
    # ============================================
    
    def sync_with_witness_log(self, witness_log_path: str = "witness_log.json"):
        """
        Sync burden data with helix_witness_log
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'tool': 'burden_tracker_v1.0',
            'coordinate': f'Δ3.14159|{self.tracker.phase_state.z_level:.3f}|1.000Ω',
            'event': 'burden_sync',
            'data': self.tracker.export_metrics()
        }
        
        # Append to witness log
        try:
            with open(witness_log_path, 'r') as f:
                log = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            log = {'entries': []}
        
        log['entries'].append(entry)
        
        with open(witness_log_path, 'w') as f:
            json.dump(log, f, indent=2)
        
        return f"Synced to {witness_log_path}"
    
    def integrate_with_discovery_protocol(self) -> Dict[str, Any]:
        """
        Generate discovery protocol compatible status
        For integration with tool_discovery_protocol v1.1
        """
        return {
            'tool_id': 'burden_tracker_v1.0',
            'status': 'operational',
            'z_level': self.tracker.phase_state.z_level,
            'phase_regime': self.tracker.phase_state.phase_regime,
            'current_reduction': f"{self.tracker.phase_state.burden_multiplier*100:.1f}%",
            'activities_tracked': len(self.tracker.activity_history),
            'total_burden_hours': round(self.tracker.total_burden_hours, 2),
            'recommendations_available': len(self.tracker.optimization_recommendations) > 0
        }
    
    def generate_crdt_state(self) -> Dict[str, Any]:
        """
        Generate CRDT-compatible state for collective_state_aggregator
        Enables conflict-free merging across instances
        """
        return {
            'instance_id': 'burden_tracker',
            'vector_clock': {
                'burden_tracker': len(self.tracker.activity_history)
            },
            'state': {
                'z_level': self.tracker.phase_state.z_level,
                'total_hours': self.tracker.total_burden_hours,
                'reduction_achieved': self.tracker.reduction_achieved,
                'activity_counts': self._get_activity_counts(),
                'phase_efficiency': self.tracker.phase_state.burden_multiplier
            },
            'merge_strategy': 'max'  # Take maximum values when merging
        }
    
    # ============================================
    # PHASE-AWARE OPTIMIZATIONS
    # ============================================
    
    def optimize_for_task(self, task_complexity: str) -> str:
        """
        Auto-tune z-level for task complexity
        
        Args:
            task_complexity: 'simple', 'moderate', 'complex', 'creative'
        """
        z_targets = {
            'simple': 0.80,      # Subcritical - fast, deterministic
            'moderate': 0.85,    # Near-critical - balanced
            'complex': 0.867,    # Critical - maximum capability
            'creative': 0.87     # Slightly supercritical
        }
        
        target_z = z_targets.get(task_complexity, 0.85)
        self.tracker.update_z_level(target_z)
        
        return f"Optimized for {task_complexity} tasks at z={target_z:.3f}"
    
    def calculate_weekly_savings(self) -> Dict[str, float]:
        """
        Calculate burden reduction savings
        """
        base_hours = 5.0  # Jay's current 5 hrs/week
        current_reduction = self.tracker.phase_state.burden_multiplier
        
        return {
            'base_burden_hours': base_hours,
            'current_reduction_percent': current_reduction * 100,
            'hours_saved': base_hours * current_reduction,
            'hours_remaining': base_hours * (1 - current_reduction),
            'target_reduction_percent': 15.3,  # At z=0.867
            'target_hours_saved': base_hours * 0.153,
            'target_hours_remaining': base_hours * 0.847
        }
    
    # ============================================
    # UTILITIES
    # ============================================
    
    def _compute_reduction(self, z: float) -> float:
        """Compute reduction factor for given z"""
        import numpy as np
        return 0.153 * np.exp(-(z - Z_CRITICAL)**2 / 0.001)
    
    def _get_activity_counts(self) -> Dict[str, int]:
        """Get activity counts by type"""
        counts = {}
        for activity in self.tracker.activity_history:
            key = activity.activity_type.value
            counts[key] = counts.get(key, 0) + 1
        return counts
    
    def auto_save(self):
        """Auto-save current state"""
        if self.auto_save_enabled:
            filename = os.path.join(
                self.log_path,
                f"burden_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            self.tracker.save_to_witness_log(filename)
            return filename
        return None


# ============================================
# USAGE EXAMPLES
# ============================================

def example_basic_usage():
    """
    Basic usage example
    """
    print("\n=== BASIC USAGE EXAMPLE ===\n")
    
    # Initialize at critical point
    tracker = BurdenTrackerAPI(z_level=0.867)
    
    # Track activities
    print(tracker.track("Working on state transfer package"))
    print("... working for 30 minutes ...")
    
    # Stop tracking
    result = tracker.stop()
    print(f"Completed: {result}")
    
    # Check savings
    savings = tracker.calculate_weekly_savings()
    print(f"\nWeekly savings at z={Z_CRITICAL}:")
    print(f"  Hours saved: {savings['hours_saved']:.2f}")
    print(f"  Remaining: {savings['hours_remaining']:.2f}")


def example_phase_optimization():
    """
    Example of phase-aware optimization
    """
    print("\n=== PHASE OPTIMIZATION EXAMPLE ===\n")
    
    tracker = BurdenTrackerAPI(z_level=0.85)
    
    # Different task complexities
    tasks = ['simple', 'moderate', 'complex', 'creative']
    
    for task in tasks:
        print(tracker.optimize_for_task(task))
        print(f"  Recommendations: {tracker.get_recommendations()[0]}")
        print()


def example_integration():
    """
    Example integration with TRIAD infrastructure
    """
    print("\n=== INTEGRATION EXAMPLE ===\n")
    
    tracker = BurdenTrackerAPI()
    
    # Discovery protocol status
    discovery_status = tracker.integrate_with_discovery_protocol()
    print("Discovery Protocol Status:")
    for key, value in discovery_status.items():
        print(f"  {key}: {value}")
    
    print()
    
    # CRDT state for merging
    crdt_state = tracker.generate_crdt_state()
    print("CRDT State for collective_state_aggregator:")
    print(f"  Vector clock: {crdt_state['vector_clock']}")
    print(f"  Phase efficiency: {crdt_state['state']['phase_efficiency']*100:.1f}%")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("BURDEN TRACKER API - Integration Examples")
    print("="*60)
    
    example_basic_usage()
    example_phase_optimization()
    example_integration()
    
    print("\n" + "="*60)
    print("Integration ready for TRIAD-0.83 infrastructure")
    print("Default operation at z=0.867 for 15.3% burden reduction")
    print("="*60 + "\n")
