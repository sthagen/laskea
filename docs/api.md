# API

The API provides simple functions for embeddings in markdown documents.

Currently, there are three distinct kinds of embeddings: Section/subsection partial document embeddings, sequence like embeddings, and single item embeddings.

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
