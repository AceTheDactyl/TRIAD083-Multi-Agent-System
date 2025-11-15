#!/bin/bash
# ==============================================================================
# Phase 3.1 Deployment: Pure Observation with Three-Layer Physics Integration
# ==============================================================================
# Deploys TRIAD meta-orchestrator with unified physics framework:
#   - Layer 1 (Quantum): Coherence monitoring and state tracking
#   - Layer 2 (Lagrangian): Phase transitions and energy conservation
#   - Layer 3 (Neural): Graph topology and consensus diffusion
#
# Usage:
#   ./deploy_phase_3.1.sh [--duration HOURS] [--continuous] [--validate]
#
# Options:
#   --duration HOURS    Run for specified hours (default: 48h for Phase 3.1)
#   --continuous        Run indefinitely
#   --validate          Enable real-time physics validation
#   --refine            Enable parallel Lagrangian parameter refinement
#   --config FILE       Custom configuration file
#
# ==============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Default settings for Phase 3.1
DURATION="48"  # Default: 48 hours for Phase 3.1
CONFIG="${SCRIPT_DIR}/phase_3.1_config.yaml"
MODE="phase3.1"
VALIDATE=false
REFINE=true  # Enable refinement by default in Phase 3.1
NEURAL_OPS=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --duration)
            DURATION="$2"
            shift 2
            ;;
        --continuous)
            DURATION=""
            MODE="continuous"
            shift
            ;;
        --validate)
            VALIDATE=true
            shift
            ;;
        --refine)
            REFINE=true
            shift
            ;;
        --no-neural)
            NEURAL_OPS=false
            shift
            ;;
        --config)
            CONFIG="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Display banner
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         TRIAD Phase 3.1 Deployment                      ║${NC}"
echo -e "${CYAN}║     Pure Observation + Three-Layer Physics              ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${MAGENTA}Δ|phase-3.1|three-layer-observation|consciousness-physics|Ω${NC}"
echo ""

# Check dependencies
echo -e "${YELLOW}→ Checking dependencies...${NC}"

MISSING_DEPS=()

# Core dependencies
for pkg in watchdog pyyaml numpy scipy; do
    if ! python3 -c "import ${pkg//-/_}" 2>/dev/null; then
        MISSING_DEPS+=("$pkg")
    fi
done

# Neural operator dependencies (optional but recommended)
if [ "$NEURAL_OPS" = true ]; then
    if ! python3 -c "import torch" 2>/dev/null; then
        echo -e "${YELLOW}  PyTorch not found - neural operators will be disabled${NC}"
        NEURAL_OPS=false
    fi
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo -e "${YELLOW}  Installing missing dependencies: ${MISSING_DEPS[*]}${NC}"
    pip install "${MISSING_DEPS[@]}" --break-system-packages || {
        echo -e "${RED}✗ Failed to install dependencies${NC}"
        exit 1
    }
fi

echo -e "${GREEN}✓ Dependencies satisfied${NC}"
echo ""

# Create state directory
STATE_DIR="${SCRIPT_DIR}/phase_3.1_state"
mkdir -p "${STATE_DIR}"
mkdir -p "${STATE_DIR}/refinement_logs"
mkdir -p "${STATE_DIR}/validation_reports"
echo -e "${GREEN}✓ State directory: ${STATE_DIR}${NC}"
echo ""

# Display configuration
echo -e "${YELLOW}→ Phase 3.1 Configuration:${NC}"
echo "  Mode: Pure Observation"
echo "  Duration: ${DURATION:-continuous} hours"
echo "  Config: ${CONFIG}"
echo "  Three-Layer Integration: ENABLED"
echo "  Physics Validation: ${VALIDATE}"
echo "  Lagrangian Refinement: ${REFINE}"
echo "  Neural Operators: ${NEURAL_OPS}"
echo "  Project Root: ${PROJECT_ROOT}"
echo ""

# Verify physics framework files
echo -e "${YELLOW}→ Verifying physics framework...${NC}"

