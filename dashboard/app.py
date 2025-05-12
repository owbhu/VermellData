from pathlib import Path

import duckdb
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

DB_PATH = "data/vermelldata.duckdb"
if not Path(DB_PATH).exists():
    raise SystemExit("Run the ingestion job first so the DB exists!")

con = duckdb.connect(DB_PATH, read_only=True)

app = Dash(__name__)
app.title = "PurpleAir Dashboard"

SENSORS = [
    {"label": str(r[0]), "value": int(r[0])}
    for r in con.execute("select distinct sensor_id from readings").fetchall()
]

app.layout = html.Div(
    style={"font-family": "sans-serif", "margin": "2rem"},
    children=[
        html.H2("PurpleAir PM2.5 readings"),
        dcc.Dropdown(id="sensor-dropdown", options=SENSORS, value=SENSORS[0]["value"]),
        dcc.Graph(id="timeseries"),
        html.Small("Data powered by PurpleAir REST API • DuckDB backend"),
    ],
)


@app.callback(Output("timeseries", "figure"), Input("sensor-dropdown", "value"))
def _update(sensor_id: int):
    q = f"""
        select ts_utc as time, pm25
        from readings
        where sensor_id = {sensor_id}
        order by time
    """
    df: pd.DataFrame = con.execute(q).df()
    fig = px.line(df, x="time", y="pm25", labels={"time": "UTC", "pm25": "PM₂.₅ (µg/m³)"})
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

