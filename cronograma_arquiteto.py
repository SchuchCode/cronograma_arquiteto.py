"""
Cronograma de Estudos — Arquiteto Fundatec
Streamlit app com checklist, progresso por semana e filtros por matéria.

Como rodar:
    pip install streamlit
    streamlit run cronograma_arquiteto.py

O progresso é salvo em um arquivo JSON local (progresso_cronograma.json),
na mesma pasta do script, para persistir entre execuções.
"""

import json
import os
from urllib.parse import quote_plus
import streamlit as st

# ---------------------------------------------------------------------------
# Config geral
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Cronograma — Arquiteto Fundatec", layout="centered")

CHECKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "progresso_cronograma.json")

SUBJECT_LABEL = {"CE": "CE", "LEG": "Legislação", "POR": "Português", "REV": "Revisão"}
SUBJECT_COLOR = {
    "CE": "#1B4B72",
    "LEG": "#8A5A12",
    "POR": "#3E6B4E",
    "REV": "#A24B34",
}

# ---------------------------------------------------------------------------
# Dados do cronograma (mesma estrutura do HTML original)
# ---------------------------------------------------------------------------
DATA = [
    {"n": 1, "range": "27/07–01/08", "phase": "Semanas 1–6 · Legislação do zero", "days": [
        {"d": "Seg", "s": "CE", "t": "Ética e disciplina do arquiteto/urbanista; áreas de atuação e atribuições profissionais; acessibilidade"},
        {"d": "Ter", "s": "LEG", "t": "Estatuto dos Funcionários Públicos de POA (LC 133/1985) — provimento e vacância"},
        {"d": "Qua", "s": "CE", "t": "Ética e disciplina do arquiteto/urbanista; áreas de atuação e atribuições profissionais; acessibilidade"},
        {"d": "Qui", "s": "LEG", "t": "Estatuto dos Funcionários Públicos — direitos, deveres e regime disciplinar"},
        {"d": "Sex", "s": "CE", "t": "Ética e disciplina do arquiteto/urbanista; áreas de atuação e atribuições profissionais; acessibilidade"},
        {"d": "Sáb", "s": "REV", "t": "Revisão da semana + simulado misto (peso maior para CE e Legislação)"},
    ]},
    {"n": 2, "range": "03/08–08/08", "phase": "Semanas 1–6 · Legislação do zero", "days": [
        {"d": "Seg", "s": "CE", "t": "Segurança contra incêndio; desempenho de edificações; conforto ambiental e ergonomia"},
        {"d": "Ter", "s": "LEG", "t": "CF/1988 — Princípios Fundamentais + Direitos e Garantias Fundamentais"},
        {"d": "Qua", "s": "CE", "t": "Segurança contra incêndio; desempenho de edificações; conforto ambiental e ergonomia"},
        {"d": "Qui", "s": "LEG", "t": "CF/1988 — Organização do Estado + Organização dos Poderes"},
        {"d": "Sex", "s": "CE", "t": "Segurança contra incêndio; desempenho de edificações; conforto ambiental e ergonomia"},
        {"d": "Sáb", "s": "REV", "t": "Revisão da semana + simulado misto (peso maior para CE e Legislação)"},
    ]},
    {"n": 3, "range": "10/08–15/08", "phase": "Semanas 1–6 · Legislação do zero", "days": [
        {"d": "Seg", "s": "CE", "t": "Elaboração de projetos arquitetônicos/urbanísticos; representação gráfica, AutoCAD 2D e BIM"},
        {"d": "Ter", "s": "LEG", "t": "CF/1988 — Defesa do Estado + Ordem Social"},
        {"d": "Qua", "s": "CE", "t": "Elaboração de projetos arquitetônicos/urbanísticos; representação gráfica, AutoCAD 2D e BIM"},
        {"d": "Qui", "s": "LEG", "t": "Lei Orgânica do Município de Porto Alegre"},
        {"d": "Sex", "s": "CE", "t": "Elaboração de projetos arquitetônicos/urbanísticos; representação gráfica, AutoCAD 2D e BIM"},
        {"d": "Sáb", "s": "REV", "t": "Revisão da semana + simulado misto (peso maior para CE e Legislação)"},
    ]},
    {"n": 4, "range": "17/08–22/08", "phase": "Semanas 1–6 · Legislação do zero", "days": [
        {"d": "Seg", "s": "CE", "t": "Gerenciamento e qualidade da construção; custo da edificação; licitações e contratos administrativos"},
        {"d": "Ter", "s": "LEG", "t": "Lei de Improbidade Administrativa (Lei 8.429/1992)"},
        {"d": "Qua", "s": "CE", "t": "Gerenciamento e qualidade da construção; custo da edificação; licitações e contratos administrativos"},
        {"d": "Qui", "s": "LEG", "t": "Lei Maria da Penha (Lei 11.340/2006)"},
        {"d": "Sex", "s": "CE", "t": "Gerenciamento e qualidade da construção; custo da edificação; licitações e contratos administrativos"},
        {"d": "Sáb", "s": "REV", "t": "Revisão da semana + simulado misto (peso maior para CE e Legislação)"},
    ]},
    {"n": 5, "range": "24/08–29/08", "phase": "Semanas 1–6 · Legislação do zero", "days": [
        {"d": "Seg", "s": "CE", "t": "Execução e fiscalização de obras públicas; instalações elétricas prediais"},
        {"d": "Ter", "s": "LEG", "t": "ECA (Lei 8.069/1990)"},
        {"d": "Qua", "s": "CE", "t": "Execução e fiscalização de obras públicas; instalações elétricas prediais"},
        {"d": "Qui", "s": "LEG", "t": "Ética no Serviço Público (Decreto 21.071/2021) + Código de Ética da Alta Administração"},
        {"d": "Sex", "s": "CE", "t": "Execução e fiscalização de obras públicas; instalações elétricas prediais"},
        {"d": "Sáb", "s": "REV", "t": "Revisão da semana + simulado misto (peso maior para CE e Legislação)"},
    ]},
    {"n": 6, "range": "31/08–05/09", "phase": "Semanas 1–6 · Legislação do zero", "days": [
        {"d": "Seg", "s": "CE", "t": "Instalações hidrossanitárias prediais; materiais e técnicas construtivas"},
        {"d": "Ter", "s": "LEG", "t": "Lei Municipal 2.902/1965 (DEMHAB) + LRF (LC 101/2000)"},
        {"d": "Qua", "s": "CE", "t": "Instalações hidrossanitárias prediais; materiais e técnicas construtivas"},
        {"d": "Qui", "s": "LEG", "t": "LGPD (Lei 13.709/2018) + revisão geral fechando toda a legislação"},
        {"d": "Sex", "s": "CE", "t": "Instalações hidrossanitárias prediais; materiais e técnicas construtivas"},
        {"d": "Sáb", "s": "REV", "t": "Revisão da semana + simulado misto (peso maior para CE e Legislação)"},
    ]},
    {"n": 7, "range": "07/09–12/09", "phase": "Semanas 7–10 · Consolidação", "days": [
        {"d": "Seg", "s": "CE", "t": "Sistemas estruturais; topografia; infraestrutura urbana"},
        {"d": "Ter", "s": "POR", "t": "Ortografia (emprego de letras, hífen, acentuação) + revisão rápida de fonologia"},
        {"d": "Qua", "s": "CE", "t": "Sistemas estruturais; topografia; infraestrutura urbana"},
        {"d": "Qui", "s": "LEG", "t": "Revisão espaçada: Estatuto dos Funcionários + Constituição Federal"},
        {"d": "Sex", "s": "CE", "t": "Sistemas estruturais; topografia; infraestrutura urbana"},
        {"d": "Sáb", "s": "REV", "t": "Simulado misto (~55–60% CE, ~20–25% Legislação, ~15–20% Português)"},
    ]},
    {"n": 8, "range": "14/09–19/09", "phase": "Semanas 7–10 · Consolidação", "days": [
        {"d": "Seg", "s": "CE", "t": "Desenho urbano; planejamento urbano; Estatuto da Cidade"},
        {"d": "Ter", "s": "POR", "t": "Morfologia: classes de palavras, flexões, formação de palavras, verbos"},
        {"d": "Qua", "s": "CE", "t": "Desenho urbano; planejamento urbano; Estatuto da Cidade"},
        {"d": "Qui", "s": "LEG", "t": "Revisão espaçada: Improbidade + Maria da Penha + ECA"},
        {"d": "Sex", "s": "CE", "t": "Desenho urbano; planejamento urbano; Estatuto da Cidade"},
        {"d": "Sáb", "s": "REV", "t": "Simulado misto (~55–60% CE, ~20–25% Legislação, ~15–20% Português)"},
    ]},
    {"n": 9, "range": "21/09–26/09", "phase": "Semanas 7–10 · Consolidação", "days": [
        {"d": "Seg", "s": "CE", "t": "Regularização fundiária urbana; parcelamento do solo urbano; política pública de habitação"},
        {"d": "Ter", "s": "POR", "t": "Sintaxe: regência, colocação pronominal, concordância verbal e nominal"},
        {"d": "Qua", "s": "CE", "t": "Regularização fundiária urbana; parcelamento do solo urbano; política pública de habitação"},
        {"d": "Qui", "s": "LEG", "t": "Revisão espaçada: Ética + DEMHAB + Lei de Responsabilidade Fiscal"},
        {"d": "Sex", "s": "CE", "t": "Regularização fundiária urbana; parcelamento do solo urbano; política pública de habitação"},
        {"d": "Sáb", "s": "REV", "t": "Simulado misto (~55–60% CE, ~20–25% Legislação, ~15–20% Português)"},
    ]},
    {"n": 10, "range": "28/09–03/10", "phase": "Semanas 7–10 · Consolidação", "days": [
        {"d": "Seg", "s": "CE", "t": "Habitação de interesse social + revisão geral de todos os temas de CE"},
        {"d": "Ter", "s": "POR", "t": "Interpretação de texto, figuras de linguagem + revisão geral + simulado de Português"},
        {"d": "Qua", "s": "CE", "t": "Habitação de interesse social + revisão geral de todos os temas de CE"},
        {"d": "Qui", "s": "LEG", "t": "Revisão espaçada: LGPD + simulado geral só de Legislação"},
        {"d": "Sex", "s": "CE", "t": "Habitação de interesse social + revisão geral de todos os temas de CE"},
        {"d": "Sáb", "s": "REV", "t": "Simulado misto (~55–60% CE, ~20–25% Legislação, ~15–20% Português)"},
    ]},
    {"n": 11, "range": "05/10–10/10", "phase": "Semanas 11–12 · Reta final", "days": [
        {"d": "Seg", "s": "CE", "t": "Simulado CE + correção"},
        {"d": "Ter", "s": "LEG", "t": "Simulado Legislação + correção (foco total nos pontos ainda decorados errado)"},
        {"d": "Qua", "s": "LEG", "t": "Revisão ativa do caderno de erros — Legislação"},
        {"d": "Qui", "s": "POR", "t": "Simulado Português + correção"},
        {"d": "Sex", "s": "CE", "t": "Revisão ativa do caderno de erros — CE"},
        {"d": "Sáb", "s": "REV", "t": "Simulado completo (as 3 matérias, tempo de prova) + correção detalhada"},
    ]},
    {"n": 12, "range": "12/10–16/10", "phase": "Semanas 11–12 · Reta final", "days": [
        {"d": "Seg", "s": "LEG", "t": "Revisão geral do caderno de erros — Legislação (sua maior lacuna)"},
        {"d": "Ter", "s": "CE", "t": "Revisão geral do caderno de erros — CE"},
        {"d": "Qua", "s": "POR", "t": "Revisão geral do caderno de erros — Português"},
        {"d": "Qui", "s": "REV", "t": "Simulado final curto, com peso extra em Legislação + correção"},
        {"d": "Sex", "s": "REV", "t": "Revisão leve: reler resumos e súmulas de todas as matérias; organizar material para a prova"},
    ]},
]


