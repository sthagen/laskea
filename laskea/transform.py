"""Transformer API for laskea.

Typical filter data comes in as JSON and maps column keys to filter tasks:

{
  "order": ["keep", "drop", "replace"],
  "keep": [
    ["startswith", "ABC-"],
    ["contains", "Z"],
    ["icontains", "m"],
    ["equals", "DEF-42"],
    ["endswith", "-123"]
  ],
  "drop": [
    ["matches", "[A-Z]+-\\d+"]
  ],
  "replace": [
    ["DEF-", "definition-"]
  ]
}

"""
import re
from laskea import FILTER_MAP_TYPE, FILTER_ORDER_TYPE, FILTER_PAYLOAD_TYPE, log

# operation keys
DROP = 'drop'
KEEP = 'keep'
ORDER = 'order'
REPLACE = 'replace'

# action keys
CONTAINS = 'contains'
ENDSWITH = 'endswith'
EQUALS = 'equals'
ICONTAINS = 'icontains'
IENDSWITH = 'iendswith'
IEQUALS = 'iequals'
ISTARTSWITH = 'istartswith'
MATCHES = 'matches'
STARTSWITH = 'startswith'

ACTION_KEYS = (
    CONTAINS,
    ENDSWITH,
    EQUALS,
    ICONTAINS,
    IENDSWITH,
    IEQUALS,
    ISTARTSWITH,
    MATCHES,
    STARTSWITH,
)


def op_contains(entry: str, that: str) -> bool:
    """Case sensitive contains."""
    return bool(that in entry)


def op_endswith(entry: str, that: str) -> bool:
    """Case sensitive ends with."""
    return bool(entry.endswith(that))


def op_equals(entry: str, that: str) -> bool:
    """Case sensitive equals."""
    return bool(that == entry)


def op_icontains(entry: str, that: str) -> bool:
    """Case insensitive contains."""
    return bool(that.lower() in entry.lower())


def op_iendswith(entry: str, that: str) -> bool:
    """Case insensitive ends with."""
    return bool(entry.lower().endswith(that.lower()))


def op_iequals(entry: str, that: str) -> bool:
    """Case insensitive equals."""
    return bool(that.lower() == entry.lower())


def op_istartswith(entry: str, that: str) -> bool:
    """Case insensitive starts with."""
    return bool(entry.lower().startswith(that.lower()))


def op_matches(entry: str, that: str) -> bool:
    """Matches regular expression."""
    return bool(re.compile(that).match(entry))


def op_startswith(entry: str, that: str) -> bool:
    """Case sensitive starts with."""
    return bool(entry.startswith(that))


ACTION_MAP = {
    CONTAINS: op_contains,
    ENDSWITH: op_endswith,
    EQUALS: op_equals,
    ICONTAINS: op_icontains,
    IENDSWITH: op_iendswith,
    IEQUALS: op_iequals,
    ISTARTSWITH: op_istartswith,
    MATCHES: op_matches,
    STARTSWITH: op_startswith,
}


class FilterMap:
    """The class FilterMap validates the task data against known operations and required arguments.

    Known operations are:

    - drop
    - keep
    - replace

    A meta operation is:

    - order

    This "operation" is optional but if present must fully specify the order of application of the "real" operations.

    The default order of application is

    1. keep
    2. drop
    3. replace

    Real operation JSON member values are a list of list of strings (the payloads).
    The payloads have length two with semantics depending on the operation.

    Operations keep amd drop both iterate over all payloads in the order given
    by applying the action encoded in the first list item and using the second item as parameter
    on the cell content (list of strings) elements.

    The encoding of actions is as follows (for cell entry `entry` and payload parameter `that`):

    - contains - `that in entry`
    - endswith - `entry.endswith(that)`
    - equals - `that == entry`
    - icontains - `that.lower() in entry.lower()`
    - iendswith - `entry.lower().endswith(that.lower())`
    - iequals - `that.lower() == entry.lower()`
    - istartswith - `entry.lower().startswith(that.lower())`
    - matches - `re.compile(that).match(entry)`
    - startswith - `entry.startswith(that)`

    The third operation (replace) is delegated to the string replace function as action.
    In this case a payload pair like ["this", "with that"] is applied as `entry.replace('this', 'with that')`.

    """

    ORDER: FILTER_ORDER_TYPE = [KEEP, DROP, REPLACE]

    def __init__(self, column: str, filter_data: FILTER_MAP_TYPE):
        self.column = column
        self.filter_data: FILTER_MAP_TYPE = filter_data

        self.order = self.filter_data[ORDER] if self.filter_data.get(ORDER, []) else FilterMap.ORDER
        log.debug(f'{self.order=}')

        self.keeps: FILTER_PAYLOAD_TYPE = self.filter_data.get(KEEP, [])  # type: ignore
        self.drops: FILTER_PAYLOAD_TYPE = self.filter_data.get(DROP, [])  # type: ignore
        self.replaces: FILTER_PAYLOAD_TYPE = self.filter_data.get(REPLACE, [])  # type: ignore

        self.operations = []
        for kind in self.order:
            if kind == KEEP:
                if self.keeps:
                    self.operations.append((kind, self.keeps))
            elif kind == DROP:
                if self.drops:
                    self.operations.append((kind, self.drops))
            elif kind == REPLACE:
                if self.replaces:
                    self.operations.append((kind, self.replaces))
            else:
                log.warning(f'ignored order element ({kind}) - please verify your filter data')

    def apply(self, entry: str) -> str:
        """Initial naive application during stage 1 implementation of transformer."""
        if not entry.strip():  # TODO(sthagen) - this may exclude use cases of manipulating space ;-)
            return ''
        if not self.operations:
            return entry
        transformed = entry
        pre_replace = False
        if self.operations:
            kind, tasks = self.operations[0]
            if kind == REPLACE and tasks:
                pre_replace = True
                for this, with_that in tasks:
                    log.debug(f'before replace("{this}", "{with_that}") call on content({transformed})')
                    transformed = transformed.replace(this, with_that)
                    log.debug(f'       replace("{this}", "{with_that}")   -->   content({transformed})')

        for kind, tasks in self.operations:
            log.debug(f'+ applying ({kind}) operations to ({transformed})')
            if kind in (KEEP, DROP):
                if tasks:
                    for key, parameter in tasks:
                        log.debug(
                            f'  - applying action ({key})({parameter}) for operation type ({kind}) on ({transformed})'
                        )
                        if key.lower() not in ACTION_KEYS:
                            log.warning(f'skipping action with unknown key ({key}) for operation type ({kind})')
                            continue
                        hit = ACTION_MAP[key.lower()](transformed, parameter)
                        log.debug(f'    ==> {"hit" if hit else "miss"} for ({transformed})')
                        if hit:
                            if kind == DROP:
                                return ''
                            if kind == KEEP:
                                return transformed
            elif not pre_replace:  # REPLACE
                if tasks:
                    for this, with_that in tasks:
                        transformed = transformed.replace(this, with_that)

        return transformed
