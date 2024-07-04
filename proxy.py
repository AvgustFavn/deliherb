from random_open_port import random_port
from random import choice
import threading
import socket
import time
import pproxy
import requests
import asyncio
import ujson
import uvloop

assigns = {}

def shadowmere() -> dict:
    return requests.get('https://shadowmere.akiel.dev/api/sub/?format=json').json()

def repeater():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1',2501))
    server.listen(3)
    while True:
        con, addr = server.accept()
        message = ujson.dumps(list(assigns.values())).encode()
        con.send(message)
        con.close()
        time.sleep(1)

async def server(key: str):
    global assigns
    print(f'started server {key}',flush=True)
    port = await asyncio.to_thread(random_port)
    local = pproxy.Server(f'http://127.0.0.1:{port}')
    remote = pproxy.Connection(key)
    args = {'rserver' : [remote], 'verbose' : print}
    assigns[key] = port
    handler = await local.start_server(args)
    try:
        await asyncio.Event().wait()
        del assigns[key]
    except KeyboardInterrupt:
        handler.close()
        await handler.wait_closed()    

def execute(key:str):
    asyncio.run(server(key))

async def run():
    update = 0
    #listing = await asyncio.to_thread(shadowmere)
    while True:
        if int(time.time()-update) >= 600:
            listing = await asyncio.to_thread(shadowmere)
            update = time.time()
            print(f'got servers list',flush=True)
        if len(assigns) < 8:
            data:dict = choice(listing)
            key = f"ss://{data['method']}:{data['password']}@{data['server']}:{data['server_port']}"
            print(f'testing {key}',flush=True)
            if key not in assigns:
                try:
                    conn = pproxy.Connection(key)
                    reader, writer = await asyncio.wait_for(conn.tcp_connect('www.deliherb.ru', 80), timeout=5)
                    writer.write(b'GET / HTTP/1.1\r\n'
                                b'Host: www.deliherb.ru\r\n'
                                b'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                b'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36\r\n'
                                b'Accept: */*\r\n'
                                b'\r\n')
                    data = await asyncio.wait_for(reader.read(1024 * 16), timeout=9)
                    data = data.decode()
                    if "301 Moved Permanently" in data:
                        task = threading.Thread(target=execute,args=(key,))
                        task.start()
                except:
                    pass
        
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    threading.Thread(target=repeater).start()
    asyncio.run(run())
