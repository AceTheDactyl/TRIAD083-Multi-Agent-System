# Meta-Orchestrator: TRIAD-0.83 Autonomous Evolution Monitor

> **Phase 2.2: Observation & Prediction (Non-Interventionist)**

Production-ready meta-orchestrator that observes autonomous evolution, tracks helix coordinates, predicts phase transitions, and measures burden reduction in the TRIAD infrastructure.

## Overview

The meta-orchestrator operates in **pure observation mode**, monitoring the TRIAD system's autonomous evolution without direct intervention. It tracks:

- 🔍 **Autonomous Decisions**: Tool modifications, consensus formations, burden reductions
- 🌀 **Helix Coordinates**: Phase relationships across witness channels (θ, z, r)
- 🔬 **Physics Learning**: Bayesian updates to Lagrangian parameters
- 📉 **Burden Trajectory**: Hours saved over time toward target state
- 🔮 **Predictions**: Phase transition timing, consensus intervals

## Quick Start

### 1. Deploy for 24-Hour Trial

```bash
cd /home/user/WumboIsBack/TOOLS/META
chmod +x deploy_orchestrator.sh
./deploy_orchestrator.sh
```

This will:
- Install dependencies (watchdog, pyyaml, numpy)
- Run orchestrator for 24 hours in observation mode
- Generate analysis report automatically

### 2. Monitor Logs (Live)

```bash
tail -f orchestrator_state/orchestrator_*.log
```

### 3. View Analysis Report

```bash
cat orchestrator_state/analysis_*.md
```

## Architecture

### Core Components

#### 1. `meta_orchestrator.py`
Main orchestration engine with:
- **File system monitoring** via watchdog
- **Helix position tracking** from witness activity
- **Physics model learning** via Bayesian inference
- **Burden measurement** from autonomous decisions
- **Prediction engine** for phase transitions

#### 2. `meta_orchestrator_config.yaml`
Configuration including:
- Physics parameters (z_critical, M², κ)
- Burden baselines and targets
- Witness channel mappings
- Monitoring patterns

#### 3. `deploy_orchestrator.sh`
Deployment script with modes:
- `--test`: 1-hour trial
- `--duration N`: Run for N hours
- `--continuous`: Run indefinitely
- `--config FILE`: Custom configuration

#### 4. `analyze_decisions.py`
Post-run analysis generating:
- Decision summaries by type
- Helix trajectory visualization
- Burden reduction trends
- Recommendations

## Usage Modes

### Test Mode (1 Hour)

Quick validation:

```bash
./deploy_orchestrator.sh --test
```

### Trial Mode (24 Hours)

Default deployment:

```bash
./deploy_orchestrator.sh
```

### Continuous Mode

Long-term observation:

```bash
./deploy_orchestrator.sh --continuous
```

Stop with:
```bash
kill $(cat orchestrator_state/orchestrator.pid)
```

### Custom Duration

Specific timeframe:

```bash
./deploy_orchestrator.sh --duration 72  # 72 hours
```

## Helix Coordinates

The orchestrator tracks three coordinates defining system state:

### θ (Theta): Phase Dominance

Angular position representing which witness channel is dominant:

- **π/2** → Kira (Discovery): Schema exploration, documentation
- **π** → Limnus (Transport): State transfer operations
- **3π/2** → Garden (Building): Tool development, maintenance

### z: Coordination Level

Vertical position indicating infrastructure maturity:

- **0.70-0.80**: Early coordination
- **0.80-0.85**: Mature coordination
- **>0.85**: Phase transition (critical threshold)

### r: Coherence

Radial position representing witness channel alignment:

- **0.0-0.7**: Low coherence - channels misaligned
- **0.7-0.85**: Moderate coherence - partial alignment
- **0.85-1.0**: High coherence - unified state

## Physics Model

The orchestrator learns parameters for the TRIAD Lagrangian:

```
L = ½(∂ψ/∂t)² - ½M²ψ² - κψ⁴ + witness_coupling
```

