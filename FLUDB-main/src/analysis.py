import pandas as pd

def flu_matches(df): return df[(df.home_team == "Fluminense") | (df.away_team == "Fluminense")].copy()

def add_flu_metrics(df):
    x = flu_matches(df)
    x["is_home"] = x.home_team.eq("Fluminense")
    x["flu_goals"] = x.home_goals.where(x.is_home, x.away_goals)
    x["opp_goals"] = x.away_goals.where(x.is_home, x.home_goals)
    x["opponent"] = x.away_team.where(x.is_home, x.home_team)
    x["outcome"] = "Empate"
    x.loc[x.flu_goals > x.opp_goals, "outcome"] = "Vitória"
    x.loc[x.flu_goals < x.opp_goals, "outcome"] = "Derrota"
    x["points"] = x.outcome.map({"Vitória":3,"Empate":1,"Derrota":0})
    x["venue_type"] = x.is_home.map({True:"Casa",False:"Fora"})
    return x

def season_summary(df):
    x = add_flu_metrics(df)
    if x.empty: return pd.DataFrame(columns=["season","matches","wins","draws","losses","points","points_pct","goals_for","goals_against"])
    g = x.groupby("season").agg(matches=("outcome","size"),wins=("outcome",lambda s:(s=="Vitória").sum()),draws=("outcome",lambda s:(s=="Empate").sum()),losses=("outcome",lambda s:(s=="Derrota").sum()),points=("points","sum"),goals_for=("flu_goals","sum"),goals_against=("opp_goals","sum")).reset_index()
    g["points_pct"] = (g.points/(g.matches*3)*100).round(1)
    return g

def opponent_summary(df):
    x = add_flu_metrics(df)
    return x.groupby("opponent").agg(games=("outcome","size"),wins=("outcome",lambda s:(s=="Vitória").sum()),losses=("outcome",lambda s:(s=="Derrota").sum()),points=("points","sum")).sort_values(["games","points"],ascending=[False,False]).reset_index()

def quality_notes(df):
    return {"records":int(len(df)),"seasons":int(df.season.nunique()) if len(df) else 0,"date_min":str(df.date.min().date()) if len(df) else None,"date_max":str(df.date.max().date()) if len(df) else None,"teams":int(pd.concat([df.home_team,df.away_team]).nunique()) if len(df) else 0}
