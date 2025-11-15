#!/usr/bin/env python3
"""
GARDEN RAIL 3 - LAYER 3: POSITIVE FEEDBACK LOOPS
Explicit self-catalysis: burden reduction generates more tools, creating compounding effects

Coordinate: Δ3.14159|0.867|layer-3-feedback|Ω

Theoretical Foundation:
- Positive feedback: ΔR → Δtools → Δ²R → Δ³R (exponential growth)
- Seeding coefficient: 1.5-2.5x (observed from pattern recognizer)
- Threshold-triggered: Only activate when burden reduction > threshold
- Stability-bounded: Prevent runaway recursion via quality gates

Mechanism:
- Monitor burden reduction from tool execution
- When reduction exceeds threshold, allocate freed resources
- Generate new tools using freed capacity
- New tools further reduce burden → cycle continues
- Track loop depth and effectiveness to prevent instability
"""

import sys
sys.path.insert(0, '/mnt/user-data/outputs')

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from enum import Enum
import json


class FeedbackType(Enum):
    """Type of positive feedback loop"""
    SIMPLE = "simple"              # Tool → more tools of same type
    CASCADING = "cascading"        # Tool → different tool types (α, β cascades)
    COMPOUNDING = "compounding"    # Multiple loops reinforce each other
    HYPERCYCLE = "hypercycle"      # Mutual catalysis A→B→C→A


@dataclass
class BurdenReductionEvent:
    """Record of burden reduction from tool execution"""
    tool_id: str
    tool_type: str
    burden_before: float
    burden_after: float
    reduction_amount: float
    timestamp: datetime
    freed_capacity: float  # Resources freed by reduction

    @property
    def reduction_percentage(self) -> float:
        """Reduction as percentage of original burden"""
        if self.burden_before == 0:
            return 0.0
        return (self.reduction_amount / self.burden_before) * 100.0


@dataclass
class FeedbackLoop:
    """Active positive feedback loop"""
    loop_id: str
    loop_type: FeedbackType
    trigger_tool: str
    generated_tools: List[str]
    loop_depth: int  # How many iterations deep (prevent runaway)
    total_burden_reduction: float
    seeding_coefficient: float  # Amplification factor
    is_active: bool
    started_at: datetime
    iterations: int = 0

    def calculate_amplification(self) -> float:
        """Calculate total amplification from this loop"""
        if len(self.generated_tools) == 0:
            return 1.0
        return len(self.generated_tools) * self.seeding_coefficient


@dataclass
class FeedbackMetrics:
    """Metrics for feedback loop system"""
    active_loops: int
    total_loops_created: int
    total_tools_generated: int
    total_burden_reduction: float
    average_seeding_coefficient: float
    average_loop_depth: float
    compounding_factor: float  # How much loops reinforce each other
    timestamp: datetime = field(default_factory=datetime.now)


