"""
Cache files, and evict if maximum storage capacity would be trespassed.
"""
import collections

CACHE_CAPACITY = 200


# The caching class is adapted from this website: https://www.kunxi.org/blog/2014/05/lru-cache-in-python/
class LRUCache:
    """
    LRU cache class, handles all access methods.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def get(self, key):
        """
        Return element from cache, set it as most recently used.
        Args:
            key: The key of the element to be retrieved.

        Returns:
            Element if element in cache, -1 if not in cache.
        """
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return -1

    def set(self, key, value):
        """
        Set value of record in cache.
        Args:
            key:
            value:

        Returns:

        """
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value


# Cache object.
cache = LRUCache(CACHE_CAPACITY)


# Accessor methods.
def set_file(metadata_object):
    # TODO delete files until desired file size reached, including new object.
    cache.set(metadata_object['id'], metadata_object)


def get_file(id):
    return cache.get(id)
