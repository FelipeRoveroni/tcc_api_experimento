# Experimento de versionamento de APIs REST

Projeto experimental do TCC **Versionamento de APIs REST e compatibilidade em
sistemas back-end**. A aplicação compara três mecanismos de seleção de versão:

- versão no caminho da URL;
- negociação pelo cabeçalho HTTP `Accept`;
- parâmetro de consulta `version`.

O recurso avaliado é `Produto`. A v1 possui `nome`, `preco` e `estoque`. A v2 é
executada isoladamente em três cenários:

| Cenário | Alteração disruptiva |
| --- | --- |
| C1 | `nome` é renomeado para `descricao` |
| C2 | `estoque` é removido |
| C3 | `categoria` passa a ser obrigatória |

## Execução local

Requer Python 3.10 ou superior.

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

No Linux ou macOS:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

A documentação interativa estará em `http://localhost:8000/docs`.

## Execução com Docker

```bash
docker compose up --build api
```

## Testes automatizados

Localmente:

```bash
pytest -q
```

Com Docker:

```bash
docker compose --profile test run --rm tests
```

## Coleta dos resultados

```bash
python -m experiment.runner
```

Ou com Docker:

```bash
docker compose --profile experiment run --rm experiment
```

O comando gera um CSV em `results/` com uma linha para cada combinação de
estratégia e cenário. Ele registra:

- funcionamento do cliente legado selecionando corretamente a v1;
- comportamento do cliente legado quando direcionado à v2 sem adaptação;
- falhas explícitas e erros silenciosos;
- validação do cliente adaptado à v2;
- taxa de compatibilidade do cliente legado.

Tempo de adaptação, quantidade de arquivos e linhas modificadas devem ser
registrados durante a alteração real do cliente, pois esses valores dependem da
execução humana e não devem ser inventados. Use o arquivo
`results/coleta_manual.csv` para preencher essas métricas durante cada adaptação.

Para realizar as nove migrações partindo de um cliente v1 independente e
comprovar separadamente listagem, consulta por ID e criação na v2, siga
[MIGRACAO.md](MIGRACAO.md). O `experiment.runner` não substitui essas rodadas.

Antes de cada rodada, registre a ordem de execução. Depois dos testes, preserve:

- o CSV automático e a ficha manual preenchida;
- a saída do `pytest -q`;
- o identificador do commit usado na API e no cliente;
- as versões obtidas com `python --version` e `python -m pip freeze`;
- eventuais logs ou capturas que expliquem falhas e erros silenciosos.

## Exemplos de seleção da versão

URL:

```text
GET /api/url/c1/v1/produtos
GET /api/url/c1/v2/produtos
```

Cabeçalho:

```text
GET /api/header/c1/produtos
Accept: application/vnd.tcc.produto.v1+json
```

Parâmetro:

```text
GET /api/query/c1/produtos?version=1
```

O endpoint `/health` informa as estratégias, os cenários e as versões
disponíveis.
