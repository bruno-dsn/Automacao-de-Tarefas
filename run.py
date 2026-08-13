from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd

from src.analytics import catalogo_liberado
from src.browser_bot import ConfiguracaoAutomacao, executar_automacao
from src.execution import resumir_execucao, simular_execucao
from src.validation import validar_catalogo


RAIZ = Path(__file__).resolve().parent


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida um catálogo e prepara sua automação de forma segura."
    )
    parser.add_argument(
        "--modo",
        choices=["validar", "simular", "executar"],
        default="validar",
    )
    parser.add_argument(
        "--arquivo",
        type=Path,
        default=RAIZ / "data" / "catalogo_sintetico.csv",
    )
    parser.add_argument("--limite", type=int, default=10)
    parser.add_argument("--saida", type=Path, default=RAIZ / "data" / "log_execucao.csv")
    parser.add_argument(
        "--url",
        default=os.getenv(
            "AUTOMATION_BASE_URL",
            "http://127.0.0.1:8000/formulario.html",
        ),
    )
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--permitir-url-externa", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = argumentos()
    dados = pd.read_csv(args.arquivo)
    resultado = validar_catalogo(dados)
    liberados = catalogo_liberado(resultado.dados).head(max(0, args.limite))

    print(f"Linhas analisadas: {len(resultado.dados)}")
    print(f"Linhas bloqueadas: {resultado.linhas_bloqueadas}")
    print(f"Linhas liberadas para a fila: {len(liberados)}")

    if args.modo == "validar":
        if resultado.ocorrencias.empty:
            print("Nenhuma ocorrência encontrada.")
        else:
            print(resultado.ocorrencias.to_string(index=False))
        return

    if args.modo == "simular":
        log = simular_execucao(liberados)
    else:
        config = ConfiguracaoAutomacao(
            url=args.url,
            headless=args.headless,
            permitir_url_externa=args.permitir_url_externa,
        )
        log = executar_automacao(liberados, config)

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    log.to_csv(args.saida, index=False)
    resumo = resumir_execucao(log)
    print(f"Concluídos: {resumo['concluidos']} de {resumo['total']}")
    print(f"Taxa de sucesso: {resumo['taxa_sucesso']:.1%}")
    print(f"Log salvo em: {args.saida}")


if __name__ == "__main__":
    main()
