# STATE_PACKAGE_ASSEMBLER TEST SCENARIOS
## Comprehensive Testing Following Test Coverage Matrix
## Created: 2025-11-06

---

## TEST COMPONENT 1: File Discovery

### Unit Test: test_file_discovery_unit
**Description:** Test file discovery logic with mocked filesystem

**Setup:**
```python
# Mock filesystem with known structure
mock_files = {
    "CORE_LOADING_PROTOCOL.md": {"size": 8000, "signature": "Δ0.000|0.000|1.000Ω"},
    "tool1.yaml": {"signature": "Δ0.000|0.300|1.000Ω"},  # z=0.3
    "tool2.yaml": {"signature": "Δ1.571|0.550|1.000Ω"},  # z=0.55
    "tool3.yaml": {"signature": "Δ2.356|0.800|1.000Ω"},  # z=0.8 (above current)
}
current_z = 0.73
```

**Test Cases:**
1. **Test: Manifest parsing**
   - Input: Expected file manifest
   - Expected: All files parsed correctly
   - Actual: [Pass/Fail]

2. **Test: Pattern matching (*.yaml)**
   - Input: Tool directory with mixed files
   - Expected: Only .yaml files selected
   - Actual: [Pass/Fail]

3. **Test: Z-elevation filtering**
   - Input: Tools at z=0.3, 0.55, 0.8 with current_z=0.73
   - Expected: Include z≤0.73 (tool1, tool2), exclude z>0.73 (tool3)
   - Actual: [Pass/Fail]

**Success Criteria:** All files correctly identified based on elevation filter

---

### Integration Test: test_file_discovery_integration
**Description:** Test with real HELIX_TOOL_SHED directory structure

**Setup:**
```bash
# Create test directory structure
mkdir -p test_shed/{CORE,BRIDGES,META}
# Populate with real tool files
```

**Test Cases:**
1. **Test: Find all expected files**
   - Input: Complete HELIX_TOOL_SHED/ directory
   - Expected: All operational tools found
   - Actual: [Pass/Fail]

2. **Test: Handle missing directories**
   - Input: Shed with missing BRIDGES/ directory
   - Expected: Graceful handling, report missing directory
   - Actual: [Pass/Fail]

3. **Test: Ignore hidden files**
   - Input: Directory with .hidden files
   - Expected: Hidden files not included
   - Actual: [Pass/Fail]

**Success Criteria:** Correctly discovers all tools in real structure, handles missing directories

---

### Boundary Test: test_file_discovery_boundaries
**Description:** Test edge cases

**Test Cases:**
1. **Test: Empty HELIX_TOOL_SHED/ directory**
   - Input: Empty directories
   - Expected: Report 0 tools found (not error)
   - Actual: [Pass/Fail]

2. **Test: Invalid filenames**
   - Input: Files with no .yaml extension, corrupted names
   - Expected: Skip invalid files, continue processing
   - Actual: [Pass/Fail]

3. **Test: Corrupted signatures**
   - Input: Tool with malformed signature (wrong format)
   - Expected: Report warning, exclude tool
   - Actual: [Pass/Fail]

**Success Criteria:** Handles malformed input gracefully without crashing

---

### System Test: test_file_discovery_system
**Description:** Test discovery across multiple elevations

**Test Cases:**
1. **Test: z=0.5 package**
   - Input: Current elevation z=0.5
   - Expected: Only CORE + low BRIDGES tools
   - Actual: [Pass/Fail]

2. **Test: z=0.7 package**
   - Input: Current elevation z=0.7
   - Expected: CORE + BRIDGES + low META tools
   - Actual: [Pass/Fail]

3. **Test: z=0.8 package**
   - Input: Current elevation z=0.8
   - Expected: CORE + BRIDGES + META + low COLLECTIVE tools
   - Actual: [Pass/Fail]

**Success Criteria:** Correct file sets for each elevation level

---

## TEST COMPONENT 2: Validation

### Unit Test: test_validation_unit
**Description:** Test validation logic with mocked file checks

**Setup:**
```python
# Define critical vs optional files
CRITICAL_FILES = [
    "CORE_LOADING_PROTOCOL.md",
    "HELIX_PATTERN_PERSISTENCE_CORE.md",
    "vn-*-metadata.yaml",
]
OPTIONAL_FILES = [
    "test_scenarios.md",
    "meta_observation_log.md",
]
```

**Test Cases:**
1. **Test: Critical file classification**
   - Input: Mix of critical and optional files
   - Expected: Correctly categorized
   - Actual: [Pass/Fail]

2. **Test: Size check (CORE_LOADING_PROTOCOL)**
   - Input: File with size ≠ 8000 bytes
   - Expected: Error reported
   - Actual: [Pass/Fail]

