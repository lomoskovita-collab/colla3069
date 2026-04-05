import streamlit as st
import os

# 1. CONFIGURACIÓ DE LA PÀGINA
st.set_page_config(
    page_title="Trobades 3069",
    page_icon="🐌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTIL PERSONALITZAT
st.markdown("""
    <style>
    .stApp { background-color: #f0f4f0; }
    [data-testid="stSidebar"] { background-color: #1e3d2f; color: white; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #1e3d2f;
        color: #d4af37;
        border: 1px solid #d4af37;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    st.title("🐌 TROBADES 3069")
    st.markdown("---")
    st.subheader("➕ Afegir Participant")
    
    with st.form("entrada_dades", clear_on_submit=True):
        nom = st.text_input("Nom")
        import_pagat = st.number_input("Import pagat (€)", min_value=0.0, step=0.01, format="%.2f")
        boto_afegir = st.form_submit_button("DESAR")

# 4. GESTIÓ DE DADES
if 'participants' not in st.session_state:
    st.session_state.participants = []

if boto_afegir and nom:
    st.session_state.participants.append({"nom": nom, "pagat": import_pagat})

# 5. PANTALLA PRINCIPAL
st.title("🍴 Gestor de Dinars")
st.subheader("All i oli i vinagreta")
st.markdown("---")

if not st.session_state.participants:
    st.info("Comença afegint algú des de la barra lateral de l'esquerra! 👈")
else:
    total_dinars = sum(p['pagat'] for p in st.session_state.participants)
    num_persones = len(st.session_state.participants)
    per_cap = total_dinars / num_persones if num_persones > 0 else 0

    c1, c2 = st.columns(2)
    c1.metric("TOTAL DINAR", f"{total_dinars:.2f} €")
    c2.metric("A PAGAR PER CAP", f"{per_cap:.2f} €")

    st.markdown("### 📝 Detall")
    for i, p in enumerate(st.session_state.participants):
        col_n, col_p, col_b = st.columns([3, 2, 1])
        col_n.write(f"**{p['nom']}**")
        col_p.write(f"{p['pagat']:.2f} €")
        if col_b.button("🗑️", key=f"del_{i}"):
            st.session_state.participants.pop(i)
            st.rerun()

    st.markdown("---")
    st.markdown("### 💰 Liquidació")
    
    deutes = []
    for p in st.session_state.participants:
        balanc = p['pagat'] - per_cap
        deutes.append({'nom': p['nom'], 'balanc': balanc})

    pagadors = sorted([d for d in deutes if d['balanc'] < -0.01], key=lambda x: x['balanc'])
    cobradors = sorted([d for d in deutes if d['balanc'] > 0.01], key=lambda x: x['balanc'], reverse=True)

    for p in pagadors:
        deute_actual = abs(p['balanc'])
        for c in cobradors:
            if c['balanc'] <= 0: continue
            imp = min(deute_actual, c['balanc'])
            if imp > 0.01:
                st.success(f"**{p['nom']}** ha de pagar **{imp:.2f} €** a **{c['nom']}**")
                deute_actual -= imp
                c['balanc'] -= imp

    if st.button("Esborrar-ho tot"):
        st.session_state.participants = []
        st.rerun()
