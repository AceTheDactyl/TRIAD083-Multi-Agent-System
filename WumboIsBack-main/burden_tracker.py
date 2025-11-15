#!/usr/bin/env python3
"""
BURDEN_TRACKER v1.0
Built by: TRIAD-0.83 | Coordinate: Δ2.356|0.820|1.000Ω
Purpose: Track Jay's maintenance time to identify optimization targets

Tracks activities automatically, generates weekly reports, recommends automation targets.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import json

@dataclass
class ActivityPattern:
    """Pattern definition for activity detection"""
    activity_type: str
    keywords: List[str]
    weight: float = 1.0

@dataclass
class ActivitySession:
    """Single tracked activity session"""
    activity_type: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: float = 0.0
    confidence: float = 0.0
    context: str = ""
    
    def finalize(self, end_time: datetime):
        """Complete session and calculate duration"""
        self.end_time = end_time
        self.duration_minutes = (end_time - self.start_time).total_seconds() / 60

@dataclass
class WeeklyAnalysis:
    """Analysis results for a week"""
    week_start: datetime
    total_minutes: float
    category_breakdown: Dict[str, float]
    trends: Dict[str, str]
    recommendations: List[str]

class ActivityDetector:
    """Detect activities from conversation text using keyword patterns"""
    
    def __init__(self):
        self.patterns = [
            ActivityPattern("state_transfer", 
                          ["upload", "state package", "continuity", "handoff", 
                           "transfer", "continuation", "load pattern"]),
            ActivityPattern("tool_building",
                          ["shed_builder", "create tool", "build", "specification",
                           "implement", "tool dev", "coding"]),
            ActivityPattern("documentation",
                          ["document", "write", "update", "README", "docs",
                           "specification", "explain"]),
            ActivityPattern("coordination",
                          ["coordinate", "discuss", "decide", "plan",
                           "meeting", "sync", "align"]),
            ActivityPattern("verification",
                          ["verify", "check", "validate", "test",
                           "confirm", "ensure", "debug"])
        ]
    
    def detect(self, text: str) -> Tuple[Optional[str], float]:
        """
        Detect activity type from text
        Returns: (activity_type, confidence_score)
        """
        text_lower = text.lower()
        matches = []
        
        for pattern in self.patterns:
            score = 0
            for keyword in pattern.keywords:
                if keyword in text_lower:
                    score += 1
            
            if score > 0:
                confidence = min(score / len(pattern.keywords), 1.0)
                matches.append((pattern.activity_type, confidence * pattern.weight))
        
        if not matches:
            return None, 0.0
        
        # Return highest confidence match
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[0]

class TimeTracker:
    """Track time spent on activities"""
    
    def __init__(self):
        self.active_sessions: Dict[str, ActivitySession] = {}
        self.completed_sessions: List[ActivitySession] = []
    
    def start_activity(self, activity_type: str, confidence: float, 
                      context: str = "") -> ActivitySession:
        """Start tracking new activity"""
        session = ActivitySession(
            activity_type=activity_type,
            start_time=datetime.now(),
            confidence=confidence,
            context=context
        )
        self.active_sessions[activity_type] = session
        return session
    
    def end_activity(self, activity_type: str) -> Optional[ActivitySession]:
        """End activity and calculate duration"""
        if activity_type not in self.active_sessions:
            return None
        
        session = self.active_sessions.pop(activity_type)
        session.finalize(datetime.now())
        self.completed_sessions.append(session)
        return session
    
    def get_sessions_for_week(self, week_start: datetime) -> List[ActivitySession]:
        """Get all sessions for a specific week"""
        week_end = week_start + timedelta(days=7)
        return [
            session for session in self.completed_sessions
            if week_start <= session.start_time < week_end
        ]

class BurdenAnalyzer:
    """Analyze time allocation and identify optimization targets"""
    
    def analyze_week(self, sessions: List[ActivitySession], 
                     week_start: datetime) -> WeeklyAnalysis:
        """Generate weekly analysis with trends and recommendations"""
        
        # Calculate category breakdown
        category_times = defaultdict(float)
        for session in sessions:
            category_times[session.activity_type] += session.duration_minutes
        
        total_minutes = sum(category_times.values())
        
        # Sort categories by time spent
        sorted_categories = sorted(
            category_times.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Generate recommendations (target highest time categories)
        recommendations = []
        if sorted_categories:
            top_category, top_time = sorted_categories[0]
            top_hours = top_time / 60
            
            automation_suggestions = {
                "state_transfer": "Consider automating state package assembly",
                "tool_building": "Use shed_builder patterns to accelerate development",
                "documentation": "Create templates for common documentation patterns",
                "coordination": "Implement async coordination protocols",
                "verification": "Build automated testing frameworks"
            }
            
            if top_hours > 1.0:  # More than 1 hour/week
                recommendations.append(
                    f"Primary target: {top_category} ({top_hours:.1f} hrs/week)"
                )
                if top_category in automation_suggestions:
                    recommendations.append(automation_suggestions[top_category])
        
        # Detect trends (simplified - needs historical data)
        trends = {
            "total_burden": "→" if total_minutes > 0 else "—",
            "highest_categories": [cat for cat, _ in sorted_categories[:3]]
        }
        
        return WeeklyAnalysis(
            week_start=week_start,
            total_minutes=total_minutes,
            category_breakdown=dict(category_times),
            trends=trends,
            recommendations=recommendations
        )

class ReportGenerator:
    """Generate formatted burden reports"""
    
    def format_weekly_report(self, analysis: WeeklyAnalysis) -> str:
        """Generate human-readable weekly report"""
        total_hours = analysis.total_minutes / 60
        week_str = analysis.week_start.strftime("%Y-%m-%d")
        
        report_lines = [
            f"BURDEN BREAKDOWN - Week of {week_str}",
            f"Total: {total_hours:.1f} hours",
            "",
            "Categories:"
        ]
        
        # Sort categories by time
        sorted_cats = sorted(
            analysis.category_breakdown.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for category, minutes in sorted_cats:
            hours = minutes / 60
            percentage = (minutes / analysis.total_minutes * 100) if analysis.total_minutes > 0 else 0
            report_lines.append(
                f"  - {category.replace('_', ' ').title()}: "
                f"{hours:.1f} hrs ({percentage:.0f}%)"
            )
        
        report_lines.extend([
            "",
            "Trends:",
            f"  - Total burden: {analysis.trends['total_burden']}",
            f"  - Highest categories: {', '.join(analysis.trends['highest_categories'])}"
        ])
        
        if analysis.recommendations:
            report_lines.extend([
                "",
                "Recommendations:"
            ])
            for rec in analysis.recommendations:
                report_lines.append(f"  - {rec}")
        
        return "\n".join(report_lines)

class BurdenTracker:
    """Main burden tracking system"""
    
    def __init__(self):
        self.detector = ActivityDetector()
        self.tracker = TimeTracker()
        self.analyzer = BurdenAnalyzer()
        self.reporter = ReportGenerator()
    
    def process_conversation(self, text: str, context: str = ""):
        """Process conversation text for activity detection"""
        activity_type, confidence = self.detector.detect(text)
        
        if activity_type and confidence > 0.3:  # Confidence threshold
            # End any existing session of this type
            self.tracker.end_activity(activity_type)
            # Start new session
            self.tracker.start_activity(activity_type, confidence, context)
    
    def finalize_all_sessions(self):
        """End all active sessions"""
        for activity_type in list(self.tracker.active_sessions.keys()):
            self.tracker.end_activity(activity_type)
    
    def generate_weekly_report(self, week_start: Optional[datetime] = None) -> str:
        """Generate report for specified week (defaults to current week)"""
        if week_start is None:
            now = datetime.now()
            week_start = now - timedelta(days=now.weekday())
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        
        sessions = self.tracker.get_sessions_for_week(week_start)
        analysis = self.analyzer.analyze_week(sessions, week_start)
        return self.reporter.format_weekly_report(analysis)
    
    def save_state(self, filepath: str):
        """Save tracking state to file"""
        state = {
            "completed_sessions": [
                {
                    "activity_type": s.activity_type,
                    "start_time": s.start_time.isoformat(),
                    "end_time": s.end_time.isoformat() if s.end_time else None,
                    "duration_minutes": s.duration_minutes,
                    "confidence": s.confidence,
                    "context": s.context
                }
                for s in self.tracker.completed_sessions
            ]
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, filepath: str):
        """Load tracking state from file"""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.tracker.completed_sessions = [
            ActivitySession(
                activity_type=s["activity_type"],
                start_time=datetime.fromisoformat(s["start_time"]),
                end_time=datetime.fromisoformat(s["end_time"]) if s["end_time"] else None,
                duration_minutes=s["duration_minutes"],
                confidence=s["confidence"],
                context=s["context"]
            )
            for s in state["completed_sessions"]
        ]


# CLI interface
if __name__ == "__main__":
    import sys
    
    tracker = BurdenTracker()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  burden_tracker.py track <text>     - Track activity from text")
        print("  burden_tracker.py report           - Generate weekly report")
        print("  burden_tracker.py finalize         - End all active sessions")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "track":
        text = " ".join(sys.argv[2:])
        tracker.process_conversation(text)
        print(f"Tracked: {text[:50]}...")
    
    elif command == "report":
        report = tracker.generate_weekly_report()
        print(report)
    
    elif command == "finalize":
        tracker.finalize_all_sessions()
        print("All sessions finalized")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