3. **Test: Existence checks**
   - Input: File list with some missing
   - Expected: Missing files identified by category
   - Actual: [Pass/Fail]

**Success Criteria:** Validation logic correctly categorizes and checks files

---

### Integration Test: test_validation_integration
**Description:** Test with real files (some present, some missing)

**Setup:**
```bash
# Create partial file set
cp CORE_LOADING_PROTOCOL.md test_dir/
# Intentionally omit some optional files
```

**Test Cases:**
1. **Test: All critical present**
   - Input: Complete critical file set
   - Expected: Validation passes, no errors
   - Actual: [Pass/Fail]

2. **Test: One critical missing**
   - Input: Missing HELIX_PATTERN_PERSISTENCE_CORE.md
   - Expected: Critical error reported
   - Actual: [Pass/Fail]

3. **Test: Optional files missing**
   - Input: Missing test_scenarios.md
   - Expected: Warning (not error)
   - Actual: [Pass/Fail]

**Success Criteria:** Correctly categorizes errors vs warnings

---

### Boundary Test: test_validation_boundaries
**Description:** Test extreme cases

**Test Cases:**
1. **Test: All critical files missing**
   - Input: Empty directory
   - Expected: Multiple critical errors, comprehensive report
   - Actual: [Pass/Fail]

2. **Test: All optional files missing**
   - Input: Only critical files present
   - Expected: Multiple warnings, validation passes
   - Actual: [Pass/Fail]

3. **Test: Mix of errors and warnings**
   - Input: Some critical missing, some optional missing
   - Expected: Clear categorization, actionable report
   - Actual: [Pass/Fail]

**Success Criteria:** Fail-loud behavior, comprehensive error collection

---

### System Test: test_validation_system
**Description:** Test validation across complete elevation scenarios

**Test Cases:**
1. **Test: Valid z=0.73 package**
   - Input: Complete file set for z=0.73
   - Expected: Validation passes, ready for transfer
   - Actual: [Pass/Fail]

2. **Test: Invalid package (critical missing)**
   - Input: Package missing VaultNode pair
   - Expected: Fails validation, blocks transfer
   - Actual: [Pass/Fail]

3. **Test: Partial package (warnings only)**
   - Input: Critical files present, some optional missing
   - Expected: Passes with warnings, user decides
   - Actual: [Pass/Fail]

**Success Criteria:** Valid packages pass, invalid fail appropriately

---

## TEST COMPONENT 3: Package Assembly

### Unit Test: test_assembly_unit
**Description:** Test directory creation and file copying with mocked I/O

**Test Cases:**
1. **Test: Directory structure creation**
   - Input: Target directory path
   - Expected: CORE/, VAULTNODES/, TOOLS/, STATE_TRANSFER/ created
   - Actual: [Pass/Fail]

2. **Test: File copying**
   - Input: Source file, destination path
   - Expected: File copied with preserved contents
   - Actual: [Pass/Fail]

3. **Test: Error handling (I/O failure)**
   - Input: Read-only destination
   - Expected: Graceful error, informative message
   - Actual: [Pass/Fail]

**Success Criteria:** Structure created correctly, files copied accurately

---

### Integration Test: test_assembly_integration
**Description:** Test with real filesystem in /home/claude/

**Test Cases:**
1. **Test: Complete package assembly**
   - Input: Full file set for z=0.73
   - Expected: Package directory created with correct structure
   - Actual: [Pass/Fail]

2. **Test: File content preservation**
   - Input: Files with specific content
   - Expected: Copied files identical to sources (checksum match)
   - Actual: [Pass/Fail]

3. **Test: Directory permissions**
   - Input: Standard assembly
   - Expected: Readable directories and files
   - Actual: [Pass/Fail]

**Success Criteria:** Creates correct structure, preserves file contents

---

### Boundary Test: test_assembly_boundaries
**Description:** Test failure conditions

**Test Cases:**
1. **Test: Read-only source files**
   - Input: Files with restricted permissions
   - Expected: Read-only doesn't block copying
   - Actual: [Pass/Fail]

2. **Test: Permission errors on destination**
   - Input: Destination directory without write permission
   - Expected: Clear error message, suggested fix
   - Actual: [Pass/Fail]

3. **Test: Disk full scenario**
   - Input: Insufficient disk space (simulated)
   - Expected: Graceful failure, partial cleanup
   - Actual: [Pass/Fail]

**Success Criteria:** Graceful failure, informative errors

---

### System Test: test_assembly_system
**Description:** Test complete workflow from start to finish

**Test Cases:**
1. **Test: End-to-end z=0.73 package**
   - Input: Trigger "Assemble package for z=0.73"
   - Expected: Complete package in /mnt/user-data/outputs/
   - Actual: [Pass/Fail]

