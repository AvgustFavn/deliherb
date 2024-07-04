from models import Offer
from random import choice
from fake_useragent import FakeUserAgent
from sqlalchemy.orm import Session
from engine import engine
import requests as rs
from bs4 import BeautifulSoup
import threading
import socket
import ujson
import time
import re
import traceback
from http import cookiejar
from random import uniform

class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

ports = []
links = []
overflow = 0

requests = rs.Session()
requests.cookies.set_policy(BlockAll())

def getdescription(soup: BeautifulSoup) -> str:
    result = []
    i: BeautifulSoup
    for i in soup.find_all('div',class_='col-xs-24'):
        temp = [i for i in str(i).strip().split('\n') if i != '']
        result.append('\n'.join(temp))
    return ''.join(result)
    
def getimages(soup: BeautifulSoup) -> str:
    result = []
    i: BeautifulSoup
    for i in soup.find_all('div',class_='carousel__slide imgvisible',attrs={'data-fancybox':'gallery','data-src':True}):
        result.append(i.get('data-src'))
    return ','.join(result)
    

def randproxy() -> str:
    global ports
    return str(choice(ports))

def getinfo(url:str) -> dict:
    start = time.time()
    while True:
        try:
            if int(time.time() - start) >= 300:
                return False
            proxy = randproxy()
            
            proxies = {
                "http"  : 'http://127.0.0.1:'+proxy,
                "https" : 'http://127.0.0.1:'+proxy
                }
            r = requests.get(url=url,proxies=proxies,headers={'User-Agent': FakeUserAgent(os=['windows']).chrome,'Referer':'https:/yandex.ru/'},timeout=9)
            soup = BeautifulSoup(r.text,'html.parser')
            
            sku = soup.find('h1',attrs={'itemprop':'name','data-product':True})
            if sku:
                sku = sku['data-product']
            else:
                sku = ''
            
            name = soup.find('meta',attrs={'itemprop':'name'})
            if name:
                name = name['content']
            else:
                name = ''
                
            stock = soup.find('meta',attrs={'itemprop':'availability'})
            if stock and stock['content'] == 'InStock' :
                stock = True
            else:
                stock = False
            
            vendor = soup.find('a',class_='nonelink',attrs={'title':True,'href':True})
            if vendor:
                vendor = vendor['title']
            else:
                vendor = ''
            
            vendorarticle = soup.find('meta',attrs={'itemprop':'sku'})
            if vendorarticle:
                vendorarticle = vendorarticle['content']
            else:
                vendorarticle = ''
            
            varprice = soup.find('span',class_='price')
            if varprice:
                    varprice = int(varprice.text.replace(' ',''))
            else:
                varprice = 0
            
            cprice = varprice
            
            barcode = soup.find('label',class_='lfeature',attrs={'id':re.compile('product_.*?_feature_102')})
            if barcode:
                barcode = barcode.text
            else:
                barcode = ''
                
            imgs = getimages(soup)
            desc = getdescription(soup)
            print(f'in {time.time() - start} sec ended Thread with {url}',flush=True)
            if sku:
                return url,name,sku,stock,varprice,cprice,barcode,vendor,vendorarticle,imgs,desc
            else:
                raise Exception('No sku found')
        except:
            pass
            
def newinfo(url:str) -> None:
    global overflow
    overflow += 1
    while True:
        try:
            info = getinfo(url=url)
            if info == False:
                return None

            with Session(engine) as session:
                of: Offer = session.query(Offer).where(Offer.url == info[0]).scalar()
                if of:
                    of.name = info[1]
                    of.sku = info[2]
                    of.stock = info[3]
                    of.varprice = info[4]
                    of.cprice = info[5]
                    of.barcode = info[6]
                    of.vendor = info[7]
                    of.vendorarticle = info[8]
                    of.images = info[9]
                    of.description = info[10]
                else:
                    offer = Offer(url = info[0], name= info[1], sku = info[2], stock = info[3], varprice = info[4], cprice = info[5], barcode = info[6], vendor = info[7], vendorarticle = info[8], images = info[9], description = info[10])
                    session.add(offer)
                print(info,flush=True)
                session.commit()
                overflow-=1
                return None
        except Exception:
            # print(traceback.format_exc(),flush=True)
            # print(url,flush=True)
            newinfo(url)

def runinfo() -> None:
    global overflow
    global links
    maxlen = len(links)
    while len(links) != 0:
        if overflow < 12:
            link = str(links.pop())
            threading.Thread(target=newinfo,args=(link,)).start()
            print(f'starting Thread with: {link}',flush=True)
            print(f'products completed: {maxlen-len(links)}/{maxlen}',flush=True)
        time.sleep(uniform(0.15,1.5))
    
def getlinks():
    print('started links collection',flush=True)
    global links
    r = requests.get('https://deliherb.ru/sitemap.xml')
    soup = BeautifulSoup(r.text,'xml')
    
    products = [i.text for i in soup.find_all('loc') if '/products/' in i.text]
    links = products
    print(len(links),flush=True)

def getbadlinks():
    global links
    try:
        with Session(engine) as session:
            urls = session.query(Offer.url).where(Offer.barcode == '').all()
            links = urls
            print(len(links),flush=True)
    except:
        getbadlinks()

def getports():
    global ports
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1',2501))
            data = client.recv(4096)
            ports = ujson.loads(data.decode())
            client.close()
            print(f'known ports: {ports}')
            time.sleep(1)
        except Exception:
            # print(traceback.print_exc())
            getports()

            
        