from msgraph import Client
import json

''' config.json
{
  "tenant": "1234-5678-9012",
  "client_id": "1234-5678-9012",
  "client_secret":"1234-5678-9012",
  "username": "user@email.com",
  "password": "123456"
}
'''
config = json.loads(open('config.json').read())

client = Client(config=config)
# client.auth_by_password("Notes.Read.All")
client.auth_by_secret_id()

print(client.token)

print(client.onenote_notebooks())
