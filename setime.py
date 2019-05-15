from calendar import isleap

class SeTime():

	def __init__(self,syear=2018,smon=1,sday=1,eyear=2018,emon=1,eday=1):
		self.sdate={              #开始年、月、日
			'syear':syear,
			'smon':smon,
			'sday':sday
			}
		self.edate={              #结束年、月、日
			'eyear':eyear,
			'emon':emon,
			'eday':eday
			}
		self.days=[31,28,31,30,31,30,31,31,30,31,30,31]
	
	def datelist(self):
		'''返回一个在起止日期之间的一个日期'''
		while self.sdate['syear']<=self.edate['eyear']:#判定是否为闰年，主要确定二月天数
			if isleap(self.sdate['syear']):
				self.days[1]=29
			else:
				self.days[1]=28

			date=str(self.sdate['syear'])+'-'
			if self.sdate['smon']<10:
				date+='0'
			date+=str(self.sdate['smon'])+'-'
			if self.sdate['sday']<10:
				date+='0'
			date+=str(self.sdate['sday'])

			yield date

			if self.sdate['syear']==self.edate['eyear'] and self.sdate['smon']==self.edate['emon'] and self.sdate['sday']==self.edate['eday'] :
				break #和结束日期一样时就结束循环

			if self.sdate['sday']==self.days[self.sdate['smon']-1]:
				if self.sdate['smon']==12:
					self.sdate['syear']+=1
					self.sdate['smon']=1
					self.sdate['sday']=1
				else:
					self.sdate['smon']+=1
					self.sdate['sday']=1
			else:
				self.sdate['sday']+=1
