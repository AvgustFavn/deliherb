from uuid import uuid4
import sqlalchemy as db
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.mysql import TEXT,MEDIUMTEXT

class Base(DeclarativeBase):
    pass

class Offer(Base):
    __tablename__ = 'offers'
    
    url = db.Column(db.String(256),primary_key=True)
    sku = db.Column(db.String(256))
    name = db.Column(db.String(256))
    varprice = db.Column(db.Integer())
    cprice = db.Column(db.Integer())
    stock = db.Column(db.Boolean())
    barcode = db.Column(db.String(256))
    vendor = db.Column(db.String(256))
    vendorarticle = db.Column(db.String(256))
    description = db.Column(MEDIUMTEXT())
    images = db.Column(TEXT())
    

class Task(Base):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer(),autoincrement=True,primary_key=True)
    weekday = db.Column(db.Integer())
    time = db.Column(db.String(256))
    
if __name__ == "__main__":
    from engine import engine
    Base.metadata.create_all(engine)