from vermelldata.db.conn import get_conn
from vermelldata.io.purpleair_client import fetch_recent_readings

CREATE_SENSORS = """
CREATE TABLE IF NOT EXISTS sensors(
  sensor_id TEXT PRIMARY KEY,
  source TEXT,
  lat DOUBLE, lon DOUBLE,
  elevation DOUBLE, location_desc TEXT,
  first_seen TIMESTAMP, last_seen TIMESTAMP
);
"""

CREATE_READINGS = """
CREATE TABLE IF NOT EXISTS readings(
  sensor_id TEXT,
  ts TIMESTAMP,
  pm25 DOUBLE, pm10 DOUBLE, temp DOUBLE, humidity DOUBLE,
  PRIMARY KEY (sensor_id, ts)
);
"""

UPSERT_SENSOR = """
INSERT OR REPLACE INTO sensors(sensor_id, source, lat, lon, elevation, location_desc, first_seen, last_seen)
VALUES (?, ?, ?, ?, NULL, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
"""

UPSERT_READING = """
INSERT OR REPLACE INTO readings(sensor_id, ts, pm25, pm10, temp, humidity)
VALUES (?, ?, ?, ?, ?, ?);
"""

def main():
    rows = fetch_recent_readings()
    con = get_conn()
    con.execute(CREATE_SENSORS)
    con.execute(CREATE_READINGS)
    for r in rows:
        con.execute(UPSERT_SENSOR, [r["sensor_id"], r["source"], r["lat"], r["lon"]])
        con.execute(UPSERT_READING, [r["sensor_id"], r["ts"], r.get("pm25"), r.get("pm10"), r.get("temp"), r.get("humidity")])
    print(f"Inserted/updated {len(rows)} readings.")
