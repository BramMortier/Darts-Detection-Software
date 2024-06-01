import numpy as np
import logging
from datetime import datetime
import requests 

BOARD_CODE = "DP_KW5PPYWD"

requestBody = {
    "dart1Sector": 20,
    "dart1Multiplier": 2,
    "dart1Score": 40,
    "dart1X": -90.00944,
    "dart1Y": -119.99386,
    "dart1IsThrown": True,

    "dart2Sector": 20,
    "dart2Multiplier": 2,
    "dart2Score": 40,
    "dart2X": -90.00944,
    "dart2Y": -119.99386,
    "dart2IsThrown": True,

    "dart3Sector": 20,
    "dart3Multiplier": 2,
    "dart3Score": 40,
    "dart3X": -90.00944,
    "dart3Y": -119.99386,
    "dart3IsThrown": True,

    "total": 120,
}

# response = requests.post(f"http://localhost:3000/boards/{BOARD_CODE}/detection", json = requestBody)
# print(response.json());

globalLogger = logging.getLogger("GLOBAL")
globalLogger.setLevel(logging.DEBUG)

baseHandler = logging.FileHandler("calculation.log", mode="w")
BaseFormatter = logging.Formatter("[%(name)s %(levelname)s] %(message)s")

baseHandler.setFormatter(BaseFormatter)
globalLogger.addHandler(baseHandler)

start = datetime.now()

# -------------------------------------------------------------------------------------------------- 
# These constants can be adjusted to make the calculation work for different dartboard sizes and 
# camera positions
# --------------------------------------------------------------------------------------------------
DARTBOARD_RADIUS = 171
CAMERA_RADIUS = 310

CAM_BLUE_POSITION = 0.2506 # used a s reference | 0 degrees correction
CAM_BLUE_CORRECTION = 0

CAM_RED_POSITION = 0.405 # 120 degrees correction
CAM_RED_CORRECTION = 2 * np.pi/3

CAM_GREEN_POSITION = 0.8062 # 240 degrees correction
CAM_GREEN_CORRECTION = 4 * np.pi/3

zones = {
    0: "6",
    1: "13",
    2: "4",
    3: "18",
    4: "1",
    5: "20",
    6: "5",
    7: "12",
    8: "9",
    9: "14",
    10: "11",
    11: "8",
    12: "16",
    13: "7",
    14: "19",
    15: "3",
    16: "17",
    17: "2", 
    18: "15",
    19: "10",
    20: "6",
}

globalLogger.info(f"BASE CONFIGURATION \n- dartboard radius: {DARTBOARD_RADIUS} \n- camera radius: {CAMERA_RADIUS} \n")

# --------------------------------------------------------------------------------------------------
# This function calculates the line equation of the line that intersects the thrown dart and the 
# camera based on where the dart is detected percentage wise on the processed image.
# --------------------------------------------------------------------------------------------------
def calculate_line_equation(dart_position):
    angle_between_tangents = np.pi - 2 * np.arccos(DARTBOARD_RADIUS/CAMERA_RADIUS)

    angle_cam_dart = -(2 * dart_position - 1) * (angle_between_tangents / 2)

    slope = np.tan(angle_cam_dart)

    y_intercept = -slope * CAMERA_RADIUS

    return slope, y_intercept

blue_line_equation = calculate_line_equation(CAM_BLUE_POSITION)
red_line_equation = calculate_line_equation(CAM_RED_POSITION)
green_line_equation = calculate_line_equation(CAM_GREEN_POSITION)

globalLogger.info(f"BASE LINE EQUATIONS \n- blue camera: {blue_line_equation[0]:.05f}x{blue_line_equation[1]:.05f} \n- red camera: {red_line_equation[0]:.05f}x{red_line_equation[1]:.05f} \n- green camera: {green_line_equation[0]:.05f}x{green_line_equation[1]:.05f}\n")

