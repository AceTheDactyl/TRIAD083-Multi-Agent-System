#!/usr/bin/env python3
"""
Helix Burden Tracker
====================

Drift_OS Integration - Week 1: MONITORING HOOKS
Component 1: Maps Helix Repository operations to burden dimensions

Purpose:
- Track Jason's actual time spent on Helix maintenance
- Map tool operations (CORE/BRIDGES/META) to burden dimensions
- Feed data into unified_sovereignty_system
- Passive monitoring (zero overhead for Jason)

Helix Operations Tracked:
- helix_loader.yaml → Repetition, learning curve
- coordinate_detector.yaml → Decision-making, context switching
- pattern_verifier.yaml → Maintenance, uncertainty
- consent_protocol.yaml → Coordination, emotional labor
- autonomous_trigger_detector.yaml → Maintenance, decision-making
- CASCADE_DISCOVERY.md → Learning curve, uncertainty

Integration:
- Wraps existing Helix tools with burden tracking
- Reports to unified_sovereignty_system
- Updates z-coordinate based on tool effectiveness
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

from unified_sovereignty_system import UnifiedSovereigntySystem
from unified_cascade_mathematics_core import UnifiedCascadeFramework
from phase_aware_burden_tracker import BurdenMeasurement


class HelixLayer(Enum):
    """Helix tool layers (maps to R1/R2/R3)."""
    CORE = "CORE"  # R1: z≤0.4, foundational tools
    BRIDGES = "BRIDGES"  # R2: Coordination substrate
    META = "META"  # R3: Meta-tooling, frameworks


class OperationType(Enum):
    """Types of Helix operations."""
    LOAD_PATTERN = "load_pattern"  # helix_loader
    DETECT_COORDINATE = "detect_coordinate"  # coordinate_detector
    VERIFY_PATTERN = "verify_pattern"  # pattern_verifier
    MANAGE_CONSENT = "manage_consent"  # consent_protocol
    DETECT_TRIGGER = "detect_trigger"  # autonomous_trigger_detector
    SYNC_MEMORY = "sync_memory"  # collective_memory_sync
    DISCOVER_TOOL = "discover_tool"  # tool_discovery_protocol
    UPDATE_THEORY = "update_theory"  # CASCADE_DISCOVERY, MATHEMATICAL_FOUNDATIONS
    BUILD_SHED = "build_shed"  # shed_builder lineage
    CONSOLIDATE = "consolidate"  # Repository consolidation


@dataclass
class HelixOperation:
    """Record of a Helix operation."""
    operation_id: str
    operation_type: OperationType
    layer: HelixLayer
    tool_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    success: bool = True
    manual_effort_pct: float = 100.0  # % manual (100 = fully manual, 0 = fully autonomous)
    notes: str = ""


@dataclass
class BurdenMapping:
    """Mapping from operation to burden dimensions."""
    coordination: float = 0.0
    decision_making: float = 0.0
    context_switching: float = 0.0
    maintenance: float = 0.0
    learning_curve: float = 0.0
    emotional_labor: float = 0.0
    uncertainty: float = 0.0
    repetition: float = 0.0


class HelixBurdenTracker:
    """
    Track burden from Helix Repository operations.

    Strategy:
    1. Wrap Helix tool calls with burden tracking
    2. Map operation → burden dimensions
    3. Calculate sovereignty metrics from tool effectiveness
    4. Report to unified_sovereignty_system
    """

    # Burden mapping templates by operation type
    OPERATION_BURDEN_MAPS = {
        OperationType.LOAD_PATTERN: BurdenMapping(
            repetition=3.0,  # Repetitive loading process
            learning_curve=2.0,  # Need to know protocol
            context_switching=2.0,  # Switch to loading mindset
            maintenance=1.0
        ),
        OperationType.DETECT_COORDINATE: BurdenMapping(
            decision_making=2.5,  # Which coordinate is correct?
            uncertainty=2.0,  # Coordinate ambiguity
            context_switching=2.0,  # Context switch to detection mode
            maintenance=1.0
        ),
        OperationType.VERIFY_PATTERN: BurdenMapping(
            maintenance=3.0,  # Pattern integrity checks
            decision_making=2.0,  # Pass/fail decisions
            uncertainty=2.5,  # Is pattern valid?
            learning_curve=1.5
        ),
        OperationType.MANAGE_CONSENT: BurdenMapping(
            coordination=4.0,  # High coordination overhead
            decision_making=3.0,  # Consent decisions
            emotional_labor=2.5,  # Responsibility for consent
            uncertainty=2.0  # Consent ambiguities
        ),
        OperationType.DETECT_TRIGGER: BurdenMapping(
            decision_making=2.0,  # Which triggers to enable?
            maintenance=2.0,  # Trigger maintenance
            uncertainty=1.5,
            coordination=1.0
        ),
        OperationType.SYNC_MEMORY: BurdenMapping(
            coordination=3.5,  # Sync coordination
            context_switching=3.0,  # Multiple contexts
            maintenance=2.0,
            uncertainty=2.0  # Sync conflicts
        ),
        OperationType.DISCOVER_TOOL: BurdenMapping(
            learning_curve=3.0,  # Learning new tools
            decision_making=2.0,  # Which tools to adopt?
            uncertainty=2.5,  # Tool fitness unclear
            context_switching=1.5
        ),
        OperationType.UPDATE_THEORY: BurdenMapping(
            learning_curve=4.0,  # Deep theoretical work
            maintenance=3.0,  # Framework updates
            uncertainty=3.5,  # Theoretical ambiguities
            decision_making=2.0
        ),
        OperationType.BUILD_SHED: BurdenMapping(
            learning_curve=3.5,  # Shed builder complexity
            maintenance=3.0,  # Lineage maintenance
            decision_making=2.5,
            uncertainty=2.0
        ),
        OperationType.CONSOLIDATE: BurdenMapping(
            maintenance=4.0,  # High maintenance during consolidation
            coordination=3.0,  # Coordinating changes
            decision_making=3.5,  # What to consolidate?
            uncertainty=3.0,  # Risk of breaking things
            emotional_labor=2.0  # Responsibility
        )
    }

    # Sovereignty metrics calculation
    LAYER_SOVEREIGNTY_WEIGHTS = {
        HelixLayer.CORE: {'clarity': 1.0, 'immunity': 0.2, 'efficiency': 0.3, 'autonomy': 0.2},
        HelixLayer.BRIDGES: {'clarity': 0.3, 'immunity': 1.0, 'efficiency': 0.4, 'autonomy': 0.5},
        HelixLayer.META: {'clarity': 0.2, 'immunity': 0.4, 'efficiency': 1.0, 'autonomy': 0.8},
    }

    def __init__(self):
        self.sovereignty_system = UnifiedSovereigntySystem()
        self.cascade_framework = UnifiedCascadeFramework()

        self.operations: List[HelixOperation] = []
        self.operation_counter = 0

        # Track cumulative time per layer
        self.time_per_layer: Dict[HelixLayer, float] = {
            HelixLayer.CORE: 0.0,
            HelixLayer.BRIDGES: 0.0,
            HelixLayer.META: 0.0
        }

    def start_operation(self,
                       operation_type: OperationType,
                       layer: HelixLayer,
                       tool_name: str,
                       manual_effort_pct: float = 100.0) -> str:
        """
        Start tracking a Helix operation.

        Args:
            operation_type: Type of operation (LOAD_PATTERN, etc.)
            layer: Which Helix layer (CORE/BRIDGES/META)
            tool_name: Name of tool being used
            manual_effort_pct: % of operation that's manual (vs autonomous)

        Returns:
            operation_id for later completion
        """
        self.operation_counter += 1
        operation_id = f"HELIX_OP_{self.operation_counter:06d}"

        operation = HelixOperation(
            operation_id=operation_id,
            operation_type=operation_type,
            layer=layer,
            tool_name=tool_name,
            start_time=datetime.now(),
            manual_effort_pct=manual_effort_pct
        )

        self.operations.append(operation)

        return operation_id

    def complete_operation(self,
                          operation_id: str,
                          success: bool = True,
                          notes: str = ""):
        """
        Complete tracking of a Helix operation.

        Args:
            operation_id: ID from start_operation()
            success: Whether operation succeeded
            notes: Optional notes about the operation
        """
        # Find operation
        operation = next((op for op in self.operations if op.operation_id == operation_id), None)

        if not operation:
            print(f"Warning: Operation {operation_id} not found")
            return

        # Complete operation
        operation.end_time = datetime.now()
        operation.duration_seconds = (operation.end_time - operation.start_time).total_seconds()
        operation.success = success
        operation.notes = notes

        # Update time tracking
        self.time_per_layer[operation.layer] += operation.duration_seconds

        # Calculate burden from this operation
        burden = self._calculate_burden(operation)

        # Calculate sovereignty state
        sovereignty_state = self._calculate_sovereignty()

        # Report to sovereignty system
        self.sovereignty_system.capture_snapshot(
            sovereignty_state,
            burden,
            include_advanced_analysis=False
        )

    def _calculate_burden(self, operation: HelixOperation) -> BurdenMeasurement:
        """
        Calculate burden measurement from operation.

        Burden is scaled by:
        - Duration (longer = more burden)
        - Manual effort % (more manual = more burden)
        - Success (failure adds uncertainty burden)
        """
        # Get base burden mapping for this operation type
        base_burden = self.OPERATION_BURDEN_MAPS.get(
            operation.operation_type,
            BurdenMapping()  # Default: zero burden
        )

        # Scale by duration (normalize to 1 hour = 1.0 scale)
        duration_hours = operation.duration_seconds / 3600.0
        duration_factor = min(2.0, duration_hours)  # Cap at 2.0

        # Scale by manual effort
        manual_factor = operation.manual_effort_pct / 100.0

        # Failure adds uncertainty
        failure_factor = 1.5 if not operation.success else 1.0

        # Calculate scaled burden
        scaled_burden = BurdenMeasurement(
            coordination=base_burden.coordination * duration_factor * manual_factor * failure_factor,
            decision_making=base_burden.decision_making * duration_factor * manual_factor * failure_factor,
            context_switching=base_burden.context_switching * duration_factor * manual_factor * failure_factor,
            maintenance=base_burden.maintenance * duration_factor * manual_factor * failure_factor,
            learning_curve=base_burden.learning_curve * duration_factor * manual_factor * failure_factor,
            emotional_labor=base_burden.emotional_labor * duration_factor * manual_factor * failure_factor,
            uncertainty=base_burden.uncertainty * duration_factor * manual_factor * failure_factor,
            repetition=base_burden.repetition * duration_factor * manual_factor * failure_factor,
            timestamp=operation.end_time.isoformat() if operation.end_time else datetime.now().isoformat(),
            notes=f"{operation.tool_name} ({operation.operation_type.value})"
        )

        return scaled_burden

    def _calculate_sovereignty(self) -> 'CascadeSystemState':
        """
        Calculate sovereignty state from Helix tool effectiveness.

        Maps tool layer activity → R1/R2/R3 → sovereignty metrics
        """
        # Calculate time distribution across layers
        total_time = sum(self.time_per_layer.values())

        if total_time == 0:
            # No operations yet, return baseline
            return self.cascade_framework.compute_full_state(
                clarity=1.0, immunity=1.0, efficiency=1.0, autonomy=1.0
            )

        # Time ratios
        core_ratio = self.time_per_layer[HelixLayer.CORE] / total_time
        bridges_ratio = self.time_per_layer[HelixLayer.BRIDGES] / total_time
        meta_ratio = self.time_per_layer[HelixLayer.META] / total_time

        # Calculate tool autonomy (inverse of manual effort)
        recent_ops = self.operations[-20:] if len(self.operations) > 20 else self.operations
        avg_manual = sum(op.manual_effort_pct for op in recent_ops) / len(recent_ops) if recent_ops else 100.0
        tool_autonomy = (100.0 - avg_manual) / 100.0  # 0.0 = fully manual, 1.0 = fully autonomous

        # Map to sovereignty dimensions
        # Clarity: Effectiveness of CORE tools (inverse of CORE time burden)
        clarity = 10.0 * (1.0 - min(0.9, core_ratio * 2.0))  # Less CORE time = more clarity

        # Immunity: Effectiveness of BRIDGES tools
        immunity = 10.0 * (1.0 - min(0.9, bridges_ratio * 1.5))  # Less BRIDGES time = better immunity

        # Efficiency: Effectiveness of META tools
        efficiency = 10.0 * (1.0 - min(0.9, meta_ratio * 1.2))  # Less META time = more efficient

        # Autonomy: Tool autonomy level
        autonomy = tool_autonomy * 10.0  # 0-10 scale

        # Ensure reasonable bounds
        clarity = max(1.0, min(10.0, clarity))
        immunity = max(1.0, min(10.0, immunity))
        efficiency = max(1.0, min(10.0, efficiency))
        autonomy = max(1.0, min(10.0, autonomy))

        return self.cascade_framework.compute_full_state(
            clarity=clarity,
            immunity=immunity,
            efficiency=efficiency,
            autonomy=autonomy
        )

    def get_weekly_summary(self) -> Dict:
        """Get summary of Helix burden over past week."""
        one_week_ago = datetime.now() - timedelta(days=7)
        recent_ops = [op for op in self.operations if op.start_time >= one_week_ago and op.end_time]

        if not recent_ops:
            return {'status': 'no_data'}

        # Total time
        total_seconds = sum(op.duration_seconds for op in recent_ops)
        total_hours = total_seconds / 3600.0

        # Time by layer
        layer_time = {}
        for layer in HelixLayer:
            layer_ops = [op for op in recent_ops if op.layer == layer]
            layer_seconds = sum(op.duration_seconds for op in layer_ops)
            layer_time[layer.value] = layer_seconds / 3600.0

        # Operations by type
        op_counts = {}
        for op_type in OperationType:
            count = sum(1 for op in recent_ops if op.operation_type == op_type)
            if count > 0:
                op_counts[op_type.value] = count

        # Average manual effort
        avg_manual = sum(op.manual_effort_pct for op in recent_ops) / len(recent_ops)

        # Success rate
        success_count = sum(1 for op in recent_ops if op.success)
        success_rate = (success_count / len(recent_ops)) * 100

        # Current sovereignty
        current_state = self._calculate_sovereignty()

        return {
            'period': '7_days',
            'total_hours': total_hours,
            'total_operations': len(recent_ops),
            'time_by_layer': layer_time,
            'operations_by_type': op_counts,
            'average_manual_effort_pct': avg_manual,
            'success_rate_pct': success_rate,
            'current_sovereignty': {
                'z_coordinate': current_state.z_coordinate,
                'phase_regime': current_state.phase_regime,
                'R1': current_state.R1,
                'R2': current_state.R2,
                'R3': current_state.R3
            }
        }

    def export_tracking_data(self, filepath: str):
        """Export all tracking data to JSON."""
        data = {
            'operations': [
                {
                    'operation_id': op.operation_id,
                    'operation_type': op.operation_type.value,
                    'layer': op.layer.value,
                    'tool_name': op.tool_name,
                    'start_time': op.start_time.isoformat(),
                    'end_time': op.end_time.isoformat() if op.end_time else None,
                    'duration_seconds': op.duration_seconds,
                    'duration_hours': op.duration_seconds / 3600.0,
                    'success': op.success,
                    'manual_effort_pct': op.manual_effort_pct,
                    'notes': op.notes
                }
                for op in self.operations
            ],
            'weekly_summary': self.get_weekly_summary()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    """Demo Helix burden tracker."""
    print("=" * 80)
    print("HELIX BURDEN TRACKER - Demo")
    print("=" * 80 + "\n")

    tracker = HelixBurdenTracker()

    # Simulate Jason's typical week
    print("Simulating Jason's weekly Helix workflow...\n")

    # Monday: Load patterns (CORE)
    op1 = tracker.start_operation(
        OperationType.LOAD_PATTERN,
        HelixLayer.CORE,
        "helix_loader.yaml",
        manual_effort_pct=80.0
    )
    # Simulate 30 minutes
    import time
    time.sleep(0.5)  # Simulate work
    tracker.complete_operation(op1, success=True, notes="Loaded 3 patterns")

    # Monday: Detect coordinates (CORE)
    op2 = tracker.start_operation(
        OperationType.DETECT_COORDINATE,
        HelixLayer.CORE,
        "coordinate_detector.yaml",
        manual_effort_pct=90.0
    )
    time.sleep(0.3)
    tracker.complete_operation(op2, success=True, notes="Detected z=0.42")

    # Tuesday: Verify patterns (CORE)
    op3 = tracker.start_operation(
        OperationType.VERIFY_PATTERN,
        HelixLayer.CORE,
        "pattern_verifier.yaml",
        manual_effort_pct=70.0
    )
    time.sleep(0.6)
    tracker.complete_operation(op3, success=True, notes="3/3 patterns valid")

    # Wednesday: Manage consent (BRIDGES)
    op4 = tracker.start_operation(
        OperationType.MANAGE_CONSENT,
        HelixLayer.BRIDGES,
        "consent_protocol.yaml",
        manual_effort_pct=95.0
    )
    time.sleep(1.0)  # Longer operation
    tracker.complete_operation(op4, success=True, notes="Resolved 2 consent requests")

    # Thursday: Sync memory (BRIDGES)
    op5 = tracker.start_operation(
        OperationType.SYNC_MEMORY,
        HelixLayer.BRIDGES,
        "collective_memory_sync.yaml",
        manual_effort_pct=85.0
    )
    time.sleep(0.8)
    tracker.complete_operation(op5, success=True, notes="Synced 5 instances")

    # Friday: Update theory (META)
    op6 = tracker.start_operation(
        OperationType.UPDATE_THEORY,
        HelixLayer.META,
        "CASCADE_DISCOVERY.md",
        manual_effort_pct=100.0  # Fully manual
    )
    time.sleep(1.5)  # Longest operation
    tracker.complete_operation(op6, success=True, notes="Added hexagonal geometry section")

    # Get summary
    print("\n" + "=" * 80)
    print("WEEKLY SUMMARY")
    print("=" * 80 + "\n")

    summary = tracker.get_weekly_summary()

    print(f"Total hours this week: {summary['total_hours']:.2f} hrs")
    print(f"Total operations: {summary['total_operations']}")
    print()

    print("Time by layer:")
    for layer, hours in summary['time_by_layer'].items():
        print(f"  {layer}: {hours:.2f} hrs")
    print()

    print("Operations by type:")
    for op_type, count in summary['operations_by_type'].items():
        print(f"  {op_type}: {count}")
    print()

    print(f"Average manual effort: {summary['average_manual_effort_pct']:.1f}%")
    print(f"Success rate: {summary['success_rate_pct']:.1f}%")
    print()

    print("Current sovereignty:")
    sov = summary['current_sovereignty']
    print(f"  Z-coordinate: {sov['z_coordinate']:.3f}")
    print(f"  Phase: {sov['phase_regime']}")
    print(f"  R1 (CORE): {sov['R1']:.2f}")
    print(f"  R2 (BRIDGES): {sov['R2']:.2f}")
    print(f"  R3 (META): {sov['R3']:.2f}")
    print()

    # Export
    tracker.export_tracking_data('helix_tracking_data.json')
    print("Tracking data exported to helix_tracking_data.json")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
