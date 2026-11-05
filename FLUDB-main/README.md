# FLUDB — Fluminense Football Database

Projeto acadêmico de análise exploratória (EDA) do Fluminense no Campeonato Brasileiro. O projeto baixa, limpa e documenta uma base histórica de partidas, gera indicadores e apresenta um dashboard interativo em Streamlit.

## Fonte dos dados
- Repositório: [Brasileirao Dataset — Adão Duque](https://github.com/adaoduque/Brasileirao_Dataset)
- CSV: [campeonato-brasileiro-full.csv](https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/master/campeonato-brasileiro-full.csv)
- O pipeline baixa a fonte no momento da execução. Os números finais (linhas, período, ausências e conclusões) são calculados e registrados, não inventados.

## Estrutura
```text
FLUDB/
├── app.py
├── requirements.txt
├── data/{raw,processed}/
├── scripts/{download_data,prepare_data}.py
├── src/{cleaning,analysis}.py
└── REPORT.md
```

## Executar localmente (Windows)
1. Instale Python 3.10 ou superior.
2. Baixe/clique em **Code → Download ZIP**, extraia e abra a pasta no VS Code.
3. No terminal da pasta:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/download_data.py
python scripts/prepare_data.py
streamlit run app.py
```

## Pipeline e qualidade
- Download da fonte pública e preservação do CSV bruto.
- Normalização de cabeçalhos, texto, nomes de clubes, data e placar.
- Identificação e remoção de duplicatas exatas.
- Registros sem data, clubes ou placar válido ficam fora do conjunto analítico; a contagem é registrada no relatório JSON.
- Exporta `data/processed/brasileirao_clean.csv` e `quality_report.json`.

## EDA (5 eixos)
1. Evolução por temporada (partidas, pontos e aproveitamento).
2. Vitórias, empates e derrotas.
3. Gols feitos e sofridos.
4. Desempenho como mandante e visitante.
5. Frequência e resultados por adversário.

## Dashboard
Quatro gráficos e três KPIs principais, com filtro de temporada. O dashboard requer que o pipeline tenha sido executado. Os gráficos são descritivos e não atribuem causalidade.

## Relatório
O `REPORT.md` é um relatório reproduzível: após rodar a preparação, copie os valores gerados no JSON/CSV para os espaços marcados. Não use valores hipotéticos como resultados reais. Inclua capturas de tela do dashboard na entrega acadêmica.

## Limitações
A base é centrada em partidas e placares; não sustenta conclusões sobre métricas individuais de jogadores, tática ou causalidade. A cobertura e consistência devem ser avaliadas pelo relatório de qualidade.

## Licença e atribuição
Consulte a licença e os termos da fonte original antes de redistribuir os dados. O repositório contém código e instruções, não a cópia do dataset bruto.