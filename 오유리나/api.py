import urllib3
import requests
from urllib.parse import unquote, urlencode, quote_plus 
import xmltodict
import json

url = "https://safemap.go.kr/openApiService/data/getFludMarksData.do"
serviceKey = "BCJJ6H0U-BCJJ-BCJJ-BCJJ-BCJJ6H0UIV"
#serviceKeyDecoded = unquote(serviceKey, 'UTF-8') 
queryParams = f'?serviceKey={serviceKey}&pageNo=10&type=xml&numOfRows=1000'
                                   

    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)

res = requests.get(url + queryParams) 
print(res.content)

jsonString = json.dumps(xmltodict.parse(res.content), indent=4)
print(jsonString)
