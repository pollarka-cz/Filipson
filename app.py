import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Vizualizace dat matriční knihy")


st.write('Matrika dětí narozených v katolickém vyznání Klucké Chvalovice 1840 - 1913. '
         'Datový soubor byl pořízen přepisem ručně psané matriky.')
# st.info('Popis dat')
# st.write('tady bude něco o starych matrikách a časovém rámci  a cíli zjišťování')
# st.balloons()
st.info('Historický kontext')
st.write('Matriky se vedly na faře, proto jsou narozené děti rozlišené podle vyznání rodičů. Zde '
         'je použita pouze matrika katolického obyvatelstva. Ve statistickém a místopisném seznamu '
         '(J.G.Sommera) z roku 1834 má vesnice 64 domů a 484 obyvatele vesměs katolického vyznání '
         '(minoritně jsou zastoupeni židé a evangelíci). K obci patří vrchnostenský dvůr (dřevěný),'
          'hostinec, myslivna (torzo hospody) a stranou ležící mlýn s pilou. V roce 1848, kdy'
         'začínají tyto matriční záznamy, bylo v obci 461 obyvatel bez ohledu na vyznání. Zároveň'
         'je rok kdy bylo možné se vykoupit z nucených prací (poddanství / robota) a v Rakouské '
         'monarchii probíhala revoluce, jejíž dopad na malé obce tkvěl mimo jiné v zavedení obecní '
         'samosprávy a další občanské svobody. Kolem roku 1860 vyhořel statek - zdroj zaměsnání místních '
         'obyvatel, nový statek byl postaven až po roce 1905.'
         )

df = pd.read_csv("https://raw.githubusercontent.com/pollarka-cz/Filipson/master/jmena7.csv",
    sep=";",
    encoding="utf-8")

counts = df["inf_rok"].value_counts().reset_index()
counts.columns = ["rok narození", "četnost porodů"]
fig = px.bar(
    counts,
    x="rok narození",
    y="četnost porodů",
    title="Počet narozených dětí ve sledovaném období"
)

fig.update_xaxes(tickangle=45)
st.plotly_chart(fig, use_container_width=True)

# st.code('zdrojová tabulka')


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


import pandas as pd
import plotly.express as px
import streamlit as st


import pandas as pd
import plotly.express as px
import streamlit as st

muzi = st.checkbox("Muž", value=True)
zeny = st.checkbox("Žena", value=True)

# Vyber pohlaví podle zaškrtnutí
vybrano = []
if muzi:
    vybrano.append("m")
if zeny:
    vybrano.append("f")

# Filtrování DataFrame podle pohlaví
df_filt = df[df["inf_fm"].isin(vybrano)]

# Spočítáme četnost pro velikost bubliny
df_counts = (
    df_filt.groupby(["inf_jmeno1", "inf_mes", "inf_rok", "inf_fm"])
    .size()
    .reset_index(name="cetnost")
)
df_counts['inf_rok'] = df_counts['inf_rok'].astype(int)
roky_serazene = sorted(df_counts['inf_rok'].unique())

# Bublinový graf
fig = px.scatter(
    df_counts,
    x="inf_jmeno1",
    y="inf_mes",
    size="cetnost",       # velikost bubliny podle četnosti
    color="inf_fm",
    animation_frame="inf_rok",
    size_max=40,
    color_discrete_map={"m": "blue", "f": "red"},
    title="Bublinový graf četnosti narození dětí podle roku a měsíce "
)

# Nastavení os
fig.update_xaxes(tickangle=45, categoryorder="category ascending")
fig.update_yaxes(categoryorder="array", categoryarray=[
    "leden","únor","březen","duben","květen","červen",
    "červenec","srpen","září","říjen","listopad","prosinec"
])
fig.update_xaxes(tickmode="linear", dtick=1)
st.plotly_chart(fig, use_container_width=True)


# -------------------------------------

dfm = df[df["inf_fm"] == "m"]

st.code('mužský graf:')


counts = dfm["inf_jmeno1"].value_counts().reset_index()
counts.columns = ["jmeno", "cetnost"]
counts = counts[counts["cetnost"] >= 2]
fig = px.bar(
    counts,
    x="jmeno",
    y="cetnost",
    title="Četnost mužských jmen"
)

fig.update_xaxes(tickangle=45)
st.plotly_chart(fig, use_container_width=True)






fig = px.scatter(
    dfm,
    x="inf_jmeno1",
    y="inf_mes",
    # size="pocet",
    # color="inf_fm",
    animation_frame="inf_rok",
    size_max=40,
    title="Bublinový graf jména × měsíc × rok pro kluky"
)
fig.update_xaxes(tickangle=45, categoryorder="category ascending")
fig.update_yaxes(categoryorder="array", categoryarray=[
    "leden","únor","březen","duben","květen","červen",
    "červenec","srpen","září","říjen","listopad","prosinec"
])
fig.update_xaxes(tickmode="linear", dtick=1)
st.plotly_chart(fig, use_container_width=True)