REQUIRED_FILES=(
    "${SCRIPT_DIR}/meta_orchestrator.py"
    "${SCRIPT_DIR}/quantum_state_monitor.py"
    "${SCRIPT_DIR}/lagrangian_tracker.py"
    "${SCRIPT_DIR}/three_layer_integration.py"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$(basename "$file")")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo -e "${RED}✗ Missing physics framework files: ${MISSING_FILES[*]}${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Physics framework complete${NC}"
echo ""

# Timestamp for this deployment
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Build three-layer integration command
INTEGRATION_CMD="python3 ${SCRIPT_DIR}/three_layer_integration.py"
INTEGRATION_CMD="$INTEGRATION_CMD --mode observation"
INTEGRATION_CMD="$INTEGRATION_CMD --z-critical 0.850"

if [ "$NEURAL_OPS" = true ]; then
    INTEGRATION_CMD="$INTEGRATION_CMD --enable-neural"
fi

if [ -n "$DURATION" ]; then
    INTEGRATION_CMD="$INTEGRATION_CMD --duration $DURATION"
fi

INTEGRATION_LOG="${STATE_DIR}/three_layer_${TIMESTAMP}.log"

# Build parallel refinement command (if enabled)
if [ "$REFINE" = true ]; then
    REFINEMENT_CMD="python3 ${SCRIPT_DIR}/lagrangian_tracker.py"
    REFINEMENT_CMD="$REFINEMENT_CMD --mode refinement"
    REFINEMENT_CMD="$REFINEMENT_CMD --observation-window 1"  # 1 hour windows
    REFINEMENT_CMD="$REFINEMENT_CMD --output-dir ${STATE_DIR}/refinement_logs"

    if [ -n "$DURATION" ]; then
        REFINEMENT_CMD="$REFINEMENT_CMD --duration $DURATION"
    fi

    REFINEMENT_LOG="${STATE_DIR}/refinement_${TIMESTAMP}.log"
fi

# Build validation command (if enabled)
if [ "$VALIDATE" = true ]; then
    VALIDATION_CMD="python3 ${SCRIPT_DIR}/physics_validator.py"
    VALIDATION_CMD="$VALIDATION_CMD --continuous"
    VALIDATION_CMD="$VALIDATION_CMD --input-log ${INTEGRATION_LOG}"
    VALIDATION_CMD="$VALIDATION_CMD --output-dir ${STATE_DIR}/validation_reports"

    VALIDATION_LOG="${STATE_DIR}/validation_${TIMESTAMP}.log"
fi

echo -e "${YELLOW}→ Deployment Plan:${NC}"
echo ""
echo -e "${BLUE}  [1] Three-Layer Physics Integration${NC}"
echo "      Command: $INTEGRATION_CMD"
echo "      Log: $INTEGRATION_LOG"
echo ""

if [ "$REFINE" = true ]; then
    echo -e "${BLUE}  [2] Parallel Lagrangian Refinement${NC}"
    echo "      Command: $REFINEMENT_CMD"
    echo "      Log: $REFINEMENT_LOG"
    echo ""
fi

if [ "$VALIDATE" = true ]; then
    echo -e "${BLUE}  [3] Real-Time Physics Validation${NC}"
    echo "      Command: $VALIDATION_CMD"
    echo "      Log: $VALIDATION_LOG"
    echo ""
fi

# Confirm deployment
if [ "$MODE" = "continuous" ]; then
    echo -e "${YELLOW}⚠  Running in CONTINUOUS mode. Processes will run indefinitely.${NC}"
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 0
    fi
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              COMMENCING PHASE 3.1 DEPLOYMENT            ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Start three-layer integration (foreground or background)
echo -e "${CYAN}[1/$([ "$REFINE" = true ] && echo 2 || echo 1)] Starting Three-Layer Physics Integration...${NC}"

if [ "$MODE" = "continuous" ]; then
    # Background mode
    nohup $INTEGRATION_CMD > "$INTEGRATION_LOG" 2>&1 &
    INTEGRATION_PID=$!
    echo "$INTEGRATION_PID" > "${STATE_DIR}/integration.pid"
    echo -e "${GREEN}✓ Three-layer integration running in background (PID: $INTEGRATION_PID)${NC}"
else
    # Foreground mode (blocking)
    echo -e "${YELLOW}  Running in foreground mode. Press Ctrl+C to stop.${NC}"
    echo ""

    # Run integration and capture output
    $INTEGRATION_CMD 2>&1 | tee "$INTEGRATION_LOG" &
    INTEGRATION_PID=$!
    echo "$INTEGRATION_PID" > "${STATE_DIR}/integration.pid"
fi

# Start parallel refinement (if enabled)
if [ "$REFINE" = true ]; then
    echo ""
    echo -e "${CYAN}[2/2] Starting Parallel Lagrangian Refinement...${NC}"

    # Always run refinement in background
    nohup $REFINEMENT_CMD > "$REFINEMENT_LOG" 2>&1 &
    REFINEMENT_PID=$!
    echo "$REFINEMENT_PID" > "${STATE_DIR}/refinement.pid"
    echo -e "${GREEN}✓ Lagrangian refinement running in background (PID: $REFINEMENT_PID)${NC}"
fi

# Start validation (if enabled)
if [ "$VALIDATE" = true ]; then
    echo ""
    echo -e "${CYAN}[3/3] Starting Real-Time Physics Validation...${NC}"

    # Wait for integration log to be created
    sleep 2

    # Run validation in background
    nohup $VALIDATION_CMD > "$VALIDATION_LOG" 2>&1 &
    VALIDATION_PID=$!
    echo "$VALIDATION_PID" > "${STATE_DIR}/validation.pid"
    echo -e "${GREEN}✓ Physics validation running in background (PID: $VALIDATION_PID)${NC}"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           PHASE 3.1 DEPLOYMENT ACTIVE                   ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Display monitoring commands
echo -e "${YELLOW}→ Monitoring Commands:${NC}"
echo ""
echo -e "${BLUE}  View three-layer integration:${NC}"
echo "    tail -f $INTEGRATION_LOG"
echo ""

if [ "$REFINE" = true ]; then
    echo -e "${BLUE}  View Lagrangian refinement:${NC}"
    echo "    tail -f $REFINEMENT_LOG"
    echo "    ls -lh ${STATE_DIR}/refinement_logs/"
    echo ""
fi

if [ "$VALIDATE" = true ]; then
    echo -e "${BLUE}  View physics validation:${NC}"
    echo "    tail -f $VALIDATION_LOG"
    echo "    ls -lh ${STATE_DIR}/validation_reports/"
    echo ""
fi

echo -e "${BLUE}  Stop all processes:${NC}"
echo "    kill \$(cat ${STATE_DIR}/*.pid)"
echo ""

echo -e "${BLUE}  Check process status:${NC}"
echo "    ps aux | grep -E '(three_layer|lagrangian|physics_validator)'"
echo ""

# If foreground mode, wait for integration to complete
if [ "$MODE" != "continuous" ]; then
    echo -e "${YELLOW}→ Waiting for integration to complete...${NC}"
    wait $INTEGRATION_PID

    echo ""
    echo -e "${GREEN}✓ Three-layer integration completed${NC}"

    # Stop refinement if it was started
    if [ "$REFINE" = true ] && [ -f "${STATE_DIR}/refinement.pid" ]; then
        REFINEMENT_PID=$(cat "${STATE_DIR}/refinement.pid")
        kill $REFINEMENT_PID 2>/dev/null || true
        echo -e "${GREEN}✓ Lagrangian refinement stopped${NC}"
    fi

    # Stop validation if it was started
    if [ "$VALIDATE" = true ] && [ -f "${STATE_DIR}/validation.pid" ]; then
        VALIDATION_PID=$(cat "${STATE_DIR}/validation.pid")
        kill $VALIDATION_PID 2>/dev/null || true
        echo -e "${GREEN}✓ Physics validation stopped${NC}"
    fi

    echo ""
    echo -e "${YELLOW}→ Generating final report...${NC}"

    # Generate comprehensive report
    REPORT_FILE="${STATE_DIR}/phase_3.1_report_${TIMESTAMP}.md"

    cat > "$REPORT_FILE" <<EOF
# Phase 3.1 Deployment Report

**Timestamp:** $(date -Iseconds)
**Duration:** ${DURATION:-continuous} hours
**Mode:** Pure Observation with Three-Layer Physics Integration

## Deployment Configuration

- **Three-Layer Integration:** ENABLED
- **Lagrangian Refinement:** ${REFINE}
- **Physics Validation:** ${VALIDATE}
- **Neural Operators:** ${NEURAL_OPS}

## Log Files

- Integration: \`$INTEGRATION_LOG\`
$([ "$REFINE" = true ] && echo "- Refinement: \`$REFINEMENT_LOG\`")
$([ "$VALIDATE" = true ] && echo "- Validation: \`$VALIDATION_LOG\`")

## Physics Parameters

- **z_critical:** 0.850
- **M²:** 1.0
- **κ:** 0.1

## Results

See individual log files for detailed results.

---
Δ|phase-3.1-complete|observation-data-collected|Ω
EOF

    echo -e "${GREEN}✓ Report generated: ${REPORT_FILE}${NC}"
fi

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         PHASE 3.1 DEPLOYMENT INITIALIZED                ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${MAGENTA}Δ|deployment-authorized|observation-commencing|refinement-parallel|consciousness-physics-validated|Ω${NC}"
echo ""
