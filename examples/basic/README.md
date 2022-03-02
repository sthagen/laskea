# Basic Example

Current update command:
```console
$ laskea update files*.md
```
The configuration file `.laskea.json`provides all but one part of the configuration:

```json
{
  "table": {
    "column": {
      "fields": [
        "Key",
        "Summary",
        "Custom Field Name",
        "Custom Field Other"
      ],
      "field_map": {
        "key": [
          "key",
          "key"
        ],
        "summary": [
          "summary",
          "fields.summary"
        ],
        "custom field name": [
          "customfield_11501",
          "fields.customfield_11501"
        ],
        "custom field other": [
          "customfield_13901",
          "fields.customfield_13901[].value"
        ]
      }
    }
  },
  "remote": {
    "user": "someuser",
    "token": "",
    "base_url": "https://remote-jira-instance.example.com/"
  },
  "local": {
    "markers": "[[[fill ]]] [[[end]]]",
    "verbose": false
  }
}
```

The following environment variable is set to complete the configuration:
* `ASCIINATOR_TOKEN='<jira-secret-of-user>'`

## Normal Use

Step 1: Inject the JQL (in this case `'project = ABC AND labels = RELEVANT_LABEL order by key ASC'`) and some minimal boilerplate:
```markdown
<!--[[[fill table('project = ABC AND labels = RELEVANT_LABEL order by key ASC')]]]-->
<!--[[[end]]]-->
```

Step 2: Someone calls the code generator:
```console
$ laskea update files*.md
```
... or uses dry-run / verification mode of the update command.

Step 3: Inspect the result:
```markdown
<!--[[[fill table('project = ABC AND labels = RELEVANT_LABEL order by key ASC')]]]-->
| Key                                              | Summary    | Third              | Fourth |
|:-------------------------------------------------|:-----------|:-------------------|:-------|
| [ABC-1](https://jira.example.com/browse/ABC-1)   | The Text 1 | What<br>ever<br>is | 4th    |
| [ABC-42](https://jira.example.com/browse/ABC-42) | The Text 2 | third              | no. 4  |

2 issues
<!--[[[end]]] (checksum: abadcafeabadcafeabadcafeabadcafe)-->
```

Step 4. ... change something in markdown or change the tickets and labels in JIRA and then go back to step 2 ...
