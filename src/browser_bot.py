from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from urllib.parse import urlparse

import pandas as pd


SELETORES = {
    "codigo": "[data-testid='codigo']",
    "produto": "[data-testid='produto']",
    "categoria": "[data-testid='categoria']",
    "marca": "[data-testid='marca']",
    "preco_venda": "[data-testid='preco-venda']",
    "custo_unitario": "[data-testid='custo-unitario']",
    "estoque": "[data-testid='estoque']",
    "fornecedor": "[data-testid='fornecedor']",
    "observacao": "[data-testid='observacao']",
    "enviar": "[data-testid='enviar-produto']",
    "resultado": "[data-testid='resultado-cadastro']",
}


@dataclass(frozen=True)
class ConfiguracaoAutomacao:
    url: str = "http://127.0.0.1:8000/formulario.html"
    headless: bool = False
    timeout_ms: int = 10_000
    permitir_url_externa: bool = False


def validar_url(url: str, permitir_externa: bool = False) -> str:
    """Bloqueia destinos externos por padrão para evitar uso acidental."""
    destino = urlparse(url)
    if destino.scheme not in {"http", "https"} or not destino.hostname:
        raise ValueError("Informe uma URL HTTP ou HTTPS válida.")
    hosts_locais = {"localhost", "127.0.0.1", "::1"}
    if destino.hostname not in hosts_locais and not permitir_externa:
        raise ValueError(
            "A automação aceita somente endereço local por padrão. "
            "Use a liberação explícita apenas em um ambiente autorizado."
        )
    return url


def _preencher_produto(pagina, produto: pd.Series) -> None:
    campos = {
        "codigo": str(produto["codigo"]),
        "produto": str(produto["produto"]),
        "categoria": str(produto["categoria"]),
        "marca": str(produto["marca"]),
        "preco_venda": f"{float(produto['preco_venda']):.2f}",
        "custo_unitario": f"{float(produto['custo_unitario']):.2f}",
        "estoque": str(int(produto["estoque"])),
        "fornecedor": str(produto["fornecedor"]),
        "observacao": str(produto.get("observacao", "")),
    }
    for campo, valor in campos.items():
        pagina.locator(SELETORES[campo]).fill(valor)


def executar_automacao(
    produtos: pd.DataFrame,
    configuracao: ConfiguracaoAutomacao | None = None,
) -> pd.DataFrame:
    """Cadastra os produtos no formulário local e devolve um log auditável."""
    config = configuracao or ConfiguracaoAutomacao()
    validar_url(config.url, config.permitir_url_externa)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as erro:
        raise RuntimeError(
            "Playwright não está instalado. Instale requirements-automation.txt "
            "e execute 'python -m playwright install chromium'."
        ) from erro

    registros: list[dict[str, object]] = []
    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch(headless=config.headless)
        pagina = navegador.new_page()
        pagina.set_default_timeout(config.timeout_ms)
        pagina.goto(config.url, wait_until="domcontentloaded")

        for ordem, (_, produto) in enumerate(produtos.iterrows(), start=1):
            inicio = perf_counter()
            status = "Concluído"
            mensagem = "Produto cadastrado no formulário local."
            try:
                _preencher_produto(pagina, produto)
                pagina.locator(SELETORES["enviar"]).click()
                pagina.locator(SELETORES["resultado"]).wait_for(state="visible")
                resposta = pagina.locator(SELETORES["resultado"]).inner_text().strip()
                if "sucesso" not in resposta.lower():
                    raise RuntimeError(resposta or "O formulário não confirmou o cadastro.")
            except Exception as erro:
                status = "Falha"
                mensagem = str(erro).splitlines()[0][:240]

            registros.append(
                {
                    "ordem": ordem,
                    "codigo": produto["codigo"],
                    "produto": produto["produto"],
                    "status_execucao": status,
                    "duracao_segundos": round(perf_counter() - inicio, 2),
                    "mensagem": mensagem,
                }
            )
        navegador.close()
    return pd.DataFrame(registros)
