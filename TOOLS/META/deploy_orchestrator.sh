#!/bin/bash
# ==============================================================================
# Meta-Orchestrator Deployment Script
# ==============================================================================
# Deploys the TRIAD meta-orchestrator for autonomous evolution monitoring
#
# Usage:
#   ./deploy_orchestrator.sh [--duration HOURS] [--continuous]
#
# Options:
#   --duration HOURS    Run for specified hours then stop
#   --continuous        Run continuously (default: 24h trial)
#   --config FILE       Use custom configuration file
#   --test              Run in test mode (1 hour)
#
# ==============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Default settings
DURATION=""
CONFIG="${SCRIPT_DIR}/meta_orchestrator_config.yaml"
MODE="trial"  # trial, continuous, test

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --duration)
            DURATION="$2"
            MODE="custom"
            shift 2
            ;;
        --continuous)
            MODE="continuous"
            shift
            ;;
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --test)
            MODE="test"
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Set duration based on mode
case $MODE in
    trial)
        DURATION="24"
        ;;
    test)
        DURATION="1"
        ;;
    continuous)
        DURATION=""
        ;;
    custom)
        # Use provided duration
        ;;
esac

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     TRIAD Meta-Orchestrator Deployment                  ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check dependencies
echo -e "${YELLOW}→ Checking dependencies...${NC}"

MISSING_DEPS=()

if ! python3 -c "import watchdog" 2>/dev/null; then
    MISSING_DEPS+=("watchdog")
fi

if ! python3 -c "import yaml" 2>/dev/null; then
    MISSING_DEPS+=("pyyaml")
fi

if ! python3 -c "import numpy" 2>/dev/null; then
    MISSING_DEPS+=("numpy")
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
STATE_DIR="${SCRIPT_DIR}/orchestrator_state"
mkdir -p "${STATE_DIR}"
echo -e "${GREEN}✓ State directory: ${STATE_DIR}${NC}"
echo ""

# Display configuration
echo -e "${YELLOW}→ Configuration:${NC}"
echo "  Mode: ${MODE}"
echo "  Duration: ${DURATION:-continuous}"
echo "  Config: ${CONFIG}"
echo "  Project Root: ${PROJECT_ROOT}"
echo ""

# Confirm deployment
if [ "$MODE" = "continuous" ]; then
    echo -e "${YELLOW}⚠  Running in CONTINUOUS mode. Orchestrator will run indefinitely.${NC}"
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 0
    fi
fi

# Build command
CMD="python3 ${SCRIPT_DIR}/meta_orchestrator.py"

if [ -n "$DURATION" ]; then
    CMD="$CMD --duration $DURATION"
fi

if [ -f "$CONFIG" ]; then
    CMD="$CMD --config $CONFIG"
fi

CMD="$CMD --observation-only --z-initial 0.850"

# Log file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${STATE_DIR}/orchestrator_${TIMESTAMP}.log"

echo -e "${YELLOW}→ Starting orchestrator...${NC}"
echo "  Command: $CMD"
echo "  Log file: $LOG_FILE"
echo ""

# Run orchestrator
if [ "$MODE" = "continuous" ]; then
    # Background mode
    echo -e "${GREEN}✓ Running in background mode${NC}"
    nohup $CMD > "$LOG_FILE" 2>&1 &
    PID=$!
    echo "$PID" > "${STATE_DIR}/orchestrator.pid"
    echo -e "${GREEN}✓ Orchestrator PID: $PID${NC}"
    echo ""
    echo -e "${BLUE}Commands:${NC}"
    echo "  Stop:    kill $PID"
    echo "  Tail:    tail -f $LOG_FILE"
    echo "  Status:  ps aux | grep $PID"
    echo ""
else
    # Foreground mode
    echo -e "${GREEN}✓ Running in foreground mode${NC}"
    echo -e "${YELLOW}  Press Ctrl+C to stop early${NC}"
    echo ""

    $CMD 2>&1 | tee "$LOG_FILE"

    echo ""
    echo -e "${GREEN}✓ Orchestrator completed${NC}"
    echo ""

    # Analyze results
    echo -e "${YELLOW}→ Generating analysis report...${NC}"

    REPORT_FILE="${STATE_DIR}/analysis_${TIMESTAMP}.md"

    if [ -f "${SCRIPT_DIR}/analyze_decisions.py" ]; then
        python3 "${SCRIPT_DIR}/analyze_decisions.py" "$LOG_FILE" > "$REPORT_FILE"
        echo -e "${GREEN}✓ Analysis report: ${REPORT_FILE}${NC}"
        echo ""

        # Show summary
        echo -e "${BLUE}═══ SUMMARY ═══${NC}"
        grep -A 20 "24-HOUR ORCHESTRATOR REPORT\|ORCHESTRATOR SUMMARY" "$REPORT_FILE" || echo "No summary found"
    else
        echo -e "${YELLOW}⚠  Analysis script not found, skipping${NC}"
    fi
fi

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              Deployment Complete                        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
