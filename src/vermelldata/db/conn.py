import os, duckdb
DB_PATH = os.getenv("DUCKDB_PATH", "data/vermelldata.duckdb")

def get_conn():
    con = duckdb.connect(DB_PATH)
    try:
        con.execute("INSTALL spatial; LOAD spatial;")  # optional
    except Exception:
        pass
    return con