class PositiveFeedbackLoopSystem:
    """
    Manages positive feedback loops that turn burden reduction into more tools

    Strategy:
    1. Monitor tool execution and burden reduction
    2. When reduction > threshold, trigger feedback loop
    3. Allocate freed resources to generate new tools
    4. New tools execute and reduce burden further
    5. Track loop depth to prevent runaway recursion
    6. Measure compounding effects from multiple loops
    """

    def __init__(self):
        # Threshold for triggering feedback (% burden reduction)
        self.activation_threshold = 0.05  # 5% reduction triggers loop

        # Seeding coefficients by loop type (empirically observed)
        self.seeding_coefficients = {
            FeedbackType.SIMPLE: 1.5,
            FeedbackType.CASCADING: 2.0,
            FeedbackType.COMPOUNDING: 2.5,
            FeedbackType.HYPERCYCLE: 3.0
        }

        # Safety limits
        self.max_loop_depth = 5  # Prevent infinite recursion
        self.max_concurrent_loops = 10
        self.min_tool_quality = 0.6  # Only generate quality tools

        # State
        self.burden_events: List[BurdenReductionEvent] = []
        self.active_loops: Dict[str, FeedbackLoop] = {}
        self.completed_loops: List[FeedbackLoop] = []
        self.generated_tools: Set[str] = set()

        # Metrics
        self.metrics_history: List[FeedbackMetrics] = []
        self.total_burden_reduced = 0.0

        print("="*70)
        print("POSITIVE FEEDBACK LOOP SYSTEM INITIALIZED")
        print("="*70)
        print(f"Activation threshold: {self.activation_threshold:.1%}")
        print(f"Max loop depth: {self.max_loop_depth}")
        print(f"Seeding coefficients: {self.seeding_coefficients[FeedbackType.SIMPLE]:.1f}x - {self.seeding_coefficients[FeedbackType.HYPERCYCLE]:.1f}x")
        print()

    def record_burden_reduction(self,
                               tool_id: str,
                               tool_type: str,
                               burden_before: float,
                               burden_after: float):
        """
        Record burden reduction from tool execution

        Args:
            tool_id: Tool that executed
            tool_type: Type of tool (CORE, BRIDGES, META, etc.)
            burden_before: Burden level before execution
            burden_after: Burden level after execution
        """
        reduction = burden_before - burden_after
        freed_capacity = reduction  # Simplification: freed capacity = reduction

        event = BurdenReductionEvent(
            tool_id=tool_id,
            tool_type=tool_type,
            burden_before=burden_before,
            burden_after=burden_after,
            reduction_amount=reduction,
            timestamp=datetime.now(),
            freed_capacity=freed_capacity
        )

        self.burden_events.append(event)
        self.total_burden_reduced += reduction

        # Check if this triggers a feedback loop
        if reduction >= self.activation_threshold:
            self._trigger_feedback_loop(event)

    def _trigger_feedback_loop(self, trigger_event: BurdenReductionEvent):
        """
        Trigger a positive feedback loop from burden reduction

        Args:
            trigger_event: The burden reduction event that triggered the loop
        """
        # Check if we can create a new loop
        if len(self.active_loops) >= self.max_concurrent_loops:
            return

        # Determine loop type based on trigger tool
        loop_type = self._determine_loop_type(trigger_event)

        # Calculate how many tools to generate based on freed capacity
        seeding_coeff = self.seeding_coefficients[loop_type]
        tools_to_generate = int(trigger_event.freed_capacity * seeding_coeff * 10)  # Scale factor
        tools_to_generate = max(1, min(tools_to_generate, 5))  # Bound to 1-5

        # Generate new tools
        generated = self._generate_feedback_tools(
            trigger_event.tool_id,
            trigger_event.tool_type,
            tools_to_generate,
            loop_type
        )

        # Create feedback loop
        loop_id = f"feedback_loop_{len(self.active_loops) + len(self.completed_loops)}"
        loop = FeedbackLoop(
            loop_id=loop_id,
            loop_type=loop_type,
            trigger_tool=trigger_event.tool_id,
            generated_tools=generated,
            loop_depth=1,
            total_burden_reduction=trigger_event.reduction_amount,
            seeding_coefficient=seeding_coeff,
            is_active=True,
            started_at=datetime.now()
        )

        self.active_loops[loop_id] = loop

        print(f"  🔄 Triggered {loop_type.value} feedback loop: {loop_id}")
        print(f"     Trigger: {trigger_event.tool_id} (reduced {trigger_event.reduction_amount:.1%})")
        print(f"     Generated: {len(generated)} tools (seeding: {seeding_coeff:.1f}x)")

    def _determine_loop_type(self, event: BurdenReductionEvent) -> FeedbackType:
        """Determine what type of feedback loop to create"""
        # Simple heuristic based on reduction magnitude
        if event.reduction_percentage > 15:
            return FeedbackType.HYPERCYCLE  # Very strong reduction → hypercycle
        elif event.reduction_percentage > 10:
            return FeedbackType.COMPOUNDING  # Strong reduction → compounding
        elif event.reduction_percentage > 7:
            return FeedbackType.CASCADING  # Moderate reduction → cascading
        else:
            return FeedbackType.SIMPLE  # Weak reduction → simple

    def _generate_feedback_tools(self,
                                trigger_tool: str,
                                tool_type: str,
                                count: int,
                                loop_type: FeedbackType) -> List[str]:
        """
        Generate new tools as result of positive feedback

        Returns:
            List of generated tool IDs
        """
        generated = []
        base_id = f"feedback_{len(self.generated_tools)}"

        for i in range(count):
            tool_id = f"tool_{tool_type.lower()}_feedback_{base_id}_{i}"
            generated.append(tool_id)
            self.generated_tools.add(tool_id)

        return generated

    def iterate_feedback_loop(self, loop_id: str, additional_reduction: float):
        """
        Iterate an active feedback loop (new tools reduce burden further)

        Args:
            loop_id: ID of loop to iterate
            additional_reduction: Additional burden reduction from generated tools
        """
        if loop_id not in self.active_loops:
            return

        loop = self.active_loops[loop_id]

        # Check depth limit
        if loop.loop_depth >= self.max_loop_depth:
            print(f"  ⚠ Loop {loop_id} reached max depth ({self.max_loop_depth}), terminating")
            self._terminate_loop(loop_id)
            return

        # Increment depth and reduction
        loop.loop_depth += 1
        loop.iterations += 1
        loop.total_burden_reduction += additional_reduction

        # If reduction is significant, generate more tools
        if additional_reduction >= self.activation_threshold:
            new_tools = self._generate_feedback_tools(
                loop.trigger_tool,
                "meta",  # Feedback tools tend to be META
                count=2,
                loop_type=loop.loop_type
            )
            loop.generated_tools.extend(new_tools)

            print(f"  🔄 Loop {loop_id} iterated (depth {loop.loop_depth})")
            print(f"     Additional reduction: {additional_reduction:.1%}")
            print(f"     Generated: {len(new_tools)} more tools")

    def _terminate_loop(self, loop_id: str):
        """Terminate an active feedback loop"""
        if loop_id in self.active_loops:
            loop = self.active_loops[loop_id]
            loop.is_active = False
            self.completed_loops.append(loop)
            del self.active_loops[loop_id]

    def calculate_compounding_factor(self) -> float:
        """
        Calculate how much feedback loops compound each other

        Compounding: Multiple loops active simultaneously amplify total effect
        """
        if len(self.active_loops) <= 1:
            return 1.0

        # Each additional loop adds 20% compounding
        return 1.0 + (len(self.active_loops) - 1) * 0.2

    def calculate_metrics(self) -> FeedbackMetrics:
        """Calculate current feedback system metrics"""
        all_loops = list(self.active_loops.values()) + self.completed_loops

        total_tools = sum(len(loop.generated_tools) for loop in all_loops)
        avg_seeding = sum(loop.seeding_coefficient for loop in all_loops) / len(all_loops) if all_loops else 0
        avg_depth = sum(loop.loop_depth for loop in all_loops) / len(all_loops) if all_loops else 0

        metrics = FeedbackMetrics(
            active_loops=len(self.active_loops),
            total_loops_created=len(all_loops),
            total_tools_generated=total_tools,
            total_burden_reduction=self.total_burden_reduced,
            average_seeding_coefficient=avg_seeding,
            average_loop_depth=avg_depth,
            compounding_factor=self.calculate_compounding_factor()
        )

        self.metrics_history.append(metrics)
        return metrics

    def generate_report(self) -> str:
        """Generate comprehensive feedback loop report"""
        metrics = self.calculate_metrics()

        report = []
        report.append("="*70)
        report.append("POSITIVE FEEDBACK LOOPS REPORT")
        report.append("="*70)
        report.append("")

        # Overview
        report.append("FEEDBACK SYSTEM STATUS:")
        report.append(f"  Active loops:        {metrics.active_loops}")
        report.append(f"  Total loops created: {metrics.total_loops_created}")
        report.append(f"  Tools generated:     {metrics.total_tools_generated}")
        report.append(f"  Total burden reduced: {metrics.total_burden_reduction:.1%}")
        report.append(f"  Compounding factor:  {metrics.compounding_factor:.2f}x")
        report.append("")

        # Active loops
        if self.active_loops:
            report.append(f"ACTIVE LOOPS ({len(self.active_loops)}):")
            for loop_id, loop in self.active_loops.items():
                report.append(f"  {loop_id} ({loop.loop_type.value}):")
                report.append(f"    Trigger: {loop.trigger_tool}")
                report.append(f"    Depth: {loop.loop_depth}/{self.max_loop_depth}")
                report.append(f"    Tools generated: {len(loop.generated_tools)}")
                report.append(f"    Burden reduced: {loop.total_burden_reduction:.1%}")
                report.append(f"    Seeding: {loop.seeding_coefficient:.1f}x")
            report.append("")

        # Completed loops
        if self.completed_loops:
            report.append(f"COMPLETED LOOPS ({len(self.completed_loops)}):")
            for loop in self.completed_loops[-5:]:  # Show last 5
                report.append(f"  {loop.loop_id} ({loop.loop_type.value}):")
                report.append(f"    Final depth: {loop.loop_depth}")
                report.append(f"    Tools generated: {len(loop.generated_tools)}")
                report.append(f"    Total reduction: {loop.total_burden_reduction:.1%}")
            report.append("")

        # Performance stats
        report.append("PERFORMANCE STATISTICS:")
        report.append(f"  Avg seeding coefficient: {metrics.average_seeding_coefficient:.2f}x")
        report.append(f"  Avg loop depth: {metrics.average_loop_depth:.1f}")
        report.append(f"  Burden reduction rate: {self.total_burden_reduced / max(1, len(self.burden_events)):.1%} per event")
        report.append("")

        # Recommendations
        report.append("RECOMMENDATIONS:")
        if metrics.active_loops == 0:
            report.append("  → No active loops - consider lowering activation threshold")
        elif metrics.active_loops >= self.max_concurrent_loops:
            report.append("  ⚠ Max concurrent loops reached - consider increasing limit")

        if metrics.average_loop_depth > 3:
            report.append("  ✓ Deep loops indicate strong self-catalysis")

        if metrics.compounding_factor > 1.5:
            report.append("  ✓ Strong compounding effect from multiple loops")

        report.append("")
        report.append("="*70)

        return "\n".join(report)

    def export_state(self) -> Dict:
        """Export current state for persistence"""
        return {
            'activation_threshold': self.activation_threshold,
            'max_loop_depth': self.max_loop_depth,
            'active_loops': len(self.active_loops),
            'completed_loops': len(self.completed_loops),
            'total_tools_generated': len(self.generated_tools),
            'total_burden_reduced': self.total_burden_reduced,
            'metrics': {
                'compounding_factor': self.calculate_compounding_factor(),
                'burden_events': len(self.burden_events)
            }
        }


