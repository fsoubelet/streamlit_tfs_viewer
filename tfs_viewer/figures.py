from itertools import zip_longest

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from tfs_viewer.forms import get_density_plot_params, get_histplot_params, get_scatter_plot_params

# ----- Plotting Functions ----- #


def plotly_line_chart(data_frame: pd.DataFrame) -> None:
    """
    Query user-given options for the plot and craft a plotly Scattergl plot from the data_frame's data.

    Args:
        data_frame (pd.DataFrame): The user loaded TFS data frame.
    """
    versus, plot_quantities, mode, height, errors_x, errors_y = get_scatter_plot_params(data_frame)

    if len(errors_x) not in [0, len(plot_quantities)] or len(errors_y) not in [0, len(plot_quantities)]:
        st.warning(
            "The amount of properties to plot and of properties to use for error bars do not match. "
            "Some properties will be plotted without error bars."
        )

    fig = go.Figure(layout=go.Layout(height=height))
    for variable, err_x, err_y in zip_longest(plot_quantities, errors_x, errors_y):
        fig.add_trace(
            go.Scattergl(
                x=data_frame[versus].to_numpy(),
                y=data_frame[variable].to_numpy(),
                mode=mode,
                name=variable,
                error_x=dict(type="data", array=data_frame[err_x].to_numpy(), visible=True)
                if err_x in data_frame.columns
                else None,
                error_y=dict(type="data", array=data_frame[err_y].to_numpy(), visible=True)
                if err_y in data_frame.columns
                else None,
            )
        )
    st.plotly_chart(fig, use_container_width=True)


def plotly_histogram(data_frame: pd.DataFrame) -> None:
    """
    Query user-given options for the plot and craft a plotly histogram plot from the data_frame's data.

    Args:
        data_frame (pd.DataFrame): The user loaded TFS data frame.
    """
    plot_quantities, marginal_mode, histnorm, n_bins, height = get_histplot_params(data_frame)
    if plot_quantities:  # errors if not
        norm_method = None if histnorm == "None" else histnorm
        fig = px.histogram(
            data_frame,
            x=plot_quantities,
            marginal=marginal_mode,
            histnorm=norm_method,
            barmode="overlay",
            height=height,
            nbins=n_bins,
        )
        st.plotly_chart(fig, use_container_width=True)


def plotly_density_contour(data_frame: pd.DataFrame) -> None:
    """
    Query user-given options for the plot and craft a plotly density contour plot from the data_frame's data.

    Args:
        data_frame (pd.DataFrame): The user loaded TFS data frame.
    """
    xcol, ycol, coloring, cmap, reverse_cmap, height = get_density_plot_params(data_frame)
    fig = px.density_contour(data_frame, x=xcol, y=ycol, height=height)
    fig.update_traces(
        contours_coloring=coloring,
        contours_showlabels=True,
        colorscale=None if cmap == "Default" else cmap,
        reversescale=True if reverse_cmap == "Reversed" else False,
    )
    st.plotly_chart(fig, use_container_width=True)
