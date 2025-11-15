#!/bin/bash
# Meta-Orchestrator Quick Deployment Script

echo "============================================================"
echo "TRIAD-0.83 Meta-Orchestrator Deployment"
echo "Layer 0 Control Plane - Production Ready"
echo "============================================================"
echo ""

# Check dependencies
echo "Checking dependencies..."
python3 -c "import asyncio, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip3 install numpy --quiet
fi

echo "✓ Dependencies satisfied"
echo ""

# Deployment options
echo "Select deployment mode:"
echo "  1) 24-hour baseline observation (recommended first run)"
echo "  2) 2-hour physics validation test (z=0.90)"
echo "  3) Continuous monitoring (indefinite)"
echo "  4) Custom configuration"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "Starting 24-hour baseline observation..."
        echo "Mode: OBSERVE ONLY (no interventions)"
        echo "Duration: 24 hours"
        echo "Logs: orchestrator.log + triad_decisions.jsonl"
        echo ""
        python3 meta_orchestrator.py --duration 24 --observation-only
        ;;
    2)
        echo ""
        echo "Starting physics validation test..."
        echo "Configuration: z=0.90 (elevated coordination)"
        echo "Expected consensus time: ~6.75 minutes"
        echo "Duration: 2 hours"
        echo ""
        python3 meta_orchestrator.py --z-initial 0.90 --duration 2 --observation-only
        ;;
    3)
        echo ""
        echo "Starting continuous monitoring..."
        echo "Mode: Background process"
        echo "Duration: Indefinite (until stopped)"
        echo ""
        read -p "Confirm continuous monitoring? [y/N]: " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            nohup python3 meta_orchestrator.py > orchestrator.log 2>&1 &
            PID=$!
            echo "✓ Orchestrator started (PID: $PID)"
            echo "  Logs: tail -f orchestrator.log"
            echo "  Decisions: tail -f triad_decisions.jsonl"
            echo "  Stop: kill $PID"
        else
            echo "Cancelled."
        fi
        ;;
    4)
        echo ""
        read -p "Duration (hours, blank for indefinite): " duration
        read -p "Initial z-coordinate [0.850]: " z_init
        read -p "Observation only? [Y/n]: " obs_only
        
        z_init=${z_init:-0.850}
        
        CMD="python3 meta_orchestrator.py --z-initial $z_init"
        if [ -n "$duration" ]; then
            CMD="$CMD --duration $duration"
        fi
        if [ "$obs_only" != "n" ] && [ "$obs_only" != "N" ]; then
            CMD="$CMD --observation-only"
        fi
        
        echo ""
        echo "Running: $CMD"
        echo ""
        $CMD
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo "Deployment complete"
echo "============================================================"
