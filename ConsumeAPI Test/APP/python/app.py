# Guide on consuming ImageBase64API on by a third-party app via the terminal
# developed with love by Pius Lucky

# You must have installed requests using the pip command
# >>> pip install requests

import requests
# r = requests.get("http://localhost:8000/api/v1/link/encode/")
context = {
  "username": "PiusLucky",
  "email": "luckypius50@gmail.com",
  "password": "luckypius5"
}
r = requests.post('http://localhost:8000/api/v1/rest-auth/login/', data = context)
print(r.text)
my_token = "874c818885100912f940647714d1763c1d8b81c8"



url = {
  "url": "http://localhost:8000/media/photo-1511469054436-c7dedf24c66b.jpg"
}
#Getting 401 (unauthorized), this might be dew to the fact that the access token has expired. Try refreshing that token.
#Getting 401 after that, just get a new token and refresh. works like charm!
#Use requests documentation to check for the parameters you can always pass in!
encode_link = requests.post("http://localhost:8000/api/v1/link/encode/", data = url, headers={ 'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyNzI2Nzk0LCJqdGkiOiI1YzBiNjY5ODIxNWY0ZjNiYmU4ODhjOWZlMzBjMjYxNCIsInVzZXJfaWQiOjN9.84hv-O12BvcIjOyESelPT9-ReoAna3w4505BWu9HHrc' })

# print(r)
# print(r.text)
print(encode_link)
output_dict = encode_link.json()
print(output_dict["image_info"])