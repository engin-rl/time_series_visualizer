import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df2 = df.copy()
df = df.set_index("date").reset_index()

df["date"] = pd.to_datetime(df["date"])

# lineplot
df = df[
    (
        (df["value"] >= df["value"].quantile(0.025))
        & (df["value"] <= df["value"].quantile(0.975))
    )
]

# barplot
df2 = df2[
    (
        (df2["value"] >= df2["value"].quantile(0.025))
        & (df2["value"] <= df2["value"].quantile(0.975))
    )
]

df2["date"] = pd.to_datetime(df2["date"])
df2.set_index("date", inplace=True)

# df2_resample = df2.resample("M").mean()
# or
df2_resample = df2.resample("ME").agg({"value": "mean"})

# df2["months"] = df2.index.month_name()
df2_resample["year"] = df2_resample.index.year
df2_resample["month"] = df2_resample.index.month_name()

df2_grouped = df2_resample.groupby(["year", "month"])["value"].sum().reset_index()
months_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
df2_grouped["month"] = pd.Categorical(
    df2_grouped["month"], categories=months_order, ordered=True
)

pivot_df = df2_grouped.pivot(index="year", columns="month", values="value")


# boxplot


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(df["date"], df["value"], linestyle="-", color="r")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig("line_plot.png")
    plt.show()
    return fig


def draw_bar_plot():

    # Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    pivot_df.plot(kind="bar", ax=ax)
    ax.set_ylabel("Average Page Views")
    ax.set_xlabel("Years")
    ax.set_xticks(range(len(pivot_df.index)))
    ax.set_xticklabels(pivot_df.index, rotation=90)
    ax.legend(title="Months")
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]
    df_box = df_box.reset_index().drop(columns=["index", "date"])
    df_box_year = df_box[["year", "value"]]
    df_box_month = df_box[["month", "value"]]
    months_order_2 = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    df_box_month["month"] = pd.Categorical(
        df_box_month["month"], categories=months_order_2, ordered=True
    )

    print(df_box_month["month"])

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(24, 8))
    sns.boxplot(x="year", y="value", data=df_box_year, ax=ax[0])
    ax[0].set_ylabel("Page Views")
    ax[0].set_xlabel("Year")
    ax[0].set_title("Year-wise Box Plot (Trend)")

    sns.boxplot(x="month", y="value", data=df_box_month, ax=ax[1])
    ax[1].set_ylabel("Page Views")
    ax[1].set_xlabel("Month")
    ax[1].set_title("Month-wise Box Plot (Seasonality)")

    # Save image and return fig (don't change this part)
    fig.savefig("box_plot.png")
    plt.show()
    return fig
