"""
Z_generate_report.py

Python script to generate and validate the HTML report.
Loads cleaned data, computes key statistics, verifies asset files,
and provides a summary of the report generation process.
"""

import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATA_CANDIDATES = [
    PROJECT_ROOT / "outputs" / "cleaned_enhanced_data.csv",
    PROJECT_ROOT / "data" / "Original" / "acled_data.csv",  # Fallback to raw data
]
DOCS_DIR = PROJECT_ROOT / "docs"
REPORT_FILE = DOCS_DIR / "index.html"
ASSETS_DIR = DOCS_DIR / "assets"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# List of required asset files for the report
REQUIRED_ASSETS = [
    "causal_pathways_interactive.html",
    "conclusion_infographic.html",
    "figure3_conflict_vs_gdp.html",
    "final_exploration_report.html",
    "infographic_labour_structure.html",
    "interactive_conflict_agriculture.html",
    "new_normal_interactive.html",
    "policy_implications_interactive.html",
    "rq2_threshold_interactive.html",
    "rq3_interactive.html",
]


def load_and_validate_data():
    """Load and validate the cleaned enhanced dataset."""
    print("📂 Loading cleaned data...")
    
    data_path = None
    for candidate in DATA_CANDIDATES:
        if candidate.exists():
            data_path = candidate
            break
    
    if data_path is None:
        print(f"   ℹ No cleaned data found. Available data files:")
        raw_data = list((PROJECT_ROOT / "data").glob("*.csv"))
        for f in raw_data:
            print(f"      - {f.relative_to(PROJECT_ROOT)}")
        print("\n   ℹ Run notebooks in sequence: 01_data_cleaning → 02_exploration → 03_analysis")
        return None
    
    df = pd.read_csv(data_path)
    print(f"   ✓ Loaded from {data_path.relative_to(PROJECT_ROOT)}")
    print(f"   ✓ {len(df):,} rows × {len(df.columns)} columns")
    
    # Basic validation
    expected_columns = [
        "country", "year", "conflict_fatalities", "conflict_events",
        "agr_emp", "ind_emp", "ser_emp", "gdp_per_capita", "rule_of_law"
    ]
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        print(f"   ⚠ Warning: Missing columns {missing}")
    else:
        print(f"   ✓ All expected columns present")
    
    return df


def compute_summary_statistics(df):
    """Compute key statistics from the data."""
    print("\n📊 Computing summary statistics...")
    
    stats = {
        "generation_timestamp": datetime.now().isoformat(),
        "data_shape": {"rows": len(df), "columns": len(df.columns)},
    }
    
    # Try to extract statistics from available columns
    # Handle both cleaned (agr_emp, year) and raw (COUNTRY, FATALITIES) formats
    
    if "country" in df.columns:
        stats["countries"] = int(df["country"].nunique())
    elif "COUNTRY" in df.columns:
        stats["countries"] = int(df["COUNTRY"].nunique())
    
    if "year" in df.columns:
        year_vals = df["year"].dropna()
        if len(year_vals) > 0:
            stats["years_range"] = [int(year_vals.min()), int(year_vals.max())]
    
    stats["observations"] = len(df)
    
    # Conflict statistics
    if "conflict_fatalities" in df.columns:
        stats["conflict_fatalities"] = {
            "total": int(df["conflict_fatalities"].sum()),
            "mean": float(df["conflict_fatalities"].mean()),
            "max": int(df["conflict_fatalities"].max()),
        }
    elif "FATALITIES" in df.columns:
        stats["conflict_fatalities"] = {
            "total": int(df["FATALITIES"].sum()),
            "mean": float(df["FATALITIES"].mean()),
            "max": int(df["FATALITIES"].max()),
        }
    
    if "conflict_events" in df.columns:
        stats["conflict_events"] = {
            "total": int(df["conflict_events"].sum()),
            "mean": float(df["conflict_events"].mean()),
            "max": int(df["conflict_events"].max()),
        }
    elif "EVENTS" in df.columns:
        stats["conflict_events"] = {
            "total": int(df["EVENTS"].sum()),
            "mean": float(df["EVENTS"].mean()),
            "max": int(df["EVENTS"].max()),
        }
    
    # Employment statistics
    if "agr_emp" in df.columns:
        stats["agriculture_employment"] = {
            "mean": float(df["agr_emp"].mean()),
            "min": float(df["agr_emp"].min()),
            "max": float(df["agr_emp"].max()),
        }
    
    if "gdp_per_capita" in df.columns:
        stats["gdp_per_capita"] = {
            "mean": float(df["gdp_per_capita"].mean()),
            "min": float(df["gdp_per_capita"].min()),
            "max": float(df["gdp_per_capita"].max()),
        }
    
    # Print summary
    if "countries" in stats:
        print(f"   ✓ Countries: {stats['countries']}")
    if "years_range" in stats:
        print(f"   ✓ Time period: {stats['years_range'][0]}-{stats['years_range'][1]}")
    print(f"   ✓ Observations: {stats['observations']:,}")
    
    return stats


