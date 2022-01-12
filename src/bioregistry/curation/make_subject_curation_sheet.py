"""Make a subject curation sheet"""

import pandas as pd

import bioregistry
from bioregistry.constants import BIOREGISTRY_MODULE


def main():
    submodule = BIOREGISTRY_MODULE.submodule("curation")
    tsv_path = submodule.join(name="subjects.tsv")
    xlsx_path = submodule.join(name="subjects.xlsx")
    columns = ["prefix", "name", "homepage", "description", "subject"]
    rows = []
    for prefix, resource in sorted(bioregistry.read_registry().items()):
        if bioregistry.get_fairsharing_prefix(prefix) or bioregistry.is_deprecated(prefix):
            continue
        rows.append(
            (
                prefix,
                bioregistry.get_name(prefix),
                bioregistry.get_homepage(prefix) or "",
                bioregistry.get_description(prefix) or "",
                "",
            )
        )

    df = pd.DataFrame(rows, columns=columns)
    df.to_excel(xlsx_path, index=False)
    df.to_csv(tsv_path, sep="\t", index=False)
    print(submodule.base)


if __name__ == "__main__":
    main()
