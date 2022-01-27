from collections import defaultdict
from typing import Any

from tabulate import tabulate

from bioregistry import Resource
from bioregistry.constants import JSON_SCHEMA_PATH

group_order = [
    "metadata",
    "properties",
    "downloads",
    "registry",
    "miriam",
    "attribution",
    "ontology",
    "comments",
]
groups = {
    "metadata": [
        "prefix",
        "preferred_prefix",
        "synonyms",
        "name",
        "description",
        "homepage",
        "repository",
        "license",
        "version",
    ],
    "properties": ["deprecated", "no_own_terms", "proprietary"],
    "downloads": ["download_owl", "download_obo", "download_json"],
    "registry": ["pattern", "uri_format", "providers", "example", "example_extras"],
    "miriam": ["namespace_in_lui", "banana"],
    "attribution": ["contact", "contributor", "reviewer"],
    "ontology": ["mappings", "part_of", "provides", "has_canonical", "appears_in", "depends_on"],
    "comments": ["references", "comment"],
}
if set(groups) != set(group_order):
    raise ValueError("forgot an element in the group order")
rv = defaultdict(list)
for k, vs in groups.items():
    for v in vs:
        rv[v] = k


def main():
    field_groups = defaultdict(dict)
    for name, field in Resource.__fields__.items():
        if field.type_ is Any:
            continue
        field_groups[rv[name]][name] = field

    with JSON_SCHEMA_PATH.open("w") as file:
        for g in group_order:
            rows = []

            for name in groups[g]:
                field = field_groups[g][name]
                rows.append(
                    (
                        field.field_info.title or name.replace("_", " ").title(),
                        # field.type_.__name__ if hasattr(field.type_, "__name__") else field.type_,
                        field.field_info.description.replace("\n", " ").replace("  ", " "),
                    )
                )
                if name not in rv:
                    raise ValueError(f"{name} is uncategorized")
            print(f"## {g.title()}\n", file=file)
            print(
                tabulate(rows, headers=["Name", "Description"], tablefmt="github") + "\n",
                file=file,
            )


if __name__ == "__main__":
    main()
