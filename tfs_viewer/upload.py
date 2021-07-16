from io import StringIO
from tempfile import mkstemp


def handle_file_upload(uploaded) -> tuple:
    """
    Handles a file uploaded with streamlit's file_uploader and writes the contents to a temporary file.
    That temporary file will then be read with tfs-pandas and destroyed. This implementation is convoluted
    but as of now tfs-pandas does not handle buffer objects as returned by streamlit.

    Args:
        uploaded: the uploaded file object given back by streamlit's file_uploader.

    Returns:
        The file object and absolute path of the temporary file where the data was written.
    """
    string_data = StringIO(uploaded.getvalue().decode("utf-8")).read()
    fd, path = mkstemp(suffix=".tfs")
    with open(path, "w") as f:
        f.write(string_data)
    return fd, path
