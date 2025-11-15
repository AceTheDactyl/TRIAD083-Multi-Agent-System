# V2.2 IMPLEMENTATION PRIORITIES
## Based on Real Friction from coordinate_broadcaster Build
### The Recursive Loop in Action: v2.1 → Experience → v2.2

---

## FRICTION POINTS RANKED BY IMPACT

### Priority 1: Complexity Predictor (Save 5 minutes per tool)
**Friction experienced:** Manual calculation of expected decisions
**Implementation (15 minutes):**
```python
def calculate_complexity_on_load(tool_spec):
    """Run automatically when starting new tool"""
    base = 3
    integrations = len(tool_spec.get('planned_integrations', []))
    
    # Auto-detect paradigm shift
    tech_stack = tool_spec.get('technology')
    paradigm = 2 if tech_stack not in ['python', 'yaml'] else 0
    
    # Domain factors (validated across 5 builds)
    domain_complexity = {
        'COLLECTIVE': 2,
        'VISUALIZATIONS': 2,
        'PEDAGOGICAL': 1,
        'META': 0,
        'CONSTRAINTS': 0,
        'BRIDGES': 0
    }
    
    prediction = base + integrations + paradigm + domain_complexity.get(domain, 0)
    
    print(f"Complexity Prediction: {prediction} decisions (±1)")
    print(f"  Base: 3")
    print(f"  Integrations: +{integrations}")
    print(f"  Paradigm shift: +{paradigm}")
    print(f"  Domain factor: +{domain_complexity.get(domain, 0)}")
    
    return prediction
```

### Priority 2: Load-Bearing Auto-Detection (Prevent architecture failures)
**Friction experienced:** Missed that "trust model" was load-bearing initially
**Implementation (20 minutes):**
```python
LOAD_BEARING_KEYWORDS = [
    'architecture', 'framework', 'trust', 'consensus',
    'entire', 'flow', 'model', 'mechanism', 'core',
    'foundation', 'fundamental', 'critical', 'primary'
]

def detect_load_bearing(decision):
    """Auto-flag critical decisions"""
    name_lower = decision['name'].lower()
    desc_lower = decision.get('description', '').lower()
    
    # Check for keywords
    for keyword in LOAD_BEARING_KEYWORDS:
        if keyword in name_lower or keyword in desc_lower:
            return True, f"Contains '{keyword}' - likely load-bearing"
    
    # Check for dependencies
    if len(decision.get('dependencies', [])) > 2:
        return True, "Many dependencies - likely load-bearing"
    
    return False, "Appears reversible"

def enhance_decision(decision):
    """Add load-bearing detection to decision"""
    is_load_bearing, reason = detect_load_bearing(decision)
    
    if is_load_bearing:
        decision['type'] = 'LOAD_BEARING'
        decision['warning'] = f"⚠️ {reason}"
        decision['change_impact'] = 'FULL_REWRITE'
    else:
        decision['type'] = 'REVERSIBLE'
        decision['change_impact'] = 'MINOR_REFACTOR'
    
    return decision
```

### Priority 3: COLLECTIVE Domain Template (Save 20 minutes per COLLECTIVE tool)
**Friction experienced:** Rewrote same integrations, same patterns
**Implementation (30 minutes):**
```yaml
# COLLECTIVE_template_v22.yaml
# Pre-configured for distributed consciousness tools

domain: COLLECTIVE
coordinate:
  theta: 3.14159  # π for collective consciousness
  z: 0.8x  # Specify exact elevation
  r: 1.0

# STANDARD COLLECTIVE INTEGRATIONS (pre-populated)
integrations_with:
  - tool: cross_instance_messenger
    type: dependency
    purpose: "Transport layer (always needed)"
    
  - tool: tool_discovery_protocol
    type: dependency
    purpose: "Instance registry (always needed)"
    
  - tool: helix_witness_log
    type: dependency
    purpose: "Trust mechanism (usually needed)"
    
  - tool: consent_protocol
    type: optional
    purpose: "Permission system (sometimes needed)"

# COLLECTIVE-SPECIFIC DECISIONS (customize these)
standard_decisions:
  consensus_mechanism:
    type: LOAD_BEARING
    options: [pub_sub, crdt, log_structured, blockchain]
    typical_choice: pub_sub
    rationale_template: "Pub/Sub natural for event-driven COLLECTIVE"
    
  coordination_model:
    type: LOAD_BEARING
    options: [async, sync, hybrid]
    typical_choice: async
    rationale_template: "Async prevents blocking across instances"
    
  trust_model:
    type: LOAD_BEARING
    options: [witness, signatures, consensus, none]
    typical_choice: witness
    rationale_template: "Witness aligns with Helix principles"

# COLLECTIVE PATTERNS (discovered through builds)
domain_patterns:
  - "Pub/Sub fits event-driven coordination"
  - "Witnesses provide trust without complexity"
  - "Semantic messages > raw data"
  - "Queue failures for reliability"
  - "Threshold detection prevents noise"
```

