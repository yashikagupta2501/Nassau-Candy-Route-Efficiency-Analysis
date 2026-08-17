import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

sys.path.append(str(SRC_DIR))

from data_analysis import load_data, validate_data, delay_analysis


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Nassau Candy Route Efficiency",
    page_icon="🍫",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🍫 Nassau Candy Route Efficiency Analysis")

st.markdown(
    """
    **Business & Logistics Performance Dashboard**

    Interactive analysis of shipment delays, factories, regions,
    shipping modes, products, and high-risk routes.
    """
)


# --------------------------------------------------
# LOAD AND PREPARE DATA
# --------------------------------------------------

@st.cache_data
def get_data():

    df = load_data()

    df_valid = validate_data(df)

    df_valid = delay_analysis(df_valid)

    return df_valid


df = get_data()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Filters")


# Factory filter
if "Factory" in df.columns:

    factories = sorted(df["Factory"].dropna().unique())

    selected_factories = st.sidebar.multiselect(
        "Factory",
        factories,
        default=factories
    )

else:
    selected_factories = []


# Region filter
if "Region" in df.columns:

    regions = sorted(df["Region"].dropna().unique())

    selected_regions = st.sidebar.multiselect(
        "Region",
        regions,
        default=regions
    )

else:
    selected_regions = []


# Ship Mode filter
if "Ship Mode" in df.columns:

    ship_modes = sorted(df["Ship Mode"].dropna().unique())

    selected_ship_modes = st.sidebar.multiselect(
        "Ship Mode",
        ship_modes,
        default=ship_modes
    )

else:
    selected_ship_modes = []


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()


if "Factory" in filtered_df.columns and selected_factories:
    filtered_df = filtered_df[
        filtered_df["Factory"].isin(selected_factories)
    ]


if "Region" in filtered_df.columns and selected_regions:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(selected_regions)
    ]


if "Ship Mode" in filtered_df.columns and selected_ship_modes:
    filtered_df = filtered_df[
        filtered_df["Ship Mode"].isin(selected_ship_modes)
    ]


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_shipments = len(filtered_df)

delayed_shipments = int(
    filtered_df["Delayed"].sum()
)

delay_rate = (
    delayed_shipments / total_shipments * 100
    if total_shipments > 0
    else 0
)

average_lead_time = (
    filtered_df["Lead Time"].mean()
    if total_shipments > 0
    else 0
)

median_lead_time = (
    filtered_df["Lead Time"].median()
    if total_shipments > 0
    else 0
)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Valid Shipments",
        f"{total_shipments:,}"
    )

with col2:
    st.metric(
        "Delayed Shipments",
        f"{delayed_shipments:,}"
    )

with col3:
    st.metric(
        "Delay Rate",
        f"{delay_rate:.2f}%"
    )

with col4:
    st.metric(
        "Average Lead Time",
        f"{average_lead_time:.2f} days"
    )


st.divider()


# --------------------------------------------------
# FACTORY PERFORMANCE
# --------------------------------------------------

st.subheader("🏭 Factory Performance")

