import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

dir = '경로'
apikey = '발급받은 api 키값'

# 나눔카 아이디 가져오기
socar = pd.read_csv(f'{dir}/test.csv', encoding='cp949')
socarzoneId = socar['거점ID'].values.tolist()

socarCnt = []

try:
    for id in socarzoneId:
        url = f'http://openapi.seoul.go.kr:8088/{apikey}/xml/NanumcarCarList/1/5/{id}/so'
        # example) 'http://openapi.seoul.go.kr:8088/인증키/xml/NanumcarCarList/1/5/113/gr'

        response = requests.get(url)
        if response.status_code == 200:
            try:
                bs_content = bs(response.content, 'xml')
                allcnt = bs_content.find('reservAbleAllCnt').text

                socarCnt.append(allcnt)
            except Exception as e:
                socarCnt.append(-100)
                print(id, e)
                continue
        else:
            socarCnt.append(-1)

except Exception as e:
    outputdata = pd.DataFrame(socarCnt, columns=['allcnt'])
    outputdata.to_csv(f'{dir}/result_err.csv')
    print(e)
    exit()

outputdata = pd.DataFrame(socarCnt, columns=['allcnt'])
outputdata.to_csv(f'{dir}/result.csv')