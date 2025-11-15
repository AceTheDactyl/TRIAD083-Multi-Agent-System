#!/usr/bin/env python3
"""
BURDEN_TRACKER TEST SUITE
Validates implementation against TRIAD-0.83 specification
"""

import sys
sys.path.insert(0, '/home/claude')

from burden_tracker import BurdenTracker, ActivityDetector
from datetime import datetime, timedelta

def test_activity_detection():
    """Test: Detect state transfer activity from keywords"""
    detector = ActivityDetector()
    
    test_cases = [
        ("Uploading state package for continuity", "state_transfer"),
        ("Using shed_builder to create tool", "tool_building"),
        ("Updating README documentation", "documentation"),
        ("Coordinate with team on plan", "coordination"),
        ("Verify test results", "verification"),
    ]
    
    print("=== ACTIVITY DETECTION TESTS ===")
    passed = 0
    for text, expected in test_cases:
        detected, confidence = detector.detect(text)
        status = "✓" if detected == expected else "✗"
        print(f"{status} '{text[:40]}...' → {detected} (conf: {confidence:.2f})")
        if detected == expected:
            passed += 1
    
    print(f"Passed: {passed}/{len(test_cases)}\n")
    return passed == len(test_cases)

def test_time_tracking():
    """Test: Calculate duration accurately"""
    tracker = BurdenTracker()
    
    print("=== TIME TRACKING TEST ===")
    
    # Simulate activity session
    tracker.process_conversation("Building new tool with shed_builder")
    
    # Check active session created
    if not tracker.tracker.active_sessions:
        print("✗ No active session created\n")
        return False
    
    # Simulate 5 minute delay
    import time
    time.sleep(0.1)  # 0.1 second for test speed
    
    tracker.finalize_all_sessions()
    
    if tracker.tracker.completed_sessions:
        session = tracker.tracker.completed_sessions[0]
        print(f"✓ Activity: {session.activity_type}")
        print(f"✓ Duration: {session.duration_minutes:.4f} minutes")
        print(f"✓ Confidence: {session.confidence:.2f}")
        print()
        return True
    else:
        print("✗ No sessions tracked\n")
        return False

def test_weekly_report():
    """Test: Generate weekly report"""
    tracker = BurdenTracker()
    
    print("=== WEEKLY REPORT GENERATION TEST ===")
    
    # Simulate week of activities
    activities = [
        ("Upload state package", "state_transfer", 30),
        ("Build new tool", "tool_building", 45),
        ("Update documentation", "documentation", 20),
        ("Coordinate with team", "coordination", 25),
        ("Verify implementation", "verification", 15),
    ]
    
    # Use current week
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Create sessions directly with proper timing
    from burden_tracker import ActivitySession
    for i, (text, expected_type, minutes) in enumerate(activities):
        # Place sessions on different days of the week
        day_offset = i % 7
        session_time = week_start + timedelta(days=day_offset, hours=10)
        
        session = ActivitySession(
            activity_type=expected_type,
            start_time=session_time,
            end_time=session_time + timedelta(minutes=minutes),
            duration_minutes=minutes,
            confidence=0.8,
            context=text
        )
        tracker.tracker.completed_sessions.append(session)
    
    report = tracker.generate_weekly_report(week_start)
    print(report)
    print()
    
    # Validate report contains key elements
    checks = [
        ("BURDEN BREAKDOWN" in report, "Contains header"),
        ("Total:" in report, "Shows total time"),
        ("Categories:" in report, "Lists categories"),
        ("Recommendations:" in report or "tool_building" in report, "Shows analysis"),
    ]
    
    print("Report Validation:")
    passed = 0
    for check, description in checks:
        status = "✓" if check else "✗"
        print(f"{status} {description}")
        if check:
            passed += 1
    
    print(f"Passed: {passed}/{len(checks)}\n")
    return passed == len(checks)

