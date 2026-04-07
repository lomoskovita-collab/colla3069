import streamlit as st

# Configuració bàsica
st.set_page_config(page_title="Gestor 3069", page_icon="🍴")

st.title("🍴 Gestor de Dinars")
st.subheader("All i oli i vinagreta")

# Inicialització de la llista de participants
if 'participants' not in st.session_state:
    st.session_state.participants = []

# --- FORMULARI D'ENTRADA ---
with st.form("entrada", clear_on_submit=True):
    col_nom, col_import = st.columns([2, 1])
    with col_nom:
        nom = st.text_input("Nom del participant")
    with col_import:
        import_pagat = st.number_input("Pagat (€)", min_value=0.0, step=0.01)
    
    botó_afegir = st.form_submit_button("AFEGIR A LA LLISTA")

if botó_afegir and nom:
    st.session_state.participants.append({"nom": nom, "pagat": import_pagat})

# --- MOSTRAR DADES I ELIMINAR ---
if st.session_state.participants:
    st.write("---")
    
    total = sum(p['pagat'] for p in st.session_state.participants)
    num = len(st.session_state.participants)
    per_cap = total / num if num > 0 else 0

    st.info(f"**Total: {total:.2f} €** |  **Per cap: {per_cap:.2f} €**")
    
    st.markdown("### 📝 Llista de Participants")
    
    # Bucle per mostrar cada persona amb el seu botó d'eliminar
    for i, p in enumerate(st.session_state.participants):
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"👤 {p['nom']}")
        col2.write(f"{p['pagat']:.2f} €")
        # El botó d'eliminar és aquí:
        if col3.button("Borrar", key=f"btn_{i}"):
            st.session_state.participants.pop(i)
            st.rerun()

    # --- LIQUIDACIÓ DE DEUTES ---
    st.write("---")
    st.subheader("💰 Qui ha de pagar a qui:")
    
    deutes = []
    for p in st.session_state.participants:
        balanc = p['pagat'] - per_cap
        deutes.append({'nom': p['nom'], 'balanc': balanc})

    pagadors = sorted([d for d in deutes if d['balanc'] < -0.01], key=lambda x: x['balanc'])
    cobradors = sorted([d for d in deutes if d['balanc'] > 0.01], key=lambda x: x['balanc'], reverse=True)

    for p in pagadors:
        deute_restant = abs(p['balanc'])
        for c in cobradors:
            if c['balanc'] <= 0: continue
            import_transf = min(deute_restant, c['balanc'])
            if import_transf > 0.01:
                st.warning(f"👉 **{p['nom']}** ha de pagar **{import_transf:.2f} €** a **{c['nom']}**")
                deute_restant -= import_transf
                c['balanc'] -= import_transf

    # Botó per netejar-ho tot
    st.write("")
    if st.button("Esborrar tota la llista"):
        st.session_state.participants = []
        st.rerun()
else:
    st.write("Encara no hi ha ningú a la llista. Comença a escriure noms!")
        
