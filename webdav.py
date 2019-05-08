#!/usr/bin/python
# -*- coding: UTF-8 -*-
from lxml import etree
# webdav operation
import os
import commands
import random
import json

def get_filelist(username, password):
#	cmd = "curl -u" + username + ":" + password +"'http://150.109.196.228/remote.php/webdav/'"
	cmd = "curl -u "+username+":"+password+" 'http://35.237.28.200/remote.php/webdav/' -X PROPFIND"	
	status,getResult = commands.getstatusoutput(cmd)
	#print getResult
	#parse xml
	parseResult = etree.HTML(getResult)
	gerResponseResult = parseResult.xpath('//multistatus/response')
	parseParentsDir = parseResult.xpath('//response/href')
	getParentsDir = parseParentsDir[0].text

	fileList = []
	childrenDirList = []
	for item in gerResponseResult:
		getDirHref = item.xpath('./href')
		judgeHref = getDirHref[0].text
		if judgeHref[-1] == "/":
			childrenDirList.append(judgeHref)
		else:
			parseFileLenth = item.xpath('.//getcontentlength')
			getContentLength = parseFileLenth[0].text
			parseContentType = item.xpath('.//getcontenttype')
			getContentType = parseContentType[0].text
			filetmp = {
                        "name":judgeHref,
                        "type":getContentType,
                        "length":getContentLength
                	}
			fileList.append(filetmp)
	childrenDirList.pop(0)
	resultJson = {
		"rootdir":getParentsDir,
		"subdir":childrenDirList,
		"files":fileList
	}
	#print resultJson
	# todo parse filelist
	return resultJson

def get_sub_filelist(username,password,subdir):
        cmd = "curl -u "+username+":"+password+" 'http://35.237.28.200/remote.php/webdav/"+subdir+"' -X PROPFIND"
        status,getResult = commands.getstatusoutput(cmd)
        #print getResult
        #parse xml
        parseResult = etree.HTML(getResult)
        gerResponseResult = parseResult.xpath('//multistatus/response')
        parseParentsDir = parseResult.xpath('//response/href')
        getParentsDir = parseParentsDir[0].text

        fileList = []
        childrenDirList = []
        for item in gerResponseResult:
                getDirHref = item.xpath('./href')
                judgeHref = getDirHref[0].text
                if judgeHref[-1] == "/":
                        childrenDirList.append(judgeHref)
                else:
                        parseFileLenth = item.xpath('.//getcontentlength')
                        getContentLength = parseFileLenth[0].text
                        parseContentType = item.xpath('.//getcontenttype')
                        getContentType = parseContentType[0].text
                        filetmp = {
                        "name":judgeHref,
                        "type":getContentType,
                        "length":getContentLength
                        }
                        fileList.append(filetmp)
        childrenDirList.pop(0)
        resultJson = {
                "rootdir":getParentsDir,
                "subdir":childrenDirList,
                "files":fileList
        }
	return json.dumps(resultJson)

def get_specific_filelist(username,password,specificpath):
	cmd = "curl -u "+username+":"+password+" 'http://35.237.28.200/remote.php/webdav/"+specificpath+"' -X PROPFIND"
	status,getSpecificFileListResult = commands.getstatusoutput(cmd)
	print status
	print getSpecificFileListResult
	return getSpecificFileListResult

def download_afile(username,password,filename):
	cmd = "curl -u "+ username +":"+password+ " -X GET 'http://35.237.28.200/remote.php/webdav/" + filename + "' --output "+ "/data/nextcloud/files/downloadfile/" + filename
	print cmd 
	status,downloadFileResult = commands.getstatusoutput(cmd)
	print status
	print downloadFileResult
	if status == 0:
		return '''{"code":200,"data":"download file success"}'''
	else:
		return '''{"code":201,"data":"download file fail"}'''

def upload_file(username,password,filename,filepath):		
#	cmd = "curl -u " + username + ":" + password +" -T " + filepath + "'http://150.109.196.228/remote.php/webdav/'"
	cmd =  "curl -u " + username+":"+password+" -T " + filename + " http://35.237.28.200/remote.php/webdav/"+filepath
        status,uploadFileResult = commands.getstatusoutput(cmd)
	print status
	if status == 0:
		return '''{"code":200,"data":"upload success"}'''
	else:
		return '''{"code":201,"data":"upload fail"}'''

def delete_file(username,password,filename):
	cmd = "curl -u "+ username +":" + password +" 'http://35.237.28.200/remote.php/webdav/'"+ filename +" -X DELETE"
	status,deleteFileResult = commands.getstatusoutput(cmd)
	print status
        if status == 0:
                return '''{"code":200,"data":"delete success"}'''
        else:
                return '''{"code":201,"data":"delete fail"}'''

def create_random_username():
	usableName_char = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	username = ""
	for i in range(8):
		username = username + random.choice(usableName_char)
	print username
	return username

class UserOperation:
	def createuser(self,username, password):
		cmd = "curl -X POST -u root:Dis@init3 http://35.237.28.200/ocs/v1.php/cloud/users -d userid='" + username + "' -d password='" + password + "' -H 'OCS-APIRequest: true'"
		status,createUserResult = commands.getstatusoutput(cmd)
		print status
		if "OK" in createUserResult:
			return '''{"code":200,"data":"create user success"}'''
		else:
			return '''{"code":201,"data":"create user fail"}'''


#def main():
#	test =fileoperation()
	
#	filepath = "/data/nextcloud/webdav"
#	result = test.uploadfile("root","Dis@init3","/data/nextcloude/webdav")
#	print result
	
if __name__ == "__main__":
#	main()	
#	result = getsubfilelist("root","Dis@init3","Photos")
#	print result
#	user = UserOperation()
#	result = user.createuser("你好","Dis@init3") 
#	print result
	result = create_random_username()
