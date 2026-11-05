# Relatório acadêmico — FLUDB

## 1. Objetivo

Analisar exploratoriamente o desempenho do Fluminense no Campeonato Brasileiro, utilizando técnicas de limpeza de dados, estatística descritiva e visualização interativa. O projeto busca transformar os registros das partidas em informações que permitam compreender o desempenho da equipe ao longo do período analisado.

## 2. Fonte e escopo

A base utilizada é o dataset público de partidas do Campeonato Brasileiro, mantido em [adaoduque/Brasileirao_Dataset](https://github.com/adaoduque/Brasileirao_Dataset). O arquivo é baixado pelo script `scripts/download_data.py`.

A base bruta contém 8.785 registros. A análise específica do Fluminense considera 856 partidas, agrupadas pelo ano da data do jogo, no período de 2003 a 2024.

## 3. Metodologia e preparação

O processo importa o CSV, normaliza os cabeçalhos, converte datas e placares para os tipos esperados e padroniza o nome do Fluminense. Duplicatas exatas são identificadas e removidas.

Registros sem data, equipes ou placares válidos, além de placares negativos ou não inteiros, são excluídos da amostra analítica. O pipeline grava o dataset tratado e um relatório de qualidade para permitir a auditoria e a reprodução do processo.

A análise exploratória considera os resultados das partidas, os gols marcados e sofridos, o aproveitamento por ano, o mando de campo e os adversários enfrentados.

## 4. Qualidade dos dados

Após a execução de `python scripts/prepare_data.py`, foram obtidos os seguintes resultados:

| Indicador | Resultado |
|---|---:|
| Total de registros brutos | 8.785 |
| Duplicatas exatas removidas | 0 |
| Registros inválidos removidos | 0 |
| Total após limpeza | 8.785 |
| Partidas do Fluminense analisadas | 856 |

A verificação de valores ausentes identificou lacunas em informações complementares. Foram encontrados 4.975 valores ausentes nas colunas de formação do mandante e visitante, e 4.610 nas colunas de técnico do mandante e visitante.

Essas colunas não são essenciais para a análise dos resultados e dos placares. Os campos utilizados como requisitos da análise foram preservados, permitindo manter os registros disponíveis.

O relatório de qualidade foi armazenado em `data/processed/quality_report.json`.

## 5. Análise exploratória (cinco eixos)

### 5.1 Evolução por temporada

A análise por ano identificou variações no aproveitamento do Fluminense ao longo do período estudado.

O maior aproveitamento foi registrado em 2012, com 67,5% em 38 partidas. O menor aproveitamento ocorreu em 2003, com 36,2% em 46 partidas.

Esses resultados demonstram diferenças de desempenho entre os anos analisados. A comparação pode ser aprofundada pela tabela `analise_por_temporada.csv`, que contém partidas, vitórias, empates, derrotas, pontos, gols marcados, gols sofridos e aproveitamento.

### 5.2 Distribuição dos resultados

Nas 856 partidas analisadas, o Fluminense obteve:

| Resultado | Quantidade | Percentual |
|---|---:|---:|
| Vitórias | 334 | 39,0% |
| Empates | 223 | 26,1% |
| Derrotas | 299 | 34,9% |

O aproveitamento geral foi de 47,7%. As vitórias foram o resultado mais frequente, seguidas pelas derrotas e pelos empates.

### 5.3 Gols marcados e sofridos

No período analisado, o Fluminense marcou 1.131 gols e sofreu 1.071 gols, resultando em um saldo positivo de 60 gols.

A comparação entre gols marcados e sofridos complementa a análise dos resultados e permite observar o desempenho ofensivo e defensivo da equipe no recorte estudado.

### 5.4 Mando de campo

A comparação entre partidas como mandante e visitante revelou diferenças no aproveitamento.

| Local | Partidas | Aproveitamento |
|---|---:|---:|
| Casa | 428 | 58,8% |
| Fora | 428 | 36,6% |

O aproveitamento como mandante foi 22,2 pontos percentuais superior ao obtido como visitante. Esse resultado indica que a equipe apresentou desempenho melhor nos jogos em casa, dentro da amostra analisada.

A análise é descritiva e não determina, isoladamente, as causas dessa diferença.

### 5.5 Adversários

A análise da frequência de confrontos identificou o São Paulo como o adversário mais frequente na base, com 44 partidas.

O arquivo `analise_adversarios.csv` permite aprofundar a comparação entre os adversários, considerando a quantidade de partidas, vitórias, empates, derrotas e pontos obtidos.

## 6. Dashboard

O aplicativo desenvolvido com Streamlit apresenta três indicadores principais: partidas analisadas, aproveitamento e distribuição de resultados. O dashboard também contém quatro gráficos e um filtro por temporada.

O aplicativo pode ser executado com o comando:

`streamlit run app.py`

Foram realizadas capturas de tela do dashboard para demonstrar a visualização dos indicadores e gráficos.

## 7. Conclusões

O projeto FLUDB possibilitou a aplicação de técnicas de processamento, limpeza e análise exploratória de dados utilizando Python e Pandas, além da construção de um dashboard interativo com Streamlit.

A análise de 856 partidas do Fluminense entre 2003 e 2024 identificou um aproveitamento geral de 47,7%, com 334 vitórias, 223 empates e 299 derrotas. O saldo de gols foi positivo em 60 gols.

A comparação entre os anos destacou 2012 como o melhor período em aproveitamento, com 67,5%, enquanto 2003 apresentou o menor valor, de 36,2%. A análise do mando de campo revelou uma diferença de 22,2 pontos percentuais entre o desempenho em casa e fora.

Os resultados mostram como a análise de dados pode transformar registros esportivos em informações compreensíveis e apoiar a interpretação do desempenho de uma equipe. As conclusões são descritivas e se limitam ao conjunto de partidas analisado.

8. Limitações
A base contém resultados de partidas e placares, mas não apresenta estatísticas individuais completas ou evidências táticas suficientes para explicar as causas dos resultados. Alterações históricas nas equipes, nos treinadores, nos elencos e nas condições de competição também não foram incorporadas ao estudo.

Além disso, a análise considera o período de 2003 a 2024, de modo que suas conclusões não devem ser generalizadas para temporadas anteriores ou posteriores. Os indicadores utilizados — vitórias, empates, derrotas, gols marcados e sofridos — permitem identificar padrões de desempenho, mas não estabelecem relações causais.

Outro aspecto importante é que o desempenho do Fluminense pode ser influenciado por fatores não contemplados na base, como lesões, calendário de jogos, decisões de arbitragem e mudanças na estratégia das equipes. Portanto, os resultados devem ser interpretados como uma análise descritiva do desempenho histórico, e não como uma explicação definitiva dos fatores que determinaram cada resultado.

Por fim, a qualidade das conclusões depende da consistência e da completude dos dados disponíveis. A inclusão futura de informações sobre jogadores, escalações, posse de bola, finalizações e outros indicadores poderia ampliar a profundidade da análise e permitir novas investigações.

A base contém resultados de partidas e placares, mas não apresenta estatísticas individuais completas ou evidências táticas suficientes para explicar as causas dos resultados.

Alterações histó
