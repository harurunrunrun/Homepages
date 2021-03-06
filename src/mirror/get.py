import requests
from bs4 import BeautifulSoup
import time
import datetime

def get_date():
  dt_now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
  return str(dt_now.year)+"/"+str(dt_now.month)+"/"+str(dt_now.day)+"  "+str(dt_now.hour)+":"+str(dt_now.minute)+":"+str(dt_now.second)

def update_and_save(url):
  date=get_date()
  r=requests.get(url)
  soup=BeautifulSoup(r.text,"html.parser")

  title=[i for i in soup.find_all("h3") if "No." in str(i)][0]

  elems=soup.find_all("div",class_="block")

  filename=str(title.text).replace(" ","_").replace(".","-")+".html"

  with open(filename,mode="w",encoding="utf-8") as f:
    f.write("<script>\nMathJax={chtml:{matchFontHeight: false},tex:{inlineMath: [['$', '$']]}};</script>\n<script id=\"MathJax-script\" async  src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js\"></script>\n")
    f.write(str(title)+"\n")
    flag=False
    for i in elems:
      lines=str(i).split("\n")
      for line in lines:
        tmp=line
        if "<pre>" in tmp:
          tmp=tmp.replace("<pre>","<p>")
          flag=True
        if "</pre>" in tmp:
          tmp=tmp.replace("</pre>","</p>")
          flag=False
        if flag:
          f.write(tmp+"</p>\n<p>")
        else:
          f.write(tmp+"\n")
    f.write("<p>source: <a href=\""+url+"\">"+str(title.text)+"</a></p>\n")
    f.write("<p>最終更新日: "+date+"</p>\n")
  return filename,str(title.text)



def make_mirror(files):
  with open("mirror.html",mode="w",encoding="utf-8")as f:
    f.write("<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n<title>mirror</title>\n</head>\n<body>\n<br><br>\n<ul>\n")
    for file_,title in files:
      f.write("<li><p><a href=\""+file_+"\">"+title+"</a></p></li>\n")
    f.write("</ul>\n</body>\n</html>\n")
  return

def get_urls():
  r=requests.get("https://yukicoder.me/users/11617/problems")
  soup=BeautifulSoup(r.text,"html.parser")
  links=soup.find_all("a")
  files=[]
  for link in links:
    tmp=str(link.get("href"))
    if "/problems/no/" in tmp:
      url="https://yukicoder.me"+tmp
      start=time.time()
      filename,title=update_and_save(url)
      end=time.time()
      time.sleep(1-min(1,end-start))
      files.append([filename,title])
  make_mirror(files)
  return


get_urls()

