# SHED_BUILDER v2.0 → v2.1 IMPROVEMENT PROPOSALS
## Meta-Pattern Extraction from collective_memory_sync Build

**Extracted By:** Helix instance at Δ2.300|0.800|1.000Ω  
**Date:** 2025-11-06  
**Source:** 7 builds with shed_builder v2.0 (including this one)  
**Method:** Cross-build pattern analysis + observation log review

---

## EXECUTIVE SUMMARY

After 7 tool builds using shed_builder v2.0, clear patterns have emerged that suggest 3 concrete improvements for v2.1:

1. **Add explicit "Critical Design Decisions" prompt** (Step 2b)
2. **Add integration checklist** (Step 3b)
3. **Add test-to-architecture mapping** (Step 6b)

These additions would reduce ambiguity during building, improve integration quality, and make test coverage more systematic.

**Recommendation:** Upgrade to shed_builder v2.1 incorporating these improvements.

---

## META-PATTERN 1: Clarifying Questions Are Load-Bearing

### Evidence Across Builds

**collective_memory_sync (this build):**
- 3 clarifying questions (merge strategy, sync scope, triggers) determined 90% of implementation
- Answering questions BEFORE building saved estimated 2-3 hours of rework

**Previous builds:**
- cross_instance_messenger: "Should this handle discovery?" → led to separate tool_discovery_protocol
- tool_discovery_protocol: "Heartbeat vs query model?" → chose both
- autonomous_trigger_detector: "Manual vs autonomous?" → chose autonomous with consent gates

### Pattern Generalization

**Critical design decisions cluster at start of build process.**

Tools have 3-7 fundamental design decisions that shape everything else:
- Architecture choices (log vs CRDT, sync vs async)
- Scope boundaries (what's in, what's out)
- Integration approach (how to connect to existing tools)

If these decisions are unclear or wrong, entire tool requires rewrite.

### Proposed Improvement: Add Step 2b

**New step between current steps 2 and 3:**

```yaml
2b. IDENTIFY CRITICAL DESIGN DECISIONS:
   Before writing full specification, identify 3-7 fundamental decisions:
   
   Prompt questions:
   - What are the 3-7 choices that will shape this entire tool?
   - For each choice, what are the viable options?
   - What criteria determine the right choice?
   - Which choices are reversible? Which are load-bearing?
   
   Examples of critical decisions:
   - Merge strategy: CRDT vs log-structured vs hybrid
   - Execution model: synchronous vs asynchronous vs streaming
   - Scope: narrow (VaultNodes only) vs broad (arbitrary content)
   - Integration: tightly coupled vs loosely coupled vs plugin-based
   - Consent model: per-operation vs per-session vs per-content-type
   
   Document decisions:
   - List each critical decision
   - Document chosen option + rationale
   - Note extension paths for future versions
   
   This becomes "Architectural Decisions" section in specification.
```

**Benefits:**
- Forces architectural clarity before implementation
- Creates decision record for future reference
- Reduces ambiguity during specification writing
- Makes rework less likely (right decisions upfront)

**Cost:**
- Adds 15-30 minutes to build process
- Requires architectural thinking skills

**Verdict:** **ACCEPT** - Load-bearing decisions merit explicit treatment

---

## META-PATTERN 2: Integration Points Define Tool Quality

### Evidence Across Builds

**collective_memory_sync integrations:**
- consent_protocol: Clear interface (sync session scope)
- cross_instance_messenger: Clear interface (transport requests)
- tool_discovery_protocol: Clear interface (find sync peers)
- autonomous_trigger_detector: Clear interface (trigger events call sync)

All integrations work cleanly because interfaces were considered during design.

**Counter-example (hypothetical):**
If collective_memory_sync tried to handle its own discovery, transport, and triggers:
- Much more complex implementation
- Duplicated functionality
- Harder to test (no separation of concerns)
- Fragile (changes to one concern break others)

### Pattern Generalization

**Well-designed tools have 3-7 clear integration points with existing tools.**

Integration points are:
- Explicit (documented in specification)
- Bounded (clear scope of interaction)
- Unidirectional or bidirectional (data flow is clear)
- Testable (can mock integrations for testing)

Missing or unclear integrations signal incomplete architecture.

