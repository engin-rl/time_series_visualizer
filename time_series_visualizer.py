import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df = df.set_index("date").reset_index()

df["date"] = pd.to_datetime(df["date"])
print(df.head())


# Clean data

df = df[
    (
        (df["value"] >= df["value"].quantile(0.025))
        & (df["value"] <= df["value"].quantile(0.975))
    )
]

print(df.count())


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


'''def draw_bar_plot():
    # Copy and modify data for monthly bar plot

    # df["month"] = df["date"].dt.month
    # df["monthly_average"] = df["date"].dt.month

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month_name()
    df["year"] = df["date"].dt.year

    df_group = (
        df.groupby(["year", "month"])
        .agg({"value": "mean"})
        .sort_values("month")
        .reset_index()
    )

    print(df)
    print(df_group)

    df_melted = pd.melt(df_group, id_vars=["year", "month"], value_name="average")

    print(df_melted)

    # plt.show()

    """years = df_group["year"]
    months = df_group["month"]
    monthly_average = df_group["value"]
    plt.bar(years, monthly_average)
    plt.show()"""

    # Save image and return fig (don't change this part)
    # fig.savefig("bar_plot.png")
    # return fig


draw_bar_plot()'''


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]

    # Draw box plots (using Seaborn)

    # Save image and return fig (don't change this part)
    fig.savefig("box_plot.png")
    return fig
