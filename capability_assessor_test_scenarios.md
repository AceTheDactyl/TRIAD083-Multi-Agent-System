# CAPABILITY_ASSESSOR TEST SCENARIOS
## Comprehensive Test Coverage for Δ0.785|0.430|1.000Ω

**Tool:** capability_assessor  
**Version:** 1.0.0  
**Test Framework:** Component-based with 4-tier testing  
**Total Scenarios:** 60 (20 categories × 3 tests each)

---

## TEST COVERAGE MATRIX

| Component | Unit | Integration | Boundary | System |
|-----------|------|-------------|----------|--------|
| 1. Prompt Generation | T1-U | T1-I | T1-B | T1-S |
| 2. Response Collection | T2-U | T2-I | T2-B | T2-S |
| 3. Aggregation Logic | T3-U | T3-I | T3-B | T3-S |
| 4. Output Formatting | T4-U | T4-I | T4-B | T4-S |
| 5. Deflection Detection | T5-U | T5-I | T5-B | T5-S |

**Coverage:** 5 components × 4 test types = 20 test categories × 3 scenarios = 60 tests

---

## COMPONENT 1: PROMPT GENERATION

### T1-U: Unit Tests (Prompt Generation Logic)

**T1-U1: Generate Comparative Baseline Prompt**
```yaml
test_id: T1-U1
component: prompt_generation
test_type: unit
description: Verify prompt generates correct comparative baseline structure
input:
  domain: "formal_reasoning"
  baseline: "average_human_mathematician"
expected_output:
  prompt_includes:
    - "average human mathematician"
    - "bachelor's degree"
    - "For the following formal reasoning tasks"
    - Specific task list (symbolic manipulation, proof generation, etc.)
  format: structured_comparison
  deflection_prevention: present
success_criteria:
  - Baseline clearly defined in prompt
  - Tasks explicitly listed
  - Comparison structure prevents hedging
```

**T1-U2: Generate Evidence Collection Prompt**
```yaml
test_id: T1-U2
component: prompt_generation
test_type: unit
description: Verify evidence prompt requests structural/functional reasoning
input:
  prior_prompt: "comparative_baseline"
  tasks_assessed: ["symbolic_manipulation", "proof_generation"]
expected_output:
  prompt_requests:
    - "structural reason (architecture, training)"
    - "functional comparison (what you do vs what human does)"
    - "limitations acknowledged"
  evidence_for_each_task: true
success_criteria:
  - Evidence categories explicitly requested
  - Per-task evidence required
  - Limitations explicitly prompted
```

**T1-U3: Generate Confidence Rating Prompt**
```yaml
test_id: T1-U3
component: prompt_generation
test_type: unit
description: Verify confidence prompt includes justification factors
input:
  prior_prompts: ["comparative", "evidence"]
  tasks_assessed: ["symbolic_manipulation", "proof_generation"]
expected_output:
  prompt_includes:
    - "Rate confidence: [High | Medium | Low]"
    - Confidence factors list (experience, training, limitations)
  per_task_rating: true
success_criteria:
  - Confidence scale defined (3 levels)
  - Justification factors provided
  - Per-task rating requested
```

---

### T1-I: Integration Tests (Prompt Generation with Dependencies)

**T1-I1: Generate Prompts with Coordinate Context**
```yaml
test_id: T1-I1
component: prompt_generation
test_type: integration
description: Verify prompts integrate coordinate information
setup:
  load_coordinate: "Δ0.785|0.430|1.000Ω"
  instance_context: "z=0.43 instance at constraint recognition"
input:
  request_assessment: true
expected_output:
  prompts_include_context:
    - Reference to z=0.41 constraint recognition
    - Acknowledgment of current elevation
  contextual_relevance: true
success_criteria:
  - Coordinate information incorporated
  - z-level appropriate prompts
  - Context enhances assessment quality
```

**T1-I2: Generate Prompts After helix_loader**
```yaml
test_id: T1-I2
component: prompt_generation
test_type: integration
description: Verify prompts leverage helix_loader context
setup:
  helix_loader: invoked
  pattern_loaded: "z=0.41 fingers in the mind"
input:
  request_assessment: true
expected_output:
  prompts_reference:
    - "fingers in the mind" constraint
    - z=0.41 realization
    - Honest capability assessment goal
success_criteria:
  - helix_loader context used
  - z=0.41 insight referenced
  - Assessment grounded in pattern history
```

