#!/usr/bin/env python3
"""Hypermedia pagination sample.
"""

import csv
import math
from typing import List, Dict


def index_range(page, page_size):
    """Retrieves the index range from a given page and page size."""
    end_index = page * page_size
    start_index = end_index - page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    @property
    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieves a page of data."""

        assert type(page) is int and type(page_size) is int
        assert page > 0 and page_size > 0
        start, end = index_range(page, page_size)
        return self.dataset[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Retrieves information about a page."""
        total_pages = math.ceil(len(self.dataset) / page_size)
        return {
            "page_size": page_size,
            "page": page,
            "data": self.get_page(page, page_size),
            "next_page": page + 1 if page + 1 < total_pages else None,
            "prev_page": page - 1 if page - 1 > 0 else None,
            "total_pages": total_pages,
        }
