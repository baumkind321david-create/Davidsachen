import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Seite konfigurieren für breiteres Layout
st.set_page_config(page_title="Ames Housing Pro Dashboard", layout="wide")


# ------------------- CSV einlesen -------------------
# (Pfade ggf. anpassen)
@st.cache_data
def load_data():
    return pd.read_csv("C:\\Users\\baumk\\Downloads\\AmesHousing.csv", sep=";", decimal=",")


da = load_data()

# ------------------- Sidebar -------------------
st.sidebar.header("Filter & Analyse")
st.sidebar.info("Dieses Dashboard filtert automatisch sinnvolle Spalten für die Visualisierung.")

# ------------------- Haupttitel -------------------
st.title("🏠 Ames Housing Markt-Analyse")
st.markdown("---")


# Kurze Zusammenfassung ganz oben
col1, col2, col3 = st.columns(3)
col1.metric("Anzahl Häuser", len(da))
col2.metric("Durchschnittspreis", f"{int(da['SalePrice'].mean()):,} €".replace(",", "."))
col3.metric("Ältestes Baujahr", int(da['Year Built'].min()))

# ------------------- Visualisierungs-Bereich -------------------
st.subheader("📊 Daten-Exploration")

# Spalten filtern
categorical_columns = [col for col in da.columns if da[col].nunique() < 15]
numerical_columns = da.select_dtypes(include=['float64', 'int64']).columns.tolist()

tab1, tab2 = st.tabs(["Kreisdiagramm (Kategorien)", "Verteilungen (Numerisch)"])

with tab1:
    var1 = st.selectbox("Wähle eine Kategorie (wenig Ausprägungen):", categorical_columns)

    c1, c2 = st.columns([1, 1])

    # Daten vorbereiten
    pie_data = da[var1].value_counts().reset_index()
    pie_data.columns = [var1, "Anzahl"]

    with c1:
        fig_pie = px.pie(pie_data, values="Anzahl", names=var1,
                         hole=0.4,
                         title=f"Verteilung von {var1}",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.write(f"Rohdaten zu {var1}")
        st.dataframe(pie_data, use_container_width=True)

with tab2:
    var2 = st.selectbox("Wähle eine Kennzahl für das Histogramm:", numerical_columns)

    # Histogramm für kontinuierliche Daten
    fig_hist = px.histogram(da, x=var2,
                            nbins=30,
                            title=f"Verteilung von {var2}",
                            color_discrete_sequence=['#636EFA'],
                            marginal="box")  # Fügt einen Boxplot oben drüber hinzu!
    st.plotly_chart(fig_hist, use_container_width=True)


st.subheader("📈 Preis-Einflussfaktoren")
col_x = st.selectbox("Wähle Variable für X-Achse (vs. SalePrice):",
                     ["Lot Area", "Overall Qual", "Year Built"])

fig_scatter = px.scatter(da, x=col_x, y="SalePrice",
                         color="Overall Qual",
                         trendline="ols",  # Fügt eine Regressionslinie hinzu
                         title=f"Zusammenhang: {col_x} vs. Verkaufspreis")
st.plotly_chart(fig_scatter, use_container_width=True)


with st.expander("Vollständige Datentabelle ansehen"):
    st.dataframe(da)