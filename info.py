from glob import glob
from bs4 import BeautifulSoup
txt=glob('./result/*.txt')
print('共计'+str(len(txt))+'天的新闻')
n=0
for file in txt:
	with open(file,'r',encoding='utf-8') as f:
		docs=f.read()
		soup=BeautifulSoup(docs,'lxml')
		for doc in soup.find_all('doc'):
			n+=1
print('共计'+str(n)+'条新闻')