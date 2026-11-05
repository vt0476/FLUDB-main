from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "brasileirao_clean.csv"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["date"])
flu = df[(df["home_team"] == "Fluminense") | (df["away_team"] == "Fluminense")].copy()

flu["is_home"] = flu["home_team"].eq("Fluminense")
flu["flu_goals"] = flu["home_goals"].where(flu["is_home"], flu["away_goals"])
flu["opponent_goals"] = flu["away_goals"].where(flu["is_home"], flu["home_goals"])
flu["opponent"] = flu["away_team"].where(flu["is_home"], flu["home_team"])
flu["venue_type"] = flu["is_home"].map({True: "Casa", False: "Fora"})

flu["outcome"] = "Empate"
flu.loc[flu["flu_goals"] > flu["opponent_goals"], "outcome"] = "Vitória"
flu.loc[flu["flu_goals"] < flu["opponent_goals"], "outcome"] = "Derrota"
flu["points"] = flu["outcome"].map({"Vitória": 3, "Empate": 1, "Derrota": 0})
flu["season"] = flu["date"].dt.year

season = flu.groupby("season").agg(
    partidas=("outcome", "size"),
    vitorias=("outcome", lambda s: (s == "Vitória").sum()),
    empates=("outcome", lambda s: (s == "Empate").sum()),
    derrotas=("outcome", lambda s: (s == "Derrota").sum()),
    pontos=("points", "sum"),
    gols_marcados=("flu_goals", "sum"),
    gols_sofridos=("opponent_goals", "sum"),
).reset_index()
season["aproveitamento_pct"] = (season["pontos"] / (season["partidas"] * 3) * 100).round(1)
season["saldo_gols"] = season["gols_marcados"] - season["gols_sofridos"]
season.to_csv(OUT / "analise_por_temporada.csv", index=False, encoding="utf-8-sig")

results = flu["outcome"].value_counts().reindex(["Vitória", "Empate", "Derrota"], fill_value=0)
venue = flu.groupby("venue_type").agg(
    partidas=("outcome", "size"),
    vitorias=("outcome", lambda s: (s == "Vitória").sum()),
    empates=("outcome", lambda s: (s == "Empate").sum()),
    derrotas=("outcome", lambda s: (s == "Derrota").sum()),
    pontos=("points", "sum"),
).reset_index()
venue["aproveitamento_pct"] = (venue["pontos"] / (venue["partidas"] * 3) * 100).round(1)
venue.to_csv(OUT / "analise_casa_fora.csv", index=False, encoding="utf-8-sig")

opponents = flu.groupby("opponent").agg(
    partidas=("outcome", "size"),
    vitorias=("outcome", lambda s: (s == "Vitória").sum()),
    empates=("outcome", lambda s: (s == "Empate").sum()),
    derrotas=("outcome", lambda s: (s == "Derrota").sum()),
    pontos=("points", "sum"),
).sort_values(["partidas", "pontos"], ascending=[False, False]).reset_index()
opponents.to_csv(OUT / "analise_adversarios.csv", index=False, encoding="utf-8-sig")

if season.empty:
    raise SystemExit("Não foram encontrados jogos do Fluminense no CSV limpo.")

best = season.loc[season["aproveitamento_pct"].idxmax()]
worst = season.loc[season["aproveitamento_pct"].idxmin()]
total_matches = len(flu)
wins, draws, losses = [int(results[k]) for k in ["Vitória", "Empate", "Derrota"]]
points_pct = round(flu["points"].sum() / (total_matches * 3) * 100, 1)
gf, ga = int(flu["flu_goals"].sum()), int(flu["opponent_goals"].sum())
most_played = opponents.iloc[0]
home = venue.loc[venue["venue_type"] == "Casa"].iloc[0]
away = venue.loc[venue["venue_type"] == "Fora"].iloc[0]

report = f"""# Resultados exploratórios FLUDB — gerados a partir da base local

## Escopo
- Partidas do Fluminense analisadas: {total_matches}
- Temporadas encontradas: {int(season['season'].min())}–{int(season['season'].max())}
- Vitórias, empates e derrotas: {wins}, {draws}, {losses}
- Aproveitamento geral: {points_pct}%
- Gols marcados e sofridos: {gf} e {ga} (saldo {gf-ga})

## Principais achados calculados
- Melhor aproveitamento anual: {int(best['season'])}, com {best['aproveitamento_pct']}% ({int(best['partidas'])} partidas).
- Menor aproveitamento anual: {int(worst['season'])}, com {worst['aproveitamento_pct']}% ({int(worst['partidas'])} partidas).
- O adversário mais frequente na base: {most_played['opponent']}, em {int(most_played['partidas'])} partidas.
- Em casa: {int(home['partidas'])} partidas, aproveitamento de {home['aproveitamento_pct']}%.
- Fora: {int(away['partidas'])} partidas, aproveitamento de {away['aproveitamento_pct']}%.

## Cinco eixos de EDA
1. Evolução por temporada: consulte `analise_por_temporada.csv` para partidas, resultados, pontos, aproveitamento, gols e saldo.
2. Distribuição de resultados: {wins} vitórias ({wins/total_matches*100:.1f}%), {draws} empates ({draws/total_matches*100:.1f}%) e {losses} derrotas ({losses/total_matches*100:.1f}%).
3. Gols: {gf} marcados e {ga} sofridos; saldo de {gf-ga}.
4. Mando de campo: consulte `analise_casa_fora.csv`; valores comparados acima.
5. Adversários: consulte `analise_adversarios.csv`; tabela ordenada por número de partidas.

## Observação
As conclusões são descritivas e não demonstram causalidade. As temporadas são agrupadas pelo ano da data da partida, conforme a implementação do projeto.
"""
(OUT / "conclusoes_eda.md").write_text(report, encoding="utf-8")
print(report)
print("\nArquivos gerados em data/processed/:")
print("- analise_por_temporada.csv")
print("- analise_casa_fora.csv")
print("- analise_adversarios.csv")
print("- conclusoes_eda.md")
