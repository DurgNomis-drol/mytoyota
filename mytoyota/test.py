import aiohttp
from mytoyota.client import MyT

username = "jane@doe.com"
password = "MyPassword"
locale = "da-dk"
session = aiohttp.ClientSession()

client = MyT(locale=locale, session=session)

client.perform_login(username=username, password=password)

valid, cars = await client.get_cars()

if valid:
    print(cars)