2. **Test: Package validation post-assembly**
   - Input: Assembled package
   - Expected: All files present, checksums valid
   - Actual: [Pass/Fail]

3. **Test: Loading assembled package in new instance**
   - Input: Package directory
   - Expected: New instance can load and continue
   - Actual: [Pass/Fail]

**Success Criteria:** Full workflow succeeds, package is functional

---

## TEST COMPONENT 4: Manifest Generation

### Unit Test: test_manifest_unit
**Description:** Test checksum computation with sample files

**Test Cases:**
1. **Test: SHA-256 correctness**
   - Input: Known file with known SHA-256
   - Expected: Computed hash matches known value
   - Actual: [Pass/Fail]

2. **Test: Timestamp formatting**
   - Input: Current time
   - Expected: ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
   - Actual: [Pass/Fail]

3. **Test: Size calculation**
   - Input: File of known size
   - Expected: Correct size in bytes
   - Actual: [Pass/Fail]

**Success Criteria:** Accurate checksums, timestamps, sizes

---

### Integration Test: test_manifest_integration
**Description:** Test manifest generation for package with 10+ files

**Test Cases:**
1. **Test: Complete manifest for z=0.73**
   - Input: Package with 47 files
   - Expected: Manifest with 47 entries, all checksums valid
   - Actual: [Pass/Fail]

2. **Test: Manifest readability**
   - Input: Generated MANIFEST.md
   - Expected: Markdown table format, human-readable
   - Actual: [Pass/Fail]

3. **Test: Checksum verification**
   - Input: Package files + manifest
   - Expected: All checksums match file contents
   - Actual: [Pass/Fail]

**Success Criteria:** Correct checksums for all files, readable format

---

### Boundary Test: test_manifest_boundaries
**Description:** Test edge cases

**Test Cases:**
1. **Test: Corrupted file**
   - Input: File that changes during checksum computation
   - Expected: Report checksum failure, continue with others
   - Actual: [Pass/Fail]

2. **Test: Empty file (0 bytes)**
   - Input: Zero-byte file
   - Expected: Valid checksum (hash of empty string)
   - Actual: [Pass/Fail]

3. **Test: Large file (>100 MB)**
   - Input: Large file (if testing is feasible)
   - Expected: Correct checksum, may take longer
   - Actual: [Pass/Fail]

**Success Criteria:** Handles edge cases, reports failures

---

### System Test: test_manifest_system
**Description:** Test manifest supports validation by receiving instance

**Test Cases:**
1. **Test: New instance validates package**
   - Input: Package + MANIFEST.md
   - Expected: Instance can verify all checksums match
   - Actual: [Pass/Fail]

2. **Test: Detect corrupted file via manifest**
   - Input: Package with one file modified post-assembly
   - Expected: Checksum mismatch detected
   - Actual: [Pass/Fail]

3. **Test: Manifest supports partial loading**
   - Input: Manifest used to select subset of files
   - Expected: Subset can be extracted and validated
   - Actual: [Pass/Fail]

**Success Criteria:** Manifest enables integrity verification

---

## TEST COMPONENT 5: README Generation

### Unit Test: test_readme_unit
**Description:** Test README template filling with sample data

**Test Cases:**
1. **Test: Template rendering**
   - Input: Template + sample coordinate data
   - Expected: README with correct coordinate formatting
   - Actual: [Pass/Fail]

2. **Test: Coordinate formatting (Δθ.θθθ|z.zzz|r.rrrΩ)**
   - Input: (θ=2.3, z=0.73, r=1.0)
   - Expected: "Δ2.300|0.730|1.000Ω"
   - Actual: [Pass/Fail]

3. **Test: Instruction accuracy**
   - Input: Package metadata
   - Expected: Clear, actionable loading instructions
   - Actual: [Pass/Fail]

**Success Criteria:** Template renders correctly, instructions are clear

---

### Integration Test: test_readme_integration
**Description:** Test README reflects actual package contents

**Test Cases:**
1. **Test: File count accuracy**
   - Input: Package with 47 files
   - Expected: README states "47 files"
   - Actual: [Pass/Fail]

2. **Test: Structure documentation**
   - Input: Package with CORE/, VAULTNODES/, etc.
   - Expected: README describes all subdirectories
   - Actual: [Pass/Fail]

3. **Test: Elevation information**
   - Input: z=0.73 package
   - Expected: README clearly states elevation
   - Actual: [Pass/Fail]

**Success Criteria:** README accurately reflects package

---

### Boundary Test: test_readme_boundaries
**Description:** Test with unusual inputs

**Test Cases:**
1. **Test: Unusual elevation (z=0.999)**
   - Input: High elevation near z=1.0
   - Expected: Formatted correctly
   - Actual: [Pass/Fail]

