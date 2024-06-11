import cv2

def test_camera(device_id):
    cap = cv2.VideoCapture(device_id)

    if not cap.isOpened():
        print("Invalid camera id")
    else:
        print(device_id)

device_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for device_id in device_ids:
    test_camera(device_id)
