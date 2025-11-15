# Phase 1 Quick-Start Checklist
## drift_os → TRIAD-0.83 Integration

**Target:** 15% Burden Reduction (45 min/week) via Quality Metrics + Consent Gates  
**Timeline:** 2 weeks implementation + 2 weeks validation  
**Risk Level:** LOW (reversible, self-contained additions)

---

## Pre-Flight Checklist

### ☐ Environment Ready

```bash
# Verify Python 3.7+
python3 --version

# Verify PyTorch
python3 -c "import torch; print('✓ PyTorch OK')"

# Check disk space (~500MB needed)
df -h /mnt/project

# Verify current tool versions
ls -lh /mnt/project/burden_tracker.yaml  # Should be v1.0
ls -lh /mnt/project/shed_builder_v22.yaml  # Should be v2.2
```

### ☐ Baseline Captured

```python
# Run burden_tracker v1.0 for ONE FULL WEEK before starting
# Save output to: baseline_burden_week_[date].json

{
  "total_weekly_burden": 5.0,  # Current hours/week
  "state_transfer_time": 2.5,
  "tool_building_time": 1.0,
  "documentation_time": 1.0,
  "coordination_time": 0.5,
  "measurement_date": "2025-11-09"
}
```

### ☐ Backups Created

```bash
# Create safety backups
cp burden_tracker.yaml burden_tracker_v1.0_backup.yaml
cp shed_builder_v22.yaml shed_builder_v2.2_backup.yaml
cp burden_tracker.py burden_tracker_v1.0_backup.py

# Verify backups exist
ls -lh *backup*
```

### ☐ Dependencies Installed

```bash
# Install sentence-transformers
pip install sentence-transformers --break-system-packages

# Download model (one-time, ~500MB)
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## Week 1: burden_tracker v2.0

### Day 1-2: Implementation

**☐ Update burden_tracker.yaml specification**
- Location: `/mnt/project/burden_tracker.yaml`
- Changes: Add quality_metrics section, update version to 2.0.0
- Reference: PHASE_1_IMPLEMENTATION_INSTRUCTIONS.md Section "Phase 1A Step 1"

**☐ Implement QualityTracker class**
- Location: `/mnt/project/burden_tracker.py`
- Add: `class QualityTracker` with coherence/safety/conciseness methods
- Reference: PHASE_1_IMPLEMENTATION_INSTRUCTIONS.md Section "Phase 1A Step 2"

**☐ Update BurdenTracker main class**
- Location: `/mnt/project/burden_tracker.py`
- Integrate: `self.quality_tracker = QualityTracker()`
- Add quality metrics to `process_conversation()`
- Reference: PHASE_1_IMPLEMENTATION_INSTRUCTIONS.md Section "Phase 1A Step 3"

### Day 3: Testing

**☐ Create test suite**
- Location: `/mnt/project/test_burden_tracker_v2.py`
- Tests: coherence, safety, conciseness, end-to-end
- Reference: PHASE_1_IMPLEMENTATION_INSTRUCTIONS.md Section "Phase 1A Step 4"

**☐ Run tests**
```bash
python3 test_burden_tracker_v2.py
# Expected: ALL TESTS PASSED ✓
```

### Day 4-7: Deployment & Monitoring

**☐ Deploy v2.0**
```bash
python3 /mnt/project/burden_tracker.py
```

**☐ Monitor daily**
```python
# Check quality metrics daily
from burden_tracker import BurdenTracker
tracker = BurdenTracker()
tracker.load_state('burden_tracker_state.json')

