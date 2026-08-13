import pandas as pd
import pytest

from src.data import gerar_catalogo_com_erros, gerar_catalogo_sintetico
from src.validation import validar_catalogo


def test_catalogo_base_nao_tem_linhas_bloqueadas():
    resultado = validar_catalogo(gerar_catalogo_sintetico(120))
    assert resultado.linhas_bloqueadas == 0
    assert not resultado.dados["status_validacao"].eq("Bloqueado").any()


def test_erros_intencionais_sao_bloqueados():
    resultado = validar_catalogo(gerar_catalogo_com_erros())
    tipos = set(resultado.erros["tipo"])
    assert resultado.linhas_bloqueadas >= 10
    assert {"Duplicidade", "Campo vazio", "Valor inválido", "Formato inválido"} <= tipos


def test_coluna_obrigatoria_ausente_gera_erro_claro():
    with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
        validar_catalogo(pd.DataFrame({"codigo": ["ABC-0001"]}))
