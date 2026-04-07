import streamlit as st

# 1. CONFIGURACIÓ I ESTILS (Colors verd fluix i verd fort)
st.set_page_config(page_title="Trobades 3069", page_icon="🐌", layout="centered")

st.markdown("""
    <style>
    /* Fons de la pàgina verd molt fluix */
    .stApp {
        background-color: #f0f7f0;
    }
    /* Botons en verd fort amb lletres daurades/blanques */
    .stButton>button {
        background-color: #1e3d2f !important;
        color: white !important;
        border-radius: 8px;
        border: 1px solid #d4af37;
    }
    /* Targetes de resultats */
    .stAlert {
        background-color: #ffffff;
        border: 1px solid #1e3d2f;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍴 Gestor de Dinars")
st.subheader("All i oli i vinagreta 🐌")
st.markdown("---")

# 2. INICIALITZACIÓ DE DADES
if 'participants' not in st.session_state:
    st.session_state.participants = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# 3. FORMULARI D'ENTRADA / EDICIÓ
# Si estem editant, omplim els camps amb les dades velles
default_nom = ""
default_imp = 0.0
if st.session_state.edit_index is not None:
    idx = st.session_state.edit_index
    default_nom = st.session_state.participants[idx]['nom']
    default_imp = st.session_state.participants[idx]['pagat']
    st.info(f"📝 Editant a: **{default_nom}**")

with st.form("formulari", clear_on_submit=True):
    c1, c2 = st.columns([2, 1])
    nom_input = c1.text_input("Nom", value=default_nom)
    imp_input = c2.number_input("Pagat (€)", min_value=0.0, step=0.01, value=default_imp)
    
    text_boto = "GUARDAR CANVIS" if st.session_state.edit_index is not None else "AFEGIR A LA LLISTA"
    submit = st.form_submit_button(text_boto)

if submit and nom_input:
    if st.session_state.edit_index is not None:
        # Actualitzem el que ja existeix
        st.session_state.participants[st.session_state.edit_index] = {"nom": nom_input, "pagat": imp_input}
        st.session_state.edit_index = None # Sortim del mode edició
    else:
        # Afegim un de nou
        st.session_state.participants.append({"nom": nom_input, "pagat": imp_input})
    st.rerun()

# 4. LLISTA I CALCULS
if st.session_state.participants:
    total = sum(p['pagat'] for p in st.session_state.participants)
    per_cap = total / len(st.session_state.participants)

    st.success(f"💰 **TOTAL: {total:.2f} €** |  👤 **PER CAP: {per_cap:.2f} €**")
    
    st.markdown("### 📋 Detall de la colla")
    
    for i, p in enumerate(st.session_state.participants):
        col_dades, col_edit, col_del = st.columns([4, 1, 1])
        
        col_dades.write(f"**{p['nom']}**: {p['pagat']:.2f} €")
        
        # Botó Editar (Llapis)
        if col_edit.button("✏️", key=f"edit_{i}"):
            st.session_state.edit_index = i
            st.rerun()
            
        # Botó Eliminar (Paperera)
        if col_del.button("🗑️", key=f"del_{i}"):
            st.session_state.participants.pop(i)
            if st.session_state.edit_index == i:
                st.session_state.edit_index = None
            st.rerun()

    # 5. LIQUIDACIÓ
    st.markdown("---")
    st.subheader("⚖️ Qui ha de pagar a qui")
    
    deutes = []
    for p in st.session_state.participants:
        balanc = p['pagat'] - per_cap
        deutes.append({'nom': p['nom'], 'balanc': balanc})

    pagadors = sorted([d for d in deutes if d['balanc'] < -0.01], key=lambda x: x['balanc'])
    cobradors = sorted([d for d in deutes if d['balanc'] > 0.01], key=lambda x: x['balanc'], reverse=True)

    for p in pagadors:
        falta = abs(p['balanc'])
        for c in cobradors:
            if c['balanc'] <= 0: continue
            donar = min(falta, c['balanc'])
            if donar > 0.01:
                st.warning(f"**{p['nom']}** 👉 **{donar:.2f} €** a **{c['nom']}**")
                falta -= donar
                c['balanc'] -= donar

    if st.button("Esborrar-ho tot"):
        st.session_state.participants = []
        st.session_state.edit_index = None
        st.rerun()
