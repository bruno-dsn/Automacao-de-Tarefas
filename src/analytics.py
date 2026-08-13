from __future__ import annotations

import pandas as pd


def catalogo_liberado(dados: pd.DataFrame) -> pd.DataFrame:
    return dados[dados["status_validacao"].ne("Bloqueado")].copy()


def resumir_catalogo(dados: pd.DataFrame) -> dict[str, float | int]:
    liberados = catalogo_liberado(dados)
    return {
        "produtos": len(dados),
        "liberados": len(liberados),
        "bloqueados": int(dados["status_validacao"].eq("Bloqueado").sum()),
        "revisar": int(dados["status_validacao"].eq("Revisar").sum()),
        "categorias": int(liberados["categoria"].nunique()),
        "marcas": int(liberados["marca"].nunique()),
        "valor_estoque": float(liberados["valor_estoque_venda"].sum()),
        "margem_mediana": float(liberados["margem_bruta_pct"].median()),
    }


def resumir_categoria(dados: pd.DataFrame) -> pd.DataFrame:
    liberados = catalogo_liberado(dados)
    return (
        liberados.groupby("categoria", dropna=False)
        .agg(
            produtos=("codigo", "count"),
            estoque=("estoque", "sum"),
            valor_estoque=("valor_estoque_venda", "sum"),
            preco_mediano=("preco_venda", "median"),
            margem_mediana=("margem_bruta_pct", "median"),
        )
        .reset_index()
        .sort_values("valor_estoque", ascending=False)
    )


def estimar_tempo(
    quantidade: int,
    segundos_manual: float,
    segundos_automacao: float,
) -> dict[str, float]:
    tempo_manual = quantidade * segundos_manual
    tempo_automacao = quantidade * segundos_automacao
    economia = max(0.0, tempo_manual - tempo_automacao)
    reducao = economia / tempo_manual if tempo_manual else 0.0
    return {
        "tempo_manual_min": tempo_manual / 60,
        "tempo_automacao_min": tempo_automacao / 60,
        "economia_min": economia / 60,
        "reducao_pct": reducao,
    }
