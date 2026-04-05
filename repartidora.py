import streamlit as st
import os

# 1. CONFIGURACIÓ DE LA PÀGINA (Sempre a dalt de tot)
st.set_page_config(
    page_title="Trobades 3069",
    page_icon="🐌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTIL PERSONALITZAT (Colors i amagar menús en anglès)
st.markdown("""
    <style>
    /* Color de fons de la web */
    .stApp {
        background-color: #f0f4f0;
    }
    /* Estil de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #1e3d2f;
        color: white;
    }
    /* Amagar el menú de Streamlit i el "Made with Streamlit" */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Botons personalitzats */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1e3d2f;
        color: #d4af37;
        border: 1px solid #d4af37;
    }
    </style>
    """, unsafe_allow_stdio=True, unsafe_allow_html=True)

# 3. LOGO I TÍTOL A LA BARRA LATERAL
with st.sidebar:
    # Intentem carregar la imatge del cargol
    if os.path.exists("cargol.jpg"):
        st.image("cargol.jpg", width=200)
    else:
        st.title("🐌 TROBADES 3069")
    
    st.markdown("---")
    st.subheader("➕ Afegir Participant")
    
    # Formulari d'entrada
    with st.form("entrada_dades", clear_on_submit=True):
        nom = st.text_input("Nom")
        import_pagat = st.number_input("Import pagat (€)", min_value=0.0, step=0.01, format="%.2f")
        botó_afegir = st.form_submit_input("DESAR")

# 4. GESTIÓ DE DADES (Session State)
if 'participants' not in st.session_state:
    st.session_state.participants = []

if botó_afegir and nom:
    st.session_state.participants.append({"nom": nom, "pagat": import_pagat})

# 5. PANTALLA PRINCIPAL
st.title("🍴 Gestor de Dinars")
st.subheader("All i oli i vinagreta")
st.markdown("---")

if not st.session_state.participants:
    st.info("Comença afegint algú des de la barra lateral de l'esquerra! 👈")
else:
    # Càlculs
    total_dinars = sum(p['pagat'] for p in st.session_state.participants)
    num_persones = len(st.session_state.participants)
    per_cap = total_dinars / num_persones if num_persones > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("TOTAL DINAR", f"{total_dinars:.2f} €")
    with col2:
        st.metric("A PAGAR PER CAP", f"{per_cap:.2f} €")

    st.markdown("### 📝 Detall")
    for i, p in enumerate(st.session_state.participants):
        col_n, col_p, col_b = st.columns([3, 2, 1])
        with col_n:
            st.write(f"**{p['nom']}**")
        with col_p:
            st.write(f"{p['pagat']:.2f} €")
        with col_b:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.participants.pop(i)
                st.rerun()

    st.markdown("---")
    st.markdown("### 💰 Liquidació")
    
    # Lògica de qui deu a qui
    deutes = []
    for p in st.session_state.participants:
        balanç = p['pagat'] - per_cap
        deutes.append({'nom': p['nom'], 'balanç': balanç})

    pagadors = sorted([d for d in deutes if d['balanç'] < -0.01], key=lambda x: x['balanç'])
    cobradors = sorted([d for d in deutes if d['balanç'] > 0.01], key=lambda x: x['balanç'], reverse=True)

    if not pagadors and not cobradors:
        st.success("Tothom està al corrent de pagament! ✅")
    else:
        for p in pagadors:
            deute_actual = abs(p['balanç'])
            for c in cobradors:
                if c['balanç'] <= 0: continue
                import_transferencia = min(deute_actual, c['balanç'])
                if import_transferencia > 0.01:
                    st.success(f"**{p['nom']}** ha de pagar **{import_transferencia:.2f} €** a **{c['nom']}**")
                    deute_actual -= import_transferencia
                    c['balanç'] -= import_transferencia

    if st.button("Esborrar-ho tot"):
        st.session_state.participants = []
        st.rerun()
