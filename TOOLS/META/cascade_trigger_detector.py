#!/usr/bin/env python3
"""
CASCADE TRIGGER DETECTOR - Garden Rail 3 Layer 1
=================================================

Detects when cascade events are about to trigger and amplifies them proactively.

Cascade triggers:
- R₂ activates when R₁ > θ₁ (currently 8%)
- R₃ activates when R₂ > θ₂ (currently 12%)

Purpose: Lower effective thresholds by detecting and preparing for cascades early.

Usage:
    python cascade_trigger_detector.py --monitor
    python cascade_trigger_detector.py --detect-opportunities
"""

import json
import math
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class CascadeTriggerDetector:
    """Detects and amplifies cascade trigger opportunities."""

    def __init__(self):
        self.theta1 = 0.08  # R₂ activation threshold (8%)
        self.theta2 = 0.12  # R₃ activation threshold (12%)
        self.detection_margin = 0.02  # Detect 2% before threshold

        self.cascade_events = []
        self.opportunities_detected = []

    def detect_R2_opportunity(self, R1_current: float) -> Optional[Dict]:
        """
        Detect if R₂ cascade is approaching.

        Args:
            R1_current: Current R₁ burden reduction

        Returns:
            Opportunity dict if cascade approaching, None otherwise
        """
        threshold_proximity = self.theta1 - R1_current

        if 0 < threshold_proximity <= self.detection_margin:
            # R₂ cascade is approaching!
            opportunity = {
                "type": "R₂_approaching",
                "R1_current": R1_current,
                "threshold": self.theta1,
                "proximity": threshold_proximity,
                "proximity_percent": (threshold_proximity / self.theta1) * 100,
                "recommendation": "Amplify R₁ to trigger R₂ cascade",
                "estimated_impact": "R₂ will add ~25% burden reduction",
                "detected_at": datetime.now().isoformat()
            }

            self.opportunities_detected.append(opportunity)
            return opportunity

        elif R1_current >= self.theta1:
            # R₂ already active
            return {
                "type": "R₂_active",
                "R1_current": R1_current,
                "threshold": self.theta1,
                "status": "R₂ cascade already triggered",
                "detected_at": datetime.now().isoformat()
            }

        return None

    def detect_R3_opportunity(self, R2_current: float, R1_current: float) -> Optional[Dict]:
        """
        Detect if R₃ cascade is approaching.

        Args:
            R2_current: Current R₂ burden reduction
            R1_current: Current R₁ burden reduction (for context)

        Returns:
            Opportunity dict if cascade approaching, None otherwise
        """
        threshold_proximity = self.theta2 - R2_current

        if 0 < threshold_proximity <= self.detection_margin:
            # R₃ cascade is approaching!
            opportunity = {
                "type": "R₃_approaching",
                "R1_current": R1_current,
                "R2_current": R2_current,
                "threshold": self.theta2,
                "proximity": threshold_proximity,
                "proximity_percent": (threshold_proximity / self.theta2) * 100,
                "recommendation": "Amplify R₂ to trigger R₃ cascade",
                "estimated_impact": "R₃ will add ~20% burden reduction",
                "detected_at": datetime.now().isoformat()
            }

            self.opportunities_detected.append(opportunity)
            return opportunity

        elif R2_current >= self.theta2:
            # R₃ already active
            return {
                "type": "R₃_active",
                "R2_current": R2_current,
                "threshold": self.theta2,
                "status": "R₃ cascade already triggered",
                "detected_at": datetime.now().isoformat()
            }

        return None

    def calculate_cascade_state(self, z_level: float) -> Dict:
        """
        Calculate current cascade state from z-level using cascade model.

        Args:
            z_level: Current coordination density

        Returns:
            Dict with R₁, R₂, R₃ values and cascade state
        """
        # Simple Allen-Cahn for R₁
        z_c = 0.867
        sigma = 0.05
        R1 = 0.153 * math.exp(-((z_level - z_c)**2) / (2 * sigma**2))

        # R₂ calculation (conditional on R₁)
        smoothness = 20.0
        H_R2 = 1.0 / (1.0 + math.exp(-smoothness * (R1 - self.theta1)))
        R2 = 2.0 * R1 * H_R2

        # R₃ calculation (conditional on R₂)
        H_R3 = 1.0 / (1.0 + math.exp(-smoothness * (R2 - self.theta2)))
        R3 = 1.6 * R1 * H_R3

        return {
            "z_level": z_level,
            "R1_coordination": R1,
            "R2_meta_tools": R2,
            "R3_self_building": R3,
            "total_reduction": R1 + R2 + R3,
            "R2_active": R1 >= self.theta1,
            "R3_active": R2 >= self.theta2
        }

    def monitor_cascade_state(self, z_level: float) -> Dict:
        """
        Monitor current cascade state and detect opportunities.

        Args:
            z_level: Current coordination density

        Returns:
            Complete cascade monitoring report
        """
        state = self.calculate_cascade_state(z_level)

        # Detect opportunities
        R2_opp = self.detect_R2_opportunity(state["R1_coordination"])
        R3_opp = self.detect_R3_opportunity(state["R2_meta_tools"], state["R1_coordination"])

        opportunities = []
        if R2_opp and R2_opp["type"] == "R₂_approaching":
            opportunities.append(R2_opp)
        if R3_opp and R3_opp["type"] == "R₃_approaching":
            opportunities.append(R3_opp)

        report = {
            "timestamp": datetime.now().isoformat(),
            "z_level": z_level,
            "cascade_state": state,
            "opportunities": opportunities,
            "active_cascades": {
                "R2": state["R2_active"],
                "R3": state["R3_active"]
            },
            "recommendations": self._generate_recommendations(state, opportunities)
        }

        return report

    def _generate_recommendations(self, state: Dict, opportunities: List[Dict]) -> List[str]:
        """Generate actionable recommendations based on cascade state."""
        recommendations = []

        R1 = state["R1_coordination"]
        R2 = state["R2_meta_tools"]

        if opportunities:
            for opp in opportunities:
                recommendations.append(opp["recommendation"])

        # Additional strategic recommendations
        if not state["R2_active"]:
            gap = self.theta1 - R1
            recommendations.append(
                f"R₂ not yet active. Need {gap*100:.1f}% more R₁ reduction to trigger. "
                f"Focus on coordination optimization tools."
            )
        elif not state["R3_active"]:
            gap = self.theta2 - R2
            recommendations.append(
                f"R₃ not yet active. Need {gap*100:.1f}% more R₂ contribution to trigger. "
                f"Focus on meta-tool composition."
            )
        else:
            recommendations.append(
                "All cascades active! Focus on amplification: increase α, β factors."
            )

        return recommendations

    def simulate_cascade_trajectory(self, z_range: tuple = (0.80, 0.95), n_points: int = 50) -> List[Dict]:
        """
        Simulate cascade behavior across z-level range.

        Args:
            z_range: (z_min, z_max) to simulate
            n_points: Number of points to simulate

        Returns:
            List of cascade states across z-range
        """
        z_min, z_max = z_range
        trajectory = []

        for i in range(n_points):
            z = z_min + (z_max - z_min) * i / (n_points - 1)
            state = self.calculate_cascade_state(z)

            # Detect cascade trigger points
            if i > 0:
                prev_state = trajectory[-1]

                # Did R₂ just activate?
                if not prev_state["R2_active"] and state["R2_active"]:
                    state["cascade_event"] = "R₂ triggered"

                # Did R₃ just activate?
                if not prev_state["R3_active"] and state["R3_active"]:
                    state["cascade_event"] = "R₃ triggered"

            trajectory.append(state)

        return trajectory

    def identify_cascade_triggers(self, trajectory: List[Dict]) -> Dict:
        """
        Identify exact z-levels where cascades trigger.

        Args:
            trajectory: Cascade trajectory from simulate_cascade_trajectory

        Returns:
            Dict with trigger points
        """
        triggers = {
            "R2_trigger_z": None,
            "R3_trigger_z": None
        }

        for state in trajectory:
            if "cascade_event" in state:
                if state["cascade_event"] == "R₂ triggered":
                    triggers["R2_trigger_z"] = state["z_level"]
                elif state["cascade_event"] == "R₃ triggered":
                    triggers["R3_trigger_z"] = state["z_level"]

        return triggers

    def prepare_cascade_amplification(self, opportunity: Dict) -> Dict:
        """
        Prepare amplification strategy for detected opportunity.

        Args:
            opportunity: Opportunity dict from detect_R2/R3_opportunity

        Returns:
            Amplification strategy
        """
        strategy = {
            "opportunity_type": opportunity["type"],
            "detected_at": opportunity["detected_at"],
            "actions": []
        }

        if opportunity["type"] == "R₂_approaching":
            strategy["actions"] = [
                "Generate 1-2 CORE tools to push R₁ over threshold",
                "Prepare BRIDGES tools for R₂ cascade",
                "Ensure meta-tool composition infrastructure ready",
                "Lower θ₁ threshold if possible (currently 8%)"
            ]
            strategy["expected_gain"] = "~25% burden reduction from R₂"

        elif opportunity["type"] == "R₃_approaching":
            strategy["actions"] = [
                "Generate 2-3 BRIDGES tools to push R₂ over threshold",
                "Prepare META tools for R₃ cascade",
                "Ensure recursive improvement infrastructure ready",
                "Lower θ₂ threshold if possible (currently 12%)"
            ]
            strategy["expected_gain"] = "~20% burden reduction from R₃"

        return strategy

    def generate_report(self, z_level: float) -> Dict:
        """Generate comprehensive cascade detection report."""
        # Monitor current state
        current_report = self.monitor_cascade_state(z_level)

        # Simulate trajectory
        trajectory = self.simulate_cascade_trajectory()
        triggers = self.identify_cascade_triggers(trajectory)

        report = {
            "timestamp": datetime.now().isoformat(),
            "current_state": current_report,
            "cascade_triggers": triggers,
            "trajectory_simulated": len(trajectory),
            "opportunities_detected": len(self.opportunities_detected),
            "recommendations": current_report["recommendations"]
        }

        return report


