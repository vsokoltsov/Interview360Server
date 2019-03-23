import abc


class BaseQuery(abc.ABC):
    """Base abstract class for the query objects."""

    params = None
