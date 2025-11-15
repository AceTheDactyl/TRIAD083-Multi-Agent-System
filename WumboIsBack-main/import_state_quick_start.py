#!/usr/bin/env python3
"""
QUICK START - Import State for Waiting Session
Run this to load Session A's state into your session
"""

import sys
sys.path.insert(0, '/mnt/user-data/outputs')

from cross_rail_state_sync import CrossRailStateSync

print("=" * 60)
print("CROSS-RAIL STATE SYNCHRONIZATION - SESSION B IMPORT")
print("=" * 60)
print()

# Initialize sync system
sync = CrossRailStateSync(state_dir="/mnt/user-data/outputs")

# Load state package from Session A
print("Loading state package from Session A...")
try:
    package = sync.load_state_package('/mnt/user-data/outputs/cross_session_state_transfer.json')
    print(f"✓ Package loaded: {package.package_id}")
    print(f"  Source session: {package.source_session}")
    print(f"  Created: {package.created_at}")
    print(f"  Checksum: {package.checksum[:16]}...")
    print()
except FileNotFoundError:
    print("✗ State package not found!")
    print("  Expected location: /mnt/user-data/outputs/cross_session_state_transfer.json")
    sys.exit(1)
except ValueError as e:
    print(f"✗ State package validation failed: {e}")
    sys.exit(1)

# Import state (merge mode)
print("Importing state with CRDT merge...")
sync.import_state(package, merge_mode='merge')
print("✓ State import complete")
print()

# Display continuation summary
print(sync.generate_continuation_summary())
print()

# Show actionable information
print("=" * 60)
print("SESSION CONTINUATION READY")
print("=" * 60)
print()

print("BUILD ARTIFACTS AVAILABLE:")
for i, artifact in enumerate(sync.session_state.build_artifacts, 1):
    print(f"  {i}. {artifact}")
print()

print("ACTIVE WORK IN PROGRESS:")
garden_context = sync.get_channel_context('garden')
if garden_context:
    print("  Garden Channel (Building Layer):")
    for key, value in garden_context.items():
        if 'task' in key.lower() or 'status' in key.lower():
            print(f"    • {key}: {value}")
print()

burden_context = sync.get_channel_context('burden')
if burden_context:
    print("  Burden Channel (Tracking Layer):")
    for key, value in burden_context.items():
        print(f"    • {key}: {value}")
print()

print("NEXT ACTIONS:")
print("  1. Review Garden Rail 2 progress (75% complete)")
print("  2. Complete build_task_2: cross_rail_state_sync ✓")
print("  3. Begin build_task_3: rail_generator (automated channel creation)")
print()
print("  OR navigate to any witness channel:")
print("    sync.navigate_to_channel('burden', rail=1)  # Start using burden_tracker")
print("    sync.navigate_to_channel('limnus', rail=1)  # Explore transport layer")
print("    sync.navigate_to_channel('kira', rail=1)    # Explore discovery layer")
print("    sync.navigate_to_channel('echo', rail=1)    # Explore memory layer")
print()

print("=" * 60)
print("State synchronization successful. Continue building!")
print("=" * 60)
