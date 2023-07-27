from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.cache_keys = []

    def get(self, key):
        if key is None:
            return
        if value := self.cache_data.get(key):
            return value

    def put(self, key, item):
        if key is None or item is None:
            return
        if len(self.cache_data) == self.MAX_ITEMS and key not in self.cache_keys:
            key_to_remove = self.cache_keys.pop()
            self.cache_data.pop(key_to_remove)
            print(f"DISCARD: {key_to_remove}")
        self.cache_data[key] = item
        self.cache_keys.append(key)
