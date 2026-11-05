from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.cleaning import load_and_clean

def main():
    source = ROOT / "data/raw/brasileirao.csv"
    output = ROOT / "data/processed"
    output.mkdir(parents=True, exist_ok=True)
    if not source.exists(): raise FileNotFoundError("Execute python scripts/download_data.py primeiro")
    df, report = load_and_clean(source)
    df.to_csv(output / "brasileirao_clean.csv", index=False, encoding="utf-8")
    (output / "quality_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
