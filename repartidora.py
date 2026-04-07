import streamlit as st

# 1. Configuració de la pàgina
st.set_page_config(page_title="Gestor 3069", page_icon="🍴", layout="centered")

st.title("🍴 Gestor de Dinars")
st.subheader("All i oli i vinagreta")
st.markdown("---")

# 2. Inicialització de dades
if 'participants' not in st.session_state:
    st.session_state.participants = []

# 3. Formulari per afegir gent
with st.form("entrada", clear_on_submit=True):
    c_nom, c_import = st.columns([2, 1])
    with c_nom:
        nom = st.text_input("Nom del participant (Ex: Ricard)")
    with c_import:
        imp = st.number_input("Pagat (€)", min_value=0.0, step=0.01, format="%.2f")
    
    submit = st.form_submit_button("AFEGIR A LA LLISTA")

if submit and nom:
    st.session_state.participants.append({"nom": nom, "pagat": imp})
    st.rerun()

# 4. Llista i càlculs
if st.session_state.participants:
    total = sum(p['pagat'] for p in st.session_state.participants)
    num = len(st.session_state.participants)
    per_cap = total / num if num > 0 else 0

    # Resum destacat
    st.success(f"💰 **Total: {total:.2f} €** |  👤 **Per cap: {per_cap:.2f} €**")
    
    st.markdown("### 📝 Llista i correccions")
    for i, p in enumerate(st.session_state.participants):
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{p['nom']}**")
        col2.write(f"{p['pagat']:.2f} €")
        # Botó d'eliminar/editar
        if col3.button("Borrar", key=f"del_{i}"):
            st.session_state.participants.pop(i)
            st.rerun()

    # 5. Liquidació (Qui deu a qui)
    st.markdown("---")
    st.subheader("⚖️ Balanç de comptes")
    
    deutes = []
    for p in st.session_state.participants:
        balanc = p['pagat'] - per_cap
        deutes.append({'nom': p['nom'], 'balanc': balanc})

    pagadors = sorted([d for d in deutes if d['balanc'] < -0.01], key=lambda x: x['balanc'])
    cobradors = sorted([d for d in deutes if d['balanc'] > 0.01], key=lambda x: x['balanc'], reverse=True)

    if not pagadors and not cobradors:
        st.write("Tothom està al dia! ✅")
    else:
        for p in pagadors:
            falta = abs(p['balanc'])
            for c in cobradors:
                if c['balanc'] <= 0: continue
                donar = min(falta, c['balanc'])
                if donar > 0.01:
                    st.warning(f"**{p['nom']}** ha de pagar **{donar:.2f} €** a **{c['nom']}**")
                    falta -= donar
                    c['balanc'] -= donar

    # Botó reset
    st.write("")
    if st.button("Esborrar-ho tot i nou dinar"):
        st.session_state.participants = []
        st.rerun()
else:
    st.info("La llista està buida. Afegeix el primer participant per començar!")
