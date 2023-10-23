from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from generate_room import generate_join_link
from multiprocessing import Process
import os
from math import ceil
from pyvirtualdisplay import Display

# get environment variables

browser_width = 400
browser_aspect_ratio = 3/4  # 4:3
browser_size = (ceil(browser_width), ceil(browser_width*browser_aspect_ratio))
browser_row_size = 3
instance_count = int(os.environ.get("INSTANCE_COUNT", 3))
room_code = os.environ.get("ROOM_CODE", "test123")
use_virtual_display = os.environ.get(
    "USE_VIRTUAL_DISPLAY", "false").lower() == "true"

# start virtual display

if use_virtual_display:
    # set xvfb display since there is no GUI in docker container.
    display = Display(visible=0, size=browser_size)
    display.start()

# declare test routine


def test_routine(i, roomCode):
    print(f"[{i}] Testing...")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # set window size to 400 x 300
    chrome_options.add_argument(
        f"window-size={browser_size[0]},{browser_size[1]}")

    # set window positiona
    x = i % browser_row_size * browser_size[0]
    y = i // browser_row_size * browser_size[1]
    chrome_options.add_argument(f"window-position={x},{y}")

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # get current project directory
    project_dir = os.getcwd()

    # save browsing session (create it if it doesn't exist)
    userDataDir = os.path.join(project_dir, f"chrome-data-{i}")
    # create folder if it doesn't exist
    if not os.path.exists(userDataDir):
        os.mkdir(userDataDir)
    chrome_options.add_argument(f"user-data-dir={userDataDir}")

    driver = webdriver.Chrome(options=chrome_options)

    join_url = generate_join_link(roomCode)
    driver.get(join_url)

    # remain running until user closes the browser
    while True:
        pass


def test():
    # create x multi processes of test_routine
    x = instance_count
    processes = []
    for i in range(x):
        processes.append(Process(target=test_routine, args=(i, room_code)))
        processes[i].start()

    # wait for all processes to finish
    for i in range(x):
        processes[i].join()


if __name__ == "__main__":
    test()
