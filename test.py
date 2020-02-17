import requests

API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjIxNjlhNTMxLWQyNzUtNDg1YS04MmJmLTU4MzNlZDA5NTk5YiIsImlhdCI6MTU4MTY5Nzg4MSwic3ViIjoiZGV2ZWxvcGVyL2NkZjQ3ZWNlLTJjZDYtNDIzOS0wYjMyLTMzY2I3OGNmYzFiZiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEyOS4yMS4xMTUuMTAiXSwidHlwZSI6ImNsaWVudCJ9XX0.mfCesbv1IDs5Z15GMX1UTxVP6YV6Oqvlnu6odZ2SoAwCWJKzd0Oh9F7og6ZdDoW36vuCJFIZNVZ5b4H2w2wUdg'

response = requests.get(
    'https://api.clashofclans.com/v1/clans/%232PCQRQVY/currentwar',
    headers={
        'Accept': 'application/json',
        'authorization': 'Bearer {}'.format(API_TOKEN),
    }
).json()

for key in response:
    print(key)