def main():
    """Main entry point for cascade trigger detector."""
    import sys

    detector = CascadeTriggerDetector()
    z_level = 0.867  # Default to current z-level

    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == "--monitor":
            print("\n" + "="*60)
            print("CASCADE TRIGGER DETECTOR - Live Monitoring")
            print("="*60 + "\n")

            report = detector.monitor_cascade_state(z_level)

            print(f"Z-level: {report['z_level']}")
            print(f"Timestamp: {report['timestamp']}\n")

            print("CASCADE STATE:")
            state = report['cascade_state']
            print(f"  R₁ (coordination):   {state['R1_coordination']*100:.1f}%")
            print(f"  R₂ (meta-tools):     {state['R2_meta_tools']*100:.1f}%")
            print(f"  R₃ (self-building):  {state['R3_self_building']*100:.1f}%")
            print(f"  Total reduction:     {state['total_reduction']*100:.1f}%\n")

            print("ACTIVE CASCADES:")
            print(f"  R₂ active: {'✓ Yes' if report['active_cascades']['R2'] else '✗ No'}")
            print(f"  R₃ active: {'✓ Yes' if report['active_cascades']['R3'] else '✗ No'}\n")

            if report['opportunities']:
                print("⚠️  OPPORTUNITIES DETECTED:")
                for opp in report['opportunities']:
                    print(f"\n  {opp['type']}:")
                    print(f"    Proximity to threshold: {opp['proximity']*100:.1f}% ({opp['proximity_percent']:.0f}% of threshold)")
                    print(f"    {opp['recommendation']}")
                    print(f"    Estimated impact: {opp['estimated_impact']}")
            else:
                print("No immediate cascade opportunities detected.\n")

            print("RECOMMENDATIONS:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"  {i}. {rec}")

        elif arg == "--detect-opportunities":
            print("\n" + "="*60)
            print("CASCADE OPPORTUNITY DETECTION")
            print("="*60 + "\n")

            # Test at various z-levels to find opportunities
            test_z_levels = [0.80, 0.82, 0.84, 0.86, 0.867, 0.88, 0.90]

            for z in test_z_levels:
                report = detector.monitor_cascade_state(z)

                print(f"\nZ = {z:.3f}:")
                print(f"  R₁: {report['cascade_state']['R1_coordination']*100:.1f}%")
                print(f"  R₂: {report['cascade_state']['R2_meta_tools']*100:.1f}%")
                print(f"  R₃: {report['cascade_state']['R3_self_building']*100:.1f}%")

                if report['opportunities']:
                    for opp in report['opportunities']:
                        print(f"  ⚠️  {opp['type']}: {opp['recommendation']}")

        elif arg == "--simulate":
            print("\n" + "="*60)
            print("CASCADE TRAJECTORY SIMULATION")
            print("="*60 + "\n")

            trajectory = detector.simulate_cascade_trajectory()
            triggers = detector.identify_cascade_triggers(trajectory)

            print("Simulated 50 points from z=0.80 to z=0.95\n")

            print("CASCADE TRIGGER POINTS:")
            if triggers["R2_trigger_z"]:
                print(f"  R₂ triggers at z = {triggers['R2_trigger_z']:.3f}")
            if triggers["R3_trigger_z"]:
                print(f"  R₃ triggers at z = {triggers['R3_trigger_z']:.3f}")

            # Show key points
            print("\nKEY TRAJECTORY POINTS:")
            for state in trajectory[::10]:  # Every 10th point
                print(f"\n  z = {state['z_level']:.3f}:")
                print(f"    R₁: {state['R1_coordination']*100:.1f}%")
                print(f"    R₂: {state['R2_meta_tools']*100:.1f}%")
                print(f"    R₃: {state['R3_self_building']*100:.1f}%")
                print(f"    Total: {state['total_reduction']*100:.1f}%")
                if "cascade_event" in state:
                    print(f"    🎯 {state['cascade_event']}")

        else:
            print("Unknown argument. Use --monitor, --detect-opportunities, or --simulate")
    else:
        # Default: show current state
        print("\n" + "="*60)
        print("CASCADE TRIGGER DETECTOR")
        print("="*60)
        print(f"\nCurrent z-level: {z_level}")
        print("\nUsage:")
        print("  --monitor                 Monitor current cascade state")
        print("  --detect-opportunities    Detect cascade opportunities")
        print("  --simulate                Simulate cascade trajectory\n")


if __name__ == "__main__":
    main()
