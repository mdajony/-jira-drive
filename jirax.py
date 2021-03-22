import csv
from jira import JIRA
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  

user = 'shahed739@gmail.com'
apikey = 'iIG9wAI7HafLxQ88L2gkFF3E'
server = 'https://ts4uwebscrapping.atlassian.net'

options = {
 'server': server
}

jira = JIRA(options, basic_auth=(user,apikey) )
jql = 'project = CORPAU AND status = Done order by created DESC'
data = jira.search_issues(jql)

with open('audit-gen.csv', mode='w') as csv_file:
    fieldnames = ['project', 'summary', 'reporter', 'status', 'timeestimate', 'timeoriginalestimate', 'aggregate progress', 'aggregate time estimate', 'aggregate time original estimate',\
                'aggregate time spent', 'assignee', 'components', 'created', 'creator', 'description',\
                'duedate', 'environment', 'fix versions', 'issue type', 'labels', 'last viewed', 'priority',\
                'percent', 'progress', 'total progress', 'resolution', 'resolutiondate',\
                'security', 'statuscategorychangedate', 'timespent', 'updated',\
                'versions', 'votes', 'watchCount', 'workratio']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for issue in data:
        print('{}: {} created_at: {} status: {}'.format(issue.key, issue.fields.summary, issue.fields.created, issue.fields.status))
        writer.writerow({
            'project': issue.fields.project,
            'summary': issue.fields.summary,
            'reporter': issue.fields.reporter,
            'status': issue.fields.status,
            'timeestimate': issue.fields.timeestimate,
            'timeoriginalestimate': issue.fields.timeoriginalestimate,
            'aggregate progress': issue.fields.aggregateprogress.progress,
            'aggregate time estimate': issue.fields.aggregatetimeestimate,
            'aggregate time original estimate': issue.fields.aggregatetimeoriginalestimate,
            'aggregate time spent': issue.fields.aggregatetimespent,
            'assignee': issue.fields.assignee,
            'components': issue.fields.components,
            'created': issue.fields.created,
            'creator': issue.fields.creator,
            'description': issue.fields.description,
            'duedate': issue.fields.duedate,
            'environment': issue.fields.environment,
            'fix versions': issue.fields.fixVersions,
            'issue type': issue.fields.issuetype,
            'last viewed': issue.fields.lastViewed,
            'priority': issue.fields.priority,
            'percent': issue.fields.progress.percent,
            'progress': issue.fields.progress.progress,
            'total progress': issue.fields.progress.total,
            'resolution': issue.fields.resolution,
            'resolutiondate': issue.fields.resolutiondate,
            'security': issue.fields.security,
            'timespent': issue.fields.timespent,
            'updated': issue.fields.updated,
            'versions': issue.fields.versions,
            'votes': issue.fields.votes,
            'watchCount': issue.fields.watches.watchCount,
            'workratio': issue.fields.workratio
        })

upload_file_list = ['audit-gen.csv']
for upload_file in upload_file_list:
	gfile = drive.CreateFile({'parents': [{'id': '159uw04c7-pr3bekSOytVm5w3R-lWrsw2'}]})
	gfile.SetContentFile(upload_file)
	gfile.Upload()

