import logging
import re
from typing import List, Optional

import sqlalchemy as sa

logger = logging.getLogger(__name__)


def get_table_names(
        engine: sa.engine,
        items: Optional[List[str]] = None,
        like: Optional[str] = None,
        regex: Optional[str] = None) -> List:
    """
    Generate a list of table names, optionally limiting only to items that end with the 
    ``filter`` string.

    Notes
    -----
    The ``items``, ``like``, and ``regex`` parameters are enforced to be mutually
    exclusive.
    """
    # Count how many of these objects are not None
    def count_not_none(*args) -> int:
        return sum(x is not None for x in args)
    
    kw_none = count_not_none(items, like, regex)
    if kw_none > 1:
        raise TypeError("Arguments `items`, `like`, and `regex` are mutually exclusive")
    
    # Inspect the database to get all the tables in the current schema
    insp = sa.inspect(engine)
    all_tables = insp.get_table_names()
    
    if items is not None:
        logger.debug("Looking for db tables: %s", items)
        exact_matches = []
        for item in items:
            reduced = filter(lambda x: x == item, all_tables)
            exact_matches.extend(list(reduced))
        return exact_matches
    elif like:
        logger.debug("Looking for tables containing: %s", like)
        def f(x):
            return like in x
        
        all_tables = list(filter(f, all_tables))
        return all_tables
    elif regex:
        logger.debug("Looking for tables matching: %s", regex)
        def f(x):
            return matcher.search(x) is not None
        
        matcher = re.compile(regex)
        all_tables = list(filter(f, all_tables))
        return all_tables
    else:
        raise TypeError("Must supply either `items`, `like`, or `regex`")
