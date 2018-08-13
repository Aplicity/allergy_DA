import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fr=pd.read_csv('init_data.csv')

# 提出年份、月份属性
year=[];month=[];day=[]
for line in fr['检测日期']:
    lineArr=line.split('-')
    year.append(lineArr[0])
    month.append(lineArr[1])
    day.append(lineArr[2])

fr['year']=year
fr['month']=month
fr['date']=day
fr['y_month']=fr['year']+ '-' +fr['month']

# 标记年龄标签
fr['label']=0
fr['label'][fr['年龄']<=12]='儿童'
fr['label'][(fr['年龄']>12)&(fr['年龄']<=24)]='青年'
fr['label'][(fr['年龄']>24)&(fr['年龄']<=60)]='中年'
fr['label'][(fr['年龄']>60)]='老年'

# 统计每个月的
fr=fr[['检测日期','性别','年龄','year','month','date','y_month','label']]
stat_year_month=fr.groupby(['year','month'])['label'].count().to_frame().reset_index()
stat_year_month['num']=stat_year_month.iloc[:,2]

df=stat_year_month.sort_values(by=['year','month'])
a=[];s=[];y_month=[]
for i in df['year']:
    a.append(str(i)+ '-')
for i in df['month']:
    s.append(str(i))
for i in range(len(s)):
    y_month.append(a[i]+s[i])

df['y_month']=y_month

plt.figure(1,figsize=(50,9))
plt.xticks(np.arange(len(y_month)),y_month)
plt.bar(y_month,df['num'])
plt.show()

plt.figure(2,figsize=(50,9))
plt.xticks(np.arange(len(y_month)),y_month)
x_len=np.arange(len(y_month))
plt.plot(x_len,df['num'])
plt.show()

# 以年份为分组统计每年的过敏人数
stat_year=df.groupby('year')['num'].sum().to_frame().reset_index()
plt.figure(3)
plt.bar(stat_year.year,stat_year.num)
plt.show()

# 以月份统计每个月的过敏人数（不同年份的数据汇总在一起）
stat_month = df.groupby('month')['num'].sum().to_frame().reset_index()
stat_month['month']=pd.to_numeric(df.month)
df=stat_month.sort_values(by='month')
plt.figure(4)
plt.xticks(np.arange(1,13))
plt.bar(df.month,df.num)
plt.show()

# 以性别为分组统计不同性别过敏人数
stat_sex = fr.groupby('性别').count().drop('未知')
stat_sex['count'] = stat_sex.iloc[:,1]
girls_num=stat_sex.loc['女']['count']
boys_num=stat_sex.loc['男']['count']
sex_num=[girls_num,boys_num]

plt.figure(5)
plt.pie(sex_num,labels=['female','male'],autopct = '%3.1f%%')
plt.axis('equal')
plt.legend()
plt.show()

# 以年龄为分组
stat_age = fr.groupby('年龄')['date'].count().to_frame().reset_index()
stat_age['count']=stat_age['date']

plt.figure(6)
plt.bar(stat_age['年龄'],stat_age['count'])
plt.show()

# 以年龄标签分组
stat_label=fr.groupby('label').sum()
sorted_stat_label=stat_label.sort_values(by='年龄')
sorted_stat_label=stat_label.sort_values(by='年龄')
x=['child','young','older','middle']
y=sorted_stat_label.iloc[:,0]

plt.figure(7)
plt.bar(x,y)
plt.show()

#不同月份下男女过敏统计人数
stat_sex_month = fr.groupby(['性别','month'])['label'].count().drop('未知').to_frame()

#不同人群下男女过敏统计人数
stat_sex_label = fr.groupby(['性别','label'])['label'].count().drop('未知').to_frame()
