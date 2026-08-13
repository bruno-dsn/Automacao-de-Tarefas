from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


COLUNAS = [
    "codigo",
    "produto",
    "categoria",
    "marca",
    "preco_venda",
    "custo_unitario",
    "estoque",
    "fornecedor",
    "observacao",
]

CATEGORIAS = {
    "Informática": ["Teclado", "Mouse", "Webcam", "Hub USB", "Suporte para notebook"],
    "Eletrônicos": ["Caixa de som", "Fone sem fio", "Carregador", "Cabo USB", "Smartwatch"],
    "Casa e Cozinha": ["Panela", "Jogo de copos", "Organizador", "Luminária", "Garrafa térmica"],
    "Beleza": ["Secador", "Escova", "Kit de cuidados", "Aparador", "Espelho"],
    "Esporte": ["Corda", "Colchonete", "Halter", "Garrafa", "Faixa elástica"],
    "Livros": ["Livro técnico", "Romance", "Biografia", "Livro infantil", "Guia prático"],
    "Papelaria": ["Caderno", "Caneta", "Marcador", "Estojo", "Agenda"],
    "Brinquedos": ["Jogo educativo", "Quebra-cabeça", "Blocos", "Boneco", "Kit criativo"],
    "Moda": ["Camiseta", "Mochila", "Boné", "Carteira", "Meia"],
    "Pet": ["Brinquedo pet", "Comedouro", "Coleira", "Cama pet", "Kit de higiene"],
    "Ferramentas": ["Jogo de chaves", "Trena", "Alicate", "Lanterna", "Organizador"],
    "Automotivo": ["Suporte veicular", "Carregador veicular", "Organizador", "Kit de limpeza", "Capa protetora"],
}

MARCAS = [
    "Alva",
    "Atlas",
    "Brisa",
    "Fluxo",
    "Horizonte",
    "Lume",
    "Nexo",
    "Orbe",
    "Ponto",
    "Prisma",
    "Raiz",
    "Terra",
    "Vértice",
    "Viva",
]

FORNECEDORES = [
    "Distribuidora Norte",
    "Central Sudeste",
    "Comercial Sul",
    "Hub Nordeste",
    "Parceiro Centro-Oeste",
]

PRECO_BASE = {
    "Informática": 180,
    "Eletrônicos": 240,
    "Casa e Cozinha": 120,
    "Beleza": 95,
    "Esporte": 85,
    "Livros": 58,
    "Papelaria": 32,
    "Brinquedos": 78,
    "Moda": 72,
    "Pet": 68,
    "Ferramentas": 110,
    "Automotivo": 92,
}


def gerar_catalogo_sintetico(
    quantidade: int = 600,
    semente: int = 42,
) -> pd.DataFrame:
    """Gera um catálogo fictício e reproduzível para o projeto."""
    rng = np.random.default_rng(semente)
    categorias = list(CATEGORIAS)
    probabilidades = np.array([0.12, 0.11, 0.10, 0.07, 0.08, 0.07, 0.08, 0.08, 0.09, 0.07, 0.07, 0.06])
    categoria = rng.choice(categorias, quantidade, p=probabilidades)

    registros: list[dict[str, object]] = []
    contadores = {nome: 0 for nome in categorias}
    prefixos = {
        "Informática": "INF",
        "Eletrônicos": "ELE",
        "Casa e Cozinha": "CAS",
        "Beleza": "BEL",
        "Esporte": "ESP",
        "Livros": "LIV",
        "Papelaria": "PAP",
        "Brinquedos": "BRI",
        "Moda": "MOD",
        "Pet": "PET",
        "Ferramentas": "FER",
        "Automotivo": "AUT",
    }

    for nome_categoria in categoria:
        contadores[nome_categoria] += 1
        indice = contadores[nome_categoria]
        nome_produto = rng.choice(CATEGORIAS[nome_categoria])
        marca = rng.choice(MARCAS)
        fator_preco = rng.lognormal(mean=0, sigma=0.38)
        preco = max(9.90, PRECO_BASE[nome_categoria] * fator_preco)
        custo = preco * rng.uniform(0.38, 0.74)
        estoque = int(np.clip(rng.negative_binomial(5, 0.16), 0, 280))
        observacao = rng.choice(
            ["", "Produto sazonal", "Revisar embalagem", "Reposição prioritária"],
            p=[0.88, 0.05, 0.04, 0.03],
        )
        registros.append(
            {
                "codigo": f"{prefixos[nome_categoria]}-{indice:04d}",
                "produto": f"{nome_produto} {marca} {indice:02d}",
                "categoria": nome_categoria,
                "marca": marca,
                "preco_venda": round(preco, 2),
                "custo_unitario": round(custo, 2),
                "estoque": estoque,
                "fornecedor": rng.choice(FORNECEDORES),
                "observacao": observacao,
            }
        )
    return pd.DataFrame(registros, columns=COLUNAS)


def gerar_catalogo_com_erros(semente: int = 42) -> pd.DataFrame:
    """Cria uma amostra pequena com inconsistências intencionais."""
    dados = gerar_catalogo_sintetico(90, semente).copy()
    dados["preco_venda"] = dados["preco_venda"].astype(object)
    dados["estoque"] = dados["estoque"].astype(object)
    dados.loc[2, "codigo"] = dados.loc[1, "codigo"]
    dados.loc[7, "produto"] = ""
    dados.loc[11, "estoque"] = -4
    dados.loc[15, "preco_venda"] = 0
    dados.loc[21, "custo_unitario"] = dados.loc[21, "preco_venda"] * 1.2
    dados.loc[28, "codigo"] = "COD INVÁLIDO"
    dados.loc[33, "categoria"] = ""
    dados.loc[41, "marca"] = ""
    dados.loc[52, "preco_venda"] = "valor inválido"
    dados.loc[63, "estoque"] = "dez"
    dados.loc[71, "fornecedor"] = ""
    dados.loc[80, "observacao"] = "Registro incluído para demonstrar a validação"
    return dados


def salvar_exemplos(diretorio: str | Path) -> tuple[Path, Path]:
    destino = Path(diretorio)
    destino.mkdir(parents=True, exist_ok=True)
    valido = destino / "catalogo_sintetico.csv"
    erros = destino / "catalogo_com_erros.csv"
    gerar_catalogo_sintetico().to_csv(valido, index=False)
    gerar_catalogo_com_erros().to_csv(erros, index=False)
    return valido, erros


def carregar_catalogo(caminho: str | Path) -> pd.DataFrame:
    return pd.read_csv(caminho)