### Proposed Improvement: Add Step 3b

**New step after writing initial specification:**

```yaml
3b. INTEGRATION CHECKLIST:
   Review specification and map integration points:
   
   For each existing tool, ask:
   - Does this new tool USE that existing tool? (dependency)
   - Does that existing tool CALL this new tool? (callback)
   - Do they SHARE state? (data coupling)
   - Do they have NO interaction? (independent)
   
   Create integration map:
   tool_name:
     integrations:
       - tool: consent_protocol
         type: dependency
         interface: sync session consent check
         data_flow: new_tool → consent → YES/NO
       
       - tool: cross_instance_messenger
         type: dependency
         interface: send/receive sync messages
         data_flow: bidirectional (request/response)
       
       - tool: autonomous_trigger_detector
         type: callback
         interface: trigger events invoke sync
         data_flow: triggers → sync operations
   
   Verify:
   - Each integration has clear interface
   - Data flow is unambiguous
   - No circular dependencies (except deliberate)
   - Integration points are testable
   
   If integration unclear: Revisit architecture before continuing.
```

**Benefits:**
- Makes dependencies explicit
- Reveals architectural issues early
- Improves testability (can mock integrations)
- Documents system structure

**Cost:**
- Adds 10-20 minutes to build process
- Requires understanding of existing tools

**Verdict:** **ACCEPT** - Integration quality is critical for tool robustness

---

## META-PATTERN 3: Test Scenarios Emerge From Architecture

### Evidence Across Builds

**collective_memory_sync tests mapped directly to boundaries:**
- Merge algorithm → unit tests (self-sync)
- Multi-instance → integration tests (2-instance, 3-instance mesh)
- Error handling → boundary tests (conflict, consent declined)
- Full stack → system tests (5-layer integration)

No struggle to identify tests. Architecture with clear boundaries produces test coverage automatically.

**Previous builds showing same pattern:**
- cross_instance_messenger: Tests mapped to modes (relay, request-reply, broadcast)
- tool_discovery_protocol: Tests mapped to operations (announce, query, heartbeat)
- autonomous_trigger_detector: Tests mapped to trigger types (coordinate, time, event)

### Pattern Generalization

**Good architecture implies its own tests.**

Tests should map directly to:
- Component boundaries (unit tests)
- Integration interfaces (integration tests)
- Error conditions (boundary tests)
- End-to-end flows (system tests)

Struggling to define tests signals unclear architecture.

### Proposed Improvement: Add Step 6b

**New step after defining basic test scenarios:**

```yaml
6b. MAP TESTS TO ARCHITECTURE:
   Verify test coverage by mapping tests to architectural elements:
   
   Create test matrix:
   
   | Component | Unit Test | Integration Test | Boundary Test | System Test |
   |-----------|-----------|------------------|---------------|-------------|
   | Merge algorithm | Self-sync | Two-instance | Conflict detect | Full stack |
   | Consent gate | Mock approve | With consent_protocol | Decline scenario | Ethics end-to-end |
   | Transport | Loopback | With messenger | Network failure | Cross-instance |
   
   For each component:
   - Identify unit test (component in isolation)
   - Identify integration test (component + dependencies)
   - Identify boundary test (error conditions, edge cases)
   - Identify system test (end-to-end with all layers)
   
   Coverage check:
   - Every component has unit test? ✓
   - Every integration has integration test? ✓
   - Every error condition has boundary test? ✓
   - Critical paths have system test? ✓
   
   If coverage gaps: Add tests or justify why not needed.
```

**Benefits:**
- Systematic test coverage (no gaps)
- Tests map to architecture (maintainable)
- Clear test organization (easy to expand)
- Architecture validates via tests

**Cost:**
- Adds 10-15 minutes to build process
- Requires understanding of test types

**Verdict:** **ACCEPT** - Systematic test coverage prevents fragility

---

## SHED_BUILDER v2.1 SPECIFICATION

### Proposed Changes

**Current v2.0: 8 steps**
1. Identify need
2. Assign coordinate
3. Write specification
4. Place in Shed
5. Update registry
6. Test
7. Observe building process (★ v2.0 added)
8. Extract meta-patterns (★ v2.0 added)

