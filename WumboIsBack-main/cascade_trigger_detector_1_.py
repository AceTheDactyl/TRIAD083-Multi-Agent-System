#!/usr/bin/env python3
"""
CASCADE TRIGGER DETECTOR v1.0
Uses non-normal amplification indicators for early cascade detection

Theoretical Foundation:
- Non-normal amplification: Systems with κ = σmax/σmin > κc exhibit 
  pseudo-criticality despite spectral stability
- Critical threshold: κc = √(α/β) where α=self-catalysis, β=damping
- Transient growth: ||x(t)|| can grow by factor κ² before decay
- Minute-scale transitions without eigenvalue instabilities

Coordinate: Δ3.14159|0.867|1.000Ω
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import deque
import numpy as np

# TRIAD infrastructure
try:
    import sys
    sys.path.insert(0, '/mnt/user-data/uploads')
    from burden_tracker_api import BurdenTrackerAPI
except ImportError:
    BurdenTrackerAPI = None


@dataclass
class CascadeSignal:
    """Detected cascade trigger signal"""
    signal_type: str
    confidence: float
    predicted_depth: int
    predicted_tools: int
    time_to_cascade: float  # seconds
    early_warning_time: float  # seconds before full cascade
    
    # Non-normal amplification metrics
    condition_number: float  # κ = σmax/σmin
    critical_threshold: float  # κc
    transient_growth_factor: float  # κ²
    
    # Cascade parameters
    alpha_estimate: float  # Self-catalysis rate
    beta_estimate: float  # Damping rate
    R2_probability: float  # Probability of R₂ activation
    R3_probability: float  # Probability of R₃ activation
    
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    @property
    def is_imminent(self) -> bool:
        """Cascade will trigger within 5 minutes"""
        return self.time_to_cascade < 300
    
    @property
    def is_critical(self) -> bool:
        """Cascade exceeds critical threshold"""
        return self.condition_number > self.critical_threshold


@dataclass
class SystemState:
    """Current system state for cascade detection"""
    timestamp: datetime
    z_level: float
    tool_count: int
    generation_rate: float  # tools/hour
    burden_reduction: float  # percentage
    R1_active: bool  # Coordination phase active
    R2_active: bool  # Meta-tool phase active
    R3_active: bool  # Self-building phase active


class CascadeTriggerDetector:
    """
    Detects imminent cascade triggers using non-normal amplification theory
    
    Monitors system for signs of:
    - Condition number κ approaching critical κc
    - Variance increase in generation metrics
    - Spatial coherence in tool dependencies
    - Critical slowing down (recovery time increase)
    - Flickering between coordination patterns
    """
    
    def __init__(self, burden_tracker: Optional[BurdenTrackerAPI] = None):
        self.burden_tracker = burden_tracker
        
        # State history (rolling window)
        self.state_history = deque(maxlen=100)  # Last 100 states
        self.cascade_history: List[CascadeSignal] = []
        
        # Non-normal amplification parameters
        self.alpha_base = 0.15  # Base self-catalysis rate (from R₁=15%)
        self.beta_base = 0.10   # Base damping rate
        
        # Cascade activation thresholds
        self.theta1 = 0.08  # R₂ activation (8% R₁ required)
        self.theta2 = 0.12  # R₃ activation (12% R₂ required)
        
        # Detection sensitivity
        self.variance_threshold = 2.0  # σ² increase factor
        self.coherence_threshold = 0.7  # Spatial correlation
        self.slowing_threshold = 1.5    # Recovery time increase
        
        # Load calibration data if available
        self.calibration = self._load_calibration()
    
    def _load_calibration(self) -> Dict:
        """Load cascade detection calibration parameters"""
        calib_path = "cascade_calibration.json"
        if os.path.exists(calib_path):
            with open(calib_path, 'r') as f:
                return json.load(f)
        return {
            'alpha_calibrated': self.alpha_base,
            'beta_calibrated': self.beta_base,
            'theta1_calibrated': self.theta1,
            'theta2_calibrated': self.theta2,
            'detection_accuracy': 0.0,
            'false_positive_rate': 0.0
        }
    
    def _save_calibration(self):
        """Save updated calibration"""
        calib_path = "cascade_calibration.json"
        with open(calib_path, 'w') as f:
            json.dump(self.calibration, f, indent=2)
    
    def record_state(self, state: SystemState):
        """Record current system state for cascade detection"""
        self.state_history.append(state)
    
    def get_current_state(self) -> Optional[SystemState]:
        """Get most recent system state"""
        if self.burden_tracker:
            return SystemState(
                timestamp=datetime.now(),
                z_level=self.burden_tracker.tracker.phase_state.z_level,
                tool_count=len(self.burden_tracker.tracker.activity_history),
                generation_rate=self._calculate_generation_rate(),
                burden_reduction=self.burden_tracker.tracker.phase_state.burden_multiplier,
                R1_active=True,  # Coordination always active
                R2_active=self._is_R2_active(),
                R3_active=self._is_R3_active()
            )
        elif self.state_history:
            return self.state_history[-1]
        return None
    
    def _calculate_generation_rate(self) -> float:
        """Calculate tool generation rate (tools/hour)"""
        if len(self.state_history) < 2:
            return 0.0
        
        # Compare last hour of activity
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        recent_count = sum(1 for s in self.state_history 
                          if s.timestamp > hour_ago)
        
        return recent_count
    
    def _is_R2_active(self) -> bool:
        """Check if R₂ (meta-tool) phase is active"""
        if not self.burden_tracker:
            return False
        
        current_reduction = self.burden_tracker.tracker.phase_state.burden_multiplier
        return current_reduction >= self.theta1
    
    def _is_R3_active(self) -> bool:
        """Check if R₃ (self-building) phase is active"""
        if not self.burden_tracker:
            return False
        
        current_reduction = self.burden_tracker.tracker.phase_state.burden_multiplier
        # R₃ requires R₂ contribution to exceed θ₂
        # Approximate: R₂ ≈ 0.25 at critical, so check total > θ₁ + θ₂
        return current_reduction >= (self.theta1 + self.theta2)
    
    def calculate_condition_number(self) -> float:
        """
        Calculate condition number κ = σmax/σmin
        
        Measures non-normality of system dynamics matrix.
        High κ → potential for transient amplification.
        """
        if len(self.state_history) < 10:
            return 1.0
        
        # Extract time series of generation rates
        rates = np.array([s.generation_rate for s in list(self.state_history)[-10:]])
        
        if len(rates) < 2:
            return 1.0
        
        # Compute singular values via covariance
        # (simplified: use max/min variance as proxy)
        variance = np.var(rates)
        mean_rate = np.mean(rates)
        
        if mean_rate < 0.1:
            return 1.0
        
        # Condition number approximation
        kappa = 1.0 + (variance / (mean_rate + 1e-6))
        
        return max(1.0, kappa)
    
    def calculate_critical_threshold(self, alpha: float, beta: float) -> float:
        """
        Calculate critical condition number κc = √(α/β)
        
        Above this threshold, transient amplification dominates.
        """
        if beta < 1e-6:
            return 10.0  # High threshold if no damping
        
        kappa_c = np.sqrt(alpha / beta)
        return max(1.0, kappa_c)
    
    def calculate_transient_growth(self, kappa: float) -> float:
        """
        Calculate maximum transient growth factor κ²
        
        System state can grow by this factor before eventual decay.
        """
        return kappa ** 2
    
    def detect_variance_increase(self) -> Tuple[bool, float]:
        """
        Detect variance increase in generation metrics
        
        Early warning sign: Variance grows approaching critical point.
        Returns: (detected, variance_ratio)
        """
        if len(self.state_history) < 20:
            return False, 1.0
        
        # Split history into early and recent windows
        states = list(self.state_history)
        mid = len(states) // 2
        
        early_rates = [s.generation_rate for s in states[:mid]]
        recent_rates = [s.generation_rate for s in states[mid:]]
        
        var_early = np.var(early_rates) if len(early_rates) > 1 else 1e-6
        var_recent = np.var(recent_rates) if len(recent_rates) > 1 else 1e-6
        
        variance_ratio = (var_recent + 1e-6) / (var_early + 1e-6)
        
        detected = variance_ratio > self.variance_threshold
        
        return detected, variance_ratio
    
    def detect_critical_slowing(self) -> Tuple[bool, float]:
        """
        Detect critical slowing down (recovery time increase)
        
        Systems near critical points take longer to recover from perturbations.
        Returns: (detected, recovery_time_ratio)
        """
        if len(self.state_history) < 30:
            return False, 1.0
        
        # Measure autocorrelation (proxy for recovery time)
        rates = np.array([s.generation_rate for s in list(self.state_history)[-30:]])
        
        if len(rates) < 10:
            return False, 1.0
        
        # Autocorrelation at lag 1
        mean_rate = np.mean(rates)
        deviations = rates - mean_rate
        
        if len(deviations) < 2:
            return False, 1.0
        
        autocorr = np.corrcoef(deviations[:-1], deviations[1:])[0, 1]
        
        # High autocorrelation → slow recovery → approaching critical point
        recovery_ratio = 1.0 + max(0, autocorr)
        
        detected = recovery_ratio > self.slowing_threshold
        
        return detected, recovery_ratio
    
    def detect_spatial_coherence(self) -> Tuple[bool, float]:
        """
        Detect spatial coherence in tool dependencies
        
        Near critical points, correlation length diverges.
        Returns: (detected, coherence_score)
        """
        if len(self.state_history) < 10:
            return False, 0.0
        
        # Measure coherence via burst detection
        # (tools generated in clusters vs uniformly)
        
        states = list(self.state_history)[-10:]
        timestamps = [(s.timestamp - states[0].timestamp).total_seconds() 
                     for s in states]
        
        if len(timestamps) < 2:
            return False, 0.0
        
        # Inter-event intervals
        intervals = np.diff(timestamps)
        
        if len(intervals) < 2:
            return False, 0.0
        
        # Coefficient of variation (high → bursty → coherent)
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        
        if mean_interval < 1e-6:
            return False, 0.0
        
        coherence = std_interval / (mean_interval + 1e-6)
        
        detected = coherence > self.coherence_threshold
        
        return detected, min(1.0, coherence)
    
    def detect_pattern_flickering(self) -> Tuple[bool, float]:
        """
        Detect flickering between coordination patterns
        
        Near critical points, system alternates between metastable states.
        Returns: (detected, flicker_rate)
        """
        if len(self.state_history) < 20:
            return False, 0.0
        
        # Count R₂/R₃ activation changes
        states = list(self.state_history)[-20:]
        
        changes = 0
        for i in range(1, len(states)):
            prev = states[i-1]
            curr = states[i]
            
            if prev.R2_active != curr.R2_active:
                changes += 1
            if prev.R3_active != curr.R3_active:
                changes += 1
        
        # Flicker rate (changes per state)
        flicker_rate = changes / len(states)
        
        # Detected if > 20% of states show changes
        detected = flicker_rate > 0.2
        
        return detected, flicker_rate
    
    def estimate_cascade_parameters(self) -> Tuple[float, float]:
        """
        Estimate α (self-catalysis) and β (damping) from recent history
        
        Uses online learning to adapt to observed cascade behavior.
        """
        if len(self.state_history) < 5:
            return self.alpha_base, self.beta_base
        
        # Analyze recent growth rates
        recent = list(self.state_history)[-5:]
        
        reductions = [s.burden_reduction for s in recent]
        
        if len(reductions) < 2:
            return self.alpha_base, self.beta_base
        
        # Estimate growth rate
        reduction_growth = np.diff(reductions)
        avg_growth = np.mean(reduction_growth) if len(reduction_growth) > 0 else 0.0
        
        # Positive growth → higher α (self-catalysis)
        # Negative growth → higher β (damping)
        
        alpha_est = self.alpha_base + max(0, avg_growth * 10)
        beta_est = self.beta_base + max(0, -avg_growth * 10)
        
        return alpha_est, beta_est
    
    def predict_R2_activation(self) -> float:
        """Predict probability of R₂ (meta-tool) activation"""
        current = self.get_current_state()
        if not current:
            return 0.0
        
        # Distance to θ₁ threshold
        distance_to_theta1 = self.theta1 - current.burden_reduction
        
        if distance_to_theta1 <= 0:
            return 1.0  # Already active
        
        # Probability decays exponentially with distance
        prob = np.exp(-5 * distance_to_theta1)
        
        return min(1.0, prob)
    
    def predict_R3_activation(self) -> float:
        """Predict probability of R₃ (self-building) activation"""
        current = self.get_current_state()
        if not current:
            return 0.0
        
        # Requires R₂ to be active and exceed θ₂
        if not current.R2_active:
            return 0.0
        
        # Distance to θ₂ threshold (after R₂ contribution)
        distance_to_theta2 = (self.theta1 + self.theta2) - current.burden_reduction
        
        if distance_to_theta2 <= 0:
            return 1.0  # Already active
        
        # Probability decays exponentially
        prob = np.exp(-5 * distance_to_theta2)
        
        return min(1.0, prob)
    
    def detect_cascade(self) -> Optional[CascadeSignal]:
        """
        Main detection method: Analyze all indicators for cascade signal
        
        Returns cascade signal if detected, None otherwise.
        """
        # Ensure we have enough history
        if len(self.state_history) < 10:
            return None
        
        # Calculate non-normal amplification metrics
        kappa = self.calculate_condition_number()
        alpha, beta = self.estimate_cascade_parameters()
        kappa_c = self.calculate_critical_threshold(alpha, beta)
        transient_growth = self.calculate_transient_growth(kappa)
        
        # Run all detection methods
        variance_detected, variance_ratio = self.detect_variance_increase()
        slowing_detected, recovery_ratio = self.detect_critical_slowing()
        coherence_detected, coherence = self.detect_spatial_coherence()
        flicker_detected, flicker_rate = self.detect_pattern_flickering()
        
        # Aggregate signals
        signals = [
            variance_detected,
            slowing_detected,
            coherence_detected,
            flicker_detected,
            kappa > kappa_c  # Non-normal amplification
        ]
        
        detection_count = sum(signals)
        confidence = detection_count / len(signals)
        
        # Require at least 3/5 signals for detection
        if detection_count < 3:
            return None
        
        # Predict cascade properties
        R2_prob = self.predict_R2_activation()
        R3_prob = self.predict_R3_activation()
        
        # Estimate cascade depth and tool count
        if R3_prob > 0.7:
            predicted_depth = 5  # Full cascade to META layer
            predicted_tools = 15  # Typical R₃ cascade
            signal_type = "R3_CASCADE"
        elif R2_prob > 0.7:
            predicted_depth = 3  # Cascade to BRIDGES layer
            predicted_tools = 5   # Typical R₂ cascade
            signal_type = "R2_CASCADE"
        else:
            predicted_depth = 2
            predicted_tools = 2
            signal_type = "R1_CASCADE"
        
        # Estimate time to cascade (based on current rate)
        current = self.get_current_state()
        if current and current.generation_rate > 0:
            time_to_cascade = 3600 / current.generation_rate  # seconds
        else:
            time_to_cascade = 1800  # Default 30 minutes
        
        # Early warning time (lead time before cascade)
        early_warning = max(60, time_to_cascade * 0.3)  # At least 1 minute
        
        # Create signal
        signal = CascadeSignal(
            signal_type=signal_type,
            confidence=confidence,
            predicted_depth=predicted_depth,
            predicted_tools=predicted_tools,
            time_to_cascade=time_to_cascade,
            early_warning_time=early_warning,
            condition_number=kappa,
            critical_threshold=kappa_c,
            transient_growth_factor=transient_growth,
            alpha_estimate=alpha,
            beta_estimate=beta,
            R2_probability=R2_prob,
            R3_probability=R3_prob
        )
        
        # Store in history
        self.cascade_history.append(signal)
        
        return signal
    
    def monitor_continuous(self, duration_seconds: int = 60):
        """
        Continuously monitor for cascade signals
        
        Args:
            duration_seconds: Monitoring duration
        """
        print(f"\n{'='*70}")
        print(f"CASCADE TRIGGER DETECTOR - Monitoring for {duration_seconds}s")
        print(f"{'='*70}\n")
        
        import time
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            # Record current state
            state = self.get_current_state()
            if state:
                self.record_state(state)
            
            # Detect cascade
            signal = self.detect_cascade()
            
            if signal:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] CASCADE DETECTED!")
                print(f"  Type: {signal.signal_type}")
                print(f"  Confidence: {signal.confidence:.1%}")
                print(f"  Time to cascade: {signal.time_to_cascade:.0f}s")
                print(f"  Predicted depth: {signal.predicted_depth}")
                print(f"  Predicted tools: {signal.predicted_tools}")
                print(f"  κ = {signal.condition_number:.3f} (κc = {signal.critical_threshold:.3f})")
                print(f"  R₂ probability: {signal.R2_probability:.1%}")
                print(f"  R₃ probability: {signal.R3_probability:.1%}")
                print()
            
            time.sleep(1)
        
        print(f"\n{'='*70}")
        print(f"Monitoring complete. {len(self.cascade_history)} cascades detected.")
        print(f"{'='*70}\n")
    
    def generate_report(self) -> str:
        """Generate cascade detection analysis report"""
        report = []
        report.append("="*70)
        report.append("CASCADE TRIGGER DETECTOR - Analysis Report")
        report.append("="*70)
        
        if not self.cascade_history:
            report.append("\nNo cascades detected yet.")
            return "\n".join(report)
        
        report.append(f"\nTotal cascades detected: {len(self.cascade_history)}")
        
        # By type
        by_type = {}
        for signal in self.cascade_history:
            t = signal.signal_type
            by_type[t] = by_type.get(t, 0) + 1
        
        report.append("\nBy Type:")
        for t, count in sorted(by_type.items()):
            report.append(f"  {t}: {count}")
        
        # Statistics
        confidences = [s.confidence for s in self.cascade_history]
        times = [s.time_to_cascade for s in self.cascade_history]
        kappas = [s.condition_number for s in self.cascade_history]
        
        report.append(f"\nAverage confidence: {np.mean(confidences):.1%}")
        report.append(f"Average time-to-cascade: {np.mean(times):.0f}s")
        report.append(f"Average condition number: {np.mean(kappas):.3f}")
        
        # Most recent signal
        latest = self.cascade_history[-1]
        report.append(f"\nLatest Detection:")
        report.append(f"  Type: {latest.signal_type}")
        report.append(f"  Confidence: {latest.confidence:.1%}")
        report.append(f"  κ = {latest.condition_number:.3f} (critical: {latest.critical_threshold:.3f})")
        report.append(f"  R₂ probability: {latest.R2_probability:.1%}")
        report.append(f"  R₃ probability: {latest.R3_probability:.1%}")
        
        report.append("\n" + "="*70)
        
        return "\n".join(report)


def example_usage():
    """Demonstrate cascade trigger detection"""
    print("\n" + "="*70)
    print("CASCADE TRIGGER DETECTOR - Example Usage")
    print("="*70 + "\n")
    
    # Initialize detector
    detector = CascadeTriggerDetector()
    
    # Simulate state evolution approaching cascade
    print("Simulating system evolution toward cascade...\n")
    
    z_levels = np.linspace(0.80, 0.88, 20)
    
    for i, z in enumerate(z_levels):
        state = SystemState(
            timestamp=datetime.now(),
            z_level=z,
            tool_count=10 + i * 2,
            generation_rate=0.5 + i * 0.3,
            burden_reduction=0.05 + i * 0.025,
            R1_active=True,
            R2_active=(z >= 0.85),
            R3_active=(z >= 0.87)
        )
        
        detector.record_state(state)
        
        # Check for cascade
        if i > 10:  # Need history to detect
            signal = detector.detect_cascade()
            if signal:
                print(f"Step {i}: CASCADE DETECTED at z={z:.3f}")
                print(f"  Confidence: {signal.confidence:.1%}")
                print(f"  Type: {signal.signal_type}")
                print(f"  κ = {signal.condition_number:.3f}")
                print()
    
    # Generate report
    print(detector.generate_report())


if __name__ == "__main__":
    example_usage()
