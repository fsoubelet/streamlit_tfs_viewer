from typing import Sequence, Tuple, Union

import pandas as pd
import plotly.express as px
import streamlit as st


def get_scatter_plot_params(
    data_frame: pd.DataFrame,
) -> Tuple[str, Sequence[str], str, int, Sequence[str], Sequence[str]]:
    """
    Form to query the user for scatter plots options with minimal reloading.

    Args:
        data_frame (pd.DataFrame): The user loaded TFS data frame.

    Returns:
        A Tuple with the following user defined properties: X-axis column, Y-axis column(s), styling mode for
        the chart, figure height, property(ies) for horizontal error bars and property(ies) for vertical
        error bars.
    """
    scatter_options_form = st.form("Scatter Plot Options")
    scatter_options_form.header("Customize Your Scatter Plot")
    versus, columns, err_x, err_y, height, mode = scatter_options_form.columns(spec=[2, 3, 3, 3, 2, 2])
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
        line_chart_height: int = st.select_slider(
            "ScatterPlot Figure Height", options=list(range(200, 1500, 50)), value=700
        )
    with err_x:
        horizontal_errors: Sequence[str] = st.multiselect(
            "Hozirontal Error Bars",
            options=[""] + data_frame.columns.tolist(),
            help="Property to use for horizontal error bars. The first property provided here will be "
            "used for errors of the first property provided there and so on. Be aware that a mismatch "
            "in the number of inputs to plot and to use as error bars means some properties will be "
            "plotted with no error bars.",
        )
    with err_y:
        vertical_errors: Sequence[str] = st.multiselect(
            "Vertical Error Bars",
            options=[""] + data_frame.columns.tolist(),
            help="Property to use for vertical error bars. The first property provided here will be "
            "used for errors of the first property provided there and so on. Be aware that a mismatch "
            "in the number of inputs to plot and to use as error bars means some properties will be "
            "plotted with no error bars.",
        )
    with mode:
        mode: str = st.selectbox(
            "Styling of the line chart",
            options=["lines", "markers", "lines+markers"],
            help="The styling of the scatter plot data",
        )
    scatter_options_form.form_submit_button("Submit and Update Plot")
    return versus, to_plot, mode, line_chart_height, horizontal_errors, vertical_errors


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
    histplot_options_form.header("Customize Your Histogram Plot")
    columns, marginal_mode, normalization_mode, height, n_bins = histplot_options_form.columns(
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
            "Histogram Figure Height", options=list(range(200, 1500, 50)), value=700
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
    xaxis, yaxis, contours, cmap, height, cmap_reverse = density_plot_options_form.columns(
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
            "Histogram Figure Height", options=list(range(200, 1500, 50)), value=700
        )
    with cmap_reverse:
        reverse_cmap: str = st.selectbox(
            "Colormap Scale",
            options=["Classic", "Reversed"],
            help="Whether to reverse the colormap for the plot",
        )
    density_plot_options_form.form_submit_button("Submit and Update Plot")
    return xaxis_var, yaxis_var, coloring, colorscale, reverse_cmap, density_plot_height
