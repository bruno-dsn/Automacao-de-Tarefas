from src.analytics import estimar_tempo, resumir_catalogo
from src.data import gerar_catalogo_sintetico
from src.validation import validar_catalogo


def test_resumo_do_catalogo():
    dados = validar_catalogo(gerar_catalogo_sintetico(60)).dados
    resumo = resumir_catalogo(dados)
    assert resumo["produtos"] == 60
    assert resumo["liberados"] == 60
    assert resumo["categorias"] > 1


def test_estimativa_de_tempo():
    tempo = estimar_tempo(100, segundos_manual=45, segundos_automacao=3)
    assert tempo["tempo_manual_min"] == 75
    assert tempo["tempo_automacao_min"] == 5
    assert round(tempo["reducao_pct"], 2) == 0.93
