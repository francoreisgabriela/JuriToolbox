# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date

# ----------------------------------
# Utilidades
# ----------------------------------
def parse_date_only(d):
    if isinstance(d, date):
        return d
    if isinstance(d, datetime):
        return d.date()
    return datetime.strptime(d, "%Y-%m-%d").date()

def load_holidays_from_csv(file):
    """
    Lê um CSV com 1 coluna de datas.
    Aceita cabeçalho 'date' ou sem cabeçalho.
    Formatos aceitos: YYYY-MM-DD, DD/MM/YYYY, etc. (o pandas tenta inferir)
    """
    try:
        df = pd.read_csv(file)
        # escolhe a primeira coluna se não houver 'date'
        col = 'date' if 'date' in df.columns else df.columns[0]
        # força parse para datetime e pega somente a parte date
        dates = pd.to_datetime(df[col], dayfirst=True, errors='coerce').dt.date
        dates = dates.dropna()
        return set(dates.tolist())
    except Exception:
        return set()

def is_business_day(d: date, holidays: set):
    # Seg(0) a Sex(4) são úteis; Sáb(5) e Dom(6) não
    return d.weekday() < 5 and d not in holidays

def add_business_days(start_date: date, n_days: int, holidays: set):
    """
    Exclui o dia do começo e conta 'n_days' dias úteis.
    Se o último cair em não útil, prorroga.
    """
    current = start_date + timedelta(days=1)  # exclui o dia do começo
    counted = 0
    while counted < n_days:
        if is_business_day(current, holidays):
            counted += 1
            if counted == n_days:
                break
        current += timedelta(days=1)
    # se último não for útil, empurra até o próximo útil
    while not is_business_day(current, holidays):
        current += timedelta(days=1)
    return current

def add_calendar_days(start_date: date, n_days: int):
    # Contagem corrida simples: exclui o dia do começo
    return start_date + timedelta(days=n_days)

def pct_to_factor(pct_int):
    return 1 + (pct_int / 100.0)

# ----------------------------------
# App
# ----------------------------------
st.set_page_config(page_title="JuriToolbox — Prazos, ANPP e Dosimetria", page_icon="⚖️", layout="wide")
st.title("⚖️ JuriToolbox")
st.caption("Caixa de ferramentas jurídica educacional — prazos (CPC/CPP), elegibilidade ao ANPP (art. 28-A CPP) e dosimetria (art. 59 CP).")

with st.sidebar:
    st.header("Módulos")
    modulo = st.radio(
        "Escolha o módulo:",
        ["Calculadora de Prazos", "Elegibilidade ANPP (art. 28-A CPP)", "Dosimetria Simplificada (art. 59 CP)"]
    )
    st.markdown("---")
    st.markdown("**Aviso**: uso acadêmico/educacional. Sempre confira a legislação e a jurisprudência.")
    st.markdown("---")
    st.markdown("Se algo falhar, confira o **requirements.txt** e atualize o cache no Streamlit Cloud.")

# ----------------------------------
# Módulo 1 — Prazos
# ----------------------------------
if modulo == "Calculadora de Prazos":
    st.subheader("🗓️ Calculadora de Prazos Processuais")

    colA, colB = st.columns(2)
    with colA:
        rito = st.selectbox("Rito / referência", ["CPC (dias úteis)", "CPP (dias corridos, salvo regra específica)"])
        data_inicial = st.date_input("Data do início do prazo", value=date.today())
        qtd_dias = st.number_input("Quantidade de dias", min_value=1, value=15, step=1)
        cpp_contar_uteis = st.checkbox("No CPP, simular contagem em dias úteis?", value=False)
    with colB:
        feriados_file = st.file_uploader("Feriados (CSV; uma coluna de datas)", type=["csv"])
        prorrogar_nao_util = st.checkbox("Prorrogar se cair em dia não útil", value=True)

    holidays = set()
    if feriados_file is not None:
        holidays = load_holidays_from_csv(feriados_file)
        if holidays:
            st.success(f"Feriados carregados: {len(holidays)} data(s).")
        else:
            st.warning("Não consegui ler feriados. Verifique o CSV (uma coluna com datas).")

    if st.button("Calcular prazo"):
        try:
            start = parse_date_only(str(data_inicial))
            if "CPC" in rito or (("CPP" in rito) and cpp_contar_uteis):
                end_date = add_business_days(start, int(qtd_dias), holidays)
            else:
                end_date = add_calendar_days(start, int(qtd_dias))
                if prorrogar_nao_util:
                    while not is_business_day(end_date, holidays):
                        end_date += timedelta(days=1)

            st.success(f"**Data final estimada:** {end_date.strftime('%d/%m/%Y')}")

            # tabela simples de timeline
            rows = []
            cur = start + timedelta(days=1)
            limite = (end_date - start).days + 1
            dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
            for _ in range(limite):
                rows.append({
                    "Data": cur.strftime("%d/%m/%Y"),
                    "Dia da semana": dias_semana[cur.weekday()],
                    "Útil?": "Sim" if is_business_day(cur, holidays) else "Não",
                    "Feriado?": "Sim" if cur in holidays else "Não",
                })
                cur += timedelta(days=1)
            st.dataframe(pd.DataFrame(rows))
            st.info("Regra didática: exclui-se o dia do começo. Em dias úteis, prorroga-se se o prazo vencer em não útil.")
        except Exception as e:
            st.error("Falha ao calcular o prazo.")
            st.exception(e)

