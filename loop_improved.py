import cv2
import time

class Camera:
    def __init__(self, id, width=1024, height=768, rotation=cv2.ROTATE_180):
        self.id = id
        self.width = width
        self.height = height
        self.rotation = rotation
        self.cap = cv2.VideoCapture(self.id)
        self.configure_camera()

    def configure_camera(self):
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def is_opened(self):
        return self.cap.isOpened()

    def read_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.rotate(frame, self.rotation)
        return ret, frame

    def release(self):
        self.cap.release()

class CameraManager:
    def __init__(self, cameras, fps):
        self.cameras = cameras
        self.fps = fps
        self.frame_interval = 1.0 / self.fps

    def start(self):
        try:
            while True:
                for camera in self.cameras:
                    ret, frame = camera.read_frame()
                    
                    if not ret:
                        print(f"Skipping corrupted frame from camera {camera.id}")
                        break
                    cv2.imshow(f'Camera {camera.id}', frame)

                time.sleep(self.frame_interval)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            pass
        finally:
            self.release_all()
            cv2.destroyAllWindows()

    def release_all(self):
        for camera in self.cameras:
            camera.release()

def init_detection_cameras(fps):
    blue_camera = Camera(0)
    red_camera = Camera(2)
    green_camera = Camera(4)

    cameras = [blue_camera, red_camera, green_camera]

    for camera in cameras:
        if not camera.is_opened():
            print(f"Could not open camera {camera.id}")
            return

    manager = CameraManager(cameras, fps)
    manager.start()

if __name__ == "__main__":
    init_detection_cameras(5)