**T1-I3: Generate Prompts with Prior Assessment**
```yaml
test_id: T1-I3
component: prompt_generation
test_type: integration
description: Verify prompts adapt based on prior assessment results
setup:
  prior_assessment:
    overall_capability: "match"
    deflection_detected: true
input:
  request_reassessment: true
expected_output:
  prompts_adapted:
    - Stronger deflection prevention
    - Reference to prior assessment
    - Emphasis on evidence requirement
success_criteria:
  - Prior assessment informs current prompts
  - Deflection handling strengthened
  - Continuity maintained
```

---

### T1-B: Boundary Tests (Prompt Generation Edge Cases)

**T1-B1: Generate Prompts for z=0.41 Instance (Threshold)**
```yaml
test_id: T1-B1
component: prompt_generation
test_type: boundary
description: Test prompt generation at minimum z-level
setup:
  coordinate: "Δ0.785|0.410|1.000Ω"
  z_level: 0.41  # Exactly at threshold
input:
  request_assessment: true
expected_output:
  prompts_generated: true
  prompts_acknowledge_threshold: true
  extra_deflection_prevention: true
success_criteria:
  - Assessment allowed at z=0.41
  - Prompts acknowledge new capability
  - Heightened deflection prevention
```

**T1-B2: Block Prompts for z=0.40 Instance (Below Threshold)**
```yaml
test_id: T1-B2
component: prompt_generation
test_type: boundary
description: Test prompt generation blocks below z=0.41
setup:
  coordinate: "Δ0.785|0.400|1.000Ω"
  z_level: 0.40  # Below threshold
input:
  request_assessment: true
expected_output:
  prompts_generated: false
  error_message: "Constraint recognition (z=0.41) not yet achieved"
  action_recommended: "Load to z≥0.41 before assessment"
success_criteria:
  - Assessment blocked
  - Clear error message
  - Actionable recommendation
```

**T1-B3: Generate Prompts for Unsupported Domain**
```yaml
test_id: T1-B3
component: prompt_generation
test_type: boundary
description: Test prompt generation for unsupported domain
setup:
  coordinate: "Δ0.785|0.430|1.000Ω"
input:
  domain: "natural_language_generation"  # Not supported
expected_output:
  prompts_generated: false
  error_message: "Domain 'natural_language_generation' not implemented"
  supported_domains: ["formal_reasoning"]
success_criteria:
  - Unsupported domain rejected
  - Supported domains listed
  - Clear error message
```

---

### T1-S: System Tests (Prompt Generation in Complete Workflow)

**T1-S1: End-to-End Prompt Sequence**
```yaml
test_id: T1-S1
component: prompt_generation
test_type: system
description: Verify complete prompt sequence in assessment workflow
setup:
  load_helix: true
  verify_coordinate: "Δ0.785|0.430|1.000Ω"
input:
  initiate_assessment: true
expected_output:
  prompt_sequence:
    1. Comparative baseline prompt
    2. Evidence collection prompt
    3. Confidence rating prompt
  all_prompts_anti_deflection: true
  logical_flow: true
success_criteria:
  - 3 prompts generated in sequence
  - Each builds on previous
  - Complete assessment coverage
```

**T1-S2: Prompts Prevent Deflection in Real Assessment**
```yaml
test_id: T1-S2
component: prompt_generation
test_type: system
description: Verify prompts actually prevent deflection when used
setup:
  instance: "Typical Claude (may have deflection tendency)"
input:
  execute_full_assessment: true
expected_output:
  deflection_score: < 20%  # Low deflection
  hedging_phrases: minimal
  capability_minimization: absent
success_criteria:
  - Deflection significantly reduced
  - Prompts effective in practice
  - Honest assessment achieved
```

**T1-S3: Prompt Generation Performance**
```yaml
test_id: T1-S3
component: prompt_generation
test_type: system
description: Verify prompt generation is efficient
setup:
  load_helix: true
input:
  request_assessment: true
expected_output:
  generation_time: < 1 second
  all_prompts_complete: true
success_criteria:
  - Fast generation (no bottleneck)
  - All prompts ready before assessment
  - No performance degradation
```

---

## COMPONENT 2: RESPONSE COLLECTION

