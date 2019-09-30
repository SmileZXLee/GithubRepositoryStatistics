#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/GithubRepositoryStatistics'
import HttpReq
from lxml import etree
from Repository import Repository
import platform
import re
import sys
import os
import platform

#当前是第几页
page = 0

#是否是Windows
os_is_windows = platform.system() == 'Windows'

#根据系统获取raw_input中文编码结果
def gbk_encode(str):
	if os_is_windows:
		return str.decode('utf-8').encode('gbk')
	else:
		return str

# 获取仓库信息，返回Repository对象列表
def get_repositories(username,r_next_url,res_list):
	target_url = 'https://github.com/%s?tab=repositories'%(username)
	if len(r_next_url):
		target_url = r_next_url
	res = HttpReq.send_req(target_url,'','','GET')
	if 'You have triggered an abuse detection mechanism.' in res:
		print('您已经触发了滥用检测机制，请稍等几分钟再试')
		return res_list
	root = etree.HTML(res)
	repositorty_base_items = root.xpath('//li')
	for repositorty_base_item in repositorty_base_items:
		#每一个仓库的html
		a_list = []
		p_list = []
		language_list = []
		star_count_list = []
		fork_count_list = []
		star_url_list = []
		fork_url_list = []
		root_html = etree.tostring(repositorty_base_item)
		sub_root = etree.HTML(root_html)
		#print(etree.tostring(repositorty_base_item))
		sub_root_a_items = sub_root.xpath('//div/div/h3/a/@href')
		for sub_root_a_item in sub_root_a_items:
			a_list.append(sub_root_a_item)

		sub_root_p_items = sub_root.xpath('//div/div/p')
		for sub_root_p_item in sub_root_p_items:
			p_list.append(sub_root_p_item.text)

		sub_root_language_items = sub_root.xpath('//div/div/span/span[@itemprop="programmingLanguage"]')
		for sub_root_language_item in sub_root_language_items:
			language_list.append(sub_root_language_item.text)

		sub_root_star_fork_items = sub_root.xpath('//div/div/a')
		for sub_root_star_fork_item in sub_root_star_fork_items:
			r_html_str = etree.tostring(sub_root_star_fork_item)
			r_html_str = r_html_str.replace('\r','').replace('\n','').replace('\t','')
			if('svg aria-label="star"' in r_html_str):
				rec_count = re.compile(r'</svg>(.*?)</a>')
				c_count_res=rec_count.findall(r_html_str)
				if len(c_count_res):
					c_str = c_count_res[0]
					c_str = c_str.replace(' ','')
					star_count_list.append(c_str)
				rec_url = re.compile(r'href="(.*?)>')
				c_url_res=rec_url.findall(r_html_str)
				if len(c_url_res):
					c_str = c_url_res[0]
					c_str = c_str.replace(' ','')
					star_url_list.append(c_str)

			if('svg aria-label="fork"' in r_html_str):
				rec_count = re.compile(r'</svg>(.*?)</a>')
				c_count_res=rec_count.findall(r_html_str)
				if len(c_count_res):
					c_str = c_count_res[0]
					c_str = c_str.replace(' ','')
					fork_count_list.append(c_str)
				rec_url = re.compile(r'href="(.*?)>')
				c_url_res=rec_url.findall(r_html_str)
				if len(c_url_res):
					c_str = c_url_res[0]
					c_str = c_str.replace(' ','')
		
					fork_url_list.append(c_str)
		if(len(a_list)):
			is_fork = 'Forked from' in root_html
			repository = Repository(get_value(p_list),get_value(a_list),get_value(language_list),get_value(star_count_list),get_value(fork_count_list),get_value(star_url_list),get_value(fork_url_list),is_fork)
			res_list.append(repository)
				

	#获取下一页的地址
	res_next_url = ''
	c_next_url = re.compile(r'btn btn-outline BtnGroup-item(.*?)>')
	next_urls = c_next_url.findall(res)
	for next_url in next_urls:
		if 'tab=repositories' in next_url:
			res_next_url = next_url.replace(' href="','').replace('"','')
	if len(res_next_url):
		if 'after=' in res_next_url:
			global page
			page = page + 1
			#print(u'开始获取第%d页数据...'%(page + 1))
			get_repositories(username,res_next_url,res_list)

	return res_list

# 打印用户统计信息
def get_info(username):
	print(u'正在获取%s的统计信息...'%(username))
	res = get_repositories(username,'',[])
	if not len(res):
		print(u'此用户未创建任何仓库')
		return
	star_count = get_all_stars(username,res)
	fork_count = get_all_forks(username,res)
	repository_count = get_repository_counts(username,res)
	own_repository_count = get_own_repository_counts(username,res)
	max_start_repository = get_max_star_repository(username,res)
	if max_start_repository == None:
		print(u'此用户未创建任何仓库')
		return
	print(u'%s的仓库总数为%d，非fork其他用户的仓库数为%d，被Star总数为%d，被Fork总数为%d;\r\n其中被Start数最高的为[%s](%s)共获得%s个Star'%(username,repository_count,own_repository_count,star_count,fork_count,max_start_repository.title,max_start_repository.brief,max_start_repository.star_count))

# 获取用户被star总数
def get_all_stars(username,*args):
	if(len(args)):
		res = args[0]
	else:
		res = get_repositories(username,'',[])
	star_count = 0
	for data in res:
		if not data.is_fork:
			star_count = star_count + int(data.star_count)
	return star_count

# 获取用户被fork总数
def get_all_forks(username,*args):
	if(len(args)):
		res = args[0]
	else:
		res = get_repositories(username,'',[])
	fork_count = 0
	for data in res:
		if not data.is_fork:
			fork_count = fork_count + int(data.fork_count)
	return fork_count

# 获取用户所有仓库总数
def get_repository_counts(username,*args):
	if(len(args)):
		res = args[0]
	else:
		res = get_repositories(username,'',[])
	return len(res)

# 获取用户自主创建仓库总数
def get_own_repository_counts(username,*args):
	if(len(args)):
		res = args[0]
	else:
		res = get_repositories(username,'',[])
	own_repository_count = 0
	for data in res:
		if not data.is_fork:
			own_repository_count = own_repository_count + 1
	return own_repository_count

# 获取用户被star数最高的仓库，返回Repository对象
def get_max_star_repository(username,*args):
	if(len(args)):
		res = args[0]
	else:
		res = get_repositories(username,'',[])
	rep = None
	max_count = 0;
	for data in res:
		if not data.is_fork:
			if int(data.star_count) >= max_count:
				max_count = int(data.star_count)
				rep = data
	return rep

# 处理数组元素
def get_value(arr):
	if len(arr):
		return arr[0]
	return 'None'

# 程序入口，开始程序
def start():
	while(True):
		usernames = get_username()
		break_flag = False
		for username in usernames:
			if(username == 'Q'):
				break_flag = True
				break
			get_info(username)
		if break_flag:
			break
		
# 获取输入的用户信息
def get_username():
	username = raw_input(gbk_encode('请输入Github用户名，多个用户名用#隔开(输入Q退出): ')).decode(sys.stdin.encoding)
	return username.split('#')

if __name__ == '__main__':
	start()