# ----------------------------------
# Módulo 2 — ANPP
# ----------------------------------
elif modulo == "Elegibilidade ANPP (art. 28-A CPP)":
    st.subheader("🤝 Elegibilidade ao Acordo de Não Persecução Penal (ANPP)")
    st.caption("Checklist educacional simplificado, com base no art. 28-A do CPP.")

    c1, c2 = st.columns(2)
    with c1:
        pena_min = st.number_input("Pena mínima cominada (anos)", min_value=0.0, value=1.0, step=0.5)
        violencia = st.selectbox("Violência ou grave ameaça?", ["Não", "Sim"])
        confissao = st.selectbox("Há confissão formal/circunstancial?", ["Sim", "Não"])
    with c2:
        reincidente = st.selectbox("Reincidência específica dolosa?", ["Não", "Sim"])
        habitual = st.selectbox("Agente habitual/profissional (reiteração)?", ["Não", "Sim"])
        hediondo = st.selectbox("Hediondo/equiparado ou violência doméstica grave?", ["Não", "Sim"])

    if st.button("Verificar elegibilidade"):
        try:
            motivos = []
            elegivel = True
            if pena_min >= 4:
                elegivel = False; motivos.append("Pena mínima ≥ 4 anos.")
            if violencia == "Sim":
                elegivel = False; motivos.append("Violência ou grave ameaça.")
            if confissao == "Não":
                elegivel = False; motivos.append("Sem confissão.")
            if reincidente == "Sim":
                elegivel = False; motivos.append("Reincidência específica em crime doloso.")
            if habitual == "Sim":
                elegivel = False; motivos.append("Habitualidade/profissionalidade (reiteração).")
            if hediondo == "Sim":
                elegivel = False; motivos.append("Hediondo/equiparado ou violência doméstica grave.")

            if elegivel:
                st.success("✅ Elegível, em tese, ao ANPP (art. 28-A).")
                st.write("**Justificativa:** pena mínima < 4 anos, sem violência/grave ameaça, com confissão e sem impedimentos legais aparentes.")
            else:
                st.error("❌ Não elegível, em tese, ao ANPP.")
                st.write("**Motivos:**\n- " + "\n- ".join(motivos))
                st.info("Análise didática; verifique exceções e jurisprudência.")
        except Exception as e:
            st.error("Falha ao avaliar ANPP.")
            st.exception(e)

# ----------------------------------
# Módulo 3 — Dosimetria
# ----------------------------------
elif modulo == "Dosimetria Simplificada (art. 59 CP)":
    st.subheader("⚖️ Dosimetria Simplificada (art. 59 CP)")
    st.caption("Ferramenta pedagógica. Percentuais ilustrativos.")

    with st.expander("Parâmetros do tipo penal"):
        min_anos = st.number_input("Pena mínima (anos)", min_value=0.0, value=1.0, step=0.5)
        max_anos = st.number_input("Pena máxima (anos)", min_value=0.5, value=5.0, step=0.5)
        if max_anos < min_anos:
            st.warning("A pena máxima deve ser maior que a mínima.")
        pena_base = (min_anos + max_anos) / 2.0
        st.write(f"Pena-base inicial (média): **{pena_base:.2f} anos**")

    st.markdown("### Circunstâncias judiciais (use -1, 0, +1)")
    labels = [
        "Culpabilidade","Antecedentes","Conduta social","Personalidade",
        "Motivos","Circunstâncias","Consequências","Comportamento da vítima"
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
    st.write(f"**Após art. 59 (didático): {pena_fase1:.2f} anos**")

    colL, colR = st.columns(2)
    with colL:
        minorantes = st.multiselect(
            "Minorantes",
            ["Confissão espontânea (-10%)", "Tentativa (-33%)", "Menoridade relativa (-5%)", "Participação de menor importância (-20%)"]
        )
    with colR:
        majorantes = st.multiselect(
            "Majorantes",
            ["Concurso de agentes (+20%)", "Emprego de arma (+20%)", "Motivo fútil/torpe (+30%)", "Crime contra vulnerável (+50%)"]
        )

    try:
        resultado = pena_fase1
        for m in minorantes:
            if "(-33%)" in m:   resultado *= pct_to_factor(-33)
            elif "(-20%)" in m: resultado *= pct_to_factor(-20)
            elif "(-10%)" in m: resultado *= pct_to_factor(-10)
            elif "(-5%)"  in m: resultado *= pct_to_factor(-5)

        for M in majorantes:
            if "(+50%)" in M:   resultado *= pct_to_factor(+50)
            elif "(+30%)" in M: resultado *= pct_to_factor(+30)
            elif "(+20%)" in M: resultado *= pct_to_factor(+20)

        resultado = max(min_anos, min(max_anos, resultado))
        st.success(f"**Pena provisória (didática): {resultado:.2f} anos**")

        fundamentos = []
        for lab, val in zip(labels, valores):
            if val == -1:
                fundamentos.append(f"{lab}: desfavorável (+{ajuste_pct}%).")
            elif val == +1:
                fundamentos.append(f"{lab}: favorável (-{ajuste_pct}%).")
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

    except Exception as e:
        st.error("Falha no cálculo da dosimetria.")
        st.exception(e)

# Rodapé
st.markdown("---")
st.caption("JuriToolbox — uso acadêmico; confira a legislação e jurisprudência atualizadas.")
