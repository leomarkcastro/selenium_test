import requests
import json
from generate_room import roomEnvironment

# create an enum of roomType, roomEnvironment
roomType = {
    "MeetingRoom": "MeetingRoom",
    "BoardRoom": "BoardRoom",
    # "Auditorium": "Auditorium",
}

roomEnvironment = {
    "FuturePop": "FuturePop",
    "Japandi": "Japandi",
    "Metaverse2033": "Metaverse2033",
}


def generate_join_link(
        roomCode="DAF231432S",
        roomEnvironment=roomEnvironment["Japandi"],
        roomType=roomType["MeetingRoom"],
        roomName="My personal room",
):
    url = "https://dev-landvault-be.int2.lv-aws-x3.xyzapps.xyz/api/users/create-shareable-link-auto"

    payload = json.dumps({
        "roomName": roomName,
        "roomCode": roomCode,
        "roomType": roomType,
        "roomEnvironment": roomEnvironment,
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # parse json response
    response_json = json.loads(response.text)

    return response_json['url']