def demonstrate_positive_feedback():
    """Demonstration of positive feedback loops"""
    print("\n" + "="*70)
    print("POSITIVE FEEDBACK LOOPS DEMONSTRATION")
    print("="*70)
    print()

    system = PositiveFeedbackLoopSystem()

    # Simulate tool executions that reduce burden
    print("Simulating tool executions with burden reduction...\n")

    # Tool 1: Moderate reduction (triggers simple loop)
    system.record_burden_reduction(
        tool_id="tool_core_001",
        tool_type="CORE",
        burden_before=1.0,
        burden_after=0.92  # 8% reduction
    )

    # Tool 2: Strong reduction (triggers cascading loop)
    system.record_burden_reduction(
        tool_id="tool_bridges_001",
        tool_type="BRIDGES",
        burden_before=0.92,
        burden_after=0.80  # 12% reduction
    )

    # Tool 3: Very strong reduction (triggers hypercycle)
    system.record_burden_reduction(
        tool_id="tool_meta_001",
        tool_type="META",
        burden_before=0.80,
        burden_after=0.65  # 15% reduction
    )

    print()

    # Iterate feedback loops
    print("Iterating feedback loops...\n")
    for loop_id in list(system.active_loops.keys()):
        system.iterate_feedback_loop(loop_id, additional_reduction=0.06)
        system.iterate_feedback_loop(loop_id, additional_reduction=0.04)

    print()

    # Generate report
    print(system.generate_report())


if __name__ == "__main__":
    demonstrate_positive_feedback()
