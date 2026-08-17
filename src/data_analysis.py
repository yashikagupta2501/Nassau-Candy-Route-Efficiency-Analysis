import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "Nassau Candy Distributor.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# PRODUCT -> FACTORY MAPPING
# ============================================================

PRODUCT_FACTORY = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    """Load and prepare the Nassau Candy dataset."""

    df = pd.read_csv(DATA_PATH)

    # Convert dates
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        dayfirst=True
    )

    # Adjust ship date to correct the dataset date offset
    DATE_SHIFT = 909

    df["Adjusted Ship Date"] = (
    df["Ship Date"] - pd.Timedelta(days=DATE_SHIFT)
    )

# Calculate corrected shipping lead time
    df["Lead Time"] = (
    df["Adjusted Ship Date"] - df["Order Date"]
    ).dt.days

    # Map products to factories
    df["Factory"] = df["Product Name"].map(
        PRODUCT_FACTORY
    )

    # Create Factory -> Customer State route
    df["Route"] = (
        df["Factory"].astype(str)
        + " -> "
        + df["State/Province"].astype(str)
    )

    return df


# ============================================================
# DATA VALIDATION
# ============================================================

def validate_data(df):
    """Validate shipment records."""

    total_records = len(df)

    valid_df = df[
        df["Lead Time"].notna()
        & (df["Lead Time"] >= 0)
    ].copy()

    invalid_records = total_records - len(valid_df)

    print("\n" + "=" * 60)
    print("DATA VALIDATION")
    print("=" * 60)

    print("Total Records:", total_records)
    print("Valid Records:", len(valid_df))
    print("Invalid Lead-Time Records:", invalid_records)

    return valid_df


# ============================================================
# BASIC SUMMARY
# ============================================================

def basic_summary(df):
    """Display basic dataset summary."""

    print("\n" + "=" * 60)
    print("NASSAU CANDY ROUTE EFFICIENCY ANALYSIS")
    print("=" * 60)

    print("\nTotal Records:", len(df))
    print("Columns:", len(df.columns))

    print("\nFactories:", df["Factory"].nunique())
    print("Routes:", df["Route"].nunique())
    print("States:", df["State/Province"].nunique())

    print("\nTotal Sales:", round(df["Sales"].sum(), 2))
    print("Total Gross Profit:", round(df["Gross Profit"].sum(), 2))
    print("Total Units:", df["Units"].sum())


# ============================================================
# ROUTE KPI ANALYSIS
# ============================================================

def route_kpi_analysis(df):
    """Calculate route-level KPIs."""

    route_kpi = (
        df.groupby("Route")
        .agg(
            Shipment_Volume=("Order ID", "count"),
            Average_Lead_Time=("Lead Time", "mean"),
            Median_Lead_Time=("Lead Time", "median"),
            Lead_Time_Std=("Lead Time", "std"),
            Minimum_Lead_Time=("Lead Time", "min"),
            Maximum_Lead_Time=("Lead Time", "max")
        )
        .reset_index()
    )

    route_kpi["Lead_Time_Range"] = (
        route_kpi["Maximum_Lead_Time"]
        - route_kpi["Minimum_Lead_Time"]
    )

    return route_kpi


# ============================================================
# DELAY ANALYSIS
# ============================================================

def delay_analysis(df):
    """
    Identify delayed shipments.

    The project analysis uses 365 days as the lead-time
    threshold for delay classification.
    """

    DELAY_THRESHOLD = 729

    df = df.copy()

    df["Delayed"] = (
        df["Lead Time"] > DELAY_THRESHOLD
    )

    return df


# ============================================================
# FACTORY IMPACT
# ============================================================

def factory_analysis(df):

    factory_impact = (
        df.groupby("Factory")
        .agg(
            Total_Shipments=("Order ID", "count"),
            Delayed_Shipments=("Delayed", "sum"),
            Average_Lead_Time=("Lead Time", "mean"),
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum")
        )
    )

    factory_impact["Delay_Rate_%"] = (
        factory_impact["Delayed_Shipments"]
        / factory_impact["Total_Shipments"]
        * 100
    )

    return factory_impact


# ============================================================
# REGION IMPACT
# ============================================================

