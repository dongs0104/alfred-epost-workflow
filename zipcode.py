#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# epost, v1.0
#

import sys
from unicodedata import normalize
import urllib, urllib2
import json
import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding('utf-8')

def send_request(q):
    params = {
        "ServiceKey": "uLEgvigbgUbygR4BPFLGjQLdxV78vuhfRZti20Xj9Gv+OhPvvkdsG6NiZs/OuFd76030lliGS+GAREtCBrBqcQ==",
        "srchwrd": q
    }
    url = "http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdSearchAllService/retrieveNewAdressAreaCdSearchAllService/getNewAddressListAreaCdSearchAll"
    url += "?ServiceKey=%s" % urllib.quote(params['ServiceKey'])
    url += "&srchwrd=%s" % urllib.quote(params['srchwrd'])

    return urllib2.urlopen(url).read()

if __name__ == '__main__':
    try:
        query = normalize('NFC', unicode(sys.argv[1])).encode('utf-8')
    except:
        query = ""

    data = send_request(query)

    output = []
    tree = ET.fromstring(data)
    success = tree.findtext('.//successYN')
    if success == 'Y':
        for item in tree.findall('newAddressListAreaCdSearchAll'):
            zipNo = item.findtext('.//zipNo')
            lnmAdres = item.findtext('.//lnmAdres')
            rnAdres = item.findtext('.//rnAdres')

            output.append({
                "title": zipNo + ' - ' + lnmAdres,
                "subtitle": rnAdres,
                "valid": True,
                "arg": zipNo
            })
    else:
        output.append({
            'title': tree.findtext('.//errMsg'),
            'valid': False

        });
    print json.dumps({"items": output})
