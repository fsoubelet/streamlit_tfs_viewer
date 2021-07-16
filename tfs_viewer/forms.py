from typing import Sequence, Tuple, Union

import pandas as pd
import plotly.express as px
import streamlit as st


def get_scatter_plot_params(data_frame: pd.DataFrame) -> Tuple[str, Sequence[str], str, int]:
    """
    Form to query the user for scatter plots options with minimal reloading.

    Args:
        data_frame (pd.DataFrame): The user loaded TFS data frame.

    Returns:
        A Tuple with the following user defined properties: X-axis column, Y-axis column, styling mode for
        the chart and figure height.
    """
    scatter_options_form = st.form("Scatter Plot Options")
    scatter_options_form.header("Customize You Scatter Plot")
    versus, columns, height, mode = scatter_options_form.beta_columns(spec=[2, 3, 2, 1])
    with versus:
        versus: str = st.selectbox(
            "Property to Plot Against",
            options=data_frame.columns.to_numpy(),
            help="Select the column that will be on the horizontal axis",
        )
    with columns:
        to_plot: Sequence[str] = st.multiselect(
            "Columns to Plot",
            options=data_frame.columns.to_numpy(),
            help="Select the columns to plot in this chart",
            key="columns_for_scatterplot",
        )
    with height:
        line_chart_height = st.select_slider(
            "ScatterPlot Figure Height", options=list(range(200, 1050, 50)), value=600
        )
    with mode:
        mode: str = st.selectbox(
            "Styling of the line chart",
            options=["lines", "markers", "lines+markers"],
            help="The styling of the scatter plot data",
        )
    scatter_options_form.form_submit_button("Submit and Update Plot")
    return versus, to_plot, mode, line_chart_height


def get_histplot_params(data_frame: pd.DataFrame) -> Tuple[Sequence[str], str, str, int, int]:
    """
    Form to query the user for histogram plot options with minimal reloading.

    Args:
        data_frame (pd.DataFrame): The user loaded TFS data frame.

    Returns:
        A Tuple with the following user defined properties: columns to plot, styling mode for the
        distribution upper plot, normalization routine for the histogram bins, number of bins and figure
        height.
    """
    histplot_options_form = st.form("Histogram Plot Options")
    histplot_options_form.header("Customize You Histogram Plot")
    columns, marginal_mode, normalization_mode, height, n_bins = histplot_options_form.beta_columns(
        spec=[4, 3, 3, 3, 2]
    )
    with columns:
        to_plot: Sequence[str] = st.multiselect(
            "Columns to Plot",
            options=data_frame.columns.to_numpy(),
            help="Select the columns to plot in this chart",
            key="columns_for_histogram",
        )
    with marginal_mode:
        mode: str = st.selectbox(
            "Styling of distribution plot",
            options=["box", "violin", "rug"],
            help="The type of distribution representation used for the upper axis",
        )
    with normalization_mode:
        histnorm: str = st.selectbox(
            "Normalization Routine",
            options=["None", "percent", "probability", "density", "probability density"],
            help="Bin normalization method. If None is selected, then the simple value counts are used",
        )
    with height:
        histogram_plot_height: int = st.select_slider(
            "Histogram Figure Height", options=list(range(200, 1050, 50)), value=600
        )
    with n_bins:
        nbins: Union[int, float] = st.number_input(  # careful streamlit might infer float from int inputs
            "Number of Bins",
            value=100,
            step=25,
            min_value=5,
            max_value=1000,
            help="Number of bins in the histogram",
        )
    histplot_options_form.form_submit_button("Submit and Update Plot")
    return to_plot, mode, histnorm, int(nbins), histogram_plot_height


def get_density_plot_params(data_frame: pd.DataFrame) -> Tuple[str, str, str, str, bool, int]:
    """
    Form to query the user for density plot options with minimal reloading.

    Args:
        data_frame (pd.DataFrame): The user loaded TFS data frame.

    Returns:
        A Tuple with the following user defined properties: X-axis column, Y-axis column, coutour type,
        color map to use, whether to reverse the colormap and figure height.
    """
    density_plot_options_form = st.form("Density Plot Options")
    density_plot_options_form.header("Customize Your Density Plot")
    xaxis, yaxis, contours, cmap, height, cmap_reverse = density_plot_options_form.beta_columns(
        spec=[3, 3, 3, 3, 3, 2]
    )
    with xaxis:
        xaxis_var: str = st.selectbox(
            "Property on the Horizontal Axis",
            options=data_frame.columns.to_numpy(),
            help="Select the column that will be on the horizontal axis",
        )
    with yaxis:
        yaxis_var: str = st.selectbox(
            "Property on the Vertical Axis",
            options=data_frame.columns.to_numpy(),
            help="Select the column that will be on the vertical axis",
        )
    with contours:
        coloring: str = st.selectbox(
            "Contour Types",
            options=["fill", "heatmap", "lines", "none"],
            help="Whether to fill the contours by extrapolating data",
        )
    with cmap:
        colorscale: str = st.selectbox(
            "Color Map",
            options=["Default"] + [cmap.capitalize() for cmap in px.colors.named_colorscales()],
            help="Which sequencial colormap to use for this plot",
        )
    with height:
        density_plot_height: int = st.select_slider(
            "Histogram Figure Height", options=list(range(200, 1050, 50)), value=600
        )
    with cmap_reverse:
        reverse_cmap: str = st.selectbox(
            "Colormap Scale",
            options=["Classic", "Reversed"],
            help="Whether to reverse the colormap for the plot",
        )
    density_plot_options_form.form_submit_button("Submit and Update Plot")
    return xaxis_var, yaxis_var, coloring, colorscale, reverse_cmap, density_plot_height
