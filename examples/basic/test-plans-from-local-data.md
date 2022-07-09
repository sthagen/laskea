<!--[[[fill
import json
import pathlib
P_C_L_FIXTURE_PATH = pathlib.Path('test', 'fixtures', 'basic', 'p_c_jira.json')
with open(P_C_L_FIXTURE_PATH, 'rt', encoding='utf-8') as handle:
    data = json.load(handle)
]]]-->
<!--[[[end]]]-->

# Basic Parent Children Sections Example File

Some constant introduction.

<!--[[[fill test_plans(data=data)]]]-->

## First summary

The Test Plan consists of 2 Test Cases

### Summary of a hundred and one

|*A*|*B*|
|:- |:- |
|v1|v2|
**Note**: Something noteworthy.

### Summary of a hundred and two

Test cases:
* C-103
**Note**: Something else worthy to state.

## Second summary

The Test Plan consists of 4 Test Cases

### Summary of a hundred and three

|*Another Head*|*Before the end column*|
|:------------ |:--------------------- |
|value 1.1|value 2.1|
|value 1.2|value 2.2|

### Summary of a hundred and four

|*Another Head*|*Before the end column*|
|:------------ |:--------------------- |
|value 1.1|value 2.1|
|A list:
- item
- meti
|value 2.2|

### Summary of a hundred and five

|Another Head|Before the end column|
|:---------- |:------------------- |
|value 1.1|A list:
* item
* meti
|
|value 1.2|value 2.2|

### Summary of a hundred and six

|Another Head|Before the end column|
|:---------- |:------------------- |
|value 1.1|value 2.1|
|value 1.2|value 2.2|

<!--[[[end]]] (checksum: 901d3ed763874b8091f3624b5bc8cbb8)-->

and:

<!--[[[fill print(json.dumps(data, indent=2))]]]-->
{
  "parent_data": {
    "data": {
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
              },
              {
                "id": 104,
                "key": "C-104",
                "fields": {
                  "issuetype": {
                    "name": "Test Case"
                  },
                  "summary": "Summary of a hundred and four"
                }
              },
              {
                "id": 105,
                "key": "C-105",
                "fields": {
                  "issuetype": {
                    "name": "Test Case"
                  },
                  "summary": "Summary of a hundred and five"
                }
              },
              {
                "id": 106,
                "key": "C-106",
                "fields": {
                  "issuetype": {
                    "name": "Test Case"
                  },
                  "summary": "Summary of a hundred and six"
                }
              }
            ]
          }
        }
      ]
    }
  },
  "children_data": {
    "data": {
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
        },
        {
          "id": 104,
          "key": "C-104",
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
            "summary": "Summary of a hundred and four",
            "description": "\n&nbsp;|*Another Head*|*Before the end column*|\n|value 1.1|value 2.1|\n|A list:\n- item\n- meti\n|value 2.2|\n\n\n",
            "created": "2019-03-12T10:01:25.000+0100",
            "updated": "2019-03-12T10:01:25.000+0100"
          }
        },
        {
          "id": 105,
          "key": "C-105",
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
            "summary": "Summary of a hundred and five",
            "description": "\n||Another Head||Before the end column||\n|value 1.1|A list:\n* item\n* meti\n|\n|value 1.2|value 2.2|\n\n\n",
            "created": "2019-03-12T10:01:25.000+0100",
            "updated": "2019-03-12T10:01:25.000+0100"
          }
        },
        {
          "id": 106,
          "key": "C-106",
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
            "summary": "Summary of a hundred and six (simulate inconsistency due to race)",
            "description": "\n||Another Head||Before the end column||\n|value 1.1|value 2.1|\n|value 1.2|value 2.2|\n\n\n",
            "created": "2019-03-12T10:01:25.000+0100",
            "updated": "2019-03-12T10:01:25.000+0100"
          }
        }
      ]
    }
  }
}
<!--[[[end]]] (checksum: 2fb37a73c62c3e16029e63c60c9e39ed)-->

Here some other text following the table ...
