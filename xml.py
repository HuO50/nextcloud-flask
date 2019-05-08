from lxml import etree
import json
resultjson={
	"parentsdir": "/remote.php/webdav/Photos",
	"childrens":["filename1","filename2"],
	"files":[{"name":"file1",
		  "type":"filetype",
		  "length":"filelenth"},
		 {"name":"file2",
		  "type":"filetype",
		  "length":"filelenth"}
		]

}

test1 = etree.HTML(test)
#print test1
#test2 = etree.parse(test1)
print test1
#result = etree.tostring(test1,pretty_print = True)
result = test1.xpath('//multistatus/response')
getparentsdir = test1.xpath('//response/href')
parentsdir = getparentsdir[0].text

filelist = []
childrendirlist = []
#print len(result)
for item in result:
	href =  item.xpath('./href')
	judgefile =  href[0].text
	print judgefile
	if judgefile[-1] == "/":
		print "childrens"+judgefile
		childrendirlist.append(judgefile)
	else:
#		print etree.tostring(item)
		list = item.xpath('.//getcontentlength')
		getcontentlenth =  list[0].text
		list = item.xpath('.//getcontenttype')
		getcontenttype = list[0].text
#		print getcontenttype
		filetmp = {
			"name":judgefile,
			"type":getcontenttype,
			"length":getcontentlenth
		}
		filelist.append(filetmp)
print filelist
print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
print childrendirlist
#childrendirlist.append("/tmp/")
childrendirlist.pop(0)
print childrendirlist
resultjson = {
	"parentsdir": parentsdir,
	"childrensdir":childrendirlist,
	"files":filelist
}
print resultjson

		#getcontentlength = item.xpath('./getcontentlength')
		
		#getcontenttype =  item.xpath('./getcontenttype')
		#print getcontenttype[0].text
	#print etree.parse(item)
#print 
#contenttype = test1.xpath('//getcontenttype')
#length = test1.xpath('//response/getcontentlength')
#print length
#response = test1.xpath('//response/href')
#print response[0].text
#print result[0].text
#print contenttype[0].text
#print length[0].text