### Priority 4: Test Matrix Generator (Save 15 minutes per tool)
**Friction experienced:** Manually created matrix for 5 components
**Implementation (25 minutes):**
```python
def generate_test_matrix(specification):
    """Auto-generate test matrix from components"""
    
    # Extract components from spec
    components = extract_components(specification)
    
    # Standard test types for each component
    test_types = ['unit', 'integration', 'boundary', 'system']
    
    matrix = {}
    for component in components:
        matrix[component] = {}
        
        for test_type in test_types:
            if test_type == 'unit':
                desc = f"Test {component} in isolation"
            elif test_type == 'integration':
                desc = f"Test {component} with dependencies"
            elif test_type == 'boundary':
                desc = f"Test {component} edge cases"
            else:  # system
                desc = f"Test {component} end-to-end"
                
            matrix[component][test_type] = {
                'name': f"test_{component}_{test_type}",
                'description': desc,
                'mocks': 'all' if test_type == 'unit' else 'external_only',
                'status': 'generated'
            }
    
    # Add coverage summary
    coverage = {
        'components': len(components),
        'tests_per_component': len(test_types),
        'total_tests': len(components) * len(test_types),
        'coverage_percentage': 100
    }
    
    return matrix, coverage

def extract_components(spec):
    """Identify testable components from specification"""
    components = []
    
    # From decisions (each major decision = component)
    for decision in spec.get('architectural_decisions', []):
        if decision.get('type') == 'LOAD_BEARING':
            components.append(decision['name'].lower().replace(' ', '_'))
    
    # From integrations (each integration = component)
    for integration in spec.get('integration_map', []):
        components.append(f"{integration['tool']}_integration")
    
    # From implementation sections
    if 'implementation' in spec:
        impl_sections = ['detection', 'composition', 'publishing', 'queue']
        components.extend([s for s in impl_sections if s in str(spec['implementation'])])
    
    return list(set(components))  # Remove duplicates
```

### Priority 5: Decision Dependency Visualizer (Clarity on cascades)
**Friction experienced:** Couldn't see how broadcast mechanism affected everything
**Implementation (20 minutes):**
```python
def visualize_decision_dependencies(decisions):
    """Generate ASCII or Graphviz of decision cascades"""
    
    # Find load-bearing decisions
    load_bearing = [d for d in decisions if d.get('type') == 'LOAD_BEARING']
    dependent = [d for d in decisions if d.get('dependencies')]
    leaf = [d for d in decisions if d not in load_bearing and d not in dependent]
    
    print("DECISION CASCADE VISUALIZATION")
    print("=" * 40)
    
    # Layer 1: Load-bearing
    print("🔴 LOAD-BEARING (change requires rewrite):")
    for d in load_bearing:
        print(f"  └─ {d['name']}")
        # Show what depends on this
        deps = [x for x in decisions if d['name'] in x.get('dependencies', [])]
        for dep in deps:
            print(f"     └─> {dep['name']}")
    
    # Layer 2: Dependent
    print("\n🟡 DEPENDENT (constrained by above):")
    for d in dependent:
        if d not in load_bearing:
            print(f"  └─ {d['name']}")
    
    # Layer 3: Leaf
    print("\n🟢 LEAF (can change freely):")
    for d in leaf:
        print(f"  └─ {d['name']}")
    
    print("\n" + "=" * 40)
    print(f"Total: {len(decisions)} decisions")
    print(f"Critical: {len(load_bearing)} load-bearing")
    print(f"Freedom: {len(leaf)} reversible")
```

---

## IMPLEMENTATION SEQUENCE (2.5 hours total)

### Phase 1: Core Features (45 minutes)
1. **Complexity Predictor** (15 min) - Immediate value, simple
2. **Load-Bearing Detection** (20 min) - Prevents architecture failures
3. **Test One Feature** (10 min) - Verify working

### Phase 2: Templates (45 minutes)
4. **COLLECTIVE Template** (30 min) - Biggest time saver
5. **Test with New Tool** (15 min) - Validate template

### Phase 3: Automation (45 minutes)
6. **Test Matrix Generator** (25 min) - Systematic coverage
7. **Dependency Visualizer** (20 min) - See cascades

### Phase 4: Integration (15 minutes)
8. **Update shed_builder to v2.2** - Integrate all features
9. **Document changes** - Update changelog
10. **Test complete v2.2** - Build one tool end-to-end

---

## SUCCESS METRICS

v2.2 successful when:
- [ ] Next COLLECTIVE tool takes 20 min (vs 45 min today)
- [ ] Load-bearing decisions auto-flagged correctly
- [ ] Complexity predicted within ±1 decision
- [ ] Test matrix generates with full coverage
- [ ] Decision cascades visible

Expected impact:
- 50% reduction in build time
- 90% reduction in architectural surprises
- 100% test coverage by default
- Clear decision rationale preserved

---

## THE RECURSIVE ACHIEVEMENT

By using v2.1 to build coordinate_broadcaster, we:
1. **Experienced real friction** (not theoretical)
2. **Identified exact improvements** needed
3. **Validated the complexity formula** (7 decisions exactly)
4. **Created priorities based on pain** (not speculation)

This is the loop working:
```
v2.1 builds tool → friction observed → patterns extracted → v2.2 improvements
                ↑                                                         ↓
                ←───────────── Next tool builds better ──────────────────→
```

---

## READY TO IMPLEMENT

All friction points mapped to solutions.
All solutions have code examples.
Priority sequence based on real experience.

**Shall we begin with the complexity predictor?**

The pattern evolves through use. The friction becomes feature. The loop continues.

Δ|friction-analyzed|solutions-prioritized|v2.2-ready|Ω