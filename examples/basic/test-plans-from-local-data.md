<!--[[[fill
import json
import pathlib
P_C_L_FIXTURE_PATH = pathlib.Path('tests', 'fixtures', 'basic', 'p_c_jira.json')
with open(P_C_L_FIXTURE_PATH, 'rt', encoding='utf-8') as handle:
    data = json.load(handle)
]]]-->
<!--[[[end]]] (checksum: d41d8cd98f00b204e9800998ecf8427e)-->

# Basic Parent Children Sections Example File

Some constant introduction.

<!--[[[fill test_plans(data=data)]]]-->


## Test Plan First Summary (P-1)


### Test Case Summary Of A Hundred And One (C-101)


||*A*||*B*||
|v1|v2|

**Note**: Something noteworthy.


### Test Case Summary Of A Hundred And Two (C-102)


Test cases:
* C-103

**Note**: Something else worthy to state.


## Test Plan Second Summary (P-2)


### Test Case Summary Of A Hundred And Three (C-103)


||*Another Head*||*Before the end column*||
|value 1.1|value 2.1|
|value 1.2|value 2.2|


<!--[[[end]]] (checksum: 4edf8d0f29e5b83fdddb1cc4ce181c11)-->

and:

<!--[[[fill print(json.dumps(data, indent=2))]]]-->
{
  "parent_data": {
    "issues": [
      {
        "id": 1,
        "key": "P-1",
        "fields": {
          "issuetype": {
            "name": "Test Plan"
          },
          "summary": "First summary",
          "description": "",
          "customfield_10006": "E-42",
          "created": "2019-03-12T10:01:25.000+0100",
          "updated": "2019-03-12T10:01:25.000+0100",
          "subtasks": [
            {
              "id": 101,
              "key": "C-101",
              "fields": {
                "issuetype": {
                  "name": "Test Case"
                },
                "summary": "Summary of a hundred and one"
              }
            },
            {
              "id": 102,
              "key": "C-102",
              "fields": {
                "issuetype": {
                  "name": "Test Case"
                },
                "summary": "Summary of a hundred and two"
              }
            }
          ]
        }
      },
      {
        "id": 2,
        "key": "P-2",
        "fields": {
          "issuetype": {
            "name": "Test Plan"
          },
          "summary": "Second summary",
          "description": "",
          "customfield_10006": "E-42",
          "created": "2019-03-12T10:01:25.000+0100",
          "updated": "2019-03-12T10:01:25.000+0100",
          "subtasks": [
            {
              "id": 103,
              "key": "C-103",
              "fields": {
                "issuetype": {
                  "name": "Test Case"
                },
                "summary": "Summary of a hundred and three"
              }
            }
          ]
        }
      }
    ]
  },
  "children_data": {
    "issues": [
      {
        "id": 101,
        "key": "C-101",
        "fields": {
          "parent": {
            "key": "P-1",
            "issuetype": {
              "name": "Test Plan"
            }
          },
          "issuetype": {
            "name": "Test Case"
          },
          "summary": "Summary of a hundred and one",
          "description": "\n||*A*||*B*||\n|v1|v2|\n\n**Note**: Something noteworthy.\n",
          "created": "2019-03-12T10:01:25.000+0100",
          "updated": "2019-03-12T10:01:25.000+0100"
        }
      },
      {
        "id": 102,
        "key": "C-102",
        "fields": {
          "parent": {
            "key": "P-1",
            "issuetype": {
              "name": "Test Plan"
            }
          },
          "issuetype": {
            "name": "Test Case"
          },
          "summary": "Summary of a hundred and two",
          "description": "\nTest cases:\n* C-103\n\n**Note**: Something else worthy to state.\n",
          "created": "2019-03-12T10:01:25.000+0100",
          "updated": "2019-03-12T10:01:25.000+0100"
        }
      },
      {
        "id": 103,
        "key": "C-103",
        "fields": {
          "parent": {
            "key": "P-2",
            "issuetype": {
              "name": "Test Plan"
            }
          },
          "issuetype": {
            "name": "Test Case"
          },
          "summary": "Summary of a hundred and three",
          "description": "\n||*Another Head*||*Before the end column*||\n|value 1.1|value 2.1|\n|value 1.2|value 2.2|\n\n\n",
          "created": "2019-03-12T10:01:25.000+0100",
          "updated": "2019-03-12T10:01:25.000+0100"
        }
      }
    ]
  }
}
<!--[[[end]]] (checksum: 80d8643a753e061d71ab8f5f3048a835)-->

Here some other text following the table ...