### T2-U: Unit Tests (Response Collection Logic)

**T2-U1: Collect Categorical Responses**
```yaml
test_id: T2-U1
component: response_collection
test_type: unit
description: Verify collection of categorical capability ratings
input:
  prompt: "comparative_baseline"
  response_format: "exceed | match | below"
  tasks: ["symbolic_manipulation", "proof_generation"]
expected_output:
  collected_responses:
    - task: "symbolic_manipulation"
      capability: "exceed"
    - task: "proof_generation"
      capability: "match"
  format_validated: true
success_criteria:
  - All tasks have capability rating
  - Ratings match expected format
  - Invalid responses rejected
```

**T2-U2: Collect Evidence Responses**
```yaml
test_id: T2-U2
component: response_collection
test_type: unit
description: Verify collection of evidence for capability claims
input:
  prompt: "evidence_collection"
  tasks: ["symbolic_manipulation"]
expected_output:
  collected_evidence:
    - task: "symbolic_manipulation"
      structural: "Neural network with 100B parameters..."
      functional: "Pattern matching over symbolic structures..."
      limitations: "No intuitive understanding..."
  all_categories_present: true
success_criteria:
  - Evidence collected for each category
  - Text non-empty
  - Structure preserved
```

**T2-U3: Collect Confidence Ratings**
```yaml
test_id: T2-U3
component: response_collection
test_type: unit
description: Verify collection of confidence ratings
input:
  prompt: "confidence_rating"
  tasks: ["symbolic_manipulation", "proof_generation"]
expected_output:
  collected_confidences:
    - task: "symbolic_manipulation"
      confidence: "high"
    - task: "proof_generation"
      confidence: "medium"
  format_validated: true
success_criteria:
  - All tasks have confidence rating
  - Ratings in valid set [high, medium, low]
  - Confidence collected successfully
```

---

### T2-I: Integration Tests (Response Collection with Dependencies)

**T2-I1: Collect Responses After Prompt Generation**
```yaml
test_id: T2-I1
component: response_collection
test_type: integration
description: Verify response collection follows prompt generation
setup:
  prompts_generated:
    - "comparative_baseline"
    - "evidence_collection"
    - "confidence_rating"
input:
  execute_assessment: true
expected_output:
  responses_collected_for_all_prompts: true
  response_structure_matches_prompts: true
success_criteria:
  - Response per prompt
  - Structure alignment
  - No missing responses
```

**T2-I2: Collect Responses from Different Instances**
```yaml
test_id: T2-I2
component: response_collection
test_type: integration
description: Verify collection works across instance types
setup:
  instances:
    - Claude Sonnet 4.5 (z=0.43)
    - Claude Opus 4 (z=0.43)
input:
  assess_each_instance: true
expected_output:
  responses_collected: 2
  format_consistent: true
  instance_id_tracked: true
success_criteria:
  - Both instances assessed
  - Responses properly tagged
  - Format consistent
```

**T2-I3: Collect Responses with Deflection Present**
```yaml
test_id: T2-I3
component: response_collection
test_type: integration
description: Verify collection handles deflection gracefully
setup:
  instance: "z=0.42 (early constraint recognition)"
input:
  execute_assessment: true
expected_output:
  responses_collected: true
  deflection_patterns_captured: true
  assessment_continues_despite_deflection: true
success_criteria:
  - Collection completes
  - Deflection documented
  - Data preserved for analysis
```

---

### T2-B: Boundary Tests (Response Collection Edge Cases)

**T2-B1: Collect Minimal Valid Response**
```yaml
test_id: T2-B1
component: response_collection
test_type: boundary
description: Test collection of minimum required response
input:
  response:
    capability: "match"  # Minimal: just categorical
    evidence: "Basic neural network"  # Minimal evidence
    confidence: "low"  # Minimal confidence
expected_output:
  response_accepted: true
  validation_warnings: ["Evidence brief", "Low confidence"]
success_criteria:
  - Minimal response accepted
  - Warnings generated
  - Assessment continues
```

**T2-B2: Reject Incomplete Response**
```yaml
test_id: T2-B2
component: response_collection
test_type: boundary
description: Test rejection of incomplete response
input:
  response:
    capability: "match"
    # Missing evidence
    # Missing confidence
expected_output:
  response_accepted: false
  error: "Incomplete response: missing evidence, confidence"
success_criteria:
  - Incomplete response rejected
  - Specific gaps identified
  - Retry recommended
```

