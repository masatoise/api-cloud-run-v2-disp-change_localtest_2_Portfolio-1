import urllib.request

url = 'https://db-connect-test-cxok76fa6a-an.a.run.app/hello'

r = urllib.request.Request(url)

with urllib.request.urlopen(r) as response:
    body = response.read()
    print(body.decode('utf-8'))


#########################
import urllib.request
import json
url = 'https://db-connect-test-cxok76fa6a-an.a.run.app/suggest'

obj = {"suggest" : "ア"} 
#json_data = json.dumps(obj).encode("utf-8")
print(json_data)
r = urllib.request.Request(url,data=obj,headers={'Content-Type': 'application/json'},method='POST')
with urllib.request.urlopen(r) as response:
    body = response.read()
    print(body.decode('utf-8'))