def region_analysis(df):

    region_impact = (
        df.groupby("Region")
        .agg(
            Total_Shipments=("Order ID", "count"),
            Delayed_Shipments=("Delayed", "sum"),
            Average_Lead_Time=("Lead Time", "mean"),
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum")
        )
    )

    region_impact["Delay_Rate_%"] = (
        region_impact["Delayed_Shipments"]
        / region_impact["Total_Shipments"]
        * 100
    )

    return region_impact


# ============================================================
# SHIP MODE IMPACT
# ============================================================

def ship_mode_analysis(df):

    ship_mode_impact = (
        df.groupby("Ship Mode")
        .agg(
            Total_Shipments=("Order ID", "count"),
            Delayed_Shipments=("Delayed", "sum"),
            Average_Lead_Time=("Lead Time", "mean"),
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum")
        )
    )

    ship_mode_impact["Delay_Rate_%"] = (
        ship_mode_impact["Delayed_Shipments"]
        / ship_mode_impact["Total_Shipments"]
        * 100
    )

    return ship_mode_impact


# ============================================================
# PRODUCT IMPACT
# ============================================================

def product_analysis(df):

    product_impact = (
        df.groupby("Product Name")
        .agg(
            Total_Shipments=("Order ID", "count"),
            Delayed_Shipments=("Delayed", "sum"),
            Average_Lead_Time=("Lead Time", "mean"),
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum"),
            Units=("Units", "sum")
        )
    )

    product_impact["Delay_Rate_%"] = (
        product_impact["Delayed_Shipments"]
        / product_impact["Total_Shipments"]
        * 100
    )

    return product_impact


# ============================================================
# HIGH-RISK ROUTES
# ============================================================

def high_risk_route_analysis(df):

    route_risk = (
        df.groupby("Route")
        .agg(
            Shipment_Volume=("Order ID", "count"),
            Delayed_Shipments=("Delayed", "sum"),
            Average_Lead_Time=("Lead Time", "mean"),
            Sales=("Sales", "sum"),
            Gross_Profit=("Gross Profit", "sum")
        )
    )

    route_risk["Delay_Rate_%"] = (
        route_risk["Delayed_Shipments"]
        / route_risk["Shipment_Volume"]
        * 100
    )

    return route_risk.sort_values(
        "Delay_Rate_%",
        ascending=False
    )


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

def correlation_analysis(route_kpi):

    correlation = route_kpi[
        [
            "Shipment_Volume",
            "Average_Lead_Time",
            "Lead_Time_Std"
        ]
    ].corr()

    print("\n" + "=" * 60)
    print("ROUTE KPI CORRELATION MATRIX")
    print("=" * 60)

    print(correlation.round(3))

    volume_lead_time = correlation.loc[
        "Shipment_Volume",
        "Average_Lead_Time"
    ]

    print(
        "\nShipment Volume vs Average Lead Time:",
        round(volume_lead_time, 3)
    )

    return correlation


# ============================================================
# SAVE CHART
# ============================================================

