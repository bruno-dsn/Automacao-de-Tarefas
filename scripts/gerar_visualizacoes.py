from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from src.analytics import estimar_tempo, resumir_catalogo, resumir_categoria
from src.data import gerar_catalogo_sintetico
from src.validation import validar_catalogo


FUNDO = "#07111F"
CARTAO = "#0D1B2A"
LINHA = "#1E3A52"
CIANO = "#24C7D9"
VERDE = "#62D6A4"
AMARELO = "#F4C95D"
TEXTO = "#EEF7FF"
MUTED = "#9EB3C7"


def moeda_curta(valor: float) -> str:
    if valor >= 1_000_000:
        return f"R$ {valor / 1_000_000:.2f} mi".replace(".", ",")
    if valor >= 1_000:
        return f"R$ {valor / 1_000:.0f} mil"
    return f"R$ {valor:.0f}"


def cartao(fig, x: float, y: float, largura: float, altura: float, raio: float = 0.016):
    figura = FancyBboxPatch(
        (x, y),
        largura,
        altura,
        boxstyle=f"round,pad=0.008,rounding_size={raio}",
        transform=fig.transFigure,
        facecolor=CARTAO,
        edgecolor=LINHA,
        linewidth=1.2,
        zorder=-20,
    )
    fig.patches.append(figura)


def criar_painel(caminho: Path) -> None:
    resultado = validar_catalogo(gerar_catalogo_sintetico())
    resumo = resumir_catalogo(resultado.dados)
    categorias = resumir_categoria(resultado.dados).head(6).sort_values("valor_estoque")
    tempo = estimar_tempo(100, 45, 3)

    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=FUNDO)
    ax_bg = fig.add_axes([0, 0, 1, 1])
    ax_bg.set_axis_off()
    grad = np.linspace(0, 1, 600)
    grad = np.vstack([grad] * 1000)
    ax_bg.imshow(grad, extent=[0.58, 1, 0.58, 1], cmap="Blues", alpha=0.12, aspect="auto")

    fig.text(0.052, 0.925, "CENTRAL DE QUALIDADE E AUTOMAÇÃO", color=CIANO, fontsize=13, fontweight="bold")
    fig.text(0.052, 0.855, "Catálogo confiável antes do robô", color=TEXTO, fontsize=38, fontweight="bold")
    fig.text(
        0.052,
        0.810,
        "Validação de dados, análise comercial e simulação de uma fila automatizada em ambiente local.",
        color=MUTED,
        fontsize=17,
    )

    metricas = [
        ("PRODUTOS", f"{resumo['produtos']}", "linhas analisadas"),
        ("LIBERADOS", f"{resumo['liberados']}", "sem erro bloqueante"),
        ("CATEGORIAS", f"{resumo['categorias']}", "portfólio sintético"),
        ("VALOR DE ESTOQUE", moeda_curta(resumo["valor_estoque"]), "a preço de venda"),
    ]
    inicio_x = 0.052
    largura = 0.205
    for indice, (rotulo, valor, detalhe) in enumerate(metricas):
        x = inicio_x + indice * 0.226
        cartao(fig, x, 0.65, largura, 0.12)
        fig.text(x + 0.018, 0.735, rotulo, color=MUTED, fontsize=10, fontweight="bold")
        fig.text(x + 0.018, 0.690, valor, color=TEXTO, fontsize=24, fontweight="bold")
        fig.text(x + 0.018, 0.665, detalhe, color=MUTED, fontsize=10)

    cartao(fig, 0.052, 0.12, 0.57, 0.47)
    ax1 = fig.add_axes([0.084, 0.17, 0.505, 0.35], facecolor=CARTAO)
    ax1.set_zorder(3)
    barras = ax1.barh(categorias["categoria"], categorias["valor_estoque"], color=CIANO, alpha=0.88, height=0.58)
    ax1.set_title("Valor de estoque por categoria", color=TEXTO, loc="left", fontsize=17, fontweight="bold", pad=18)
    ax1.tick_params(colors=MUTED, labelsize=11, length=0)
    ax1.xaxis.set_visible(False)
    for lado in ax1.spines.values():
        lado.set_visible(False)
    ax1.grid(False)
    for barra, valor in zip(barras, categorias["valor_estoque"]):
        ax1.text(valor + 6000, barra.get_y() + barra.get_height() / 2, moeda_curta(valor), va="center", color=TEXTO, fontsize=10)

    cartao(fig, 0.65, 0.12, 0.30, 0.47)
    fig.text(0.68, 0.525, "CENÁRIO DE 100 ITENS", color=MUTED, fontsize=11, fontweight="bold")
    fig.text(0.68, 0.477, "70 min", color=VERDE, fontsize=36, fontweight="bold")
    fig.text(0.68, 0.445, "economia potencial de tempo", color=MUTED, fontsize=11)
    ax2 = fig.add_axes([0.68, 0.245, 0.235, 0.155], facecolor=CARTAO)
    ax2.set_zorder(3)
    processos = ["Manual", "Automação"]
    minutos = [tempo["tempo_manual_min"], tempo["tempo_automacao_min"]]
    barras = ax2.bar(processos, minutos, color=[AMARELO, CIANO], width=0.52)
    ax2.set_ylim(0, 86)
    ax2.tick_params(colors=MUTED, labelsize=11, length=0)
    ax2.yaxis.set_visible(False)
    for lado in ax2.spines.values():
        lado.set_visible(False)
    for barra, valor in zip(barras, minutos):
        ax2.text(barra.get_x() + barra.get_width() / 2, valor + 3, f"{valor:.0f} min", ha="center", color=TEXTO, fontsize=11, fontweight="bold")
    fig.text(0.68, 0.171, "Estimativa configurável, não resultado de produção.", color=MUTED, fontsize=9)

    fig.text(0.052, 0.065, "Dados sintéticos e reproduzíveis  |  Python  |  Pandas  |  Streamlit  |  Plotly  |  Playwright", color=MUTED, fontsize=11)
    fig.savefig(caminho, facecolor=FUNDO, bbox_inches=None, pad_inches=0)
    plt.close(fig)


