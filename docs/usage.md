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
  update   Fill in some parts of the input document.
  verify   Answer the question if the input document is in good shape.
  version  Display the laskea version and exit.
```

## Update

```console
$ laskea update tests/fixtures/basic/empty.md
using configuration ({})
Would act on command ='update', inp ='tests/fixtures/basic/empty.md', and config ='/Users/ruth/.laskea.json'
NotImplemented (yet)
```

### Help

```console
$ laskea update -h
Usage: laskea update [OPTIONS] [SOURCE]

  Fill in some parts of the input document.

Arguments:
  [SOURCE]  [default: ]

Options:
  -i, --input <sourcepath>   Path to input file
  -c, --config <configpath>  Path to config file (default is
                             $HOME/.laskea.json)
  -h, --help                 Show this message and exit.
```

## Verify

```console
$ laskea verify tests/fixtures/basic/empty.md
using configuration ({})
Would act on command ='verify', inp ='tests/fixtures/basic/empty.md', and config ='/Users/ruth/.laskea.json'
NotImplemented (yet)
```

### Help

```console
$ laskea verify -h
Usage: laskea verify [OPTIONS] [SOURCE]

  Answer the question if the input document is in good shape.

Arguments:
  [SOURCE]  [default: ]

Options:
  -i, --input <sourcepath>   Path to input file
  -c, --config <configpath>  Path to config file (default is
                             $HOME/.laskea.json)
  -h, --help                 Show this message and exit.
```

## Version

```console
$ laskea version
Calculate (Finnish: laskea) some parts. version 2022.2.28+parent.39977ab5
```
