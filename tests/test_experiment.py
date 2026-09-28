from experiment.runner import execute


def test_experiment_generates_one_row_per_combination():
    rows = execute()

    assert len(rows) == 9
    assert {(row["estrategia"], row["cenario"]) for row in rows} == {
        (strategy, scenario)
        for strategy in ("url", "header", "query")
        for scenario in ("c1", "c2", "c3")
    }
    assert all(row["legado_v1_contrato_valido"] for row in rows)
    assert all(row["adaptado_v2_contrato_valido"] for row in rows)
    assert all(row["compatibilidade_legado_percentual"] == 100.0 for row in rows)
    assert sum(int(row["falhas_explicitas"]) for row in rows) == 3
    assert sum(int(row["erros_silenciosos"]) for row in rows) == 6
