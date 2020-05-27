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
    """Search and click sumbit button in the search by term page.

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
    """Locate 'Advanced Search' button and click in the 'Look Up Classes' page.

    Parameters: webdriver
    Returns: None
    """
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

def locateButton(driver, button):
    inputs = driver.find_elements_by_tag_name("input")
    result = None
    for selection in inputs:
        if button == "advance":
            if "submit" == selection.get_attribute("type") and \
                "Advanced Search" == selection.get_attribute("value"):
                result = selection
                break
        elif button == "submit":
            if "submit" == selection.get_attribute("type") and selection.is_enabled() and selection.is_displayed():
                result = selection
                break
    if not result:
        raise NoSuchElementException(button+" element is not found!")


def login_myportal(driver):
    """Open myportal website and login.

    Parameters: webdriver
    Returns: None
    """
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

    Parameters: webdriver
    Returns: None
    """
    findAppsMenu(driver)
    classes = lookUpClasses(driver)
    mainWindowName = driver.window_handles[0]
    classes.click()
    time.sleep(2)
    windowNames = driver.window_handles
    for name in windowNames:
        if mainWindowName != name:
            driver.switch_to_window(name)
    waitUtilPageLoaded(driver)


def findAppsMenu(driver):
    """Find Apps menu.

    Parameters: webdriver
    Returns: None
    """
    menus = driver.find_elements_by_class_name("list-group-item")
    appMenu = []
    for menu in menus:
        txt = menu.text
        if "apps" == txt.lower():
            appMenu = menu
            break
    if not appMenu:
        raise NoSuchElementException("Apps menu is not found!")
    time.sleep(2)
    appMenu.click()


def lookUpClasses(driver):
    """Find app list.

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
    """Fill advance search.

    Go to the advanced options page and start filling in various search terms
    Parameters: webdriver
    Returns: None
    """
    subjectList = driver.find_element_by_id("subj_id")  # web element
    subjectOptions = subjectList.find_elements_by_tag_name("option")  # list
    subjectListSelect = Select(subjectList)
    logger.info("Start to select all the contents in the multi-selection drop-down box.")
    for i in range(0, len(subjectOptions)):
        subjectListSelect.select_by_index(i)
    sectionSearch(driver)


def sectionSearch(driver):
    """Locate section search button and click.

    Parameters: webdriver
    Returns: None
    """
    ipts = driver.find_elements_by_tag_name("input")
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
    """Save the results of courses to a html.

    Parameters: webdriver
    Returns: html
    Return type: String
    """
    waitUtilPageLoaded(driver)
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    html = driver.page_source
    time.sleep(5)
    return html

def waitUtilPageLoaded(driver):
    """Wait until page loaded.

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
    """Download course information from De Anza myportal.

    Login in De Anza myportal using username and password.
    click Apps-Lookup Classes-Select by term -submit-Advanced Search-in Subject, select all-Section search-Download all the course infromation-Save in an excel
    """
    
    driver = webdriver.Chrome()
    login_myportal(driver)

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
        openSearchPage(driver)
        selectelement = driver.find_element_by_tag_name("select")
        quarter_downlist = Select(selectelement)
        value = parser.get('db','db_value')
        quarter_downlist.select_by_value(value)
        submitClick(driver)
        advanceSearch(driver)
        waitUtilPageLoaded(driver)
        fillAdvanceSearch(driver)
        html = saveResult(driver)
        filename = parser.get('db', 'db_filename')
        firstline = parser.get('db', 'db_firstline')
        object = DataProcess()
        object.data_process(html,filename, firstline)
    except Exception as e:
        logger.error(str(e))
        sys.exit(-1)


if __name__ == "__main__":
    main()