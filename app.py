from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.analytics import (
    catalogo_liberado,
    estimar_tempo,
    resumir_catalogo,
    resumir_categoria,
)
from src.data import gerar_catalogo_com_erros, gerar_catalogo_sintetico
from src.execution import resumir_execucao, simular_execucao
from src.validation import ResultadoValidacao, validar_catalogo


RAIZ = Path(__file__).resolve().parent
CORES = {
    "fundo": "#07111F",
    "cartao": "#0D1B2A",
    "linha": "#1E3A52",
    "ciano": "#24C7D9",
    "verde": "#62D6A4",
    "amarelo": "#F4C95D",
    "vermelho": "#FF6B6B",
    "texto": "#EEF7FF",
    "muted": "#9EB3C7",
}


def moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def inteiro(valor: int | float) -> str:
    return f"{valor:,.0f}".replace(",", ".")


def percentual(valor: float) -> str:
    return f"{valor:.1%}".replace(".", ",")


def csv_bytes(dados: pd.DataFrame) -> bytes:
    return dados.to_csv(index=False).encode("utf-8-sig")


def preparar_grafico(fig, altura: int = 390):
    fig.update_layout(
        height=altura,
        margin=dict(l=12, r=12, t=55, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=CORES["texto"]),
        title_font=dict(size=18),
        legend_title_text="",
        hoverlabel=dict(bgcolor=CORES["cartao"], font_color=CORES["texto"]),
    )
    fig.update_xaxes(gridcolor="rgba(158,179,199,.12)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(158,179,199,.12)", zeroline=False)
    return fig


