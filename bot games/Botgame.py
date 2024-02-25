import cv2 
import numpy as np
import pyautogui
import mss
from time import sleep
import keyboard

pyautogui.FAILSAFE = False
sct = mss.mss()
default_monitor = sct.monitors[1]

def click_template_image(
    template_image_path: str,
    monitor=default_monitor,
    threshold: float = 0.6,
    number_of_clicks: int = 1,
):
    
    print(f"{template_image_path} search")
    template_image = cv2.imread(template_image_path, 1)
    game_screenshot = np.array(sct.grab((0, 0, monitor["width"], monitor["height"])))
    game_screenshot = game_screenshot[:, :, :3]  # remove alpha
    search_result = cv2.matchTemplate(
        game_screenshot, template_image, cv2.TM_CCOEFF_NORMED
    )
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(search_result)
    print(max_val)

    y_coords, x_coords = np.where(search_result >= threshold)  

    width_reset_multiplier = game_screenshot.shape[1] / monitor["width"]
    height_reset_multiplier = game_screenshot.shape[0] / monitor["height"]
    w = template_image.shape[1]
    h = template_image.shape[0]
    for idx in range(number_of_clicks):
        if idx + 1 > len(x_coords):
            continue
        x, y = x_coords[idx], y_coords[idx]
        x /= width_reset_multiplier
        y /= height_reset_multiplier
        x_c = int((x + x + w) // 2)
        y_c = int((y + y + h) // 2)
        pyautogui.click(x=x_c, y=y_c)  # type:ignore
        sleep(0.2) 

close_buttons = [
    "close.png",
]

valuables = [
   "star.png",
   "cash.png",
   "key.png",
   "red-cash.png",
]

stop_key = 'Esc'  
running = True 
while running:
    if keyboard.is_pressed(stop_key):
        running = False
        break 
    for valuable_image in valuables:
        click_template_image("images/" + valuable_image)
    for close_button_image in close_buttons:
        click_template_image("images/" + close_button_image)


    
    