"""Gateway to fill in the generated tables into the documents."""
import os
import laskea.api.jira as asciinator

__all__ = ['COLUMNS', 'table']
COLUMNS = ('Key', 'Summary', 'Third', 'Fourth')
asciinator.DEFAULT_COLUMN_FIELDS = COLUMNS
asciinator.KNOWN_CI_FIELDS = {
    'key': ('key', 'issues[].key'),
    'summary': ('summary', 'issues[].fields.summary'),
    'priority': ('priority', 'issues[].fields.priority.name'),
    'status': ('status', 'issues[].fields.status.name'),
    'third': ('customfield_12345', 'issues[].fields.customfield_12345'),
    'fourth': ('customfield_54321', 'issues[].fields.customfield_54321[].value'),
}
JIRA = asciinator.login()


def table(jql_text):
    """Public interface in the documents to generate the table data."""
    print(asciinator.markdown_table(JIRA, jql_text, COLUMNS))
