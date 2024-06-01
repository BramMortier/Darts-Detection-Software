import cv2
import numpy as np

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

ret, image = cam.read()
image = cv2.rotate(image, cv2.ROTATE_180)

# cv2.imwrite('/home/bram/Documents/dartpoint/assets/base.jpg', image)
cv2.imwrite('/home/bram/Documents/dartpoint/assets/dart.jpg', image)

dart_path = '/home/bram/Documents/dartpoint/assets/dart.jpg'
base_path = '/home/bram/Documents/dartpoint/assets/base.jpg'

dart = cv2.imread(dart_path)
base = cv2.imread(base_path)

if dart is None or base is None:
    print("One of the images could not be read. Check the file paths.")
else:
    diff = cv2.absdiff(base, dart)

    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    _, binary_diff = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

    cv2.imwrite('/home/bram/Documents/dartpoint/assets/diff.jpg', binary_diff)

    white_pixels = np.column_stack(np.where(binary_diff == 255))

    if len(white_pixels) == 0:
        print("No differing pixels found.")
    else:
        lowest_white_pixel = white_pixels[:, 0].max()

        start_row = max(0, lowest_white_pixel - 10)
        end_row = lowest_white_pixel
        cropped_diff = binary_diff[start_row:end_row, :]

        cropped_diff_path = '/home/bram/Documents/dartpoint/assets/cropped.jpg'
        cv2.imwrite(cropped_diff_path, cropped_diff)

        white_pixel_columns = np.where(cropped_diff == 255)[1]

        if len(white_pixel_columns) > 0:
            leftmost_white_pixel = white_pixel_columns.min()
            rightmost_white_pixel = white_pixel_columns.max()
            center_white_pixel = (leftmost_white_pixel + rightmost_white_pixel) / 2
            width_position_percentage = (center_white_pixel / cropped_diff.shape[1]) * 100

            print(f"The dart sits at {width_position_percentage:.2f}% of the width starting from the left.")
        else:
            print("No white pixels found in the cropped image.")

cam.release()
