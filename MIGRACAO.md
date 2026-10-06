# Guia de migração e reprodução das verificações

Este guia complementa o TCC **Versionamento de APIs REST e compatibilidade em sistemas back-end**. Ele identifica as evidências coletadas e os procedimentos para conferir a API e as nove adaptações do cliente de ensaio.

## 1. Evidências e revisão do código

A revisão de partida da API e do cliente v1 foi:

```text
e9d13c1cd4257f133934ab6d1d376a328f3a7d58
```

As atualizações posteriores em `main` disponibilizam documentos e registros. Para conferir o código utilizado no estudo, use a revisão de partida e os commits dos clientes abaixo.

| Arquivo | Data da coleta | Conteúdo | Uso no TCC |
| --- | --- | --- | --- |
| [execucao_validacao_final.csv](results/execucao_validacao_final.csv) | 25/09/2026 | Nove observações automáticas | Tabela 3 |
| [experimento_20260928_112054.csv](results/experimento_20260928_112054.csv) | 28/09/2026 | Nove observações automáticas | Tabela 3 |
| [coleta_manual.csv](results/coleta_manual.csv) | 30/09/2026 | Nove migrações, com ordem, horários, linhas e commits | Tabelas 4 e 5 |
| [coleta_manual_modelo.csv](results/coleta_manual_modelo.csv) | Modelo para novas coletas | Matriz em branco | Não constitui resultado do estudo |

A ficha preenchida é o registro histórico das migrações. Para uma nova coleta, copie o modelo para um arquivo com nome próprio e registre novas medições.

### Migrações preservadas

A ordem apresentada foi extraída da ficha manual. As branches contêm adaptações independentes e cada commit alterou apenas `clients/trial_client.py`.

