import streamlit as st
from decimal import Decimal, getcontext

getcontext().prec = 4

st.set_page_config(page_title="Calculadora MVA Ajustado", page_icon="📊", layout="centered")

st.title("Calculadora MVA Ajustado")
st.caption("Cálculo do MVA Ajustado para ICMS-ST (Substituição Tributária).")

with st.form("mva_form"):
    mva_original = st.number_input(
        "MVA Original (%)", min_value=0.0, value=35.0, step=0.01, format="%.2f"
    )
    col1, col2 = st.columns(2)
    with col1:
        aliq_inter = st.number_input(
            "Alíquota Interestadual (%)", min_value=0.0, max_value=100.0, value=12.0, step=0.01, format="%.2f"
        )
    with col2:
        aliq_intra = st.number_input(
            "Alíquota Intraestadual (%)", min_value=0.0, max_value=100.0, value=18.0, step=0.01, format="%.2f"
        )

    calcular = st.form_submit_button("Calcular", use_container_width=True)

if calcular:
    mva_orig_dec = Decimal(str(mva_original)) / 100
    aliq_inter_dec = Decimal(str(aliq_inter)) / 100
    aliq_intra_dec = Decimal(str(aliq_intra)) / 100

    denominador = 1 - aliq_intra_dec

    if denominador <= 0:
        st.error("Alíquota intraestadual inválida — divisão por zero.")
    else:
        mva_ajustado = ((((1 + mva_orig_dec) * (1 - aliq_inter_dec)) / denominador) - 1) * 100

        st.divider()
        st.subheader("Resultado")
        st.metric("MVA Ajustado", f"{mva_ajustado:.4f}%".replace(".", ","))

        st.caption(
            f"MVA Original: {mva_original:.2f}%  |  "
            f"Alíq. Interestadual: {aliq_inter:.2f}%  |  "
            f"Alíq. Intraestadual: {aliq_intra:.2f}%"
        )

with st.expander("Entenda o MVA Ajustado"):
    st.write(
        "O **MVA Ajustado** é utilizado nas operações interestaduais com ICMS-ST (Substituição Tributária). "
        "Quando o remetente e o destinatário estão em estados com alíquotas diferentes, a MVA original "
        "precisa ser ajustada para neutralizar o efeito da diferença de alíquotas, garantindo que a "
        "base de cálculo do ICMS-ST reflita corretamente o valor final ao consumidor."
    )
