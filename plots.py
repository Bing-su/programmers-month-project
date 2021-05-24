import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


def rating_average(df, style):
    if style == "altair":
        with st.echo():
            fig = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x="mean(average rating):Q",
                    y=alt.Y("category:N", sort="-x"),
                    color=alt.Color("category:N", legend=None),
                )
            )
        return fig

    elif style == "seaborn":
        fig, ax = plt.subplots()
        with st.echo():
            result = (
                df.groupby("category")
                .mean()
                .reset_index()
                .sort_values("average rating", ascending=False)
            )

            sns.barplot(
                x="average rating", y="category", data=df, order=result["category"],
            )
        return fig


def rating_sum(df, style):
    if style == "altair ":
        with st.echo():
            brush = alt.selection(type="interval", encodings=["y"])

            bar = (
                alt.Chart()
                .mark_bar()
                .encode(
                    x="mean(total ratings):Q",
                    y=alt.Y("category:N", sort="-x"),
                    color=alt.Color("category:N", legend=None),
                    opacity=alt.condition(
                        brush, alt.OpacityValue(1), alt.OpacityValue(0.7)
                    ),
                )
                .add_selection(brush)
            )

            line = (
                alt.Chart()
                .mark_rule(color="firebrick")
                .encode(x="mean(total ratings):Q", size=alt.SizeValue(3))
                .transform_filter(brush)
            )

            fig = alt.layer(bar, line, data=df)
        return fig

    elif style == "seaborn":
        fig, ax = plt.subplots()
        with st.echo():
            result = (
                df.groupby("category")
                .mean()
                .reset_index()
                .sort_values("total ratings", ascending=False)
            )

            sns.barplot(
                x="total ratings", y="category", data=df, order=result["category"],
            )
        return fig


def top10(df, genre, col):
    with st.echo():
        top10 = df[df["category"] == genre].iloc[:10, :]

        fig = (
            alt.Chart(top10)
            .mark_bar()
            .encode(
                x=f"{col}:Q",
                y=alt.Y("title:N", sort={"field": "rank"}),
                color=alt.Color(f"{col}:Q", legend=None),
            )
        )

    return fig


def growth(df, days):
    days = 30 if days == "30일" else 60

    with st.echo():
        selection = alt.selection(type="single", on="mouseover", fields=["category"])

        fig = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=f"mean(growth ({days} days)):Q",
                y=alt.Y("category:N", sort="-x"),
                color=alt.Color("category:N", legend=None),
                opacity=alt.condition(selection, alt.value(1), alt.value(0.5)),
            )
            .add_selection(selection)
        )

    return fig

