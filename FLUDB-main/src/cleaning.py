import re
import unicodedata
import pandas as pd


ALIASES = {
    "data": "date",
    "date": "date",
    "mandante": "home_team",
    "home_team": "home_team",
    "visitante": "away_team",
    "away_team": "away_team",
    "mandante_placar": "home_goals",
    "visitante_placar": "away_goals",
    "home_goals": "home_goals",
    "away_goals": "away_goals",
    "vencedor": "winner",
    "arena": "venue",
    "estadio": "venue",
    "id": "match_id",
    "match_id": "match_id",
    "rodada": "round",
    "hora": "time",
}


def normalize_column_name(column):
    value = unicodedata.normalize("NFKD", str(column).strip())
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"\s+", "_", value)
    return value.lower()


def clean_text(value):
    if pd.isna(value):
        return pd.NA

    value = re.sub(r"\s+", " ", str(value).strip())
    return value if value else pd.NA


def team_name(value):
    value = clean_text(value)

    if pd.isna(value):
        return pd.NA

    key = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )

    return {
        "fluminense": "Fluminense",
        "fluminense football club": "Fluminense",
    }.get(key, value)


def load_and_clean(path):

    raw = pd.read_csv(
        path,
        encoding="utf-8-sig",
        sep=None,
        engine="python"
    )

    raw_count = len(raw)
    original_cols = list(raw.columns)

    raw.columns = [
        normalize_column_name(column)
        for column in raw.columns
    ]

    rename_map = {
        column: ALIASES[column]
        for column in raw.columns
        if column in ALIASES
    }

    df = raw.rename(columns=rename_map).copy()

    required = [
        "date",
        "home_team",
        "away_team",
        "home_goals",
        "away_goals",
    ]

    missing = [
        column for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Colunas ausentes {missing}; "
            f"recebidas: {list(df.columns)}. "
            f"Originais: {original_cols}"
        )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
        dayfirst=True
    )

    for column in [
        "home_team",
        "away_team",
        "winner",
        "venue"
    ]:
        if column in df.columns:
            df[column] = df[column].map(clean_text)

    df["home_team"] = df["home_team"].map(team_name)
    df["away_team"] = df["away_team"].map(team_name)

    for column in ["home_goals", "away_goals"]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    duplicate_rows_removed = int(df.duplicated().sum())

    df = df.drop_duplicates()

    invalid_required_rows_removed = int(
        df[required].isna().any(axis=1).sum()
    )

    df = df.dropna(subset=required)

    valid_scores = (
        (df["home_goals"] >= 0)
        & (df["away_goals"] >= 0)
        & (df["home_goals"] % 1 == 0)
        & (df["away_goals"] % 1 == 0)
    )

    df = df.loc[valid_scores].copy()

    df["home_goals"] = df["home_goals"].astype(int)
    df["away_goals"] = df["away_goals"].astype(int)

    df["season"] = df["date"].dt.year

    df["result"] = "Draw"

    df.loc[
        df["home_goals"] > df["away_goals"],
        "result"
    ] = "Home win"

    df.loc[
        df["home_goals"] < df["away_goals"],
        "result"
    ] = "Away win"

    report = {
        "rows_raw": raw_count,
        "duplicate_rows_removed": duplicate_rows_removed,
        "rows_after_exact_dedup": raw_count - duplicate_rows_removed,
        "invalid_required_rows_removed": invalid_required_rows_removed,
        "rows_clean": len(df),
        "columns_original": original_cols,
        "missing_by_column_raw": (
            raw.isna().sum().astype(int).to_dict()
        ),
    }

    return (
        df.sort_values("date").reset_index(drop=True),
        report
    )