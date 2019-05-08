

import os
import commands

cmd ='''curl -u root:Dis@init3 http://35.237.28.200/remote.php/dav/files/root/ -X PROPFIND --data '<?xml version="1.0" encoding="UTF-8"?><d:propfind xmlns:d="DAV:"><d:prop xmlns:oc="http://owncloud.org/ns"><d:getcontenttype/><oc:permissions/></d:prop></d:propfind>' '''

status,output = commands.getstatusoutput(cmd)
print status,output
