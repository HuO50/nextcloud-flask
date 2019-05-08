#!/bin/sh

curl -u root:root 'http://150.109.196.228/remote.php/webdav/tmp' -X PROPFIND --data '<?xml version="1.0" encoding="UTF-8"?>
 <d:propfind xmlns:d="DAV:">
   <d:prop xmlns:oc="http://150.109.196.228/ns">
     <d:getlastmodified/>
     <d:getcontentlength/>
     <d:getcontenttype/>
     <oc:permissions/>
     <d:resourcetype/>
     <d:getetag/>
   </d:prop>
 </d:propfind>'
echo '***********************'
curl -u root:root 'http://150.109.196.228/remote.php/webdav/tmp'  -X PROPFIND

echo '***********************'
curl -u root:root webdav 'http://150.109.196.228/remote.php/webdav/tmp/webdav' -X PUT

