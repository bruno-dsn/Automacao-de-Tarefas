# Automação de Cadastro de Produtos

Projeto de automação desenvolvido em Python para automatizar o processo de cadastro de produtos em sistemas web.

## Sobre o Projeto

Este projeto foi desenvolvido como parte do meu aprendizado em Python e automação de tarefas. O objetivo é automatizar o cadastro massivo de produtos em um sistema web, eliminando a necessidade de digitação manual repetitiva.

A automação utiliza a biblioteca PyAutoGUI para simular interações humanas com o navegador, como cliques e digitação, e a biblioteca Pandas para processar dados de arquivos CSV.

## Funcionalidades

- Abertura automática do navegador Chrome
- Login automático no sistema
- Leitura de dados de produtos a partir de arquivo CSV
- Cadastro automatizado de múltiplos produtos
- Compatibilidade com macOS e Windows

## Tecnologias Utilizadas

- Python 3.7 ou superior
- PyAutoGUI - Automação de interface gráfica
- Pandas - Manipulação de dados tabulares
- Pyperclip - Operações de clipboard

## Requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- Python 3.7 ou versão mais recente
- Google Chrome
- pip (gerenciador de pacotes do Python)

## Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/automacao-cadastro-produtos.git
cd automacao-cadastro-produtos
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

### Obter Coordenadas da Tela

As coordenadas dos campos do formulário variam conforme a resolução da tela. Para obter as coordenadas corretas:

1. Execute o script auxiliar:
```bash
python pegar_posicao.py
```

2. Posicione o mouse sobre o campo desejado quando solicitado
3. Anote as coordenadas X e Y exibidas

### Atualizar Coordenadas no Código

Abra o arquivo `codigo.py` e localize as seguintes linhas:

```python
CAMPO_EMAIL_X = 2532
CAMPO_EMAIL_Y = 380
CAMPO_PRODUTO_X = 2524
CAMPO_PRODUTO_Y = 264
```

Substitua pelos valores obtidos no passo anterior.

## Estrutura do Arquivo CSV

O arquivo `produtos.csv` deve conter as seguintes colunas:

- codigo: Código único do produto
- marca: Marca do produto
- tipo: Tipo ou categoria do produto
- categoria: Número da categoria
- preco_unitario: Preço de venda
- custo: Custo de aquisição
- obs: Observações (opcional)

Exemplo:

```csv
codigo,marca,tipo,categoria,preco_unitario,custo,obs
PROD001,Nike,Tenis,1,299.90,150.00,Tamanho 42
PROD002,Adidas,Camisa,2,129.90,60.00,
```

## Como Usar

1. Certifique-se de que o arquivo `produtos.csv` está na mesma pasta do script
2. Feche outras janelas do Chrome que possam interferir
3. Execute o script:

```bash
python codigo.py
```

4. Aguarde 10 segundos sem tocar no mouse ou teclado
5. O script executará automaticamente todo o processo

## Observações Importantes

- Durante a execução, não utilize o mouse ou teclado
- Para interromper emergencialmente, mova o mouse para o canto superior esquerdo da tela
- O tempo total de execução depende da quantidade de produtos (aproximadamente 1 segundo por produto)
- Certifique-se de que a janela do navegador está visível e não minimizada

## Solução de Problemas

### O Chrome não abre
Verifique se o Google Chrome está instalado corretamente no sistema.

### Coordenadas incorretas
Execute novamente o script `pegar_posicao.py` e certifique-se de que a resolução da tela não foi alterada.

### Campos não são preenchidos corretamente
Aumente os valores de `time.sleep()` no código para dar mais tempo ao sistema processar cada ação.

### Arquivo CSV não encontrado
Certifique-se de que o arquivo `produtos.csv` está na mesma pasta que o script `codigo.py`.

## Estrutura do Projeto

```
automacao-cadastro-produtos/
├── codigo.py              # Script principal de automação
├── pegar_posicao.py       # Utilitário para capturar coordenadas
├── produtos.csv           # Dados dos produtos a serem cadastrados
├── requirements.txt       # Dependências do projeto
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Este arquivo
```

## Aprendizados

Este projeto me permitiu aprender e praticar:

- Automação de interfaces gráficas com PyAutoGUI
- Manipulação de arquivos CSV com Pandas
- Detecção de sistema operacional em Python
- Controle de fluxo e loops
- Tratamento de dados tabulares
- Boas práticas de documentação de código

## Limitações Conhecidas

- Requer que o navegador esteja visível durante a execução
- Dependente de coordenadas específicas da tela
- Sensível a mudanças no layout do site
- Não funciona com o computador bloqueado

## Melhorias Futuras

- Implementação com Selenium para maior robustez
- Interface gráfica para facilitar configuração
- Sistema de log detalhado
- Tratamento de erros mais robusto
- Suporte para múltiplos navegadores
- Validação de dados antes do cadastro

## Contribuições

Este é um projeto de aprendizado, mas sugestões e melhorias são bem-vindas. Sinta-se livre para abrir issues ou enviar pull requests.

## Licença

Este projeto foi desenvolvido para fins educacionais.

## Autor

Projeto desenvolvido como parte do aprendizado em Python e automação.

## Contato

Para dúvidas ou sugestões, abra uma issue neste repositório.
