import streamlit as st

# Títol simple
st.title("🍴 Gestor de Dinars")
st.subheader("All i oli i vinagreta")

# Inicialització de dades
if 'participants' not in st.session_state:
    st.session_state.participants = []

# Formulari a la part principal (sense barra lateral per evitar embolics)
with st.form("entrada", clear_on_submit=True):
    nom = st.text_input("Nom del participant")
    import_pagat = st.number_input("Import pagat (€)", min_value=0.0, step=0.01)
    afegir = st.form_submit_button("Afegir a la llista")

if afegir and nom:
    st.session_state.participants.append({"nom": nom, "pagat": import_pagat})

# Mostrar resultats
if st.session_state.participants:
    total = sum(p['pagat'] for p in st.session_state.participants)
    num = len(st.session_state.participants)
    per_cap = total / num if num > 0 else 0

    st.markdown(f"### Total: **{total:.2f} €** | Per cap: **{per_cap:.2f} €**")
    
    st.write("---")
    for i, p in enumerate(st.session_state.participants):
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(p['nom'])
        col2.write(f"{p['pagat']:.2f} €")
        if col3.button("Eliminar", key=f"del_{i}"):
            st.session_state.participants.pop(i)
            st.rerun()

    st.write("---")
    st.subheader("💰 Qui ha de pagar a qui:")
    
    # Lògica de liquidació
    deutes = []
    for p in st.session_state.participants:
        balanc = p['pagat'] - per_cap
        deutes.append({'nom': p['nom'], 'balanc': balanc})

    pagadors = [d for d in deutes if d['balanc'] < -0.01]
    cobradors = [d for d in deutes if d['balanc'] > 0.01]

    for p in pagadors:
        deute = abs(p['balanc'])
        for c in cobradors:
            if c['balanc'] <= 0: continue
            transfer = min(deute, c['balanc'])
            if transfer > 0.01:
                st.warning(f"**{p['nom']}** ha de pagar **{transfer:.2f} €** a **{c['nom']}**")
                deute -= transfer
                c['balanc'] -= transfer

    if st.button("Esborrar-ho tot i començar de nou"):
        st.session_state.participants = []
        st.rerun()
