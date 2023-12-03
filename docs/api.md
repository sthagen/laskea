# API

The API provides simple functions for embeddings in markdown documents.

Currently, there are three distinct kinds of embeddings: Section/subsection partial document embeddings, sequence like embeddings, and single item embeddings.

## Configuration

The configuration per `.laskea.json` as well via environment variables allows for simplifying the 
embedded function calls.

### Column Filter Map

Either as `.laskea.json` values from key `filter_map` or by setting the environment variable `LASKEA_COL_FILTERS`
to the JSON object accordingly a column filter map can be defined to process the values in cells of columns
as returned by the data source before transforming into the layout representation.

Example for a filter map only applying filters to entries retrieved for the `"custom field name"` column:

```json
{
  "key": {},
  "summary": {},
  "custom field name": {
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
  },
  "custom field other": {}
}
```

#### Domain Specific Language

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
In this case a payload pair like \["this", "with that"] is applied as `entry.replace('this', 'with that')`.

##### Examples of Transform Application

Sub minimal:

```python
import laskea.transform as tr
c_filter = tr.FilterMap('c', {})
assert c_filter.apply('foo') == 'foo'
```

Minimal:

```python
import laskea.transform as tr
c_filter = tr.FilterMap('c', {'drop': [['equals', 'that']]})
assert c_filter.apply('that') == ''
```

Order impact:

```python
import laskea.transform as tr
c_filter = tr.FilterMap('c', {'keep': [['iequals', 'that']], 'drop': [['equals', 'THAT']]})
assert c_filter.apply('THAT') == 'THAT'
```


Example with pre replace effect:

```python
import laskea.transform as tr
c_filter = tr.FilterMap(
    'c',
    {
        'order': ['replace', 'keep', 'drop'],
        'replace': [['THAT', 'that']],
        'keep': [['equals', 'THAT']],
        'drop': [['equals', 'that']],
    },
)
assert c_filter.apply('THAT') == ''
```

Further examples can be found at the end of the `test/test_transform.py` file.

## Document Part Functions

The following function produces markdown constructs that map parent issues with children issues onto subsections and subsubsections:

* `test_plans(parents_query_text, children_query_text)` - parent issues become subsections and children issues (including their description as content) become subsubsections

## Sequence Functions

The following functions produce markdown constructs that receive sequences:

* `mbom_table(filename)` - a markdown GFM table from an excel workbook `filename`
* `metrics_table(configuration)` - a markdown GFM table from a REST interface defined per configuration
* `table(query_text, caption='', column_fields=None)` - a markdown GFM table
* `dl(query_text)` - a definition (description) list
* `ol(query_text)` - an ordered list
* `ul(query_text)` - an unordered list


### Table Caption DSL

Since version 2023.11.21 the caption string offers a mini DSL to transform the summary information
into the form expected for the documents.

An example value is provided by `laskea.DEFAULT_CAPTION`:

```python
DEFAULT_CAPTION = "$NL$$NL$Table: Search '$QUERY_TEXT$' resulted in $ISSUE_COUNT$ issue$SINGULAR$$PLURAL$s$"
``` 

the table call will replace any:

* `$NL$` with a newline (`\n`)
* `$QUERY_TEXT$` with the JQL query text
* `$ISSUE_COUNT$` with the count of issues found that match the search (the JQL query)
* `$SINGULAR$$PLURAL$s$` with `s` if the issue count is not 1 else an empty string

The above default template will result in a table caption as expected by pandoc like e.g.

```
...
| A-1 | b |

Table: Search 'key = A-1' resulted in 1 issue
<!--...
```

**Note**: the table function allows to change the column labels by adding entries that are tuples or lists with two ordered members: `key` and `label`. 
The following example will change the displayed column label for column `Summary` to only show `S`:

```python
table('project = FOO AND labels = BAR', column_fields=('Key', ('Summary', 'S'), 'Baz', 'Quux'))
```

The following function produces separated values lists from JQL queries:

* `svl(query_text, key_magic=False, field_sep='|')` - a separated values list from a REST interface defined per configuration

## Single Item Returning Functions

* `h1(query_text)` - a level 1 heading
* `h2(query_text)` - a level 2 heading
* `h3(query_text)` - a level 3 heading
* `h4(query_text)` - a level 4 heading
* `h5(query_text)` - a level 5 heading
* `h6(query_text)` - a level 6 heading

## Additional Parameters

All functions accept an optional keyword parameter `data` that when given will render that data instead of querying a server.

This can be helpful to test the format without always querying the server.

For this data inject to work, the following characteristic must be present in the data:

* `data`value is a dict
    * with at least one `rows` key with a list as value.
        * that list contains one or more dicts with 
            * the expected keys (from the column spec) and
            * the values that should be injected.

```python
from laskea import *
ul('', data={'rows': [{'key': 'A', 'summary': 'B'}, {'key': 'C', 'summary': 'D'}]})
```

This should yield the following output:

```markdown
- [A](https://remote-jira-instance.example.com/browse/A) - B
- [C](https://remote-jira-instance.example.com/browse/C) - D

```

Using the svl function (that implements the csv command of the app:

```python
from laskea import *
data = {'rows': [{'key': 'A', 'summary': 'B'}, {'key': 'C', 'summary': 'D'}]}
svl('', field_sep='x', data=data)
```

This should yield the following output:

```csv
keyxsummary
AxB
CxD

```

Using a field separator / delimiter that is contained within one of more values
like e.g. here the letter `u` and a replacement text `xoxo`:

```python
from laskea import *
data = {'rows': [{'key': 'A', 'summary': 'B'}, {'key': 'C', 'summary': 'D'}]}
svl('', field_sep='u', replacement='xoxo', data=data)
```

Yields:

```csv
keyusxoxommary
AuB
CuD

```