# --------------------------------------------------------------------------------------------------
# This function transforms cartesian coords to polar coords whilst also optionally taking in 
# to account a correction angle. We use this correction to put all line equations in the same space.
# --------------------------------------------------------------------------------------------------
def transform_to_polar_coords(x, y, correction):
    radius = np.sqrt(np.square(x) + np.square(y))

    angle = np.arctan2(y, x)
    angle = calculate_angle_correction_within_range(angle, correction)

    return radius, angle

# --------------------------------------------------------------------------------------------------
# This small helper function is used to keep the corrected angle between -π and π
# --------------------------------------------------------------------------------------------------
def calculate_angle_correction_within_range(angle, correction):
    return (np.mod(angle - correction + np.pi, 2 * np.pi)) - np.pi

blue_polar_coords_y_crossing = transform_to_polar_coords(0, blue_line_equation[1], CAM_BLUE_CORRECTION)
red_polar_coords_y_crossing = transform_to_polar_coords(0, red_line_equation[1], CAM_RED_CORRECTION)
green_polar_coords_y_crossing = transform_to_polar_coords(0, green_line_equation[1], CAM_GREEN_CORRECTION)

blue_polar_coords_x_crossing = transform_to_polar_coords(CAMERA_RADIUS, 0, CAM_BLUE_CORRECTION)
red_polar_coords_x_crossing = transform_to_polar_coords(CAMERA_RADIUS, 0, CAM_RED_CORRECTION)
green_polar_coords_x_crossing = transform_to_polar_coords(CAMERA_RADIUS, 0, CAM_GREEN_CORRECTION)

globalLogger.info(f"CORRECTED POLAR COORDS \nblue camera: \n- x crossing: {blue_polar_coords_x_crossing} \n- y crossing: {blue_polar_coords_y_crossing} \nred camera: \n- x crossing: {red_polar_coords_x_crossing} \n- y crossing: {red_polar_coords_y_crossing}\ngreen camera: \n- x crossing: {green_polar_coords_x_crossing} \n- y crossing: {green_polar_coords_y_crossing}\n")

# --------------------------------------------------------------------------------------------------
# This small helper transforms polar coords back to cartesian coords.
# --------------------------------------------------------------------------------------------------
def transform_to_cartesian_coords(radius, angle):
    x = np.cos(angle) * radius
    y = np.sin(angle) * radius

    return x, y

blue_cartesian_coords_y = transform_to_cartesian_coords(blue_polar_coords_y_crossing[0], blue_polar_coords_y_crossing[1])
blue_cartesian_coords_x = transform_to_cartesian_coords(blue_polar_coords_x_crossing[0], blue_polar_coords_x_crossing[1])
blue_slope_ref = (blue_cartesian_coords_y[1] - blue_cartesian_coords_x[1]) / (blue_cartesian_coords_y[0] - blue_cartesian_coords_x[0]) 
blue_y_intercept_ref = blue_cartesian_coords_y[1] - blue_slope_ref * blue_cartesian_coords_y[0]

red_cartesian_coords_y = transform_to_cartesian_coords(red_polar_coords_y_crossing[0], red_polar_coords_y_crossing[1])
red_cartesian_coords_x = transform_to_cartesian_coords(red_polar_coords_x_crossing[0], red_polar_coords_x_crossing[1])
red_slope_ref = (red_cartesian_coords_y[1] - red_cartesian_coords_x[1]) / (red_cartesian_coords_y[0] - red_cartesian_coords_x[0]) 
red_y_intercept_ref = red_cartesian_coords_y[1] - red_slope_ref * red_cartesian_coords_y[0]

green_cartesian_coords_y = transform_to_cartesian_coords(green_polar_coords_y_crossing[0], green_polar_coords_y_crossing[1])
green_cartesian_coords_x = transform_to_cartesian_coords(green_polar_coords_x_crossing[0], green_polar_coords_x_crossing[1])
green_slope_ref = (green_cartesian_coords_y[1] - green_cartesian_coords_x[1]) / (green_cartesian_coords_y[0] - green_cartesian_coords_x[0]) 
green_y_intercept_ref = green_cartesian_coords_y[1] - green_slope_ref * green_cartesian_coords_y[0]

