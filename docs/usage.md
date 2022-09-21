# Example Usage

**Note**: After having set up a local configuration, normally only two of the many possible environment
variables are set: `LASKEA_USER` and `LASKEA_TOKEN`. In some cases the debug variable `LASKEA_DEBUG`
may be helpful temporarily.

## Help

```console
$ laskea
Usage: laskea [OPTIONS] COMMAND [ARGS]...

  Calculate (Finnish: laskea) some parts.

Options:
  -V, --version  Display the laskea version and exit
  -h, --help     Show this message and exit.

Commands:
  report    Write a report of the environment for bug reports to standard...
  template  Write a template of a well-formed JSON configuration to...
  update    Fill in some parts of the input document.
  version   Display the laskea version and exit.
```

## Report

```console
$ laskea report

--------------------------------------------------------------------------------
  Date: Thu Jul 28 04:47:55 2022 UTC

                OS : Linux
            CPU(s) : 1
           Machine : x86_64
      Architecture : 64bit
       Environment : Python

  Python 3.9.13 (main, May 25 2022, 05:23:35)  [GCC 9.4.0]

            laskea : 2022.7.27+parent.c14c701a
         atlassian : 3.25.0
     cogapp.cogapp : 3.3.0
          jmespath : 1.0.1
          pydantic : 1.9.1
    requests_cache : 0.9.5
            scooby : 0.5.12
             typer : 0.6.1
--------------------------------------------------------------------------------
```

### Help

```console
Usage: laskea report [OPTIONS]

  Output either text options for the user to report her env or the report of
  the environment for support.

Options:
  -s, --shallow  Shallow reporting - no setuptools required (default is False)
  -h, --help     Show this message and exit.
```

## Template

```console
$ laskea template
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
      },
      "lf_only": true,
      "join_string": " <br>"
    }
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
  }
}
```

### Help

```console
$ laskea template --help
Usage: laskea template [OPTIONS]

  Write a template of a well-formed JSON configuration to standard out and
  exit

  The strategy for looking up configurations is to start at the current
  working directory trying to read a file with the name `.laskea.json` else
  try to read same named file in the user folder (home).

  In case an explicit path is given to the config option of commands that
  offer it, only that path is considered.

Options:
  -h, --help  Show this message and exit.
```

## Update

```console
$ laskea update tests/fixtures/basic/empty.md
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
      },
      "lf_only": false,
      "join_string": " <br>"
    }
  },
  "remote": {
    "is_cloud": true,
    "user": "someuser",
    "token": "",
    "base_url": "https://some.server.example.com/"
  },
  "local": {
    "markers": "[[[fill ]]] [[[end]]]",
    "quiet": false,
    "verbose": false,
    "strict": false
  }
}
# --- E N D ---
INFO: Upstream JIRA instance is addressed per cloud rules
Cogging tests/fixtures/basic/empty.md
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
$ laskea update -h
Usage: laskea update [OPTIONS] SOURCE...

  Fill in some parts of the input document.

  You can set some options per evironment variables:

  * LASKEA_USER='remote-user'
  * LASKEA_TOKEN='remote-secret'
  * LASKEA_BASE_URL='https://remote-jira-instance.example.com/'
  * LASKEA_CACHE_EXPIRY_SECONDS=180
  * LASKEA_COL_FIELDS: '["Key", "Summary", "Custom Field Name"]'
  * LASKEA_COL_MAPS='{"key": ["key", "key"], "summary": ["summary", "fields.summary"],
    "custom field name": ["customfield_123", "fields.customfield_123"]}'
  * LASKEA_JOIN_STRING=' <br>'
  * LASKEA_LF_ONLY='AnythingTruthy'
  * LASKEA_IS_CLOUD='WhenNotConnectingToJiraServerButJiraCloud'
  * LASKEA_MARKERS='[[[fill ]]] [[[end]]]'
  * LASKEA_DEBUG='AnythingTruthy'
  * LASKEA_VERBOSE='AnythingTruthy'
  * LASKEA_STRICT='AnythingTruthy'

  The quiet option (if given) disables any conflicting verbosity setting.

Arguments:
  SOURCE...  [required]

Options:
  -i, --input <sourcepath>        Path to input file
  -c, --config <configpath>       Path to config file (default is
                                  $HOME/.laskea.json)
  -n, --dry-run                   Dry run (default is False)
  -v, --verbose                   Verbose output (default is False)
  -q, --quiet                     Minimal output (default is False)
  -s, --strict                    Ouput noisy warnings on console and in the
                                  processed document (default is False)
  -x, --cache-expiry-seconds INTEGER
                                  Request cache expiry in seconds (default is
                                  180)  [default: 180]
  -h, --help                      Show this message and exit.
```

## Version

```console
$ laskea version
Calculate (Finnish: laskea) some parts. version 2022.7.27+parent.c14c701a
```
