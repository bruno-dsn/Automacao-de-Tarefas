from pathlib import Path

from src.browser_bot import SELETORES


def test_formulario_contem_todos_os_seletores():
    pagina = (Path(__file__).parents[1] / "demo" / "formulario.html").read_text()
    for seletor in SELETORES.values():
        testid = seletor.split("'")[1]
        assert f'data-testid="{testid}"' in pagina
