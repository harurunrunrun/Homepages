import requests
from bs4 import BeautifulSoup

def update_and_save(url):
  r=requests.get(url)
  soup=BeautifulSoup(r.text,"html.parser")

  title=[i for i in soup.find_all("h3") if "No." in str(i)][0]

  elems=soup.find_all("div",class_="block")

  filename=str(title.text).replace(" ","_").replace(".","-")+".html"

  with open(filename,mode="w",encoding="utf-8") as f:
    f.write(str(title)+"\n")
    for i in elems:
      f.write(str(i)+"\n")
    f.write("<p>source: <a href=\""+url+"\">"+str(title.text)+"</a></p>\n")
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
      filename,title=update_and_save(url)
      files.append([filename,title])
  make_mirror(files)
  return


get_urls()

