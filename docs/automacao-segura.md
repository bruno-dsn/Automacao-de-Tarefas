# Automação segura

## Por que o projeto usa Playwright

Automação por coordenadas do mouse depende de resolução, posição da janela e tempo de carregamento. O Playwright localiza elementos pelo HTML, permite esperar estados da página e devolve erros mais úteis.

Neste projeto, cada campo possui um atributo `data-testid`. O robô conhece esses identificadores por meio do dicionário `SELETORES` em `src/browser_bot.py`.

## Proteções incluídas

- A URL padrão aponta para `127.0.0.1`.
- Hosts externos são bloqueados, salvo liberação explícita.
- O projeto não contém login, senha, token ou chave de API.
- O log guarda status, duração e mensagem de cada item.
- A validação antecede a execução.
- O formulário de demonstração não envia dados à internet.

## Como funciona o formulário local

O arquivo `demo/formulario.html` é servido por um servidor HTTP simples:

```bash
python -m http.server 8000 --directory demo
```

O navegador acessa:

```text
http://127.0.0.1:8000/formulario.html
```

Ao receber um produto, a página exibe a confirmação e mantém uma tabela dos cadastros realizados naquela sessão. Os dados são perdidos quando a página é fechada.

## Como adaptar os seletores

Em um ambiente próprio e autorizado:

1. abra as ferramentas de desenvolvimento do navegador;
2. identifique um atributo estável em cada campo;
3. altere somente o dicionário `SELETORES`;
4. mantenha os testes de contrato para detectar mudanças;
5. valide poucos registros em homologação antes de aumentar o lote.

Evite seletores baseados em posição, nomes de classes gerados automaticamente ou texto que muda com frequência.

## Uso de URL externa

O argumento abaixo existe para tornar a política explícita:

```bash
python run.py --modo executar --url https://sistema-autorizado.exemplo/formulario --permitir-url-externa
```

Não use essa opção em um site sem autorização. Antes de qualquer adaptação real, revise os termos do sistema, limites de acesso, política de dados, tratamento de credenciais e impacto operacional.

## Credenciais

Se um ambiente autorizado exigir autenticação:

- use variáveis de ambiente ou um gerenciador de segredos;
- nunca salve senhas no código, CSV, README ou histórico do Git;
- utilize uma conta de homologação com o menor privilégio possível;
- evite registrar informações sensíveis no log;
- defina como interromper e reprocessar a fila com segurança.

## O que faltaria para produção

- fila persistente e idempotência;
- tentativas com política de espera;
- captura de evidências e monitoramento;
- limites de volume e janela de execução;
- gestão de credenciais;
- logs centralizados e alertas;
- homologação com responsáveis pelo sistema de destino;
- revisão de segurança, privacidade e conformidade.
