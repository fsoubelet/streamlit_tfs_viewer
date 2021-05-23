import pandas as pd
import pandas_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report

# ----- Display Components ----- #


def display_file_headers(headers_dict: dict) -> None:
    """Simply display headers dict."""
    st.header("File Headers", anchor="headers")
    st.write(headers_dict)


def display_file_dataframe(data_frame: pd.DataFrame, height: int) -> None:
    """Simply display dataframe."""
    st.header("File Data", anchor="dataframe")
    st.dataframe(data_frame, height=height)


def display_dataframe_report(data_frame: pd.DataFrame) -> None:
    """
    Generate and display in an expandable block the profile report of the data frame from pandas_profiling.
    """
    with st.beta_expander("EXPLORATIVE REPORT (Collapsible)"):
        st_profile_report(data_frame.profile_report(explorative=True))


# ----- Chart Components ----- #


def get_plot_df(data_frame: pd.DataFrame, key: str = None) -> pd.DataFrame:
    """
    Get a simple DataFrame with only elements relevant to the desired plotting, queried as select boxes in
    streamlit. A select box will query for a column to use as horizontal axis, and another for all columns
    to plot versus the aforementioned quantity.

    Args:
        data_frame (pd.DataFrame): the original dataframe to pick elements from.
        key (str): unique identifier for the select boxes in case the fucntion is used several times in app.

    Returns:
        The rearranged pandas.DataFrame.
    """
    plot_versus, plot_columns = st.beta_columns([1, 3])
    with plot_versus:
        versus = st.selectbox(
            "Property to Plot Against",
            options=data_frame.columns.to_numpy(),
            help="Select the column that will be on the horizontal axis",
            key=key,
        )
    plot_df = data_frame.set_index(versus, drop=True)
    with plot_columns:
        to_plot = st.multiselect(
            "Columns to Plot",
            options=plot_df.columns.to_numpy(),
            help="Select the columns to plot in this chart",
            key=key,
        )
    plot_df = plot_df.loc[:, to_plot]
    return plot_df


def craft_line_chart(data_frame: pd.DataFrame, height: int) -> None:
    """
    Query for columns to plot and display a simple line chart via streamlit's syntactic sugar around Altair.
    """
    st.header("Craft Your Own Line Chart", anchor="line_chart")
    plot_df = get_plot_df(data_frame, key="line_chart_widgets")
    st.line_chart(plot_df, height=height)


def craft_bar_chart(data_frame: pd.DataFrame, height: int) -> None:
    """
    Query for columns to plot and display a simple bar chart via streamlit's syntactic sugar around Altair.
    """
    st.header("Craft Your Own Bar Chart", anchor="bar_chart")
    plot_df = get_plot_df(data_frame, key="bar_chart_widgets")
    st.bar_chart(plot_df, height=height)
