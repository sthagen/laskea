# Basic Example

Current update command:
```console
$ cog -I. -P -c -r --markers='[[[fill ]]] [[[end]]]' -p "from api import *" files*.md
```

The following three environment variables are set:
* `ASCIINATOR_USER=<jira-user>`
* `ASCIINATOR_TOKEN='<jira-secret-of-user>'`
* `ASCIINATOR_BASE_URL='https://jira.example.com/' `

## Normal Use

Step 1: Inject the JQL (in this case `'project = ABC AND labels = RELEVANT_LABEL order by key ASC'`) and some minimal boilerplate:
```markdown
<!--[[[fill table('project = ABC AND labels = RELEVANT_LABEL order by key ASC')]]]-->
<!--[[[end]]]-->
```

Step 2: Someone calls the code generator:
```console
$ cog -I. -P -c -r --markers='[[[fill ]]] [[[end]]]' -p "from api import *" files*.md
```
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
