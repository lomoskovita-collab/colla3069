import streamlit as st
# Ara afegeix la configuració màgica (Línia 2):
st.set_page_config(initial_sidebar_state="expanded")
import os

# -- CONFIGURACIÓ DE PÀGINA --
st.set_page_config(page_title="Trobades 3069", page_icon="🐌", layout="wide")

# -- DISSENY I AMAGAR MENÚ ANGLÈS --
st.markdown("""
<style>
    /* Amagar el menú de la dreta i el peu de pàgina de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Fons principal verd molt clar */
    .stApp {
        background-color: #f0f7f4;
    }
    
    /* Barra lateral verd fosc */
    [data-testid="stSidebar"] {
        background-color: #0d4332;
    }
    
    /* Títols en groc daurat */
    h1, h2, h3, span, label {
        color: #d1b110 !important;
        font-family: 'Serif', 'Georgia', serif;
    }

    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label {
        color: #f0f7f4 !important;
    }

    /* Botons personalitzats */
    button, .stButton>button {
        background-color: #0d4332 !important;
        color: #d1b110 !important;
        border: 2px solid #d1b110 !important;
        border-radius: 10px;
        font-weight: bold;
    }
    
    button:hover, .stButton>button:hover {
        background-color: #d1b110 !important;
        color: #0d4332 !important;
    }
</style>
""", unsafe_allow_html=True)

# -- INICIALITZACIÓ --
if 'participants' not in st.session_state:
    st.session_state.participants = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# -- BARRA LATERAL --
with st.sidebar:
    # Carregar el cargol (ara més gran)
    if os.path.exists("cargol.jpg"):
        st.image("cargol.jpg", width=250) # Mida augmentada
    else:
        st.markdown("# 🐌")
        
    st.markdown("<h2 style='text-align: center;'>TROBADES 3069</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    titol_formulari = "✏️ Editar" if st.session_state.edit_index is not None else "➕ Afegir"
    with st.form("formulari_persona", clear_on_submit=True):
        st.write(f"**{titol_formulari} Participant**")
        
        def_nom = ""
        def_import = 0.0
        if st.session_state.edit_index is not None:
            p_edit = st.session_state.participants[st.session_state.edit_index]
            def_nom = p_edit['nom']
            def_import = p_edit['pagat']

        nom_input = st.text_input("Nom", value=def_nom)
        import_input = st.number_input("Import pagat (€)", min_value=0.0, step=0.01, value=def_import)
        
        submit = st.form_submit_button("DESAR")
        if submit and nom_input:
            if st.session_state.edit_index is not None:
                st.session_state.participants[st.session_state.edit_index] = {"nom": nom_input, "pagat": import_input}
                st.session_state.edit_index = None
            else:
                st.session_state.participants.append({"nom": nom_input, "pagat": import_input})
            st.rerun()

# -- COS PRINCIPAL --
st.title("🍴 Gestor de Dinars")
# Canvi de frases segons la teva petició
st.markdown("### All i oli i vinagreta") 

if st.session_state.participants:
    st.markdown("---")
    for i, p in enumerate(st.session_state.participants):
        col_nom, col_preu, col_edit, col_del = st.columns([3, 2, 1, 1])
        col_nom.write(f"**{p['nom']}**")
        col_preu.write(f"{p['pagat']:.2f} €")
        
        if col_edit.button("✏️", key=f"edit_{i}"):
            st.session_state.edit_index = i
            st.rerun()
            
        if col_del.button("🗑️", key=f"del_{i}"):
            st.session_state.participants.pop(i)
            st.rerun()

    if len(st.session_state.participants) > 1:
        st.markdown("---")
        total = sum(p['pagat'] for p in st.session_state.participants)
        mitjana = total / len(st.session_state.participants)
        
        c1, c2 = st.columns(2)
        c1.metric("TOTAL DINAR", f"{total:.2f} €")
        c2.metric("A PAGAR PER CAP", f"{mitjana:.2f} €")

        st.subheader("💰 Liquidació")
        balanços = {p['nom']: p['pagat'] - mitjana for p in st.session_state.participants}
        deutors = sorted([[n, b] for n, b in balanços.items() if b < -0.01], key=lambda x: x[1])
        creditors = sorted([[n, b] for n, b in balanços.items() if b > 0.01], key=lambda x: x[1], reverse=True)

        while deutors and creditors:
            d, c = deutors[0], creditors[0]
            quantitat = min(-d[1], c[1])
            st.success(f"**{d[0]}** ha de pagar **{quantitat:.2f} €** a **{c[0]}**")
            d[1] += quantitat
            c[1] -= quantitat
            if abs(d[1]) < 0.01: deutors.pop(0)
            if abs(c[1]) < 0.01: creditors.pop(0)

    st.write("")
    if st.button("Esborrar-ho tot"):
        st.session_state.participants = []
        st.rerun()
else:
    st.info("Comença afegint algú des de la barra lateral de l'esquerra! 👈")
