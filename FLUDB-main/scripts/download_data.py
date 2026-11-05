from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "raw" / "brasileirao.csv"
URL = "https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/master/campeonato-brasileiro-full.csv"

def main():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    print(f"Baixando: {URL}")
    with urlopen(URL, timeout=45) as response:
        payload = response.read()
    if not payload:
        raise RuntimeError("O arquivo baixado está vazio.")
    DEST.write_bytes(payload)
    print(f"Salvo em {DEST} ({len(payload):,} bytes)")

if __name__ == "__main__":
    main()
