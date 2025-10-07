import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- DATA INLADEN ---
stations = pd.read_csv("cycle_stations.csv")
bike = pd.read_csv("bike_rentals.csv")
weather = pd.read_csv("weather_london.csv")

st.title("🚲 NS: LondOnderweg!")
st.markdown("Welkom bij ons mobiliteitsdashboard! Ontdek hoe weer en fietsen samen Londen in beweging houden.")

# --- TAB STRUCTUUR ---
tab1, tab2, tab3 = st.tabs(["📊 Data Exploration", "🗺️ London Maps", "🌦️ Weer & Fietsverhuur"])

# =====================
# TAB 1: Data Exploration
# =====================
with tab1:
    st.header("📈 Fietsverhuur en Weerdata")

    st.markdown("Hieronder zie je de ruwe data die we gebruiken voor onze analyses.")
    st.dataframe(weather.head())

    # Selecteer een weerfactor
    weather_factor = st.selectbox("Kies een weerfactor:", ["tavg", "tmin", "tmax", "prcp"])

    # Maak een simpele correlatieplot tussen weer en fietsverhuur (dummy)
    if weather_factor in weather.columns:
        # Simuleer aantal verhuurde fietsen (je kunt dit later koppelen aan echte telling)
        np.random.seed(42)
        weather["rentals"] = np.random.randint(5000, 55000, size=len(weather))

        # Plot regressie
        fig, ax = plt.subplots()
        sns.regplot(data=weather, x=weather_factor, y="rentals", scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
        ax.set_title(f"Regressie: {weather_factor} vs. Fietsverhuur")
        ax.set_xlabel(weather_factor)
        ax.set_ylabel("Aantal Fietsverhuringen")
        st.pyplot(fig)
    else:
        st.warning("Weerfactor niet gevonden in de dataset.")

# =====================
# TAB 2: London Maps
# =====================
with tab2:
    st.header("🗺️ Fietsverhuurstations in Londen")

    st.markdown("Deze kaart toont de locaties van de fietsverhuurstations, met het aantal beschikbare fietsen per station.")
    st.write("📋 Kolomnamen in cycle_stations.csv:", list(stations.columns))

    # Handmatige mapping van kolommen
    lat_col = "lat"
    lon_col = "long"
    bikes_col = "nbBikes"

    # Controle of kolommen bestaan
    if lat_col in stations.columns and lon_col in stations.columns:
        st.success(f"✅ Kolommen gevonden → latitude: `{lat_col}`, longitude: `{lon_col}`")

        # Toon samenvatting
        st.metric(label="Gemiddeld aantal fietsen per station", value=round(stations[bikes_col].mean(), 1))
        st.metric(label="Totaal aantal fietsen", value=int(stations[bikes_col].sum()))

        # Toon kaart
        st.map(stations[[lat_col, lon_col]].dropna(), zoom=11)
    else:
        st.error(f"❌ Kon kolommen niet vinden. Gevonden: lat={lat_col in stations.columns}, lon={lon_col in stations.columns}")

# =====================
# TAB 3: Weer & Fietsverhuur
# =====================
with tab3:
    st.header("🌦️ Correlatie tussen weer en fietsverhuur")

    # Controleer of tavg aanwezig is
    if "tavg" in weather.columns:
        st.success("✅ Weerdata succesvol geladen!")
        st.dataframe(weather[["tavg", "tmin", "tmax", "prcp"]].head())

        corr = weather.corr(numeric_only=True)
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.error("❌ Kon geen 'tavg' kolom vinden in weather_london.csv.")
