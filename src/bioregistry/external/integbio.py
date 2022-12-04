# -*- coding: utf-8 -*-

"""Download the Integbio registry."""

import json

import pandas as pd

from bioregistry.constants import EXTERNAL
from bioregistry.utils import removeprefix

URL = "https://integbio.jp/dbcatalog/files/zip/en_integbio_dbcatalog_cc0_20221202_utf8.csv.zip"

DIRECTORY = EXTERNAL / "integbio"
DIRECTORY.mkdir(exist_ok=True, parents=True)
RAW_PATH = DIRECTORY / "raw.txt"
PROCESSED_PATH = DIRECTORY / "processed.json"


def get_integbio(force_download: bool = False):
    """Get the Integbio registry."""
    if PROCESSED_PATH.exists() and not force_download:
        with PROCESSED_PATH.open() as file:
            return json.load(file)

    data = {row["Database ID"]: _process_row(row) for _, row in pd.read_csv(URL).iterrows()}

    PROCESSED_PATH.write_text(json.dumps(data, indent=2, sort_keys=True))

    return data


def _process_row(row):
    fairsharing = row.get("Link to FAIRsharing")
    if pd.notna(fairsharing) and fairsharing:
        fairsharing = removeprefix(fairsharing, "https://fairsharing.org/")
    rv = {
        "prefix": row["Database ID"],
        "name": row["Database name"],
        "altname": row.get("Alternative name"),
        "homepage": row["URL"],
        "description": row.get("Database description"),
        "fairsharing": fairsharing,
    }
    return {k: v for k, v in rv.items() if pd.notna(v)}


if __name__ == "__main__":
    print(len(get_integbio(force_download=True)))  # noqa:T201
