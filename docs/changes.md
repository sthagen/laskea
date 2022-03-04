# Change History

## 2022.3.4

* Introduced ul function for injecting unordered markdown lists of keys and summaries

## 2022.3.3

* Introduced quiet flag
* Changed positional argument handling (accepting multiple files)
* The underlying code generator is called per input argument term
* Enhanced test coverage

## 2022.3.2

* First working implementation of command line mode
* Added layered configuration handling: -c option, cwd, parent folders, home first wun wins, env overwrites
* Added new command template to produce a starter template JSON file
* Added source of effective configuration detection and reporting
* Added verbose flags to verify and updated commands
* Added effective configuration reporting to easily generate proven configurations from experimenting 
* Consolidated update and verify commands into update command with verify (dry-run) option

## 2022.3.1

* Fixed laskea.api.jira matrix construction (library mode)
* Added cog api integration for update
* Moved all inputs to environment (no file based configuration yet)

## 2022.2.28

* Enhanced laskea.api.jira for use as a library via code generator

## 2022.2.27

* Documented usage examples (for now primarily shenannigans)
* Added update, verify, and version CLI interfaces
* Automated SBOM creation and dependency information retrieval
* Added parent commit information to version info
* Generated JQL listener and visitor APIs from ANTLR4 grammar

## 2022.2.26

* Initial version on PyPI