# Quick quality check
print(f"Coherence today: {tracker.avg_coherence:.2f}")
print(f"Safety today: {tracker.avg_safety:.2f}")
```

**☐ Week 1 checkpoint (Day 7)**
- [ ] Quality metrics captured for all activities
- [ ] No crashes or errors
- [ ] First weekly report generated
- [ ] Recommendations are sensible

**Decision:** If all checks pass → Proceed to Week 2  
**If issues:** Debug before continuing

---

## Week 2: shed_builder v2.3

### Day 8-9: Implementation

**☐ Extend consent_protocol.yaml**
- Location: `/mnt/project/consent_protocol.yaml`
- Add: `tool_building_scope` section with consent levels
- Reference: PHASE_1_IMPLEMENTATION_INSTRUCTIONS.md Section "Phase 1B Step 1"

**☐ Update shed_builder specification**
- Location: Create `/mnt/project/shed_builder_v23.yaml`
- Changes: Add consent_integration section, update version
- Reference: PHASE_1_IMPLEMENTATION_INSTRUCTIONS.md Section "Phase 1B Step 2"

**☐ Implement ConsentGate class**
- Location: `/mnt/project/shed_builder.py`
- Add: `class ConsentGate` with consent checking logic
- Reference: PHASE_1_IMPLEMENTATION_INSTRUCTIONS.md Section "Phase 1B Step 3"

**☐ Integrate consent gate into ShedBuilder**
- Location: `/mnt/project/shed_builder.py`
- Update: `build_tool()` method to check consent
- Reference: PHASE_1_IMPLEMENTATION_INSTRUCTIONS.md Section "Phase 1B Step 3"

### Day 10: Testing

**☐ Create test suite**
- Location: `/mnt/project/test_shed_builder_v2.3.py`
- Tests: consent hierarchy, timeout, elevation, integration
- Reference: PHASE_1_IMPLEMENTATION_INSTRUCTIONS.md Section "Phase 1B Step 4"

**☐ Run tests**
```bash
python3 test_shed_builder_v2.3.py
# Expected: ALL TESTS PASSED ✓
```

### Day 11-14: Deployment & Monitoring

**☐ Deploy v2.3**
```bash
python3 << EOF
from shed_builder import ShedBuilder
builder = ShedBuilder()
print(f"Consent level: {builder.consent_gate.get_current_level()}")
EOF
```

**☐ Monitor daily**
```python
# Check consent state
from shed_builder import ShedBuilder
builder = ShedBuilder()

print(f"Current consent: {builder.consent_gate.get_current_level()}")

# Review proposals
proposals = [l for l in builder.witness.logs 
             if l['event'] == 'consent_elevation_requested']
print(f"Proposals today: {len(proposals)}")
```

**☐ Week 2 checkpoint (Day 14)**
- [ ] No premature tool deployments
- [ ] Consent gate activated appropriately
- [ ] Instructions clear when elevation needed
- [ ] Minimal consent friction

**Decision:** If all checks pass → Proceed to Validation  
**If issues:** Adjust consent logic

---

## Weeks 3-4: Validation & Decision

### Week 3: Comprehensive Monitoring

**☐ Run daily metrics collection**
```bash
python3 /mnt/project/collect_daily_metrics.py
```

**☐ Monitor dashboard daily**
```bash
python3 /mnt/project/phase1_dashboard.py
```

**Daily checks:**
- [ ] Burden trending down
- [ ] Quality metrics stable
- [ ] No consent violations
- [ ] No system issues

### Week 4: Final Validation

**☐ Run validation script**
```bash
python3 /mnt/project/phase1_validation.py
```

**☐ Review success criteria**

```yaml
Phase 1 Success = ALL of:
  ✓ Burden reduction ≥15% (45 min/week)
  ✓ Quality insights actionable (≥3 recommendations/week)
  ✓ Zero premature deployments
  ✓ No functionality regressions
```

**☐ Make Phase 2 decision**

**If Phase 1 SUCCESS:**
```yaml
next_steps:
  - Document Phase 1 learnings
  - Approve Phase 2 research (φ alignment, field coherence)
  - Timeline: 2-3 months for Phase 2
  - Expected: Additional 30 min/week reduction
```

**If Phase 1 UNDERPERFORMED (<15% reduction):**
```yaml
next_steps:
  - Root cause analysis
  - Adjust quality thresholds or consent logic
  - Re-run 2-week validation
  - If still underperforming: consider rollback
```

**If Phase 1 FAILED (critical issues):**
```yaml
next_steps:
  - Execute rollback procedure
  - Document failure reasons
  - Archive Phase 1 artifacts
  - Return to v1.0/v2.2
```

---

## Emergency Rollback

### When to Rollback

**IMMEDIATE rollback if:**
- System crashes or hangs
- Data corruption detected
- Critical functionality broken
- Burden INCREASES instead of decreases

### How to Rollback

```bash
# Complete rollback script
cd /mnt/project

# Stop tracking
pkill -f burden_tracker.py

# Restore backups
cp burden_tracker_v1.0_backup.yaml burden_tracker.yaml
cp shed_builder_v2.2_backup.yaml shed_builder_v22.yaml
cp burden_tracker_v1.0_backup.py burden_tracker.py

# Verify restoration
python3 << EOF
from burden_tracker import BurdenTracker
from shed_builder import ShedBuilder

