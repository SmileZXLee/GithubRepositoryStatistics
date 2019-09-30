#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/GithubRepositoryStatistics'
import requests
from requests.cookies import RequestsCookieJar
session = requests.Session()
token = ''
def send_req(url,headers,data,post_type):
	org_headers = {
		'Referer': 'https://github.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Host': 'github.com'
	}
	if not token == '':
		data['token'] = token
	final_headers = org_headers.copy()
	if headers :
		final_headers.update(headers)
	if post_type.upper() == 'POST':
		res = session.post(url,data=data,headers=final_headers)
	elif post_type.upper() == 'PUT':
		res = session.put(url,data=data,headers=final_headers)
	elif post_type.upper() == 'GET':
		res = session.get(url,headers=final_headers)
	else:
		print('TypeErr')
	return res.text

def save_token(new_token):
	token = new_token



