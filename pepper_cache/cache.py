import re
from os import makedirs
from time import time_ns
from pathlib import Path
from hashlib import sha1
from logging import getLogger
from typing import Any, Literal, Optional

logger = getLogger("pepper-cache")


class Cache:
    _store: dict[str, tuple[str, Any, int]]
    _store_path: Path
    _serializer: str

    def __init__(self, cache_path: str, *, serializer: Literal["pickle", "json"] = "pickle"):
        self._store = {}
        self._store_path = Path.home().joinpath(".cache", cache_path)
        self._store_path.mkdir(parents=True) if not self._store_path.exists() else None
        self._serializer = serializer
        self.__load_objects_from_files()

    def set(self, key: str, value: Any, *, ttl: int = 0) -> None:
        """
        Sets an item in the cache. Existing items will be overwritten.

        :param key: The name of the cached value
        :param value: The value to store
        :param ttl: The time in milliseconds that the value should remain in the cache or 0  for indefinitely, defaults to 0
        """
        expires = (self._unix_time() + ttl) if ttl > 0 else 0
        store_object = (key, value, expires)
        self._store[key] = store_object
        self.__write_file_object(key, store_object)

    def get(self, key: str, *, default: Any = None) -> Optional[Any]:
        """
        Retrieves a value from the cache if it exists and has not expired.

        :param key: The key of the cache item to retrieve
        :param default: The default value to return if the value is not stored
        """
        if key in self._store:
            logger.debug("\"%s\" found in store" % key)
            (key, value, expires) = self._store[key]
            if self.__object_has_expired(expires):
                self.__delete_file_object(key)
                logger.debug("Deleted expired file object for \"%s\"" % key)
                return default

            return value

        logger.debug("\"%s\" not found in store" % key)

        return default

    def has(self, key: str) -> bool:
        """
        Returns True if an item exists in the cache by its key.

        :param key: The key of the cache item to check the existence of
        """
        return key in self._store

    def delete(self, key: str) -> None:
        """
        Deletes an item from the cache if it exists.

        :param key: The key of the cache item to delete from the cache
        """
        if key in self._store:
            del self._store[key]
            self.__delete_file_object(key)

    @staticmethod
    def _unix_time() -> int:
        return time_ns() // 1_000_000

    @staticmethod
    def _clean_filename(filename: str) -> str:
        # Based on https://github.com/django/django/blob/main/django/utils/text.py
        s = str(filename).strip().replace(" ", "_")
        s = re.sub(r"(?u)[^-\w.]", "", s)
        if s in {"", ".", ".."}:
            raise Exception("Could not derive file name from '%s'" % filename)

        return s

    def __get_file_object_path(self, key: str) -> Path:
        filename = sha1(key.encode("utf-8")).hexdigest()

        return Path(self._store_path, filename[0:2], filename[2:4], filename)

    def __load_object_from_file(self, path: Path) -> None:
        if path.exists():
            object_expired = False
            mode = "rb" if self._serializer == "pickle" else "r"
            with path.open(mode) as file:
                if self._serializer == "pickle":
                    from pickle import load
                else:
                    from json import load
                data = load(file)
                (key, _, expires) = data
                if self.__object_has_expired(expires):
                    object_expired = True
                else:
                    logger.debug("Loaded file object for \"%s\"" % key)
                    self._store[key] = data

            if object_expired:
                self.__delete_file_object(key)

    def __load_objects_from_files(self) -> None:
        objects = list(self._store_path.glob("**/*"))
        for obj in objects:
            if obj.is_file():
                logger.debug("Loading file object \"%s\"" % obj)
                self.__load_object_from_file(obj)

    def __write_file_object(self, key: str, value: tuple[str, Any, int]) -> None:
        filepath = self.__get_file_object_path(key)
        filedir = filepath.parent

        makedirs(filedir) if not filedir.exists() else None

        mode = "wb" if self._serializer == "pickle" else "w"
        with filepath.open(mode) as file:
            if self._serializer == "pickle":
                from pickle import dumps
            else:
                from json import dumps

            data = dumps(value)
            file.write(data)
            logger.debug("Wrote data to file object \"%s\"" % filepath)

    def __delete_file_object(self, key: str) -> None:
        filepath = self.__get_file_object_path(key)
        if filepath.exists():
            filepath.unlink()
            logger.debug("Deleted file object \"%s\"" % filepath)

    def __object_has_expired(self, expires: int) -> bool:
        return expires != 0 and self._unix_time() >= expires
