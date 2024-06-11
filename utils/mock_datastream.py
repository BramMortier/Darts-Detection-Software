import requests 
import time
import random

BOARD_CODE = "DP_KW5PPYWD"

def init_mock_datastream():
    while True:
        dart_sector = random.randint(1, 20)
        dart_multiplier = random.randint(1, 3)

        requestBody = {
            "dart_zone": dart_sector,
            "dart_multiplier": dart_multiplier,
            "dart_score": dart_sector * dart_multiplier,
            "dart_x": "",
            "dart_y": "",
            "thrown": True,
        }

        response = requests.post(f"http://localhost:3000/boards/{BOARD_CODE}/detection", json = requestBody)
        print(response.json());

        time.sleep(2)

if __name__ == "__main__":
    init_mock_datastream();