def save_bar_chart(data, column, title, filename):

    chart_data = data[column].sort_values()

    plt.figure(figsize=(10, 6))

    chart_data.plot(kind="barh")

    plt.title(title)
    plt.xlabel(column)
    plt.ylabel("")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    # Load data
    df = load_data()

    # Basic summary
    basic_summary(df)

    # Validate records
    df_valid = validate_data(df)

    # Delay classification
    df_valid = delay_analysis(df_valid)

    # --------------------------------------------------------
    # Overall KPIs
    # --------------------------------------------------------

    total_shipments = len(df_valid)

    delayed_shipments = int(
        df_valid["Delayed"].sum()
    )

    delay_rate = (
        delayed_shipments
        / total_shipments
        * 100
    )

    print("\n" + "=" * 60)
    print("OVERALL KPI SUMMARY")
    print("=" * 60)

    print("Valid Shipments:", total_shipments)
    print("Delayed Shipments:", delayed_shipments)
    print("Delay Rate:", round(delay_rate, 2), "%")
    print(
        "Average Lead Time:",
        round(df_valid["Lead Time"].mean(), 2)
    )
    print(
        "Median Lead Time:",
        round(df_valid["Lead Time"].median(), 2)
    )

    # --------------------------------------------------------
    # Route KPIs
    # --------------------------------------------------------

    route_kpi = route_kpi_analysis(df_valid)

    print("\n" + "=" * 60)
    print("TOP 10 SLOWEST ROUTES")
    print("=" * 60)

    print(
        route_kpi
        .sort_values(
            "Average_Lead_Time",
            ascending=False
        )
        .head(10)
        .round(2)
        .to_string(index=False)
    )

    # --------------------------------------------------------
    # Factory Analysis
    # --------------------------------------------------------

    factory_impact = factory_analysis(df_valid)

    print("\n" + "=" * 60)
    print("FACTORY PERFORMANCE")
    print("=" * 60)

    print(
        factory_impact
        .sort_values(
            "Delay_Rate_%",
            ascending=False
        )
        .round(2)
    )

    # --------------------------------------------------------
    # Region Analysis
    # --------------------------------------------------------

    region_impact = region_analysis(df_valid)

    print("\n" + "=" * 60)
    print("REGION PERFORMANCE")
    print("=" * 60)

    print(
        region_impact
        .sort_values(
            "Delay_Rate_%",
            ascending=False
        )
        .round(2)
    )

    # --------------------------------------------------------
    # Ship Mode Analysis
    # --------------------------------------------------------

    ship_mode_impact = ship_mode_analysis(df_valid)

    print("\n" + "=" * 60)
    print("SHIP MODE PERFORMANCE")
    print("=" * 60)

    print(
        ship_mode_impact
        .sort_values(
            "Delay_Rate_%",
            ascending=False
        )
        .round(2)
    )

    # --------------------------------------------------------
    # Product Analysis
    # --------------------------------------------------------

    product_impact = product_analysis(df_valid)

    print("\n" + "=" * 60)
    print("TOP PRODUCTS BY DELAYED SHIPMENTS")
    print("=" * 60)

    print(
        product_impact
        .sort_values(
            "Delayed_Shipments",
            ascending=False
        )
        .head(10)
        .round(2)
    )

    # --------------------------------------------------------
    # High Risk Routes
    # --------------------------------------------------------

    high_risk_routes = high_risk_route_analysis(
        df_valid
    )

    print("\n" + "=" * 60)
    print("TOP 10 HIGH-RISK ROUTES")
    print("=" * 60)

    print(
        high_risk_routes
        .head(10)
        .round(2)
    )

    # --------------------------------------------------------
    # High Volume + High Risk Routes
    # --------------------------------------------------------

    high_volume_routes = (
        high_risk_routes[
            high_risk_routes["Shipment_Volume"] >= 20
        ]
        .head(10)
    )

    print("\n" + "=" * 60)
    print("HIGH-VOLUME ROUTES WITH HIGH DELAY RATES")
    print("=" * 60)

    print(
        high_volume_routes
        .round(2)
    )

    # --------------------------------------------------------
    # Correlation
    # --------------------------------------------------------

    correlation_analysis(route_kpi)

    # --------------------------------------------------------
    # Save Important Charts
    # --------------------------------------------------------

    save_bar_chart(
        factory_impact,
        "Delay_Rate_%",
        "Factory-wise Shipment Delay Rate",
        "factory_delay_rate.png"
    )

    save_bar_chart(
        region_impact,
        "Delay_Rate_%",
        "Region-wise Shipment Delay Rate",
        "region_delay_rate.png"
    )

    save_bar_chart(
        ship_mode_impact,
        "Delay_Rate_%",
        "Ship Mode-wise Shipment Delay Rate",
        "ship_mode_delay_rate.png"
    )

    save_bar_chart(
        product_impact
        .sort_values(
            "Delay_Rate_%",
            ascending=False
        )
        .head(10),
        "Delay_Rate_%",
        "Top 10 Products by Delay Rate",
        "top_products_delay_rate.png"
    )

    save_bar_chart(
        high_risk_routes.head(10),
        "Delay_Rate_%",
        "Top 10 High-Risk Routes",
        "top_high_risk_routes.png"
    )

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(
        "\nCharts saved in:",
        OUTPUT_DIR
    )


if __name__ == "__main__":
    main()