from nextcloud_server import db
from datetime import datetime

class User(db.Model):
        __tablename__ = "user"
        user_id = db.Column(db.Integer,primary_key=True)
        user_name = db.Column(db.String(100))
        user_wxid = db.Column(db.String(100))
        user_createdata = db.Column(db.Date)
        user_appid = db.Column(db.String(100))
        user_sessionkey = db.Column(db.String(100))
        user_openid = db.Column(db.String(100))
        user_passwd = db.Column(db.String(100))

#class File(db.Model):
#	__tablename__ = "file"
#	flie
