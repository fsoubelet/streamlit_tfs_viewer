from typing import Sequence, Tuple

import pandas as pd
import streamlit as st

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
    st.write(
        "-----\n"
        "Please note that displaying big dataframes is a strain on `Streamlit`'s frontend and will "
        "slow down page refreshes when applying operations. If you loaded a heavy dataframe, consider "
        "un-ticking the `Show File DataFrame` box in the sidebar."
    )
