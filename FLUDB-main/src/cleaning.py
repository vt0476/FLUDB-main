import re
import unicodedata
import pandas as pd

ALIASES = {
    "data": "date",
    "mandante": "home_team",
    "visitante": "away_team",
    "mandante_Placar": "home_goals",
    "visitante_Placar": "away_goals",
    "vencedor": "winner",
    "arena": "venue",
    "match_id": "match_id",
    "rodada": "round",
    "hora": "time",
}

def clean_text(value):
    if pd.isna(value): return pd.NA
    value = re.sub(r"\s+", " ", str(value).strip())
    return value or pd.NA

def team_name(value):
    value = clean_text(value)
    if pd.isna(value): return pd.NA
    key = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return {"fluminense":"Fluminense", "fluminense football club":"Fluminense"}.get(key, value)

def load_and_clean(path):
    raw = pd.read_csv(path, encoding="utf-8", sep=None, engine="python")
    raw_count, original_cols = len(raw), list(raw.columns)
    raw.columns = [str(c).strip().replace(" ", "_") for c in raw.columns]
    df = raw.rename(columns={c: ALIASES[c] for c in raw.columns if c in ALIASES}).copy()
    required = ["date", "home_team", "away_team", "home_goals", "away_goals"]
    missing = [c for c in required if c not in df]
    if missing: raise ValueError(f"Colunas ausentes {missing}; recebidas: {list(df.columns)}")
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    for c in ["home_team", "away_team", "winner", "venue"]:
        if c in df: df[c] = df[c].map(clean_text)
    df["home_team"] = df["home_team"].map(team_name)
    df["away_team"] = df["away_team"].map(team_name)
    for c in ["home_goals", "away_goals"]: df[c] = pd.to_numeric(df[c], errors="coerce")
    dup = int(df.duplicated().sum())
    df = df.drop_duplicates()
    invalid = int(df[required].isna().any(axis=1).sum())
    df = df.dropna(subset=required)
    df = df[(df.home_goals >= 0) & (df.away_goals >= 0) & (df.home_goals % 1 == 0) & (df.away_goals % 1 == 0)]
    df["home_goals"] = df.home_goals.astype(int); df["away_goals"] = df.away_goals.astype(int)
    df["season"] = df.date.dt.year
    df["result"] = "Draw"
    df.loc[df.home_goals > df.away_goals, "result"] = "Home win"
    df.loc[df.home_goals < df.away_goals, "result"] = "Away win"
    report = {"rows_raw":raw_count,"duplicate_rows_removed":dup,"rows_after_exact_dedup":raw_count-dup,"invalid_required_rows_removed":invalid,"rows_clean":len(df),"columns_original":original_cols,"missing_by_column_raw":raw.isna().sum().astype(int).to_dict()}
    return df.sort_values("date").reset_index(drop=True), report
