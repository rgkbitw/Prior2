import urllib.parse as par
import json
from utils import *
import csv
import pandas as pd
import pickle

language = 'cpp'
df = pd.read_csv(language + '.csv')
df = df[df['open_issues_count'] > 30]
base_url = 'https://api.github.com/repos/dotnet/roslyn/issues'
issues = []; labels = []
data_dir = 'data/'

for i in range(len(df)):
	print('Repo {}/{}'.format(i+1, len(df)))
	base_url = df.iloc[i]['issues_url'][:-9]
	url = base_url + '?' + par.urlencode(issue_params)
	page = 1

	while url is not None:
		iss, ls, url, n_pages = getIssueData(url)
		issues += iss; labels += ls
		print('[Page {}/{}]'.format(page, n_pages))
		page += 1
		# print('Next url: [{}]'.format(url))
		# url = None

issues_df = pd.DataFrame(issues)
without_title_body = issues_df.drop(columns = ['body', 'issue_title'])
without_title_body.to_csv(data_dir + language + '_issues.csv')
with open(data_dir + language + '_issues.pickle', 'wb') as f:
	pickle.dump(issues, f)

if labels != []:
	labels_df = pd.DataFrame(labels)
	labels_df.to_csv(data_dir + language + '_labels.csv')
	with open(data_dir + language + '_labels.pickle', 'wb') as f:
		pickle.dump(labels, f)
else:
	print('No labels found.')

print('Written to file.')
