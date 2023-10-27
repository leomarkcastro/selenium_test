# Landvault Test

## How to run

1. Install python
2. On cmd, run `python -m venv ./venv`
3. On cmd, run `venv\Scripts\activate.bat`
4. On cmd, run `pip install -r requirements.txt`
5. Go to join_test.py to change some run settings like browser size, how many simultaneous browsers, etc.
6. On cmd, run `py join_test.py`

## Build Command

docker build -t sel_test .

## Run Command

docker run -it --env-file .env sel_test
