.PHONY: dev ingest inspect
dev:
	python3 -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt && pip install -e .
ingest:
	. .venv/bin/activate && python scripts/ingest_once.py
inspect:
	python - <<'PY'
import os, duckdb
db=os.getenv("DUCKDB_PATH","data/vermelldata.duckdb")
con=duckdb.connect(db)
print(con.execute("SELECT COUNT(*) AS n FROM readings").df())
print(con.execute("SELECT sensor_id, ts, pm25, pm10 FROM readings ORDER BY ts DESC LIMIT 10").df())
PY
