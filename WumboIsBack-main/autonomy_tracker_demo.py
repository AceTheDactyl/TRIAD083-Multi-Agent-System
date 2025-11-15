#!/usr/bin/env python3
"""
AUTONOMY TRACKER DEMO
=====================

Simulates a 30-day progression toward agent-class to demonstrate
the phase-aware autonomy tracker in action.

Shows how sovereignty metrics evolve through phase regimes:
- Subcritical → Near-critical → Critical → Supercritical → Agent-class

Demonstrates phase-adaptive recommendations and milestone detection.
"""

from autonomy_tracker import PhaseAwareAutonomyTracker
from datetime import datetime, timedelta
import time


def simulate_progression():
    """
    Simulate a 30-day progression toward agent-class.

    Progression pattern:
    - Days 1-10: Subcritical (building foundation)
    - Days 11-20: Near-critical (approaching threshold)
    - Days 21-25: Critical (phase transition)
    - Days 26-30: Supercritical + Agent-class
    """
    print("="*70)
    print("AUTONOMY TRACKER - 30-DAY PROGRESSION SIMULATION")
    print("="*70)
    print("\nSimulating daily measurements with realistic growth patterns...")
    print("(Autonomy is primary driver r=0.843)\n")

    # Create tracker
    tracker = PhaseAwareAutonomyTracker(storage_path="demo_autonomy_tracker.json")

    # Simulation data: (clarity, immunity, efficiency, autonomy)
    # Realistic growth: autonomy grows fastest (primary driver)
    progression_schedule = [
        # Week 1: Subcritical - Building foundation
        (0.30, 0.40, 0.25, 0.20, 5, 4, 1, ["Started sovereignty practice"]),
        (0.35, 0.45, 0.30, 0.25, 6, 4, 2, ["Clarity improving"]),
        (0.38, 0.50, 0.32, 0.28, 5, 3, 2, ["Noticed first pattern"]),
        (0.40, 0.55, 0.35, 0.32, 7, 4, 3, ["Immunity strengthening"]),
        (0.42, 0.58, 0.38, 0.35, 6, 3, 3, ["Week 1 complete"]),
        (0.45, 0.60, 0.40, 0.38, 5, 2, 3, ["More author mode"]),
        (0.47, 0.62, 0.42, 0.40, 8, 4, 4, ["Week 1 reflection"]),

        # Week 2: Still subcritical, accelerating
        (0.50, 0.64, 0.45, 0.43, 6, 3, 3, ["Shortcuts emerging"]),
        (0.52, 0.66, 0.48, 0.46, 7, 3, 4, ["Pattern recognition active"]),
        (0.54, 0.68, 0.50, 0.48, 5, 2, 3, ["Efficiency improving"]),
        (0.56, 0.70, 0.52, 0.50, 8, 3, 5, ["Autonomous moments"]),
        (0.58, 0.72, 0.54, 0.52, 6, 2, 4, ["Week 2 complete"]),
        (0.60, 0.73, 0.56, 0.54, 7, 2, 5, ["Consistency building"]),
        (0.62, 0.74, 0.58, 0.56, 5, 1, 4, ["Boundary activation faster"]),

        # Week 3: Approaching near-critical
        (0.64, 0.75, 0.60, 0.58, 8, 2, 6, ["Near-critical approaching"]),
        (0.66, 0.76, 0.62, 0.60, 6, 1, 5, ["Integration deepening"]),
        (0.68, 0.77, 0.64, 0.62, 7, 2, 5, ["Frameworks emerging"]),
        (0.70, 0.78, 0.66, 0.64, 9, 2, 7, ["Meta-cognition depth +1"]),
        (0.71, 0.79, 0.68, 0.66, 5, 1, 4, ["Week 3 complete"]),
        (0.72, 0.80, 0.70, 0.68, 8, 1, 7, ["Near-critical phase!"]),
        (0.73, 0.81, 0.71, 0.70, 7, 1, 6, ["Autonomy threshold (0.70) crossed!"]),

        # Week 4: Critical phase transition
        (0.74, 0.82, 0.72, 0.72, 10, 2, 8, ["Critical phase - cascade active"]),
        (0.75, 0.83, 0.73, 0.74, 8, 1, 7, ["Amplification boosted 50%"]),
        (0.76, 0.84, 0.74, 0.76, 9, 1, 8, ["Self-catalyzing confirmed"]),
        (0.77, 0.85, 0.75, 0.78, 7, 0, 7, ["100% author mode today!"]),
        (0.78, 0.86, 0.76, 0.80, 8, 1, 7, ["Week 4 complete - supercritical!"]),

        # Week 5: Supercritical + Agent-class
        (0.79, 0.87, 0.77, 0.82, 10, 1, 9, ["Supercritical confirmed"]),
        (0.80, 0.88, 0.78, 0.84, 9, 0, 9, ["Framework-building active"]),
        (0.81, 0.89, 0.79, 0.86, 8, 0, 8, ["Agent-class achieved!", "Untouchable except through reciprocity"]),
        (0.82, 0.90, 0.80, 0.88, 11, 0, 11, ["Autonomy compounding"]),
        (0.83, 0.91, 0.81, 0.90, 10, 0, 10, ["Day 30: Full agent-class operational"])
    ]

    # Run simulation
    start_date = datetime.now() - timedelta(days=30)

    for day, (clarity, immunity, efficiency, autonomy, interactions, character, author, obs) in enumerate(progression_schedule, 1):
        # Simulate measurement timestamp
        measurement_date = start_date + timedelta(days=day)

        # Temporarily override tracker's timestamp for demo
        snapshot = tracker.measure_sovereignty(
            clarity, immunity, efficiency, autonomy,
            interactions, character, author, obs
        )

        # Override timestamp for simulation
        snapshot.timestamp = measurement_date
        tracker.trajectory.snapshots[-1].timestamp = measurement_date

        # Save after each day
        tracker._save_trajectory()

        # Print progress for key days
        if day in [1, 7, 14, 21, 28, 30]:
            print(f"\n📅 Day {day} ({measurement_date.strftime('%Y-%m-%d')})")
            print(f"   Phase: {snapshot.phase_regime.value}")
            print(f"   Agency: {snapshot.agency_level.value}")
            print(f"   s-coordinate: {snapshot.phase_coordinate:.3f}")
            print(f"   Autonomy: {snapshot.autonomy_score:.2f}")
            print(f"   Total sovereignty: {snapshot.total_sovereignty:.2f}")
            print(f"   Amplification: {snapshot.predicted_amplification:.1f}x")

            if snapshot.observations:
                print(f"   Notes: {', '.join(snapshot.observations)}")

        # Show milestones as they're reached
        if len(tracker.trajectory.milestones_reached) > 0:
            latest_milestone = tracker.trajectory.milestones_reached[-1]
            if latest_milestone['timestamp'] == snapshot.timestamp.isoformat():
                print(f"\n   🎉 MILESTONE: {latest_milestone['description']}")

    print("\n" + "="*70)
    print("Simulation complete! Generating final report...")
    print("="*70)

    # Generate final status report
    print("\n")
    print(tracker.generate_status_report())

    # Show trajectory summary
    print("\n")
    print("="*70)
    print("TRAJECTORY SUMMARY")
    print("="*70)

    summary = tracker.get_trajectory_summary()
    print(f"\nDuration: {summary['duration_days']} days")
    print(f"Measurements: {summary['measurements']}")
    print(f"\nProgression:")
    print(f"  Phase: {summary['start_phase']} → {summary['current_phase']}")
    print(f"  Agency: {summary['start_agency']} → {summary['current_agency']}")

    print(f"\nGrowth:")
    for metric, growth in summary['sovereignty_growth'].items():
        print(f"  {metric.capitalize()}: +{growth:.2f}")

    print(f"\nMilestones: {summary['milestones_count']} reached")
    print(f"Agent-class: {'✅ ACHIEVED' if summary['agent_class_achieved'] else '⏳ In progress'}")

    print("\n" + "="*70)
    print("Demo data saved to: demo_autonomy_tracker.json")
    print("Run 'python3 autonomy_tracker.py --status' to see live tracker")
    print("="*70)


if __name__ == "__main__":
    simulate_progression()
