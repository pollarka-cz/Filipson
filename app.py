import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Modrý den")


st.write('aplikace, která bude moji vyslednou projektovou prezentaci')
st.info('Popis dat')
st.write('tady bude něco o starych matrikách a časovém rámci  a cíli zjišťování')
# st.balloons()
st.info('Prvni sekce')
st.write('chce to sem hodit text nebo odsazieni? ')
st.code('zdrojová tabulka')

# df_iris = px.data.iris()
# st.dataframe(df_iris, hide_index=True)
#
# st.scatter_chart(df_iris, x="sepal_width", y="sepal_length", color='species')

df = pd.read_csv("https://raw.githubusercontent.com/pollarka-cz/Fileson/main/jmenaa.csv",
    sep=";",
    encoding="utf-8")

# st.title("Vizualizace kousku matriky z minulosti")

st.write('Zdrojová data k nahlédnutí')
st.dataframe(df)
#
# # Výběr sloupců pro osu X a Y
# x_col = st.selectbox("inf_rok_nar:", df.columns)
# y_col = st.selectbox("inf_jmeno1:", df.columns)
#
# # Interaktivní bodový graf
# fig = px.scatter(df, x=x_col, y=y_col, title="Interaktivní bodový graf")
# st.plotly_chart(fig, use_container_width=True)


st.code('první graf:')
fig = px.scatter(
    df,
    x="inf_jmeno1",
    y="inf_mec_nar",
    # size="pocet",
    color="inf_fm",
    animation_frame="inf_rok_nar",
    size_max=40,
    #category_orders={"mesic": [
    #   "leden", "únor", "březen", "duben", "květen", "červen",
#   "červenec", "srpen", "září", "říjen", "listopad", "prosinec"
#   ]},
    width=1800,
    height=500,
    title="Bublinový graf jména × měsíc × rok"
)

# Zobrazení grafu
st.plotly_chart(fig, use_container_width=True)