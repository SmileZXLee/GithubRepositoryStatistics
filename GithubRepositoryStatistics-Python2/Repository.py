#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/GithubRepositoryStatistics'

class Repository :
	def __init__(self,brief,url,language,star_count,fork_count,star_url,fork_url,is_fork):
		#仓库介绍
	    self.brief = brief.replace('\r','').replace('\n','').replace('\t','').strip()
	    #仓库url
	    self.url = url
	    #仓库所使用的编程语言
	    self.language = language
	    #star数量
	    if star_count == 'None':
	    	self.star_count = '0'
	    else:
	    	self.star_count = star_count
	    self.star_count = self.star_count.replace(',','')
	    #fork数量
	    if fork_count == 'None':
	    	self.fork_count = '0'
	    else:
	    	self.fork_count = fork_count
	    self.fork_count = self.fork_count.replace(',','')
	    #star成员页面
	    self.star_url = star_url
	    #fork成员页面
	    self.fork_url = fork_url
	    #是否是fork他人的项目
	    self.is_fork = is_fork
	    #仓库的标题
	    self.title = self.url.split('/')[-1]


