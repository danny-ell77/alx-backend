#!/usr/bin/python3
""" BasicCache module
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    def __init__(self):
        """intializes cache_keys"""
        super().__init__()
        self.cache_keys = []

    def get(self, key):
        """returns a values"""
        if key is None:
            return
        if value := self.cache_data.get(key):
            return value

    def put(self, key, item):
        """sets a value"""
        if key is None or item is None:
            return
        if len(self.cache_data) == self.MAX_ITEMS and key not in self.cache_keys:
            key_to_remove = self.cache_keys.pop(0)
            self.cache_data.pop(key_to_remove)
            print(f"DISCARD: {key_to_remove}")
        self.cache_data[key] = item
        if key not in self.cache_keys:
            self.cache_keys.append(key)
