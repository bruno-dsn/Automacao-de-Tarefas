from __future__ import annotations

from dataclasses import dataclass
import re

import numpy as np
import pandas as pd

from src.data import COLUNAS


COLUNAS_OBRIGATORIAS = [
    "codigo",
    "produto",
    "categoria",
    "marca",
    "preco_venda",
    "custo_unitario",
    "estoque",
    "fornecedor",
]

COLUNAS_TEXTO = ["codigo", "produto", "categoria", "marca", "fornecedor", "observacao"]
COLUNAS_NUMERICAS = ["preco_venda", "custo_unitario", "estoque"]
PADRAO_CODIGO = re.compile(r"^[A-Z0-9]{3,6}-[A-Z0-9]{3,8}$")


@dataclass
class ResultadoValidacao:
    dados: pd.DataFrame
    ocorrencias: pd.DataFrame

    @property
    def erros(self) -> pd.DataFrame:
        return self.ocorrencias[self.ocorrencias["severidade"] == "Erro"].copy()

    @property
    def avisos(self) -> pd.DataFrame:
        return self.ocorrencias[self.ocorrencias["severidade"] == "Aviso"].copy()

    @property
    def linhas_bloqueadas(self) -> int:
        return int(self.erros["linha"].nunique()) if not self.erros.empty else 0

    @property
    def score_qualidade(self) -> float:
        if self.dados.empty:
            return 0.0
        linhas_com_ocorrencia = self.ocorrencias["linha"].nunique()
        return max(0.0, 100 * (1 - linhas_com_ocorrencia / len(self.dados)))


def _ocorrencia(
    linha: int,
    codigo: str,
    campo: str,
    tipo: str,
    mensagem: str,
    severidade: str = "Erro",
) -> dict[str, object]:
    return {
        "linha": linha,
        "codigo": codigo,
        "campo": campo,
        "tipo": tipo,
        "mensagem": mensagem,
        "severidade": severidade,
    }


def _preparar_colunas(dados: pd.DataFrame) -> pd.DataFrame:
    faltantes = sorted(set(COLUNAS_OBRIGATORIAS) - set(dados.columns))
    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(faltantes)}")

    produtos = dados.copy().reset_index(drop=True)
    if "observacao" not in produtos.columns:
        produtos["observacao"] = ""
    produtos = produtos[COLUNAS].copy()
    produtos.insert(0, "linha_origem", produtos.index + 2)

    for coluna in COLUNAS_TEXTO:
        produtos[coluna] = produtos[coluna].fillna("").astype(str).str.strip()
    for coluna in COLUNAS_NUMERICAS:
        produtos[coluna] = pd.to_numeric(produtos[coluna], errors="coerce")
    return produtos


def validar_catalogo(dados: pd.DataFrame) -> ResultadoValidacao:
    produtos = _preparar_colunas(dados)
    ocorrencias: list[dict[str, object]] = []
    duplicados = produtos["codigo"].duplicated(keep=False)

    for indice, produto in produtos.iterrows():
        linha = int(produto["linha_origem"])
        codigo = str(produto["codigo"])

        for campo in ["codigo", "produto", "categoria", "marca", "fornecedor"]:
            if not produto[campo]:
                ocorrencias.append(
                    _ocorrencia(linha, codigo, campo, "Campo vazio", "Preencha o campo obrigatório.")
                )

        if codigo and not PADRAO_CODIGO.fullmatch(codigo):
            ocorrencias.append(
                _ocorrencia(
                    linha,
                    codigo,
                    "codigo",
                    "Formato inválido",
                    "Use letras e números no formato ABC-0001.",
                )
            )
        if codigo and bool(duplicados.iloc[indice]):
            ocorrencias.append(
                _ocorrencia(linha, codigo, "codigo", "Duplicidade", "O código deve ser único.")
            )

        preco = produto["preco_venda"]
        custo = produto["custo_unitario"]
        estoque = produto["estoque"]
        if pd.isna(preco) or preco <= 0:
            ocorrencias.append(
                _ocorrencia(linha, codigo, "preco_venda", "Valor inválido", "Informe um preço maior que zero.")
            )
        if pd.isna(custo) or custo < 0:
            ocorrencias.append(
                _ocorrencia(linha, codigo, "custo_unitario", "Valor inválido", "Informe um custo igual ou maior que zero.")
            )
        if not pd.isna(preco) and not pd.isna(custo) and preco > 0 and custo > preco:
            ocorrencias.append(
                _ocorrencia(
                    linha,
                    codigo,
                    "custo_unitario",
                    "Margem negativa",
                    "O custo não pode superar o preço de venda neste fluxo.",
                )
            )
        if pd.isna(estoque) or estoque < 0 or (not pd.isna(estoque) and not float(estoque).is_integer()):
            ocorrencias.append(
                _ocorrencia(linha, codigo, "estoque", "Valor inválido", "Informe uma quantidade inteira igual ou maior que zero.")
            )

        if not pd.isna(preco) and not pd.isna(custo) and preco > 0 and 0 <= custo <= preco:
            margem = (preco - custo) / preco
            if margem < 0.20:
                ocorrencias.append(
                    _ocorrencia(
                        linha,
                        codigo,
                        "custo_unitario",
                        "Margem baixa",
                        "A margem bruta está abaixo de 20%.",
                        "Aviso",
                    )
                )

    validos_para_outlier = produtos[
        produtos["preco_venda"].notna() & produtos["categoria"].ne("")
    ]
    for _, grupo in validos_para_outlier.groupby("categoria"):
        if len(grupo) < 8:
            continue
        q1 = grupo["preco_venda"].quantile(0.25)
        q3 = grupo["preco_venda"].quantile(0.75)
        limite = q3 + 1.5 * (q3 - q1)
        for _, produto in grupo[grupo["preco_venda"] > limite].iterrows():
            ocorrencias.append(
                _ocorrencia(
                    int(produto["linha_origem"]),
                    str(produto["codigo"]),
                    "preco_venda",
                    "Preço fora do padrão",
                    "Revise o preço, pois ele está acima da faixa usual da categoria.",
                    "Aviso",
                )
            )

    tabela = pd.DataFrame(
        ocorrencias,
        columns=["linha", "codigo", "campo", "tipo", "mensagem", "severidade"],
    )
    linhas_erro = set(tabela.loc[tabela["severidade"] == "Erro", "linha"]) if not tabela.empty else set()
    linhas_aviso = set(tabela.loc[tabela["severidade"] == "Aviso", "linha"]) if not tabela.empty else set()

    def status(linha: int) -> str:
        if linha in linhas_erro:
            return "Bloqueado"
        if linha in linhas_aviso:
            return "Revisar"
        return "Pronto"

    produtos["status_validacao"] = produtos["linha_origem"].map(status)
    produtos["margem_bruta"] = produtos["preco_venda"] - produtos["custo_unitario"]
    produtos["margem_bruta_pct"] = np.where(
        produtos["preco_venda"] > 0,
        produtos["margem_bruta"] / produtos["preco_venda"],
        np.nan,
    )
    produtos["valor_estoque_venda"] = produtos["preco_venda"] * produtos["estoque"]
    return ResultadoValidacao(produtos, tabela)
