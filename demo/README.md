# Formulário local de demonstração

Esta página é o destino seguro da automação com Playwright. Ela roda apenas no computador do usuário e não envia informações para um servidor externo.

Na raiz do projeto, execute:

```bash
python -m http.server 8000 --directory demo
```

Depois abra `http://127.0.0.1:8000/formulario.html` ou execute:

```bash
python run.py --modo executar --limite 10
```

Os campos usam atributos `data-testid`. Eles funcionam como um contrato estável entre o HTML e `src/browser_bot.py`.
