from .cache import Cache
from typing import Literal, Optional

_CACHES: dict[str, Cache] = {}


def create_cache(name: str, path: str, *, serializer: Literal["pickle", "json"] = "pickle") -> Cache:
    """
    Creates a Cache instance.

    :param name: The name of the cache instance
    :param path: The directory in which to store cache files relative to <HOME>/.cache
    :param serializer: The serializer to use when writing values to the disk, defaults to using pickle
    """
    if name not in _CACHES:
        cache_instance = Cache(path, serializer=serializer)
        _CACHES[name] = cache_instance
        return cache_instance

    raise Exception(f"Cache instance \"{name}\" has already been created")


def get_cache(name: str) -> Optional[Cache]:
    """
    Retrieves a Cache instance if it exists.

    :param name: The name of the cache instance to retrieve
    """
    return _CACHES[name] if name in _CACHES else None
