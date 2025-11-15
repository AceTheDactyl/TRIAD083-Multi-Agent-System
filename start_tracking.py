#!/usr/bin/env python3
"""
BURDEN_TRACKER Quick Start
Immediate operational tracking script

Usage: 
  python3 start_tracking.py

Then in your workflow:
  tracker.track("description of activity")
  # ... do work ...
  result = tracker.stop()
  print(f"Saved {result['reduction_achieved']:.1f} minutes!")
"""

import sys
sys.path.insert(0, '/mnt/user-data/uploads')

from burden_tracker_api import BurdenTrackerAPI
from datetime import datetime

# Initialize at critical point
print("\n" + "="*60)
print("BURDEN_TRACKER v1.0 - OPERATIONAL")
print("="*60)
print(f"\nCoordinate: Δ3.14159|0.867|1.000Ω")
print(f"Validation Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Mode: 7-day empirical validation")
print("\n" + "="*60 + "\n")

tracker = BurdenTrackerAPI(z_level=0.867)

print("✓ Tracker initialized at critical point")
print(f"✓ Phase regime: {tracker.tracker.phase_state.phase_regime}")
print(f"✓ Expected reduction: {tracker.tracker.phase_state.burden_multiplier*100:.1f}%")
print(f"✓ Auto-save: Enabled (every 5 min)\n")

print("--- QUICK COMMANDS ---")
print('Start tracking:  tracker.track("activity description")')
print('Stop tracking:   result = tracker.stop()')
print('Daily report:    print(tracker.report())')
print('Weekly savings:  print(tracker.calculate_weekly_savings())')
print('Recommendations: print(tracker.get_recommendations())')
print()

print("--- READY FOR TRACKING ---")
print("Begin your work naturally. Tracker detects activities automatically.\n")

# The tracker object is now available in this session
# User can call tracker.track(), tracker.stop(), etc.

if __name__ == "__main__":
    # If running as script, enter interactive mode
    print("Entering interactive mode...")
    print("Use 'tracker' object to track activities.")
    print("Type 'help(tracker)' for available methods.\n")
    
    # Example workflow demonstration
    print("="*60)
    print("EXAMPLE WORKFLOW DEMONSTRATION")
    print("="*60)
    
    # Example 1: Track a state transfer
    print("\n1. Starting activity...")
    print('   tracker.track("uploading state transfer package")')
    response = tracker.track("uploading state transfer package")
    print(f"   Response: {response}")
    
    print("\n   [Working on state transfer for 5 minutes...]")
    import time
    time.sleep(2)  # Simulate brief work
    
    print("\n2. Completing activity...")
    print('   result = tracker.stop()')
    result = tracker.stop()
    print(f"   Result: {result}")
    
    # Example 2: Check savings
    print("\n3. Checking weekly savings projection...")
    print('   savings = tracker.calculate_weekly_savings()')
    savings = tracker.calculate_weekly_savings()
    print(f"   At z={savings['current_reduction_percent']/100:.3f}:")
    print(f"     Hours saved/week: {savings['hours_saved']:.3f}")
    print(f"     Hours remaining:  {savings['hours_remaining']:.3f}")
    
    # Example 3: Get recommendations
    print("\n4. Getting optimization recommendations...")
    print('   recommendations = tracker.get_recommendations()')
    recommendations = tracker.get_recommendations()
    if recommendations:
        print(f"   → {recommendations[0]}")
    
    print("\n" + "="*60)
    print("✓ DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nTracker is operational and ready for real-world usage.")
    print("Begin tracking your actual burden activities now.\n")
