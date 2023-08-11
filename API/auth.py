import requests

def AuthenticateCode(code: str, name: str) -> bool:
    response = requests.get(f'https://api.mc-oauth.com/v1/code/{code}')
    if response.status_code == 200:
        data = response.json()
        player_name = data.get("ign")
        return player_name == name
    else:
        print("Error: Unable to retrieve player name.")
        return None