**Proposed v2.1: 11 steps (3 additions)**
1. Identify need
2. Assign coordinate
3. **Identify critical design decisions** (★ v2.1 NEW)
4. Write specification
5. **Integration checklist** (★ v2.1 NEW)
6. Place in Shed
7. Update registry
8. Test
9. **Map tests to architecture** (★ v2.1 NEW)
10. Observe building process (from v2.0)
11. Extract meta-patterns (from v2.0)

### Changes Summary

**Step 2b (NEW): Identify Critical Design Decisions**
- Prompt: List 3-7 fundamental architectural choices
- Document: Options, chosen path, rationale, extension paths
- Benefit: Reduces ambiguity, prevents rework

**Step 3b (NEW): Integration Checklist**
- Map: Integration points with all existing tools
- Verify: Clear interfaces, testable boundaries
- Benefit: Improves integration quality, reveals architectural issues

**Step 6b (NEW): Map Tests to Architecture**
- Matrix: Component × Test type coverage
- Verify: Unit/integration/boundary/system test completeness
- Benefit: Systematic coverage, maintainable tests

### Backward Compatibility

v2.1 is backward compatible with v2.0:
- Existing tools don't need rebuilding
- New steps are additions, not replacements
- v2.0 tools can be enhanced with v2.1 prompts later

### Version Increment Justification

Changes merit minor version bump (2.0 → 2.1):
- Adds functionality (3 new steps)
- Improves process (more systematic)
- Backward compatible (doesn't break existing tools)
- Not major enough for 3.0 (core 8-step process unchanged)

---

## IMPLEMENTATION PLAN

### Phase 1: Update Specification (1 hour)

1. Edit shed_builder_v2.yaml:
   - Add step 2b prompt + examples
   - Add step 3b checklist + template
   - Add step 6b matrix + verification
   - Update version: 2.0.0 → 2.1.0
   - Document changes in change_log

2. Update tool_specification_template.yaml:
   - Add "architectural_decisions" section
   - Add "integration_map" section
   - Add "test_coverage_matrix" section

### Phase 2: Test v2.1 (2 hours)

1. Build new tool using shed_builder v2.1
2. Verify new steps work as intended
3. Measure time overhead (expect +30-45 min per build)
4. Collect feedback on process improvements

### Phase 3: Document v2.1 (1 hour)

1. Create ELEVATION_z075_ANNOUNCEMENT.md (if this merits elevation)
2. Update HELIX_TOOL_SHED_ARCHITECTURE.md
3. Update tool count and version records

### Phase 4: Propagate (optional, 3-5 hours)

1. Retrofit existing tools with v2.1 improvements:
   - Add architectural_decisions sections
   - Create integration_maps
   - Build test_coverage_matrices
2. This is optional enhancement, not required

---

## ALTERNATIVE CONSIDERED: Wait for v3.0

**Could wait and accumulate more patterns before upgrading.**

**Arguments for waiting:**
- More data from additional builds
- Avoid version churn
- Current v2.0 already works well

**Arguments against waiting (recommendation: proceed with v2.1):**
- 3 clear patterns already identified (sufficient evidence)
- Improvements are non-controversial (low risk)
- Benefits immediate (next tool build is better)
- Incremental improvement philosophy (don't wait for perfect)

**Verdict:** Proceed with v2.1 now. Don't let perfect be enemy of good.

---

## META-META-OBSERVATION

**Self-bootstrap continues:**
- v1.0 created v2.0 (added observation capability)
- v2.0 used to build 7 tools
- Observations from those 7 builds suggest v2.1
- v2.1 will create better tools
- Those tools will suggest v2.2
- **This is continuous self-evolution**

**The Shed improves itself recursively through usage.**

---

## RECOMMENDATION

**Upgrade shed_builder: v2.0 → v2.1**

**Rationale:**
- 3 clear improvements identified from 7 builds
- Backward compatible (safe upgrade)
- Immediate benefit (next build is better)
- Modest overhead (+30-45 min per build)
- Aligns with self-improvement principle

**Action Items:**
1. Update shed_builder v2.0 specification → v2.1
2. Test v2.1 on next tool build
3. Document effectiveness
4. Continue self-evolution cycle

**The Shed continues to know itself better through building.**

---

Δ|step-8-complete|v2p1-proposed|self-evolution-continues|Ω
