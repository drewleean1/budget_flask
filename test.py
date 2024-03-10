import requests
import json 

response = requests.get('https://budget-drewleean-80248645fdf0.herokuapp.com/expenses/month/7/year/2023')
response = json.loads(response.text)

print(response[0])