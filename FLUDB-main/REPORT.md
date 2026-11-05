# Relatório acadêmico — FLUDB

## 1. Objetivo
Analisar exploratoriamente o desempenho do Fluminense no Campeonato Brasileiro, utilizando limpeza de dados, estatística descritiva e visualização interativa.

## 2. Fonte e escopo
A base utilizada é o dataset público de partidas do Campeonato Brasileiro, mantido em [adaoduque/Brasileirao_Dataset](https://github.com/adaoduque/Brasileirao_Dataset). O arquivo é baixado pelo script `scripts/download_data.py`. O período e a quantidade de linhas devem ser extraídos do arquivo `data/processed/quality_report.json` após a execução; não foram fixados aqui para evitar declarar números sem conferir a versão atual da fonte.

## 3. Metodologia e preparação
O processo importa o CSV, normaliza cabeçalhos, converte datas e placares para os tipos esperados e padroniza o nome Fluminense. Duplicatas exatas são identificadas e removidas. Registros sem data, equipes ou placares válidos, além de placares negativos ou não inteiros, são excluídos da amostra analítica. O pipeline grava o dataset tratado e um relatório de qualidade para permitir auditoria.

## 4. Qualidade dos dados
Após executar `python scripts/prepare_data.py`, consultar `quality_report.json` e reportar: total bruto, duplicatas, registros inválidos, total final e ausências por coluna. Evite interpretar ausências de colunas não utilizadas como se invalidassem todas as partidas.

## 5. Análise exploratória (cinco eixos)
1. **Evolução por temporada:** comparar partidas, pontos e aproveitamento do Fluminense.
2. **Resultados:** contabilizar vitórias, empates e derrotas.
3. **Gols:** comparar gols marcados e sofridos.
4. **Mando de campo:** comparar resultados como mandante e visitante.
5. **Adversários:** identificar frequência de confrontos e balanço de vitórias/derrotas.

Os valores específicos devem ser transcritos das tabelas calculadas e das visualizações do dashboard depois de executar o pipeline. Não se deve inventar valores nem inferir causalidade a partir de estatísticas descritivas.

## 6. Dashboard
O app Streamlit apresenta três KPIs (partidas, aproveitamento e distribuição de resultados), quatro gráficos e filtro por temporada. Execute `streamlit run app.py` e registre capturas de tela para anexar ao trabalho.

## 7. Conclusões
Preencher com os padrões efetivamente observados na tabela por temporada e nos gráficos: temporadas de melhor/pior aproveitamento, balanço de gols e diferenças entre casa/fora. Relacione cada afirmação a um resultado calculado.

## 8. Limitações
A base contém resultados de partidas e placares, não estatísticas individuais completas ou evidência tática. Alterações históricas e padronização de nomes na fonte podem afetar comparações. Os resultados são descritivos, não causais.

## 9. Reprodutibilidade
Python 3.10+; dependências em `requirements.txt`. Recriação: `python scripts/download_data.py`, `python scripts/prepare_data.py` e `streamlit run app.py`.
