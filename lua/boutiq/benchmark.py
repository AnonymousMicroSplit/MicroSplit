import requests

data = {
  'currency_code': 'EUR'
}

 requests.post('http://10.102.243.173:80/setCurrency', data=data)
print(response)
