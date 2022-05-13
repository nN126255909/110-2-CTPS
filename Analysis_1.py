#!/usr/bin/env python
# coding: utf-8

# In[129]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({'font.size': 14})


# In[40]:


df = pd.read_csv("ctps_0513_2.csv")
df.columns = ["ID", "實驗期間是否登入", "實驗組別", "裝置", "關掉訊息框時間", "按鈕點擊時間"]
df = df.fillna(0)
df


# In[20]:


# col_names = ["ID",  "實驗組別", "裝置", "關掉訊息框時間", "按鈕點擊時間"]
# for i in range(len(df)):
#     for n in range(len(col_names)):
#         df[col_names[n]][i] = df[col_names[n]][i][2:-1]
# df


# In[41]:


for i in range(len(df)):
    if df["關掉訊息框時間"][i]!=0: 
        df["關掉訊息框時間"][i] = df["關掉訊息框時間"][i][:10] + " " + df["關掉訊息框時間"][i][11:19]
    if df["按鈕點擊時間"][i]!=0:
        df["按鈕點擊時間"][i] = df["按鈕點擊時間"][i][:10] + " " + df["按鈕點擊時間"][i][11:19]
df


# In[46]:


df["關掉訊息框日期"] = [i[:10] if i!=0 else 0 for i in df["關掉訊息框時間"]  ]
df["關掉訊息框時間點"] = [i[11:19] if i!=0 else 0 for i in df["關掉訊息框時間"]]
df["按鈕點擊日期"] = [i[:10] if i!=0 else 0 for i in df["按鈕點擊時間"]]
df["按鈕點擊時間點"] = [i[11:19] if i!=0 else 0 for i in df["按鈕點擊時間"]]

df


# In[48]:


# df.to_csv("data_0513_v.csv", encoding='utf-8')


# ## 各組登入情況

# In[49]:


df.groupby("實驗組別")["實驗期間是否登入"].value_counts()


# In[50]:


df.value_counts("實驗期間是否登入")


# In[ ]:


df[(df["實驗組別"]=="A")&(df["實驗期間是否登入"]==True)]


# In[145]:


len(df[(df["實驗組別"]=="C")&(df["關掉訊息框時間"]!=0)])


# In[52]:


df_clickA = df[(df["實驗期間是否登入"]==True)&(df["實驗組別"]=="A")].groupby("按鈕點擊日期")["實驗組別"].count().reset_index()
df_clickB = df[(df["實驗期間是否登入"]==True)&(df["實驗組別"]=="B")].groupby("按鈕點擊日期")["實驗組別"].count().reset_index()
df_clickC = df[(df["實驗期間是否登入"]==True)&(df["實驗組別"]=="C")].groupby("按鈕點擊日期")["實驗組別"].count().reset_index()
df_clickC


# ## 不同日期的點擊按鈕人數

# In[68]:


plt.figure(figsize=(14,5))
plt.plot(df_clickA["按鈕點擊日期"][1:], df_clickA["實驗組別"][1:], label="A", color = "#6C6C6C", lw=3)
plt.plot(df_clickB["按鈕點擊日期"][1:], df_clickB["實驗組別"][1:], label="B", color = "#005AB5", lw=3)
plt.plot(df_clickC["按鈕點擊日期"][1:], df_clickC["實驗組別"][1:], label="C", color = "#F75000", lw=3)

plt.xticks(rotation="45")
plt.legend()


# ## 登入但沒點擊

# In[70]:


plt.figure(figsize=(8,5))
plt.bar(["A", "B", "C"], [df_clickA["實驗組別"][0], df_clickB["實驗組別"][0], df_clickC["實驗組別"][0]], width=0.7)


# In[139]:


lo = []
for i in range(len(df)):
    
    if (df["關掉訊息框日期"][i] == df["按鈕點擊日期"][i]) & (df["關掉訊息框日期"][i]!=0):
        lo.append(1)
    else:
        lo.append(0)
np.sum(lo)


# In[79]:


df_tw = pd.read_csv("MI_5MINS_HIST.csv", encoding= 'unicode_escape')
df_tw.columns = [ "日期","開盤指數","最高指數","最低指數","收盤指數"]

df_tw


# In[84]:


df_tw.loc[2:]


# In[93]:


tw = [16696.12,
 16408.20,16408.20,16408.20,
 16048.92,
 16061.70,
 16006.25,
 15616.68,
 15832.54]
tw


# In[80]:


len(df_clickA["按鈕點擊日期"][1:])


# In[135]:


plt.figure(figsize=(14,5))
plt.plot(df_clickA["按鈕點擊日期"][1:], df_clickA["實驗組別"][1:].cumsum(), label="A", color = "#6C6C6C", lw=3)
plt.plot(df_clickB["按鈕點擊日期"][1:], df_clickB["實驗組別"][1:].cumsum(), label="B", color = "#005AB5", lw=3)
plt.plot(df_clickC["按鈕點擊日期"][1:], df_clickC["實驗組別"][1:].cumsum(), label="C", color = "#F75000", lw=3)
# plt.plot(df_clickC["按鈕點擊日期"][1:], tw, label="tw", color = "#A23400", lw=3)

plt.xticks(rotation="45")
plt.legend()


# In[136]:


# plt.figure(figsize=(18,5))

x = df_clickA["按鈕點擊日期"][1:]
y1 = df_clickA["實驗組別"][1:].cumsum()
y2 = df_clickB["實驗組別"][1:].cumsum()
y3 = df_clickC["實驗組別"][1:].cumsum()
y4 = tw

fig = plt.figure(figsize=(18,5))

ax1 = fig.add_subplot(111)
ax1.plot(x,y1,label="A", color = "#6C6C6C", lw=3)
ax1.plot(x,y2,  label="B", color = "#005AB5", lw=3)
ax1.plot(x,y3,  label="C", color = "#F75000", lw=3)
plt.xticks(rotation="35")
plt.legend()

ax1.set_ylabel('點擊按鈕次數')

ax2 = ax1.twinx() # this is the important function
ax2.plot(x,y4, label="tw", color = "black", lw=3)
# plt.legend()


ax2.set_ylabel('大盤指數(收盤)')
# ax2.set_xlabel('大盤指數(收盤)')


plt.show()


# In[109]:


plt.figure(figsize=(14,5))
plt.plot(df_clickC["按鈕點擊日期"][1:], tw, label="tw", color = "#A23400", lw=3)
plt.xticks(rotation="45")
plt.legend()


# In[134]:


df_clickC["實驗組別"][1:].cumsum()


# In[149]:


df.head()


# In[151]:


83000*4000/9000


# In[155]:


df[(df["實驗組別"]=="C")&(df["關掉訊息框時間"]!=0)]

