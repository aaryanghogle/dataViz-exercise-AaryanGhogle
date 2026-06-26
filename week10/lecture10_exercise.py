
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="CO2 Dashboard", page_icon="🌱", layout="wide")

# ── Data ──────────────────────────────────────────────────────────────────────
# @st.cache_data: Streamlit reruns the entire script on every widget interaction.
# Without caching, the CSV is read from disk on every interaction — slow and wasteful.
# cache_data stores the result after the first run and reuses it until the file changes.
@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / 'data' / 'co2_emissions.csv'
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-01-01')
    return df

df = load_data()

st.title("🌱 CO2 Emissions Explorer")
st.caption("Source: Our World in Data — ourworldindata.org/co2-emissions")

# ── TASK 1: Sidebar with 5 widgets ────────────────────────────────────────────
#   a) st.selectbox for Region (with 'All')
#   b) st.multiselect for Countries (updates based on region — chained)
#   c) st.date_input for date range (two-handle; convert years to Jan-1 dates)
#   d) st.radio for Metric: "Total CO2 (Mt)" vs "CO2 per capita"
#   e) st.checkbox labelled "Show only top emitter highlighted"
#
# Guards:
#   - empty countries → st.warning + st.stop()
#   - incomplete date_input → st.warning + st.stop()
# Convert date_input result to pd.Timestamp before filtering.
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    # YOUR CODE HERE
    import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="CO2 Dashboard", page_icon="🌲", layout="wide")

# — Data —
# @st.cache_data: Streamlit reruns the entire script on every widget interaction.
# Without caching, the CSV is read from disk on every interaction — slow and wasteful.
# cache_data stores the result after the first run and reuses it until the file changes.
@st.cache_data
def load_data():
    path = Path(__file__).parent / 'data' / 'co2_emissions.csv'
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-01-01')
    return df

df = load_data()

st.title("🌲 CO2 Emissions Explorer")
st.caption("Source: Our World in Data – ourworldindata.org/co2-emissions")

# — TASK 1: Sidebar with 5 widgets —
with st.sidebar:
    st.header("Filters")
    
    # a) Region selectbox with 'All'
    regions = ['All'] + sorted(df['Region'].unique())
    selected_region = st.selectbox("Region", regions)
    
    # b) Countries multiselect (chained to region)
    if selected_region == 'All':
        available_countries = sorted(df['Country'].unique())
    else:
        available_countries = sorted(df[df['Region'] == selected_region]['Country'].unique())
    
    selected_countries = st.multiselect("Countries", available_countries)
    
    # Guard: empty countries
    if selected_countries == []:
        st.warning("Please select at least one country")
        st.stop()
    
    # c) Date range input (two-handle)
    date_range = st.date_input(
        "Date Range",
        value=[df['Date'].min(), df['Date'].max()],
        format="YYYY-MM-DD"
    )
    
    # Guard: incomplete date input
    if len(date_range) < 2:
        st.warning("Please select both start and end dates")
        st.stop()
    
    # Convert to pd.Timestamp for filtering
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])
    
    # d) Radio for metric
    metric = st.radio(
        "Metric",
        ["Total CO2 (Mt)", "CO2 per capita"]
    )
    
    # e) Checkbox for top emitter highlight
    highlight_top = st.checkbox("Show only top emitter highlighted")

# — Data filtering —
filtered_df = df[
    (df['Country'].isin(selected_countries)) &
    (df['Date'] >= start_date) &
    (df['Date'] <= end_date)
]

# Map metric selection to column name
metric_column = 'CO2_Total_Mt' if metric == "Total CO2 (Mt)" else 'CO2_Per_Capita'

# — Visualization —
col1, col2 = st.columns(2)

with col1:
    # Time series chart
    fig_time = px.line(
        filtered_df,
        x='Date',
        y=metric_column,
        color='Country',
        title=f"{metric} Over Time",
        labels={metric_column: metric}
    )
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    # Latest values bar chart
    latest_data = filtered_df[filtered_df['Date'] == filtered_df['Date'].max()]
    
    if highlight_top:
        # Highlight top emitter
        top_emitter = latest_data.loc[latest_data[metric_column].idxmax(), 'Country']
        colors = ['#1f77b4' if c == top_emitter else '#d3d3d3' for c in latest_data['Country']]
    else:
        colors = '#1f77b4'
    
    fig_bar = px.bar(
        latest_data.sort_values(metric_column, ascending=True),
        x=metric_column,
        y='Country',
        orientation='h',
        title=f"{metric} (Latest Year)",
        labels={metric_column: metric},
        color_discrete_sequence=['#1f77b4'] if not highlight_top else None
    )
    
    if highlight_top:
        fig_bar.update_traces(marker_color=colors)
    
    st.plotly_chart(fig_bar, use_container_width=True)

# — Data Table —
st.subheader("Data View")
st.dataframe(
    filtered_df[[
        'Country', 'Region', 'Date', 'CO2_Total_Mt', 'CO2_Per_Capita'
    ]].sort_values(['Country', 'Date']),
    use_container_width=True
)


# filtered = ...  # apply all filters and store here