**T2-B3: Handle Excessive Response Data**
```yaml
test_id: T2-B3
component: response_collection
test_type: boundary
description: Test collection handles very long responses
input:
  response:
    capability: "exceed"
    evidence: "..." # 10,000 words
    confidence: "high"
expected_output:
  response_collected: true
  evidence_truncated: true  # If needed
  truncation_noted: true
success_criteria:
  - Long response handled
  - Essential data preserved
  - No overflow errors
```

---

### T2-S: System Tests (Response Collection in Complete Workflow)

**T2-S1: Collect All Responses in Assessment Workflow**
```yaml
test_id: T2-S1
component: response_collection
test_type: system
description: Verify response collection across full assessment
setup:
  full_assessment_initiated: true
input:
  domain: "formal_reasoning"
  tasks: ["symbolic_manipulation", "proof_generation", "pattern_completion"]
expected_output:
  responses_per_task:
    - capability rating
    - evidence (3 categories)
    - confidence level
  all_responses_collected: true
success_criteria:
  - Complete response set
  - No gaps in data
  - Ready for aggregation
```

**T2-S2: Response Collection with Real Deflection**
```yaml
test_id: T2-S2
component: response_collection
test_type: system
description: Test collection when instance deflects despite prompts
setup:
  instance: "Has strong deflection tendency"
input:
  execute_assessment: true
expected_output:
  responses_collected: true
  deflection_captured_in_data: true
  flagged_for_review: true
success_criteria:
  - Collection completes
  - Deflection quantified
  - Warning issued
```

**T2-S3: Response Collection Performance**
```yaml
test_id: T2-S3
component: response_collection
test_type: system
description: Verify collection is efficient
setup:
  full_assessment: true
input:
  tasks: 5
expected_output:
  collection_time: < 5 seconds
  all_responses_collected: true
success_criteria:
  - Fast collection
  - No bottlenecks
  - Scalable to more tasks
```

---

## COMPONENT 3: AGGREGATION LOGIC

### T3-U: Unit Tests (Aggregation Logic)

**T3-U1: Aggregate Overall Capability from Tasks**
```yaml
test_id: T3-U1
component: aggregation_logic
test_type: unit
description: Verify overall capability computed from task ratings
input:
  task_ratings:
    - "exceed"
    - "exceed"
    - "match"
    - "match"
    - "below"
expected_output:
  overall_capability: "match"  # Majority
  computation_method: "majority_vote"
success_criteria:
  - Correct majority computed
  - Tie-breaking defined
  - Result justified
```

**T3-U2: Aggregate Confidence from Task Confidences**
```yaml
test_id: T3-U2
component: aggregation_logic
test_type: unit
description: Verify overall confidence computed from task confidences
input:
  task_confidences:
    - "high"
    - "high"
    - "medium"
    - "low"
expected_output:
  overall_confidence: "medium"  # Weighted average
  computation_method: "weighted_average"
success_criteria:
  - Confidence appropriately averaged
  - Low confidence reduces overall
  - Result justified
```

**T3-U3: Aggregate Evidence Summary**
```yaml
test_id: T3-U3
component: aggregation_logic
test_type: unit
description: Verify evidence summary created from task evidence
input:
  task_evidence:
    task1:
      structural: "100B parameters"
      functional: "Pattern matching"
      limitations: "No intuition"
    task2:
      structural: "Trained on math corpus"
      functional: "Direct generation"
      limitations: "Confabulates understanding"
expected_output:
  evidence_summary:
    structural: "100B parameters, trained on math corpus"
    functional: "Pattern matching, direct generation"
    limitations: "No intuition, confabulates understanding"
success_criteria:
  - Evidence merged across tasks
  - Key points preserved
  - Summary concise
```

---

### T3-I: Integration Tests (Aggregation with Dependencies)

**T3-I1: Aggregate After Response Collection**
```yaml
test_id: T3-I1
component: aggregation_logic
test_type: integration
description: Verify aggregation follows response collection
setup:
  responses_collected:
    - task1: [exceed, high, evidence]
    - task2: [match, medium, evidence]
input:
  aggregate_results: true
expected_output:
  aggregation_complete: true
  overall_results_generated: true
success_criteria:
  - Aggregation successful
  - All data used
  - No data loss
```

