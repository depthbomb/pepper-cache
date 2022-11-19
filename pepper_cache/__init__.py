from pathlib import Path
from typing import Literal, Optional

from .cache import Cache

_CACHES: dict[str, Cache] = {}


def create_cache(name: str, *, path: Optional[str | Path] = None, serializer: Literal["pickle", "json"] = "pickle") -> Cache:
    """
    Creates a Cache instance.

    :param name: The name of the cache instance, also used for the directory relative to $HOME/.cache if no path is supplied
    :param path: The directory in which to store cache files relative to $HOME/.cache
    :param serializer: The serializer to use when writing values to the disk, defaults to "pickle"
    """
    if name not in _CACHES:
        cache_path = Cache.clean_filename(name) if not path else path
        cache_instance = Cache(cache_path, serializer=serializer)
        _CACHES[name] = cache_instance
        return cache_instance

    raise Exception(f"Cache instance \"{name}\" has already been created")


def get_cache(name: str, *, create: bool = False) -> Optional[Cache]:
    """
    Retrieves a Cache instance if it exists.

    :param name: The name of the cache instance to retrieve
    :param create: Whether to create the cache if it does not exist
    """
    return _CACHES[name] if name in _CACHES else create_cache(name) if create else None
