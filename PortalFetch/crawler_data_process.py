#!/usr/bin/env python
"""Process html course information to save in a .csv file.

It requires file 'user.ini' to load the user's own user name and password.
"""
from bs4 import BeautifulSoup
import csv
import logging


class DataProcess:
    def __get_contents(self, ulist, text):
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

    def __save_contents(self, filename, firstline, urlist):
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

    def data_process(self, text, filename, firstline):
        courseList = []
        self.__get_contents(courseList, text)  # Extract course information from html
        self.__save_contents(filename, firstline, courseList)  # Save course information as a csv file
