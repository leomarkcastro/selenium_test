import requests
import json


def generate_join_link():
    url = "https://dev-landvault-be.int2.lv-aws-x3.xyzapps.xyz/api/users/create-shareable-link-auto"

    payload = json.dumps({
        "roomName": "My personal room",
        "roomCode": "DAF231432S",
        "roomType": "MeetingRoom",
        "roomEnvironment": "Japandi"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # parse json response
    response_json = json.loads(response.text)

    return response_json['url']
