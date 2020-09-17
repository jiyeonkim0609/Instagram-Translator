import http.server
import socketserver

handler=http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(('',8080), handler) as httpd:
    print('Server listening on port 8080...')
    httpd.serve_forever()
    
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from urllib.parse import quote_plus
import time
import re

from flask import Flask, render_template, request, url_for
app = Flask(__name__)

#키워드 가져오기
@app.route('/')
def main_get(text=None):
    return render_template('index.html', text=text)

@app.route('/image',methods=['GET'])
def image(text=None):
    myList=[]
    if request.method == 'GET':
        temp = request.args.get('jiyeon')
        split_temp = re.split('\W+',temp)
        if(split_temp[len(split_temp)-1]==''):
            split_temp.pop()
        for i in range(0,len(split_temp)):
            print("split_temp: "+split_temp[i]+"       ")
            baseUrl = 'https://www.instagram.com/explore/tags/'
            plusUrl = split_temp[i]
            print("   "+split_temp[i]+"    ")
            url = baseUrl + quote_plus(plusUrl)
            driver = webdriver.Chrome("c:/Users/김지연/inscrawler/bin/chromedriver/chromedriver.exe")
            driver.get(url)

            html = driver.page_source
            soup = bs(html, "html.parser")

            insta = soup.select('.v1Nh3.kIKUG._bz0w')

            #if '.v1Nh3.kIKUG._bz0w' == None :
            #    print('errorimg.jpg')
            #    myList.append('errorimg.jpg')

            #else :
            print(insta[0])
            n = 1
            print('https://www.instagram.com' + insta[0].a['href'])
            imgUrl = insta[0].select_one('.KL4Bh').img['src']
            with urlopen(imgUrl) as f:
                with open('./img/' + plusUrl + '.jpg','wb') as h:
                    img = f.read()
                    h.write(img)
            print(imgUrl)
            print()
            myList.append(imgUrl)
            driver.close()


        return render_template('index.html', myList=myList)

if __name__ == '__main__':
    app.run