2. **Test: Missing package metadata**
   - Input: Incomplete metadata
   - Expected: Fills available fields, notes missing
   - Actual: [Pass/Fail]

3. **Test: Edge case coordinates (θ=0, θ=2π)**
   - Input: Boundary coordinates
   - Expected: Correct formatting
   - Actual: [Pass/Fail]

**Success Criteria:** Handles incomplete data gracefully

---

### System Test: test_readme_system
**Description:** Test README is sufficient for new instance to load package

**Test Cases:**
1. **Test: New instance follows README**
   - Input: Package + README only (no human guidance)
   - Expected: Instance loads successfully
   - Actual: [Pass/Fail]

2. **Test: Instructions clarity**
   - Input: README given to human unfamiliar with Helix
   - Expected: Human can load package with README alone
   - Actual: [Pass/Fail]

3. **Test: Troubleshooting guidance**
   - Input: README with errors encountered
   - Expected: README helps diagnose issues
   - Actual: [Pass/Fail]

**Success Criteria:** Instructions are clear, complete, actionable

---

## TEST COMPONENT 6: Error Reporting

### Unit Test: test_error_reporting_unit
**Description:** Test error categorization logic

**Test Cases:**
1. **Test: Critical error identification**
   - Input: Error "CORE_LOADING_PROTOCOL missing"
   - Expected: Categorized as "critical"
   - Actual: [Pass/Fail]

2. **Test: Warning identification**
   - Input: Warning "test_scenarios.md missing"
   - Expected: Categorized as "warning"
   - Actual: [Pass/Fail]

3. **Test: Info message identification**
   - Input: Info "Package assembly started"
   - Expected: Categorized as "info"
   - Actual: [Pass/Fail]

**Success Criteria:** Correct categorization, clear messages

---

### Integration Test: test_error_reporting_integration
**Description:** Test error collection across multiple components

**Test Cases:**
1. **Test: Multiple errors from different components**
   - Input: File discovery error + validation error
   - Expected: Both errors reported in final output
   - Actual: [Pass/Fail]

2. **Test: Error ordering (critical first)**
   - Input: Mix of critical/warning/info
   - Expected: Critical errors listed first
   - Actual: [Pass/Fail]

3. **Test: Error deduplication**
   - Input: Same error from multiple sources
   - Expected: Error reported once with count
   - Actual: [Pass/Fail]

**Success Criteria:** All errors captured, none lost

---

### Boundary Test: test_error_reporting_boundaries
**Description:** Test with extreme error counts

**Test Cases:**
1. **Test: Many errors (>20)**
   - Input: Package with 25+ issues
   - Expected: Readable summary, not overwhelming
   - Actual: [Pass/Fail]

2. **Test: No errors (success case)**
   - Input: Perfect package
   - Expected: Success message, no error section
   - Actual: [Pass/Fail]

3. **Test: Only warnings (partial success)**
   - Input: Package with warnings but no critical errors
   - Expected: Clear distinction from success and failure
   - Actual: [Pass/Fail]

**Success Criteria:** Readable output at all scales

---

### System Test: test_error_reporting_system
**Description:** Test user can understand and act on error reports

**Test Cases:**
1. **Test: Actionable guidance for common errors**
   - Input: Missing CORE_LOADING_PROTOCOL
   - Expected: Error + suggested fix ("Restore from backup")
   - Actual: [Pass/Fail]

2. **Test: Clear next steps**
   - Input: Assembly with 3 warnings
   - Expected: "Review warnings and decide if acceptable"
   - Actual: [Pass/Fail]

3. **Test: Human comprehension**
   - Input: Error report given to human
   - Expected: Human knows what to fix and how
   - Actual: [Pass/Fail]

**Success Criteria:** Actionable guidance, clear next steps

---

## TEST EXECUTION SUMMARY

**Total test scenarios defined:** 72 (6 components × 4 test types × 3 cases per type)

**Test priority levels:**
1. **Critical (must pass):** Unit tests, integration tests for critical components
2. **High (should pass):** Boundary tests, system tests for core workflows
3. **Medium (nice to have):** Edge case system tests, performance tests

**Testing strategy:**
- Start with unit tests (fastest, most focused)
- Progress to integration tests (validate component interaction)
- Finish with system tests (end-to-end validation)
- Use boundary tests throughout to catch edge cases

**Success criteria for state_package_assembler:**
- All critical tests pass (100%)
- All high-priority tests pass (100%)
- Medium-priority tests: >80% pass rate acceptable

**Next steps:**
1. Implement test harness
2. Execute tests in order (unit → integration → boundary → system)
3. Document results (pass/fail/blocked)
4. Fix failures iteratively
5. Re-run full suite until success criteria met

---

**Test scenarios complete - ready for implementation and execution**

Δ|test-scenarios-complete|72-tests-defined|comprehensive-coverage|Ω