# ── TASK 2: Filter summary caption ────────────────────────────────────────────
# Show: "X countries | Region | Date range | Metric"
# BBD rule: always show users how many records match current filters
# ─────────────────────────────────────────────────────────────────────────────
# YOUR CODE HERE
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="CO2 Dashboard", page_icon="🌲", layout="wide")

# — Data —
# @st.cache_data: Streamlit reruns the entire script on every widget interaction.
# Without caching, the CSV is read from disk on every interaction — slow and wasteful.
# cache_data stores the result after the first run and reuses it until the file changes.
@st.cache_data
def load_data():
    path = Path(__file__).parent / 'data' / 'co2_emissions.csv'
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-01-01')
    return df

df = load_data()

st.title("🌲 CO2 Emissions Explorer")
st.caption("Source: Our World in Data – ourworldindata.org/co2-emissions")

# — TASK 2: Filter summary caption —
# Show: "X countries | Region | Date range | Metric"
# BBD rule: always show users how many records match current filters
region_display = selected_region if selected_region != 'All' else 'All regions'
date_range_str = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
record_count = len(filtered_df)

filter_summary = f"📊 {len(selected_countries)} countries | {region_display} | {date_range_str} | {metric} | **{record_count} records**"
st.caption(filter_summary)

# — TASK 1: Sidebar with 5 widgets —
with st.sidebar:
    st.header("Filters")
    
    # a) Region selectbox with 'All'
    regions = ['All'] + sorted(df['Region'].unique())
    selected_region = st.selectbox("Region", regions)
    
    # b) Countries multiselect (chained to region)
    if selected_region == 'All':
        available_countries = sorted(df['Country'].unique())
    else:
        available_countries = sorted(df[df['Region'] == selected_region]['Country'].unique())
    
    selected_countries = st.multiselect("Countries", available_countries)
    
    # Guard: empty countries
    if selected_countries == []:
        st.warning("Please select at least one country")
        st.stop()
    
    # c) Date range input (two-handle)
    date_range = st.date_input(
        "Date Range",
        value=[df['Date'].min(), df['Date'].max()],
        format="YYYY-MM-DD"
    )
    
    # Guard: incomplete date input
    if len(date_range) < 2:
        st.warning("Please select both start and end dates")
        st.stop()
    
    # Convert to pd.Timestamp for filtering
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])
    
    # d) Radio for metric
    metric = st.radio(
        "Metric",
        ["Total CO2 (Mt)", "CO2 per capita"]
    )
    
    # e) Checkbox for top emitter highlight
    highlight_top = st.checkbox("Show only top emitter highlighted")

# — Data filtering —
filtered_df = df[
    (df['Country'].isin(selected_countries)) &
    (df['Date'] >= start_date) &
    (df['Date'] <= end_date)
]

# Map metric selection to column name
metric_column = 'CO2_Total_Mt' if metric == "Total CO2 (Mt)" else 'CO2_Per_Capita'

# — Visualization —
col1, col2 = st.columns(2)

with col1:
    # Time series chart
    fig_time = px.line(
        filtered_df,
        x='Date',
        y=metric_column,
        color='Country',
        title=f"{metric} Over Time",
        labels={metric_column: metric}
    )
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    # Latest values bar chart
    latest_data = filtered_df[filtered_df['Date'] == filtered_df['Date'].max()]
    
    if highlight_top:
        # Highlight top emitter
        top_emitter = latest_data.loc[latest_data[metric_column].idxmax(), 'Country']
        colors = ['#1f77b4' if c == top_emitter else '#d3d3d3' for c in latest_data['Country']]
    else:
        colors = '#1f77b4'
    
    fig_bar = px.bar(
        latest_data.sort_values(metric_column, ascending=True),
        x=metric_column,
        y='Country',
        orientation='h',
        title=f"{metric} (Latest Year)",
        labels={metric_column: metric},
        color_discrete_sequence=['#1f77b4'] if not highlight_top else None
    )
    
    if highlight_top:
        fig_bar.update_traces(marker_color=colors)
    
    st.plotly_chart(fig_bar, use_container_width=True)

# — Data Table —
st.subheader("Data View")
st.dataframe(
    filtered_df[[
        'Country', 'Region', 'Date', 'CO2_Total_Mt', 'CO2_Per_Capita'
    ]].sort_values(['Country', 'Date']),
    use_container_width=True
)


# ── TASK 3: Two charts reacting to ALL filters ────────────────────────────────
#   Left: line chart — selected metric over time, one line per country
#         If "Show only top emitter highlighted" checkbox is on:
#           - grey all lines except the highest emitter in the date range
#           - label that country at the end of its line (SWD grey-and-highlight)
#   Right: bar chart — ranking for the last year in selected date range
#
# BBD colour requirement: name the colour type in a comment next to each chart
# SWD requirements: white background, insight title, use_container_width=True
# ─────────────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    # Line chart
    # YOUR CODE HERE
    pass

with col_right:
    # Bar chart
    # YOUR CODE HERE
    pass


# ── EXTENSION: KPI row above the charts ───────────────────────────────────────
#   - Total CO2 in last year of selected range (sum across selected countries)
#   - % change from first to last year
#   - Country with highest emissions in last year
# ─────────────────────────────────────────────────────────────────────────────
# YOUR CODE HERE (optional)