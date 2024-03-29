# Example Usage

**Note**: After having set up a local configuration, normally only two of the many possible environment
variables are set: `LASKEA_USER` and `LASKEA_TOKEN`. In some cases the debug variable `LASKEA_DEBUG`
may be helpful temporarily.

## Help

```console
❯ laskea


 Usage: laskea [OPTIONS] COMMAND [ARGS]...

 Calculate (Finnish: laskea) some parts.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version  -V        Display the laskea version and exit                                                 │
│ --help     -h        Show this message and exit.                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ csv       Export query result as separated values list.                                                  │
│ report    Output either text options for the user to report her env or the report of the environment for │
│           support.                                                                                       │
│ template  Write a template of a well-formed JSON configuration to standard out and exit                  │
│ update    Fill in some parts of the input document.                                                      │
│ version   Display the laskea version and exit.                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Report

```console
❯ laskea report

--------------------------------------------------------------------------------
  Date: Sun Dec 03 21:11:11 2023 CET

                OS : Darwin
            CPU(s) : 8
           Machine : arm64
      Architecture : 64bit
               RAM : 16.0 GiB
       Environment : Python
       File system : apfs

  Python 3.10.12 (main, Jul 16 2023, 10:40:08) [Clang 16.0.6 ]

            laskea : 2023.12.3
         atlassian : 3.41.4
     cogapp.cogapp : 3.3.0
          jmespath : 1.0.1
          pydantic : 2.5.2
    requests_cache : 1.1.1
            scooby : 0.9.2
             typer : 0.9.0
--------------------------------------------------------------------------------
```

### Help

```console
❯ laskea report --help

 Usage: laskea report [OPTIONS]

 Output either text options for the user to report her env or the report of the environment for support.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --shallow  -s        Shallow reporting - no setuptools required (default is False)                       │
│ --help     -h        Show this message and exit.                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Template

```console
❯ laskea template
{
  "table": {
    "column": {
      "fields": [
        "Key",
        "Summary",
        "Custom Field Name",
        ["Custom Field Other", "Display Name"]
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
      },
      "filter_map": {
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
            ["matches", "[A-Z]+-\d+"]
          ],
          "replace": [
            ["DEF-", "definition-"]
          ]
        },
        "custom field other": {}
      },
      "lf_only": true,
      "join_string": " <br>"
    },
    "caption": "$NL$$NL$Table: Search '$QUERY_TEXT$' resulted in $ISSUE_COUNT$ issue$SINGULAR$$PLURAL$s$"
  },
  "remote": {
    "is_cloud": false,
    "user": "",
    "token": "",
    "base_url": "https://remote-jira-instance.example.com/"
  },
  "local": {
    "markers": "[[[fill ]]] [[[end]]]",
    "quiet": false,
    "verbose": false,
    "strict": false
  },
  "excel": {
    "mbom": "mbom.xlsm"
  },
  "tabulator": {
    "overview": {
        "base_url": "https://example.com/metrics/",
        "path": "$year$/kpi-table-$year$.json",
        "years": [2022],
        "matrix": [
            ["section", "Section", False, "L"],
            ["name", "Name", False, "L"],
            ["unit", "Unit", False, "C"],
            ["all", "ALL", True, "R"],
            ["pr1", "PR1", True, "R"],
            ["pr2", "PR2", True, "R"],
            ["pr3", "PR3", True, "R"],
            ["description", "Description", False, "L"]
        ]
    },
    "metrics": {
        "base_url": "https://example.com/metrics/",
        "paths": {
            "review_effectivity": "$year$/review_effectivity/kpi-review_effectivity-per_product-report-$year$.json",
            "sprint_effectivity": "$year$/sprint_effectivity/kpi-sprint_effectivity-per_product-report-$year$.json",
            "task_traceability": "$year$/task_traceability/kpi-task_traceability-per_product-report-$year$.json",
        },
        "years": [2021, 2022],
        "matrix": [
            ["month", "Month", False, "L"],
            ["all", "ALL", True, "R"],
            ["pr1", "PR1", True, "R"],
            ["pr2", "PR2", True, "R"],
            ["pr3", "PR3", True, "R"],
            ["trend_all", "±ALL", True, "R"],
            ["trend_pr1", "±PR1", True, "R"],
            ["trend_pr2", "±PR2", True, "R"],
            ["trend_pr3", "±PR3", True, "R"]
        ]
    }
  }
}
```