globalLogger.info(f"CORRECTED LINE EQUATIONS \n- blue camera: {blue_slope_ref:.05f}x{blue_y_intercept_ref:.05f}\n- green camera: {green_slope_ref:.05f}x{green_y_intercept_ref:.05f}\n- red camera: {red_slope_ref:.05f}x{red_y_intercept_ref:.05f}\n")

# --------------------------------------------------------------------------------------------------
# This function calculates an intersection point of two lines. We use it to determine the points
# of the triangle were the dart is located.
# --------------------------------------------------------------------------------------------------
def calculate_intersection(slope1, y_intercept1, slope2, y_intercept2):
    x_intersection = (y_intercept2 - y_intercept1) / (slope1 - slope2)

    y1_intersection = slope1 * x_intersection + y_intercept1
    y2_intersection = slope2 * x_intersection + y_intercept2

    # average calculated from the results of both line equations
    y_intersection = (y1_intersection + y2_intersection) / 2

    return x_intersection, y_intersection

triangle_point_blue_red = calculate_intersection(blue_slope_ref, blue_y_intercept_ref, red_slope_ref, red_y_intercept_ref)
triangle_point_blue_green = calculate_intersection(blue_slope_ref, blue_y_intercept_ref, green_slope_ref, green_y_intercept_ref)
triangle_point_green_red = calculate_intersection(green_slope_ref, green_y_intercept_ref, red_slope_ref, red_y_intercept_ref)

globalLogger.info(f"LINE INTERSECTIONS / TRAIGLE POINTS\n- first point: {triangle_point_blue_red[0]:.05f}, {triangle_point_blue_red[1]:.05f}\n- second point: {triangle_point_blue_green[0]:.05f}, {triangle_point_blue_green[1]:.05f}\n- third point: {triangle_point_green_red[0]:.05f}, {triangle_point_green_red[1]:.05f}\n")

result_x = (triangle_point_blue_green[0] + triangle_point_blue_red[0] + triangle_point_green_red[0]) / 3
result_y = (triangle_point_blue_green[1] + triangle_point_blue_red[1] + triangle_point_green_red[1]) / 3

globalLogger.info(f"FINAL DART POSITION CARTESIAN COORDS\n- x: {result_x:.05f}\n- y: {result_y:.05f}\n")

result_polar_coords = transform_to_polar_coords(result_x, result_y, 0)

globalLogger.info(f"FINAL DART POSITION POLAR COORDS\n- radius: {result_polar_coords[0]:.05f}\n- angle (radians): {result_polar_coords[1]:.05f}\n- angle (degrees): {np.degrees(result_polar_coords[1]):.05f}\n")

def check_multiplier(distance):
    if distance >= 0 and distance <= 0.7:
        return "double bull"
    elif distance > 0.7 and distance <= 1.6:
        return "bull"
    elif distance > 9.75 and distance <= 10.75:
        return 3
    elif distance > 16 and distance <= 17:
        return 2
    elif distance > 17:
        return 0
    else:
        return 1
    
def check_zone(angle):
    if(angle < 0): angle = angle + 360

    angle_zone = np.floor((angle + 9) / 18)

    for zone, score in zones.items():
        if(angle_zone == zone):
            return score

multiplier = check_multiplier(result_polar_coords[0] / 10);
zone = check_zone(np.degrees(result_polar_coords[1]))
		
if(multiplier == "bull"):
	score = 25
elif(multiplier == "double bull"):
	score = 50
     
print(multiplier)
print(zone)

end = datetime.now()

delta = (end - start).total_seconds() * 10**3
globalLogger.info(f"PROGRAM EXECUTION TIME: {delta:.05f}ms")