import os
from typing import Tuple

import pandas as pd
import streamlit as st
import tfs

from tfs_viewer.displays import display_dataframe_report, display_file_dataframe, display_file_headers
from tfs_viewer.figures import plotly_density_contour, plotly_histogram, plotly_line_chart
from tfs_viewer.upload import handle_file_upload

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
    return data_frame.query(dataframe_query)


# ----- Page Config ----- #

st.set_page_config(
    page_title="TFS File Explorer",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title(f"TFS File Explorer [![Github]({GITHUB_BADGE})]({GITHUB_URL})")

# ----- Sidebar Data Manipulation Options ----- #

data_form = st.sidebar.form("Data Options")
data_form.header("Data Manipulation")
chosen_index: str = data_form.text_input("Select Load Index", help="Column to use as index.")
dataframe_query: str = data_form.text_input(
    "Apply Query to Data",
    help="Any query to apply to the dataframe, to be given to `DataFrame.query`. See the [documentation]"
    "(https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) "
    "for usage details.",
)
data_form.form_submit_button("Apply Options")

# ----- Sidebar Data Display Options ----- #

display_form = st.sidebar.form("Display Options")
display_form.header("Display Options")
show_headers: bool = display_form.checkbox(
    "Show File Headers", value=False, help="Whether to display the `header` of the loaded file."
)
show_dataframe: bool = display_form.checkbox(
    "Show File DataFrame", value=True, help="Whether to display the `DataFrame` of the loaded file."
)
dataframe_height: int = display_form.select_slider(
    "DataFrame Display Height", options=list(range(100, 850, 50)), value=400
)
color_map: str = display_form.selectbox(
    "Display Color Map",
    options=["None", "viridis", "plasma", "inferno", "magma", "cividis"],
    help="Which colormap to apply when styling the `DataFrame`.",
)
display_form.form_submit_button("Apply Options")

# ----- Sidebar Visualization Options ----- #

plots_form = st.sidebar.form("Plotting Choices")
plots_form.header("Visualizations")
make_scatterplot: bool = plots_form.checkbox(
    "Craft a ScatterPlot", help="Check this box to create a `Plotly` scatter or line plot."
)
make_histogram: bool = plots_form.checkbox(
    "Craft a Histogram", help="Check this box to create a `Plotly` histogram plot."
)
make_density_plot: bool = plots_form.checkbox(
    "Craft a Density Plot", help="Check this box to create a `Plotly` density plot."
)
plots_form.form_submit_button("Apply")

# ----- Sidebar Data Exploration Options ----- #

generate_report: bool = st.sidebar.button(
    "Generate An Exploratory Report",
    help="Generate and display a `pandas_profiling` report. Beware: This can be time-intensive on big files!",
)

# ----- Section: User Input ----- #

st.header("Let's Get Your File")
uploaded_file = st.file_uploader("File to load", help="Select your TFS File.")

if uploaded_file is not None:
    # At each new upload streamlit increments uploaded_file.id so we can check there to handle session state.
    # If we return to a previously uploaded file, all this block runs again - but `load_tfs_file` is cached.
    # However at each change in the page that is not uploadnig a new file, we use session state and don't
    # run the temporary writing and TFS loading -> very useful for big files!
    if "id" not in st.session_state or st.session_state.id != uploaded_file.id:
        st.session_state.id = uploaded_file.id
        file, file_path = handle_file_upload(uploaded_file)
        st.session_state.headers, st.session_state.dataframe = load_tfs_file(file_path, chosen_index, file)

    # Sets desired index if it is changed in the sidebar for an already uploaded file
    if chosen_index != "" and chosen_index in st.session_state.dataframe.columns:
        st.session_state.dataframe = st.session_state.dataframe.set_index(chosen_index)

    dataframe = (
        apply_dataframe_query(st.session_state.dataframe, dataframe_query)
        if dataframe_query != ""
        else st.session_state.dataframe
    )

    # ----- Section: File Data Display ----- #
    if show_headers:
        with st.beta_expander("Headers Section - Click to Fold", expanded=True):
            display_file_headers(st.session_state.headers)
    if show_dataframe:
        with st.beta_expander("Data Section - Click to Fold", expanded=True):
            display_file_dataframe(dataframe, dataframe_height, color_map)
    if generate_report:
        display_dataframe_report(dataframe)

    # ----- Section: Visualizations ----- #
    if make_scatterplot:
        plotly_line_chart(dataframe)
    if make_histogram:
        plotly_histogram(dataframe)
    if make_density_plot:
        plotly_density_contour(dataframe)

# ----- Footer ----- #

st.markdown("-----")

with st.beta_expander("What is This and Who is it For?"):
    st.write(
        "This is a prototype of a simple `streamlit` app to allow my team and I to easily delve into the "
        "contents of a [TFS file](https://mad.web.cern.ch/mad/madx.old/Introduction/tfs.html), which we use "
        "in our work. It uses our own `tfs-pandas` package to handle the format and integrates the "
        "`pandas_profiling` library to get quick insights into the data. Options are also provided to "
        "quickly craft simple plots from the data using `streamlit`'s API."
    )
    st.write("**DISCLAIMER**: Functionality may change quickly without notice.")
