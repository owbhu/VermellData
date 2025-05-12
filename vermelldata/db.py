import duckdb
from pathlib import Path

from .settings import settings

# ensure data/ exists
Path("data").mkdir(exist_ok=True)

con = duckdb.connect(settings.db_url.removeprefix("duckdb://"))


def init_schema() -> None:
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS readings (
            sensor_id   INTEGER,
            ts_utc      TIMESTAMP,
            pm25        DOUBLE,
            humidity    DOUBLE,
            temperature DOUBLE,
            pressure    DOUBLE,
            PRIMARY KEY (sensor_id, ts_utc)
        )
        """
    )

