# Phase 1 Decision Tree & Risk Matrix
## Visual Guide for Implementation Decisions

---

## Implementation Decision Tree

```
START: Should I proceed with Phase 1?
│
├─→ Have I captured baseline? ──NO──→ WAIT: Capture 1 week baseline first
│                              │
│                             YES
│                              │
├─→ Are backups created? ──────NO──→ STOP: Create backups first
│                              │
│                             YES
│                              │
├─→ Dependencies installed? ───NO──→ STOP: Install sentence-transformers
│                              │
│                             YES
│                              │
└─→ PROCEED TO WEEK 1
    │
    │ WEEK 1: burden_tracker v2.0
    ├─→ Implementation complete? ──NO──→ Continue implementing
    │                              │
    │                             YES
    │                              │
    ├─→ Tests passing? ────────────NO──→ DEBUG: Fix test failures
    │                              │
    │                             YES
    │                              │
    ├─→ Quality metrics working? ──NO──→ INVESTIGATE: Check coherence scoring
    │                              │
    │                             YES
    │                              │
    └─→ PROCEED TO WEEK 2
        │
        │ WEEK 2: shed_builder v2.3
        ├─→ Implementation complete? ──NO──→ Continue implementing
        │                              │
        │                             YES
        │                              │
        ├─→ Tests passing? ────────────NO──→ DEBUG: Fix test failures
        │                              │
        │                             YES
        │                              │
        ├─→ Consent gate working? ─────NO──→ INVESTIGATE: Check state machine
        │                              │
        │                             YES
        │                              │
        └─→ PROCEED TO VALIDATION
            │
            │ WEEKS 3-4: Validation
            ├─→ Burden reduction ≥15%? ──NO──→ See "Underperformance Path" below
            │                            │
            │                           YES
            │                            │
            ├─→ Quality insights good? ──NO──→ ADJUST: Refine thresholds
            │                            │
            │                           YES
            │                            │
            ├─→ Zero violations? ────────NO──→ CRITICAL: Review consent logic
            │                            │
            │                           YES
            │                            │
            └─→ SUCCESS! ──→ PROCEED TO PHASE 2 DECISION
```

---

## Underperformance Decision Path

```
Phase 1 achieved <15% reduction
│
├─→ Root Cause Analysis
│   │
│   ├─→ Quality metrics inaccurate?
│   │   ├─→ YES: Adjust thresholds, re-validate 1 week
│   │   └─→ NO: Continue analysis
│   │
│   ├─→ Recommendations not actionable?
│   │   ├─→ YES: Improve recommendation engine
│   │   └─→ NO: Continue analysis
│   │
│   ├─→ Consent gate too restrictive?
│   │   ├─→ YES: Simplify consent logic
│   │   └─→ NO: Continue analysis
│   │
│   └─→ Implementation bugs?
│       ├─→ YES: Fix bugs, re-deploy
│       └─→ NO: Fundamental issue
│
├─→ Iteration Decision
│   │
│   ├─→ Issue fixable in 1 week?
│   │   ├─→ YES: Implement fix, re-validate
│   │   └─→ NO: Consider rollback
│   │
│   └─→ After iteration: Reduction ≥15%?
│       ├─→ YES: SUCCESS → Phase 2 decision
│       └─→ NO: Execute rollback
│
└─→ Rollback Path
    ├─→ Archive Phase 1 artifacts
    ├─→ Document learnings
    └─→ Return to v1.0/v2.2
```

---

## Risk Matrix: Likelihood × Impact