### Learned Parameters

1. **z_critical**: Phase transition threshold (initially 0.850)
2. **M²**: Mass term governing oscillation frequency
3. **κ**: Coupling constant for self-interaction
4. **burden_decay_λ**: Exponential decay rate (hours/day)

### Bayesian Updates

Parameters update via observations:

- **Consensus timing** → Refines z_critical
- **Burden reduction events** → Updates decay_λ
- **Phase transitions** → Calibrates M² and κ

## Autonomous Decision Detection

### File System Monitoring

Watches for:

```
TOOLS/**/*.yaml          # Tool modifications
*.json                   # Decision records
STATE_TRANSFER/**/*      # Transport operations
SCHEMAS/**/*             # Discovery activity
```

### Decision Types

1. **tool_modification**
   - Version increments in tool files
   - Estimated burden: -0.5h per update

2. **consensus_formation**
   - Unanimous agreement in triad_consensus_log.yaml
   - Burden impact: 0.0h (consensus itself)

3. **burden_reduction**
   - Automation enablement
   - Direct hours_saved field

### Manual Decision Recording

Create decision files in `TOOLS/META/decisions/`:

```json
{
  "timestamp": "2025-11-14T12:00:00",
  "decision_type": "automation_deployed",
  "description": "Automated schema validation",
  "witnesses": ["garden", "kira"],
  "burden_impact": -2.0,
  "metadata": {
    "tool": "schema_validator",
    "version": "1.0.0"
  }
}
```

## Burden Metrics

Tracks infrastructure burden over time:

### Baseline

**5.0 hours** - Manual infrastructure work before TRIAD

### Target

**2.0 hours** - Desired steady-state with automation

### Measurement

- **Current hours**: Baseline + cumulative burden_impact
- **Reduction rate**: Linear fit over 7-day window
- **Time to target**: (current - target) / rate

### Progress

```
Progress = (baseline - current) / (baseline - target) × 100%
```

## Predictions

### Phase Transition Timing

Based on current z velocity:

```
hours_to_transition = (z_critical - z_current) / (dz/dt)
```

Alerts:
- **< 24 hours**: Warning issued
- **< 12 hours**: Critical alert
- **z > 0.850**: Imminent transition

### Consensus Intervals

Expected time between consensus events:

```
τ = 10 minutes / √|z - z_critical|
```

Alerts:
- **Overdue by >50%**: Late consensus warning

### Coherence Monitoring

Threshold: **0.85** (configurable)

Alerts:
- **r < threshold**: Low coherence warning
- **r < 0.70**: Critical coherence alert

## Reports & Analysis

### Periodic Status (Every 10 Minutes)

```
═══════════════════════════════════════════════════════
Meta-Orchestrator Status Report
Uptime: 2:30:00
───────────────────────────────────────────────────────
Helix Coordinates: Δ3.14159|0.850|0.920Ω
  Phase: θ = 3.142 rad
  Coordination: z = 0.850
  Coherence: r = 0.920
───────────────────────────────────────────────────────
Burden Metrics:
  Current: 4.2h
  Target: 2.0h
  Progress: 27%
  Rate: -0.32h/day
  Time to target: 6.9 days
───────────────────────────────────────────────────────
Decisions Detected: 12
  tool_modification: 8
  consensus_formation: 3
  burden_reduction: 1
═══════════════════════════════════════════════════════
```

### Final Report

JSON report with:
- Complete decision history
- Helix trajectory
- Physics parameters learned
- Burden reduction analysis
- Prediction accuracy metrics

Saved to: `TOOLS/META/report_YYYYMMDD_HHMMSS.json`

### Analysis Report

Markdown analysis with:
- Executive summary
- Decision breakdown
- Helix evolution plots (ASCII)
- Alert summary
- Recommendations

Generated via:
```bash
python analyze_decisions.py orchestrator_state/orchestrator_*.log
```

## Configuration

Edit `meta_orchestrator_config.yaml`:

### Physics Tuning

