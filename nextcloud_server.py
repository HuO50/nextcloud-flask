# -*- coding:UTF-8 -*-
from flask import Flask, request, redirect, url_for, send_from_directory,session,render_template, jsonify
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wxapp import WXApp
#from webdav import getfilelist,getsubfilelist,getspecificfilelist,uploadfile,deletefile,UserOperation
from webdav import *
import os
import flask
import base64
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

UPLOAD_FOLDER = '/data/nextcloud/files/uploadfile'
DOWNLOAD_FOLDER = '/data/nextcloud/files/downloadfile'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

SESSION_TYPE = 'redis'

nextcloud_server = Flask(__name__)
Session(nextcloud_server)
nextcloud_server.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
nextcloud_server.config['DOWNLOAD_FOLDER']=DOWNLOAD_FOLDER
nextcloud_server.config['MAX_CONTENT_LENGTH']=16*1024*1024
nextcloud_server.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost:3306/nextcloud?charset=utf8"

nextcloud_server.config['WX_APPID'] = 'wx0d086fd72142e36a'
nextcloud_server.config['WX_SECRET'] = '3532e548bc867aef427eb27e2ea2816b'
nextcloud_server.config['SESSION_KEY'] = ''
nextcloud_server.secret_key='\xf1\x92Y\xdf\x8ejY\x04\x96\xb4V\x88\xfb\xfc\xb5\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'


db = SQLAlchemy(nextcloud_server)
wxapp = WXApp()
wxapp.init_app(nextcloud_server)

class User(db.Model):
	__tablename__ = "user"
	user_id = db.Column(db.Integer,primary_key=True)
	user_name = db.Column(db.String(100))
	user_openid = db.Column(db.String(100))
	user_passwd = db.Column(db.String(100))
	def __init__(self,username,useropenid,userpasswd):
		self.user_name = username
		self.user_openid = useropenid
		self.user_passwd = userpasswd
	def __repr__(self):
		return '<User %r>' % self.user_name

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@nextcloud_server.route("/api/test")
def helloworld():
	return "hello world!"

@nextcloud_server.route("/api/login",methods=['GET','POST'])
def nextcloudLogin():
	js_code = request.values.get('code')
	result = wxapp.jscode2session(js_code)
	print result
	#print result['openid']
	#print result['session_key']
	with open('./session_key','w') as f:
		f.writelines(result['session_key'])
	f.close()
	#query user
	queryUserResult = User.query.filter_by(user_openid=result['openid']).first()
	if queryUserResult is None:
		print "no register"
		return jsonify({'code':201,'data':"No this user"})
	else:
		print "registered"
		getfilelist = get_filelist(queryUserResult.user_name,queryUserResult.user_passwd)
		return jsonify({'code':200,'username':queryUserResult.user_name,'data':getfilelist})

@nextcloud_server.route("/api/getuserinfo",methods=['POST'])
def getUserInfo():
#	encryptedData = request.form['encryptedData']
#	print encryptedData
	req_data = request.get_json()
	print req_data
	encryptedData = req_data['encryptedData']
	print encryptedData
	iv = req_data['iv']
	print iv
#	code = request.values.get('code')
	#decrythe code
	with open("./session_key","r") as f:
		session_key = f.readline()
	f.close()
	result = wxapp.decrypt(session_key, encryptedData, iv)	
	print result
        username = create_random_username()
#	checkuser = User.query.filter_by(username=username).first()
#	if checkuser == None:
        defaultpasswd = "Dis@init7"
       	newUser = User(username,result['openId'],defaultpasswd)
       	db.session.add(newUser)
       	db.session.commit()
       	createNextcloudUser = UserOperation()
       	createUserResult = createNextcloudUserResult = createNextcloudUser.createuser(username,defaultpasswd)
       	getfilelist = get_filelist(username,defaultpasswd)
       	return jsonify({'code':200,'username':username,'data':getfilelist})

#@nextcloud_server.route("/api/getfilelist")
#def get_file_list():
#	username = request.values.get("username")
#	getUser = User.query.filter_by(user_name = username).first()
#	result = get_filelist(getUser.user_name,getUser.user_passwd)
#	return jsonify({'code':200,'data':result})

@nextcloud_server.route("/api/getdir")
def getsubdir():
	print "***********************************"
	username = request.values.get("username")
	filepath = request.values.get("filepath")
	print filepath
	filename = ""
	if (filepath == "/remote.php/webdav/"):
		filename = ""
		getUser = User.query.filter_by(user_name = username).first()
		result = get_sub_filelist(getUser.user_name,getUser.user_passwd,filename)
		return result
	else:
		splitresult = filepath.split('/')
		print splitresult
		filename = splitresult[-2]
		print filename
		getUser = User.query.filter_by(user_name = username).first()
		result = get_sub_filelist(getUser.user_name,getUser.user_passwd,filename)
		return result

@nextcloud_server.route("/api/gethtml")
def indexpage():
	return render_template('upload.html')

@nextcloud_server.route("/api/uploadfile",methods=['GET', 'POST'])
def upload():
	username = request.values.get('username')
	print username
	filepath = request.values.get('filepath')
	print filepath
	filepath = filepath[19:]
	uploadUser = User.query.filter_by(user_name=username).first()
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			filename = file.filename
			file.save(os.path.join(nextcloud_server.config['UPLOAD_FOLDER'], filename))
#			token = base64.b64encode(filename)
			result = upload_file(uploadUser.user_name,uploadUser.user_passwd,os.path.join(nextcloud_server.config['UPLOAD_FOLDER'], filename),filepath)
			if result.find('201') == -1:
			        return jsonify({"errno":200,"errmsg":"上传成功"})
			else:
				return jsonify({"errno":201,"errmsg":"上传失败"})
		else:
			return jsonify({"errno":202,"errmsg":"文件类型错误"})


@nextcloud_server.route('/api/downloadfile',methods=['GET','POST'])
def download_file():
	#get username and filepath
	print "*********************************"
	username = request.values.get('username')
	print username
	filepath = request.values.get('filepath')
	print filepath
	getfilename = filepath.split('/')
	filename = getfilename[-1]
	print filename
	downloadUser = User.query.filter_by(user_name=username).first()
	# get user password
	result = download_afile(downloadUser.user_name,downloadUser.user_passwd,filename)
	result = json.loads(result)
	if result['code'] == 201 :
		print "download fail!"
		return result
	else:
		print "download success"
		getfilename = filepath.split('/')
		filename = getfilename[-1]
		return send_from_directory(nextcloud_server.config['DOWNLOAD_FOLDER'],filename)

@nextcloud_server.route('/api/deletefile',methods=['GET','POST'])
def delete_afile():
	username=request.values.get('username')
	filepath=request.values.get('filepath')
	print filepath
	filename=filepath[19:]
	deleteUser = User.query.filter_by(user_name=username).first()
	deleteresult = delete_file(deleteUser.user_name,deleteUser.user_passwd,filename)
	return deleteresult

@nextcloud_server.route('/api/movefileto',methods=['GET','POST'])
def move_fileto():
	username = request.values.get('username')
	filepath = request.values.get('filepath')
	newfilepath = request.values.get('newfilepath')
	return "success"

@nextcloud_server.route("/")
def test():
	return "123"


if __name__ == "__main__":
	nextcloud_server.run(
		host='0.0.0.0',
		threaded=True,
		debug=True,
		port=30000
	)
