import urllib2  # the lib that handles the url stuff
import re
import os

def get_all_phone_models_html():
    count=0
    with open("C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/urls_brands.txt") as f:
      for myurls in f:
        count=count+1
        myurls=myurls.split("*",2)
        model=myurls[0] #it's not using now.Because i don't need each brand category
        data = urllib2.urlopen(str(myurls[1]))
        to_file = "C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/Pages/" + str(count) + ".txt"
        f = open(str(to_file), 'a')
        for line in data: #get urls
            f.write(line)
        extract_phones()
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return [s[start:end],start,end]
    except ValueError:
        return ""
def count_files(dir):
    list = os.listdir(dir) # dir is your directory path
    return  len(list)


def extract_phones():
  count_directory=count_files("C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/Pages/")
  #for i in range(1,count_directory):
  pr_dir="C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/Pages/"+str(count_directory)+".txt"
  print(pr_dir)
  with open(str(pr_dir)) as f:
            for i in f:
              start = tstart = 0
              if find_between(i, "title", "Announced" ) !="":
                  end=len(i)
                  count = len(re.findall(r'\w+', i))
                  for k in range(int(count)):
                    try:
                        text,start,end=find_between(i[start:end], 'title="', "Announced")
                        start=tstart+end
                        tstart=start
                        openfile = open('C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/phones.txt', 'a')
                        openfile.write(text.replace(".","")+"\n")
                        end = len(i)
                    except:
                     pass
def get_brands():
    url='http://www.gsmarena.com/makers.php3'
    data = urllib2.urlopen(str(url)) # it's a file like object and works just like a file
    for line in data: # files are iterable                        f-1-0-p2.php
        f = open('C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/brands.txt', 'a')
        f.write(line)
def extract_brands():
    with open("C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/brands.txt") as f:
            for i in f:
              print(i)
              start = tstart = 0
              if find_between(i, "<td><a href=", ".php>" ) !="":
                  end=len(i)
                  count = len(re.findall(r'\w+', i))
                  for k in range(int(count)):
                    try:
                        text,start,end=find_between(i[start:end], "<td><a href=", ".php>")
                        start=tstart+end
                        tstart=start
                        end = len(i)
                        openfile = open('C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/clean_brands.txt', 'a')
                        openfile.write(text+"\n")
                    except:
                     pass
def prepare_brands_urls():
    with open("C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/clean_brands.txt") as f:
        for i in f:
            print(i)
            for j in range(2,14):
                splitted=i.split("-phones-",2)
                suburl=str(splitted[0])+"*http://www.gsmarena.com/"+splitted[0]+"-phones-f-"+splitted[1].replace("\n","")+"-0-p"+str(j)+".php"
                k = open('C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/urls_brands.txt', 'a')
                k.write(suburl + "\n")
            baseurl = str(splitted[0])+"*http://www.gsmarena.com/" + str(i.replace("\n", "")) + ".php"
            k.write(baseurl + "\n")

def get_phone_name():
    return 'C:/Users/asus/Documents/Bireysel Projeler/Sahibinden/Objeler/phones.txt'

#get_brands()
#extract_brands()
#prepare_brands_urls()
#get_all_phone_models_html()
#extract_phones()
