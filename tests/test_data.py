from src.data import COLUNAS, gerar_catalogo_com_erros, gerar_catalogo_sintetico


def test_catalogo_sintetico_e_reproduzivel():
    primeiro = gerar_catalogo_sintetico(50, semente=7)
    segundo = gerar_catalogo_sintetico(50, semente=7)
    assert primeiro.equals(segundo)
    assert list(primeiro.columns) == COLUNAS
    assert len(primeiro) == 50


def test_amostra_com_erros_tem_tamanho_previsto():
    assert len(gerar_catalogo_com_erros()) == 90
