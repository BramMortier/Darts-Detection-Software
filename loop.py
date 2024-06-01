import cv2
import time

def init_detection_cameras(fps):
    blue_camera = cv2.VideoCapture(0)
    red_camera = cv2.VideoCapture(2)
    green_camera = cv2.VideoCapture(4)

    blue_camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

    blue_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    blue_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

    red_camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

    red_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    red_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

    green_camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

    green_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    green_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
    
    if not blue_camera.isOpened():
        print("Could not open blue camera")
        return
    if not red_camera.isOpened():
        print("Could not open red camera")
        return
    if not green_camera.isOpened():
        print("Could not open green camera")
        return
    
    frame_interval = 1.0 / fps
    
    try:
        while True:
            ret_blue, frame_blue = blue_camera.read()
            ret_red, frame_red = red_camera.read()
            ret_green, frame_green = green_camera.read()

            frame_blue = cv2.rotate(frame_blue, cv2.ROTATE_180)
            frame_red = cv2.rotate(frame_red, cv2.ROTATE_180)
            frame_green = cv2.rotate(frame_green, cv2.ROTATE_180)
            
            if not ret_blue:
                print("skipping corrupted blue camera frame")
                break

            if not ret_red:
                print("skipping corrupted red camera frame")
                break

            if not ret_green:
                print("skipping corrupted green camera frame")
                break
            
            cv2.imshow('Blue Camera', frame_blue)
            cv2.imshow('Red Camera', frame_red)
            cv2.imshow('Green Camera', frame_green)
            
            time.sleep(frame_interval)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        blue_camera.release()
        red_camera.release()
        green_camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    init_detection_cameras(5)
