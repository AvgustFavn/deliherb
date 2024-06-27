import sqlalchemy as db
import os

basedir = os.getcwd()
engine = db.create_engine(url=f'mysql+pymysql://root:root@127.0.0.1:3306/offers')