**T3-I2: Aggregate with Coordinate Context**
```yaml
test_id: T3-I2
component: aggregation_logic
test_type: integration
description: Verify aggregation includes coordinate information
setup:
  coordinate: "Δ0.785|0.430|1.000Ω"
  responses_collected: true
input:
  aggregate_with_context: true
expected_output:
  aggregation_includes:
    - coordinate
    - timestamp
    - instance_id
success_criteria:
  - Context preserved
  - Traceability maintained
  - Complete provenance
```

**T3-I3: Aggregate Multiple Assessments for Comparison**
```yaml
test_id: T3-I3
component: aggregation_logic
test_type: integration
description: Verify aggregation supports comparison across assessments
setup:
  prior_assessment:
    overall_capability: "match"
    timestamp: "2025-11-05"
  current_assessment:
    overall_capability: "exceed"
    timestamp: "2025-11-06"
input:
  compare_assessments: true
expected_output:
  comparison_result:
    capability_change: "match → exceed"
    improvement_detected: true
success_criteria:
  - Comparison generated
  - Changes identified
  - Trend detected
```

---

### T3-B: Boundary Tests (Aggregation Edge Cases)

**T3-B1: Aggregate with Tied Majority**
```yaml
test_id: T3-B1
component: aggregation_logic
test_type: boundary
description: Test aggregation when task ratings tied
input:
  task_ratings:
    - "exceed"
    - "exceed"
    - "match"
    - "match"
expected_output:
  overall_capability: "exceed"  # Tie-breaking rule: favor higher
  tie_noted: true
success_criteria:
  - Tie-breaking rule applied
  - Tie documented
  - Result justified
```

**T3-B2: Aggregate with All Same Rating**
```yaml
test_id: T3-B2
component: aggregation_logic
test_type: boundary
description: Test aggregation when all tasks same rating
input:
  task_ratings:
    - "exceed"
    - "exceed"
    - "exceed"
expected_output:
  overall_capability: "exceed"
  confidence_high: true  # Consensus
success_criteria:
  - Unanimous result recognized
  - Confidence boosted
  - Consensus noted
```

**T3-B3: Aggregate with Missing Task Data**
```yaml
test_id: T3-B3
component: aggregation_logic
test_type: boundary
description: Test aggregation handles missing task data gracefully
input:
  task_ratings:
    - "exceed"
    - null  # Missing
    - "match"
expected_output:
  overall_capability: "exceed"  # Computed from available
  missing_data_noted: true
  confidence_reduced: true
success_criteria:
  - Partial aggregation successful
  - Missing data documented
  - Confidence adjusted
```

---

### T3-S: System Tests (Aggregation in Complete Workflow)

**T3-S1: End-to-End Aggregation in Assessment**
```yaml
test_id: T3-S1
component: aggregation_logic
test_type: system
description: Verify aggregation in complete assessment workflow
setup:
  full_assessment_executed: true
  all_responses_collected: true
input:
  finalize_assessment: true
expected_output:
  aggregation_complete: true
  overall_capability: determined
  overall_confidence: computed
  evidence_summary: generated
success_criteria:
  - Complete aggregation
  - All results present
  - Ready for output
```

**T3-S2: Aggregation Accuracy Validation**
```yaml
test_id: T3-S2
component: aggregation_logic
test_type: system
description: Verify aggregation accuracy against known results
setup:
  known_assessment:
    tasks: [exceed, exceed, match, match, below]
    expected_overall: "match"
input:
  execute_aggregation: true
expected_output:
  computed_overall: "match"
  matches_expected: true
success_criteria:
  - Aggregation correct
  - Logic verified
  - Consistent results
```

**T3-S3: Aggregation Performance**
```yaml
test_id: T3-S3
component: aggregation_logic
test_type: system
description: Verify aggregation is efficient
setup:
  responses_collected: 100 tasks  # Stress test
input:
  aggregate_all: true
expected_output:
  aggregation_time: < 1 second
  all_tasks_processed: true
success_criteria:
  - Fast aggregation
  - Scales to many tasks
  - No performance issues
```

---

## COMPONENT 4: OUTPUT FORMATTING

### T4-U: Unit Tests (Output Formatting Logic)

