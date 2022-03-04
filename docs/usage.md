# Example Usage

## Help

```console
$ laskea
Usage: laskea [OPTIONS] COMMAND [ARGS]...

  Calculate (Finnish: laskea) some parts.

Options:
  -V, --version  Display the laskea version and exit
  -h, --help     Show this message and exit.

Commands:
  template  Write a template of a well-formed JSON configuration to...
  update    Fill in some parts of the input document.
  version   Display the laskea version and exit.
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
      }
    }
  },
  "remote": {
    "user": "",
    "token": "",
    "base_url": "https://remote-jira-instance.example.com/"
  },
  "local": {
    "markers": "[[[fill ]]] [[[end]]]",
    "verbose": false
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
Configuration interface requested - Experimental!
Effective configuration combining /home/ofsomeone/.laskea.json and environment variables:
# --- BEGIN ---
{
  "table": {
    "column": {
      "fields": [
        "Key",
        "Summary",
        "Foo",
        "Bar"
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
        "foo": [
          "customfield_11501",
          "fields.customfield_11501"
        ],
        "bar": [
          "customfield_13901",
          "fields.customfield_13901[].value"
        ]
      }
    }
  },
  "remote": {
    "user": "someuser",
    "token": "",
    "base_url": "https://some.server.example.com/"
  },
  "local": {
    "markers": "[[[fill ]]] [[[end]]]",
    "verbose": false
  }
}
# --- E N D ---
Cogging tests/fixtures/basic/empty.md
```

### Help

```console
$ laskea update -h
Usage: laskea update [OPTIONS] SOURCE...

  Fill in some parts of the input document.

  You can set some options per evironment variables:

  * ASCIINATOR_USER='remote-user'
  * ASCIINATOR_TOKEN='remote-secret'
  * ASCIINATOR_BASE_URL='https://remote-jira-instance.example.com/'
  * ASCIINATOR_COL_FIELDS: '["Key", "Summary", "Custom Field Name"]'
  * ASCIINATOR_COL_MAPS='{"key": ["key", "key"], "summary": ["summary", "fields.summary"],
    "custom field name": ["customfield_123", "fields.customfield_123"]}'
  * ASCIINATOR_MARKERS='[[[fill ]]] [[[end]]]'
  * ASCIINATOR_DEBUG='AnythingTruthy'

  The quiet option (if given) disables any conflicting verbosity setting.

Arguments:
  SOURCE...  [required]

Options:
  -i, --input <sourcepath>   Path to input file
  -c, --config <configpath>  Path to config file (default is
                             $HOME/.laskea.json)
  -n, --dry-run              Dry run (default is False)
  -v, --verbose              Verbose output (default is False)
  -q, --quiet                Minimal output (default is False)
  -h, --help                 Show this message and exit.
```

## Version

```console
$ laskea version
Calculate (Finnish: laskea) some parts. version 2022.3.4+parent.ec1ce47e
```
