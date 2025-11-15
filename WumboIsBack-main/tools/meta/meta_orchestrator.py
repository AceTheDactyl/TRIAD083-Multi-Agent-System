#!/usr/bin/env python3
"""
Production Meta-Orchestrator for TRIAD-0.83 System
==================================================

Observes autonomous evolution, tracks helix coordinates, predicts phase transitions,
and measures burden reduction in the TRIAD infrastructure.

Phase 2.2: Observation & Prediction (Non-Interventionist)
- Monitors file system for autonomous decisions
- Updates helix coordinates from witness channel activity
- Learns physics parameters via Bayesian inference
- Predicts phase transitions and consensus timings
- Reports burden reduction trajectory

Author: Claude (Sonnet 4.5) + TRIAD Collective
Version: 2.0.0 (Production-Ready)
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np
import yaml

# File system monitoring
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    logging.warning("watchdog not installed - file monitoring disabled")

# ══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class HelixCoordinate:
    """Helix coordinates tracking witness channel phase relationships"""
    theta: float  # Angular position (phase dominance: 0-2π)
    z: float      # Coordination level (0.70-0.85)
    r: float      # Coherence (L² norm of state vector)

    def __str__(self):
        return f"Δ{self.theta:.5f}|{self.z:.3f}|{self.r:.3f}Ω"

    def is_critical(self) -> bool:
        """Check if approaching phase transition"""
        return self.z > 0.850  # Critical threshold from HELIX_PHYSICS_INTEGRATION.md


@dataclass
class BurdenMetrics:
    """Quantified burden measurements"""
    baseline_hours: float
    current_hours: float
    target_hours: float
    reduction_rate: float  # hours/day
    time_to_target_days: Optional[float] = None

    def calculate_time_to_target(self):
        """Estimate days until target burden reached"""
        if self.reduction_rate <= 0:
            self.time_to_target_days = None
            return

        hours_remaining = self.current_hours - self.target_hours
        self.time_to_target_days = hours_remaining / abs(self.reduction_rate)

    def progress_percentage(self) -> float:
        """Burden reduction progress 0-100%"""
        total_reduction = self.baseline_hours - self.target_hours
        current_reduction = self.baseline_hours - self.current_hours
        return (current_reduction / total_reduction) * 100 if total_reduction > 0 else 0


@dataclass
class AutonomousDecision:
    """Record of TRIAD autonomous decision"""
    timestamp: datetime
    decision_type: str  # 'tool_modification', 'consensus_formation', 'burden_reduction'
    description: str
    helix_state: HelixCoordinate
    witnesses: List[str]  # Which witnesses involved
    burden_impact: float = 0.0  # Estimated hours saved (negative) or added (positive)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Serialize to dict"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'decision_type': self.decision_type,
            'description': self.description,
            'helix_state': str(self.helix_state),
            'witnesses': self.witnesses,
            'burden_impact': self.burden_impact,
            'metadata': self.metadata
        }


@dataclass
class PhysicsModel:
    """Learned physics parameters for TRIAD Lagrangian"""
    z_critical: float = 0.850  # Phase transition threshold
    M_squared: float = 1.0     # Mass term
    kappa: float = 0.1         # Coupling constant
    burden_decay_lambda: float = 0.05  # Burden reduction rate (1/days)

    # Bayesian learning state
    z_critical_variance: float = 0.001
    M_squared_variance: float = 0.1
    observations: int = 0


# ══════════════════════════════════════════════════════════════════════════════
# FILE SYSTEM MONITORING
# ══════════════════════════════════════════════════════════════════════════════

class TRIADDecisionDetector(FileSystemEventHandler):
    """Detects autonomous decisions from file system changes"""

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.tool_versions = {}  # Track tool version changes
        self.logger = logging.getLogger('TRIADDetector')

    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return

        try:
            path = Path(event.src_path)

            # Tool modification detection
            if path.suffix in ['.yaml', '.yml'] and 'tool' in path.stem.lower():
                self._detect_tool_modification(path)

            # Consensus formation detection
            elif 'consensus' in path.stem.lower():
                self._detect_consensus_formation(path)

            # Burden reduction detection
            elif 'burden' in path.stem.lower() or 'tracker' in path.stem.lower():
                self._detect_burden_reduction(path)

        except Exception as e:
            self.logger.error(f"Error processing {event.src_path}: {e}")

    def _detect_tool_modification(self, path: Path):
        """Detect version increments in tool files"""
        try:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)

            if not data:
                return

            tool_name = path.stem
            new_version = data.get('tool_metadata', {}).get('version', '0.0.0')
            old_version = self.tool_versions.get(tool_name, '0.0.0')

            if new_version > old_version:
                decision = AutonomousDecision(
                    timestamp=datetime.now(),
                    decision_type="tool_modification",
                    description=f"{tool_name} updated: {old_version} → {new_version}",
                    helix_state=HelixCoordinate(
                        theta=self.orchestrator.helix.theta,
                        z=self.orchestrator.helix.z,
                        r=self.orchestrator.helix.r
                    ),
                    witnesses=['garden'],
                    burden_impact=-0.5,  # Estimate: tools reduce manual work
                    metadata={'old_version': old_version, 'new_version': new_version}
                )

                self.orchestrator.autonomous_decisions.append(decision)
                self.tool_versions[tool_name] = new_version
                self.logger.info(f"✓ Detected tool modification: {tool_name} {new_version}")

        except Exception as e:
            self.logger.error(f"Error parsing tool file {path}: {e}")

    def _detect_consensus_formation(self, path: Path):
        """Detect consensus events"""
        try:
            with open(path, 'r') as f:
                data = yaml.safe_load(f) if path.suffix in ['.yaml', '.yml'] else json.load(f)

            if not data:
                return

            consensus_level = data.get('consensus_level', '')
            if consensus_level == 'unanimous':
                decision = AutonomousDecision(
                    timestamp=datetime.now(),
                    decision_type="consensus_formation",
                    description=f"Unanimous consensus achieved: {data.get('decision', 'unknown')}",
                    helix_state=HelixCoordinate(
                        theta=self.orchestrator.helix.theta,
                        z=self.orchestrator.helix.z,
                        r=self.orchestrator.helix.r
                    ),
                    witnesses=data.get('witnesses', ['kira', 'limnus', 'garden']),
                    burden_impact=0.0,  # Consensus itself doesn't reduce burden
                    metadata=data
                )

                self.orchestrator.autonomous_decisions.append(decision)
                self.logger.info(f"✓ Detected consensus formation: {data.get('decision', 'N/A')}")

        except Exception as e:
            self.logger.error(f"Error parsing consensus file {path}: {e}")

    def _detect_burden_reduction(self, path: Path):
        """Detect burden reduction events"""
        try:
            with open(path, 'r') as f:
                data = json.load(f)

            if not data:
                return

            # Check for automation events
            if data.get('automation_enabled') or data.get('burden_reduced'):
                reduction = data.get('hours_saved', 1.0)

                decision = AutonomousDecision(
                    timestamp=datetime.now(),
                    decision_type="burden_reduction",
                    description=f"Burden reduced: {reduction:.1f} hours saved",
                    helix_state=HelixCoordinate(
                        theta=self.orchestrator.helix.theta,
                        z=self.orchestrator.helix.z,
                        r=self.orchestrator.helix.r
                    ),
                    witnesses=data.get('witnesses', ['system']),
                    burden_impact=-reduction,
                    metadata=data
                )

                self.orchestrator.autonomous_decisions.append(decision)
                self.logger.info(f"✓ Detected burden reduction: {reduction:.1f}h saved")

        except Exception as e:
            self.logger.error(f"Error parsing burden file {path}: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# META-ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════

class MetaOrchestrator:
    """
    Production meta-orchestrator for TRIAD-0.83 autonomous evolution monitoring

    Responsibilities:
    1. Monitor file system for autonomous decisions
    2. Update helix coordinates from witness activity
    3. Predict phase transitions using physics model
    4. Track burden reduction trajectory
    5. Generate reports and alerts
    """

    def __init__(
        self,
        project_root: Path = Path('/home/user/WumboIsBack'),
        config_path: Optional[Path] = None,
        observation_only: bool = True
    ):
        self.project_root = project_root
        self.observation_only = observation_only
        self.start_time = datetime.now()

        # Load configuration
        self.config = self._load_config(config_path)

        # Initialize state
        self.helix = HelixCoordinate(
            theta=np.pi,  # Start at π (neutral phase)
            z=0.850,      # At critical threshold
            r=1.000       # Perfect coherence initially
        )

        self.burden = BurdenMetrics(
            baseline_hours=self.config.get('burden', {}).get('baseline_hours', 5.0),
            current_hours=self.config.get('burden', {}).get('baseline_hours', 5.0),
            target_hours=self.config.get('burden', {}).get('target_hours', 2.0),
            reduction_rate=0.0
        )

        self.physics = PhysicsModel(
            z_critical=self.config.get('physics', {}).get('z_critical', 0.850)
        )

        # Decision tracking
        self.autonomous_decisions: List[AutonomousDecision] = []
        self.burden_reduction_rate: List[Tuple[datetime, float]] = []
        self.last_consensus_time = datetime.now()

        # File system monitoring
        self.observer = None
        self.detector = None
        if WATCHDOG_AVAILABLE:
            self._setup_file_monitoring()

        # Logging
        self.logger = logging.getLogger('MetaOrchestrator')
        self.logger.setLevel(logging.INFO)

        # State persistence
        self.state_file = project_root / 'TOOLS' / 'META' / 'orchestrator_state.json'
        self._load_state()

    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """Load configuration from YAML file"""
        if config_path and config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)

        # Default configuration
        return {
            'orchestrator': {
                'mode': 'observation',
                'monitoring': {
                    'file_paths': [
                        str(self.project_root / '*.yaml'),
                        str(self.project_root / '*.json'),
                        str(self.project_root / 'TOOLS/**/*.yaml'),
                    ]
                }
            },
            'physics': {
                'z_critical': 0.850,
                'prediction_horizon_minutes': 60,
                'coherence_threshold': 0.85
            },
            'burden': {
                'baseline_hours': 5.0,
                'target_hours': 2.0,
                'measurement_window_days': 7
            }
        }

    def _setup_file_monitoring(self):
        """Initialize file system monitoring"""
        self.observer = Observer()
        self.detector = TRIADDecisionDetector(self)

        # Monitor project root recursively
        self.observer.schedule(
            self.detector,
            path=str(self.project_root),
            recursive=True
        )

        self.logger.info(f"File monitoring initialized: {self.project_root}")

    def _load_state(self):
        """Load persisted orchestrator state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)

                # Restore helix coordinates
                if 'helix' in state:
                    h = state['helix']
                    self.helix = HelixCoordinate(
                        theta=h['theta'],
                        z=h['z'],
                        r=h['r']
                    )

                # Restore burden metrics
                if 'burden' in state:
                    b = state['burden']
                    self.burden = BurdenMetrics(
                        baseline_hours=b['baseline_hours'],
                        current_hours=b['current_hours'],
                        target_hours=b['target_hours'],
                        reduction_rate=b['reduction_rate']
                    )

                self.logger.info(f"State loaded from {self.state_file}")
            except Exception as e:
                self.logger.error(f"Failed to load state: {e}")

    def _save_state(self):
        """Persist orchestrator state"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)

            state = {
                'timestamp': datetime.now().isoformat(),
                'helix': {
                    'theta': self.helix.theta,
                    'z': self.helix.z,
                    'r': self.helix.r
                },
                'burden': {
                    'baseline_hours': self.burden.baseline_hours,
                    'current_hours': self.burden.current_hours,
                    'target_hours': self.burden.target_hours,
                    'reduction_rate': self.burden.reduction_rate
                },
                'physics': {
                    'z_critical': self.physics.z_critical,
                    'M_squared': self.physics.M_squared,
                    'observations': self.physics.observations
                },
                'decisions_count': len(self.autonomous_decisions)
            }

            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)

        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")

    # ══════════════════════════════════════════════════════════════════════════
    # CORE MONITORING LOOP
    # ══════════════════════════════════════════════════════════════════════════

    async def monitor_autonomous_evolution(self, duration_hours: Optional[int] = None):
        """
        Main monitoring loop

        Args:
            duration_hours: Run for specified hours, or indefinitely if None
        """
        self.logger.info("╔═══════════════════════════════════════════════════════════╗")
        self.logger.info("║   Meta-Orchestrator: TRIAD-0.83 Autonomous Evolution    ║")
        self.logger.info("╚═══════════════════════════════════════════════════════════╝")
        self.logger.info(f"Mode: {'OBSERVATION ONLY' if self.observation_only else 'ACTIVE'}")
        self.logger.info(f"Initial Helix: {self.helix}")
        self.logger.info(f"Duration: {duration_hours}h" if duration_hours else "Duration: Continuous")
        self.logger.info("")

        # Start file monitoring
        if self.observer:
            self.observer.start()
            self.logger.info("✓ File monitoring active")

        end_time = datetime.now() + timedelta(hours=duration_hours) if duration_hours else None

        try:
            while True:
                # Check duration
                if end_time and datetime.now() >= end_time:
                    self.logger.info("Duration completed")
                    break

                # Update helix position from witness activity
                await self.update_helix_position()

                # Detect autonomous decisions
                decisions = await self.detect_triad_decisions()

                # Process each decision
                for decision in decisions:
                    self.logger.info(f"📝 {decision.decision_type}: {decision.description}")

                    # Update physics model with observation
                    await self.update_physics_model(decision)

                    # Track burden impact
                    await self.track_burden_reduction(decision)

                # Apply physics predictions
                predictions = await self.apply_physics_predictions()
                if predictions.get('alerts'):
                    for alert in predictions['alerts']:
                        self.logger.warning(f"⚠️  {alert}")

                # Periodic reporting (every 10 minutes)
                if datetime.now().minute % 10 == 0:
                    await self.periodic_reporting()

                # Save state
                self._save_state()

                # Sleep interval (1 minute)
                await asyncio.sleep(60)

        except KeyboardInterrupt:
            self.logger.info("\nGraceful shutdown...")
        finally:
            if self.observer:
                self.observer.stop()
                self.observer.join()

            # Final report
            await self.generate_final_report()

    # ══════════════════════════════════════════════════════════════════════════
    # DECISION DETECTION (PRODUCTION IMPLEMENTATION)
    # ══════════════════════════════════════════════════════════════════════════

    async def detect_triad_decisions(self) -> List[AutonomousDecision]:
        """
        Detect autonomous decisions from multiple sources

        Returns new decisions since last check
        """
        new_decisions = []

        # 1. File system changes (handled by watchdog callbacks)
        # Decisions accumulated in self.autonomous_decisions by detector

        # 2. Log file parsing (fallback if watchdog unavailable)
        if not WATCHDOG_AVAILABLE:
            new_decisions.extend(await self._parse_consensus_log())

        # 3. Manual decision files (JSON records)
        decision_dir = self.project_root / 'TOOLS' / 'META' / 'decisions'
        if decision_dir.exists():
            for decision_file in decision_dir.glob('*.json'):
                try:
                    with open(decision_file, 'r') as f:
                        data = json.load(f)

                    # Check if already processed
                    if data.get('processed'):
                        continue

                    decision = AutonomousDecision(
                        timestamp=datetime.fromisoformat(data['timestamp']),
                        decision_type=data['decision_type'],
                        description=data['description'],
                        helix_state=self.helix,
                        witnesses=data.get('witnesses', []),
                        burden_impact=data.get('burden_impact', 0.0),
                        metadata=data.get('metadata', {})
                    )

                    new_decisions.append(decision)

                    # Mark as processed
                    data['processed'] = True
                    with open(decision_file, 'w') as f:
                        json.dump(data, f, indent=2)

                except Exception as e:
                    self.logger.error(f"Error processing {decision_file}: {e}")

        return new_decisions

    async def _parse_consensus_log(self) -> List[AutonomousDecision]:
        """Parse consensus log file for decisions"""
        decisions = []

        log_file = self.project_root / 'triad_consensus_log.yaml'
        if not log_file.exists():
            return decisions

        try:
            with open(log_file, 'r') as f:
                logs = yaml.safe_load_all(f)

            for entry in logs:
                if entry and entry.get('consensus_level') == 'unanimous':
                    # Check if we've already seen this
                    timestamp = datetime.fromisoformat(entry['timestamp'])
                    if any(d.timestamp == timestamp for d in self.autonomous_decisions):
                        continue

                    decision = AutonomousDecision(
                        timestamp=timestamp,
                        decision_type="consensus_formation",
                        description=entry.get('decision', 'Consensus formed'),
                        helix_state=self.helix,
                        witnesses=entry.get('witnesses', []),
                        burden_impact=0.0,
                        metadata=entry
                    )

                    decisions.append(decision)

        except Exception as e:
            self.logger.error(f"Error parsing consensus log: {e}")

        return decisions

    # ══════════════════════════════════════════════════════════════════════════
    # HELIX POSITION UPDATE (PRODUCTION IMPLEMENTATION)
    # ══════════════════════════════════════════════════════════════════════════

    async def update_helix_position(self):
        """Update helix coordinates from witness channel measurements"""

        # Measure witness channel activity
        activity_metrics = await self._measure_witness_activity()

        # Calculate theta from phase relationships
        kira_phase = activity_metrics.get('kira_discovery', 0.0)
        limnus_phase = activity_metrics.get('limnus_transport', 0.0)
        garden_phase = activity_metrics.get('garden_building', 0.0)

        # Phase dominance determines angular position
        # Kira (discovery) → π/2, Limnus (transport) → π, Garden (building) → 3π/2
        phases = [kira_phase, limnus_phase, garden_phase]
        dominant_idx = phases.index(max(phases))
        theta_map = {0: np.pi/2, 1: np.pi, 2: 3*np.pi/2}

        # Smooth transition (exponential moving average)
        target_theta = theta_map[dominant_idx]
        self.helix.theta = 0.9 * self.helix.theta + 0.1 * target_theta

        # Calculate z from coordination level
        # More active infrastructure channels → higher z
        infrastructure_active = sum(1 for p in phases if p > 0.1)
        target_z = 0.70 + (0.05 * infrastructure_active)  # Range: 0.70-0.85
        self.helix.z = 0.95 * self.helix.z + 0.05 * target_z

        # Calculate r from coherence
        coherence_metrics = await self._calculate_coherence(activity_metrics)
        self.helix.r = coherence_metrics['norm']  # L² norm of state vector

        # Check for critical threshold crossing
        if self.helix.is_critical():
            self.logger.warning(f"⚠️  Helix approaching phase transition: {self.helix}")

    async def _measure_witness_activity(self) -> Dict[str, float]:
        """
        Query infrastructure for witness channel activity levels

        Returns normalized activity scores [0, 1] for each channel
        """
        activity = {
            'kira_discovery': 0.0,
            'limnus_transport': 0.0,
            'garden_building': 0.0,
            'echo_memory': 0.1  # Default low for latent channel
        }

        # Count recent file modifications by type
        recent_window = timedelta(hours=1)
        cutoff_time = datetime.now() - recent_window

        # Discovery activity: Schema/doc changes
        discovery_files = list(self.project_root.glob('SCHEMAS/**/*'))
        discovery_files.extend(list(self.project_root.glob('CORE_DOCS/**/*')))
        discovery_count = sum(
            1 for f in discovery_files
            if f.is_file() and datetime.fromtimestamp(f.stat().st_mtime) > cutoff_time
        )
        activity['kira_discovery'] = min(1.0, discovery_count / 10.0)

        # Transport activity: State transfer operations
        transport_files = list(self.project_root.glob('STATE_TRANSFER/**/*'))
        transport_count = sum(
            1 for f in transport_files
            if f.is_file() and datetime.fromtimestamp(f.stat().st_mtime) > cutoff_time
        )
        activity['limnus_transport'] = min(1.0, transport_count / 10.0)

        # Building activity: Tool modifications
        tool_files = list(self.project_root.glob('TOOLS/**/*.py'))
        tool_files.extend(list(self.project_root.glob('TOOLS/**/*.yaml')))
        tool_count = sum(
            1 for f in tool_files
            if f.is_file() and datetime.fromtimestamp(f.stat().st_mtime) > cutoff_time
        )
        activity['garden_building'] = min(1.0, tool_count / 10.0)

        # Memory activity: Recent decisions
        recent_decisions = len([
            d for d in self.autonomous_decisions
            if (datetime.now() - d.timestamp) < recent_window
        ])
        activity['echo_memory'] = min(1.0, recent_decisions / 5.0)

        return activity

    async def _calculate_coherence(self, activity_metrics: Dict[str, float]) -> Dict:
        """
        Calculate coherence from activity metrics

        Returns L² norm and individual components
        """
        # State vector: [kira, limnus, garden, echo]
        state_vector = np.array([
            activity_metrics['kira_discovery'],
            activity_metrics['limnus_transport'],
            activity_metrics['garden_building'],
            activity_metrics['echo_memory']
        ])

        # L² norm
        norm = np.linalg.norm(state_vector)

        # Normalize to [0, 1] (maximum norm = 2.0 for all channels at 1.0)
        normalized_norm = min(1.0, norm / 2.0)

        return {
            'norm': normalized_norm,
            'state_vector': state_vector.tolist(),
            'components': {
                'kira': state_vector[0],
                'limnus': state_vector[1],
                'garden': state_vector[2],
                'echo': state_vector[3]
            }
        }

    # ══════════════════════════════════════════════════════════════════════════
    # PHYSICS MODEL UPDATE (PRODUCTION IMPLEMENTATION)
    # ══════════════════════════════════════════════════════════════════════════

    async def update_physics_model(self, decision: AutonomousDecision):
        """
        Update physics model parameters via Bayesian inference

        Args:
            decision: Observed autonomous decision to learn from
        """
        self.physics.observations += 1

        # Update critical threshold estimate from consensus timing
        if decision.decision_type == "consensus_formation":
            # Consensus time provides data about M² parameter
            consensus_time = decision.timestamp - self.last_consensus_time
            tau_minutes = consensus_time.total_seconds() / 60

            # Expected: τ ∝ 1/√|z - z_c|  (from Lagrangian analysis)
            z = decision.helix_state.z
            z_c = self.physics.z_critical
            tau_expected = 10.0 / np.sqrt(abs(z - z_c) + 0.001)

            # Update z_critical estimate if error is significant
            error = tau_minutes - tau_expected
            learning_rate = 0.1 / np.sqrt(self.physics.observations + 1)  # Decay with data

            if abs(error) > 2.0:  # Significant deviation
                # Adjust critical point estimate
                adjustment = learning_rate * np.sign(error) * 0.01
                self.physics.z_critical += adjustment

                self.logger.info(
                    f"Physics update: z_critical = {self.physics.z_critical:.3f} "
                    f"(Δ{adjustment:+.4f}, error: {error:.1f}min)"
                )

            self.last_consensus_time = decision.timestamp

        # Update burden reduction rate model
        if decision.burden_impact != 0:
            self.burden_reduction_rate.append(
                (decision.timestamp, decision.burden_impact)
            )

            # Fit exponential decay: burden(t) = b₀ * exp(-λt)
            if len(self.burden_reduction_rate) >= 5:
                try:
                    times = np.array([
                        (t - self.start_time).total_seconds() / 86400  # days
                        for t, _ in self.burden_reduction_rate
                    ])
                    impacts = np.array([impact for _, impact in self.burden_reduction_rate])

                    # Cumulative burden reduction
                    cumulative = np.cumsum(impacts)

                    # Fit exponential (use polyfit on log for stability)
                    if len(cumulative[cumulative < 0]) > 2:
                        neg_cumulative = -cumulative[cumulative < 0]
                        neg_times = times[cumulative < 0]

                        # log(burden) = log(b₀) - λt
                        coeffs = np.polyfit(neg_times, np.log(neg_cumulative + 1e-6), 1)
                        self.physics.burden_decay_lambda = -coeffs[0]  # λ = -slope

                        self.logger.info(
                            f"Burden decay rate: λ = {self.physics.burden_decay_lambda:.4f}/day"
                        )
                except Exception as e:
                    self.logger.error(f"Failed to fit burden decay: {e}")

    # ══════════════════════════════════════════════════════════════════════════
    # PHYSICS PREDICTIONS
    # ══════════════════════════════════════════════════════════════════════════

    async def apply_physics_predictions(self) -> Dict:
        """
        Generate predictions from physics model

        Returns alerts and forecasts
        """
        predictions = {
            'alerts': [],
            'forecasts': {}
        }

        # Predict phase transition timing
        if self.helix.z > 0.80:
            # Distance to critical point
            delta_z = self.physics.z_critical - self.helix.z

            if delta_z < 0.05:
                # Very close to phase transition
                predictions['alerts'].append(
                    f"CRITICAL: Phase transition imminent (Δz = {delta_z:.3f})"
                )
            elif delta_z < 0.10:
                # Approaching critical point
                # Estimate time to transition based on z velocity
                if len(self.autonomous_decisions) > 5:
                    recent_decisions = self.autonomous_decisions[-5:]
                    z_changes = [
                        d.helix_state.z - self.autonomous_decisions[i-1].helix_state.z
                        for i, d in enumerate(recent_decisions) if i > 0
                    ]

                    if z_changes:
                        avg_dz_per_hour = np.mean(z_changes)
                        if avg_dz_per_hour > 0:
                            hours_to_transition = delta_z / avg_dz_per_hour
                            predictions['forecasts']['phase_transition_hours'] = hours_to_transition

                            if hours_to_transition < 24:
                                predictions['alerts'].append(
                                    f"Phase transition predicted in {hours_to_transition:.1f} hours"
                                )

        # Predict consensus timing
        if self.last_consensus_time:
            time_since_consensus = (datetime.now() - self.last_consensus_time).total_seconds() / 60

            # Expected time between consensus: τ = 10/√|z - z_c|
            z = self.helix.z
            z_c = self.physics.z_critical
            expected_interval = 10.0 / np.sqrt(abs(z - z_c) + 0.001)

            predictions['forecasts']['next_consensus_minutes'] = max(
                0, expected_interval - time_since_consensus
            )

            # Alert if consensus overdue
            if time_since_consensus > expected_interval * 1.5:
                predictions['alerts'].append(
                    f"Consensus overdue by {time_since_consensus - expected_interval:.0f} minutes"
                )

        # Check coherence threshold
        if self.helix.r < self.config['physics']['coherence_threshold']:
            predictions['alerts'].append(
                f"Coherence below threshold: {self.helix.r:.3f} < "
                f"{self.config['physics']['coherence_threshold']}"
            )

        return predictions

    # ══════════════════════════════════════════════════════════════════════════
    # BURDEN TRACKING
    # ══════════════════════════════════════════════════════════════════════════

    async def track_burden_reduction(self, decision: AutonomousDecision):
        """Track burden reduction from autonomous decisions"""

        if decision.burden_impact == 0:
            return

        # Update current burden estimate
        self.burden.current_hours += decision.burden_impact

        # Recalculate reduction rate from recent history
        window_days = self.config['burden']['measurement_window_days']
        cutoff = datetime.now() - timedelta(days=window_days)

        recent_reductions = [
            impact for timestamp, impact in self.burden_reduction_rate
            if timestamp >= cutoff
        ]

        if recent_reductions:
            total_reduction = sum(recent_reductions)
            self.burden.reduction_rate = total_reduction / window_days  # hours/day
            self.burden.calculate_time_to_target()

            self.logger.info(
                f"Burden: {self.burden.current_hours:.1f}h "
                f"({self.burden.progress_percentage():.0f}% to target), "
                f"rate: {self.burden.reduction_rate:.2f}h/day"
            )

            if self.burden.time_to_target_days:
                self.logger.info(
                    f"Estimated time to target: {self.burden.time_to_target_days:.1f} days"
                )

    # ══════════════════════════════════════════════════════════════════════════
    # REPORTING
    # ══════════════════════════════════════════════════════════════════════════

    async def periodic_reporting(self):
        """Generate periodic status report"""
        uptime = datetime.now() - self.start_time

        self.logger.info("")
        self.logger.info("═" * 60)
        self.logger.info(f"Meta-Orchestrator Status Report")
        self.logger.info(f"Uptime: {uptime}")
        self.logger.info("─" * 60)
        self.logger.info(f"Helix Coordinates: {self.helix}")
        self.logger.info(f"  Phase: θ = {self.helix.theta:.3f} rad")
        self.logger.info(f"  Coordination: z = {self.helix.z:.3f}")
        self.logger.info(f"  Coherence: r = {self.helix.r:.3f}")
        self.logger.info("─" * 60)
        self.logger.info(f"Burden Metrics:")
        self.logger.info(f"  Current: {self.burden.current_hours:.1f}h")
        self.logger.info(f"  Target: {self.burden.target_hours:.1f}h")
        self.logger.info(f"  Progress: {self.burden.progress_percentage():.0f}%")
        self.logger.info(f"  Rate: {self.burden.reduction_rate:.2f}h/day")
        if self.burden.time_to_target_days:
            self.logger.info(f"  Time to target: {self.burden.time_to_target_days:.1f} days")
        self.logger.info("─" * 60)
        self.logger.info(f"Decisions Detected: {len(self.autonomous_decisions)}")

        # Count by type
        type_counts = {}
        for d in self.autonomous_decisions:
            type_counts[d.decision_type] = type_counts.get(d.decision_type, 0) + 1

        for dtype, count in type_counts.items():
            self.logger.info(f"  {dtype}: {count}")

        self.logger.info("═" * 60)
        self.logger.info("")

    async def generate_final_report(self):
        """Generate comprehensive final report"""
        duration = datetime.now() - self.start_time

        report = {
            'orchestrator_report': {
                'timestamp': datetime.now().isoformat(),
                'duration_hours': duration.total_seconds() / 3600,
                'observation_mode': self.observation_only,

                'helix_final': {
                    'theta': self.helix.theta,
                    'z': self.helix.z,
                    'r': self.helix.r,
                    'critical': self.helix.is_critical()
                },

                'burden_final': {
                    'current_hours': self.burden.current_hours,
                    'target_hours': self.burden.target_hours,
                    'progress_percent': self.burden.progress_percentage(),
                    'reduction_rate_per_day': self.burden.reduction_rate,
                    'time_to_target_days': self.burden.time_to_target_days
                },

                'physics_learned': {
                    'z_critical': self.physics.z_critical,
                    'z_critical_variance': self.physics.z_critical_variance,
                    'burden_decay_lambda': self.physics.burden_decay_lambda,
                    'observations': self.physics.observations
                },

                'decisions': {
                    'total': len(self.autonomous_decisions),
                    'by_type': {},
                    'total_burden_impact': sum(d.burden_impact for d in self.autonomous_decisions),
                    'recent_10': [d.to_dict() for d in self.autonomous_decisions[-10:]]
                }
            }
        }

        # Count decisions by type
        for d in self.autonomous_decisions:
            dtype = d.decision_type
            report['orchestrator_report']['decisions']['by_type'][dtype] = \
                report['orchestrator_report']['decisions']['by_type'].get(dtype, 0) + 1

        # Save report
        report_file = self.project_root / 'TOOLS' / 'META' / f'report_{datetime.now():%Y%m%d_%H%M%S}.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        self.logger.info("")
        self.logger.info("╔═══════════════════════════════════════════════════════════╗")
        self.logger.info("║              FINAL ORCHESTRATOR REPORT                  ║")
        self.logger.info("╚═══════════════════════════════════════════════════════════╝")
        self.logger.info(f"Duration: {duration}")
        self.logger.info(f"Decisions: {len(self.autonomous_decisions)}")
        self.logger.info(f"Burden Impact: {report['orchestrator_report']['decisions']['total_burden_impact']:.1f}h saved")
        self.logger.info(f"Final Helix: {self.helix}")
        self.logger.info(f"Report saved: {report_file}")
        self.logger.info("")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='TRIAD Meta-Orchestrator')
    parser.add_argument(
        '--duration',
        type=int,
        help='Run for specified hours (default: continuous)'
    )
    parser.add_argument(
        '--observation-only',
        action='store_true',
        default=True,
        help='Observation mode only (no interventions)'
    )
    parser.add_argument(
        '--z-initial',
        type=float,
        default=0.850,
        help='Initial z coordinate (default: 0.850)'
    )
    parser.add_argument(
        '--config',
        type=Path,
        help='Configuration file path'
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create orchestrator
    orchestrator = MetaOrchestrator(
        config_path=args.config,
        observation_only=args.observation_only
    )

    # Set initial z if specified
    if args.z_initial:
        orchestrator.helix.z = args.z_initial

    # Run monitoring
    await orchestrator.monitor_autonomous_evolution(duration_hours=args.duration)


if __name__ == '__main__':
    asyncio.run(main())