if "Factory" in filtered_df.columns:

    factory_data = (
        filtered_df
        .groupby("Factory")
        .agg(
            Total_Shipments=("Delayed", "count"),
            Delayed_Shipments=("Delayed", "sum")
        )
    )

    factory_data["Delay_Rate_%"] = (
        factory_data["Delayed_Shipments"]
        / factory_data["Total_Shipments"]
        * 100
    )

    factory_data = factory_data.sort_values(
        "Delay_Rate_%",
        ascending=False
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    factory_data["Delay_Rate_%"].plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Delay Rate (%)")
    ax.set_ylabel("Factory")
    ax.set_title("Factory-wise Shipment Delay Rate")

    st.pyplot(fig)

    st.dataframe(
        factory_data.round(2),
        use_container_width=True
    )


# --------------------------------------------------
# REGION PERFORMANCE
# --------------------------------------------------

st.subheader("🌎 Region Performance")

if "Region" in filtered_df.columns:

    region_data = (
        filtered_df
        .groupby("Region")
        .agg(
            Total_Shipments=("Delayed", "count"),
            Delayed_Shipments=("Delayed", "sum")
        )
    )

    region_data["Delay_Rate_%"] = (
        region_data["Delayed_Shipments"]
        / region_data["Total_Shipments"]
        * 100
    )

    region_data = region_data.sort_values(
        "Delay_Rate_%",
        ascending=False
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    region_data["Delay_Rate_%"].plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Delay Rate (%)")
    ax.set_ylabel("Region")
    ax.set_title("Region-wise Shipment Delay Rate")

    st.pyplot(fig)

    st.dataframe(
        region_data.round(2),
        use_container_width=True
    )


# --------------------------------------------------
# SHIPPING MODE PERFORMANCE
# --------------------------------------------------

st.subheader("🚚 Shipping Mode Performance")

if "Ship Mode" in filtered_df.columns:

    ship_data = (
        filtered_df
        .groupby("Ship Mode")
        .agg(
            Total_Shipments=("Delayed", "count"),
            Delayed_Shipments=("Delayed", "sum")
        )
    )

    ship_data["Delay_Rate_%"] = (
        ship_data["Delayed_Shipments"]
        / ship_data["Total_Shipments"]
        * 100
    )

    ship_data = ship_data.sort_values(
        "Delay_Rate_%",
        ascending=False
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ship_data["Delay_Rate_%"].plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Delay Rate (%)")
    ax.set_ylabel("Ship Mode")
    ax.set_title("Ship Mode-wise Shipment Delay Rate")

    st.pyplot(fig)

    st.dataframe(
        ship_data.round(2),
        use_container_width=True
    )


# --------------------------------------------------
# PRODUCT PERFORMANCE
# --------------------------------------------------

st.subheader("🍬 Top Products by Delay Rate")

if "Product Name" in filtered_df.columns:

    product_data = (
        filtered_df
        .groupby("Product Name")
        .agg(
            Total_Shipments=("Delayed", "count"),
            Delayed_Shipments=("Delayed", "sum")
        )
    )

    product_data["Delay_Rate_%"] = (
        product_data["Delayed_Shipments"]
        / product_data["Total_Shipments"]
        * 100
    )

    product_data = (
        product_data
        .sort_values("Delay_Rate_%", ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    product_data["Delay_Rate_%"].sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Delay Rate (%)")
    ax.set_ylabel("Product")
    ax.set_title("Top 10 Products by Delay Rate")

    st.pyplot(fig)

    st.dataframe(
        product_data.round(2),
        use_container_width=True
    )


# --------------------------------------------------
# ROUTE PERFORMANCE
# --------------------------------------------------

st.subheader("🛣️ High-Risk Routes")

if "Route" in filtered_df.columns:

    route_data = (
        filtered_df
        .groupby("Route")
        .agg(
            Shipment_Volume=("Delayed", "count"),
            Delayed_Shipments=("Delayed", "sum"),
            Average_Lead_Time=("Lead Time", "mean")
        )
    )

    route_data["Delay_Rate_%"] = (
        route_data["Delayed_Shipments"]
        / route_data["Shipment_Volume"]
        * 100
    )

    high_risk_routes = (
        route_data
        .sort_values("Delay_Rate_%", ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(11, 6))

    high_risk_routes["Delay_Rate_%"].sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Delay Rate (%)")
    ax.set_ylabel("Route")
    ax.set_title("Top 10 High-Risk Routes")

    st.pyplot(fig)

    st.dataframe(
        high_risk_routes.round(2),
        use_container_width=True
    )


# --------------------------------------------------
# LEAD TIME SUMMARY
# --------------------------------------------------

st.subheader("⏱️ Lead Time Analysis")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Average Lead Time",
        f"{average_lead_time:.2f} days"
    )

with col2:

    st.metric(
        "Median Lead Time",
        f"{median_lead_time:.2f} days"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Nassau Candy Route Efficiency Analysis | "
    "Python • Pandas • NumPy • Matplotlib • Streamlit"
)