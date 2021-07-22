# TFS File Viewer

This is a prototype app using [streamlit][streamlit] to explore the contents of a **TFS** file.
It lets load and query your data, and visualize its headers and contents by creating and customizing scatter, histogram and density plots on the fly.
The app also integrates `pandas_profiling` to easily create a report on the data.

## Getting Started

[![Open in Streamlit][streamlit_badge]][demo_link]

To run the app locally, you will need to get [Poetry][poetry] and clone this repository.
Steps are simple:
```bash
git clone https://github.com/fsoubelet/tfs_viewer_prototype
cd tfs_viewer_prototype
poetry install
poetry run streamlit run tfs_viewer/app.py
```

## License

Copyright &copy; 2021 Felix Soubelet. [MIT License](LICENSE)


[streamlit]: https://streamlit.io/
[streamlit_badge]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[demo_link]: https://share.streamlit.io/fsoubelet/streamlit_tfs_viewer/tfs_viewer/app.py
[poetry]: https://python-poetry.org/
