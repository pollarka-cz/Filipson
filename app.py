import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Vizualizace dat matriční knihy")


st.write('Matrika dětí narozených v katolickém vyznání Klucké Chvalovice 1840 - 1913. '
         'Datový soubor byl pořízen přepisem ručně psané matriky.')

st.info('Historický kontext')
st.write('Matriky se vedly na faře, proto jsou narozené děti rozlišené podle vyznání rodičů. Zde '
         'je použita pouze matrika katolického obyvatelstva. Ve statistickém a místopisném seznamu '
         '(J.G.Sommera) z roku 1834 má vesnice 64 domů a 484 obyvatele vesměs katolického vyznání '
         '(minoritně jsou zastoupeni židé a evangelíci). K obci patří vrchnostenský dvůr (dřevěný),'
          'hostinec, myslivna (v r. 2025 torzo hospody) a stranou ležící mlýn s pilou.'
         ' V roce 1848, kdy začínají tyto matriční záznamy, bylo v obci 461 obyvatel bez ohledu na' 
         'vyznání. Zároveň je to rok kdy bylo možné se vykoupit z nucených prací (poddanství / robota)'
          'a v Rakouské monarchii probíhala revoluce. Dopad změn na malé obce tkvěl mimo jiné v zavedení'
          'obecní samosprávy a další občanské svobody. Kolem roku 1860 vyhořel statek - zdroj zaměsnání 
          'místních obyvatel, nový statek byl postaven až po roce 1905.'
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




muzi = st.checkbox("Muž", value=True, key="1_m")
zeny = st.checkbox("Žena", value=True, key="1_f")


vybrano = []
if muzi:
    vybrano.append("m")
if zeny:
    vybrano.append("f")

# Filtr
df_filt = df[df["inf_fm"].isin(vybrano)]

# četnost
df_counts = (
    df_filt.groupby(["inf_jmeno1", "inf_mes", "inf_rok", "inf_fm"])
    .size()
    .reset_index(name="cetnost")
)
df_counts['inf_rok'] = df_counts['inf_rok'].astype(int)
roky_serazene = sorted(df_counts['inf_rok'].unique())

fig = px.scatter(
    df_counts,
    x="inf_jmeno1",
    y="inf_mes",
    size="cetnost",
    color="inf_fm",
    animation_frame="inf_rok",
    size_max=40,
    color_discrete_map={"m": "blue", "f": "#ff0066"},
    title="Bublinový graf četnosti narození dětí podle roku a měsíce "
)

# Nastavení os
fig.update_xaxes(tickangle=45, categoryorder="category ascending")
fig.update_yaxes(categoryorder="array", categoryarray=[
    "leden","únor","březen","duben","květen","červen",
    "červenec","srpen","září","říjen","listopad","prosinec"
])

fig.update_layout(yaxis_title="Měsíc narození", xaxis_title="Jméno",
                  legend_title_text="Pohlaví")

fig.update_xaxes(tickmode="linear", dtick=1)
st.plotly_chart(fig, use_container_width=True)


# -------------------------------------
# kluci
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

# -------------------------------------
# holky
dff = df[df["inf_fm"] == "f"]

st.code('ženský graf:')

counts = dfm["inf_jmeno1"].value_counts().reset_index()
counts.columns = ["jmeno", "cetnost"]
counts = counts[counts["cetnost"] >= 2]
fig = px.bar(
    counts,
    x="jmeno",
    y="cetnost",
    title="Četnost ženských jmen",
    color_discrete_sequence=[ "#ff0066"])

fig.update_xaxes(tickangle=45)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------


fig = px.scatter(
    dff,
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



# -------------------------

# --- Zaškrtávátka ---
show_all = st.checkbox("Vše", value=False, key="3_all")
show_mu = st.checkbox("Muži", value=True, key="3_m")
show_ze = st.checkbox("Ženy", value=True, key="3_f")

# --- Agregace ---
if show_all:
    # součet všech pohlaví
    df_grouped = df.groupby("inf_rok").size().reset_index(name="pocet")
    color_col = None
else:
    df_grouped = df.groupby(["inf_rok", "inf_fm"]).size().reset_index(name="pocet")

    # filtr podle checkboxů
    filtry = []
    if show_mu:
        filtry.append("m")
    if show_ze:
        filtry.append("f")

    if filtry:
        df_grouped = df_grouped[df_grouped["inf_fm"].isin(filtry)]
        color_col = "inf_fm"
    else:
        st.warning("Vyber aspoň jednu možnost.")
        st.stop()

# --- Liniový graf ---
fig = px.line(df_grouped,
              x="inf_rok",
              y="pocet",
              color=color_col,
              markers=True,
              title="Počet narozených podle roku a pohlaví",
             color_discrete_sequence=["#1f77b4", "#ff0066"])

fig.update_layout(yaxis_title="Počet narozených", xaxis_title="Rok narození",
                  legend_title_text="Pohlaví" if not show_all else "")

st.plotly_chart(fig, use_container_width=True)

# -----------------------------

