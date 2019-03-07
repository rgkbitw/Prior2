import urllib.request as req
import urllib.parse as par
import json
import re

params = {'per_page':100,'access_token':'333e47550eefd347b65b295bf08085f627949737'}
issue_params = dict(params); issue_params.update({'state':'all'})

def nextLink(headers):
    links = re.findall(r'<(.+?)>', headers)
    pointers = re.findall(r'rel=\"(\S+)\"', headers)
    limit = re.findall(r'X-RateLimit-Remaining: (\d+)', headers)
    return links, pointers, limit

def getDnH(url):
    connection = req.urlopen(url)
    headers = str(connection.info())
    data = connection.read().decode()
    return headers, data

# new params with 'state' as key must be passed
def getNumClosed(url):
    url = url[:-9]
    url += '?' + par.urlencode(issue_params)
    h, d = getDnH(url)
    ls, ps, lms = nextLink(h)
    print('---- Per hour left', format(int(lms[0])), '----')
    if 'last' in ps:
        ind = ps.index('last')
        n_pages = int(ls[ind][ls[ind].rfind('&')+6:])
        closed_issues = (n_pages - 1) * 100
        h, d  = getDnH(ls[ind])
        js = json.loads(d)
        closed_issues += len(js)
    else:
        closed_issues = len(json.loads(d))
    return closed_issues

def isBug(title, labels):
    label_str = ''
    for l in labels:
        label_str += l['name'] + ' '
    label_str += ' ' + title
    if 'bug' in label_str:
        return True
    else:
        return False

def getRepoData(repos_url):
    repo_data = []
    headers, data = getDnH(repos_url)
    links, pointers, limit = nextLink(headers)
    print('---- Per minute left', int(limit[0]), '----')
    if 'next' in pointers:
        ind = pointers.index('next')
        next_link = links[ind]
    else:
        next_link = None

    keys = ['id', 'full_name', 'url', 'forks_count',
            'stargazers_count', 'watchers_count',
            'language', 'open_issues_count', 'issues_url',
            'issue_events_url', 'issue_comment_url']

    js = json.loads(data)
    for i, repo in enumerate(js['items']):
        print('Repo {}/{}'.format(i+1, len(js['items'])))
        repo_dict = {}
        for k in keys:
            repo_dict[k] = repo[k]

        # getting number of closed issues
        # print('Getting closed issues..')
        # nc = getNumClosed(repo_dict['issues_url'])
        # repo_dict['closed_issues_count'] = nc
        repo_data.append(repo_dict)

    return repo_data, next_link, js['total_count']

def getIssueData(issue_url):
    h, d = getDnH(issue_url)
    links, pointers, limit = nextLink(h)
    print('---- Per hour left', int(limit[0]), '----')
    if 'next' in pointers:
        ind = pointers.index('next')
        next_link = links[ind]
    else:
        next_link = None
    if 'last' in pointers:
        ind = pointers.index('last')
        n_pages = int(links[ind][links[ind].rfind('&')+6:])
    else:
        n_pages = -1
    keys = ['id', 'number', 'url', 'title', 'state',
            'comments', 'created_at', 'author_association',
            'body', 'events_url']
    js = json.loads(d)
    issues = []; labels = []
    for i, issue in enumerate(js):
        print('Issue {}/{}'.format(i+1, len(js)))
        issue_dict = {}
        for k in keys:
            if k in ['id', 'number', 'title', 'url']:
                issue_dict['issue_' + k] = issue[k]
            else:
                issue_dict[k] = issue[k]
        # adding user details for further analysis
        issue_dict['user_id'] = issue['user']['id']
        issue_dict['user_login'] = issue['user']['login']
        issue_dict['user_url'] = issue['user']['url']
        issue_dict['nAssignees'] = len(issue['assignees'])
        if 'pull_request' in issue:
            issue_dict['isPr'] = True
        else:
            issue_dict['isPr'] = False
        if 'closed_at' in issue:
            issue_dict['closed_at'] = issue['closed_at']
        else:
            issue_dict['closed_at'] = None
        issue_dict['isBug'] = isBug(issue['title'], issue['labels'])
        issues.append(issue_dict)

        # Labels
        if len(issue['labels']) > 0:
            for l in issue['labels']:
                label_dict = {}
                label_dict['issue_id'] = issue_dict['issue_id']
                label_dict['issue_url'] = issue_dict['issue_url']
                label_dict['issue_number'] = issue_dict['issue_number']
                label_dict['label_id'] = l['id']
                label_dict['label_name'] = l['name']
            labels.append(label_dict)

    return issues, labels, next_link, n_pages