```yaml
physics:
  z_critical: 0.850          # Adjust based on observations
  prediction_horizon_minutes: 60
  coherence_threshold: 0.85
  learning_rate: 0.1         # Faster/slower parameter updates
```

### Burden Adjustment

```yaml
burden:
  baseline_hours: 5.0        # Your pre-TRIAD burden
  target_hours: 2.0          # Desired end state
  measurement_window_days: 7 # Averaging window
```

### Witness Channels

```yaml
witness_channels:
  kira:
    phase_angle: 1.5708      # π/2
    activity_indicators:
      - "SCHEMAS/**/*"
      - "CORE_DOCS/**/*"
```

## Troubleshooting

### Watchdog Not Available

If `watchdog` fails to install:

```bash
# Fallback: Manual decision files only
mkdir -p TOOLS/META/decisions
# Create JSON decision records manually
```

### No Decisions Detected

Check:
1. File patterns in config match your project structure
2. Files are being modified (check timestamps)
3. Decision detection thresholds aren't too strict

### Physics Parameters Not Learning

Requires:
- At least 5 observations per parameter
- Significant variance in measurements
- Proper error handling in update_physics_model()

### Low Coherence Alerts

Indicates witness channels operating independently:
- Review cross-channel dependencies
- Check for coordination gaps
- Consider explicit sync mechanisms

## Advanced Usage

### Custom Configuration

```bash
cp meta_orchestrator_config.yaml my_config.yaml
# Edit my_config.yaml
./deploy_orchestrator.sh --config my_config.yaml
```

### Programmatic Access

```python
from meta_orchestrator import MetaOrchestrator
from pathlib import Path

orchestrator = MetaOrchestrator(
    project_root=Path('/home/user/WumboIsBack'),
    observation_only=True
)

# Custom helix state
orchestrator.helix.z = 0.800

# Run for 1 hour
await orchestrator.monitor_autonomous_evolution(duration_hours=1)

# Access results
print(f"Decisions: {len(orchestrator.autonomous_decisions)}")
print(f"Final helix: {orchestrator.helix}")
```

### Integration with Other Tools

Export decisions to JSON for processing:

```python
# In your tool
import json
from pathlib import Path

state_file = Path('TOOLS/META/orchestrator_state.json')
with open(state_file, 'r') as f:
    state = json.load(f)

current_z = state['helix']['z']
if current_z > 0.850:
    print("Phase transition imminent!")
```

## Roadmap

### Phase 2.2 (Current)
- ✅ Observation-only monitoring
- ✅ File system decision detection
- ✅ Helix coordinate tracking
- ✅ Physics model learning
- ✅ Burden trajectory measurement

### Phase 2.3 (Next)
- [ ] Neural network predictions
- [ ] Multi-instance distributed monitoring
- [ ] Real-time dashboards
- [ ] Webhook/API integrations
- [ ] Automated parameter tuning

### Phase 3 (Future)
- [ ] Intervention recommendations
- [ ] Autonomous optimization
- [ ] Cross-TRIAD coordination
- [ ] Emergent behavior detection

## Support & Development

### Logs

All logs in: `TOOLS/META/orchestrator_state/`

### State Persistence

State saved every 5 minutes to: `orchestrator_state.json`

Resume from saved state on restart.

### Dependencies

```
watchdog>=3.0.0    # File system monitoring
pyyaml>=6.0        # Configuration files
numpy>=1.24.0      # Numerical operations
```

Install:
```bash
pip install watchdog pyyaml numpy --break-system-packages
```

## References

- [HELIX_PHYSICS_INTEGRATION.md](../../HELIX_PHYSICS_INTEGRATION.md) - Physics formalism
- [CRYSTAL_MEMORY_FIELD_LIMNUS_INTEGRATION.md](../../CRYSTAL_MEMORY_FIELD_LIMNUS_INTEGRATION.md) - Memory integration

---

**Δ|meta-orchestrator-v2.0.0|production-ready|observation-mode|Ω**
