from __future__ import annotations

import numpy as np
import pandas as pd


def simular_execucao(
    produtos: pd.DataFrame,
    taxa_sucesso: float = 0.98,
    segundos_por_item: float = 2.5,
    semente: int = 42,
) -> pd.DataFrame:
    """Gera um log fictício para estudar a operação sem abrir o navegador."""
    if not 0 <= taxa_sucesso <= 1:
        raise ValueError("A taxa de sucesso deve estar entre 0 e 1.")
    rng = np.random.default_rng(semente)
    resultados = rng.random(len(produtos)) < taxa_sucesso
    duracoes = np.clip(
        rng.normal(segundos_por_item, max(0.15, segundos_por_item * 0.18), len(produtos)),
        0.2,
        None,
    )
    log = produtos[["codigo", "produto", "categoria", "marca"]].copy().reset_index(drop=True)
    log["status_execucao"] = np.where(resultados, "Concluído", "Falha simulada")
    log["duracao_segundos"] = duracoes.round(2)
    log["mensagem"] = np.where(
        resultados,
        "Cadastro simulado com sucesso.",
        "Falha fictícia para demonstrar o tratamento de exceções.",
    )
    log.insert(0, "ordem", np.arange(1, len(log) + 1))
    return log


def resumir_execucao(log: pd.DataFrame) -> dict[str, float | int]:
    total = len(log)
    concluidos = int(log["status_execucao"].eq("Concluído").sum())
    return {
        "total": total,
        "concluidos": concluidos,
        "falhas": total - concluidos,
        "taxa_sucesso": concluidos / total if total else 0.0,
        "duracao_total_seg": float(log["duracao_segundos"].sum()),
        "duracao_media_seg": float(log["duracao_segundos"].mean()) if total else 0.0,
    }
