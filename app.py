import xml.etree.ElementTree as ET
from models import Offer, Task
from sqlalchemy.orm import Session
from flask import Flask, Response, request, render_template, abort, redirect
from engine import engine
import hashlib

app = Flask(__name__)            

def ishash(check: str) -> bool:
    with open('creds.txt','r') as file:
        based = file.read().split('\n')
    original = hashlib.sha256(''.join(based).encode()).hexdigest()
    if original == check:
        return True

@app.post('/task')
def newtask():
    token = request.cookies.get('token')
    if token and ishash(token):
        time = request.form.get('time')
        day = request.form.get('weekday')
        try:
            if time and day:
                with Session(engine) as session:
                    task = Task(weekday=int(day),time=str(time))
                    session.add(task)
                    session.commit()
            return redirect('/')
        except:
            return newtask()
    else:
        return redirect('/login')
    
@app.post('/delete')
def deltask():
    token = request.cookies.get('token')
    if token and ishash(token):
        index = request.form.get('index')
        try:
            with Session(engine) as session:
                obj = session.query(Task).where(Task.id == index).scalar()
                session.delete(obj)
                session.commit()
            return redirect('/')
        except:
            return deltask()
    else:
        return redirect('/login')
    
    

@app.post('/login')
def dologin():
    login = request.form.get('login')
    password = request.form.get('password')
    if ishash(hashlib.sha256((str(login+password).encode())).hexdigest()):
        resp = redirect('/')
        resp.set_cookie('token',hashlib.sha256(str(login+password).encode()).hexdigest())
        return resp
    return abort(401)
    

@app.get('/login')
def relogin():
    return render_template('login.html')

@app.get('/')
def panel():
    token = request.cookies.get('token')
    if token and ishash(token):
        weekdays = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье','Каждый день']
        try:
            with Session(engine) as session:
                tasks:list[Task] = session.query(Task).all()
                tasks = [[i.id,weekdays[i.weekday],i.time] for i in tasks]
                return render_template('panel.html',tasks = tasks)
        except:
            return panel()
    else:
        return redirect('/login')

@app.get('/download')
def downloadxml():
    try:
        with Session(engine) as session:
            elements: list[Offer] = session.query(Offer).all()
            data = ET.Element('offers')
            for i in elements:
                if i.barcode != '' and i.vendorarticle != '':
                    base = ET.SubElement(data,'offer')

                    sku = ET.SubElement(base,'sku')
                    vendorarticle = ET.SubElement(base,'vendorarticle')
                    vendor = ET.SubElement(base,'vendor')
                    name = ET.SubElement(base,'name')
                    url = ET.SubElement(base,'url')
                    price = ET.SubElement(base,'price')
                    barcode = ET.SubElement(base,'barcode')
                    available = ET.SubElement(base,'available')
                    description = ET.SubElement(base,'description')
                    pictures = ET.SubElement(base,'picture')

                    url.text = str(i.url)
                    name.text = str(i.name)
                    sku.text = str(i.sku)
                    price.text = str(i.varprice)
                    available.text = str(int(bool(i.stock)))
                    barcode.text = str(i.barcode)
                    vendorarticle.text = str(i.vendorarticle)
                    vendor.text = str(i.vendor)
                    description.text = str(i.description)
                    pictures.text = str(i.images)
            resp = Response(ET.tostring(data, encoding='utf8'),mimetype='text/xml')
            resp.headers['Content-Disposition'] = 'attachment'
            return resp
    except:
        return downloadxml()
    
@app.get('/download-min')
def downloadminxml():
    try:
        with Session(engine) as session:
            elements: list[Offer] = session.query(Offer).all()
            data = ET.Element('offers')
            for i in elements:
                if i.barcode != '' and i.vendorarticle != '':
                    base = ET.SubElement(data,'offer')

                    sku = ET.SubElement(base,'sku')
                    vendorarticle = ET.SubElement(base,'vendorarticle')
                    vendor = ET.SubElement(base,'vendor')
                    name = ET.SubElement(base,'name')
                    url = ET.SubElement(base,'url')
                    price = ET.SubElement(base,'price')
                    barcode = ET.SubElement(base,'barcode')
                    available = ET.SubElement(base,'available')

                    url.text = str(i.url)
                    name.text = str(i.name)
                    sku.text = str(i.sku)
                    price.text = str(i.varprice)
                    available.text = str(int(bool(i.stock)))
                    barcode.text = str(i.barcode)
                    vendorarticle.text = str(i.vendorarticle)
                    vendor.text = str(i.vendor)
            resp = Response(ET.tostring(data, encoding='utf8'),mimetype='text/xml')
            resp.headers['Content-Disposition'] = 'attachment'
            return resp
    except:
        return downloadminxml()

@app.get('/show')
def showxml():
    try:
        with Session(engine) as session:
            elements: list[Offer] = session.query(Offer).all()
            data = ET.Element('offers')
            for i in elements:
                if i.barcode != '' and i.vendorarticle != '':
                    base = ET.SubElement(data,'offer')

                    sku = ET.SubElement(base,'sku')
                    vendorarticle = ET.SubElement(base,'vendorarticle')
                    vendor = ET.SubElement(base,'vendor')
                    name = ET.SubElement(base,'name')
                    url = ET.SubElement(base,'url')
                    price = ET.SubElement(base,'price')
                    barcode = ET.SubElement(base,'barcode')
                    available = ET.SubElement(base,'available')
                    description = ET.SubElement(base,'description')
                    pictures = ET.SubElement(base,'picture')

                    url.text = str(i.url)
                    name.text = str(i.name)
                    sku.text = str(i.sku)
                    price.text = str(i.varprice)
                    available.text = str(int(bool(i.stock)))
                    barcode.text = str(i.barcode)
                    vendorarticle.text = str(i.vendorarticle)
                    vendor.text = str(i.vendor)
                    description.text = str(i.description)
                    pictures.text = str(i.images)
            resp = Response(ET.tostring(data, encoding='utf8'),mimetype='text/xml')
            return resp
    except:
        return showxml()
    
@app.get('/show-min')
def showminxml():
    try:
        with Session(engine) as session:
            elements: list[Offer] = session.query(Offer).all()
            data = ET.Element('offers')
            for i in elements:
                if i.barcode != '' and i.vendorarticle != '':
                    base = ET.SubElement(data,'offer')

                    sku = ET.SubElement(base,'sku')
                    vendorarticle = ET.SubElement(base,'vendorarticle')
                    vendor = ET.SubElement(base,'vendor')
                    name = ET.SubElement(base,'name')
                    url = ET.SubElement(base,'url')
                    price = ET.SubElement(base,'price')
                    barcode = ET.SubElement(base,'barcode')
                    available = ET.SubElement(base,'available')

                    url.text = str(i.url)
                    name.text = str(i.name)
                    sku.text = str(i.sku)
                    price.text = str(i.varprice)
                    available.text = str(int(bool(i.stock)))
                    barcode.text = str(i.barcode)
                    vendorarticle.text = str(i.vendorarticle)
                    vendor.text = str(i.vendor)
            resp = Response(ET.tostring(data, encoding='utf8'),mimetype='text/xml')
            return resp
    except:
        return showminxml()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='2500')