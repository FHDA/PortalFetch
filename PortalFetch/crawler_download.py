#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(filename='../log/' +
                    str(datetime.datetime.now()).replace(
                        ' ', '_').replace(':', '')[:17] + '_crawler.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
parser = ConfigParser()
parser.read('crawler.config')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


def locateButton(driver, button):
    """Search a specific button and click it if found.

    Args:
        driver: the webdriver object of this class
        button: the intended button for search
    Raises:
        NoSuchElementException: The button is not found
    Returns:
        None

    """
    inputs = driver.find_elements_by_tag_name("input")
    result = None
    for selection in inputs:
        val = selection.get_attribute("value").lower()
        if selection.get_attribute("type") == "submit":
            if button == "advance" and "advanced search" == val:
                result = selection
            elif button == "submit" and selection.is_enabled() and selection.is_displayed():
                result = selection
            elif button == "section" and "section search" == val:
                result = selection
            if result:
                result.click()
                return
    raise NoSuchElementException(button + " element is not found!")


def login_myportal(driver):
    """Open myportal website and login.

    Args:
        driver: the webdriver object of this class
    Raises:
        KeyError: Login is failed with given information
    Returns:
        None

    """
    # Open MyPortal Browser
    driver.get("https://myportal.fhda.edu/")
    try:
        username = parser.get('campus', 'username')
        driver.find_element_by_id("j_username").send_keys(username)
        password = parser.get('campus', 'password')
        driver.find_element_by_id("j_password").send_keys(password)
        driver.find_element_by_id(
            "btn-eventId-proceed").click()
        logger.info("Log in finished.")
    except:
        raise KeyError("Login failed, please check input username/password!")


def openSearchPage(driver):
    """Click 'Apps'->'Look Up Classes' and open search page.

    Args:
        driver: the webdriver object of this class
        button: the intended button for search
    Returns:
        None

    """
    # Find the Apps menu and click
    findAppsMenu(driver)
    # Find in App List（Look Up Classes）button
    classes = lookUpClasses(driver)
    # Get ain window name
    mainWindowName = driver.window_handles[0]
    classes.click()
    # Make sure the new window is open
    time.sleep(2)
    windowNames = driver.window_handles
    for name in windowNames:
        if mainWindowName != name:
            driver.switch_to.window(name)
    # Waiting for elements in the page to appear, indicating that the page has finished loading
    waitUtilPageLoaded(driver, 30)


def findAppsMenu(driver):
    """Find Apps menu.

    Args:
        driver: the webdriver object of this class
    Raises:
        NoSuchElementException: The app menu is not found
    Returns:
        None

    """
    menus = driver.find_elements_by_class_name("list-group-item")
    appMenu = []
    for menu in menus:
        txt = menu.text
        if "apps" == txt.lower():
            appMenu = menu
            appMenu.click()
    if not appMenu:
        raise NoSuchElementException("Apps menu is not found!")


def lookUpClasses(driver):
    """Find app list.

    Args:
        driver: the webdriver object of this class
    Raises:
        NoSuchElementException: The app menu is not found
    Returns:
        classes: the list of found classes

    """
    myappsclasses = driver.find_elements_by_class_name("myapps-item")
    classes = []
    for myappsclass in myappsclasses:
        txt = str.strip(myappsclass.find_element_by_class_name("myapps-item-label").text)
        if ("look up classes" == txt.lower()):
            classes = myappsclass
            return classes
    raise NoSuchElementException("No Look Up Classes feature found in the app list!")


def fillAdvanceSearch(driver):
    """Go to the advanced options page and select all options in Subject list.

    Args:
        driver: the webdriver object of this class
    Returns:
        None

    """
    # Select all options in Subject list
    subjectList = driver.find_element_by_id("subj_id")  # web element
    subjectOptions = subjectList.find_elements_by_tag_name("option")  # list
    subjectListSelect = Select(subjectList)
    logger.info("Start to select all the contents in the multi-selection drop-down box.")
    for i in range(len(subjectOptions)):
        subjectListSelect.select_by_index(i)
    locateButton(driver, "section")


def saveResult(driver):
    """Save the results of courses to a html.

    Args:
        driver: the webdriver object of this class
    Returns:
        html: the html of result page source

    """
    waitUtilPageLoaded(driver, 30)
    html = driver.page_source
    return html


def waitUtilPageLoaded(driver, count):
    """Wait until page loaded.

    Args:
        driver: the webdriver object of this class
    Raises:
        ElementNotVisibleException: Could not load full page in given count-down
    Returns:
        None

    """
    while count:
        count -= 1
        if driver.find_element_by_class_name("banner_copyright"):
            return
    raise ElementNotVisibleException("Could not load the full page!")


def generateQuarterAndFilename(quarterValueStr):
    """Return quarter and filename.

    Args:
        quarterValue:the quarter_value in crawler.config
    Returns:
        quarter str list and filename str list

    """
    n = 6
    quarterValueList = [quarterValueStr[i:i+n] for i in range(0, len(quarterValueStr), n)]
    fileNameOutput = []
    quarterOutput = []
    for quarterValue in quarterValueList:
        year = quarterValue[0:4]
        quarterSwitcher = {
            "1": "Summer",
            "2": "Fall",
            "3": "Winter",
            "4": "Spring",
        }
        schoolSwitcher = {
            "1": "Foothill",
            "2": "De Anza",
        }
        school = schoolSwitcher.get(quarterValue[5], "")
        quarter = quarterSwitcher.get(quarterValue[4], "")
        if quarter == "Summer":
            year = str(int(year)-1)

        quarterOutput.append(year + " " + quarter + " " + school)
        if school == "De Anza":
            school = "De_Anza"

        fileNameOutput.append(year + "_" + quarter + "_" + school + "_courseData.json")

    return quarterOutput, fileNameOutput


def main():
    """Download course information from De Anza myportal.

    Login in De Anza myportal using username and password.
    click Apps-Lookup Classes-Select by term -submit-Advanced Search-in Subject, select all-Section search-Download all the course infromation-Save in an excel
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    login_myportal(driver)

    # Wait for the 'list-group-item' can be found and clicked
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
        selectelement = driver.find_element_by_tag_name("select")
        # Select specified course
        quarter_downlist = Select(selectelement)
        value = parser.get('config', 'quarter_value')
        quarter_downlist.select_by_value(value)
        # click 'Submit' button
        locateButton(driver, "submit")
        # click 'Advance Search' button
        locateButton(driver, "advance")
        # Wait while the page is loading
        waitUtilPageLoaded(driver, 30)
        # Go to the advanced options page and start filling in various search terms
        fillAdvanceSearch(driver)
        # Save searched courses
        html = saveResult(driver)
        # get quarter and filename based on quarter_value in crawler.config
        quarter_list, filename_list = generateQuarterAndFilename(value)
        for i in range(0, len(filename_list)):
            DataProcess().data_process(html, filename_list[i], quarter_list[i])

        logging.info("Download Finished!")
    except Exception as e:
        logger.error(repr(e))
        sys.exit(-1)


if __name__ == "__main__":
    main()
