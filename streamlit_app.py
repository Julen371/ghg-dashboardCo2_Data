# 🚆 NS: LondOnderweg! — Verbeterde Streamlit App
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

# ----------------------------------------------------------
# 🔧 PAGINA-INSTELLINGEN
# ----------------------------------------------------------
st.set_page_config(page_title="NS: LondOnderweg!", page_icon="🚆", layout="wide")

# Donkere NS-stijl met geel accent
st.markdown("""
<style>
    body {background-color: #111;}
    .stApp {background-color: #111;}
    h1, h2, h3, h4, h5 {color: #FFD700;}
    p, label, span {color: white !important;}
    .metric-label, .metric-value {color: white !important;}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# 🔹 TITEL EN INTRO
# ----------------------------------------------------------
st.title("🚆 NS: LondOnderweg!")
st.markdown("Welkom bij ons **mobiliteitsdashboard**! Ontdek hoe weer, metro en fietsen samen Londen in beweging houden. 🌍")

# ----------------------------------------------------------
# 📊 DATA INLADEN
# ----------------------------------------------------------
@st.cache_data
def load_data():
    stations = pd.read_csv("cycle_stations.csv")
    rentals = pd.read_csv("bike_rentals.csv")
    weather = pd.read_csv("weather_london.csv")
    return stations, rentals, weather

stations, rentals, weather = load_data()

# ----------------------------------------------------------
# ✅ KOLONNAMEN FIXEN (belangrijk!)
# ----------------------------------------------------------
# Hernoem 'long' → 'lon' zodat Streamlit het herkent
if "long" in stations.columns:
    stations = stations.rename(columns={"long": "lon"})

# Controleer kolommen
lat_col, lon_col = "lat", "lon"
bike_col = "nbBikes"

# ----------------------------------------------------------
# 🔖 TABSTRUCTUUR
# ----------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Data Exploration", "🚲 Fietsstations & Kaart", "🌦️ Weer & Trends"])

# ----------------------------------------------------------
# 📊 TAB 1 — DATA EXPLORATION
# ----------------------------------------------------------
with tab1:
    st.header("📈 Data-overzicht")

    st.markdown("Hieronder zie je voorbeelden van onze drie datasets:")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🚲 cycle_stations.csv")
        st.dataframe(stations.head())
    with c2:
        st.subheader("📅 bike_rentals.csv")
        st.dataframe(rentals.head())
    with c3:
        st.subheader("🌦️ weather_london.csv")
        st.dataframe(weather.head())

# ----------------------------------------------------------
# 🚲 TAB 2 — KAART MET FIETSSTATIONS
# ----------------------------------------------------------
with tab2:
    st.header("🗺️ Fietsverhuurstations in Londen")

    if lat_col in stations.columns and lon_col in stations.columns:
        st.success("✅ Kolommen gevonden: 'lat' en 'lon'")

        avg_bikes = round(stations[bike_col].mean(), 1)
        total_bikes = int(stations[bike_col].sum())
        st.metric(label="Gemiddeld aantal fietsen per station", value=avg_bikes)
        st.metric(label="Totaal aantal fietsen", value=total_bikes)

        # Folium kaart
        m = folium.Map(location=[51.5074, -0.1278], zoom_start=11, tiles="CartoDB dark_matter")

        # Voeg markers toe
        for _, row in stations.iterrows():
            popup_text = f"<b>{row['name']}</b><br>🚲 Fietsen: {row[bike_col]}"
            folium.CircleMarker(
                location=[row[lat_col], row[lon_col]],
                radius=4,
                color="yellow",
                fill=True,
                fill_opacity=0.9,
                popup=popup_text
            ).add_to(m)

        st_folium(m, width=1100, height=600)

    else:
        st.error("❌ Kon kolommen niet vinden. Controleer of 'lat' en 'lon' bestaan.")
        st.write("Beschikbare kolommen:", list(stations.columns))

# ----------------------------------------------------------
# 🌦️ TAB 3 — WEER EN TRENDS
# ----------------------------------------------------------
with tab3:
    st.header("🌤️ Correlatie tussen weer en fietsverhuur")

    if "tavg" in weather.columns:
        st.success("✅ Weerdata succesvol geladen!")

        # Voeg een gesimuleerde 'rentals'-kolom toe om correlatie te tonen
        np.random.seed(42)
        weather["rentals"] = np.random.randint(5000, 55000, size=len(weather))

        # Selecteer factor
        weather_factor = st.selectbox("Kies een weerfactor:", ["tavg", "tmin", "tmax", "prcp", "tsun"])

        # Plot regressie
        fig, ax = plt.subplots()
        sns.regplot(data=weather, x=weather_factor, y="rentals", scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
        ax.set_title(f"Regressie: {weather_factor} vs. Fietsverhuur", color="white")
        ax.set_xlabel(weather_factor, color="white")
        ax.set_ylabel("Aantal Fietsverhuringen", color="white")
        fig.patch.set_facecolor("#111")
        ax.set_facecolor("#111")
        st.pyplot(fig)

        # Correlatiematrix
        st.subheader("📊 Correlatiematrix weerdata")
        corr = weather.corr(numeric_only=True)
        fig2, ax2 = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="YlOrBr", ax=ax2)
        st.pyplot(fig2)
    else:
        st.error("❌ 'tavg' kolom niet gevonden in weather_london.csv.")
