# API

The API provides simple functions for embeddings in markdown documents.

Currently, there are two distinct kinds of embeddings: Sequence like embeddings and single item embeddings.

## Sequence Functions

The following functions produce markdown constructs that receive sequences:

* `table(query_text)` - a markdown GFM table
* `dl(query_text)` - a definition (description) list
* `ol(query_text)` - an ordered list
* `ul(query_text)` - an unordered list

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

* `data`value is a dict, with at lease one `rows` key with a list as value.
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
