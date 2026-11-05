from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from src.analysis import add_flu_metrics, season_summary, opponent_summary, quality_notes

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data/processed/brasileirao_clean.csv"
st.set_page_config(page_title="FLUDB | Fluminense",page_icon="⚽",layout="wide")
st.markdown("<style>.stApp{background:#111820;color:#e8edf2}[data-testid='stMetric']{background:#1b2632;border:1px solid #344252;padding:12px;border-radius:10px}h1,h2,h3{color:#f2f5f8}</style>",unsafe_allow_html=True)
st.title("FLUDB")
st.caption("Fluminense Football Database • Campeonato Brasileiro • EDA")
if not DATA.exists():
    st.warning("Dataset não encontrado. Execute no terminal: `python scripts/download_data.py` e depois `python scripts/prepare_data.py`.")
    st.stop()
df=pd.read_csv(DATA,parse_dates=["date"])
seasons=sorted(df.season.dropna().astype(int).unique())
selected=st.sidebar.multiselect("Temporadas",seasons,default=seasons)
filtered=df[df.season.isin(selected)]
flu=add_flu_metrics(filtered)
if flu.empty: st.info("Não há jogos do Fluminense no filtro."); st.stop()
n=len(flu); wins=int((flu.outcome=="Vitória").sum()); draws=int((flu.outcome=="Empate").sum()); losses=int((flu.outcome=="Derrota").sum()); pct=flu.points.sum()/(n*3)*100
c1,c2,c3=st.columns(3); c1.metric("Partidas",f"{n:,}"); c2.metric("Aproveitamento",f"{pct:.1f}%"); c3.metric("Vitórias • Empates • Derrotas",f"{wins} • {draws} • {losses}")
season=season_summary(filtered)
a,b=st.columns(2)
with a:
 st.subheader("1. Pontos por temporada"); fig,ax=plt.subplots(); ax.plot(season.season,season.points,marker="o"); ax.set_xlabel("Temporada"); ax.set_ylabel("Pontos"); ax.grid(alpha=.2); st.pyplot(fig); plt.close(fig)
with b:
 st.subheader("2. Gols marcados e sofridos"); fig,ax=plt.subplots(); ax.bar(["Marcados","Sofridos"],[flu.flu_goals.sum(),flu.opp_goals.sum()]); ax.set_ylabel("Gols"); st.pyplot(fig); plt.close(fig)
a,b=st.columns(2)
with a:
 st.subheader("3. Resultados em casa e fora"); p=flu.groupby(["venue_type","outcome"]).size().unstack(fill_value=0).reindex(index=["Casa","Fora"],columns=["Vitória","Empate","Derrota"],fill_value=0); fig,ax=plt.subplots(); p.plot(kind="bar",ax=ax); ax.set_xlabel(""); ax.set_ylabel("Partidas"); st.pyplot(fig); plt.close(fig)
with b:
 st.subheader("4. Adversários mais enfrentados"); opp=opponent_summary(filtered).head(10).sort_values("games"); fig,ax=plt.subplots(); ax.barh(opp.opponent,opp.games); ax.set_xlabel("Partidas"); st.pyplot(fig); plt.close(fig)
st.subheader("Análises exploratórias")
st.markdown("- Evolução de pontos e aproveitamento por temporada.\n- Distribuição de vitórias, empates e derrotas.\n- Gols pró e contra.\n- Diferença entre mandante e visitante.\n- Frequência de confrontos e resultados por adversário.")
st.dataframe(season,use_container_width=True,hide_index=True)
with st.expander("Metadados da amostra selecionada"): st.json(quality_notes(filtered))
