#adapted from comp0034 week 9 tutorial
import json
import os
import socket
import subprocess
import time
import pytest
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from tfl_frontend_flask import create_app, API_PORT
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def chrome_driver():
    """
    Fixture to create a Chrome driver.

    On GitHub or other container it needs to run headless, i.e. the browser doesn't open and display on screen.
    Running locally you may want to display the tests in a large window to visibly check the behaviour.
    """
    options = ChromeOptions()
    #service = Service(chrome_driver_path)
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")

    driver = Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def flask_port():
    """
    Gets a free port from the operating system.

    See: https://github.com/pytest-dev/pytest-flask/issues/54
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port



@pytest.fixture(scope="session")
def live_server_api_flask():
    """Runs the Flask app as a live server for Selenium tests (tfl portal app)

    Renamed to live_server_flask to avoid issues with pytest-flask live_server
    """
    # Construct the command string with formatted dictionary
    #Command used to run REST API
    command1 = """flask --app 'tfl_restapi_flask:create_app(test_config={"TESTING": True, "WTF_CSRF_ENABLED": False})' run --port """ + API_PORT
    #Command used to run front-end application
    try:
        server1 = subprocess.Popen(command1, shell=True)
        # Allow time for the app to start
        time.sleep(3)
        yield server1
        server1.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")


@pytest.fixture(scope="session")
def live_server_frontend_flask(flask_port):
    """Runs the Flask app as a live server for Selenium tests (tfl portal app)

    Renamed to live_server_flask to avoid issues with pytest-flask live_server
    """
    # Construct the command string with formatted dictionary
    #Command used to run REST API
    #Command used to run front-end application
    command2 = """flask --app 'tfl_frontend_flask:create_app(test_config={"TESTING": True, "WTF_CSRF_ENABLED": False})' run --port """ + str(flask_port)
    try:
        server2 = subprocess.Popen(command2, shell=True)
        # Allow time for the app to start
        time.sleep(3)
        yield server2
        server2.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")