### Help

```console
❯ laskea template --help

 Usage: laskea template [OPTIONS]

 Write a template of a well-formed JSON configuration to standard out and exit

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
## CSV (Separated Values List)

```console
❯ laskea csv -h

 Usage: laskea csv [OPTIONS] [QUERY]

 Export query result as separated values list.
 You can set some options per evironment variables:
 * LASKEA_USER='remote-user'
 * LASKEA_TOKEN='remote-secret'
 * LASKEA_BASE_URL='https://remote-jira-instance.example.com/'
 * LASKEA_CACHE_EXPIRY_SECONDS=180
 * LASKEA_COL_FIELDS: '[
     "Key",
     "Summary",
     "Custom Field Name",
     ["Custom Field Other", "Display Name"]
   ]'
 * LASKEA_COL_MAPS='{
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
   }'
 * LASKEA_COL_FILTERS='{
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
         ["matches", "[A-Z]+-\d+"]
       ],
       "replace": [
         ["DEF-", "definition-"]
       ]
     },
     "custom field other": {}
   }'
 * LASKEA_JOIN_STRING=' <br>'
 * LASKEA_LF_ONLY='AnythingTruthy'
 * LASKEA_CAPTION='empty or special DSL'
 * LASKEA_IS_CLOUD='WhenNotConnectingToJiraServerButJiraCloud'
 * LASKEA_MARKERS='[[[fill ]]] [[[end]]]'
 * LASKEA_DEBUG='AnythingTruthy'
 * LASKEA_VERBOSE='AnythingTruthy'
 * LASKEA_STRICT='AnythingTruthy'

 The quiet option (if given) disables any conflicting verbosity setting.

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────╮
│   query      [QUERY]                                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --jql-query             -j      <jql-query>         The query in JQL format. For example given a project │
│                                                     YES and two issues 123 and 124: 'project = YES and   │
│                                                     key in (YES-123, YES-124) order by created DESC'     │
│ --config                -c      <configpath>        Path to config file (default is $HOME/.laskea.json)  │
│ --key-magic             -k                          Apply magic to key by replacing with markdown like   │
│                                                     link (default is False)                              │
│ --delimiter             -d      <field-separator>   Delimiter / field separator On output, header and    │
│                                                     data cell values will have any occurences of the     │
│                                                     field separator replaced with the replacement string │
│                                                     [default: |]                                         │
│ --replacement           -r      <replacement-text>  Replacement string for occurences of FS in text      │
│                                                     On output, header and data cell values will have any │
│                                                     occurences of the field separator replaced with the  │
│                                                     replacement string                                   │
│                                                     [default: $FIELD_SEPARATOR$]                         │
│ --dry-run               -n                          Dry run (default is False)                           │
│ --verbose               -v                          Verbose output (default is False)                    │
│ --strict                -s                          Ouput noisy warnings on console and in the processed │
│                                                     document (default is False)                          │
│ --cache-expiry-seconds  -x      INTEGER             Request cache expiry in seconds [default: 180]       │
│ --help                  -h                          Show this message and exit.                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Update