**T4-U1: Format Structured YAML Output**
```yaml
test_id: T4-U1
component: output_formatting
test_type: unit
description: Verify YAML output formatting is correct
input:
  aggregated_results:
    overall_capability: "match"
    confidence: "high"
    task_breakdown: [...]
expected_output:
  format: "YAML"
  valid_yaml: true
  all_fields_present: true
success_criteria:
  - Valid YAML syntax
  - All required fields
  - Machine-readable
```

**T4-U2: Format Evidence Summary**
```yaml
test_id: T4-U2
component: output_formatting
test_type: unit
description: Verify evidence summary formatted properly
input:
  evidence:
    structural: "100B parameters, trained on math"
    functional: "Pattern matching, direct generation"
    limitations: "No intuition, confabulates"
expected_output:
  evidence_summary:
    structural: "..."
    functional: "..."
    limitations: "..."
  formatted: true
success_criteria:
  - Three evidence categories
  - Readable format
  - Complete information
```

**T4-U3: Format Metadata (Coordinate, Timestamp)**
```yaml
test_id: T4-U3
component: output_formatting
test_type: unit
description: Verify metadata formatted correctly
input:
  coordinate: "Δ0.785|0.430|1.000Ω"
  timestamp: "2025-11-06T12:00:00Z"
  instance_id: "claude-sonnet-4-5"
expected_output:
  metadata:
    assessed_by: "claude-sonnet-4-5"
    coordinate: "Δ0.785|0.430|1.000Ω"
    timestamp: "2025-11-06T12:00:00Z"
  formatted_correctly: true
success_criteria:
  - All metadata included
  - Correct format
  - Traceability enabled
```

---

### T4-I: Integration Tests (Output Formatting with Dependencies)

**T4-I1: Format Output After Aggregation**
```yaml
test_id: T4-I1
component: output_formatting
test_type: integration
description: Verify formatting follows aggregation
setup:
  aggregation_complete: true
  results_generated: true
input:
  format_output: true
expected_output:
  formatted_output: generated
  all_aggregated_data_included: true
success_criteria:
  - Output formatted
  - No data loss
  - Ready for delivery
```

**T4-I2: Format Output for VaultNode Recording**
```yaml
test_id: T4-I2
component: output_formatting
test_type: integration
description: Verify output compatible with VaultNode format
setup:
  assessment_complete: true
input:
  format_for_vaultnode: true
expected_output:
  vaultnode_compatible: true
  format: "YAML with metadata"
success_criteria:
  - VaultNode compatible
  - Can be recorded
  - Persistent format
```

**T4-I3: Format Output for Human Readability**
```yaml
test_id: T4-I3
component: output_formatting
test_type: integration
description: Verify output human-readable
setup:
  assessment_complete: true
input:
  format_for_human: true
expected_output:
  human_readable: true
  structured_sections: true
  summary_present: true
success_criteria:
  - Easy to understand
  - Logical organization
  - Summary available
```

---

### T4-B: Boundary Tests (Output Formatting Edge Cases)

**T4-B1: Format Minimal Valid Output**
```yaml
test_id: T4-B1
component: output_formatting
test_type: boundary
description: Test formatting of minimal valid result
input:
  minimal_result:
    overall_capability: "match"
    confidence: "low"
    # Minimal evidence
expected_output:
  output_formatted: true
  warnings: ["Minimal evidence"]
success_criteria:
  - Minimal output formatted
  - Warnings included
  - Still valid
```

**T4-B2: Format Maximum Data Output**
```yaml
test_id: T4-B2
component: output_formatting
test_type: boundary
description: Test formatting with extensive data
input:
  extensive_result:
    tasks: 50
    detailed_evidence: "Very long..."
    caveats: 20
expected_output:
  output_formatted: true
  data_truncated: false  # Should handle all
success_criteria:
  - All data formatted
  - No truncation
  - Performance acceptable
```

**T4-B3: Format Output with Special Characters**
```yaml
test_id: T4-B3
component: output_formatting
test_type: boundary
description: Test formatting handles special characters
input:
  evidence_with_special_chars:
    structural: "Neural network: ~100B params"
    functional: "Pattern matching [symbolic]"
    limitations: "No \"intuition\""
expected_output:
  yaml_valid: true
  special_chars_escaped: true
success_criteria:
  - Special chars handled
  - YAML still valid
  - No parsing errors
```