def aplicar_estilo() -> None:
    st.set_page_config(
        page_title="Central de Qualidade e Automação",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        .stApp { background: radial-gradient(circle at 88% 4%, #11304A 0, #07111F 34%); }
        [data-testid="stSidebar"] { background: #091725; border-right: 1px solid #1E3A52; }
        [data-testid="stMetric"] { background: rgba(13,27,42,.86); border: 1px solid #1E3A52; padding: 18px; border-radius: 14px; }
        [data-testid="stMetricLabel"] { color: #9EB3C7; }
        [data-testid="stMetricValue"] { color: #EEF7FF; }
        .hero { padding: 34px 36px; border: 1px solid #1E3A52; border-radius: 22px; background: linear-gradient(120deg, rgba(13,27,42,.97), rgba(12,41,60,.84)); margin-bottom: 24px; }
        .eyebrow { color: #24C7D9; text-transform: uppercase; letter-spacing: .15em; font-size: .74rem; font-weight: 800; }
        .hero h1 { font-size: clamp(2rem, 4vw, 3.8rem); line-height: 1.02; margin: 10px 0 14px; max-width: 940px; }
        .hero p { color: #B7C9D8; max-width: 900px; font-size: 1.05rem; line-height: 1.62; margin: 0; }
        .decision { border-left: 4px solid #62D6A4; background: rgba(98,214,164,.08); padding: 17px 19px; border-radius: 0 12px 12px 0; margin: 14px 0 24px; }
        .warning-box { border-left: 4px solid #F4C95D; background: rgba(244,201,93,.08); padding: 16px 18px; border-radius: 0 12px 12px 0; }
        .step { min-height: 142px; padding: 18px; border: 1px solid #1E3A52; border-radius: 14px; background: rgba(13,27,42,.84); }
        .step b { color: #24C7D9; }
        .step p { color: #AFC2D2; margin: 8px 0 0; line-height: 1.52; }
        div[data-testid="stDataFrame"] { border: 1px solid #1E3A52; border-radius: 12px; overflow: hidden; }
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] { background: rgba(13,27,42,.7); border-radius: 10px; padding: 10px 18px; }
        .stTabs [aria-selected="true"] { color: #24C7D9; border: 1px solid #24C7D9; }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def catalogo_padrao() -> pd.DataFrame:
    caminho = RAIZ / "data" / "catalogo_sintetico.csv"
    if caminho.exists():
        return pd.read_csv(caminho)
    return gerar_catalogo_sintetico()


@st.cache_data
def catalogo_erros() -> pd.DataFrame:
    caminho = RAIZ / "data" / "catalogo_com_erros.csv"
    if caminho.exists():
        return pd.read_csv(caminho)
    return gerar_catalogo_com_erros()


def escolher_dados() -> pd.DataFrame:
    st.sidebar.markdown("## Fonte dos dados")
    arquivo = st.sidebar.file_uploader("Envie um catálogo CSV", type="csv")
    if arquivo is not None:
        try:
            dados = pd.read_csv(arquivo)
        except Exception as erro:
            st.sidebar.error(f"Não foi possível ler o CSV: {erro}")
            st.stop()
        st.sidebar.success(f"Arquivo recebido: {len(dados)} linhas")
        return dados

    amostra = st.sidebar.radio(
        "Ou escolha uma amostra",
        ["Catálogo pronto", "Catálogo com erros"],
        help="A segunda opção demonstra como o sistema bloqueia inconsistências.",
    )
    if amostra == "Catálogo com erros":
        st.sidebar.caption("90 produtos, com falhas inseridas de propósito.")
        return catalogo_erros()
    st.sidebar.caption("600 produtos fictícios, reproduzíveis e sem falhas bloqueantes.")
    return catalogo_padrao()


def cabecalho() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">projeto de portfólio em engenharia de dados e automação</div>
          <h1>Central de Qualidade e Automação de Catálogo</h1>
          <p>Uma aplicação para validar lotes de produtos, explicar cada bloqueio, analisar o catálogo e demonstrar uma fila automatizada em ambiente local. O robô só recebe registros que passaram pelas regras de negócio.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def painel_executivo(resultado: ResultadoValidacao) -> None:
    resumo = resumir_catalogo(resultado.dados)
    categorias = resumir_categoria(resultado.dados)
    colunas = st.columns(4)
    colunas[0].metric("Linhas analisadas", inteiro(resumo["produtos"]))
    colunas[1].metric("Liberadas para a fila", inteiro(resumo["liberados"]))
    colunas[2].metric("Bloqueadas", inteiro(resumo["bloqueados"]))
    colunas[3].metric("Valor de estoque", moeda(resumo["valor_estoque"]))

    principal = categorias.iloc[0]
    st.markdown(
        f"""
        <div class="decision"><b>Leitura principal:</b> {principal['categoria']} concentra o maior valor de estoque entre as linhas liberadas, com {moeda(principal['valor_estoque'])}. O catálogo tem margem bruta mediana de {percentual(resumo['margem_mediana'])}.</div>
        """,
        unsafe_allow_html=True,
    )

    esquerda, direita = st.columns([1.15, 1])
    with esquerda:
        figura = px.bar(
            categorias.head(8).sort_values("valor_estoque"),
            x="valor_estoque",
            y="categoria",
            orientation="h",
            title="Valor de estoque por categoria",
            color="valor_estoque",
            color_continuous_scale=[[0, "#1B6D82"], [1, CORES["ciano"]]],
            labels={"valor_estoque": "Valor de estoque", "categoria": ""},
        )
        figura.update_layout(coloraxis_showscale=False)
        figura.update_xaxes(tickprefix="R$ ", tickformat=",.0f")
        st.plotly_chart(preparar_grafico(figura), use_container_width=True)

    with direita:
        status = (
            resultado.dados["status_validacao"]
            .value_counts()
            .rename_axis("status")
            .reset_index(name="linhas")
        )
        figura = px.bar(
            status,
            x="status",
            y="linhas",
            color="status",
            title="Situação das linhas após a validação",
            color_discrete_map={
                "Pronto": CORES["verde"],
                "Revisar": CORES["amarelo"],
                "Bloqueado": CORES["vermelho"],
            },
            text="linhas",
        )
        figura.update_traces(textposition="outside")
        st.plotly_chart(preparar_grafico(figura), use_container_width=True)

    st.markdown("### O que este painel responde")
    col1, col2, col3 = st.columns(3)
    col1.markdown('<div class="step"><b>01. O lote está confiável?</b><p>O score e os bloqueios indicam se a fila pode avançar ou precisa voltar para correção.</p></div>', unsafe_allow_html=True)
    col2.markdown('<div class="step"><b>02. Onde está o valor?</b><p>Preço, margem, estoque e categoria ajudam a priorizar a operação e a revisão.</p></div>', unsafe_allow_html=True)
    col3.markdown('<div class="step"><b>03. O que pode ser automatizado?</b><p>Somente linhas sem erro bloqueante entram no simulador ou no formulário local.</p></div>', unsafe_allow_html=True)


def painel_qualidade(resultado: ResultadoValidacao) -> None:
    total = len(resultado.dados)
    colunas = st.columns(4)
    colunas[0].metric("Score de qualidade", f"{resultado.score_qualidade:.1f}/100")
    colunas[1].metric("Erros", inteiro(len(resultado.erros)))
    colunas[2].metric("Avisos", inteiro(len(resultado.avisos)))
    colunas[3].metric("Linhas afetadas", inteiro(resultado.ocorrencias["linha"].nunique() if not resultado.ocorrencias.empty else 0))

    st.caption(
        "O score representa a proporção de linhas sem nenhuma ocorrência. Erros bloqueiam a automação; avisos pedem revisão, mas não bloqueiam."
    )

    if resultado.ocorrencias.empty:
        st.success(f"As {inteiro(total)} linhas passaram sem erros ou avisos.")
    else:
        grafico, explicacao = st.columns([1.1, 1])
        with grafico:
            contagem = (
                resultado.ocorrencias.groupby(["tipo", "severidade"])
                .size()
                .reset_index(name="ocorrencias")
                .sort_values("ocorrencias")
            )
            figura = px.bar(
                contagem,
                x="ocorrencias",
                y="tipo",
                orientation="h",
                color="severidade",
                title="Ocorrências por regra",
                color_discrete_map={"Erro": CORES["vermelho"], "Aviso": CORES["amarelo"]},
                labels={"ocorrencias": "Ocorrências", "tipo": ""},
            )
            st.plotly_chart(preparar_grafico(figura), use_container_width=True)
        with explicacao:
            st.markdown("#### Como interpretar")
            st.markdown(
                """
                - **Erro:** dado incompleto, inválido ou incoerente. A linha não entra na fila.
                - **Aviso:** possível exceção comercial. A linha pode avançar, mas merece revisão.
                - **Linha de origem:** número da linha no CSV, considerando o cabeçalho como linha 1.
                - **Mensagem:** orientação direta para corrigir o problema.
                """
            )

        severidade = st.segmented_control(
            "Filtrar ocorrências",
            ["Todas", "Erro", "Aviso"],
            default="Todas",
        )
        tabela = resultado.ocorrencias
        if severidade != "Todas":
            tabela = tabela[tabela["severidade"].eq(severidade)]
        st.dataframe(tabela, use_container_width=True, hide_index=True)
        st.download_button(
            "Baixar relatório de ocorrências",
            csv_bytes(resultado.ocorrencias),
            "relatorio_ocorrencias.csv",
            "text/csv",
        )

    st.markdown("### Regras implementadas")
    regras = pd.DataFrame(
        [
            ["Campos obrigatórios", "Código, produto, categoria, marca e fornecedor devem estar preenchidos.", "Erro"],
            ["Formato do código", "Usa o padrão ABC-0001 para padronizar a identificação.", "Erro"],
            ["Código único", "Dois produtos não podem compartilhar o mesmo código.", "Erro"],
            ["Valores numéricos", "Preço, custo e estoque precisam ser válidos e não negativos.", "Erro"],
            ["Coerência comercial", "O custo não pode superar o preço de venda neste fluxo.", "Erro"],
            ["Margem baixa", "Margens abaixo de 20% são destacadas para revisão.", "Aviso"],
            ["Preço fora do padrão", "Outliers por categoria são sinalizados pelo intervalo interquartil.", "Aviso"],
        ],
        columns=["Regra", "Decisão", "Severidade"],
    )
    st.dataframe(regras, use_container_width=True, hide_index=True)


def painel_catalogo(resultado: ResultadoValidacao) -> None:
    base = catalogo_liberado(resultado.dados)
    st.markdown("Somente linhas sem erro bloqueante aparecem nesta área.")
    col1, col2 = st.columns(2)
    categorias = sorted(base["categoria"].dropna().unique())
    marcas = sorted(base["marca"].dropna().unique())
    filtro_categoria = col1.multiselect("Categoria", categorias, placeholder="Todas")
    filtro_marca = col2.multiselect("Marca", marcas, placeholder="Todas")
    filtrado = base.copy()
    if filtro_categoria:
        filtrado = filtrado[filtrado["categoria"].isin(filtro_categoria)]
    if filtro_marca:
        filtrado = filtrado[filtrado["marca"].isin(filtro_marca)]

    metricas = st.columns(4)
    metricas[0].metric("Produtos no recorte", inteiro(len(filtrado)))
    metricas[1].metric("Estoque total", inteiro(filtrado["estoque"].sum()))
    metricas[2].metric("Preço mediano", moeda(filtrado["preco_venda"].median() if not filtrado.empty else 0))
    metricas[3].metric("Margem mediana", percentual(filtrado["margem_bruta_pct"].median() if not filtrado.empty else 0))

    if filtrado.empty:
        st.warning("Nenhum produto corresponde aos filtros escolhidos.")
        return

    esquerda, direita = st.columns(2)
    with esquerda:
        figura = px.scatter(
            filtrado,
            x="custo_unitario",
            y="preco_venda",
            color="categoria",
            size="estoque",
            hover_name="produto",
            title="Custo, preço e estoque",
            labels={"custo_unitario": "Custo unitário", "preco_venda": "Preço de venda"},
        )
        figura.update_xaxes(tickprefix="R$ ")
        figura.update_yaxes(tickprefix="R$ ")
        st.plotly_chart(preparar_grafico(figura), use_container_width=True)
    with direita:
        figura = px.histogram(
            filtrado,
            x="margem_bruta_pct",
            nbins=22,
            title="Distribuição da margem bruta",
            color_discrete_sequence=[CORES["verde"]],
            labels={"margem_bruta_pct": "Margem bruta", "count": "Produtos"},
        )
        figura.update_xaxes(tickformat=".0%")
        st.plotly_chart(preparar_grafico(figura), use_container_width=True)

    exibicao = filtrado[
        [
            "codigo",
            "produto",
            "categoria",
            "marca",
            "preco_venda",
            "custo_unitario",
            "estoque",
            "margem_bruta_pct",
            "status_validacao",
        ]
    ]
    st.dataframe(
        exibicao,
        use_container_width=True,
        hide_index=True,
        column_config={
            "preco_venda": st.column_config.NumberColumn("Preço", format="R$ %.2f"),
            "custo_unitario": st.column_config.NumberColumn("Custo", format="R$ %.2f"),
            "margem_bruta_pct": st.column_config.NumberColumn("Margem", format="percent"),
        },
    )
    st.download_button(
        "Baixar catálogo liberado",
        csv_bytes(filtrado),
        "catalogo_liberado.csv",
        "text/csv",
    )


def painel_simulacao(resultado: ResultadoValidacao) -> None:
    fila = catalogo_liberado(resultado.dados)
    st.markdown(
        '<div class="warning-box"><b>Cenário hipotético:</b> os tempos e as falhas deste simulador não são resultados de produção. Eles servem para dimensionar uma fila e demonstrar tratamento de exceções.</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    col1, col2, col3, col4 = st.columns(4)
    maximo = max(1, min(600, len(fila)))
    quantidade = col1.number_input("Itens na fila", 1, maximo, min(100, maximo))
    segundos_manual = col2.number_input("Segundos por item manual", 5.0, 180.0, 45.0, 5.0)
    segundos_robo = col3.number_input("Segundos por item automatizado", 0.5, 30.0, 3.0, 0.5)
    taxa = col4.slider("Taxa de sucesso simulada", 80, 100, 98) / 100

    tempo = estimar_tempo(int(quantidade), segundos_manual, segundos_robo)
    metricas = st.columns(4)
    metricas[0].metric("Tempo manual", f"{tempo['tempo_manual_min']:.1f} min")
    metricas[1].metric("Tempo automatizado", f"{tempo['tempo_automacao_min']:.1f} min")
    metricas[2].metric("Tempo potencialmente poupado", f"{tempo['economia_min']:.1f} min")
    metricas[3].metric("Redução estimada", percentual(tempo["reducao_pct"]))

    comparacao = pd.DataFrame(
        {
            "processo": ["Preenchimento manual", "Automação simulada"],
            "minutos": [tempo["tempo_manual_min"], tempo["tempo_automacao_min"]],
        }
    )
    figura = px.bar(
        comparacao,
        x="processo",
        y="minutos",
        color="processo",
        text_auto=".1f",
        title="Comparação de tempo no cenário escolhido",
        color_discrete_sequence=[CORES["amarelo"], CORES["ciano"]],
        labels={"processo": "", "minutos": "Minutos"},
    )
    figura.update_traces(textposition="outside")
    st.plotly_chart(preparar_grafico(figura, 360), use_container_width=True)

    if st.button("Gerar log da simulação", type="primary", use_container_width=True):
        st.session_state["log_simulado"] = simular_execucao(
            fila.head(int(quantidade)),
            taxa_sucesso=taxa,
            segundos_por_item=segundos_robo,
            semente=42,
        )

    log = st.session_state.get("log_simulado")
    if log is not None:
        resumo = resumir_execucao(log)
        st.markdown(
            f"**Resultado do log:** {resumo['concluidos']} concluídos, {resumo['falhas']} falhas simuladas e taxa de sucesso de {percentual(resumo['taxa_sucesso'])}."
        )
        st.dataframe(log, use_container_width=True, hide_index=True)
        st.download_button(
            "Baixar log simulado",
            csv_bytes(log),
            "log_execucao_simulada.csv",
            "text/csv",
        )


def painel_metodo() -> None:
    st.markdown("### Fluxo do projeto")
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div class="step"><b>01. Entrada</b><p>CSV próprio ou uma das duas amostras sintéticas incluídas no repositório.</p></div>', unsafe_allow_html=True)
    col2.markdown('<div class="step"><b>02. Qualidade</b><p>Regras de campos, formato, duplicidade, números, margem e preço por categoria.</p></div>', unsafe_allow_html=True)
    col3.markdown('<div class="step"><b>03. Fila</b><p>Erros são bloqueados. Linhas prontas ou em revisão podem ser exportadas.</p></div>', unsafe_allow_html=True)
    col4.markdown('<div class="step"><b>04. Execução</b><p>Simulador no painel ou Playwright contra o formulário local de demonstração.</p></div>', unsafe_allow_html=True)

    st.markdown("### Como testar a automação local")
    st.code(
        """# Terminal 1: abra o formulário local
python -m http.server 8000 --directory demo

# Terminal 2: instale o navegador do Playwright e execute 10 itens
python -m playwright install chromium
python run.py --modo executar --limite 10""",
        language="bash",
    )
    st.markdown(
        """
        O robô usa atributos `data-testid`, que são mais estáveis que coordenadas da tela. A URL externa é bloqueada por padrão. Para adaptar o projeto a um sistema real, seria necessário ter autorização, mapear os campos do ambiente de homologação, revisar limites de acesso e proteger qualquer credencial fora do código.
        """
    )
    st.info(
        "O painel publicado no Streamlit demonstra qualidade, análise e simulação. A execução com navegador é feita localmente porque o Streamlit Community Cloud não foi desenhado para abrir uma janela interativa do Chromium."
    )


def main() -> None:
    aplicar_estilo()
    cabecalho()
    dados = escolher_dados()
    try:
        resultado = validar_catalogo(dados)
    except ValueError as erro:
        st.error(str(erro))
        st.markdown("Use o arquivo `data/catalogo_sintetico.csv` como modelo das colunas esperadas.")
        st.stop()

    st.sidebar.markdown("## Leitura rápida")
    st.sidebar.metric("Score de qualidade", f"{resultado.score_qualidade:.1f}/100")
    st.sidebar.metric("Linhas bloqueadas", resultado.linhas_bloqueadas)
    st.sidebar.caption("Dados sintéticos. Nenhuma empresa ou produto real é representado.")

    abas = st.tabs(
        [
            "Visão executiva",
            "Qualidade dos dados",
            "Catálogo liberado",
            "Simulador de execução",
            "Como funciona",
        ]
    )
    with abas[0]:
        painel_executivo(resultado)
    with abas[1]:
        painel_qualidade(resultado)
    with abas[2]:
        painel_catalogo(resultado)
    with abas[3]:
        painel_simulacao(resultado)
    with abas[4]:
        painel_metodo()


if __name__ == "__main__":
    main()