# ---------------------------------------------------------------------------
# Links oficiais por assunto (casamento por palavra-chave no texto do tópico)
# Leis federais: fonte Planalto. Leis/decretos municipais de Porto Alegre:
# fonte leismunicipais.com.br (portal de legislação consolidada).
# ---------------------------------------------------------------------------
KNOWN_LINKS = [
    ("Estatuto dos Funcionários Públicos",
     "Estatuto dos Funcionários Públicos de POA — LC 133/1985",
     "https://leismunicipais.com.br/a/rs/p/porto-alegre/lei-complementar/1985/13/133/"
     "lei-complementar-n-133-1985-estabelece-o-estatuto-dos-funcionarios-publicos-do-municipio-de-porto-alegre"),
    ("CF/1988",
     "Constituição Federal de 1988 — texto atualizado (Planalto)",
     "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm"),
    ("Lei Orgânica do Município de Porto Alegre",
     "Lei Orgânica do Município de Porto Alegre",
     "https://leismunicipais.com.br/lei-organica-porto-alegre-rs"),
    ("Improbidade Administrativa",
     "Lei nº 8.429/1992 — Lei de Improbidade Administrativa (Planalto)",
     "https://www.planalto.gov.br/ccivil_03/leis/l8429.htm"),
    ("Maria da Penha",
     "Lei nº 11.340/2006 — Lei Maria da Penha (Planalto)",
     "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11340.htm"),
    ("ECA (Lei 8.069/1990)",
     "Lei nº 8.069/1990 — Estatuto da Criança e do Adolescente (Planalto)",
     "https://www.planalto.gov.br/ccivil_03/leis/l8069.htm"),
    ("Ética no Serviço Público",
     "Decreto nº 21.071/2021 — Código de Ética, Conduta e Integridade de POA",
     "https://leismunicipais.com.br/a/rs/p/porto-alegre/decreto/2021/2108/21071/"
     "decreto-n-21071-2021-institui-o-codigo-de-etica-de-conduta-e-de-integridade-dos-agentes-publicos-e-da-alta-administracao-do-municipio-de-porto-alegre"),
    ("DEMHAB",
     "Lei nº 2.902/1965 — Cria o DEMHAB",
     "https://leismunicipais.com.br/a/rs/p/porto-alegre/lei-ordinaria/1965/291/2902/"
     "lei-ordinaria-n-2902-1965-fixa-diretrizes-para-a-politica-habitacional-do-municipio-reestrutura-sob-a-denominacao-de-departamento-municipal-de-habitacao-demhab-o-departamento-municipal-da-casa-popular-e-da-outras-providencias"),
    ("LRF (LC 101/2000)",
     "LC nº 101/2000 — Lei de Responsabilidade Fiscal (Planalto)",
     "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp101.htm"),
    ("LGPD (Lei 13.709/2018)",
     "Lei nº 13.709/2018 — LGPD (Planalto)",
     "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm"),
    ("Estatuto da Cidade",
     "Lei nº 10.257/2001 — Estatuto da Cidade (Planalto)",
     "https://www.planalto.gov.br/ccivil_03/leis/leis_2001/l10257.htm"),
]


