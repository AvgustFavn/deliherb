import requests
import bs4
from lookup import getdescription,getinfo,getports
import ujson
import threading
threading.Thread(target=getports).start()
r = getinfo('https://deliherb.ru/products/alr-industries-chain-d-out-lemon-lime-10-58-oz-300-g')
print(r[10])