#!/usr/bin/env python
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path.cwd()/".env")  # ok if file missing
from vermelldata.etl.ingest import main
if __name__ == "__main__":
    main()
