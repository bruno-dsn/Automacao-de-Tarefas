from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from src.data import salvar_exemplos


if __name__ == "__main__":
    caminhos = salvar_exemplos(RAIZ / "data")
    for caminho in caminhos:
        print(f"Arquivo criado: {caminho.relative_to(RAIZ)}")
