# Change History

2023.12.10
:    * Breaking change: Added an option to enable the checksum feature (<https://todo.sr.ht/~sthagen/laskea/14>)

2023.12.4
:    * Amended the debug logs with more context info (<https://todo.sr.ht/~sthagen/laskea/12>)
* Documented how to change log levels (<https://todo.sr.ht/~sthagen/laskea/9>)
* Removed filtered out entries from sequence cell content (<https://todo.sr.ht/~sthagen/laskea/13>)

2023.12.3
:    * Added filtering on table cell content to table function (<https://todo.sr.ht/~sthagen/laskea/8>)
* Made summary / caption per DSL / configuration target more versatile (<https://todo.sr.ht/~sthagen/laskea/7>)
* Started to add logging insteda of print to stderr.

2023.11.21
:    * Implemented make summary / caption a DSL / configuration target (<https://todo.sr.ht/~sthagen/laskea/6>)

2023.11.19
:    * Made summary into self documenting useful markdown table caption (warning may change again)

2023.10.9
:    * Made summary in tables optional and false as default (<https://todo.sr.ht/~sthagen/laskea/5>)

2023.10.7
:    * Fixed the field names config handling to allow per config renaming of columns (<https://todo.sr.ht/~sthagen/laskea/4>)

2023.7.20
:    * Fixed the broken packaging - api is missing in 2023.6.18 (<https://todo.sr.ht/~sthagen/laskea/2>)
* Implemented a per embed table call configurable column head renaming (<https://todo.sr.ht/~sthagen/laskea/3>)

2023.6.18
:    * Added timeout to http requests (<https://todo.sr.ht/~sthagen/laskea/1>)
* Moved SBOM noise into folder and added SPDX SBOM (derived) in multiple file formats
* Updated dependencies

## 2022

2022.11.7
:    * Fixed positional argument (query) handling for the csv command

2022.11.6
:    * Added replacement option to the csv command that extracts separated values lists ...

2022.11.3
:    * Added csv command to extract separated values lists from ticket systems per queries in JQL

2022.9.22
:    * Hotfix to enable the console script again

2022.9.21
:    * Added API to read MBOM from office table file per convention

2022.7.27
:    * Bumped dependencies
* Updated SBOM as well as third-party documentation (prose)
* Moved documentation to [codes.dilettant.life/docs](https://codes.dilettant.life/docs/laskea)
* Moved tracker to [todo.sr.ht/~sthagen](https://todo.sr.ht/~sthagen/laskea)
* Moved normative source repo to [git.sr.ht/~sthagen](https://git.sr.ht/~sthagen/laskea)
* Provide test coverage documentation at [codes.dilettant.life/coverage](https://codes.dilettant.life/coverage/laskea)

2022.7.10
:    * Updated SBOM as well as third-party documentation (prose) and fixed findings from static code analysis.

2022.6.8
:    * Updated SBOM as well as third-party documentation (prose) and enhanced the naive table transformer.

2022.6.7
:    * Updated SBOM as well as third-party documentation (prose) and enhanced the experimental feature (#29).

2022.6.6
:    * Updated SBOM as well as third-party documentation (prose) and added an experimental feature (#29).

2022.5.31
:    * Bumped dependencies and updated SBOM as well as third-party documentation (prose).

2022.4.30
:    * Added configuration parameter to enable server certificate verification for tabulator API

2022.4.29
:    * Enlarged query result limit for JIRA backend (partially implementing #25 Offer a parameter to extend the limit for JIRA backend)

2022.4.26
:    * Fix for configuration file discovery (#23 Configuration search ignores current dir)
* Bumped atlassian API dependency

2022.3.23
:    * Hotfix for URL construction in kpi table to prepend the base url
 
2022.3.22
:    * Added tabulator mode table backend

2022.3.9
:    * Breaking change: Use `LASKEA_` prefixed environment variables (instead of `ASCIINATOR_`) - cf. `laskea update -h` for the names
* Moved "cloudness" log statement out of inject area for documents and redirected all logging to stderr
* Added JOIN_STRING parameter defaulting to `' <br>'` (before not customizable and fixed to be `'<br>'` which is stripped in PDF/DOCX conversions)
* Added LF_ONLY parameter defaulting to `True` (which will remove any `\r` from markdown output)

2022.3.8
:    * Introduced strict option to expose warnings on unexpected query result sizes otherwise inject empty strings
* Removed JQL grammar, parser, and antlr4 dependency (YAGNI) there is a tag `yagni-jql-parser` for sentimental days
* Coverage therefore jumped to above 2/3.
* Added more variables as entries to the template configuration
* Documented (some) usage changes and removed experimental warning

2022.3.7
:    * Reduced noise in dry-run mode when warnings were duplicated if not splitting stderr stream
* Added new dependency requests-cache to ease the load on the server
* Added new option for update command to set the expiry of the cache in seconds (default is 180 seconds or 3 minutes)
* Updated baseline, third-party information, and SBOM

2022.3.6
:    * Enhanced user experience for HTTP/400 client errors - failing JQL
* Enhanced user experience for unexpected results in embedded calls
* Added cloud switch to JIRA API - new environment variable and login parameter
* Added further embed calls for definition lists, and headers
* Added security baseline and hardened configuration resource handling
* Added tests growing the coverage to 55 %

2022.3.5
:    * Refactored codebase and tests
* Nits

2022.3.4
:    * Introduced ul function for injecting unordered markdown lists of keys and summaries
* Added report of environment facts command to support bug reports (new dependency scooby)

2022.3.3
:    * Introduced quiet flag
* Changed positional argument handling (accepting multiple files)
* The underlying code generator is called per input argument term
* Enhanced test coverage

2022.3.2
:    * First working implementation of command line mode
* Added layered configuration handling: -c option, cwd, parent folders, home first wun wins, env overwrites
* Added new command template to produce a starter template JSON file
* Added source of effective configuration detection and reporting
* Added verbose flags to verify and updated commands
* Added effective configuration reporting to easily generate proven configurations from experimenting 
* Consolidated update and verify commands into update command with verify (dry-run) option

2022.3.1
:    * Fixed laskea.api.jira matrix construction (library mode)
* Added cog api integration for update
* Moved all inputs to environment (no file based configuration yet)

2022.2.28
:    * Enhanced laskea.api.jira for use as a library via code generator

2022.2.27
:    * Documented usage examples (for now primarily shenannigans)
* Added update, verify, and version CLI interfaces
* Automated SBOM creation and dependency information retrieval
* Added parent commit information to version info
* Generated JQL listener and visitor APIs from ANTLR4 grammar

2022.2.26
:    * Initial version on PyPI
