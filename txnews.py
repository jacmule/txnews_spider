import requests
import json
import os
import time
from w3lib.html import remove_tags
from bs4 import BeautifulSoup
from setime import SeTime
from urllib.parse import urlencode
from tqdm import tqdm

class txnews_spider():
	
	def __init__(self,sy,sm,sd,ey,em,ed):
		#'Referer':'http://finance.qq.com/articleList/rolls/'
		self.headers={
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
		'Host':'roll.news.qq.com',
		'Referer':'http://finance.qq.com/articleList/rolls/'
		}
		self.base_url='http://roll.news.qq.com/interface/cpcroll.php?'
		self.params={
			'callback':'rollback',
			'mode':'1',
			'site':'sports',
			'page':'1',
			
			}
		self.columns=['finance','news','ent','sports','tech','edu','games']
		self.date=SeTime(sy,sm,sd,ey,em,ed)
		self.save_path='./result'#爬取到的新闻存储路径

	def gene_url(self,base_url,params):#生成url
		return base_url+urlencode(params)
	def seq_like_xml(self,f,title,content):
		f.write('<doc>'+'\n')
		f.write('<contenttitle>'+title+'</contenttitle>')
		f.write('\n')
		f.write('<content>'+content+'</content>'+'\n')
		f.write('</doc>'+'\n')
	def parse_urllist(self,urllist,date):
		with open(os.path.join(self.save_path,'txnews_'+date+'.txt'),'a',encoding='utf-8') as f:
			for url in tqdm(urllist):
				try:
					response=requests.get(url,timeout=15)
					if response.status_code==200:
						html=response.text
						soup=BeautifulSoup(html,'lxml')
						if soup is None:
							print(url+'   为空！！！')
							continue
						title=''
						if soup.find('div',class_='hd'):
							if soup.find('div',class_='hd').find('h1'):
								title=soup.find('div',class_='hd').find('h1').get_text()

						content=''
						if not soup.find_all('p',class_='text'):
							continue
						ps=soup.find_all('p',class_='text')
						for p in ps:
							if p:
								content+=p.get_text()
						if title and content:
							self.seq_like_xml(f,title,content)
				except Exception:
					print('解析 '+url+'时，出现异常！')
					continue

	def get_page(self):		
		for date in self.date.datelist():
			print('正在爬取'+date+'日的内容......'+'\n')
			self.params['date']=date
			for site in self.columns:
				urllist=[]
				self.params['page']='1'
				print('当前爬取栏目为：'+site)
				self.params['site']=site
				self.headers['Host']='roll.{}.qq.com'.format(site)
				self.headers['Referer']='http://{}.qq.com/articleList/rolls/'.format(site)
				url=self.gene_url(self.base_url,self.params)
				print('初次解析时的url：   '+url)
				try:
					response=requests.get(url,headers=self.headers,timeout=15)
					count=0
					if response.status_code==200:
						if len(response.text)>11:
							page_1=json.loads(response.text[9:-1])#获取第一页的内容
							if page_1.get('data'):
								result=page_1.get('data')
								count=result.get('count') #得到页数
								print(date+'日, '+site+' 栏目共有'+str(count)+'页新闻')
								for info in result.get('article_info'):
									urllist.append(info['url'])
								for i in range(2,count+1):#获取第2页及之后的内容
									self.params['page']=str(i)
									url=self.gene_url(self.base_url,self.params)
									response=requests.get(url,headers=self.headers,timeout=15)
									if response.status_code==200:
										if len(response.text)>11:
											page_n=json.loads(response.text[9:-1])#获取第一页的内容
											if page_n.get('data'):
												results=page_n.get('data')
												for info in results.get('article_info'):
													urllist.append(info['url'])
							print(str(count)+' 页共计 '+str(len(urllist))+' 条新闻')
							print('爬取进度：')
							self.parse_urllist(urllist,date)
							#可以注释掉sleep来提高爬取速度 不过不建议
							#time.sleep(30)
					else:
						print('爬取失败！无法获得页面!!')
				except Exception:
					print('解析 '+url+'时，出现异常！')
					continue

if __name__=='__main__':

	he=txnews_spider(2019,1,3,2019,1,4)#控制爬取日期区间 前者为起始年、月、日，后者为终止年、月、日
	he.get_page()
