#!/usr/bin/env python
"""Deputy .html file to .json file.

It needs to import an .html file of De Anza courses information website.
"""
from bs4 import BeautifulSoup
from lxml.html import fromstring, tostring
import json
import collections


class DataProcess:
    def __getContents(self, courseList, html):
        """
        Get result contents from html.

        Input: html is html of the courses, ulist is an empty list []
        Output : ulist will include all the courses list in text
        Parameters: List, String
        Returns: None
        """
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr')
        for tr in trs:
            ui = []
            for td in tr:
                if td == '\n':
                    continue
                elif td.string:
                    ui.append(str(td.string))
                else:
                    ui.append(td)
            if len(ui) == 19:
                temp = []
                for u in ui:
                    if u is not None:
                        if type(u) is not str:
                            soup = BeautifulSoup(str(u), 'lxml')
                            u = soup.get_text()
                        temp.append((u))
                courseList.append(temp[:18])


    def __deputyList(self, courseList):
        """
        Deputy courseList to a json file.

        Input: courseLise is courses list from __getContents
        Output : .json file  will include all the courses informatiom
        Parameters: List,
        Returns: None
        """
        dic = {}
        title = ['Select', 'CRN', 'Coreq', 'Subj', 'Crse', 'Sec', 'Cmp', 'Cred', 'Title', 'Days', 'Time', 'Act', 'Rem',
                 'WL Rem', 'Instructor', 'Date (MM/DD)', 'Location', 'Attribute', 'lab']
        for i in range(len(courseList)):
            if courseList[i][0] == 'Select':
                subj = courseList[i+1][3]
                d = []
                dic[subj] = d
            else:
                if courseList[i][0] != '\xa0':
                    di = {}
                    count = -1
                    for ele in courseList[i]:
                        count += 1
                        if count != 3 and count != 2 :
                            di[title[count]] = ele if ele != '\xa0' else ""
                    di['lab'] = []
                    dic[courseList[i][3]].append(di)
                elif courseList[i][0] == '\xa0':
                    dl = {}
                    count = -1
                    j = i-1
                    while courseList[j][3]== '\xa0':
                        j -= 1
                    subj = courseList[j][3]
                    for ele in courseList[i]:
                        count += 1
                        if ele != '\xa0':
                            dl[title[count]] = ele
                    dic[subj][-1]['lab'].append(dl)
        return dic


    def htmlToJson(self, htmlFile, jsonFile, quarter, fetchTime):
        """
        Deputy htmlFile to a json file.

        Input:  htmlFile is a .html file got from __deputyList,
                jsonFile is .json file name you want to give for the output
                quarter is the name of the course quarter.
                fetchTime is the fetch time of crawler
        Output : .json file  will include all the courses informatiom
        Parameters: string, string, string, string
        Returns: None
        """
        f = open(htmlFile, "r")
        file = f.read()
        courseList = []
        self.__getContents(courseList, file)
        d = self.__deputyList(courseList)
        output = {}
        output[quarter] ={}
        output[quarter]["FetchTime"] = fetchTime
        output[quarter]["CourseData"] = d
        with open(jsonFile, 'w') as outfile:
            json.dump(output, outfile, indent=4)