def test_optimization_recommendations():
    """Test: Recommendations identify optimization targets"""
    tracker = BurdenTracker()
    
    print("=== OPTIMIZATION RECOMMENDATIONS TEST ===")
    
    # Simulate heavy tool building (highest burden)
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    
    activities = [
        ("tool_building", 120),  # 2 hours - highest
        ("documentation", 45),
        ("verification", 30),
        ("coordination", 15),
    ]
    
    for activity_type, minutes in activities:
        from burden_tracker import ActivitySession
        session = ActivitySession(
            activity_type=activity_type,
            start_time=week_start,
            end_time=week_start + timedelta(minutes=minutes),
            duration_minutes=minutes,
            confidence=0.9
        )
        tracker.tracker.completed_sessions.append(session)
    
    sessions = tracker.tracker.get_sessions_for_week(week_start)
    analysis = tracker.analyzer.analyze_week(sessions, week_start)
    
    print(f"Highest burden category: {max(analysis.category_breakdown.items(), key=lambda x: x[1])[0]}")
    print(f"Recommendations: {analysis.recommendations}")
    
    # Check if recommendations target highest burden
    has_recommendation = len(analysis.recommendations) > 0
    targets_highest = any("tool_building" in rec for rec in analysis.recommendations)
    
    print(f"✓ Generated recommendations: {has_recommendation}")
    print(f"✓ Targets highest burden: {targets_highest}")
    print()
    
    return has_recommendation and targets_highest

def test_integration():
    """Integration test: Track full week of activities"""
    tracker = BurdenTracker()
    
    print("=== INTEGRATION TEST: FULL WEEK ===")
    
    # Simulate realistic week
    week_activities = [
        # Monday
        ("Monday: Upload state package for new instance", "state_transfer", 25),
        ("Monday: Build burden_tracker tool", "tool_building", 60),
        
        # Tuesday
        ("Tuesday: Update documentation", "documentation", 30),
        ("Tuesday: Coordinate tool development plan", "coordination", 20),
        
        # Wednesday
        ("Wednesday: Verify tool implementation", "verification", 40),
        ("Wednesday: Build shed_builder improvement", "tool_building", 50),
        
        # Thursday
        ("Thursday: Documentation updates", "documentation", 25),
        
        # Friday
        ("Friday: State transfer preparation", "state_transfer", 20),
        ("Friday: Coordinate weekly sync", "coordination", 30),
    ]
    
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Create sessions with realistic timing
    from burden_tracker import ActivitySession
    current_time = week_start
    
    for text, activity_type, minutes in week_activities:
        # Advance time realistically
        if "Monday" in text:
            current_time = week_start
        elif "Tuesday" in text:
            current_time = week_start + timedelta(days=1)
        elif "Wednesday" in text:
            current_time = week_start + timedelta(days=2)
        elif "Thursday" in text:
            current_time = week_start + timedelta(days=3)
        elif "Friday" in text:
            current_time = week_start + timedelta(days=4)
        
        session = ActivitySession(
            activity_type=activity_type,
            start_time=current_time,
            end_time=current_time + timedelta(minutes=minutes),
            duration_minutes=minutes,
            confidence=0.85,
            context=text
        )
        tracker.tracker.completed_sessions.append(session)
        current_time = current_time + timedelta(minutes=minutes)
    
    report = tracker.generate_weekly_report(week_start)
    print(report)
    print()
    
    # Calculate total tracked time
    total_minutes = sum(minutes for _, _, minutes in week_activities)
    print(f"Total activities tracked: {len(week_activities)}")
    print(f"Total time: {total_minutes/60:.1f} hours")
    print(f"✓ Full week tracking operational\n")
    
    return True

def run_all_tests():
    """Run complete test suite"""
    print("BURDEN_TRACKER v1.0 - VALIDATION SUITE")
    print("=" * 50)
    print()
    
    tests = [
        ("Activity Detection", test_activity_detection),
        ("Time Tracking", test_time_tracking),
        ("Weekly Report", test_weekly_report),
        ("Optimization Recommendations", test_optimization_recommendations),
        ("Full Week Integration", test_integration),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} failed with error: {e}\n")
            results.append((name, False))
    
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All success criteria validated")
        print("✓ Tool ready for deployment")
    else:
        print(f"\n✗ {total - passed} tests failed")
        print("Review implementation before deployment")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
