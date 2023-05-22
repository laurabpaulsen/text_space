"""
Using Dash to create a web app for the project
"""
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parents[2] / "TextSpace"))

from dash_application import get_dash_app


if __name__ == '__main__':
    path = Path(__file__)
    data_path = path.parents[2] / 'data' / 'plotly_data.csv'
    print("Running Dash app...")
    app = get_dash_app(data_path=data_path)
    print("Go to the link provided in the terminal when the app is done opening.")
    print("Press CTRL+C to stop the app.")
    app.run_server(debug=False)