| Ordem | Estratégia | Cenário | Branch | Commit do cliente |
| --- | --- | --- | --- | --- |
| 1 | url | c1 | [migracao-url-c1](https://github.com/FelipeRoveroni/tcc_api_experimento/tree/migracao-url-c1) | [8b9b2a319b23c46f25e93a2908d2f457135f1c16](https://github.com/FelipeRoveroni/tcc_api_experimento/commit/8b9b2a319b23c46f25e93a2908d2f457135f1c16) |
| 2 | header | c1 | [migracao-header-c1](https://github.com/FelipeRoveroni/tcc_api_experimento/tree/migracao-header-c1) | [4ad305b42562db1b56b29b6cb80a5c4384c7d79e](https://github.com/FelipeRoveroni/tcc_api_experimento/commit/4ad305b42562db1b56b29b6cb80a5c4384c7d79e) |
| 3 | query | c1 | [migracao-query-c1](https://github.com/FelipeRoveroni/tcc_api_experimento/tree/migracao-query-c1) | [1d69b16e294d0f0c1a466065163b9ae13017e947](https://github.com/FelipeRoveroni/tcc_api_experimento/commit/1d69b16e294d0f0c1a466065163b9ae13017e947) |
| 4 | header | c2 | [migracao-header-c2](https://github.com/FelipeRoveroni/tcc_api_experimento/tree/migracao-header-c2) | [ce6d6a3167c6375af7b4958ae6432fbd560fc079](https://github.com/FelipeRoveroni/tcc_api_experimento/commit/ce6d6a3167c6375af7b4958ae6432fbd560fc079) |
| 5 | query | c2 | [migracao-query-c2](https://github.com/FelipeRoveroni/tcc_api_experimento/tree/migracao-query-c2) | [1fdd80a50d1ef363b312ff7725f833ddf896206c](https://github.com/FelipeRoveroni/tcc_api_experimento/commit/1fdd80a50d1ef363b312ff7725f833ddf896206c) |
| 6 | url | c2 | [migracao-url-c2](https://github.com/FelipeRoveroni/tcc_api_experimento/tree/migracao-url-c2) | [7be47babb4f4cc8414f484adeb98adc886892615](https://github.com/FelipeRoveroni/tcc_api_experimento/commit/7be47babb4f4cc8414f484adeb98adc886892615) |
| 7 | query | c3 | [migracao-query-c3](https://github.com/FelipeRoveroni/tcc_api_experimento/tree/migracao-query-c3) | [bf79fa663ebc69b722cf4d773dfeae9d540fcd61](https://github.com/FelipeRoveroni/tcc_api_experimento/commit/bf79fa663ebc69b722cf4d773dfeae9d540fcd61) |
| 8 | url | c3 | [migracao-url-c3](https://github.com/FelipeRoveroni/tcc_api_experimento/tree/migracao-url-c3) | [92e6dbb98d886b925332fba9352f85ca71f47345](https://github.com/FelipeRoveroni/tcc_api_experimento/commit/92e6dbb98d886b925332fba9352f85ca71f47345) |
| 9 | header | c3 | [migracao-header-c3](https://github.com/FelipeRoveroni/tcc_api_experimento/tree/migracao-header-c3) | [ac34f07b5cc65e4f6a2223fc663574f6d4f02ee7](https://github.com/FelipeRoveroni/tcc_api_experimento/commit/ac34f07b5cc65e4f6a2223fc663574f6d4f02ee7) |

## 2. Preparação do ambiente

Clone o repositório público e obtenha as referências:

```bash
git clone https://github.com/FelipeRoveroni/tcc_api_experimento.git
cd tcc_api_experimento
git fetch origin
```

Utilize Python 3.10 ou superior. O inventário informado ao final das migrações registrou Python 3.10.6; as dependências fixadas estão em `requirements.txt`. As execuções automáticas anteriores não registraram todas as dependências, e o inventário final não comprova retrospectivamente esses ambientes.

Os testes utilizaram `TestClient`, que acessa diretamente a aplicação. Não é necessário iniciar um servidor Uvicorn para os comandos de teste deste guia.

## 3. Conferência da revisão inicial

Crie uma árvore de trabalho independente com a revisão de partida:

```bash
git worktree add --detach ../tcc-base-verificacao e9d13c1cd4257f133934ab6d1d376a328f3a7d58
cd ../tcc-base-verificacao
python -m venv .venv
```

Ative o ambiente virtual no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Em Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale as dependências e execute a suíte padrão:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

A coleta original registrou **68 testes aprovados** na suíte padrão da base. Essa suíte inclui verificações do cliente v1. Nas revisões adaptadas, execute a aceitação v2 indicada na próxima seção.

Para observar o estado anterior à adaptação, execute explicitamente:

```bash
python -m pytest -q tests/migration_acceptance.py --strategy url --scenario c1
```

Na base v1, esperam-se três falhas. Os testes comparam primeiro o seletor do cliente com o alvo v2; essa falha ocorre antes da requisição e, isoladamente, não comprova uma rejeição de contrato pela API.

## 4. Conferência de um cliente já adaptado

A partir da pasta do clone principal, crie outra árvore de trabalho para o commit URL/C1:

```bash
git worktree add --detach ../tcc-url-c1-verificacao 8b9b2a319b23c46f25e93a2908d2f457135f1c16
cd ../tcc-url-c1-verificacao
python -m venv .venv
```

Ative o ambiente conforme a seção anterior, instale as dependências e execute:

```bash
python -m pip install -r requirements.txt
python -m pytest -q tests/migration_acceptance.py --strategy url --scenario c1
```

O critério de aceitação é a aprovação conjunta de **três testes**: listagem, consulta por identificador e criação. A criação também é conferida por uma consulta posterior. O estado em memória é reinicializado para cada teste.

Para conferir outra combinação, utilize uma nova pasta de trabalho, o commit correspondente na tabela e os valores `url`, `header` ou `query` em `--strategy`, e `c1`, `c2` ou `c3` em `--scenario`. Cada cliente foi preparado para sua própria combinação; use o cenário e a estratégia associados ao commit.

As nove migrações originais registraram três aprovações cada, totalizando 27 verificações de aceitação. Esse total permanece separado da suíte padrão de 68 testes da base.

## 5. Coleta automática

No ambiente da revisão inicial, gere um arquivo novo, preservando os CSVs históricos:

```bash
python -m experiment.runner --output results/reproducao_nova.csv
```

Escolha um nome diferente para cada execução. A rotina percorre as nove combinações e verifica a listagem legada na v1, o acesso à v2 sem adaptação e a criação com um cliente previamente adaptado. Ela não mede o intervalo de migração do cliente de ensaio.

Na coleta original:

- A listagem na v1 retornou HTTP 200 e passou na validação do contrato em todas as combinações.
- Em C1 e C2, a listagem na v2 retornou HTTP 200, mas não correspondeu ao modelo legado.
- Em C3, a criação sem `categoria` retornou HTTP 422. Nesse caso, o indicador de contrato foi marcado como `False` pelo protocolo, sem validar o corpo de erro como produto v1.
- A criação com o cliente adaptado retornou HTTP 201 e contrato válido em todas as combinações.

O campo `compatibilidade_legado_percentual` foi usado como indicador binário da listagem v1: 100 para sucesso com contrato válido e zero nos demais casos. Ele não representa disponibilidade de toda a API.

## 6. Nova rodada de migração assistida

Para realizar uma nova adaptação, parta da mesma base em uma branch nova. Exemplo URL/C1, executado a partir do clone principal:

```bash
git worktree add -b reproducao-url-c1 ../tcc-nova-url-c1 e9d13c1cd4257f133934ab6d1d376a328f3a7d58
cd ../tcc-nova-url-c1
```

Prepare o ambiente virtual e execute a aceitação antes de modificar o código. Em seguida, adapte somente `clients/trial_client.py`, preservando a API e os testes.

| Cenário | Alteração necessária no cliente |
| --- | --- |
| C1 | Selecionar v2, utilizar o modelo de resposta C1 e substituir `nome` por `descricao` no envio e nas expectativas. |
| C2 | Selecionar v2, utilizar o modelo de resposta C2 e retirar `estoque` do envio e das expectativas. |
| C3 | Selecionar v2, utilizar o modelo de resposta C3 e fornecer `categoria` na criação. |

A seleção da v2 depende da estratégia: caminho `/v2/` em URL; tipo de mídia `application/vnd.tcc.produto.v2+json` em `Accept`; ou `version=2` no parâmetro de consulta.

No PowerShell, registre o início imediatamente antes da adaptação:

```powershell
$inicioMigracao = Get-Date
```

Depois da edição, execute os testes e registre o término apenas após sua aprovação:

```powershell
python -m pytest -q tests/migration_acceptance.py --strategy url --scenario c1
if ($LASTEXITCODE -ne 0) { throw "Os testes de aceitação não foram aprovados." }
$fimMigracao = Get-Date
$inicioMigracao.ToString("o")
$fimMigracao.ToString("o")
($fimMigracao - $inicioMigracao).TotalMinutes
```

Confira as alterações, registre o commit do cliente e preencha uma cópia do modelo de coleta:

```bash
git diff --numstat e9d13c1cd4257f133934ab6d1d376a328f3a7d58 -- clients/trial_client.py
git diff --check
git add clients/trial_client.py
git commit -m "Registra nova migração URL/C1"
git rev-parse HEAD
python --version
python -m pip freeze
```

Registre a ordem, os marcos de tempo, a quantidade de arquivos, as linhas adicionadas e removidas, a revisão da API e o commit do cliente. Documente também a assistência utilizada e os resultados dos testes. Preserve as saídas e o inventário do ambiente em arquivos próprios da nova rodada.

Para comparar um commit já concluído com a base, use:

```bash
git diff --numstat e9d13c1cd4257f133934ab6d1d376a328f3a7d58 8b9b2a319b23c46f25e93a2908d2f457135f1c16 -- clients/trial_client.py
```

A soma de linhas adicionadas e removidas descreve alteração textual, incluindo comentários e formatação. Os intervalos originais abrangeram adaptação assistida, validação e pausas entre comandos; não foram medidas de latência da API. Uma única migração por combinação não permitiu estabelecer superioridade de esforço entre estratégias.

Uma reprodução gera novas verificações e novos intervalos. Os horários e as medidas históricas dos CSVs devem continuar associados às execuções originais.
