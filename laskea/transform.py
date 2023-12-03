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
]
}

"""
from laskea import FILTER_MAP_TYPE, FILTER_ORDER_TYPE, FILTER_PAYLOAD_TYPE, log


DROP = 'drop'
KEEP = 'keep'
ORDER = 'order'
REPLACE = 'replace'


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

    contains - `that in entry`
    endswith - `entry.endswith(that)`
    equals - `that == entry`
    icontains - `that.lower() in entry.lower()`
    iendswith - `entry.lower().endswith(that.lower())`
    iequals - `that.lower() == entry.lower()`
    istartswith - `entry.lower().startswith(that.lower())`
    matches - `re.compile(that).matches(entry)`
    startswith - `entry.startswith(that)`

    The third operation (replace) is delegated to the string replace function as action.
    In this case a payload pair like ["this", "with that"] is applied as `entry.replace('this', 'with that')`.

    """

    ORDER: FILTER_ORDER_TYPE = [KEEP, DROP, REPLACE]

    def __init__(self, column: str, filter_data: FILTER_MAP_TYPE):
        self.column = column
        self.filter_data: FILTER_MAP_TYPE = filter_data
        self.order = self.filter_data[ORDER] if self.filter_data.get(ORDER, []) else FilterMap.ORDER
        self.keeps: FILTER_PAYLOAD_TYPE = self.filter_data.get(KEEP, [[]])  # type: ignore
        self.drops: FILTER_PAYLOAD_TYPE = self.filter_data.get(DROP, [[]])  # type: ignore
        self.replaces: FILTER_PAYLOAD_TYPE = self.filter_data.get(REPLACE, [[]])  # type: ignore
        self.tasks = []
        for operation in self.order:
            if operation == KEEP:
                self.tasks.append((KEEP, self.keeps))
            elif operation == DROP:
                self.tasks.append((DROP, self.drops))
            elif operation == REPLACE:
                self.tasks.append((REPLACE, self.replaces))
            else:
                log.warning(f'ignored order element ({operation}) - please verify your filter data')

    def apply(self, entry: str) -> str:
        """Initial naive application during stage 1 implementation of transformer."""
        if not entry.strip():  # TODO(sthagen) - this may exclude use cases of manipulating space ;-)
            return ''
        if not self.tasks:
            return entry
        transformed = entry
        for kind, task in self.tasks:
            pass

        return transformed
