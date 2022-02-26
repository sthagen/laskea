# Third Party Dependencies

The [SBOM in CycloneDX v1.4 JSON format](https://github.com/sthagen/laskea/blob/default/sbom.json) with
SHA256 checksum ([0d891aab ...](https://raw.githubusercontent.com/sthagen/laskea/default/sbom.json.sha256 "sha256:0d891aab5a0651e2c8cd3c62bcc2ef83531c73f7636c6f469dac8182774d769d")).

## Licenses 

JSON files with complete license info of: [direct dependencies](direct-dependency-licenses.json) | [all dependencies](all-dependency-licenses.json)

### Direct Dependencies

| Name                                                                          | Version | License                 | Author             | Description (from packaging data)                                       |
|:------------------------------------------------------------------------------|:--------|:------------------------|:-------------------|:------------------------------------------------------------------------|
| [atlassian-python-api](https://github.com/atlassian-api/atlassian-python-api) | 3.20.1  | Apache Software License | Matt Harasymczuk   | Python Atlassian REST API Wrapper                                       |
| [cogapp](http://nedbatchelder.com/code/cog)                                   | 3.3.0   | MIT License             | Ned Batchelder     | Cog: A content generator for executing Python snippets in source files. |
| [jmespath](https://github.com/jmespath/jmespath.py)                           | 0.10.0  | MIT License             | James Saryerwinnie | JSON Matching Expressions                                               |
| [pydantic](https://github.com/samuelcolvin/pydantic)                          | 1.9.0   | MIT License             | Samuel Colvin      | Data validation and settings management using python 3.6 type hinting   |
| [typer](https://github.com/tiangolo/typer)                                    | 0.4.0   | MIT License             | Sebastián Ramírez  | Typer, build great CLIs. Easy to code. Based on Python type hints.      |

### Indirect Dependencies

| Name                                                               | Version   | License                              | Author                 | Description (from packaging data)                                                                       |
|:-------------------------------------------------------------------|:----------|:-------------------------------------|:-----------------------|:--------------------------------------------------------------------------------------------------------|
| [Deprecated](https://github.com/tantale/deprecated)                | 1.2.13    | MIT License                          | Laurent LAPORTE        | Python @deprecated decorator to deprecate old python classes, functions or methods.                     |
| [certifi](https://certifiio.readthedocs.io/en/latest/)             | 2021.10.8 | Mozilla Public License 2.0 (MPL 2.0) | Kenneth Reitz          | Python package for providing Mozilla's CA Bundle.                                                       |
| [charset-normalizer](https://github.com/ousret/charset_normalizer) | 2.0.12    | MIT License                          | Ahmed TAHRI @Ousret    | The Real First Universal Charset Detector. Open, modern and actively maintained alternative to Chardet. |
| [click](https://palletsprojects.com/p/click/)                      | 8.0.4     | BSD License                          | Armin Ronacher         | Composable command line interface toolkit                                                               |
| [idna](https://github.com/kjd/idna)                                | 3.3       | BSD License                          | Kim Davies             | Internationalized Domain Names in Applications (IDNA)                                                   |
| [oauthlib](https://github.com/oauthlib/oauthlib)                   | 3.2.0     | BSD License                          | The OAuthlib Community | A generic, spec-compliant, thorough implementation of the OAuth request-signing logic                   |
| [requests](https://requests.readthedocs.io)                        | 2.27.1    | Apache Software License              | Kenneth Reitz          | Python HTTP for Humans.                                                                                 |
| [requests-oauthlib](https://github.com/requests/requests-oauthlib) | 1.3.1     | BSD License                          | Kenneth Reitz          | OAuthlib authentication support for Requests.                                                           |
| [six](https://github.com/benjaminp/six)                            | 1.16.0    | MIT License                          | Benjamin Peterson      | Python 2 and 3 compatibility utilities                                                                  |
| [typing-extensions](https://github.com/python/typing)              | 4.1.1     | Python Software Foundation License   | UNKNOWN                | Backported and Experimental Type Hints for Python 3.6+                                                  |
| [urllib3](https://urllib3.readthedocs.io/)                         | 1.26.8    | MIT License                          | Andrey Petrov          | HTTP library with thread-safe connection pooling, file post, and more.                                  |
| [wrapt](https://github.com/GrahamDumpleton/wrapt)                  | 1.13.3    | BSD License                          | Graham Dumpleton       | Module for decorators, wrappers and monkey patching.                                                    |
 
## Dependency Tree(s)

JSON file with the complete package dependency tree info of: [the full dependency tree](package-dependency-tree.json)

### Rendered SVG

![Trees of the direct dependencies](package-dependency-tree.svg)

### Console Representation

```console
atlassian-python-api==3.20.1
  - deprecated [required: Any, installed: 1.2.13]
    - wrapt [required: >=1.10,<2, installed: 1.13.3]
  - oauthlib [required: Any, installed: 3.2.0]
  - requests [required: Any, installed: 2.27.1]
    - certifi [required: >=2017.4.17, installed: 2021.10.8]
    - charset-normalizer [required: ~=2.0.0, installed: 2.0.12]
    - idna [required: >=2.5,<4, installed: 3.3]
    - urllib3 [required: >=1.21.1,<1.27, installed: 1.26.8]
  - requests-oauthlib [required: Any, installed: 1.3.1]
    - oauthlib [required: >=3.0.0, installed: 3.2.0]
    - requests [required: >=2.0.0, installed: 2.27.1]
      - certifi [required: >=2017.4.17, installed: 2021.10.8]
      - charset-normalizer [required: ~=2.0.0, installed: 2.0.12]
      - idna [required: >=2.5,<4, installed: 3.3]
      - urllib3 [required: >=1.21.1,<1.27, installed: 1.26.8]
  - six [required: Any, installed: 1.16.0]
cogapp==3.3.0
jmespath==0.10.0
pydantic==1.9.0
  - typing-extensions [required: >=3.7.4.3, installed: 4.1.1]
typer==0.4.0
  - click [required: >=7.1.1,<9.0.0, installed: 8.0.4]
```