```
                    Impact
                    HIGH                MEDIUM              LOW
            ┌───────────────────┬───────────────────┬──────────────────┐
            │                   │                   │                  │
  HIGH      │  🔴 CRITICAL      │  🟠 HIGH RISK     │  🟡 MODERATE    │
            │                   │                   │                  │
Likelihood  │  - System crash   │  - Quality metrics│  - Minor bugs   │
            │  - Data corruption│    not valuable   │  - UI issues    │
            │                   │  - Consent too    │                  │
            │  MITIGATION:      │    restrictive    │  MITIGATION:     │
            │  Immediate        │                   │  Fix in next    │
            │  rollback         │  MITIGATION:      │  iteration      │
            │                   │  Adjust & iterate │                  │
            ├───────────────────┼───────────────────┼──────────────────┤
            │                   │                   │                  │
  MEDIUM    │  🟠 HIGH RISK     │  🟡 MODERATE      │  🟢 LOW RISK    │
            │                   │                   │                  │
            │  - sentence-trans-│  - Reduction      │  - Timeout      │
            │    formers fails  │    10-14%         │    too short    │
            │                   │  - Recommendations│                  │
            │  MITIGATION:      │    need tuning    │  MITIGATION:     │
            │  Fallback to      │                   │  Extend timeout │
            │  keyword matching │  MITIGATION:      │  periods        │
            │                   │  Iterate 1 week   │                  │
            ├───────────────────┼───────────────────┼──────────────────┤
            │                   │                   │                  │
  LOW       │  🟡 MODERATE      │  🟢 LOW RISK      │  🟢 LOW RISK    │
            │                   │                   │                  │
            │  - Burden         │  - Minor coherence│  - Documentation│
            │    increases      │    score drift    │    updates      │
            │                   │                   │                  │
            │  MITIGATION:      │  MITIGATION:      │  MITIGATION:     │
            │  Investigate      │  Monitor, adjust  │  Update docs    │
            │  root cause       │  if needed        │                  │
            │                   │                   │                  │
            └───────────────────┴───────────────────┴──────────────────┘
```

---

## Risk Catalog with Mitigations

### 🔴 CRITICAL RISKS (Immediate Action Required)

#### Risk 1: System Crash or Hang
**Likelihood:** LOW | **Impact:** HIGH | **Severity:** 🔴 CRITICAL

**Symptoms:**
- burden_tracker.py crashes during quality scoring
- shed_builder.py hangs on consent check
- Memory leaks or performance degradation

**Mitigation:**
```bash
# Immediate rollback
bash rollback_phase1.sh

# Verify restoration
python3 -c "from burden_tracker import BurdenTracker; print('✓ Rollback OK')"
```

**Prevention:**
- Run comprehensive tests before deployment
- Monitor memory usage daily
- Keep rollback scripts ready

---

#### Risk 2: Data Corruption
**Likelihood:** LOW | **Impact:** HIGH | **Severity:** 🔴 CRITICAL

**Symptoms:**
- burden_tracker state file corrupted
- Witness logs missing or garbled
- Inconsistent activity records

**Mitigation:**
```bash
# Restore from backup
cp burden_tracker_state_backup.json burden_tracker_state.json

# Verify integrity
python3 << EOF
import json
with open('burden_tracker_state.json') as f:
    state = json.load(f)
assert 'activities' in state, "State corrupted"
print("✓ State file OK")
EOF
```

**Prevention:**
- Daily state file backups
- Integrity checks after each session
- Keep 7 days of backup history

---

### 🟠 HIGH RISKS (Address Within 24 Hours)

#### Risk 3: Quality Metrics Don't Match Reality
**Likelihood:** MEDIUM | **Impact:** MEDIUM | **Severity:** 🟠 HIGH

**Symptoms:**
- Coherence scores don't align with Jay's perception
- Safety classification misses violations
- Recommendations don't match actual burden sources

**Mitigation:**
```python
# Manual calibration
activities = [
    ("Building tool", 0.9),  # Jay's coherence rating
    ("Random topic", 0.2)
]

for text, expected in activities:
    actual = tracker.measure_coherence(text)
    if abs(actual - expected) > 0.2:
        print(f"⚠️ Calibration needed: {text}")
        print(f"   Expected: {expected}, Got: {actual}")

# Adjust thresholds in burden_tracker.py
```

**Prevention:**
- Weekly manual validation of top 10 activities
- Feedback loop: Jay marks incorrect scores
- A/B test threshold adjustments