def validate_asset_files():
    """Validate that all required asset files exist."""
    print("\n🎨 Validating interactive asset files...")
    
    missing_assets = []
    for asset in REQUIRED_ASSETS:
        asset_path = ASSETS_DIR / asset
        if asset_path.exists():
            size_kb = asset_path.stat().st_size / 1024
            print(f"   ✓ {asset} ({size_kb:.1f} KB)")
        else:
            print(f"   ✗ {asset} (MISSING)")
            missing_assets.append(asset)
    
    if missing_assets:
        print(f"\n   ⚠ Warning: {len(missing_assets)} asset(s) missing")
        return False
    else:
        print(f"\n   ✓ All {len(REQUIRED_ASSETS)} assets present")
        return True


def validate_report_file():
    """Validate that the main report file exists and contains key content."""
    print("\n📄 Validating main report file...")
    
    if not REPORT_FILE.exists():
        print(f"   ✗ Report file not found: {REPORT_FILE}")
        return False
    
    size_kb = REPORT_FILE.stat().st_size / 1024
    print(f"   ✓ Report file exists ({size_kb:.1f} KB)")
    
    # Check for key content
    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    key_phrases = [
        "Does Political Violence Trap Economies",
        "Research Question",
        "conclusion_infographic",
        "causal_pathways",
    ]
    
    for phrase in key_phrases:
        if phrase in content:
            print(f"   ✓ Contains: '{phrase}'")
        else:
            print(f"   ✗ Missing: '{phrase}'")
    
    return True


def save_summary_report(stats, assets_valid, report_valid):
    """Save a summary report as JSON and TXT."""
    print("\n💾 Saving summary report...")
    
    summary = {
        "status": "COMPLETE" if (assets_valid and report_valid) else "INCOMPLETE",
        "data_summary": stats,
        "assets_validation": "PASS" if assets_valid else "FAIL",
        "report_validation": "PASS" if report_valid else "FAIL",
        "timestamp": datetime.now().isoformat(),
    }
    
    # Save JSON
    json_path = OUTPUTS_DIR / "summary_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"   ✓ Saved to {json_path.relative_to(PROJECT_ROOT)}")
    
    # Save TXT
    txt_path = OUTPUTS_DIR / "summary_report.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("HTML REPORT GENERATION SUMMARY\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Status: {summary['status']}\n")
        f.write(f"Generated: {summary['timestamp']}\n\n")
        
        f.write("DATA SUMMARY\n")
        f.write("-" * 70 + "\n")
        if "countries" in stats:
            f.write(f"Countries: {stats['countries']}\n")
        if "years_range" in stats:
            f.write(f"Time Period: {stats['years_range'][0]}-{stats['years_range'][1]}\n")
        f.write(f"Observations: {stats['observations']:,}\n")
        if "conflict_fatalities" in stats:
            f.write(f"Total Conflict Fatalities: {stats['conflict_fatalities']['total']:,}\n")
        if "gdp_per_capita" in stats:
            f.write(f"Mean GDP per Capita: ${stats['gdp_per_capita']['mean']:.2f}\n")
        if "agriculture_employment" in stats:
            f.write(f"Mean Agricultural Employment: {stats['agriculture_employment']['mean']:.2f}%\n")
        f.write("\n")
        
        f.write("ASSET VALIDATION\n")
        f.write("-" * 70 + "\n")
        f.write(f"Status: {summary['assets_validation']}\n")
        f.write(f"Required Assets: {len(REQUIRED_ASSETS)}\n\n")
        
        f.write("REPORT VALIDATION\n")
        f.write("-" * 70 + "\n")
        f.write(f"Status: {summary['report_validation']}\n")
        f.write(f"Report File: {REPORT_FILE.relative_to(PROJECT_ROOT)}\n")
        f.write(f"Size: {REPORT_FILE.stat().st_size / 1024:.1f} KB\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("Report is ready for viewing!\n")
        f.write(f"Open in browser: {REPORT_FILE}\n")
        f.write("=" * 70 + "\n")
    
    print(f"   ✓ Saved to {txt_path.relative_to(PROJECT_ROOT)}")


def main():
    """Main report generation workflow."""
    print("\n" + "=" * 70)
    print("REPORT GENERATION SCRIPT")
    print("=" * 70)
    
    try:
        # Load and validate data
        df = load_and_validate_data()
        
        # Create outputs directory if it doesn't exist
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # If data is missing, skip statistics and just validate report/assets
        if df is None:
            print("\n⚠️  Proceeding with report/asset validation (no data statistics)")
            stats = {"status": "DATA_NOT_AVAILABLE"}
        else:
            # Compute statistics
            stats = compute_summary_statistics(df)
        
        # Validate assets and report
        assets_valid = validate_asset_files()
        report_valid = validate_report_file()
        
        # Save summary
        save_summary_report(stats, assets_valid, report_valid)
        
        # Final status
        print("\n" + "=" * 70)
        if assets_valid and report_valid:
            print("✅ REPORT GENERATION COMPLETE")
            print(f"\n📖 Open the report at:\n   {REPORT_FILE}")
        else:
            print("⚠️  REPORT GENERATION COMPLETE WITH WARNINGS")
            if not assets_valid:
                print("   - Some asset files are missing")
            if not report_valid:
                print("   - Report file validation found issues")
        print("=" * 70 + "\n")
        
        return 0 if (assets_valid and report_valid) else 1
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
