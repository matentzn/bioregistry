# -*- coding: utf-8 -*-

"""API for collections."""

from typing import Mapping, Optional

from .schema import Collection, Context
from .schema_utils import read_collections, read_contexts

__all__ = [
    "get_collection",
    "get_context",
    "get_collection_part_of",
]


def get_collection(identifier: str) -> Optional[Collection]:
    """Get the collection entry for the given identifier."""
    return read_collections().get(identifier)


def get_collection_part_of() -> Mapping[str, Collection]:
    return {
        collection.part_of_key: collection
        for identifier, collection in read_collections().items()
        if collection.part_of_key
    }


def get_context(identifier: str) -> Optional[Context]:
    """Get the context for the given identifier."""
    return read_contexts().get(identifier)