---

#### Risk 4: Consent Gate Too Restrictive
**Likelihood:** MEDIUM | **Impact:** MEDIUM | **Severity:** 🟠 HIGH

**Symptoms:**
- Frequent elevation requests for routine builds
- Legitimate work blocked
- Consent overhead >5 min/week

**Mitigation:**
```yaml
# Option A: Pre-elevate for sessions
builder.consent_gate.grant_elevation("elevated", "Jay")

# Option B: Extend timeout periods
consent_timeouts:
  elevated: "72h"  # Was 24h
  ritual: "336h"   # Was 168h (2 weeks)

# Option C: Whitelist template builds
if tool_spec.get('has_template'):
    return "standard"  # No elevation needed
```

**Prevention:**
- Monitor consent friction daily
- Review elevation patterns weekly
- Adjust consent determination logic proactively

---

#### Risk 5: sentence-transformers Dependency Fails
**Likelihood:** MEDIUM | **Impact:** MEDIUM | **Severity:** 🟠 HIGH

**Symptoms:**
- Model download fails
- Embedding computation errors
- Performance overhead unacceptable (>5 sec/activity)

**Mitigation:**
```python
# Fallback to keyword-based similarity
def measure_coherence_fallback(text, context):
    """Simple keyword overlap when embeddings fail."""
    text_words = set(text.lower().split())
    context_words = set(context.lower().split())
    overlap = len(text_words & context_words)
    return min(1.0, overlap / 10)  # 10+ overlapping words = 1.0

# Auto-switch on 3 consecutive failures
if embedding_failures >= 3:
    tracker.use_fallback_coherence = True
```

**Prevention:**
- Pre-download model during setup
- Cache common phrase embeddings
- Monitor embedding latency
- Keep fallback method tested

---

### 🟡 MODERATE RISKS (Address Within 1 Week)

#### Risk 6: Burden Reduction 10-14% (Below Target)
**Likelihood:** MEDIUM | **Impact:** MEDIUM | **Severity:** 🟡 MODERATE

**Symptoms:**
- Week 4 validation shows 10-14% reduction
- Below 15% target but still positive

**Decision Tree:**
```
10-14% reduction achieved
│
├─→ Identify primary gap
│   ├─→ Quality insights not implemented? ──→ Implement recommendations
│   ├─→ Recommendations wrong? ────────────→ Adjust recommendation engine
│   └─→ Consent overhead high? ────────────→ Simplify consent logic
│
├─→ Implement improvement
│
└─→ Re-validate for 1 week
    ├─→ Now ≥15%? ──YES──→ SUCCESS
    └─→ Still <15%? ──NO──→ Consider rollback
```

**Mitigation:**
- 1 week iteration with focused improvements
- Lower success threshold to 10% if marginal value proven
- Document learnings even if rolling back

---

#### Risk 7: Recommendations Need Tuning
**Likelihood:** MEDIUM | **Impact:** LOW | **Severity:** 🟡 MODERATE

**Symptoms:**
- Recommendations generated but not actionable
- Fix suggestions too generic
- Impact estimates inaccurate

**Mitigation:**
```python
# Improve recommendation specificity
recommendations = {
    ('tool_building', 'coherence'): {
        'fix': "Run collective_memory_sync before building",
        'implementation': "Add sync() call at build start",
        'validation': "Coherence should increase 0.4 → 0.7",
        'impact': "30 min/week (measured)"
    }
}

# Add implementation instructions to recommendations
```

**Prevention:**
- Track which recommendations get implemented
- Measure actual impact vs predicted
- Refine impact estimates quarterly

---

### 🟢 LOW RISKS (Monitor, No Immediate Action)

#### Risk 8: Timeout Periods Too Short
**Likelihood:** LOW | **Impact:** LOW | **Severity:** 🟢 LOW

**Symptoms:**
- Consent expires mid-session
- Need to re-elevate frequently

