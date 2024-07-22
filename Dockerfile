FROM debian:bookworm-slim

# packages
RUN apt-get update && apt-get install -y xvfb python3-selenium python3-requests python3-pyvirtualdisplay python3-decouple git firefox-esr

# cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# this code
COPY . /root/gsuite-tools
WORKDIR /root/gsuite-tools

# geckodriver
ADD https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.34.0-linux64.tar.gz .
RUN tar xvzf geckodriver-v0.34.0-linux64.tar.gz -C /usr/bin
