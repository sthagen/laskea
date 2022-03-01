"""Gateway to fill in the generated tables into the documents."""
import laskea.api.jira as asciinator

__all__ = ['COLUMNS', 'table']
COLUMNS = ('Key', 'Summary', 'Third', 'Fourth')
asciinator.DEFAULT_COLUMN_FIELDS = COLUMNS
asciinator.KNOWN_CI_FIELDS = {
    'key': ('key', 'key'),
    'summary': ('summary', 'fields.summary'),
    'priority': ('priority', 'fields.priority.name'),
    'status': ('status', 'fields.status.name'),
    'third': ('customfield_12345', 'fields.customfield_12345'),
    'fourth': ('customfield_54321', 'fields.customfield_54321[].value'),
}
JIRA = asciinator.login()


def table(jql_text):
    """Public interface in the documents to generate the table data."""
    print(asciinator.markdown_table(JIRA, jql_text, COLUMNS))
