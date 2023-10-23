# Use an official Python runtime as a parent image
FROM python:3.11.6-bookworm

ARG INSTANCE_COUNT 
ARG ROOM_CODE

ENV INSTANCE_COUNT=$INSTANCE_COUNT
ENV ROOM_CODE=$ROOM_CODE

# Set the working directory to /app
WORKDIR /app

# install google chrome version 114
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip
RUN unzip /tmp/chromedriver.zip "chromedriver-linux64/*" -d /usr/local/bin/

RUN apt-get install -y xvfb

# Copy the current directory contents into the container at /app
COPY requirements.txt ./requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# copy the source code into /app and move into that directory.
COPY . .

# set display port to avoid crash
ENV DISPLAY=:99

# Run app.py when the container launches
CMD ["python", "join_test.py"]
