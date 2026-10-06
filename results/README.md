# Resultados do TCC

Esta pasta reúne as evidências utilizadas em **Versionamento de APIs REST e compatibilidade em sistemas back-end**.

| Arquivo | Data | Registros | Uso |
| --- | --- | --- | --- |
| [execucao_validacao_final.csv](execucao_validacao_final.csv) | 25/09/2026 | 9 combinações automáticas | Tabela 3 |
| [experimento_20260928_112054.csv](experimento_20260928_112054.csv) | 28/09/2026 | 9 combinações automáticas | Tabela 3 |
| [coleta_manual.csv](coleta_manual.csv) | 30/09/2026 | 9 migrações assistidas | Tabelas 4 e 5 |
| [coleta_manual_modelo.csv](coleta_manual_modelo.csv) | Modelo em branco | 9 linhas para novas medições | Formulário de apoio |

## Interpretação dos registros

Os arquivos automáticos registram o cliente legado na v1, o acesso à v2 sem adaptação e a criação com um cliente previamente adaptado. Em C3, o indicador de contrato do acesso legado à v2 foi marcado como `False` pelo protocolo após a rejeição HTTP 422; o corpo de erro não foi validado como produto v1.

A ficha manual contém ordem de execução, marcos de início e término, arquivos e linhas modificados, intervalo em minutos, revisão da API, commit do cliente e observações sobre a assistência e os testes. Os segundos da Tabela 4 correspondem à diferença entre os marcos. A Tabela 5 soma as linhas adicionadas e removidas, incluindo comentários e formatação.

As duas execuções automáticas não constituem novas migrações independentes. Os intervalos das nove adaptações assistidas não permitem classificar uma estratégia como superior em esforço.

## Reprodução

Consulte [MIGRACAO.md](../MIGRACAO.md) para a revisão inicial, os commits das nove adaptações e os comandos.

Copie o modelo em branco para um arquivo com nome próprio ao realizar novas migrações. Preserve os CSVs históricos e registre, em cada nova rodada, a data, as revisões do código, o ambiente e as saídas dos testes. A rotina `python -m experiment.runner` gera novos CSVs automáticos; use um nome distinto para cada execução.
