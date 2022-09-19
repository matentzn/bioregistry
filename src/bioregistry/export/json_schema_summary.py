"""Create a human-readable version of data model."""

from collections import defaultdict
from textwrap import dedent
from typing import Any, DefaultDict, Dict

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
    "provenance",
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
    "downloads": ["download_owl", "download_obo", "download_json", "download_rdf"],
    "registry": [
        "pattern",
        "uri_format",
        "providers",
        "example",
        "example_extras",
        "example_decoys",
    ],
    "miriam": ["namespace_in_lui", "banana", "banana_peel"],
    "attribution": ["contact", "contributor", "reviewer", "contributor_extras", "twitter"],
    "ontology": ["mappings", "part_of", "provides", "has_canonical", "appears_in", "depends_on"],
    "provenance": ["references", "comment", "publications", "github_request_issue"],
}
if set(groups) != set(group_order):
    raise ValueError("forgot an element in the group order")
rv: Dict[str, str] = {}
for group_key, group_values in groups.items():
    for group_value in group_values:
        if group_value in rv:
            raise KeyError
        rv[group_value] = group_key


def main():
    """Generate the data model pages."""
    field_groups: DefaultDict[str, Dict[str, str]] = defaultdict(dict)
    for name, field in Resource.__fields__.items():
        if field.type_ is Any:
            continue
        field_groups[rv[name]][name] = field

    with JSON_SCHEMA_PATH.open("w") as file:
        print(  # noqa:T201
            dedent(
                """\
        ---
        layout: page
        title: Resource Data Model
        permalink: /schema/resource
        ---
        This document describes the data model for resources in the Bioregistry.
        There are a few alternate views in this description:

        1. The technical documentation at https://bioregistry.readthedocs.io/en/latest/api/bioregistry.Resource.html
        2. The corresponding JSON schema is under version control on GitHub at
           https://github.com/biopragmatics/bioregistry/blob/main/src/bioregistry/schema/schema.json
        3. The corresponding JSON schema is distributed via the Bioregistry site at
           https://bioregistry.io/schema.json
        """
            ),
            file=file,
        )
        for group in group_order:
            rows = []

            for name in groups[group]:
                field = field_groups[group][name]
                rows.append(
                    (
                        field.field_info.title or name.replace("_", " ").title(),
                        # field.type_.__name__ if hasattr(field.type_, "__name__") else field.type_,
                        field.field_info.description.replace("\n", " ").replace("  ", " "),
                    )
                )
                if name not in rv:
                    raise ValueError(f"{name} is uncategorized")
            print(f"## {group.title()}\n", file=file)  # noqa:T201
            print(  # noqa:T201
                tabulate(rows, headers=["Name", "Description"], tablefmt="github") + "\n",
                file=file,
            )


if __name__ == "__main__":
    main()
