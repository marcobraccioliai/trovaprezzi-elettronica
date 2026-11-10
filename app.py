import streamlit as st
import pandas as pd

st.set_page_config(page_title="TrovaPrezzi Tech Romagna", page_icon="⚡", layout="wide")

st.title("⚡ TrovaPrezzi Elettronica - Cesena & Forlì")
st.write("Cerca offerte su TV, smartphone, elettrodomestici e gadget tra i volantini tech della zona!")

# Carichiamo il file CSV dell'elettronica
@st.cache_data
def carica_dati():
    return pd.read_csv("prezzi_elettronica.csv")

df = carica_dati()

# --- BARRA LATERALE PER I FILTRI E LA CACHE ---
st.sidebar.header("Pannello di Controllo")

# Pulsante magico per pulire la cache e ricaricare i dati freschi da GitHub
if st.sidebar.button("🔄 Aggiorna Dati da GitHub"):
    st.cache_data.clear()
    st.success("Cache pulita! Dati aggiornati.")
    # Ricarica i dati freschi dopo aver pulito la cache
    df = carica_dati()

st.sidebar.markdown("---")
st.sidebar.header("Filtri Tech")

città_disponibili = sorted(df['città'].unique())
città_scelta = st.sidebar.selectbox("Seleziona la città", ["Tutte"] + città_disponibili)

catene_disponibili = sorted(df['catena'].unique())
catena_scelta = st.sidebar.selectbox("Seleziona la catena", ["Tutte"] + catene_disponibili)

prodotto_input = st.text_input("Cosa cerchi? (es. TV, iPhone, Frigorifero o lascia vuoto per tutto)", "")

# --- FILTRAGGIO ---
risultati = df.copy()

if città_scelta != "Tutte":
    risultati = risultati[risultati['città'].str.lower() == città_scelta.lower()]

if catena_scelta != "Tutte":
    risultati = risultati[risultati['catena'].str.upper() == catena_scelta.upper()]

if prodotto_input.strip() and prodotto_input.strip().lower() != "tutto":
    risultati = risultati[risultati['prodotto'].str.contains(prodotto_input, case=False, na=False)]

risultati_ordinati = risultati.sort_values(by='prezzo', ascending=True)

# --- MOSTRA RISULTATI ---
st.subheader(f"Offerte tech trovate: {len(risultati_ordinati)}")

if not risultati_ordinati.empty:
    st.dataframe(
        risultati_ordinati[['catena', 'città', 'prodotto', 'prezzo', 'offerta']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Nessun prodotto trovato con questi criteri.")
