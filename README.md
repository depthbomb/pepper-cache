# pepper-cache

![PyPI](https://img.shields.io/pypi/v/pepper-cache?color=0073b7&label=version&logo=python&logoColor=white&style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dd/pepper-cache?color=0073b7&logo=python&logoColor=white&style=flat-square)

A simple, persistent key/value cache with no dependencies.

## Installation

```shell
$ pip install pepper-cache
```

## API

- `create_cache` - Creates a Cache instance.
  - `name: str` - The name of the cache instance
  - `path: str` - The directory in which to store cache files relative to `<HOME>/.cache`
  - `serializer: "pickle"|"json" = "pickle"` - The serializer to use when writing values to the disk, defaults to "pickle"
```python
my_cache = create_cache("my cache", "my_app/my_cache", serializer="json")
```

---

- `get_cache` - Retrieves a Cache instance.
  - `name: str` - The name of the cache instance to retrieve
```python
my_cache = get_cache("my cache")
my_cache2 = get_cache("my cache 2")  # raises a KeyError
```

---

- `Cache.set` - Sets an item in the cache. Existing items will be overwritten.
  - `key: str` - The name of the cached value
  - `value: Any` - The value to store
  - `ttl: int = 0` - The time in milliseconds that the value should remain in the cache or 0  for indefinitely, defaults to `0`
```python
cache.set("my key", my_value)  # stored indefinitely
cache.set("my key", my_value, ttl=1000)  # stored for one second
```

---

- `Cache.get` - Retrieves a value from the cache if it exists and has not expired.
  - `key: str` - The key of the cache item to retrieve
  - `default: Any` - The default value to return if the value is not stored
```python
my_value = cache.get("my key 2")  # returns None if the value is not stored or has expired. Consider checking if the item exists below
my_value2 = cache.get("my key 2", default="now has a value")
```

---

- `Cache.has` - Returns `True` if an item exists in the cache by its key.
  - `key: str` - The key of the cache item to check the existence of
```python
if not cache.has("my key 2"):
    cache.set("my key 2", "has a value!")
```

---

- `Cache.delete` - Deletes an item from the cache if it exists.
  - `key: str` - The key of the cache item to delete from the cache
```python
cache.delete("my key 2"):
cache.get("my key 2")  # None
```

---

"pepper" comes from the code name of a project of mine and instead of writing packages like this specifically for the project, I decided to instead make them full on Python packages that anyone can use.
