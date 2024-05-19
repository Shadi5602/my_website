import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from tfl_frontend_flask import API_PORT

def test_API_is_up_and_running(live_server_api_flask):
    """
    GIVEN a live REST API
    WHEN a GET HTTP request is made to the main api url ('/')
    THEN the http response code should be 200 confirming the api is active and ready for use by the front-end
    """
    url = f'http://127.0.0.1:{API_PORT}/'
    response = requests.get(url)
    assert response.status_code == 200


def test_frontend_server_is_up_and_running(live_server_frontend_flask,live_server_api_flask,flask_port):
    """
    GIVEN running TFL front-end and API servers
    WHEN a GET HTTP request to the home page of the tfl portal app
    THEN the HTTP response should return a status code of 200, confirming the server is running and the API is accessible
    """
    url1 = f'http://127.0.0.1:{flask_port}/'
    response1 = requests.get(url1)
    assert response1.status_code == 200
  


def test_home_page_title(chrome_driver, live_server_frontend_flask,live_server_api_flask, flask_port):
    """
    GIVEN running TFL front-end and API servers
    WHEN the homepage is accessed
    THEN the value of the page title should be "TFL Cycling and Weather Data Portal"
    """
    url = f'http://127.0.0.1:{flask_port}/'
    chrome_driver.get(url)
    # Wait for the title to be there and its value to be "Paralympics - Home"
    WebDriverWait(chrome_driver, 2).until(EC.title_is("TFL Cycling and Weather Data Portal"))
    assert chrome_driver.title == "TFL Cycling and Weather Data Portal"


def test_user_log_in(chrome_driver, live_server_frontend_flask, live_server_api_flask, flask_port):
    """
    GIVEN running TFL front-end and API servers and an example signed up user "example","examplepw"
    WHEN a user logs in with these credentials
    THEN the logged in page should load with title "TFL Cycling and Weather Data Portal - Logged In"
    """
    url = f'http://127.0.0.1:{flask_port}/'
    chrome_driver.get(url)
    
    # Click on the element with id "login_nav_bar_button"
    login_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "login_nav_bar_button")
    )
    login_button.click()
    

    # Fill the email field with "example"
    email_field = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "email_field")
    )

    email_field.send_keys("example")

    
    # Fill the password field with "examplepw"
    password_field = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "password_field")
    )
    password_field.send_keys("examplepw")

    
    # Click on the login button
    login_submit_button = password_field = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "login_button")
    )
    login_submit_button.click()
    
    #Assert the logged in page has loaded with a correct title
    WebDriverWait(chrome_driver, 2).until(EC.title_is("TFL Cycling and Weather Data Portal - Logged In"))
    assert chrome_driver.title == "TFL Cycling and Weather Data Portal - Logged In"

def test_chart_creation_correct_field_entry(chrome_driver, live_server_frontend_flask,live_server_api_flask, flask_port):
    """
    GIVEN running TFL front-end and API servers
    AND a logged in user
    WHEN the user clicks on create a chart from nav-bar and fills in all relevant fields in the correct format
    THEN the page should display a "chart created succesfuly" message in the color blue
    """
    #Go to chart creation page
    chart_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "create_chart_navbar")
    )
    chart_button.click()
    
    # Fill figure name field with "example figure"
    name_field = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "figure_name")
    )
    name_field.send_keys("example figure")

    
    # Fill start date and end date fields
    startdate_field = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "start_date")
    )
    startdate_field.send_keys("01/01/2012")

    enddate_field = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "end_date")
    )
    enddate_field.send_keys("01/01/2015")

    #Make drop down selection:
    #data-type selection
    datatype_dropdown = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "data_type")
    )
    data_type_selection = Select(datatype_dropdown)
    data_type_selection.select_by_visible_text("Temperature")

    #Chart type selection
    datatype_dropdown = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "chart_type")
    )
    data_type_selection = Select(datatype_dropdown)
    data_type_selection.select_by_visible_text("Scatter plot")

    #Click create chart button
    create_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "create_button")
    )
    create_button.click()

    #Assert "chart created" message is displayed to user in blue text
    user_message = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "user-message")
    )
    #assert correct message is displayed
    assert "Chart saved!" in user_message.text
    #assert color of message is blue through check of css property value (blue color)
    assert "rgba(0, 0, 255, 1)" in user_message.value_of_css_property("color")

def test_chart_creation_wrong_field_entry(chrome_driver, live_server_frontend_flask,live_server_api_flask, flask_port):
    """
    GIVEN running TFL front-end and API servers
    AND a logged in user
    WHEN the user clicks on create a chart from nav-bar but does NOT fill in fields in the correct format
    THEN the page should display a "Failed creation" message in the color red
    """
    #Go to chart creation page
    chart_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "create_chart_navbar")
    )
    chart_button.click()
    
    # Fill figure name field with "example figure"
    name_field = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "figure_name")
    )
    name_field.send_keys("example figure")

    
    # Fill start date and end date fields in an INCORRECT format
    startdate_field = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "start_date")
    )
    startdate_field.send_keys("AB/01/2012")

    enddate_field = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "end_date")
    )
    enddate_field.send_keys("CD/01/2015")

    #Make drop down selection:
    #data-type selection
    datatype_dropdown = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "data_type")
    )
    data_type_selection = Select(datatype_dropdown)
    data_type_selection.select_by_visible_text("Temperature")

    #Chart type selection
    datatype_dropdown = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "chart_type")
    )
    data_type_selection = Select(datatype_dropdown)
    data_type_selection.select_by_visible_text("Scatter plot")

    #Click create chart button
    create_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "create_button")
    )
    create_button.click()

    #Assert "failed" message is displayed to user in red text
    user_message = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "user-message")
    )
    #assert "failed" message is displayed
    assert "Failed" in user_message.text
    #assert color of message is red through check of css property value (blue color)
    assert "rgba(255, 0, 0, 1)" in user_message.value_of_css_property("color")


def test_correct_selection_chart_viewing(chrome_driver, live_server_frontend_flask,live_server_api_flask, flask_port):
    """
    GIVEN running TFL front-end and API servers
    AND a logged in user
    WHEN the user clicks on view my charts from nav-bar and selects a created chart
    THEN the page should display the chart and NO error message
    """
    view_chart_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "view_charts_navbar")
    )
    view_chart_button.click()

    #Make drop down selection:
    #data-type selection
    figure_dropdown = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "select_chart")
    )
    figure_selection = Select(figure_dropdown)
    figure_selection.select_by_visible_text("example figure (id:1)")


    #click view now
    view_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "view_now_button")
    )
    view_button.click()
    
    #ensure figure element loads on page
    chart_image = WebDriverWait(chrome_driver, timeout=10).until(
        lambda d: d.find_element(By.ID, "chart_image")
    )
    assert "chart_image" in chart_image.get_attribute("id")

    #ensure no error message is displayed:
    error_message = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "user-message")
    )
    assert "" == error_message.text


def test_wrong_selection_chart_viewing(chrome_driver, live_server_frontend_flask,live_server_api_flask, flask_port):
    """
    GIVEN running TFL front-end and API servers
    AND a logged in user
    WHEN the user clicks on view my charts from nav-bar BUT has not selected chart from the drop-down list
    THEN the page should display an error message to the user informing them of the need to select a chart
    """
    view_chart_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "view_charts_navbar")
    )
    view_chart_button.click()


    #click view now
    view_button = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "view_now_button")
    )
    view_button.click()
    

    #ensure correct error message is displayed:
    error_message = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "user-message")
    )
    assert "Please make a selection." == error_message.text

