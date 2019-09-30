# GithubRepositoryStatistics
### 使用方法
#### 安装必要的包
```
pip install requests
```
```
pip install lxml
```
#### cd到项目文件夹下执行python Statistics.py
***

### 主要功能
* 获取仓库信息，返回Repository对象列表
```python
get_repositories(username,'',[])
```
* 获取用户所有仓库被star总数(不包括fork他人的仓库)
```python
get_all_stars(username)
```
* 获取用户所有仓库被fork总数(不包括fork他人的仓库)
```python
get_all_forks(username)
```
* 获取用户所有仓库总数
```python
get_repository_counts(username)
```
* 获取用户自主创建仓库总数
```python
get_own_repository_counts(username)
```
* 获取用户被star数最高的仓库，返回Repository对象
```python
get_max_star_repository(username)
```
* 用户仓库详细信息
```python
#仓库标题
repository.title
#仓库介绍
repository.brief
#仓库url
repository.url
#仓库所使用的编程语言
repository.language
#star数量
repository.star
#fork数量
repository.fork
#star这个项目的所有成员页面
repository.star_url
#fork这个项目的所有成员页面
repository.fork_url
#是否是fork他人的项目
repository.is_fork
```
### 预览
![Image text](http://www.zxlee.cn/GithubRepositoryStatisticsDemo.png)