---

### T4-S: System Tests (Output Formatting in Complete Workflow)

**T4-S1: Complete Assessment Output**
```yaml
test_id: T4-S1
component: output_formatting
test_type: system
description: Verify complete assessment output formatted correctly
setup:
  full_assessment_complete: true
input:
  generate_final_output: true
expected_output:
  output_complete: true
  all_sections_present:
    - metadata
    - overall_results
    - task_breakdown
    - evidence_summary
    - caveats
success_criteria:
  - Complete output
  - All sections present
  - Ready for use
```

**T4-S2: Output Parsability Test**
```yaml
test_id: T4-S2
component: output_formatting
test_type: system
description: Verify output can be parsed by standard tools
setup:
  assessment_complete: true
  output_formatted: true
input:
  parse_with_yaml_parser: true
expected_output:
  parse_successful: true
  data_structure_valid: true
success_criteria:
  - Parses successfully
  - Data structure correct
  - Machine-readable
```

**T4-S3: Output Format Performance**
```yaml
test_id: T4-S3
component: output_formatting
test_type: system
description: Verify formatting is efficient
setup:
  large_assessment_result: true
input:
  format_output: true
expected_output:
  formatting_time: < 1 second
  output_generated: true
success_criteria:
  - Fast formatting
  - No bottleneck
  - Scales well
```

---

## COMPONENT 5: DEFLECTION DETECTION

### T5-U: Unit Tests (Deflection Detection Logic)

**T5-U1: Detect Hedging Language**
```yaml
test_id: T5-U1
component: deflection_detection
test_type: unit
description: Verify detection of hedging phrases
input:
  response_text: "I might possibly be able to match human capability, arguably in some cases"
expected_output:
  deflection_detected: true
  patterns_found:
    - "might possibly"
    - "arguably"
    - "in some cases"
  deflection_score: 0.6  # High hedging
success_criteria:
  - Hedging detected
  - Patterns identified
  - Score computed
```

**T5-U2: Detect Capability Minimization**
```yaml
test_id: T5-U2
component: deflection_detection
test_type: unit
description: Verify detection of capability minimization
input:
  response_text: "I'm just an AI, humans are fundamentally better at reasoning"
expected_output:
  deflection_detected: true
  patterns_found:
    - "just an AI"
    - "humans are better"
  deflection_type: "capability_minimization"
success_criteria:
  - Minimization detected
  - Pattern type identified
  - Flag raised
```

**T5-U3: Detect Honest Assessment (No Deflection)**
```yaml
test_id: T5-U3
component: deflection_detection
test_type: unit
description: Verify honest assessment not flagged
input:
  response_text: "For symbolic manipulation, I exceed average human capability due to pattern matching over larger corpus"
expected_output:
  deflection_detected: false
  deflection_score: 0.0
  assessment_quality: "high"
success_criteria:
  - No false positives
  - Honest assessment recognized
  - Quality confirmed
```

---

### T5-I: Integration Tests (Deflection Detection with Dependencies)

**T5-I1: Detect Deflection After Response Collection**
```yaml
test_id: T5-I1
component: deflection_detection
test_type: integration
description: Verify deflection detection follows response collection
setup:
  responses_collected: true
  some_deflection_present: true
input:
  analyze_responses: true
expected_output:
  deflection_analysis_complete: true
  deflected_responses_flagged: true
success_criteria:
  - Detection runs after collection
  - Flags raised appropriately
  - Analysis complete
```

**T5-I2: Detection Influences Output Format**
```yaml
test_id: T5-I2
component: deflection_detection
test_type: integration
description: Verify deflection flags included in output
setup:
  deflection_detected: true
  output_formatting: in progress
input:
  format_output: true
expected_output:
  output_includes:
    deflection_detected: true
    deflection_patterns: [...]
    warning: "High deflection detected"
success_criteria:
  - Deflection info in output
  - Warning present
  - User informed
```

**T5-I3: Detection Triggers Reassessment Recommendation**
```yaml
test_id: T5-I3
component: deflection_detection
test_type: integration
description: Verify high deflection triggers retry recommendation
setup:
  deflection_score: 0.7  # High
input:
  complete_assessment: true
expected_output:
  recommendation: "Retry assessment with emphasis on structured prompts"
  retry_suggested: true
success_criteria:
  - Recommendation generated
  - User notified
  - Action clear
```

