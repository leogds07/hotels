#IMPORTS
import json
import http.client
from handle_password import load_key, decrypt_message


#execute api
def get_json(location, api_key):
    #decrypt api key
    key = load_key()
    API_KEY = decrypt_message(api_key, key)

    #SETTINGS
    conn = http.client.HTTPSConnection("api.hasdata.com")
    headers = { 'x-api-key': API_KEY }

    #start connection and get response
    conn.request("GET", f"/scrape/google-maps/search?q=Hotels+in+{location}", headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")

    return data

#extract websites
def extract_websites(json_data) -> list:
    websites = []

    data = json.loads(json_data)

    for result in data["localResults"]:
        websites.append(result.get('website'))

    return websites