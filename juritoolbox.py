# app.py
import streamlit as st

# ----------------------------------
# Funções auxiliares
# ----------------------------------
def pct_to_factor(pct_int):
    return 1 + (pct_int / 100.0)

# ----------------------------------
# Interface principal
# ----------------------------------
st.set_page_config(page_title="JuriToolbox — ANPP e Dosimetria", page_icon="⚖️", layout="wide")
st.title("⚖️ JuriToolbox")
st.caption("Ferramenta jurídica educacional — ANPP (art. 28-A CPP) e Dosimetria (art. 59 CP).")

with st.sidebar:
    st.header("Módulos")
    modulo = st.radio(
        "Escolha o módulo:",
        ["Elegibilidade ANPP (art. 28-A CPP)", "Dosimetria Simplificada (art. 59 CP)"]
    )
    st.markdown("---")
    st.markdown("**Aviso:** uso acadêmico. Sempre confira a legislação e a jurisprudência atualizadas.")

# ----------------------------------
# Módulo 1 — ANPP
# ----------------------------------
if modulo == "Elegibilidade ANPP (art. 28-A CPP)":
    st.subheader("🤝 Elegibilidade ao Acordo de Não Persecução Penal (ANPP)")
    st.caption("Checklist educacional com base no art. 28-A do Código de Processo Penal.")

    col1, col2 = st.columns(2)
    with col1:
        pena_min = st.number_input("Pena mínima cominada (em anos)", min_value=0.0, value=1.0, step=0.5)
        violencia = st.selectbox("Houve violência ou grave ameaça?", ["Não", "Sim"])
        confissao = st.selectbox("Há confissão formal/circunstancial?", ["Sim", "Não"])
    with col2:
        reincidente = st.selectbox("Reincidência específica em crime doloso?", ["Não", "Sim"])
        habitual = st.selectbox("Agente habitual/profissional (reiteração delitiva)?", ["Não", "Sim"])
        hediondo = st.selectbox("Crime hediondo/equiparado ou violência doméstica grave?", ["Não", "Sim"])

    if st.button("Verificar elegibilidade"):
        motivos = []
        elegivel = True

        # regras simplificadas
        if pena_min >= 4:
            elegivel = False; motivos.append("Pena mínima igual ou superior a 4 anos.")
        if violencia == "Sim":
            elegivel = False; motivos.append("Crime com violência ou grave ameaça.")
        if confissao == "Não":
            elegivel = False; motivos.append("Ausência de confissão formal/circunstancial.")
        if reincidente == "Sim":
            elegivel = False; motivos.append("Reincidência específica em crime doloso.")
        if habitual == "Sim":
            elegivel = False; motivos.append("Habitualidade/profissionalidade (reiteração delitiva).")
        if hediondo == "Sim":
            elegivel = False; motivos.append("Crime hediondo/equiparado ou violência doméstica grave.")

        if elegivel:
            st.success("✅ **Elegível**, em tese, ao ANPP (art. 28-A CPP).")
            st.write("**Justificativa:** pena mínima inferior a 4 anos, sem violência ou grave ameaça, com confissão e sem impedimentos legais aparentes.")
        else:
            st.error("❌ **Não elegível**, em tese, ao ANPP (art. 28-A CPP).")
            st.write("**Motivos:**\n- " + "\n- ".join(motivos))
            st.info("Análise **didática**; verifique exceções e jurisprudência atual.")

# ----------------------------------
# Módulo 2 — Dosimetria Simplificada
# ----------------------------------
elif modulo == "Dosimetria Simplificada (art. 59 CP)":
    st.subheader("⚖️ Dosimetria Simplificada — Pena-Base e Ajustes")
    st.caption("Ferramenta pedagógica (percentuais ilustrativos).")

    with st.expander("Parâmetros do tipo penal"):
        min_anos = st.number_input("Pena mínima (anos)", min_value=0.0, value=1.0, step=0.5)
        max_anos = st.number_input("Pena máxima (anos)", min_value=0.5, value=5.0, step=0.5)
        if max_anos < min_anos:
            st.warning("A pena máxima deve ser maior que a mínima.")
        pena_base = (min_anos + max_anos) / 2.0
        st.write(f"Pena-base inicial (média): **{pena_base:.2f} anos**")

    st.markdown("### Circunstâncias judiciais (art. 59 CP)")
    st.caption("Use −1 (desfavorável), 0 (neutra) ou +1 (favorável). Cada ponto altera ±10 % da pena-base.")
    labels = [
        "Culpabilidade", "Antecedentes", "Conduta social", "Personalidade",
        "Motivos", "Circunstâncias", "Consequências", "Comportamento da vítima"
    ]
    cols = st.columns(4)
    valores = []
    for i, lab in enumerate(labels):
        with cols[i % 4]:
            valores.append(st.slider(lab, -1, 1, 0))

    ajuste_pct = 10
    total = sum(valores)
    fator = pct_to_factor(total * ajuste_pct)
    pena_fase1 = max(min_anos, min(max_anos, pena_base * fator))
    st.write(f"**Pena após art. 59 (didática): {pena_fase1:.2f} anos**")

    colL, colR = st.columns(2)
    with colL:
        minorantes = st.multiselect(
            "Minorantes",
            ["Confissão espontânea (−10 %)", "Tentativa (−33 %)", "Menoridade relativa (−5 %)", "Participação de menor importância (−20 %)"]
        )
    with colR:
        majorantes = st.multiselect(
            "Majorantes",
            ["Concurso de agentes (+20 %)", "Emprego de arma (+20 %)", "Motivo fútil/torpe (+30 %)", "Crime contra vulnerável (+50 %)"]
        )

    resultado = pena_fase1
    for m in minorantes:
        if "(−33" in m:   resultado *= pct_to_factor(-33)
        elif "(−20" in m: resultado *= pct_to_factor(-20)
        elif "(−10" in m: resultado *= pct_to_factor(-10)
        elif "(−5"  in m: resultado *= pct_to_factor(-5)
    for M in majorantes:
        if "(+50" in M:   resultado *= pct_to_factor(+50)
        elif "(+30" in M: resultado *= pct_to_factor(+30)
        elif "(+20" in M: resultado *= pct_to_factor(+20)

    resultado = max(min_anos, min(max_anos, resultado))
    st.success(f"**Pena provisória (didática): {resultado:.2f} anos**")

    fundamentos = []
    for lab, val in zip(labels, valores):
        if val == -1:
            fundamentos.append(f"{lab}: desfavorável (+{ajuste_pct} %).")
        elif val == +1:
            fundamentos.append(f"{lab}: favorável (−{ajuste_pct} %).")
        else:
            fundamentos.append(f"{lab}: neutra.")

    texto = f"""
Pena-base entre {min_anos:.2f} e {max_anos:.2f} anos; adotada a média ({pena_base:.2f} anos).
Art. 59 CP:
- """ + "\n- ".join(fundamentos) + f"""

Após a 1ª fase, pena provisória: {pena_fase1:.2f} anos (ilustrativa).
Aplicadas minorantes/majorantes selecionadas (percentuais pedagógicos).
Pena resultante (limitada ao tipo): {resultado:.2f} anos.
"""
    st.markdown("### Rascunho de fundamentação")
    st.code(texto.strip(), language="markdown")

st.markdown("---")
st.caption("JuriToolbox — uso acadêmico. Verifique legislação e jurisprudência atualizadas.")
