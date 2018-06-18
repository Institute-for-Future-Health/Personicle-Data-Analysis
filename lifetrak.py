##POST http://lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com/api/v2/auth/login HTTP/1.1
##x-client-id: da9c4bfdc65c6478d3e248d588f11b160a6a47de65658afc4c03bf08a179b98f
##x-client-secret: 721cb656035a4b28b9208a0c83b7704b36a21ea940c55c49bb069a85bdd7cd0a1992837fe335370cc8d27131a41dc155db1f2e6a9e29c0fd33582385b7a6a9d1
##x-access-token: 
##Content-Type: application/x-www-form-urlencoded; charset=UTF-8
##Content-Length: 43
##Host: lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com
##Connection: Keep-Alive
##Accept-Encoding: gzip
##User-Agent: okhttp/2.2.0
##
##email=kchian%40uci.edu&password=password123
##


##GET http://lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com/api/v2/hrv?start=2016-04-01&end=2018-02-23&page=0&page_size=1000 HTTP/1.1
##x-client-id: da9c4bfdc65c6478d3e248d588f11b160a6a47de65658afc4c03bf08a179b98f
##x-client-secret: 721cb656035a4b28b9208a0c83b7704b36a21ea940c55c49bb069a85bdd7cd0a1992837fe335370cc8d27131a41dc155db1f2e6a9e29c0fd33582385b7a6a9d1
##x-access-token: Fe26.2*JDOsu9gFwKO8i6D*cc44c5966e6edd0e27bdf24a892b9d944cda89521155e236741e6cd72fcbc89a*NJTtnPDCrKWm25crr-sqvg*U0Hrs7d7p-FClcEeBUy1iO0Rf7detOEXZUbSfC6NPeK3oWl6PRZcjm2uLg16KJUS*1519991387952*1c95ab9e2e28e30c5ceff037f9b89d838275324c82efb1ea8aef3ce40519c3a6*azeL1f7Xmbw56didMMyK7sUts-zDt6NkraEYNDw7F1k
##Host: lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com
##Connection: Keep-Alive
##Accept-Encoding: gzip
##User-Agent: okhttp/2.2.0
##

##GET http://lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com/api/v2/freeliving?with=datapoints,lightpoints&start=2018-01-11&end=2018-02-10&page=0&page_size=50 HTTP/1.1
##x-client-id: da9c4bfdc65c6478d3e248d588f11b160a6a47de65658afc4c03bf08a179b98f
##x-client-secret: 721cb656035a4b28b9208a0c83b7704b36a21ea940c55c49bb069a85bdd7cd0a1992837fe335370cc8d27131a41dc155db1f2e6a9e29c0fd33582385b7a6a9d1
##x-access-token: Fe26.2*JDOsu9gFwKO8i6D*cc44c5966e6edd0e27bdf24a892b9d944cda89521155e236741e6cd72fcbc89a*NJTtnPDCrKWm25crr-sqvg*U0Hrs7d7p-FClcEeBUy1iO0Rf7detOEXZUbSfC6NPeK3oWl6PRZcjm2uLg16KJUS*1519991387952*1c95ab9e2e28e30c5ceff037f9b89d838275324c82efb1ea8aef3ce40519c3a6*azeL1f7Xmbw56didMMyK7sUts-zDt6NkraEYNDw7F1k
##Host: lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com
##Connection: Keep-Alive
##Accept-Encoding: gzip
##User-Agent: okhttp/2.2.0
##
#
# GET http://lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com/api/v2/sleep?start=2016-04-01&end=2018-02-23&page=0&page_size=1000 HTTP/1.1
# x-client-id: da9c4bfdc65c6478d3e248d588f11b160a6a47de65658afc4c03bf08a179b98f
# x-client-secret: 721cb656035a4b28b9208a0c83b7704b36a21ea940c55c49bb069a85bdd7cd0a1992837fe335370cc8d27131a41dc155db1f2e6a9e29c0fd33582385b7a6a9d1
# x-access-token: Fe26.2*JDOsu9gFwKO8i6D*cc44c5966e6edd0e27bdf24a892b9d944cda89521155e236741e6cd72fcbc89a*NJTtnPDCrKWm25crr-sqvg*U0Hrs7d7p-FClcEeBUy1iO0Rf7detOEXZUbSfC6NPeK3oWl6PRZcjm2uLg16KJUS*1519991387952*1c95ab9e2e28e30c5ceff037f9b89d838275324c82efb1ea8aef3ce40519c3a6*azeL1f7Xmbw56didMMyK7sUts-zDt6NkraEYNDw7F1k
# Host: lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com
# Connection: Keep-Alive
# Accept-Encoding: gzip
# User-Agent: okhttp/2.2.0






import datetime
import json
import requests
import sys


headers = {}
r = ''

if __name__ == '__main__':

    headers['x-client-id'] = 'da9c4bfdc65c6478d3e248d588f11b160a6a47de65658afc4c03bf08a179b98f'
    headers['x-client-secret'] = '721cb656035a4b28b9208a0c83b7704b36a21ea940c55c49bb069a85bdd7cd0a1992837fe335370cc8d27131a41dc155db1f2e6a9e29c0fd33582385b7a6a9d1'
    headers['x-access-token'] = ''
    headers['User-Agent'] = 'okhttp/2.2.0'
    headers['Accept-Encoding'] = 'gzip'
    payload = {'email':'kchian@uci.edu','password':'password123'}

    r = requests.post('http://lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com/api/v2/auth/login',data=payload,headers=headers)
    if r.status_code != 200:
        print(r.text)
        sys.exit(-1)
    print('login success')
    headers['x-access-token'] = json.loads(r.text)['data']['token']

    today = datetime.datetime.today().strftime('%Y-%m-%d')
    hrv = requests.get('http://lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com/api/v2/hrv?start=2016-04-01&end='+today+'&page=0&page_size=1000',headers=headers)
    hrv_json = json.loads(hrv.text)
    if hrv.status_code != 200:
        print(r.text)
        sys.exit(-1)
    print('hrv success')

    start_date = datetime.datetime(2016,5,1)
    td = datetime.timedelta(30)
    today = datetime.datetime.today()
    one_day = datetime.timedelta(1)
    hr_results = []
    while start_date < today:
        postdate = start_date + td
        print('trying start='+start_date.strftime('%Y-%m-%d')+' end='+postdate.strftime('%Y-%m-%d'))
        hr = requests.get('http://lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com/api/v2/freeliving?with=datapoints,lightpoints&start='+start_date.strftime('%Y-%m-%d')+'&end='+postdate.strftime('%Y-%m-%d')+'&page=0&page_size=50',headers=headers)
        if hr.status_code != 200:
            print(hr.text)
            sys.exit(-1)
        else:
            hr_results.extend(json.loads(hr.text)['data']['results'])
        start_date = postdate + one_day
    print('hr success')

    today = datetime.datetime.today().strftime('%Y-%m-%d')

    sleep = requests.get('http://lifetrakfitproduction-2050721770.us-east-1.elb.amazonaws.com/api/v2/sleep?start=2016-04-01&end='+today+'&page=0&page_size=1000',headers=headers)
    if sleep.status_code != 200:
        print(r.text)
        sys.exit(-1)
    print('sleep success')

    with open('sleep_dump','w+') as f:
        f.write(str(json.loads(sleep.text)))
    with open('hr_dump','w+') as f:
        f.write(str(hr_results))
    with open('hrv_dump','w+') as f:
        f.write(str(hrv_json))
    print('done')
