#!/usr/bin/env python
"""Fetch course information from De Anza myportal.

It requires file 'user.ini' to load the user's own user name and password.
"""
import sys
import time
import logging
import chromedriver_binary
import datetime
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from crawler_data_process import DataProcess

logging.basicConfig(filename = '../log/' + 
                str(datetime.datetime.now()).replace(' ', '_').replace(':', '')[:17] + '_crawler.log', 
                level=logging.INFO, 
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
parser = ConfigParser()
parser.read('dev.ini')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

def submitClick(driver):
    """
    Search and click sumbit button in the search by term page.

    Parameters: webdriver
    Returns: None
    """
    inputs = driver.find_elements_by_tag_name("input")
    submit = None
    for selection in inputs:
        if "submit" == selection.get_attribute("type") and selection.is_enabled() and selection.is_displayed():
            submit = selection
            break
    if not submit:
        raise NoSuchElementException("Input element is not found!")
    submit.click()
    time.sleep(2)  # Waiting for completion


def advanceSearch(driver):
    """
    Locate 'Advanced Search' button and click in the 'Look Up Classes' page.

    Parameters: webdriver
    Returns: None
    """
    # Locate and click the Advanced Search  button
    inputs = driver.find_elements_by_tag_name("input")
    submit = None
    for selection in inputs:
        if "submit" == selection.get_attribute("type") and \
                "Advanced Search" == selection.get_attribute("value"):
            submit = selection
            break
    if not submit:
        raise NoSuchElementException("Advanced Search element is not found!")
    submit.click()


def login_myportal(driver):
    """
    Open myportal website and login.

    Parameters: webdriver
    Returns: None
    """
    # Open the browser (The true url is：https://myportal.fhda.edu/）
    driver.get("https://myportal.fhda.edu/")
    try:
        # input username
        username = parser.get('campus', 'username')
        driver.find_element_by_id("j_username").send_keys(username)
        # input password
        password = parser.get('campus', 'password')
        driver.find_element_by_id("j_password").send_keys(password)
        driver.find_element_by_id(
            "btn-eventId-proceed").click()  # Wait for the response from the next page and make sure the page is loaded!
        logger.info("Log in finished.")
    except:
        raise KeyError("Login failed, please check input username/password!")


def openSearchPage(driver):
    """
    Click 'Apps'->'Look Up Classes' and open search page.

    Parameters: webdriver
    Returns: None
    """
    # Find the Apps menu and click
    findAppsMenu(driver)
    # Find in App List（Look Up Classes）button
    classes = lookUpClasses(driver)
    mainWindowName = driver.window_handles[0]  # Main window name
    classes.click()
    time.sleep(2)  # Make sure the new window is open
    # Switch to the newly opened window, because this window is the course search page, you must switch the program pointer to this window to operate this window
    windowNames = driver.window_handles  # Get all window names
    for name in windowNames:
        if mainWindowName != name:
            driver.switch_to_window(name)  # Do not switch to the main window because the search page opens from the main window
    # Waiting for elements in the page to appear, indicating that the page has finished loading
    waitUtilPageLoaded(driver)


def findAppsMenu(driver):
    """
    Find Apps menu.

    Parameters: webdriver
    Returns: None
    """
    menus = driver.find_elements_by_class_name("list-group-item")
    appMenu = []
    for menu in menus:
        txt = menu.text
        if "apps" == txt.lower():  # No left menu found
            appMenu = menu
            break
    if not appMenu:
        raise NoSuchElementException("Apps menu is not found!")
    time.sleep(2)  # Wait for the next page to come over
    appMenu.click()  # Open the menu


def lookUpClasses(driver):
    """
    Find app list.

    Parameters: webdriver
    Returns: classes
    Return type: list
    """
    myappsclasses = driver.find_elements_by_class_name("myapps-item")
    classes = []
    for myappsclass in myappsclasses:
        txt = str.strip(myappsclass.find_element_by_class_name("myapps-item-label").text)
        if ("look up classes" == txt.lower()):
            classes = myappsclass
            break
    if not classes:
        raise NoSuchElementException("No Look Up Classes feature found in the app list!")
    return classes


def fillAdvanceSearch(driver):
    """
    Fill advance search.

    Go to the advanced options page and start filling in various search terms
    Parameters: webdriver
    Returns: None
    """
    # Select all options in Subject list
    subjectList = driver.find_element_by_id("subj_id")  # web element
    subjectOptions = subjectList.find_elements_by_tag_name("option")  # list
    subjectListSelect = Select(subjectList)
    logger.info("Start to select all the contents in the multi-selection drop-down box.")
    for i in range(0, len(subjectOptions)):
        subjectListSelect.select_by_index(i)
    # Submit search and click
    sectionSearch(driver)


def sectionSearch(driver):
    """
    Locate section search button and click.

    Parameters: webdriver
    Returns: None
    """
    ipts = driver.find_elements_by_tag_name("input")  # list of Web Element
    submit = None
    for ipt in ipts:
        if "submit" == ipt.get_attribute("type").lower() and \
                "section search" == ipt.get_attribute("value").lower():
            submit = ipt
            break
    if not submit:
        raise NoSuchElementException("No section search button found!")
    submit.click()
    time.sleep(3)


def saveResult(driver):
    """
    Save the results of courses to a html.

    Parameters: webdriver
    Returns: html
    Return type: String
    """
    waitUtilPageLoaded(driver)
    # Scroll down a page to show the table (no practical meaning, just look at the effect)
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    # After loading is complete, the entire form page
    html = driver.page_source
    time.sleep(5)  # Wait for a while, let people take a look, in fact, it does not make sense to the programmer
    return html


# Wait until the page is loaded! This only applies to child pages, not to the main page, because there is no banner_copyright information in the main page
def waitUtilPageLoaded(driver):
    """
    Wait until page loaded.

    Parameters: webdriver
    Returns: None
    """
    count = 0
    while count < 30:
        count += 1
        if driver.find_element_by_class_name("banner_copyright"):
            return
    raise ElementNotVisibleException("Could not load the full page!")


def main():
    """
    Download course information from De Anza myportal.

    Login in De Anza myportal using username and password.
    click Apps-Lookup Classes-Select by term -submit-Advanced Search-in Subject, select all-Section search-Download all the course infromation-Save in an excel
    """
    
    driver = webdriver.Chrome()
    login_myportal(driver)
    # The way to judge is that the left menu can be found in the interface, and the menu style has list-group-item)
    web_driver_counter = 400
    list_group_item = None
    while web_driver_counter:
        try:
            list_group_item = driver.find_element_by_class_name("list-group-item")
        except:
            pass
        web_driver_counter -= 1
    if not list_group_item:
        logger.error("Could not find list-group item!")
        raise NoSuchElementException("Could not find list-group item!")

    try:
        # Course search page from homepage after login
        openSearchPage(driver)

        # choose course
        selectelement = driver.find_element_by_tag_name("select")  # Because the page has only one drop-down box
        # Select specified course
        quarter_downlist = Select(selectelement)  # a Select object
        value = parser.get('db','db_value')
        quarter_downlist.select_by_value(value)
        # Element positioning through select objects, value positioning (value of option)
        # click 'Submit' button
        submitClick(driver)
        # click 'Advance Search' button
        advanceSearch(driver)
        # Wait for a while to make sure the page loads
        waitUtilPageLoaded(driver)
        # Go to the advanced options page and start filling in various search terms
        fillAdvanceSearch(driver)
        # Save searched courses
        html = saveResult(driver)  # see method
        filename = parser.get('db', 'db_filename')
        firstline = parser.get('db', 'db_firstline')
        object = DataProcess()
        object.data_process(html,filename, firstline)
    except Exception as e:
        logger.error(str(e))
        sys.exit(-1)


if __name__ == "__main__":
    main()