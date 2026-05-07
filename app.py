import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Kanji Learning Order', layout='wide')

def get_conn():
    return sqlite3.connect('kanji.db')

st.title('Optimizing Kanji Learning Order')
st.markdown('A data-driven approach to Japanese character acquisition.')

# Setting up the sidebar and main table.
st.divider()
st.subheader('Recommended Learning Order')
st.markdown('''Use the filters in the sidebar to explore the recommended learning order.''')
st.markdown('''**Cluster** groups characters by their simplicity and utility profile.''')
st.markdown('''**JLPT** filters by the official proficiency level.''')
st.markdown('''**Learning Order** determines how the middle clusters are prioritized — *Utility First* places 
            *Hard & Common* before *Easy & Rare*, while *Simplicity First* does the opposite.''')
st.markdown('''> **Note:** The **Learning Order** dropdown only has purpose when browsing with both **Cluster** and 
            **JLPT** set to **All**.''')
st.markdown('''<br>''', unsafe_allow_html=True)

st.sidebar.header('Filters')

version = st.sidebar.selectbox(
    'Learning Order',
    options=[('Utility First', 'learning_order_u'), ('Simplicity First', 'learning_order_s')],
    format_func=lambda x: x[0]
)

cluster = st.sidebar.selectbox(
    'Cluster',
    options=['All', 'Easy & Common', 'Hard & Common', 'Easy & Rare', 'Hard & Rare']
)

jlpt = st.sidebar.selectbox(
    'JLPT Level',
    options=['All', 1, 2, 3, 4, 5]
)

# The main querying method.
def fetch(version, cluster, jlpt):
    conn = get_conn()
    query = f'''
        SELECT lo.rank AS Rank, k.character AS Character, k.jlpt_new AS JLPT, k.wk_level AS "WaniKani Level",
               k.strokes AS Strokes, c.util_score AS "Utility Score", c.simp_score AS "Simplicity Score", 
               c.learnability AS Learnability, c.cluster_label AS Cluster
        FROM kanji k
        JOIN clusters c ON k.unicode = c.unicode
        JOIN {version[1]} lo ON k.unicode = lo.unicode
        WHERE k.jlpt_new != 0
    '''
    if cluster != 'All':
        query += f" AND c.cluster_label = '{cluster}'"
    if jlpt != 'All':
        query += f" AND k.jlpt_new = {jlpt}"
    query += ' ORDER BY lo.rank ASC'
    df = pd.read_sql(query, conn)
    conn.close()
    return df

display_cols = ['Rank', 'Character', 'JLPT', 'WaniKani Level', 'Strokes', 'Learnability', 'Cluster']
df = fetch(version, cluster, jlpt)
df.index = range(1, len(df) + 1)
st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

# Character lookup.
search = st.text_input('Enter a kanji character:')
lookup_version = st.selectbox(
    'Learning Order For Search',
    options=[('Utility First', 'learning_order_u'), ('Simplicity First', 'learning_order_s')],
    format_func=lambda x: x[0],
    key='lookup_version'
)

if search:
    conn = get_conn()
    result = pd.read_sql(f'''
        SELECT lo.rank, k.character AS Character, c.cluster_label AS Cluster, c.learnability AS Learnability, 
                k.jlpt_new AS JLPT, k.wk_level AS "WaniKani Level", k.strokes AS Strokes
        FROM kanji k
        JOIN clusters c ON k.unicode = c.unicode
        JOIN {lookup_version[1]} lo ON k.unicode = lo.unicode
        WHERE k.character = "{search}"
    ''', conn)
    conn.close()
    
    if result.empty:
        st.warning('Character not found.')
    else:
        st.markdown(f'**Rank:** {result["rank"].values[0]} / 2136')
        result.index = [1]
        st.dataframe(result[['Character', 'Cluster', 'Learnability', 'JLPT', 'WaniKani Level', 'Strokes']], use_container_width=True, hide_index=True)

# The main scatterplot.
st.divider()
st.subheader('Simplicity vs. Utility')
fig = px.scatter(
    df,
    x='Simplicity Score',
    y='Utility Score', 
    color='Cluster',
    hover_data={'Character': True, 'Learnability': ':.4f', 'Simplicity Score': ':.4f', 'Utility Score': ':.4f'}
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('''
**Simplicity Score** reflects how easy a character is to write; a score of 1 indicates the fewest strokes, 
while 0 indicates the most.''')
st.markdown('''**Utility Score** reflects how frequently a character appears across various sources; 
a score of 1 indicates the most common, while 0 indicates the rarest.''')

# Exploratory analysis.
st.divider()
st.subheader('Exploratory Analysis')

conn = get_conn()
full_df = pd.read_sql('''
    SELECT k.character, k.jlpt_new, k.wk_level, k.grade, c.simp_score, c.util_score, c.learnability
    FROM kanji k JOIN clusters c ON k.unicode = c.unicode
''', conn)
conn.close()

full_jlpt = full_df[full_df['jlpt_new'] != 0]

# The comparative scatterplots.
for col, title, data in [
    ('jlpt_new', 'JLPT Level', full_jlpt),
    ('wk_level', 'WaniKani Level', full_df),
    ('grade', 'Grade', full_df)
]:
    fig = px.scatter(data, x='simp_score', y='util_score', color=col,
        labels={'character':'Character', 'simp_score': 'Simplicity Score', 'util_score': 'Utility Score', col: title},
        hover_data={'character':True, 'simp_score':':.4f', 'util_score':':.4f'},
        title=f'Simplicity vs. Utility by {title}')
    st.plotly_chart(fig, use_container_width=True)

# The comparative histograms.
for col, title, data in [
    ('jlpt_new', 'JLPT Level', full_jlpt),
    ('wk_level', 'WaniKani Level', full_df)
]:
    avg = data.groupby(col)['learnability'].mean().reset_index()
    fig = px.bar(avg, x=col, y='learnability',
        labels={col: title, 'learnability': 'Average Learnability'},
        hover_data={'learnability':':.4f'},
        title=f'Average Learnability by {title}')
    st.plotly_chart(fig, use_container_width=True)

# Citations and stuff.
st.divider()
st.markdown('### Data Sources')
st.markdown('''
- **WaniKani API**: Kanji levels and radical names. © Tofugu LLC
- **[kanji-data](https://github.com/davidluzgouveia/kanji-data)** by davidluzgouveia: JLPT levels, stroke counts, and grade. (MIT License)
- **[kanji-frequency](https://github.com/scriptin/kanji-frequency)** by Dmitry Shpika: Corpus frequency ranks. (CC BY 4.0)
''')

# Acknowledging Claude.
st.markdown('<p style="font-size: 12px; color: gray;">This dashboard was made using assistance from <a href="https://claude.ai">Claude</a> by Anthropic.</p>', unsafe_allow_html=True)