def criar_capa_linkedin(caminho: Path) -> None:
    resultado = validar_catalogo(gerar_catalogo_sintetico())
    resumo = resumir_catalogo(resultado.dados)
    tempo = estimar_tempo(100, 45, 3)

    fig = plt.figure(figsize=(12, 6.27), dpi=100, facecolor=FUNDO)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    grad = np.linspace(0, 1, 500)
    grad = np.vstack([grad] * 900)
    ax.imshow(grad, extent=[0.42, 1, 0, 1], cmap="Blues", alpha=0.14, aspect="auto")

    fig.text(0.065, 0.865, "PROJETO DE PORTFÓLIO", color=CIANO, fontsize=12, fontweight="bold")
    fig.text(0.065, 0.695, "Qualidade de dados\nantes da automação", color=TEXTO, fontsize=37, fontweight="bold", linespacing=1.02)
    fig.text(0.065, 0.555, "Um catálogo passa por regras de negócio antes de entrar\nem uma fila controlada com Playwright.", color=MUTED, fontsize=14, linespacing=1.5)

    itens = [
        ("600", "produtos fictícios"),
        ("12", "categorias"),
        ("70 min", "economia estimada em 100 itens"),
    ]
    for indice, (valor, legenda) in enumerate(itens):
        x = 0.065 + indice * 0.292
        cartao(fig, x, 0.205, 0.255, 0.18, 0.02)
        fig.text(x + 0.018, 0.308, valor, color=VERDE if indice == 2 else TEXTO, fontsize=22, fontweight="bold")
        fig.text(x + 0.018, 0.242, legenda, color=MUTED, fontsize=9.5)

    fig.text(0.065, 0.095, "Python  |  Pandas  |  Streamlit  |  Plotly  |  Playwright", color=MUTED, fontsize=10)
    fig.text(0.935, 0.095, "BRUNO NUNES", color=CIANO, fontsize=10, fontweight="bold", ha="right")
    fig.savefig(caminho, facecolor=FUNDO, bbox_inches=None, pad_inches=0)
    plt.close(fig)


if __name__ == "__main__":
    destino = RAIZ / "assets"
    destino.mkdir(parents=True, exist_ok=True)
    criar_painel(destino / "painel_automacao.png")
    criar_capa_linkedin(destino / "capa_linkedin.png")
    print("Visualizações criadas em assets/.")
