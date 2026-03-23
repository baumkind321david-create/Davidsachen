import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

de = pd.read_csv("C:/Users/David/Downloads/AmesHousing.csv", sep=";")

st.title("AmesHousing Dashboard")

st.subheader("Wichtigste Kennzahlen")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Häuser gesamt", len(de))
with col2:
    avg_price = f"{int(de['SalePrice'].mean()):,}".replace(",", ".")
    st.metric("∅ Verkaufspreis", f"{avg_price} $")
with col3:
    st.metric("∅ Baujahr", int(de['Year Built'].mean()))
with col4:
    st.metric("Max. Preis", f"{int(de['SalePrice'].max()):,}".replace(",", ".") + " $")

st.divider()

st.markdown("*Datensatz:*")
st.dataframe(de.head())

st.markdown("*Diagramme:*")
pie_column = st.selectbox("Wählen Sie eine Spalte aus für Kreisdiagramm", de.select_dtypes(include=["object"]).columns)
pie_data = de[pie_column].value_counts()

percentages = (pie_data / pie_data.sum()) * 100
mask = percentages >= 5
pie_data_filtered = pie_data[mask].copy()

if (others_sum := pie_data[~mask].sum()) > 0:
    pie_data_filtered["Sonstige"] = others_sum

fig1, ax1 = plt.subplots()
ax1.pie(pie_data_filtered, labels=None, autopct="%1.1f%%", startangle=90)
ax1.legend(pie_data_filtered.index, title="Kategorien", loc="center left", bbox_to_anchor=(1, 0.5))
ax1.set_title(f"Verteilung: {pie_column}")
st.pyplot(fig1)
st.caption("Alles unter 5 % wird als 'Sonstige' zusammengefasst.")

st.subheader("Preis-Analyse nach Filter")
c1, c2 = st.columns(2)
neighborhood = c1.selectbox("Nachbarschaft wählen:", sorted(de["Neighborhood"].unique()))
building_type = c2.selectbox("Gebäudetyp wählen:", sorted(de["Bldg Type"].unique()))

filtered_df = de[(de['Neighborhood'] == neighborhood) & (de['Bldg Type'] == building_type)]

if not filtered_df.empty:
    fig2, ax2 = plt.subplots()
    ax2.boxplot(filtered_df["SalePrice"])
    ax2.set_title(f"Verkaufspreis in {neighborhood}")
    ax2.set_ylabel("Verkaufspreis in $")
    st.pyplot(fig2)
else:
    st.warning("Keine Daten für diese Kombination gefunden.")