```console
❯ laskea update test/fixtures/basic/empty.md
Reading from discovered configuration path /home/ofsomeone/.laskea.json
Configuration interface combined file, environment, and commandline values!
Effective configuration combining /home/ofsomeone/.laskea.json, environment variables, and defaults:
# --- BEGIN ---
{
  "table": {
    "column": {
      "fields": [
        "Key",
        "Summary",
        "Custom Field Name",
        [
          "Custom Field Other",
          "Display Name"
        ]
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
      },
      "lf_only": true,
      "join_string": " <br>"
    },
    "caption": "$NL$$NL$Table: Search '$QUERY_TEXT$' resulted in $ISSUE_COUNT$ issue$SINGULAR$$PLURAL$s$"
  },
  "remote": {
    "is_cloud": true,
    "user": "someuser",
    "token": "",
    "base_url": "https://some.example.com"
  },
  "local": {
    "markers": "[[[fill ]]] [[[end]]]",
    "quiet": false,
    "verbose": false,
    "strict": false
  }
}
# --- E N D ---
Cogging test/fixtures/basic/empty.md
```

Using the `mbom_table('mbom.xlsx')` feature requires an excel workbook `mbom.xlsx` with 
fields like e.g.:

```
Level	   P/N	    Item Name	    SW Version
0	       1233333	asdasd	
1	       124	    a a	          1
2	       123	    b b	          2
```

The resulting markdown inject after update will look like:

```markdown
<!--[[[fill mbom_table('mbom.xlsx')]]]-->
<!-- anchor: ('0', '1233333', 'asdasd', '')-->
| Level | P/N | Item Name | SW Version |
|:------|:----|:----------|:-----------|
| 1     | 124 | a a       | 1          |
| 2     | 123 | b b       | 2          |
<!-- source: mbom.xlsx-->
<!-- s-hash: sha512:98f49a212325387c2a800c000f6892879a38cae9fde357cca3de57bfcc18bb285d34ad81f19fae1df735ec85e8ada40e7f4ae06ffb5bfb4f89bc7592c8d63111-->
<!--[[[end]]] (checksum: 758ae76dfd82d3d10a9930047ea4a71f)-->
```

### Help

```console
❯ laskea update -h

 Usage: laskea update [OPTIONS] SOURCE...

 Fill in some parts of the input document.
 You can set some options per evironment variables:
 * LASKEA_USER='remote-user'
 * LASKEA_TOKEN='remote-secret'
 * LASKEA_BASE_URL='https://remote-jira-instance.example.com/'
 * LASKEA_CACHE_EXPIRY_SECONDS=180
 * LASKEA_COL_FIELDS: '[
     "Key",
     "Summary",
     "Custom Field Name",
     ["Custom Field Other", "Display Name"]
   ]'
 * LASKEA_COL_MAPS='{
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
   }'
 * LASKEA_COL_FILTERS='{
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
         ["matches", "[A-Z]+-\d+"]
       ],
       "replace": [
         ["DEF-", "definition-"]
       ]
     },
     "custom field other": {}
   }'
 * LASKEA_JOIN_STRING=' <br>'
 * LASKEA_LF_ONLY='AnythingTruthy'
 * LASKEA_CAPTION='empty or special DSL'
 * LASKEA_IS_CLOUD='WhenNotConnectingToJiraServerButJiraCloud'
 * LASKEA_MARKERS='[[[fill ]]] [[[end]]]'
 * LASKEA_DEBUG='AnythingTruthy'
 * LASKEA_VERBOSE='AnythingTruthy'
 * LASKEA_STRICT='AnythingTruthy'

 The quiet option (if given) disables any conflicting verbosity setting.

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    source      SOURCE...  [default: None] [required]                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --input                 -i      <sourcepath>  Path to input file                                         │
│ --config                -c      <configpath>  Path to config file (default is $HOME/.laskea.json)        │
│ --dry-run               -n                    Dry run (default is False)                                 │
│ --verbose               -v                    Verbose output (default is False)                          │
│ --quiet                 -q                    Minimal output (default is False)                          │
│ --strict                -s                    Ouput noisy warnings on console and in the processed       │
│                                               document (default is False)                                │
│ --cache-expiry-seconds  -x      INTEGER       Request cache expiry in seconds [default: 180]             │
│ --help                  -h                    Show this message and exit.                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Version

```console
❯ laskea version
Calculate (Finnish: laskea) some parts. version 2023.12.3+parent.dirty
```
