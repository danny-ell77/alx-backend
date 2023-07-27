#!/usr/bin/python3
""" BasicCache module
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    def __init__(self):
        """initializes the Cache"""
        super().__init__()
        self.cache_keys = {}

    def get(self, key):
        """returns a value"""
        if key is None:
            return None
        value = self.cache_data.get(key)
        if value is not None:
            self.register_usage(key)
        return value

    def put(self, key, item):
        """sets a value"""
        if key is None or item is None:
            return
        if len(self.cache_data) == self.MAX_ITEMS and key not in self.cache_data:
            key_to_remove = self.find_min_usage()
            self.cache_keys.pop(key_to_remove)
            self.cache_data.pop(key_to_remove)
            print(f"DISCARD: {key_to_remove}")
        self.cache_data[key] = item
        self.register_usage(key)

    def find_min_usage(self):
        """finds min usage"""
        min_usage = min(self.cache_keys.values())
        min_keys = [key for key, usage in self.cache_keys.items() if usage == min_usage]
        return min_keys[0]

    def register_usage(self, key):
        """register's usage"""
        self.cache_keys[key] = self.cache_keys.get(key, 0) + 1