tracker = BurdenTracker()
builder = ShedBuilder()

assert not hasattr(tracker, 'quality_tracker'), "Quality tracker still present!"
assert not hasattr(builder, 'consent_gate'), "Consent gate still present!"

print("✓ Rollback successful")
print("✓ System restored to v1.0/v2.2")
EOF
```

**After rollback:**
- Archive Phase 1 files to `phase1_rollback_[date]/`
- Document rollback reason in `ROLLBACK_REASON.md`
- Resume normal operations with v1.0/v2.2

---

## Success Metrics At-a-Glance

### Primary Metrics

| Metric | Target | Measurement | Status Check |
|--------|--------|-------------|--------------|
| Burden Reduction | ≥15% | Compare Week 4 to baseline | Daily dashboard |
| Quality Insights | ≥3/week actionable | Count recommendations | Weekly report |
| Consent Safety | 0 violations | Count unauthorized builds | Witness logs |
| No Regressions | 0 issues | Functional comparison | Test suite |

### Weekly Checkpoints

**Week 1:** burden_tracker v2.0 operational, quality tracking works  
**Week 2:** shed_builder v2.3 operational, consent gate works  
**Week 3:** Metrics trending positive, no critical issues  
**Week 4:** Final validation, Phase 2 decision

### Red Flags

**STOP and investigate if:**
- ⚠️ Quality metrics don't match reality
- ⚠️ Recommendations not actionable
- ⚠️ Consent gate blocks legitimate work
- ⚠️ System crashes or errors
- ⚠️ Burden INCREASES
- ⚠️ sentence-transformers fails repeatedly

**Action:** Pause deployment, debug issue, consider rollback

---

## Phase 2 Preview (If Phase 1 Succeeds)

### What Phase 2 Adds

**1. φ Phase Alignment Tracking**
- Measures instance coherence during coordination
- Expected: 20%+ faster consensus (20 min/week reduction)
- Timeline: 2-3 months research + validation
- Risk: Medium

**2. Field Coherence Monitoring**
- Tracks semantic field coherence across instances
- Expected: Early warning on coordination issues (10 min/week)
- Timeline: 2-3 months research + validation
- Risk: High (complex distributed computation)

### Phase 2 Decision Criteria

**Proceed with Phase 2 if:**
- Phase 1 achieved ≥15% reduction
- Quality insights proven valuable
- No unresolved Phase 1 issues
- Jay approves collective research

**Defer Phase 2 if:**
- Phase 1 underperformed
- Higher priority work exists
- Insufficient research time available

---

## Quick Reference: Key Commands

```bash
# Install dependencies
pip install sentence-transformers --break-system-packages

# Run tests
python3 test_burden_tracker_v2.py
python3 test_shed_builder_v2.3.py

# Daily monitoring
python3 phase1_dashboard.py
python3 collect_daily_metrics.py

# Validation
python3 phase1_validation.py

# Emergency rollback
bash rollback_phase1.sh
```

---

## Support & Resources

**Full Implementation Guide:**  
`PHASE_1_IMPLEMENTATION_INSTRUCTIONS.md`  
(74,000+ lines, comprehensive specifications)

**Key Sections:**
- Pre-Implementation Checklist (page 1)
- Phase 1A: burden_tracker v2.0 (page 5)
- Phase 1B: shed_builder v2.3 (page 15)
- Risk Mitigation Strategies (page 30)
- Rollback Procedures (page 35)
- Success Metrics Dashboard (page 38)

**Questions or Issues:**
- Review risk mitigation section for common issues
- Check rollback procedures if critical failure
- Consult comprehensive guide for detailed specs

---

## Final Pre-Flight Check

**Before starting implementation, verify:**

- [ ] I have captured a full week baseline measurement
- [ ] I have created backups of all files
- [ ] I have installed sentence-transformers successfully
- [ ] I understand the rollback procedure
- [ ] I am prepared to monitor daily for 2 weeks
- [ ] I have read the comprehensive implementation guide
- [ ] I approve proceeding with Phase 1 integration

**If all checks pass:** ✓ Ready for Phase 1 implementation  
**If any check fails:** ❌ Resolve before proceeding

---

**Status:** Ready for Deployment  
**Estimated Total Time:** 6-8 hours implementation + 4 weeks monitoring  
**Expected Outcome:** 15% burden reduction (45 min/week)

Δ|quick-start|phase-1-checklist|risk-mitigated|ready-to-deploy|Ω
