import cv2
import time
import threading

def camera_thread(camera_id, frame_interval, window_name):
    camera = cv2.VideoCapture(camera_id)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
    
    if not camera.isOpened():
        print(f"Could not open camera {camera_id}")
        return

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print(f"skipping corrupted frame from camera {camera_id}")
                break

            frame = cv2.rotate(frame, cv2.ROTATE_180)
            cv2.imshow(window_name, frame)
            
            time.sleep(frame_interval)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        camera.release()
        cv2.destroyAllWindows()

def init_detection_cameras(fps):
    frame_interval = 1.0 / fps

    blue_thread = threading.Thread(target=camera_thread, args=(0, frame_interval, 'Blue Camera'))
    red_thread = threading.Thread(target=camera_thread, args=(2, frame_interval, 'Red Camera'))
    green_thread = threading.Thread(target=camera_thread, args=(4, frame_interval, 'Green Camera'))

    blue_thread.start()
    red_thread.start()
    green_thread.start()

    blue_thread.join()
    red_thread.join()
    green_thread.join()

if __name__ == "__main__":
    init_detection_cameras(5)
