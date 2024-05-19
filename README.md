# COMP0034 Coursework 2: Transport for London (TFL) Data Portal and Chart Creation with User Login Application
GITHUB Link: https://github.com/ucl-comp0035/comp0034-cw2i-Shadi5602.git
## Accessing application
Before beginning , it is important to note:
*in order to access the application, both the REST API (src1) and the front-end application (src2) flask apps must be running.* 

1. ABegin by creating a virtual enviornment, installing requirements.txt (pip install -r requirements.txt), and running (pip install -e .)

2. Open *two* terminal windows. One will be used for running the rest api and one for the front-end application. 

3. To run the rest api, type the following command in the first terminal: "flask --app tfl_restapi_flask run --port 5001"
    IMPORTANT NOTE 1: If port 5001 is unavailable, then you will need to change a variable "API_PORT" at the top of __init__.py at path (src2/tfl_frontend_flask/__init__.py). This ensures the front-end app uses the correct api url's for requests. 

    IMPORTANT NOTE 2: If facing flask errors when trying to run the servers for the FIRST time, run __init__.py in (src1/tfl_restapi_flask/) and __init__.py in (src2/tfl_frontend_flask). Then attempt to run the flask development servers again. 

4. To run the front-end application, run the following in the second terminal: "flask --app tfl_frontend_flask run".
    If necessary, specify an available port. 

Through the above steps, the application should be accessible and usable through the local host link provided from running the command in step 4. 

## Running testing
Testing will use the API port specified in __init__.py of “tfl_frontend_flask” to run the API server and will automatically find an available port to run the main application. To run tests, simply navigate to the main directory of the repository, then in terminal run the “pytest” command. 

Ensure suitable versions of chromedriver and Google Chrome are available to run the test cases through selenoum webdriver. 