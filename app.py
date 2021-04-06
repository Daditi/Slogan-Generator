from flask import Flask, render_template,request
app = Flask(__name__) #creating the Flask class object   
from gensim.summarization import keywords
import pandas as pd
import re
import urllib.request
import bs4 as bs

ws=[]
sauce=urllib.request.urlopen("https://sixads.net/blog/powerful-call-to-action-phrases/")
soup=bs.BeautifulSoup(sauce,"lxml")
for i in soup.find_all('span',class_="ez-toc-section"):
    ws.append(i.string)
ws=ws[9:-1]
wsf=[]
for i in ws:
    l,t=i.split(" ",1)
    wsf.append(t)
print(wsf)

@app.route('/') 
def index():
    return render_template('index.html')  

@app.route('/final',methods=['POST','GET'])
def final():
    v=request.form["speechToText"]
    t=request.form["cta"]
    text=v.lower()
    keys=keywords(text, words=3)
    keys=re.split(" ", keys)
    print(keys)
    li=pd.read_csv(r"C:\Users\Dell\aditi\anaconda-jupyter-notebooks\MHSCC#Hackathon\ifp.csv")
    cta=t
    keyword = keys
    print(keyword)
    l=[list(li["CTA"]),list(li["Keywords"]),list(li["Statements"])]
    result=[]
    for i in range(len(li["CTA"])):
        if(l[0][i]==cta.lower()):
            temp=l[1][i].split(",")
            t1=set(keyword)
            t2=set(temp)
            if(t1.intersection(t2)):
                result.append(l[2][i])
    for i in wsf:
        text=i.lower()
        keys1=keywords(text, words=3)
        keys1=keys1.replace("\n"," ")
        keys1=re.split(" ", keys1)
        t1=set(keys1)
        t2=set(keyword)
        if(t1.intersection(t2)):
                result.append(i)

    for i in result:
        print(i)
    length=len(v)
    return render_template('index.html',v=result,length=length)   

if __name__ =='__main__':  
    app.run(debug = True)  