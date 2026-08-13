# Dados e metodologia

## Origem dos dados

Este projeto usa apenas dados sintéticos. Nenhuma linha representa produto, marca, fornecedor ou operação real.

A função `gerar_catalogo_sintetico` cria uma base reproduzível com semente aleatória fixa. O objetivo é permitir que qualquer pessoa execute o repositório e obtenha os mesmos resultados apresentados no README.

O catálogo principal contém:

- 600 produtos;
- 12 categorias;
- 14 marcas fictícias;
- 5 fornecedores fictícios;
- preço, custo e estoque em faixas coerentes com cada categoria.

O preço é gerado a partir de um valor base da categoria e de uma distribuição lognormal. O custo corresponde a uma fração do preço e o estoque usa uma distribuição binomial negativa, adequada para criar muitos valores moderados e poucos valores altos.

## Duas amostras

| Arquivo | Finalidade |
|---|---|
| `catalogo_sintetico.csv` | Demonstrar o fluxo principal sem erros bloqueantes |
| `catalogo_com_erros.csv` | Mostrar duplicidade, campo vazio, número inválido, margem negativa e código fora do padrão |

Os erros da segunda base são inseridos pelo código. Isso torna o comportamento verificável nos testes e evita editar o CSV manualmente.

## Score de qualidade

O score é calculado como:

```text
100 x (1 - linhas com qualquer ocorrência / total de linhas)
```

Uma ocorrência pode ser um erro ou um aviso. Por isso, uma base sem bloqueios ainda pode ter score inferior a 100 quando contém preços atípicos ou outra situação que mereça revisão.

## Erro e aviso

**Erro** indica que a linha não deve seguir para a fila. Exemplos: código duplicado, campo obrigatório vazio, preço igual a zero e estoque negativo.

**Aviso** indica que a linha pode ser válida, mas precisa de atenção. Exemplos: margem abaixo de 20% e preço acima da faixa usual da categoria.

## Preço fora do padrão

O projeto calcula o primeiro quartil, o terceiro quartil e o intervalo interquartil dos preços em cada categoria.

```text
limite superior = Q3 + 1,5 x (Q3 - Q1)
```

Um preço acima desse limite recebe aviso. O método é simples, explicável e resistente a valores extremos, mas não substitui uma política comercial real.

## Indicadores comerciais

- **Margem bruta:** preço de venda menos custo unitário.
- **Margem bruta percentual:** margem bruta dividida pelo preço de venda.
- **Valor de estoque:** preço de venda multiplicado pela quantidade em estoque.

O valor de estoque é apresentado a preço de venda. Ele não representa receita realizada, lucro ou valor contábil.

## Limitações metodológicas

- Não há histórico temporal, demanda, impostos, frete ou descontos.
- Os parâmetros geradores foram escolhidos para demonstração, não estimados de uma empresa.
- O limite de margem de 20% é uma regra didática.
- O método de outlier sinaliza exceções, mas não decide sozinho se o preço está errado.
- O score mede consistência segundo as regras implementadas, não qualidade universal dos dados.
