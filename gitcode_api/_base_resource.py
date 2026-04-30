"""Resource base classe for the GitCode SDK."""

from functools import cached_property, lru_cache

_UTILITY_METHODS = {"methods", "method_signature"}
_DATA_MODEL_PATH = "gitcode_api._models."


class BaseResource:
    """Resource group base class"""

    def __del__(self) -> None:
        """Attempt to clear the lru cache."""
        self.method_signature.cache_clear()

    @cached_property
    def methods(self) -> tuple[str, ...]:
        """Public callable names on this resource group in stable SDK order.

        Ordering uses :func:`sorted` with a key derived from each name's
        underscore-separated segments (for example two-part names are ordered
        as if ``second_first``). This is not plain lexicographic order on the
        full method string. Excludes ``methods``, names starting with ``_``,
        and non-callables. The result is cached on first access.

        :returns: Tuple of method names in that order.
        """

        def _is_valid_func(name: str):
            return not (name.startswith("_") or name in _UTILITY_METHODS) and callable(getattr(self, name))

        def _sort_helper(method_name: str):
            name_parts = method_name.split("_")
            num_part = len(name_parts)
            if num_part == 2:
                return f"{name_parts[1]}_{name_parts[0]}"
            if num_part == 3:
                return f"{{{name_parts[0]}_"
            return "_" + method_name

        return tuple(
            sorted(
                (func for func in dir(self) if _is_valid_func(func)),
                key=_sort_helper,
            )
        )

    @lru_cache(maxsize=50)
    def method_signature(self, method_name: str) -> str:
        """Return signature for a method in this resource group, result is cached.

        For example ``client.pulls.method_signature("list_issues")`` would return:
        list_issues(*, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> List[Issue]

        :param method_name: Attribute name of a callable on this resource.
        :returns: Formatted signature.
        """
        import inspect

        return method_name + str(inspect.signature(getattr(self, method_name))).replace(_DATA_MODEL_PATH, "")
