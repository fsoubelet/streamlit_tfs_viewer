from typing import Sequence, Tuple

import pandas as pd
import pandas_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report

# ----- Display Components ----- #


def display_file_headers(headers_dict: dict) -> None:
    """Simply display headers dict."""
    st.header("File Headers", anchor="headers")
    st.write(headers_dict)


def display_file_dataframe(data_frame: pd.DataFrame, height: int, colormap: str) -> None:
    """Simply display dataframe, as a Styler object if a colormap is given."""
    st.header("File Data", anchor="dataframe")
    styler = (
        data_frame.style.background_gradient(cmap=colormap).highlight_null(null_color="red")
        if colormap != "None"
        else data_frame
    )
    st.dataframe(styler, height=height)


def display_dataframe_report(data_frame: pd.DataFrame) -> None:
    """
    Generate and display in an expandable block the profile report of the data frame from pandas_profiling.
    """
    with st.beta_expander("EXPLORATIVE REPORT (Collapsible)"):
        st_profile_report(data_frame.profile_report(explorative=True))
