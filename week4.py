import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DataViz Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Mono', monospace;
}

.stApp {
    background: #0d0d0d;
    color: #f0f0f0;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.chart-card {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.purpose-tag {
    display: inline-block;
    background: #1a1a2e;
    color: #7c6af7;
    border: 1px solid #7c6af7;
    border-radius: 4px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

div[data-testid="stSidebarContent"] {
    background: #111111;
    border-right: 1px solid #222;
}

.sidebar-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    color: #7c6af7;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">▸ DATAVIZ EXPLORER</p>', unsafe_allow_html=True)
    st.markdown("---")
    chart_choice = st.radio(
        "Select Chart Purpose",
        options=[
            "1 · Comparing Categorical Values",
            "2 · Part-of-a-Whole Relationships",
            "3 · Changes Over Time",
            "4 · Geo-Spatial Data",
            "5 · Relationships & Correlations",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Built with Plotly + Streamlit")


# ═══════════════════════════════════════════════════════════════
# 1. COMPARING CATEGORICAL VALUES — Horizontal Bar Chart
# ═══════════════════════════════════════════════════════════════
if chart_choice.startswith("1"):
    st.markdown('<span class="purpose-tag">PURPOSE 01 — COMPARISON</span>', unsafe_allow_html=True)
    st.title("Comparing Categorical Values")
    st.markdown("**Chart type:** Horizontal Bar Chart  \n**Dataset:** Programming Language Popularity Index 2024")

    np.random.seed(42)
    languages = ["Python", "JavaScript", "TypeScript", "Rust", "Go", "Java", "C++", "Kotlin", "Swift", "Ruby"]
    scores = [94.3, 88.1, 72.4, 65.9, 61.2, 58.7, 55.3, 49.1, 43.8, 37.2]
    colors = ["#7c6af7" if s == max(scores) else "#3a3a5c" for s in scores]

    df = pd.DataFrame({"Language": languages, "Popularity Score": scores})
    df = df.sort_values("Popularity Score")

    fig = go.Figure(go.Bar(
        x=df["Popularity Score"],
        y=df["Language"],
        orientation="h",
        marker=dict(
            color=["#7c6af7" if lang == "Python" else "#3a3a5c" for lang in df["Language"]],
            line=dict(color="#0d0d0d", width=1),
        ),
        text=df["Popularity Score"].apply(lambda x: f"{x:.1f}"),
        textposition="outside",
        textfont=dict(color="#aaa", size=12, family="Space Mono"),
    ))

    fig.update_layout(
        paper_bgcolor="#161616",
        plot_bgcolor="#161616",
        font=dict(color="#f0f0f0", family="DM Sans"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#252525",
            range=[0, 110],
            title="Popularity Score",
            tickfont=dict(color="#888"),
        ),
        yaxis=dict(tickfont=dict(color="#ccc", size=13)),
        margin=dict(l=20, r=60, t=20, b=40),
        height=420,
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("🥇 Top Language", "Python", "+5.2 pts YoY")
    col2.metric("📈 Fastest Growing", "Rust", "+12.3 pts YoY")
    col3.metric("Languages Tracked", "10", "")

    with st.expander("📌 Insight"):
        st.write(
            "Horizontal bar charts excel at comparing categorical values when labels are long or numerous. "
            "Sorting by value (ascending or descending) makes rank ordering immediately obvious. "
            "Highlighting the top or focus item with a distinct colour draws the reader's eye."
        )


# ═══════════════════════════════════════════════════════════════
# 2. PART-OF-A-WHOLE — Treemap + Sunburst
# ═══════════════════════════════════════════════════════════════
elif chart_choice.startswith("2"):
    st.markdown('<span class="purpose-tag">PURPOSE 02 — HIERARCHY & PART-OF-WHOLE</span>', unsafe_allow_html=True)
    st.title("Hierarchies & Part-of-a-Whole")
    st.markdown("**Chart types:** Treemap & Sunburst  \n**Dataset:** Global Tech Company Market Cap (USD Billions)")

    data = {
        "Sector": ["Cloud", "Cloud", "Cloud", "Consumer", "Consumer", "Consumer", "Enterprise", "Enterprise", "Semiconductor", "Semiconductor"],
        "Company": ["Microsoft", "Amazon", "Google", "Apple", "Meta", "Netflix", "Salesforce", "Oracle", "Nvidia", "TSMC"],
        "Market Cap ($B)": [3100, 1900, 1800, 3400, 1300, 280, 320, 410, 2800, 900],
    }
    df = pd.DataFrame(data)

    tab1, tab2 = st.tabs(["🗺 Treemap", "☀️ Sunburst"])

    with tab1:
        fig = px.treemap(
            df,
            path=["Sector", "Company"],
            values="Market Cap ($B)",
            color="Market Cap ($B)",
            color_continuous_scale=["#1a1a2e", "#7c6af7", "#c4b5fd"],
            title="",
        )
        fig.update_layout(
            paper_bgcolor="#161616",
            font=dict(color="#f0f0f0", family="DM Sans"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=450,
            coloraxis_colorbar=dict(tickfont=dict(color="#ccc")),
        )
        fig.update_traces(textfont=dict(size=14))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig2 = px.sunburst(
            df,
            path=["Sector", "Company"],
            values="Market Cap ($B)",
            color="Market Cap ($B)",
            color_continuous_scale=["#1a1a2e", "#7c6af7", "#c4b5fd"],
        )
        fig2.update_layout(
            paper_bgcolor="#161616",
            font=dict(color="#f0f0f0", family="DM Sans"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=450,
        )
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📌 Insight"):
        st.write(
            "Treemaps show hierarchical data where area encodes magnitude — ideal for spotting dominant "
            "categories at a glance. Sunbursts add an explicit parent–child relationship layer through "
            "concentric rings. Both reveal part-of-whole proportions within a two-level hierarchy."
        )


# ═══════════════════════════════════════════════════════════════
# 3. CHANGES OVER TIME — Multi-line Area Chart
# ═══════════════════════════════════════════════════════════════
elif chart_choice.startswith("3"):
    st.markdown('<span class="purpose-tag">PURPOSE 03 — TIME SERIES</span>', unsafe_allow_html=True)
    st.title("Changes Over Time")
    st.markdown("**Chart type:** Multi-Line Area Chart  \n**Dataset:** Monthly Active Users (Millions) — 2022–2024")

    np.random.seed(7)
    months = pd.date_range("2022-01-01", periods=36, freq="MS")
    products = {
        "Product A": np.cumsum(np.random.normal(4, 1.5, 36)) + 50,
        "Product B": np.cumsum(np.random.normal(3, 2, 36)) + 30,
        "Product C": np.cumsum(np.random.normal(1.5, 1, 36)) + 15,
    }

    df = pd.DataFrame(products, index=months).reset_index().rename(columns={"index": "Date"})
    df_melted = df.melt("Date", var_name="Product", value_name="MAU (M)")

    palette = {
        "Product A": {"line": "#7c6af7", "fill": "rgba(124,106,247,0.08)"},
        "Product B": {"line": "#38bdf8", "fill": "rgba(56,189,248,0.08)"},
        "Product C": {"line": "#f472b6", "fill": "rgba(244,114,182,0.08)"},
    }

    fig = go.Figure()
    for product, colors in palette.items():
        subset = df_melted[df_melted["Product"] == product]
        fig.add_trace(go.Scatter(
            x=subset["Date"],
            y=subset["MAU (M)"],
            name=product,
            mode="lines",
            line=dict(color=colors["line"], width=2.5),
            fill="tozeroy",
            fillcolor=colors["fill"],
            hovertemplate="%{x|%b %Y}<br>MAU: %{y:.1f}M<extra>%{fullData.name}</extra>",
        ))

    fig.update_layout(
        paper_bgcolor="#161616",
        plot_bgcolor="#161616",
        font=dict(color="#f0f0f0", family="DM Sans"),
        xaxis=dict(showgrid=False, tickfont=dict(color="#888")),
        yaxis=dict(showgrid=True, gridcolor="#252525", title="MAU (Millions)", tickfont=dict(color="#888")),
        legend=dict(bgcolor="#161616", bordercolor="#2a2a2a", borderwidth=1),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=20),
        height=430,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Sparkline row
    col1, col2, col3 = st.columns(3)
    for col, prod in zip([col1, col2, col3], palette.keys()):
        latest = df[prod].iloc[-1]
        delta = df[prod].iloc[-1] - df[prod].iloc[-13]
        col.metric(prod, f"{latest:.1f}M MAU", f"{delta:+.1f}M vs last year")

    with st.expander("📌 Insight"):
        st.write(
            "Area charts work well for time series when you want to convey volume alongside trend. "
            "Using semi-transparent fills preserves legibility when multiple series overlap. "
            "Unified hover tooltips let users compare values across series at any given date."
        )


# ═══════════════════════════════════════════════════════════════
# 4. GEO-SPATIAL — Choropleth World Map
# ═══════════════════════════════════════════════════════════════
elif chart_choice.startswith("4"):
    st.markdown('<span class="purpose-tag">PURPOSE 04 — GEO-SPATIAL</span>', unsafe_allow_html=True)
    st.title("Mapping Geo-Spatial Data")
    st.markdown("**Chart type:** Choropleth Map  \n**Dataset:** Internet Penetration Rate by Country (%)")

    # Sample dataset — a representative spread of countries
    geo_data = {
        "Country": [
            "United States", "United Kingdom", "Germany", "France", "Japan",
            "China", "India", "Brazil", "Nigeria", "South Africa",
            "Australia", "Canada", "Russia", "Mexico", "Indonesia",
            "Saudi Arabia", "Argentina", "Egypt", "Pakistan", "South Korea",
            "Italy", "Spain", "Sweden", "Norway", "Finland",
            "Kenya", "Ethiopia", "Ghana", "Morocco", "Tanzania",
            "Netherlands", "Switzerland", "Austria", "Belgium", "Denmark",
        ],
        "ISO": [
            "USA", "GBR", "DEU", "FRA", "JPN",
            "CHN", "IND", "BRA", "NGA", "ZAF",
            "AUS", "CAN", "RUS", "MEX", "IDN",
            "SAU", "ARG", "EGY", "PAK", "KOR",
            "ITA", "ESP", "SWE", "NOR", "FIN",
            "KEN", "ETH", "GHA", "MAR", "TZA",
            "NLD", "CHE", "AUT", "BEL", "DNK",
        ],
        "Internet %": [
            92, 95, 91, 86, 93,
            75, 52, 81, 43, 72,
            96, 94, 88, 78, 77,
            99, 85, 72, 36, 98,
            85, 94, 97, 99, 96,
            40, 24, 61, 88, 33,
            96, 97, 93, 92, 98,
        ],
    }
    df = pd.DataFrame(geo_data)

    projection = st.selectbox("Map Projection", ["natural earth", "equirectangular", "orthographic", "mercator"], index=0)

    fig = px.choropleth(
        df,
        locations="ISO",
        color="Internet %",
        hover_name="Country",
        color_continuous_scale=["#1a1a2e", "#312e81", "#7c6af7", "#c4b5fd", "#ede9fe"],
        range_color=(20, 100),
        projection=projection,
    )

    fig.update_layout(
        paper_bgcolor="#161616",
        geo=dict(
            bgcolor="#161616",
            landcolor="#1e1e2e",
            oceancolor="#0d0d0d",
            showocean=True,
            lakecolor="#0d0d0d",
            showland=True,
            showframe=False,
            coastlinecolor="#333",
        ),
        font=dict(color="#f0f0f0", family="DM Sans"),
        coloraxis_colorbar=dict(
            title="Internet %",
            tickfont=dict(color="#ccc"),
            title_font=dict(color="#ccc"),
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        height=480,
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("🌍 Highest", f"{df.loc[df['Internet %'].idxmax(), 'Country']}", f"{df['Internet %'].max()}%")
    col2.metric("🌍 Lowest", f"{df.loc[df['Internet %'].idxmin(), 'Country']}", f"{df['Internet %'].min()}%")
    col3.metric("🌐 Global Avg (sample)", f"{df['Internet %'].mean():.1f}%", "")

    with st.expander("📌 Insight"):
        st.write(
            "Choropleth maps encode a continuous variable through colour intensity across geographic regions. "
            "They excel at revealing spatial patterns and regional disparities. "
            "The colour scale should be perceptually uniform — sequential palettes work best for ratio data."
        )


# ═══════════════════════════════════════════════════════════════
# 5. RELATIONSHIPS — Scatter + Bubble Chart
# ═══════════════════════════════════════════════════════════════
elif chart_choice.startswith("5"):
    st.markdown('<span class="purpose-tag">PURPOSE 05 — RELATIONSHIPS & CORRELATIONS</span>', unsafe_allow_html=True)
    st.title("Charting Relationships & Correlations")
    st.markdown("**Chart type:** Bubble Scatter Plot  \n**Dataset:** Country GDP per Capita vs Life Expectancy (2024 est.)")

    np.random.seed(21)
    countries = [
        "USA", "Norway", "Switzerland", "Germany", "UK", "France", "Japan", "South Korea",
        "Australia", "Canada", "Italy", "Spain", "Brazil", "China", "India", "Mexico",
        "Nigeria", "Ethiopia", "Pakistan", "Egypt", "Indonesia", "Turkey", "Argentina",
        "South Africa", "Saudi Arabia", "Russia", "Poland", "Sweden", "Denmark", "Finland",
    ]
    regions = [
        "Americas", "Europe", "Europe", "Europe", "Europe", "Europe", "Asia", "Asia",
        "Oceania", "Americas", "Europe", "Europe", "Americas", "Asia", "Asia", "Americas",
        "Africa", "Africa", "Asia", "Africa", "Asia", "Europe", "Americas",
        "Africa", "Middle East", "Europe", "Europe", "Europe", "Europe", "Europe",
    ]
    gdp = [
        80000, 106000, 98000, 54000, 47000, 44000, 38000, 36000,
        65000, 57000, 37000, 33000, 10000, 12000, 2400, 11000,
        2100, 1000, 1500, 3700, 4600, 12000, 13000,
        6500, 28000, 15000, 20000, 61000, 68000, 55000,
    ]
    life_exp = [
        78, 83, 84, 81, 81, 82, 84, 83,
        83, 82, 83, 83, 75, 77, 70, 75,
        54, 66, 67, 72, 72, 78, 76,
        64, 76, 73, 77, 82, 82, 82,
    ]
    population = np.random.randint(1, 140, size=30) * 10  # millions, rough

    df = pd.DataFrame({
        "Country": countries,
        "Region": regions,
        "GDP per Capita ($)": gdp,
        "Life Expectancy": life_exp,
        "Population (M)": population,
    })

    region_colors = {
        "Americas": "#f472b6",
        "Europe": "#7c6af7",
        "Asia": "#38bdf8",
        "Africa": "#fb923c",
        "Oceania": "#34d399",
        "Middle East": "#facc15",
    }

    fig = px.scatter(
        df,
        x="GDP per Capita ($)",
        y="Life Expectancy",
        size="Population (M)",
        color="Region",
        hover_name="Country",
        text="Country",
        size_max=50,
        color_discrete_map=region_colors,
        log_x=True,
        labels={"GDP per Capita ($)": "GDP per Capita (USD, log scale)", "Life Expectancy": "Life Expectancy (years)"},
    )

    # Trendline via numpy
    log_gdp = np.log10(df["GDP per Capita ($)"])
    z = np.polyfit(log_gdp, df["Life Expectancy"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(log_gdp.min(), log_gdp.max(), 100)
    fig.add_trace(go.Scatter(
        x=10 ** x_line,
        y=p(x_line),
        mode="lines",
        line=dict(color="rgba(255,255,255,0.19)", dash="dot", width=1.5),
        name="Trend",
        hoverinfo="skip",
    ))

    fig.update_traces(
        textposition="top center",
        textfont=dict(size=9, color="#aaa"),
        selector=dict(mode="markers+text"),
    )

    fig.update_layout(
        paper_bgcolor="#161616",
        plot_bgcolor="#161616",
        font=dict(color="#f0f0f0", family="DM Sans"),
        xaxis=dict(showgrid=True, gridcolor="#252525", tickfont=dict(color="#888")),
        yaxis=dict(showgrid=True, gridcolor="#252525", tickfont=dict(color="#888"), range=[50, 90]),
        legend=dict(bgcolor="#1e1e1e", bordercolor="#2a2a2a", borderwidth=1),
        margin=dict(l=20, r=20, t=20, b=20),
        height=480,
    )

    st.plotly_chart(fig, use_container_width=True)

    corr = np.corrcoef(np.log10(df["GDP per Capita ($)"]), df["Life Expectancy"])[0, 1]
    col1, col2, col3 = st.columns(3)
    col1.metric("Pearson Correlation (log GDP)", f"{corr:.3f}", "Strong positive")
    col2.metric("Highest GDP/capita", "Norway", "$106,000")
    col3.metric("Longest Life Expectancy", "Switzerland / Japan", "84 yrs")

    with st.expander("📌 Insight"):
        st.write(
            "Scatter plots reveal the relationship between two continuous variables. "
            "Adding a third dimension (bubble size) and a fourth (colour by category) enables rich multivariate storytelling. "
            "A log scale on GDP linearises the relationship, making the positive correlation with life expectancy much cleaner. "
            "The dotted trendline confirms the direction without overpowering the data."
        )
