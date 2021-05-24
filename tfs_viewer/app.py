import os
from typing import Tuple

import pandas as pd
import streamlit as st
import tfs

from tfs_viewer.components import display_dataframe_report, display_file_dataframe, display_file_headers
from tfs_viewer.figures import plotly_distplot, plotly_line_chart
from tfs_viewer.utils import handle_file_upload

GITHUB_BADGE = "https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"
GITHUB_URL = "https://github.com/fsoubelet/tfs_viewer_prototype"

# ----- Cached Functions ----- #


@st.cache()
def load_tfs_file(tfs_file_path: str, index: str, file_obj: int) -> Tuple[dict, pd.DataFrame]:
    """
    Loads the chosen TFS file, returns the headers and the dataframe itself. The results are cached for
    efficiency on heavy files. The file will be a temporary file created from uploaded data, and the file
    object is used so we can properly close it.

    Args:
        tfs_file_path (str): absolute path to the file to load.
        index (str): which column to use as inndex during loading.
        file_obj (int): OS-level handle to the opened file as returned by the tempfile.mkstemp function.

    Returns:
        A tuple of the TfsDataFrame's headers (dictionary) and the dataframe itself as a pandas.DataFrame.
    """
    try:
        tfs_df = tfs.read(tfs_file_path, index)
        os.close(file_obj)  # remember to close (and delete) the tempfile
        return tfs_df.headers, pd.DataFrame(tfs_df)
    except Exception as error:
        st.write(error)


@st.cache()
def apply_dataframe_query(data_frame: pd.DataFrame, query: str) -> pd.DataFrame:
    return dataframe.query(dataframe_query)


# ----- Page Config ----- #

st.set_page_config(
    page_title="TFS File Explorer",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title(f"TFS File Explorer [![Github]({GITHUB_BADGE})]({GITHUB_URL})")

# ----- Sidebar Widgets ----- #

st.sidebar.header("Data Manipulation")
chosen_index: str = st.sidebar.text_input("Select Load Index", help="Column to use as index.")
dataframe_query: str = st.sidebar.text_input(
    "Apply Query to Data",
    help="Any query to apply to the dataframe, to be given to `DataFrame.query`. See the [documentation]"
    "(https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) "
    "for usage details.",
)
st.sidebar.header("Display Options")
show_headers: bool = st.sidebar.checkbox(
    "Show File Headers", value=False, help="Whether to display the `header` of the loaded file."
)
show_dataframe: bool = st.sidebar.checkbox(
    "Show File DataFrame", value=True, help="Whether to display the `DataFrame` of the loaded file."
)
if show_dataframe:
    dataframe_height: int = st.sidebar.select_slider(
        "DataFrame Display Height", options=list(range(100, 850, 50)), value=400
    )
    color_map: str = st.sidebar.selectbox(
        "Display Color Map",
        options=["None", "viridis", "plasma", "inferno", "magma", "cividis"],
        help="Which colormap to apply when styling the `DataFrame`.",
    )
generate_report: bool = st.sidebar.button(
    "Generate An Exploratory Report",
    help="Generate and display a `pandas_profiling` report. Beware: This can be time-intensive on big files!",
)

# ----- Sidebar Visualization Options ----- #

st.sidebar.header("Visualizations")
make_scatterplot: bool = st.sidebar.checkbox(
    "Craft a ScatterPlot",
    help="Check this box to create a `Plotly` histogram plot.",
)
if make_scatterplot:
    line_chart_height = st.sidebar.select_slider(
        "ScatterPlot Figure Height", options=list(range(200, 1050, 50)), value=600
    )

make_histogram: bool = st.sidebar.checkbox(
    "Craft a Histogram", help="Check this box to create a `Plotly` histogram plot."
)
if make_histogram:
    histogram_plot_height = st.sidebar.select_slider(
        "Histogram Figure Height", options=list(range(200, 1050, 50)), value=600
    )

# ----- Section: User Input ----- #

st.header("Let's Get Your File")
uploaded_file = st.file_uploader("File to load", help="Select your TFS File.")

if uploaded_file is not None:
    file, file_path = handle_file_upload(uploaded_file)
    headers, dataframe = load_tfs_file(file_path, chosen_index, file)
    dataframe = apply_dataframe_query(dataframe, dataframe_query) if dataframe_query != "" else dataframe

    # ----- Section: File Data Display ----- #
    if show_headers:
        display_file_headers(headers)
    if show_dataframe:
        display_file_dataframe(dataframe, dataframe_height, color_map)
    if generate_report:
        display_dataframe_report(dataframe)

    # ----- Section: Visualizations ----- #
    if make_scatterplot:
        plotly_line_chart(dataframe, line_chart_height)
    if make_histogram:
        plotly_distplot(dataframe, histogram_plot_height)

# ----- Footer ----- #

with st.beta_expander("What is This and Who is it For?"):
    st.write(
        "This is a prototype of a simple `streamlit` app to allow my team and I to easily delve into the "
        "contents of a [TFS file](https://mad.web.cern.ch/mad/madx.old/Introduction/tfs.html), which we use "
        "in our work. It uses our own `tfs-pandas` package to handle the format and integrates the "
        "`pandas_profiling` library to get quick insights into the data. Options are also provided to "
        "quickly craft simple plots from the data using `streamlit`'s API."
    )
    st.write("**DISCLAIMER**: Functionality may change quickly without notice.")