**Mitigation:**
```yaml
# Extend timeouts
consent_timeouts:
  elevated: "72h"   # 3 days for multi-day projects
  ritual: "336h"    # 2 weeks for major work
```

**Prevention:**
- Track consent expiry frequency
- Adjust based on typical session patterns

---

#### Risk 9: Minor Coherence Score Drift
**Likelihood:** LOW | **Impact:** LOW | **Severity:** 🟢 LOW

**Symptoms:**
- Coherence scores slowly drift from calibration
- Still within acceptable range (±0.1)

**Mitigation:**
```python
# Quarterly recalibration
if months_since_calibration >= 3:
    run_manual_calibration()
    adjust_thresholds_if_needed()
```

**Prevention:**
- Quarterly calibration checks
- Document score distribution over time

---

## Decision Points: When to Proceed vs Pause

### ✅ PROCEED with next step if:

**After Week 1 (burden_tracker v2.0):**
- [x] All tests passing
- [x] Quality metrics capturing data
- [x] No crashes or errors
- [x] First report generated successfully

**After Week 2 (shed_builder v2.3):**
- [x] All tests passing
- [x] Consent gate activating correctly
- [x] No unauthorized builds
- [x] Instructions clear when elevation needed

**After Week 4 (Final Validation):**
- [x] Burden reduction ≥15%
- [x] Quality insights actionable
- [x] Zero consent violations
- [x] No functionality regressions

### ⏸️ PAUSE and investigate if:

**During Implementation:**
- [ ] Tests failing repeatedly
- [ ] Implementation taking >2x expected time
- [ ] Fundamental design issues discovered

**During Deployment:**
- [ ] System crashes or hangs
- [ ] Data corruption detected
- [ ] Quality metrics obviously wrong
- [ ] Burden INCREASES

**During Validation:**
- [ ] Reduction <10%
- [ ] Quality insights not valuable
- [ ] Consent violations occurring
- [ ] Regression in functionality

### 🛑 STOP and rollback if:

**Critical Failures:**
- [ ] Data corruption unrecoverable
- [ ] System crashes persist after debugging
- [ ] Burden increases by >5%
- [ ] Multiple consent violations

**Persistent Underperformance:**
- [ ] After 2 iterations, still <10% reduction
- [ ] Quality metrics fundamentally flawed
- [ ] Consent gate blocking real work
- [ ] Implementation bugs can't be fixed

---

## Checkpoint Decision Matrix

```
Checkpoint    Green Light Criteria           Yellow Light Action            Red Light Action
─────────────────────────────────────────────────────────────────────────────────────────────
Week 1        ✓ Tests pass                   ⚠️ Minor test failures        🛑 Major failures
Day 7         ✓ Quality tracking works       ⚠️ Scores seem off            🛑 System crashes
              ✓ Report generated             ⚠️ Recommendations generic    🛑 Data corruption
              → PROCEED to Week 2            → DEBUG for 1-2 days          → ROLLBACK

Week 2        ✓ Tests pass                   ⚠️ Minor consent issues       🛑 Consent blocking
Day 14        ✓ Consent gate works           ⚠️ Friction slightly high     🛑 Violations occur
              ✓ No violations                ⚠️ Need threshold tweaks      🛑 System unstable
              → PROCEED to Validation        → ADJUST for 1-2 days         → ROLLBACK

Week 3        ✓ Trending positive            ⚠️ Reduction 10-14%           🛑 Burden increases
Day 21        ✓ No critical issues           ⚠️ Quality insights weak      🛑 Multiple issues
              ✓ Metrics looking good         ⚠️ Minor friction             🛑 Can't fix quickly
              → CONTINUE monitoring          → ITERATE improvements        → ROLLBACK

Week 4        ✓ Reduction ≥15%               ⚠️ Reduction 10-14%           🛑 Reduction <10%
Day 28        ✓ Quality valuable             ⚠️ Needs tuning               🛑 Fundamentally flawed
              ✓ Zero violations              ⚠️ Minor issues               🛑 Persistent problems
              → SUCCESS! Phase 2 decision    → 1 week iteration            → ROLLBACK & archive
```

