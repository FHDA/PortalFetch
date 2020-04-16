#!/usr/bin/env python
"""Fetch course information from De Anza myportal.

It requires the users input their own user name and password.
"""
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import sys
import csv
from bs4 import BeautifulSoup
import time
import chromedriver_binary
import logging

def submitClick(driver):
    """
    Search and click sumbit button in the search by term page.

    Parameters: webdriver
    Returns: None
    """
    inputs = driver.find_elements_by_tag_name("input")
    submit = ""
    for input in inputs:
        if "submit" == input.get_attribute("type") and input.is_enabled() and input.is_displayed():
            submit = input
            break
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
    submit = ""
    for ipt in inputs:
        if "submit".lower() == ipt.get_attribute("type") and \
                "Advanced Search" == ipt.get_attribute("value"):
            submit = ipt
            break
    if not submit:
        logging.info("Advanced Search is not found!")
        sys.exit(-1)
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
        parser = ConfigParser()
        parser.read('user.ini')
        username = parser.get('db', 'db_username')
        driver.find_element_by_id("j_username").send_keys(username)
        # input password
        password = parser.get('db', 'db_password')
        driver.find_element_by_id("j_password").send_keys(password)
        driver.find_element_by_id(
            "btn-eventId-proceed").click()  # Wait for the response from the next page and make sure the page is loaded!
        logging.info("Log in finished.")
    except:
        logging.error("Value Error: Log in failed.")
        sys.exit(-1)


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
        if mainWindowName == name:
            continue  # Do not switch to the main window because the search page opens from the main window
        driver.switch_to_window(name)
        break  # Because there are only two windows: the main window and the open window, switching directly to the end is over
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
        if "apps".lower() == txt.lower():  # No left menu found
            appMenu = menu
            break
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
        txt = myappsclass.find_element_by_class_name("myapps-item-label").text
        txt = str.strip(txt)
        if ("look up classes" == txt.lower()):
            classes = myappsclass
            break
    if not classes:
        logging.info("No Look Up Classes feature found in the app list!")
        sys.exit(-1)
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
    logging.info("Start to select all the contents in the multi-selection drop-down box. There are many options. You may have to wait for more time. Don't worry ...")
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
    submit = ""  # webElement
    for ipt in ipts:
        if "submit" == ipt.get_attribute("type").lower() and \
                "Section Search".lower() == ipt.get_attribute("value").lower():
            submit = ipt
            break
    try:
        submit.click()
    except:
        logging.error("No submit button found! ! ")
        sys.exit(-1)
    # Wait for a while, wait for the page to open and make sure it loads
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
    while True and count < 30:
        count += 1
        try:
            driver.find_element_by_class_name("banner_copyright")
            break
        except:
            logging.info("retry after 1 second...")
            time.sleep(1)
            pass



def get_contents(ulist, text):
    """
    Get result contents from html.

    Input: text is html of the courses, ulist is an empty list []
    Output : ulist will include all the courses list in text
    Parameters: List, String
    Returns: None
    """
    soup = BeautifulSoup(text, 'lxml')
    trs = soup.find_all('tr')
    for tr in trs:
        ui = []
        for td in tr:
            ui.append(td.string)
        ulist.append(ui)


def save_contents(filename, firstline, urlist):
    """
    Save course result to a .csv file.

    input : urlist is the courses list we get from get_contents
    output : save courses in a file "DeAnza2020spring.csv"

    Parameters: String, String, List
    Returns: None
    """
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([firstline])

        for i in range(8, len(urlist)-1):
            if len(urlist[i]) >= 35:
                writer.writerow([urlist[i][1], urlist[i][3], urlist[i][5],urlist[i][7], urlist[i][9], urlist[i][11],
                            urlist[i][13], urlist[i][15], urlist[i][17],urlist[i][19], urlist[i][21], urlist[i][23],
                            urlist[i][25], urlist[i][27], urlist[i][29],urlist[i][31], urlist[i][33], urlist[i][35]]
                            )
            else:
                writer.writerow(urlist[i])
    logging.info("Download Finished!")


def main():
    """
    Download course information from De Anza myportal.

    Login in De Anza myportal using username and password.
    click Apps-Lookup Classes-Select by term -submit-Advanced Search-in Subject, select all-Section search-Download all the course infromation-Save in an excel
    """
    driver = webdriver.Chrome()
    login_myportal(driver)
    # The way to judge is that the left menu can be found in the interface, and the menu style has list-group-item)
    while True:
        try:
            driver.find_element_by_class_name("list-group-item")
        except NoSuchElementException:
            time.sleep(1)
            logging.info('wait for seconds...')
            continue
        break

    # Course search page from homepage after login
    openSearchPage(driver)

    # choose course
    selectelement = driver.find_element_by_tag_name("select")  # Because the page has only one drop-down box
    # Select specified course
    quarter_downlist = Select(selectelement)  # a Select object
    parser = ConfigParser()
    parser.read('dev.ini')
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
    courseList = []
    get_contents(courseList, html)  # Extract course information from html

    filename = parser.get('db', 'db_filename')
    firstline = parser.get('db', 'db_firstline')
    save_contents(filename, firstline, courseList)  # Save course information as a csv file


if __name__ == "__main__":
    main()