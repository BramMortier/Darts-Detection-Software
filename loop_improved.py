# -------------------------------------------------------------------------------------------------- 
# Module imports
# --------------------------------------------------------------------------------------------------
import cv2
import time

# -------------------------------------------------------------------------------------------------- 
# These constants determine how the detection system will be configured
# --------------------------------------------------------------------------------------------------
CAM_WIDTH = 1024
CAM_HEIGHT = 768
DETECTION_FPS = 5

# -------------------------------------------------------------------------------------------------- 
# The Camera class lets us instanciate a camera that's automatically configured. It also checks if 
# the camera is responding correctly
# --------------------------------------------------------------------------------------------------
class Camera:
    def __init__(self, id, name, width=CAM_WIDTH, height=CAM_HEIGHT, rotation=cv2.ROTATE_180):
        self.id = id
        self.name = name
        self.width = width
        self.height = height
        self.rotation = rotation
        self.video_capture = cv2.VideoCapture(self.id)
        self.configure_camera()

        if not self.is_opened():
            print(f"Could not open camera {self.name}")

    def configure_camera(self):
        self.video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def is_opened(self):
        return self.video_capture.isOpened()

    def read_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.rotate(frame, self.rotation)
        return ret, frame

    def release(self):
        self.video_capture.release()

# -------------------------------------------------------------------------------------------------- 
# The Camera class lets us instanciate a camera that's automatically configured. It also checks if 
# the camera is responding correctly
# --------------------------------------------------------------------------------------------------
class DetectionSystem:
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
                        print(f"Skipping corrupted frame from camera {camera.name}")
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

if __name__ == "__main__":
    cameras = [Camera(0, "blue_camera"), Camera(2, "blue_camera"), Camera(4, "blue_camera")]

    DetectionSystem(cameras, DETECTION_FPS).start()
