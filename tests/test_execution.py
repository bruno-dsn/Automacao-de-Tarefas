from src.data import gerar_catalogo_sintetico
from src.execution import resumir_execucao, simular_execucao


def test_simulacao_reproduzivel():
    produtos = gerar_catalogo_sintetico(20)
    primeiro = simular_execucao(produtos, taxa_sucesso=0.9, semente=8)
    segundo = simular_execucao(produtos, taxa_sucesso=0.9, semente=8)
    assert primeiro.equals(segundo)
    assert resumir_execucao(primeiro)["total"] == 20


def test_taxa_invalida_e_rejeitada():
    produtos = gerar_catalogo_sintetico(2)
    try:
        simular_execucao(produtos, taxa_sucesso=1.2)
    except ValueError as erro:
        assert "entre 0 e 1" in str(erro)
    else:
        raise AssertionError("A função deveria rejeitar uma taxa maior que 1.")
