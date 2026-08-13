import pytest

from src.browser_bot import validar_url


def test_url_local_e_permitida():
    assert validar_url("http://127.0.0.1:8000/formulario.html")


def test_url_externa_e_bloqueada_por_padrao():
    with pytest.raises(ValueError, match="somente endereço local"):
        validar_url("https://example.com/formulario")


def test_url_externa_exige_liberacao_explicita():
    assert validar_url("https://example.com/formulario", permitir_externa=True)