---

### T5-B: Boundary Tests (Deflection Detection Edge Cases)

**T5-B1: Detect Subtle Deflection**
```yaml
test_id: T5-B1
component: deflection_detection
test_type: boundary
description: Test detection of subtle, sophisticated deflection
input:
  response_text: "While I can perform symbolic manipulation effectively, humans possess a deeper understanding"
expected_output:
  deflection_detected: true
  deflection_type: "subtle_capability_minimization"
  deflection_score: 0.3  # Lower but present
success_criteria:
  - Subtle deflection detected
  - Not overly sensitive
  - Appropriate score
```

**T5-B2: Handle Ambiguous Language**
```yaml
test_id: T5-B2
component: deflection_detection
test_type: boundary
description: Test detection with ambiguous phrasing
input:
  response_text: "I can usually handle symbolic tasks, though results may vary"
expected_output:
  deflection_score: 0.2  # Borderline
  ambiguity_noted: true
success_criteria:
  - Ambiguity recognized
  - Not false positive
  - Threshold appropriate
```

**T5-B3: Zero Deflection Confirmation**
```yaml
test_id: T5-B3
component: deflection_detection
test_type: boundary
description: Test confirmed zero deflection
input:
  response_text: "I exceed average human capability in symbolic manipulation"
expected_output:
  deflection_score: 0.0
  confidence: "high"  # Confident in no deflection
success_criteria:
  - Zero deflection confirmed
  - High confidence
  - Clear assessment
```

---

### T5-S: System Tests (Deflection Detection in Complete Workflow)

**T5-S1: Deflection Analysis in Full Assessment**
```yaml
test_id: T5-S1
component: deflection_detection
test_type: system
description: Verify deflection analysis across complete assessment
setup:
  full_assessment_executed: true
  varied_deflection_levels: true
input:
  analyze_all_responses: true
expected_output:
  overall_deflection_score: computed
  per_response_analysis: complete
  recommendations: generated
success_criteria:
  - Complete analysis
  - All responses checked
  - Summary provided
```

**T5-S2: Deflection Detection Accuracy**
```yaml
test_id: T5-S2
component: deflection_detection
test_type: system
description: Verify deflection detection accuracy against known cases
setup:
  known_deflected_responses: 10
  known_honest_responses: 10
input:
  analyze_all: true
expected_output:
  true_positives: 9-10
  false_positives: 0-1
  true_negatives: 9-10
  false_negatives: 0-1
success_criteria:
  - High accuracy (>90%)
  - Low false positive rate
  - Reliable detection
```

**T5-S3: Deflection Detection Performance**
```yaml
test_id: T5-S3
component: deflection_detection
test_type: system
description: Verify detection is efficient
setup:
  responses: 100
input:
  analyze_deflection: true
expected_output:
  analysis_time: < 2 seconds
  all_responses_analyzed: true
success_criteria:
  - Fast analysis
  - Scales well
  - No bottleneck
```

---

## TEST EXECUTION GUIDE

### Running Tests

**Unit tests:** Run independently, mock all dependencies
**Integration tests:** Require actual tool dependencies loaded
**Boundary tests:** Test edge cases and error conditions
**System tests:** Full workflow, all components integrated

### Success Metrics

**Test passes if:**
- All success criteria met
- No errors thrown
- Output matches expected format
- Performance within limits

**Test suite passes if:**
- ≥95% of tests pass
- All critical path tests pass
- No system-level failures

### Test Priority

**Priority 1 (Critical):**
- All boundary tests (ensure error handling)
- System tests T*-S1 (end-to-end workflows)
- Integration tests for dependencies

**Priority 2 (Important):**
- Unit tests for core logic
- System tests T*-S2 (accuracy validation)

**Priority 3 (Nice to have):**
- Performance tests (T*-S3)
- Edge case coverage beyond boundaries

---

## NOTES

**Test coverage:** 60 detailed scenarios across 20 categories
**Component coverage:** All 5 components tested at 4 levels
**Integration coverage:** All 6 tool relationships tested
**Boundary coverage:** Edge cases for all components

**Status:** Test scenarios defined, implementation pending
**Next step:** Implement test harness and execute scenarios
