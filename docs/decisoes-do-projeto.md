# Decisões do projeto

## 1. O robô não é o centro da solução

O projeto anterior demonstrava preenchimento de formulário, mas não respondia o que aconteceria se o CSV tivesse duplicidades, preço inválido ou estoque negativo. A nova versão começa pela qualidade dos dados e apresenta a automação como etapa posterior.

## 2. O destino é local

Um site externo pode mudar, exigir credenciais ou proibir automação. O formulário incluído no repositório torna a demonstração reproduzível e evita depender de terceiros.

## 3. Erro e aviso têm decisões diferentes

Bloquear qualquer exceção gera uma fila desnecessariamente rígida. Ignorar exceções gera risco. O projeto separa:

- erro, que impede o envio;
- aviso, que pede revisão humana sem interromper automaticamente.

## 4. O painel e a execução são separados

O Streamlit apresenta a análise e a simulação. O Playwright é executado localmente pela linha de comando. Essa divisão evita prometer um navegador interativo em um ambiente de publicação que pode não suportá-lo.

## 5. A estimativa é configurável

O simulador pede quantidade, tempo manual, tempo automatizado e taxa de sucesso. Nenhum valor é tratado como produtividade real. O objetivo é responder perguntas de capacidade com hipóteses visíveis.

## 6. Os dados são sintéticos e reproduzíveis

O projeto não disfarça dados fictícios como reais. A geração está no código, a semente é fixa e os resultados podem ser recalculados.

## 7. Seletores são contratos

O HTML e o robô compartilham atributos `data-testid`. Um teste verifica se todo seletor esperado existe na página. Se o formulário mudar, o teste sinaliza a incompatibilidade antes da execução.

## Próximas evoluções possíveis

- editor de regras pela interface;
- armazenamento do histórico de execuções;
- autenticação em ambiente de homologação;
- política de reprocessamento de falhas;
- integração com banco de dados ou fila de mensagens;
- validação de esquema com uma biblioteca dedicada;
- testes completos do navegador em integração contínua.
