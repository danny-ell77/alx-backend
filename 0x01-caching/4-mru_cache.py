from base_caching import BaseCaching


class MRUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.usage_order = []

    def get(self, key):
        if key is None:
            return None
        value = self.cache_data.get(key)
        if value is not None:
            self.update_usage_order(key)
        return value

    def put(self, key, item):
        if key is None or item is None:
            return
        if len(self.cache_data) == self.MAX_ITEMS and key not in self.cache_data:
            self.evict_least_recently_used()
        self.cache_data[key] = item
        self.update_usage_order(key)

    def evict_least_recently_used(self):
        mru_key = self.usage_order.pop()
        self.cache_data.pop(mru_key)
        print(f"DISCARD: {mru_key}")

    def update_usage_order(self, key):
        if key in self.usage_order:
            self.usage_order.remove(key)
        self.usage_order.append(key)
