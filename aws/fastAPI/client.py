import requests

url = 'https://crwz9c23wa.execute-api.us-east-1.amazonaws.com/default/rcwApp/test'
url ='https://xgvxgfg32f7okiqws56hlxmf5m0jqifq.lambda-url.us-east-1.on.aws/test'
url = 'https://crwz9c23wa.execute-api.us-east-1.amazonaws.com/v1/test'
url = 'https://crwz9c23wa.execute-api.us-east-1.amazonaws.com/v3/test/'
data = {'value': ''}
response = requests.get(url, data)
response = response.json()
print(response)