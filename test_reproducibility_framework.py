#!/usr/bin/env python3
"""
Quick validation test for reproducibility framework.
Tests with n=5 trials at z=0.867 to verify everything works.
"""

from reproducibility_study import ReproducibilityStudy

def main():
    print("Quick Validation Test")
    print("=" * 80)
    print("Testing framework with 5 trials at z=0.867 (critical point)\n")

    # Create minimal study
    study = ReproducibilityStudy(
        z_min=0.867,
        z_max=0.867,
        z_step=0.01,
        trials_per_z=5
    )

    # Run scan
    z_analyses = study.run_z_range_scan()

    # Generate and print report
    report = study.generate_report(z_analyses)
    study.print_summary(report)

    print("\n✅ Framework validation complete!")
    print(f"   Mean reduction: {report.overall_mean_reduction:.1f}%")
    print(f"   Expected: ~60% (if original signal is real)")
    print(f"   Predicted: {report.predicted_reduction}%")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
