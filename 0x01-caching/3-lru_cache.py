#!/usr/bin/python3
""" BasicCache module
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    def __init__(self):
        """initializes the class"""
        super().__init__()
        self.usage_order = []

    def get(self, key):
        """gets a value"""
        if key is None:
            return None
        value = self.cache_data.get(key)
        if value is not None:
            self.update_usage_order(key)
        return value

    def put(self, key, item):
        """sets a value"""
        if key is None or item is None:
            return
        if len(self.cache_data) == self.MAX_ITEMS and key not in self.cache_data:
            self.evict_least_recently_used()
        self.cache_data[key] = item
        self.update_usage_order(key)

    def evict_least_recently_used(self):
        """evicts least recently used key"""
        lru_key = self.usage_order[0]
        self.usage_order.pop(0)
        self.cache_data.pop(lru_key)
        print(f"DISCARD: {lru_key}")

    def update_usage_order(self, key):
        """updates the order of key usage"""
        if key in self.usage_order:
            self.usage_order.remove(key)
        self.usage_order.append(key)
