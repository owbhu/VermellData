"""
CLI-friendly ingestion job:

`python -m vermelldata.pull`

• reads sensor IDs from sensor_group.txt
• calls PurpleAir API
• inserts new rows into DuckDB
"""

import csv
import datetime as dt
from pathlib import Path

import typer

from .client import get_history
from .db import con, init_schema

app = typer.Typer(add_completion=False)
FILE = Path(__file__).with_name("sensor_group.txt")


def _load_ids() -> list[int]:
    return [int(row[0]) for row in csv.reader(FILE.read_text().splitlines()) if row]


def _insert(sensor_id: int, rows: list[list]):
    # API payload: header row first, then data rows
    for row in rows:
        ts_epoch = row[0]
        ts = dt.datetime.fromtimestamp(ts_epoch, dt.timezone.utc)
        pm25, hum, temp, pres = row[1:5]
        con.execute(
            "INSERT OR IGNORE INTO readings VALUES (?, ?, ?, ?, ?, ?)",
            (sensor_id, ts, pm25, hum, temp, pres),
        )


@app.command()
def run(minutes: int = 5):
    """Pull newest data for each sensor group."""
    init_schema()
    for sid in _load_ids():
        res = get_history(sid, minutes=minutes)
        _insert(sid, res["data"])
        typer.echo(f"ingested sensor {sid}  ({len(res['data'])} rows)")
    con.close


if __name__ == "__main__":
    app()

