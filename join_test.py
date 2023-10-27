from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from generate_room import generate_join_link, roomEnvironmentList, roomTypeList
from multiprocessing import Process
import os
from math import ceil
from time import sleep
from pyvirtualdisplay import Display


def get_env(key, default):
    return os.environ.get(key, default)

# get environment variables


browser_width = 400
browser_aspect_ratio = 3/4  # 4:3
browser_size = (ceil(browser_width), ceil(browser_width*browser_aspect_ratio))
browser_row_size = 3
instance_count = int(get_env("INSTANCE_COUNT", 1))
room_code = get_env("ROOM_CODE", "test123")
use_virtual_display = get_env(
    "USE_VIRTUAL_DISPLAY", "false").lower() == "true"
use_gpu = get_env(
    "USE_GPU", "false").lower() == "true"

# start virtual display

if use_virtual_display:
    print("Starting virtual display")
    # set xvfb display since there is no GUI in docker container.
    display = Display(visible=0, size=browser_size)
    display.start()

# declare test routine


def hold_key(driver, key, duration, sleep_duration):
    for i in range(duration):
        driver.find_element(By.TAG_NAME, "body").send_keys(key)
        sleep(0.1)
    sleep(sleep_duration)


def test_routine(i, roomCode):
    print(f"[{i}] Testing...")
    chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)

    # set window size to 400 x 300
    chrome_options.add_argument(
        f"window-size={browser_size[0]},{browser_size[1]}")

    # set window positiona
    x = i % browser_row_size * browser_size[0]
    y = i // browser_row_size * browser_size[1]
    chrome_options.add_argument(f"window-position={x},{y}")

    if use_virtual_display:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # q: 4GB in MB
    # a: 40961
    if (use_gpu):
        chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--js-flags="--max_old_space_size=8192"')

    # get current project directory
    project_dir = os.getcwd()

    # save browsing session (create it if it doesn't exist)
    userDataDir = os.path.join(project_dir, f"chrome-data-{i}")
    # create folder if it doesn't exist
    if not os.path.exists(userDataDir):
        os.mkdir(userDataDir)
    chrome_options.add_argument(f"user-data-dir={userDataDir}")
    # enlarge memory

    chrome_options.set_capability("goog:loggingPrefs", {  # old: loggingPrefs
        "browser": "ALL"})

    chrome_options.page_load_strategy = 'none'

    print(f"[{i}] Starting Chrome...")
    driver = webdriver.Chrome(options=chrome_options)

    print(f"[{i}] Create room link...")
    join_url = generate_join_link(
        roomCode,
        get_env("ROOM_ENVIRONMENT", roomEnvironmentList["Japandi"]),
        get_env("ROOM_TYPE", roomTypeList["MeetingRoom"])
    )

    print(f"[{i}] Joining room (no-wait)...")
    driver.get(join_url)

    print(f"[{i}] Waiting for page to load...")
    total_logs = 0
    # remain running until user closes the browser
    while True:
        # simulate key hold to body
        # keys = ["w", "a", "s", "d"]
        # shuffle(keys)
        # for i in keys:
        #     hold_key(driver, i, randint(1000, 5000), randint(1, 2))

        logs = driver.get_log("browser")
        if (len(logs) > 0):
            for log in logs:
                total_logs += 1
                print(f"[{i}] >> {total_logs} - {log['level']} - {log['message']}")

        sleep(5)


def test():
    print("Starting test...")
    # test_routine(0, room_code)
    # create x multi processes of test_routine
    x = instance_count
    print(
        f"Spawing {x} instance(s) of test_routine with roomCode: {room_code}")
    processes = []
    for i in range(x):
        processes.append(Process(target=test_routine, args=(i, room_code)))
        print(f"Spawning process {i}")
        processes[i].start()
        print(f"Process {i} started")

    # wait for all processes to finish
    for i in range(x):
        processes[i].join()
        print(f"Process {i} ended")


if __name__ == "__main__":
    print("Starting Test")
    test()
