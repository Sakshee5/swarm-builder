import requests
import base64

client_id = 'fe55761c9d6c43d2be9c3ed57f506577'
client_secret = '9bb23630df894400b831dbc622d82c6c'

# Encode Client ID and Secret
auth_string = f"{client_id}:{client_secret}"
b64_auth_string = base64.b64encode(auth_string.encode()).decode()

# Request Token
token_url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {b64_auth_string}"
}
data = {
    "grant_type": "client_credentials"
}

response = requests.post(token_url, headers=headers, data=data)
response_data = response.json()

if response.status_code == 200:
    access_token = response_data['access_token']
    print("Access Token:", access_token)
else:
    print("Error:", response_data)
