#!/usr/bin/env python3
"""Pagination helper function.
"""


def index_range(page, page_size):
    """Retrieves the index range from a given page and page size."""
    end_index = page * page_size
    start_index = end_index - page_size
    return start_index, end_index