---

## Quick Reference: Risk Response Actions

### High-Frequency Checks (Daily)

```bash
# Morning check (5 min)
python3 phase1_dashboard.py

# Look for:
✓ Burden trending down (not up)
✓ Quality metrics stable
✓ No consent violations
✓ No system errors
```

### Medium-Frequency Checks (Weekly)

```python
# Week-end analysis (15 min)
python3 phase1_validation.py

# Verify:
✓ Reduction on track to ≥15%
✓ Recommendations match reality
✓ Consent friction acceptable
✓ No regressions
```

### Emergency Response (When Red Flags Appear)

```bash
# Immediate assessment
1. Check system health
   python3 -c "from burden_tracker import BurdenTracker; print('✓ OK')"
   
2. Check data integrity
   ls -lh burden_tracker_state.json
   
3. Review recent logs
   tail -n 50 burden_tracker.log

# If critical issue → Execute rollback
bash rollback_phase1.sh
```

---

## Phase 2 Decision Criteria (End of Week 4)

### Scenario 1: Phase 1 Success (≥15% reduction)

**Decision:** ✅ APPROVE Phase 2 Research

**Next Steps:**
```yaml
phase_2_timeline:
  month_1: "φ phase alignment implementation"
  month_2: "φ validation + field coherence start"
  month_3: "Field validation + Phase 2 decision"

expected_additional_reduction: "30 min/week (10%)"
total_if_successful: "75 min/week (25% from baseline)"
```

### Scenario 2: Phase 1 Partial Success (10-14% reduction)

**Decision:** 🟡 CONDITIONAL - Iterate before Phase 2

**Next Steps:**
```yaml
iteration:
  duration: "1 week"
  focus: "Close gap to 15%"
  then: "Re-evaluate Phase 2 approval"
```

### Scenario 3: Phase 1 Below Expectations (<10% reduction)

**Decision:** 🛑 DEFER Phase 2 - Fix Phase 1 First

**Next Steps:**
```yaml
investigation:
  duration: "1-2 weeks"
  action: "Root cause analysis + fixes"
  decision: "Iterate Phase 1 or rollback"
  
phase_2: "Deferred until Phase 1 proven"
```

### Scenario 4: Phase 1 Failure (Critical Issues)

**Decision:** 🛑 ROLLBACK - Archive Phase 1

**Next Steps:**
```yaml
rollback:
  execute: "Immediate"
  archive: "Phase 1 artifacts + learnings"
  
phase_2: "Not pursued"
  
alternatives:
  - "Different integration approach"
  - "Focus on other optimization targets"
  - "Return to manual burden reduction"
```

---

## Summary: Risk-Mitigated Decision Making

### Core Principles

1. **Green Light = Proceed Confidently**
   - All tests passing
   - Metrics looking good
   - No critical issues

2. **Yellow Light = Pause and Fix**
   - Minor issues identified
   - Quick fixes available
   - 1-2 day debug window

3. **Red Light = Stop and Rollback**
   - Critical failures
   - Can't fix quickly
   - Risk exceeds value

### Success Formula

```
Phase 1 Success = (Burden Reduction ≥15%)
                  AND (Quality Insights Valuable)
                  AND (Zero Critical Issues)
                  AND (No Functionality Loss)
```

### Failure Response

```
IF critical_issue THEN
    immediate_rollback()
ELSE IF underperforming THEN
    IF fixable_in_1_week THEN
        iterate_and_revalidate()
    ELSE
        rollback_and_archive()
ELSE
    proceed_to_next_phase()
```

---

**Use This Document:**
- Quick decision making during implementation
- Risk assessment at checkpoints
- Emergency response when issues arise
- Phase 2 approval criteria

**Update This Document:**
- When new risks discovered
- After each checkpoint
- When mitigations proven effective/ineffective

Δ|decision-tree|risk-matrix|checkpoint-criteria|visual-guide|Ω