def get_links(topic_text: str):
    """Retorna links relacionados ao tópico: matches diretos de legislação
    (quando existem) + links de pesquisa (Google e YouTube) como reforço de estudo."""
    links = []
    for keyword, label, url in KNOWN_LINKS:
        if keyword.lower() in topic_text.lower():
            links.append((label, url))

    search_term = topic_text.split(";")[0].split("(")[0].strip()
    query = quote_plus(f"{search_term} concurso arquiteto")
    links.append(("Pesquisar no Google", f"https://www.google.com/search?q={query}"))
    links.append(("Vídeos no YouTube", f"https://www.youtube.com/results?search_query={quote_plus(search_term)}"))
    return links


# ---------------------------------------------------------------------------
# Persistência simples em JSON
# ---------------------------------------------------------------------------
def day_id(week_n: int, idx: int) -> str:
    return f"w{week_n}-d{idx}"


def load_checks() -> dict:
    if os.path.exists(CHECKS_FILE):
        try:
            with open(CHECKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_checks(checks: dict) -> None:
    try:
        with open(CHECKS_FILE, "w", encoding="utf-8") as f:
            json.dump(checks, f, ensure_ascii=False, indent=2)
    except OSError:
        st.warning("Não foi possível salvar o progresso em disco.")


if "checks" not in st.session_state:
    st.session_state.checks = load_checks()


# ---------------------------------------------------------------------------
# CSS leve para os badges de matéria
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .badge {
        display: inline-block;
        font-family: monospace;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 3px;
        text-transform: uppercase;
        margin-right: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def badge_html(subject: str) -> str:
    color = SUBJECT_COLOR[subject]
    return f'<span class="badge" style="background:{color}22;color:{color};">{SUBJECT_LABEL[subject]}</span>'


# ---------------------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------------------
st.title("Cronograma de Estudos — Arquiteto Fundatec")
st.caption(
    "Período: 27/07/2026 — 16/10/2026 · Seg–Sex 19h–22h · Sáb 16h–21h · "
    "Peso na prova: CE 80 · Leg 10 · Port 10"
)

# ---------------------------------------------------------------------------
# Progresso geral
# ---------------------------------------------------------------------------
total_all = sum(len(w["days"]) for w in DATA)
done_all = sum(
    1
    for w in DATA
    for idx in range(len(w["days"]))
    if st.session_state.checks.get(day_id(w["n"], idx))
)
overall_pct = round(done_all / total_all * 100) if total_all else 0

st.progress(overall_pct / 100)
st.caption(f"Progresso geral: {done_all} / {total_all} itens ({overall_pct}%)")

# ---------------------------------------------------------------------------
# Filtro por matéria
# ---------------------------------------------------------------------------
filtro = st.radio(
    "Filtrar por matéria",
    options=["Todas", "CE", "Legislação", "Português", "Revisão/Simulado"],
    horizontal=True,
)
FILTER_MAP = {"Todas": None, "CE": "CE", "Legislação": "LEG", "Português": "POR", "Revisão/Simulado": "REV"}
subject_filter = FILTER_MAP[filtro]

if st.button("Zerar progresso"):
    st.session_state.checks = {}
    save_checks(st.session_state.checks)
    st.rerun()

st.divider()

# ---------------------------------------------------------------------------
# Semanas
# ---------------------------------------------------------------------------
last_phase = None
for week in DATA:
    if week["phase"] != last_phase:
        st.subheader(week["phase"])
        last_phase = week["phase"]

    week_total = len(week["days"])
    week_done = sum(
        1 for idx in range(week_total) if st.session_state.checks.get(day_id(week["n"], idx))
    )
    week_pct = round(week_done / week_total * 100) if week_total else 0

    with st.expander(f"Semana {week['n']} — {week['range']}  ·  {week_pct}%"):
        st.progress(week_pct / 100)
        for idx, day in enumerate(week["days"]):
            if subject_filter and day["s"] != subject_filter:
                continue
            did = day_id(week["n"], idx)
            checked = st.session_state.checks.get(did, False)

            col_chk, col_txt = st.columns([1, 11])
            with col_chk:
                new_val = st.checkbox("", value=checked, key=did, label_visibility="collapsed")
            with col_txt:
                if new_val:
                    st.markdown(f"~~{day['t']}~~ {badge_html(day['s'])} **{day['d']}**", unsafe_allow_html=True)
                else:
                    st.markdown(f"**{day['d']}**  {badge_html(day['s'])}  {day['t']}", unsafe_allow_html=True)

                links = get_links(day["t"])
                links_line = " &nbsp;·&nbsp; ".join(f"[{lbl}]({url})" for lbl, url in links)
                st.caption(links_line)

            if new_val != checked:
                st.session_state.checks[did] = new_val
                save_checks(st.session_state.checks)
                st.rerun()

st.divider()
st.caption("Marcações salvas automaticamente em progresso_cronograma.json")